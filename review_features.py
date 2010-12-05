import itertools
import math
import re

import win32com.client, os

import constants
from spellchecker import is_typo
from util import anew_scoring
from util.loader import *

def __fill_special_word_freq(review, key, word_set):
    """Fill `key` in `review` with the frequency of the 
    of review words that appear in `word_set`."""
    word_count = 0
    total_num_words = 0
    for word in re.findall("\w+", review['text']):
        total_num_words += 1
        if word.lower() in word_set:
            word_count += 1
    if total_num_words > 0:
        review[key] = float(word_count) / total_num_words
    else:
        review[key] = 0.0

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
    """Compute the frequency of typos in the text of the review
    and add it to review["typos"]"""
    num_typos = 0
    words = [word.lower() for word in re.findall('\w+', review['text'])]
    for word in words:
        if is_typo(word):
            num_typos += 1
    review['feature_typos'] = float(num_typos) / len(words)
        
def fill_price_range(review):
    """Assign a price range between 0 (cheap) and 1 (expensive)."""

    if 'feature_price_range' in review:
        return

    def fill_amazon_price(review):
        price_scores = ((30, 0.2), (80, 0.5), (200, 0.9))
        amazonprice = int(AZ_PRODUCTS[review['product_id']]['amazonprice'])
        for price, score in price_scores:
            if amazonprice < price:
                review['feature_price_range'] = score
                break
        else:
            review['feature_price_range'] = 1.0
    
    def fill_yelp_price(review):
        try:
            yelpprice = int(YELP_BIZ_INFO[review['biz_id']]['price'])
        except Exception:
            yelpprice = 0
        review['feature_price_range'] = float(yelpprice) / 4

    if 'product_id' in review:
        fill_amazon_price(review)
    elif 'biz_id' in review:
        fill_yelp_price(review)

def fill_word_count(review):
    """The number of words in the review"""
    words = re.split('\W+',review['text'])
    review['word_count'] = len(words) - 1

def fill_ave_words_per_sentence(review):
    """Average number of words per sentence"""
    body=review['text']
    words=re.split('\W+',body)
    ends = re.compile('[.!?]+\W+')
    sentences=[m for m in ends.split(body) if len(m) > 5]
    if len(sentences) > 0:
        review['mean_words_per_sent'] = float(len(words)-1)/len(sentences)
    else:
        review['mean_words_per_sent'] = 0

def fill_ave_length_of_words(review):
    body = review['text']
    words = re.split('\W+', body)
    total_length = 0
    for word in words:
        length = len(word)
        if length > 1:
            total_length += length
    review['mean_word_length'] = float(total_length)/(review['word_count'] or 1)
            
def fill_amazon_frac_voted_useful(review):
    amazon_useful = float(review.get('useful') or 0.0)
    amazon_outof = float(review.get('outof') or 0.0)
    review['amazon_frac_voted_useful'] = amazon_useful / amazon_outof if amazon_outof else 0.0
    review['amazon_bin_voted_useful'] = int(review['amazon_frac_voted_useful'] + 0.5)

def fill_all_caps_words(review):
    """Fill ALL CAPS feature"""
    body = review['text']
    words = re.split('\W+', body)
    num_all_caps = 0
    for word in words:
        if word.isupper() and len(word) > 1:
            num_all_caps += 1
    review['feature_all_caps'] = float(num_all_caps)/(review['word_count'] or 1)

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
    review['feature_caps_err'] = float(num_caps_err)/(review['word_count'] or 1)

def fill_num_urls(review):
    """Fill number of URLs in the review text"""
    body=review['text']
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
    review['num_urls'] = len(urls)

def fill_valence_score(review):
    """Fill ANEW valence weighted score"""
    review['feature_valence_score'] = anew_scoring.weighted_normalized_freq_score(
                                                               re.findall("\w+", review['text']), 
                                                               'valence_mean')

def fill_arousal_score(review):
    """Fill ANEW arousal weighted score"""
    review['feature_arousal_score'] = anew_scoring.weighted_normalized_freq_score(
                                                               re.findall("\w+", review['text']), 
                                                               'arousal_mean')
    
def fill_dominance_score(review):
    """Fill ANEW dominance weighted score"""
    review['feature_dominance_score'] = anew_scoring.weighted_normalized_freq_score(
                                                                 re.findall("\w+", review['text']), 
                                                                 'dominance_mean')

