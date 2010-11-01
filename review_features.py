import re

import sat_gre_words

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
	__fill_special_word_freq(review, 'gre_word_freq', sat_gre_words.GRE_WORDS)

def fill_sat_word_freq(review):
	__fill_special_word_freq(review, 'sat_word_freq', sat_gre_words.SAT_WORDS)


def fill_review_features(review):
	"""Fill all review features in `review`"""
	fill_gre_word_freq(review)
	fill_sat_word_freq(review)

def word_count(feature):
    """The number of words in the review"""
    words=re.split('\w+',body)
    return len(words)-1

def ave_words_per_sentence(feature):
    """Average number of words per sentence"""
    body=feature['text']
    words=re.split('\w+',body)
    ends = re.compile('[.!?]+')
    sentences = ends.split(body)
    sentences=[m for m in sentences if len(m) > 5]
    return float(len(words)-1)/len(sentences)

