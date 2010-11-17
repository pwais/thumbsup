import csv
import os
import sys

import simplejson

from review_features import fill_all_review_features

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
    else:
        streamer = stream_reviews_from_json
    
    review_keys = None
    feature_keys = None

    header = True
    for review in streamer():
        if review_keys is None:
            review_keys = set(review.keys())

        fill_all_review_features(review)

        if feature_keys is None:
            feature_keys = set(review.keys()) - review_keys

        for key in review_keys:
            if key != 'id':
                del review[key]
        
        if header:
            print >>sys.stdout, ",".join(feature_keys)
            header = False
		
        print >>sys.stdout, ",".join(str(review[k]) for k in feature_keys)