def fill_writing_errors_using_word(review,app):
    wdDoNotSaveChanges = 0
    path = os.path.abspath('tmp/tmp'+review['id']+'.txt')
    file = open(path, 'w')
    #review['text'].decode('unicode')
    #file.write(review['text'].encode('utf-8'))
    file.write(review['text'])
    file.close()
    doc = app.Documents.Open(path)
    review['feature_grammar_err']=doc.GrammaticalErrors.Count
    review['feature_typos']=doc.SpellingErrors.Count
    app.ActiveDocument.Close(SaveChanges=False)
    #review['text'].decode('utf-8')

# Fill everything
def fill_all_review_features(review,app):
    """Fill all review features in `review`"""
    fill_word_count(review)
    fill_gre_word_freq(review)
    fill_sat_word_freq(review)
    fill_ave_words_per_sentence(review)
    #fill_review_typos(review)   TODO make this faster
    fill_writing_errors_using_word(review,app)
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
    fill_price_range(review)
    fill_ave_length_of_words(review)


##
## Sparse version of the above features
##

_WORD_SET = frozenset(itertools.chain(
                      constants.GRE_WORDS, 
                      constants.SAT_WORDS,
                      anew_scoring.ANEW_HIGH_VALENCE_WORDS,
                      anew_scoring.ANEW_LOW_VALENCE_WORDS))
_NGRAM_SET = frozenset(itertools.chain(
                       constants.ILLUSTRATION,
                       constants.CONTRAST,
                       constants.ADDITION,
                       constants.TIME,
                       constants.SPACE,
                       constants.CONCESSION,
                       constants.COMPARISON,
                       constants.EMPHASIS,
                       constants.DETAILS,
                       constants.EXAMPLES,
                       constants.CONSEQUENCE,
                       constants.SUMMARY,
                       constants.SUGGESTION))

def fill_special_word_count_sparse(review):
    
    
    if 'sparse_features' not in review:
        review['sparse_features'] = {}

    # Collect all word features
    words = [wd.lower() for wd in re.findall("\w+", review['text'])]
    for word in words:
        if word in _WORD_SET:
            review['sparse_features'].setdefault(word, 0)
            review['sparse_features'][word] += 1
    
    # Collect all ngram features
    MAX_NGRAM_LENGTH = 6
    for start in xrange(len(words)):
        for ngram_length in xrange(1, MAX_NGRAM_LENGTH + 1):
            ngram = ' '.join(words[start:start+ngram_length])
            if ngram in _NGRAM_SET and len(ngram) >= 4:
                review['sparse_features'].setdefault(ngram, 0)
                review['sparse_features'][ngram] += 1

FILL_SENT_LENGTH_MAX_SENTENCES = 20
def fill_sent_length_sparse(review):
    if 'sparse_features' not in review:
        review['sparse_features'] = {}
    
    sent_wd_counts = []
    for sent in re.split("[.!?]+", review['text']):
        sent_wd_counts.append(len(re.findall("\w+", sent)))
    
    for sent_num, wd_count in enumerate(sent_wd_counts[:FILL_SENT_LENGTH_MAX_SENTENCES]):
        key = 'f_sent_%s_wd_count' % sent_num
        review['sparse_features'][key] = wd_count

def _fill_copy_feature_to_sparse(review, fill_method, key):
    if 'sparse_features' not in review:
        review['sparse_features'] = {}
    
    fill_method(review)
    
    sparse_key = 'f_%s' % key
    review['sparse_features'][sparse_key] = review[key]

def fill_all_sparse_features(review):
    fill_word_count(review)
    fill_special_word_count_sparse(review)
    fill_sent_length_sparse(review)
    
    _fill_copy_feature_to_sparse(review, fill_num_urls, 'num_urls')
    _fill_copy_feature_to_sparse(review, fill_capitalization_errors, 'feature_caps_err')
    _fill_copy_feature_to_sparse(review, fill_all_caps_words, 'feature_all_caps')
    _fill_copy_feature_to_sparse(review, fill_ave_length_of_words, 'mean_word_length')
    _fill_copy_feature_to_sparse(review, fill_price_range, 'feature_price_range')
