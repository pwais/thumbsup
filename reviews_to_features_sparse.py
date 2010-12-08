"""Given a stream of reviews on stdin, write sparse review features to stdout
 
Example:
python reviews_to_features_sparse.py json l1 yelp label_useful_extreme_percentile < external/yelp/review_dump_11-4-2010.json > experiment_data/yelp_sparse_features.csv 
head -n 15000 external/amazon/reviewsTableCSV.csv | python reviews_to_features_sparse.py csv l1 amazon label_useful_extreme_percentile > experiment_data/amazon_features_sparse.csv
"""
import csv
import itertools
import os
import sys

import simplejson

import review_features
import reviews_features
from util import idf
from util import typos

def stream_reviews_from_csv():
    for review in csv.DictReader(sys.stdin):
        yield review

def stream_reviews_from_json():
    review_data = simplejson.load(sys.stdin)
    for review in review_data:
        yield review

if __name__ == '__main__':
    source = sys.argv[1]
    if source == 'csv':
        streamer = stream_reviews_from_csv
    elif source == 'json':
        streamer = stream_reviews_from_json
    
    normalize = sys.argv[2]
    normalize_overall = False
    if normalize == 'scores':
        normalizer = reviews_features.normalize_sparse_features
        normalize_overall = True
    elif normalize == 'l1':
        normalizer = reviews_features.l1_normalize_sparse_features
    elif normalize == 'l2':
        normalizer = reviews_features.l2_normalize_sparse_features
    
    source = sys.argv[3]
    if source == 'amazon':
        fill_idf_feature = idf.fill_amazon_idf_feature_sparse
        fill_typos_feature = typos.fill_amazon_typo_feature
    elif source == 'yelp':
        fill_idf_feature = idf.fill_yelp_idf_feature_sparse
        fill_typos_feature = typos.fill_yelp_typo_feature
    
    label_key = sys.argv[4]
    
    all_sparse_feature_keys = set()
    reviews = []
    for review in streamer():
        if not review['text']:
            continue
        
        review_features.fill_all_sparse_features(review)
        fill_idf_feature(review)
        fill_typos_feature(review)
        
        if not normalize_overall:
            normalizer(review)
        
        all_sparse_feature_keys.update(review['sparse_features'].keys())
        reviews.append(review)
    
    print >>sys.stderr, "Computed all review features"
    
    if normalize_overall:
        normalize(reviews)
    
    reviews_features.fill_all_reviews_features_sparse(reviews)

    print >>sys.stderr, "Starting to write out feature CSV"

    all_sparse_feature_keys = list(all_sparse_feature_keys)
    print >>sys.stdout, ",".join(all_sparse_feature_keys + [label_key])
    for rev_idx, review in enumerate(reviews):
        if review[label_key] is None:
            continue

        print >>sys.stdout, ",".join(
                                  itertools.chain(
                                        (str(review['sparse_features'].get(k, '')) 
                                         for k in all_sparse_feature_keys),
                                        iter([str(review[label_key])])))

        print >>sys.stderr, "Finished review %s" % rev_idx

