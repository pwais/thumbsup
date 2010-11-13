import re

import constants
from spellchecker import is_typo
from loader import *
from util import anew_scoring

def __fill_special_word_freq(review, key, word_set):
    """Fill `key` in `review` with the frequency of the 
    of review words that appear in `word_set`."""

    word_count = 0
    total_num_words = 0
    for word in re.findall("\w+", review['text']):
        total_num_words += 1
        if word.lower() in word_set:
            word_count += 1
    review[key] = float(word_count) / total_num_words

def fill_gre_word_freq(review):
    __fill_special_word_freq(review, 'feature_gre_word_freq', constants.GRE_WORDS)

def fill_sat_word_freq(review):
    __fill_special_word_freq(review, 'feature_sat_word_freq', constants.SAT_WORDS)

def fill_illustration_word_freq(review):
    __fill_special_word_freq(review, 'feature_illustration_word_freq', constants.ILLUSTRATION)

def fill_contrast_word_freq(review):
    __fill_special_word_freq(review, 'feature_contrast_word_freq', constants.CONTRAST)

def fill_addition_word_freq(review):
    __fill_special_word_freq(review, 'feature_addition_word_freq', constants.ADDITION)

def fill_time_word_freq(review):
    __fill_special_word_freq(review, 'feature_time_word_freq', constants.TIME)
    
def fill_space_word_freq(review):
    __fill_special_word_freq(review, 'feature_space_word_freq', constants.SPACE)

def fill_concession_word_freq(review):
    __fill_special_word_freq(review, 'feature_concession_word_freq', constants.CONCESSION)

def fill_comparison_word_freq(review):
    __fill_special_word_freq(review, 'feature_comparision_word_freq', constants.COMPARISON)

def fill_emphasis_word_freq(review):
    __fill_special_word_freq(review, 'feature_emphasis_word_freq', constants.EMPHASIS)

def fill_details_word_freq(review):
    __fill_special_word_freq(review, 'feature_details_word_freq', constants.DETAILS)

def fill_examples_word_freq(review):
    __fill_special_word_freq(review, 'feature_examples_word_freq', constants.EXAMPLES)

def fill_consequence_word_freq(review):
    __fill_special_word_freq(review, 'feature_consequence_word_freq', constants.CONSEQUENCE)

def fill_summary_word_freq(review):
    __fill_special_word_freq(review, 'feature_summary_word_freq', constants.SUMMARY)

def fill_suggestion_word_freq(review):
    __fill_special_word_freq(review, 'feature_suggestion_word_freq', constants.SUGGESTION)

def fill_review_typos(review):
    """compute the number of typos in the text of the review
    and add it to review["typos"]"""
    num_typos = 0
    words = [word.lower() for word in re.findall('\w+', review['text'])]
    for word in words:
        if is_typo(word):
            num_typos += 1
    review['feature_typos'] = num_typos
        
def fill_review_price_range(review):
    '''assign a price range between 0 (cheap) and 3
    (expensive). The category is store in review["price_range"]'''
    load_products()
    price_categories = (30,80,200)
    amazonprice = AZ_PRODUCTS[review['product_id']]['amazonprice']
    for cat,price in enumerate(price_categories):
        if amazonprice < price:
            review['feature_price_range'] = cat
            break
    else:
        review['feature_price_range'] = 3

def fill_word_count(review):
    """The number of words in the review"""
    words=re.split('\W+',review['text'])
    review['feature_word_count'] = len(words)-1

def fill_ave_words_per_sentence(review):
    """Average number of words per sentence"""
    body=review['text']
    words=re.split('\W+',body)
    ends = re.compile('[.!?]+\W+')
    sentences=[m for m in ends.split(body) if len(m) > 5]
    review['feature_ave_words_per_sent'] = float(len(words)-1)/len(sentences)

def fill_amazon_frac_voted_useful(review):
    amazon_useful = float(review.get('useful') or 0.0)
    amazon_outof = float(review.get('outof') or 0.0)
    review['feature_amazon_frac_voted_useful'] = amazon_useful / amazon_outof if amazon_outof else 0.0

def fill_all_caps_words(review):
    """Fill ALL CAPS feature"""
    body = review['text']
    words = re.split('\W+', body)
    num_all_caps = 0
    for word in words:
        if word.isupper() and len(word) > 1:
            num_all_caps += 1
    review['feature_all_caps'] = num_all_caps

def fill_capitalization_errors(review):
    """Fill Capitalization Errors"""
    body = review['text']
    words = re.split('\w+', body)
    ends = re.compile('[.!?]+\W+')
    sentences=[m for m in ends.split(body) if len(m) > 5]
    num_caps_err = 0
    for sentence in sentences:
        if not sentence[0].istitle():
            num_caps_err += 1
    review['feature_caps_err'] = num_caps_err

def fill_num_urls(review):
    """Fill number of URLs in the review text"""
    body=review['text']
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
    review['feature_num_urls'] = len(urls)

def fill_valence_score(review):
    """Fill ANEW valence weighted score"""
    review['feature_valence_score'] = anew_scoring.weighted_freq_score(re.findall("\w+", review['text']), 
                                                               'valence_mean')

def fill_arousal_score(review):
    """Fill ANEW arousal weighted score"""
    review['feature_arousal_score'] = anew_scoring.weighted_freq_score(re.findall("\w+", review['text']), 
                                                               'arousal_mean')
    
def fill_dominance_score(review):
    """Fill ANEW dominance weighted score"""
    review['feature_dominance_score'] = anew_scoring.weighted_freq_score(re.findall("\w+", review['text']), 
                                                                 'dominance_mean')

# Fill everything
def fill_all_review_features(review):
    """Fill all review features in `review`"""
    fill_gre_word_freq(review)
    fill_sat_word_freq(review)
    fill_word_count(review)
    fill_ave_words_per_sentence(review)
    fill_review_typos(review)
    fill_amazon_frac_voted_useful(review)
    fill_all_caps_words(review)
    fill_capitalization_errors(review)
    fill_num_urls(review)
    fill_valence_score(review)
    fill_arousal_score(review)
    fill_dominance_score(review)
    fill_illustration_word_freq(review)
    fill_contrast_word_freq(review)
    fill_addition_word_freq(review)
    fill_time_word_freq(review)
    fill_space_word_freq(review)
    fill_concession_word_freq(review)
    fill_comparison_word_freq(review)
    fill_emphasis_word_freq(review)
    fill_details_word_freq(review)
    fill_examples_word_freq(review)
    fill_consequence_word_freq(review)
    fill_summary_word_freq(review)
    fill_suggestion_word_freq(review)
