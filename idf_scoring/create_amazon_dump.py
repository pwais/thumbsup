"""Create a dump of category counts and reviews suitable for use with
mr_ngram_tf_idf.py.

For example, run:
python idf_scoring/create_amazon_dump.py external/amazon/reviewsTableCSV.csv external/amazon/productsTableCSV.csv experiment_data/amazon_reviews_dump.json experiment_data/amazon_product_to_cat.json experiment_data/amazon_cat_to_count.json
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
    
    reviews_in_path, products_in_path, review_dump_out_path, product_to_cats_out_path, cat_to_doc_count_out_path = sys.argv[1:]
    
    # First, build a map of document ID to categories
    product_id_to_categories = {}
    for product in csv.DictReader(open(products_in_path, 'rb')):
        product_id_to_categories[product['id']] = \
                categories.get_amazon_roots_for_cat_id(product['category_id'])
    
    simplejson.dump(product_id_to_categories, 
                    open(product_to_cats_out_path, 'wbc'), 
                    indent=2)
    
    print >>sys.stderr, "Saved product to category map to %s" % product_to_cats_out_path
    
    # Save the map of categories to product counts
    category_to_product_count = defaultdict(int)
    for product_id, cats in product_id_to_categories.iteritems():
        if not cats:
            category_to_product_count['__uncategorized'] += 1
        else:
            for cat in cats:
                category_to_product_count[cat] += 1
    
    simplejson.dump(category_to_product_count, 
                    open(cat_to_doc_count_out_path, 'wbc'), 
                    indent=2)
    
    print >>sys.stderr, "Saved category to product count to %s" % cat_to_doc_count_out_path

    
    
    # Now build the review dump
    with open(review_dump_out_path, 'wbc') as reviews_out_file:
        for review in csv.DictReader(open(reviews_in_path, 'rb')):
            print >>reviews_out_file, \
                    encode_document(review['product_id'],
                                    review['text'])

    print >>sys.stderr, "Saved review dump to %s" % review_dump_out_path