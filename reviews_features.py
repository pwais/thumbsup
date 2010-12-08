"""Features that require iterating over all reviews"""

import bisect
import math

import config
from review_features import FILL_SENT_LENGTH_MAX_SENTENCES

def _fill_percentile(reviews, fill_key, feature_key, default=0.0):
    sorted_values = sorted(review.get(feature_key, default) for review in reviews)
    for review in reviews:
        idx = bisect.bisect_left(sorted_values, review.get(feature_key, default))
        review[fill_key] = 100.0 * (idx + 1) / len(sorted_values)

def _fill_normalized(reviews, fill_key, feature_key):
    max_feat_val = float(max(review.get(feature_key, 0) for review in reviews))
    for review in reviews:
        review[fill_key] = review[feature_key] / max_feat_val if max_feat_val != 0 else 0

def fill_useful_percentile(reviews):
    if 'useful' in reviews[0]:
        _fill_percentile(reviews, 'useful_percentile', 'useful')
    elif 'u_count' in reviews[0]:
        _fill_percentile(reviews, 'useful_percentile', 'u_count')
    else:
        raise ValueError(reviews[0]) # wtf?

def fill_useful_above_median(reviews):
    for review in reviews:
        review['label_upper_median'] = str(review['useful_percentile'] >= 50)

def fill_useful_extreme_percentile(reviews):
    for review in reviews:
        if review['useful_percentile'] >= config.USEFUL_MIN_PERCENTILE:
            review['label_useful_extreme_percentile'] = True
        elif review['useful_percentile'] <= config.NONUSEFUL_MAX_PERCENTILE:
            review['label_useful_extreme_percentile'] = False
        else:
            # Dump scripts should skip examples with 'None' as a label
            review['label_useful_extreme_percentile'] = None

def fill_normalized_word_count(reviews):
    _fill_normalized(reviews, 'feature_normalized_word_count', 'word_count')

def fill_all_mean_words_per_sentence(reviews):
    _fill_normalized(reviews, 'feature_normalized_mean_wds_per_sentence', 'mean_words_per_sent')

def fill_all_mean_length_of_words(reviews):
    _fill_normalized(reviews, 'feature_normalized_mean_wd_length', 'mean_word_length')

def fill_normalized_url_count(reviews):
    _fill_normalized(reviews, 'feature_normalized_url_count', 'num_urls')

def _fill_percentile_geq_75th(reviews, key):
    for review in reviews:
        review['percentile_geq_75th'] = bool(review[key] >= 75)

def fill_all_reviews_features(reviews):
    """Fill everything"""
    fill_useful_percentile(reviews)
    fill_useful_extreme_percentile(reviews)
    fill_normalized_word_count(reviews)
    fill_all_mean_words_per_sentence(reviews)
    fill_all_mean_length_of_words(reviews)
    fill_normalized_url_count(reviews)
#    fill_useful_above_median(reviews)

##
## Sparse features
##

def _normalize_sparse_feature(reviews, feature_key):
    max_feat_val = float(max(review['sparse_features'].get(feature_key, 0) 
                             for review in reviews))
    for review in reviews:
        if feature_key in review['sparse_features']:
            review['sparse_features'][feature_key] /= max_feat_val

def normalize_sparse_features(reviews):
    _normalize_sparse_feature(reviews, 'f_feature_caps_err')
    _normalize_sparse_feature(reviews, 'f_feature_all_caps')
    _normalize_sparse_feature(reviews, 'f_mean_word_length')
    _normalize_sparse_feature(reviews, 'f_feature_price_range')
    
    for sent_num in xrange(FILL_SENT_LENGTH_MAX_SENTENCES):
        key = 'f_sent_%s_wd_count' % sent_num
        _normalize_sparse_feature(reviews, key)

def l1_normalize_sparse_features(review):
    vec_len = float(sum(abs(v) for v in review['sparse_features'].itervalues()))
    for key in review['sparse_features'].iterkeys():
        review['sparse_features'][key] /= vec_len

def l2_normalize_sparse_features(review):
    vec_len = float(math.sqrt(sum(v ** 2 for v in review['sparse_features'].itervalues())))
    for key in review['sparse_features'].iterkeys():
        review['sparse_features'][key] /= vec_len

def fill_all_reviews_features_sparse(reviews):
    """Fill everything"""
    fill_useful_percentile(reviews)
    fill_useful_extreme_percentile(reviews)
