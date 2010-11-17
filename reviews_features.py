"""Features that require iterating over all reviews"""

import bisect

def _fill_percentile(reviews, fill_key, feature_key, default=0.0):
    sorted_values = sorted(review.get(feature_key, default) for review in reviews)
    for review in reviews:
        idx = bisect.bisect_left(sorted_values, review.get(feature_key, default))
        review[fill_key] = 100.0 * (idx + 1) / len(sorted_values)

def fill_amazon_useful_percentile(reviews):
    _fill_percentile(reviews, 'amazon_useful_percentile', 'useful')

def fill_yelp_useful_percentile(reviews):
    _fill_percentile(reviews, 'yelp_useful_percentile', 'u_count')

def fill_all_reviews_features(reviews):
    """Fill everything"""
    fill_amazon_useful_percentile(reviews)
    fill_yelp_useful_percentile(reviews)
