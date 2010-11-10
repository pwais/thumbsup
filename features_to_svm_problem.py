"""
Script to convert JSON features file to an svm_light-compatible input file.

Example:
    python features_to_svm_problem < features.json > svm_problem.txt
"""

import sys

import simplejson

LABEL_FEATURE = 'amazon_frac_voted_useful'
INPUT_FEATURES = ('gre_word_freq',
                  'sat_word_freq',
                  'ave_words_per_sent',
                  'word_count',
                  'typos')

if __name__ == '__main__':
    feature_rows = []
    for line in sys.stdin:
        feature_rows.append(simplejson.loads(line.strip()))
    
    def to_svm_input_line(feature_row):
        label = str(2*int(feature_row[LABEL_FEATURE] > 0.5) - 1)
        values = []
        for key_idx, key in enumerate(INPUT_FEATURES):
            values.append("%s:%s" % (key_idx + 1, feature_row[key]))
        return ' '.join([label] + values)
    
    for feature_row in feature_rows:
        print >>sys.stdout, to_svm_input_line(feature_row)