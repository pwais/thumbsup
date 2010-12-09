"""
Script to convert JSON features file to an svm_light-compatible input file.

Example:
    python features_to_svm_problem LABEL_FEATURE_NAME < features.csv > svm_problem.txt
"""

import csv
import sys

if __name__ == '__main__':
    label_feature_name = sys.argv[1]

    # Start streaming input
    feature_csv_streamer = csv.DictReader(sys.stdin)
    
    # Create a canonical order over feature keys
    row = feature_csv_streamer.next()
    feature_keys = list(row.iterkeys())
    feature_keys.remove(label_feature_name)
    
    def to_svm_input_line(feature_row):
        """Defines how to write an SVM input given a feature_row dict"""
        label = str(2*int(eval(feature_row[label_feature_name])) - 1)
        values = []
        for key_idx, key in enumerate(feature_keys):
            if feature_row.get(key):
                values.append("%s:%s" % (key_idx + 1, feature_row[key]))
        return ' '.join([label] + values)
    
    # Write out the first row
    print >>sys.stdout, to_svm_input_line(row)
    
    # Stream out the subsequent rows
    for row in feature_csv_streamer:
        print >>sys.stdout, to_svm_input_line(row)
