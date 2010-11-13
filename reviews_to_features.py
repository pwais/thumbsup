import csv
import os
import sys

from review_features import fill_all_review_features

if __name__ == '__main__':
    
    review_keys = None
    feature_keys = None

	header = True
    for review in csv.DictReader(sys.stdin):
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
		
        print >>sys.stdout, ",".join(review[k] for k in feature_keys)
