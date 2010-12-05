"""Given a stream of reviews (i.e. document JSON objects), calculate the IDF 
(broken down by category) of all n-grams in the reviews.

Loosely based upon the MRTextClassifier mrjob example.

Try, for example:
head -n 100 experiment_data/yelp_reviews_dump.json | python idf_scoring/mr_ngram_tf_idf.py --cats-to-num-docs=experiment_data/yelp_cat_to_count.json --doc-to-cats=experiment_data/yelp_biz_to_cats.json
"""

import math
import re
import os

import simplejson

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

WORD_RE = re.compile(r"[\w'-]+", re.UNICODE)

STOP_WORDS = frozenset(['a', 'about', 'also', 'am', 'an', 'and', 'any', 'are', 'as', 
'at', 'be', 'but', 'by', 'can', 'com', 'did', 'do', 'does', 'for', 'from', 'had', 'has', 
'have', 'he', "he'd", "he'll", "he's", 'her', 'here', 'hers', 'him', 'his', 'i', "i'd", 
"i'll", "i'm", "i've", 'if', 'in', 'into', 'is', 'it', "it's", 'its', 'just', 'me', 'mine', 
'my', 'of', 'on', 'or', 'org', 'our', 'ours', 'she', "she'd", "she'll", "she's", 'some', 'than', 
'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', "they'd", "they'll", "they're", 
'this', 'those', 'to', 'us', 'was', 'we', "we'd", "we'll", "we're", 'were', 'what', 'where', 
'which', 'who', 'will', 'with', 'would', 'you', 'your', "you're", 'yours',

'all', 'yes'])

STOP_NGRAMS = frozenset([])

def encode_document(doc_id, text):
    """Encode a document as a JSON dictionary so that MRNgramIDFUtility can read it.
    We intend to use `doc_id` as a business/product/entity ID rather than the ID of
    an individual review."""
    
    #text = unicode(text) RAWR some amazon reviews won't encode
    return JSONValueProtocol.write(
        None, {'doc_id': doc_id, 'text': text})

class MRNgramIDFUtility(MRJob):
    DEFAULT_INPUT_PROTOCOL = 'json_value'

    def __init__(self, *args, **kwargs):
        super(MRNgramIDFUtility, self).__init__(*args, **kwargs)
    
    def configure_options(self):
        """Add command line options specific to this script"""
        super(MRNgramIDFUtility, self).configure_options()
        
        self.add_file_option(
            '--cats-to-num-docs', dest='cats_to_num_docs',
            help="Path to a JSON file containing a map of categories to doc counts")
        self.add_file_option(
            '--doc-to-cats', dest='doc_to_cats',
            help="Path to a JSON file containing a map of doc IDs to categories")
        self.add_passthrough_option(
            '--min-gram-length', dest='min_ngram_length', type='int', default=1,
            help="Minimum ngram length [default=%default]")
        self.add_passthrough_option(
            '--max-gram-length', dest='max_ngram_length', type='int', default=5,
            help="Maximum ngram length [default=%default]")

    def steps(self):
        return [self.mr(self.generate_ngrams, self.calculate_idf)]

    ### Lazy-load all reference files
    
    @property
    def cats_to_num_docs(self):
        if not hasattr(self, '_cats_to_num_docs'):
            self._cats_to_num_docs = simplejson.load(
                                            open(self.options.cats_to_num_docs, 'rb'))
        return self._cats_to_num_docs
    
    @property
    def doc_to_cats(self):
        if not hasattr(self, '_doc_to_cats'):
            self._doc_to_cats = simplejson.load(
                                            open(self.options.doc_to_cats, 'rb'))
        return self._doc_to_cats
    
    @property
    def total_num_docs(self):
        return len(self.doc_to_cats)

    def generate_ngrams(self, _, doc):
        """Yield a stream of ngrams from the reviews in the given `doc`"""
        
        # Extract words from the review
        words = []
        for wd in re.findall(WORD_RE, doc['text']):
            wd = wd.lower()
            if wd in STOP_WORDS:
                continue
            wd = wd.replace("'", "")
            wd = wd.replace("-", "")
            wd = wd.replace("_", "")
            if len(wd) <= 2:
                continue
            if re.match('\d+', wd):
                continue
            words.append(wd)

        # Now emit all ngrams
        ngram_lengths = range(self.options.min_ngram_length, 
                              self.options.max_ngram_length + 1)

        for start in xrange(len(words)):
            for ngram_length in ngram_lengths:
                ngram = ' '.join(words[start:start+ngram_length])
                if ngram not in STOP_NGRAMS:
                    yield ngram, doc['doc_id']
    
    def calculate_idf(self, ngram, doc_ids):
        """Yield IDF values for the ngram over all documents as well as
        documents broken down by category"""
        
        def idf(total_num_docs, num_matching_docs):
            return math.log(float(total_num_docs) / num_matching_docs)
        
        # Tally up matching docs by categories
        cat_to_doc_count = dict((cat, 0) for cat in self.cats_to_num_docs.iterkeys())
        total_num_matching_docs = 0
        for doc_id in doc_ids:
            for cat in self.doc_to_cats[doc_id]:
                cat_to_doc_count[cat] += 1
            total_num_matching_docs += 1
        
        yield ngram, ('overall', idf(self.total_num_docs, total_num_matching_docs))
        
        for cat, doc_count in cat_to_doc_count.iteritems():
            if doc_count > 0:
                yield ngram, (cat, 
                              idf(self.cats_to_num_docs.get(cat, 0), 
                                  doc_count))

if __name__ == '__main__':
    MRNgramIDFUtility.run()
