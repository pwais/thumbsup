import csv
import os
import sys
import win32com.client
import simplejson

from review_features import fill_all_review_features
from reviews_features import fill_all_reviews_features

def stream_reviews_from_csv():
    for review in csv.DictReader(sys.stdin):
        yield review

def stream_reviews_from_json():
    review_data = simplejson.load(sys.stdin)
    for review in review_data:
        yield review

def exportable_key(key):
    return key.startswith('feature') or key.startswith('label') or key == 'id'

if __name__ == '__main__':
    source = sys.argv[1]
    if source == 'csv':
        streamer = stream_reviews_from_csv
    else:
        streamer = stream_reviews_from_json
    
    review_keys = None
    feature_keys = None

    reviews = []
    app = win32com.client.gencache.EnsureDispatch('Word.Application')
    for review in streamer():
        
        # Record non-feature keys
        if review_keys is None:
            review_keys = set(review.keys())

        fill_all_review_features(review, app)
        reviews.append(review)
    
    print >>sys.stderr, "Read all reviews"
    app.Quit()    
    fill_all_reviews_features(reviews)

    print >>sys.stdout, ",".join(k for k in review.keys() if exportable_key(k))
    for review in reviews:
        print >>sys.stdout, ",".join(str(review[k]) for k in review.keys()
                                     if exportable_key(k))
