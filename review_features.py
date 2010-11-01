import re

from spellchecker import is_typo

import constants

def __fill_special_word_freq(review, key, word_set):
    """Fill `key` in `review` with the frequency of the 
    of review words that appear in `word_set`."""

    iter_matches = re.finditer("(\w+)", review['text'])
    iter_words = (m.groups()[0] for m in iter_matches)
    word_count = 0
    total_num_words = 0
    for word in iter_words:
        total_num_words += 1
        if word.lower() in word_set:
            word_count += 1
    review[key] = float(word_count) / total_num_words

def fill_gre_word_freq(review):
    __fill_special_word_freq(review, 'gre_word_freq', constants.GRE_WORDS)

def fill_sat_word_freq(review):
    __fill_special_word_freq(review, 'sat_word_freq', constants.SAT_WORDS)

def fill_review_typos(review):
    '''Fill compute the number of typos in the text of the review
    and add it to review["typos"]'''
    num_typos = 0
    words = [word.lower() for word in re.findall('\w+', review['text'])]
    for word in words:
        if is_typo(word):
            num_typos += 1
    review['typos'] = num_typos
        
def __fill_word_count(review, key):
    """The number of words in the review"""
    words=re.split('\w+',review['text'])
    review[key] = len(words)-1

def __fill_ave_words_per_sentence(review, key):
    """Average number of words per sentence"""
    body=review['text']
    words=re.split('\w+',body)
    ends = re.compile('[.!?]+')
    sentences=[m for m in ends.split(body) if len(m) > 5]
    review[key] = float(len(words)-1)/len(sentences)

def fill_word_count(review):
    __fill_word_count(review, 'word_count')

def fill_ave_words_per_sentence(review):
    __fill_ave_words_per_sentence(review, 'ave_words_per_sent')

# Fill everything
def fill_all_review_features(review):
    """Fill all review features in `review`"""
    fill_gre_word_freq(review)
    fill_sat_word_freq(review)
    fill_word_count(review)
    fill_ave_words_per_sentence(review)
    fill_review_typos(review)
