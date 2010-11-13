"""
Script to convert JSON features file to an svm_light-compatible input file.

Example:
    python features_to_svm_problem < features.json > svm_problem.txt
"""

import sys

import simplejson

LABEL_FEATURE = 'amazon_frac_voted_useful'

if __name__ == '__main__':
    feature_rows = []
    for line in sys.stdin:
        feature_rows.append(simplejson.loads(line.strip()))
   
	# TODO: make typos feature run faster
	feature_keys = [k for k in feature_rows[0].keys() if k.startswith('feature_') and k != 'feature_typos']

    def to_svm_input_line(feature_row):
        label = str(2*int(feature_row[LABEL_FEATURE] > 0.5) - 1)
        values = []
        for key_idx, key in enumerate(feature_keys):
            values.append("%s:%s" % (key_idx + 1, feature_row[key]))
        return ' '.join([label] + values)
    
    for feature_row in feature_rows:
        print >>sys.stdout, to_svm_input_line(feature_row)
