import re
import constants
from spellchecker import is_typo
from loader import *

def __fill_special_word_freq(review, key, word_set):
    """Fill `key` in `review` with the frequency of the 
    of review words that appear in `word_set`."""

    word_count = 0
    total_num_words = 0
    for word in re.finditer("\w+", review['text']):
        total_num_words += 1
        if word.lower() in word_set:
            word_count += 1
    review[key] = float(word_count) / total_num_words

def fill_gre_word_freq(review):
    __fill_special_word_freq(review, 'gre_word_freq', constants.GRE_WORDS)

def fill_sat_word_freq(review):
    __fill_special_word_freq(review, 'sat_word_freq', constants.SAT_WORDS)

def fill_review_typos(review):
    """compute the number of typos in the text of the review
    and add it to review["typos"]"""
    num_typos = 0
    words = [word.lower() for word in re.findall('\w+', review['text'])]
    for word in words:
        if is_typo(word):
            num_typos += 1
    review['typos'] = num_typos
        
def fill_review_price_range(review):
    '''assign a price range between 0 (cheap) and 3
    (expensive). The category is store in review["price_range"]'''
    load_products()
    price_categories = (30,80,200)
    amazonprice = AZ_PRODUCTS[review['product_id']]['amazonprice']
    for cat,price in enumerate(price_categories):
        if amazonprice < price:
            review['price_range'] = cat
            break
    else:
        review['price_range'] = 3

def __fill_word_count(review, key):
    """The number of words in the review"""
    words=re.split('\W+',review['text'])
    review[key] = len(words)-1

def __fill_ave_words_per_sentence(review, key):
    """Average number of words per sentence"""
    body=review['text']
    words=re.split('\W+',body)
    ends = re.compile('[.!?]+\W+')
    sentences=[m for m in ends.split(body) if len(m) > 5]
    review[key] = float(len(words)-1)/len(sentences)

def __fill_all_caps_words(review, key):
    """Fill ALL CAPS feature"""
    body=review['text']
    words=re.split('\W+',body)
    num_all_caps = 0
    for word in words:
        if word.isupper() and len(word) > 1:
            num_all_caps += 1
    review[key] = num_all_caps

def __fill_capitalization_errors(review, key):
    """Fill Capitalization Errors"""
    body=review['text']
    words=re.split('\w+',body)
    ends = re.compile('[.!?]+\W+')
    sentences=[m for m in ends.split(body) if len(m) > 5]
    num_caps_err = 0
    for sentence in sentences:
        if not sentence[0].istitle():
            num_caps_err += 1
    review[key] = num_caps_err

def __fill_num_urls(review, key):
    """Fill number of URLs in the review text"""
    body=review['text']
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
    review[key] = len(urls)

def fill_word_count(review):
    __fill_word_count(review, 'word_count')

def fill_ave_words_per_sentence(review):
    __fill_ave_words_per_sentence(review, 'ave_words_per_sent')

def fill_amazon_frac_voted_useful(review):
    amazon_useful = float(review.get('useful') or 0.0)
    amazon_outof = float(review.get('outof') or 0.0)
    review['amazon_frac_voted_useful'] = amazon_useful / amazon_outof if amazon_outof else 0.0

def fill_all_caps_words(review):
    __fill_all_caps_words(review, 'all_caps')

def fill_capitalization_errors(review):
    __fill_capitalization_errors(review, 'caps_err')

def fill_num_urls(review):
    __fill_num_urls(review, 'num_urls')

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
