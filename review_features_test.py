import random
import unittest

from review_features import *

test_review = {}
# review with 6 typos.
test_review['text'] = '''Brand new owner, brand new wine lis, brand
new feeel. Go check it out! Have the cheeze appetizer. I forjet what
it's callede. But it was amazing! Give it a try and I promese you will
be back.'''

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

    def test_fill_price_category(self):
        # number from the data
        price_categories = [(28830,0),(43,1),(2,2),(1,3)]
        for pid,cat in price_categories:
            review = {'product_id':pid}
            fill_review_price_category(review)
            assert review['price_cat'] == cat

class LoaderTests(unittest.TestCase):

    def test_load_products(self):
        pass

if __name__ == '__main__':
    unittest.main()
