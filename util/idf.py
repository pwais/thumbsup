import os
import re
import sys

import simplejson

import config

# Load the idf features from an external source
YELP_IDF_MAP = simplejson.load(open(config.YELP_IDF_PATH))
AMAZON_IDF_MAP = simplejson.load(open(config.AZ_IDF_PATH))

print >>sys.stderr, "Loaded idf feature data"

# ngrams with idf score above these thresholds are too sparse to be useful.  These
# are manually-determined 90th percentiles (or so).. should probably automate this part :)
YELP_MAX_IDF = 8.0
AMAZON_MAX_IDF = 11.2

MAX_NGRAM_LENGTH = 5

MAX_NUM_IDF_FEATS = 10

def get_top_ngram_idfs(review, idf_map, max_idf, category='overall'):
    words = [wd.lower() for wd in re.findall("\w+", review['text'])]
    ngram_to_idf = {}
    for start in xrange(len(words)):
        for ngram_length in xrange(1, MAX_NGRAM_LENGTH + 1):
            ngram = ' '.join(words[start:start+ngram_length])
            if ngram in idf_map and idf_map[ngram]['overall'] <= max_idf and len(ngram) >= 4:
                ngram_to_idf[ngram] = idf_map[ngram]['overall']
    
    # Grab the top ten idf-scoring ngrams
    top_ngram_idf = sorted(ngram_to_idf.iteritems(), key=lambda e: -1*e[1])[:MAX_NUM_IDF_FEATS]
    return top_ngram_idf

def __fill_idf_feature_sparse(review, idf_map, max_idf, category='overall'):
    top_ngram_idf = get_top_ngram_idfs(review, idf_map, max_idf, category=category)
    for ngram, idf in top_ngram_idf:
        review['sparse_features']['f_idf_%s' % ngram] = idf

def __fill_idf_feature_dense(review, idf_map, max_idf, category='overall', key='feature_idf'):
    top_ngram_idf = get_top_ngram_idfs(review, idf_map, max_idf, category=category)
    review[key] = sum(idf for ngram, idf in top_ngram_idf)

def fill_amazon_idf_feature_sparse(review):
    __fill_idf_feature_sparse(review, AMAZON_IDF_MAP, AMAZON_MAX_IDF)

def fill_yelp_idf_feature_sparse(review):
    __fill_idf_feature_sparse(review, YELP_IDF_MAP, YELP_MAX_IDF)

def fill_amazon_idf_feature(review):
    __fill_idf_feature_dense(review, AMAZON_IDF_MAP, AMAZON_MAX_IDF)

def fill_yelp_idf_feature(review):
    __fill_idf_feature_dense(review, YELP_IDF_MAP, YELP_MAX_IDF)


