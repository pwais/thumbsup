import os
import sys

import simplejson

import config

# Load the typo features from an external source
YELP_TYPO_FEATURES = simplejson.load(open(config.YELP_TYPOS_PATH))
AMAZON_TYPO_FEATURES = simplejson.load(open(config.AZ_TYPOS_PATH))

print >>sys.stderr, "Loaded typo feature data"

def fill_amazon_typo_feature(review):
    review.update(AMAZON_TYPO_FEATURES[int(review['id'])-1])

def fill_yelp_typo_feature(review):
    review.update(YELP_TYPO_FEATURES[review['id']])
