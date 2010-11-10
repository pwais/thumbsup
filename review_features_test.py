import random
import unittest

from review_features import *
from util import anew_scoring

test_review = {}
# review with 6 typos.
test_review['text'] = '''Brand new owner, brand new wine lis, brand
new feeel. GO check it out at http://www.iloveboobs.com ! Have the cheeze appetizer. i forjet what
it's callede. But it was AMAZING! give it a try and I promese you WILL
be BACK. '''

class FeaturesTests(unittest.TestCase):

    def test_is_typo(self):
        # edit distance 1
        assert is_typo('speling') == True # delete
        assert is_typo('spelilng') == True # swap
        assert is_typo('spellling') == True # insert
        assert is_typo('spellimg') == True # replace
        # edit distance 2
        assert is_typo('speing') == True # delete
        assert is_typo('spelilgn') == True # swap
        assert is_typo('spelllling') == True # insert
        assert is_typo('sbellimg') == True # replace
        # edit distance 3 or more - false
        assert is_typo('spelling') == False    # correct
        assert is_typo('pselilgn') == False # swap
        assert is_typo('spellllling') == False # insert
        assert is_typo('zbellimg') == False # replace

    def test_fill_review_typos(self):
        fill_review_typos(test_review)
        assert test_review['typos'] == 6

    def test_fill_price_range(self):
        # numbers from the data
        price_categories = [(28830,0),(43,1),(2,2),(1,3)]
        for pid,cat in price_categories:
            review = {'product_id':pid}
            fill_review_price_range(review)
            assert review['price_range'] == cat

    def test_fill_num_urls(self):
        fill_num_urls(test_review)
        assert test_review['num_urls'] == 1
        
    def test_fill_all_caps(self):
        fill_all_caps_words(test_review)
        assert test_review['all_caps'] == 4

    def test_word_count(self):
        fill_word_count(test_review)
        assert test_review['word_count'] == 44

    def test_fill_capitalization_errors(self):
        fill_capitalization_errors(test_review)
        assert test_review['caps_err'] == 2
    
    def test_anew_scoring(self):
        fill_valence_score(test_review)
        fill_arousal_score(test_review)
        fill_dominance_score(test_review)
        # The test review contains only one valence word
        assert test_review['valence_score'] == anew_scoring.ANEW_WORD_MAP['wine']['valence_mean']
        assert test_review['arousal_score'] == anew_scoring.ANEW_WORD_MAP['wine']['arousal_mean']
        assert test_review['dominance_score'] == anew_scoring.ANEW_WORD_MAP['wine']['dominance_mean']

class LoaderTests(unittest.TestCase):

    def test_load_products(self):
        '''Assumes amazon data for now'''
        load_products()
        assert AZ_PRODUCTS
        for key in AZ_PRODUCTS.iterkeys():
            assert type(key) == int
            assert type(AZ_PRODUCTS[key]['amazonprice'])==float 

if __name__ == '__main__':
    unittest.main()
