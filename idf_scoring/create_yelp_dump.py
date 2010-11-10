"""Create a dump of category counts and reviews suitable for use with
mr_ngram_tf_idf.py.

For example, run:
python idf_scoring/create_yelp_dump.py external/yelp/review_dump_11-4-2010.json external/yelp/biz_dump_11-4-2010.json experiment_data/yelp_reviews_dump.json experiment_data/yelp_biz_to_cats.json experiment_data/yelp_cat_to_count.json
"""

from __future__ import with_statement

import csv
import os
import sys
from collections import defaultdict

import simplejson

from idf_scoring.mr_ngram_tf_idf import encode_document
from util import categories

if __name__ == '__main__':
    
    reviews_in_path, business_in_path, review_dump_out_path, biz_to_cats_out_path, cat_to_biz_count_out_path = sys.argv[1:]
    
    # Save a map of biz ID to categories
    biz_id_to_categories = {}
    for business in simplejson.load(open(business_in_path, 'rb')):
        roots = set()
        for cat in business['categories']:
            roots.update(categories.get_yelp_roots_for_cat(cat))
        biz_id_to_categories[business['id']] = list(roots)
    
    simplejson.dump(biz_id_to_categories,
                    open(biz_to_cats_out_path, 'wbc'),
                    indent=2)
   
    print >>sys.stderr, "Saved biz to category map to %s" % biz_to_cats_out_path
    
    
    
    # Save the map of categories to biz counts
    category_to_biz_count = defaultdict(int)
    for biz_id, cats in biz_id_to_categories.iteritems():
        if not cats:
            category_to_biz_count['__uncategorized'] += 1
        else:
            for cat in cats:
                category_to_biz_count[cat] += 1
    
    simplejson.dump(category_to_biz_count, 
                    open(cat_to_biz_count_out_path, 'wbc'), 
                    indent=2)
    
    print >>sys.stderr, "Saved category to biz count to %s" % cat_to_biz_count_out_path

    
    
    # Now build the review dump
    with open(review_dump_out_path, 'wbc') as reviews_out_file:
        for review in simplejson.load(open(reviews_in_path, 'rb')):
            print >>reviews_out_file, \
                    encode_document(review['biz_id'],
                                    review['text'])
    print >>sys.stderr, "Saved review dump to %s" % review_dump_out_path