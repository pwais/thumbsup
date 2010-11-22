
import unittest

import reviews_features

class ReviewsFeaturesTest(unittest.TestCase):
    
    def test_fill_percentile(self):
        
        mock_fill_key = 'test_percentile'
        mock_feature_key = 'test_feature'
        
        values = [1, 1, 1, 4, 5, 6, 6, 8, 9, 10]
        mock_reviews = [{mock_feature_key: v} for v in values]
        
        reviews_features._fill_percentile(mock_reviews, mock_fill_key, mock_feature_key)
        
        percentiles = [r[mock_fill_key] for r in mock_reviews]
        
        self.assertEqual(percentiles, [10, 10, 10, 40, 50, 60, 60, 80, 90, 100])

if __name__ == '__main__':
    unittest.main()
