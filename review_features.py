import re
from spellchecker import known_edits2, DICTIONARY
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

# Typo helper functions
def is_typo(word):
	'''A word is considered a typo whenever it not in the
	dictionary AND another word that is at edit-distance of 2 or
	less is in the dictionary.'''
	if not word in DICTIONARY and known_edits2(word):
		return True
	return False

def fill_review_typos(review):
	'''Fill compute the number of typos in the text of the review
	and add it to review["typos"]'''
	num_typos = 0
	words = [word.lower() for word in re.findall('\w+', review['text'])]
	for word in words:
		if is_typo(word):
			num_typos += 1
	review['typos'] = num_typos
		
def fill_all_review_features(review):
	"""Fill all review features in `review`"""
	fill_gre_word_freq(review)
	fill_sat_word_freq(review)

