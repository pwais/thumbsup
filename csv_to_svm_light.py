import csv
import sys

if __name__ == '__main__':
    
    idx_to_feature_key = {}
    for row in csv.DictReader(sys.stdin):
        if not idx_to_feature_key:
            feature_keys = [k for k in row.keys() if not k.startswith('label')]
            label_key = list(set(row.keys()) - set(feature_keys))[0]
            idx_to_feature_key = dict(enumerate(feature_keys))
        
        label = '1' if eval(row[label_key]) else '-1'
        feature_text = ' '.join("%s:%s" % (key_idx + 1, row[feature_key])
                                for key_idx, feature_key in idx_to_feature_key.iteritems()
                                if row.get(feature_key))
        
        print "%s %s" % (label, feature_text)
