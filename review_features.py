import re

import sat_gre_words

def __fill_special_word_count(review, key, word_set):
	"""Fill `key` in `review` with a count of the number
	of review words that appear in `word_set`."""

	iter_matches = re.finditer("(\w+)", review['text'])
	iter_words = (m.groups()[0] for m in iter_matches)
	review[key] = sum(1 for word in iter_words
						if word.lower() in word_set)

def fill_gre_word_count(review):
	__fill_special_word_count(review, 'gre_word_count', sat_gre_words.GRE_WORDS)

def fill_sat_word_count(review):
	__fill_special_word_count(review, 'sat_word_count', sat_gre_words.SAT_WORDS)


def fill_review_features(review):
	"""Fill all review features in `review`"""
	fill_gre_word_count(review)
	fill_sat_word_count(review)

