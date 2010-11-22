"""
Script to convert JSON features file to an svm_light-compatible input file.

Example:
    python features_to_svm_problem LABEL_FEATURE_NAME < features.json > svm_problem.txt
"""

import csv
import sys

if __name__ == '__main__':
    label_feature_name = sys.argv[1]
    
    feature_rows = []
    for line in csv.DictReader(sys.stdin):
        feature_rows.append(line)
   
	feature_keys = [k for k in feature_rows[0].keys() 
                      if (k.startswith('feature_') and
                          # TODO: make typos feature run faster 
                          k != 'feature_typos')]

    def to_svm_input_line(feature_row):
        label = str(2*int(float(feature_row[label_feature_name]) > 0.2) - 1)
        values = []
        for key_idx, key in enumerate(feature_keys):
            values.append("%s:%s" % (key_idx + 1, feature_row[key]))
        return ' '.join([label] + values)
    
    for feature_row in feature_rows:
        print >>sys.stdout, to_svm_input_line(feature_row)
