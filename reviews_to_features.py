import csv
import itertools
import os
import sys

import simplejson

from review_features import fill_all_review_features
from reviews_features import fill_all_reviews_features
from util import idf
from util import typos

def stream_reviews_from_csv():
    for review in csv.DictReader(sys.stdin):
        yield review

def stream_reviews_from_json():
    review_data = simplejson.load(sys.stdin)
    for review in review_data:
        yield review

def exportable_key(key):
    return key.startswith('feature')

if __name__ == '__main__':
    source = sys.argv[1]
    if source == 'csv':
        streamer = stream_reviews_from_csv
    else:
        streamer = stream_reviews_from_json

    source = sys.argv[2]

    review_keys = None
    feature_keys = None

    reviews = []
    for review in streamer():
        
        # Record non-feature keys
        if review_keys is None:
            review_keys = set(review.keys())

        fill_all_review_features(review)
        if source == 'amazon':
            fill_idf_feature = idf.fill_amazon_idf_feature
            fill_typos_feature = typos.fill_amazon_typo_feature
        elif source == 'yelp':
            fill_idf_feature = idf.fill_yelp_idf_feature
            fill_typos_feature = typos.fill_yelp_typo_feature

        fill_idf_feature(review)
        fill_typos_feature(review)

        reviews.append(review)
    
    print >>sys.stderr, "Read all reviews"
    
    fill_all_reviews_features(reviews)
    
    num_pos = 0
    num_neg = 0
    for review in reviews:
        if review.get('label_useful_extreme_percentile') == True:
            num_pos += 1
        elif review.get('label_useful_extreme_percentile') == False:
            num_neg += 1
    print >>sys.stderr, "Got %s positive examples and %s negative examples" % (num_pos, num_neg)

    print >>sys.stdout, ",".join(k for k in review.keys() if exportable_key(k))
    for review in reviews:
        if review.get('label_useful_extreme_percentile') is not None:
            # Weka uses the last feature as the label by convention
            print >>sys.stdout, ",".join(
                                      itertools.chain((str(review[k]) for k in review.keys()
                                                       if exportable_key(k)),
                                                      iter([review['label_useful_extreme_percentile']])))
