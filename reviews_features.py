"""Features that require iterating over all reviews"""

import bisect

def _fill_percentile(reviews, fill_key, feature_key, default=0.0):
    sorted_values = sorted(review.get(feature_key, default) for review in reviews)
    for review in reviews:
        idx = bisect.bisect_left(sorted_values, review.get(feature_key, default))
        review[fill_key] = 100.0 * (idx + 1) / len(sorted_values)

def _fill_normalized(reviews, fill_key, feature_key):
    max_feat_val = float(max(review.get(feature_key, 0) for review in reviews))
    for review in reviews:
        review[fill_key] = review[feature_key] / max_feat_val

def fill_useful_percentile(reviews):
    if 'useful' in reviews[0]:
        _fill_percentile(reviews, 'useful_percentile', 'useful')
    elif 'u_count' in reviews[0]:
        _fill_percentile(reviews, 'useful_percentile', 'u_count')

def fill_useful_above_75th(reviews):
    for review in reviews:
        review['label_upper_quartile'] = str(review['useful_percentile'] >= 80)

def fill_normalized_word_count(reviews):
    _fill_normalized(reviews, 'feature_normalized_word_count', 'word_count')

def fill_all_mean_words_per_sentence(reviews):
    _fill_normalized(reviews, 'feature_normalized_mean_wds_per_sentence', 'mean_words_per_sent')

def fill_all_mean_length_of_words(reviews):
    _fill_normalized(reviews, 'feature_normalized_mean_wd_length', 'mean_word_length')

def fill_normalized_url_count(reviews):
    _fill_normalized(reviews, 'feature_normalized_url_count', 'num_urls')

def fill_all_reviews_features(reviews):
    """Fill everything"""
    fill_useful_percentile(reviews)
    fill_normalized_word_count(reviews)
    fill_all_mean_words_per_sentence(reviews)
    fill_all_mean_length_of_words(reviews)
    fill_normalized_url_count(reviews)
    fill_useful_above_75th(reviews)
