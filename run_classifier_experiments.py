"""Script to run all classifier experiments (using weka) for a single CSV data file"""
from __future__ import with_statement

import os
import subprocess
import sys

JAVA_CMD = "java -Xmx2g -cp external/weka/weka.jar:external/weka/libsvm.jar"

WEKA_CLASSIFIER_CMDS = {
#    'adaboost': 
#        JAVA_CMD + "weka.classifiers.meta.AdaBoostM1 -D -x 5 -i -k -t %s -d %s",
    'svm_linear': 
        #"weka.classifiers.functions.LibSVM -D -x 5 -i -k -K 0 -t %s -d %s",
	"external/libsvm-weights-3.0/svm-train -t 0 -v 5 %s %s",
    'svm_poly': 
        #"weka.classifiers.functions.LibSVM -D -x 5 -i -k -K 1 -t %s -d %s",
	"external/libsvm-weights-3.0/svm-train -t 1 -d 3 -v 5 %s %s",
    'svm_rbf': 
        #"weka.classifiers.functions.LibSVM -D -x 5 -i -k -K 3 -t %s -d %s",
	"external/libsvm-weights-3.0/svm-train -t 2 -g 10 -v 5 %s %s",
#    'naive_bayes': 
#        JAVA_CMD + "weka.classifiers.bayes.NaiveBayes -D -x 5 -i -k -threshold-file bayes_threshes.csv -t %s -d %s",
}

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    for classifier_name, cmd_txt in WEKA_CLASSIFIER_CMDS.iteritems():
        output_file_name = "%s_%s" % (output_file, classifier_name)
        txt_out_name = "%s_%s_stdout" % (output_file, classifier_name)
        
        cmd_txt = cmd_txt % (input_file, output_file_name)
        
        print "Running: %s saving stdout to %s" % (cmd_txt, txt_out_name)
        
        stdoutf = open(txt_out_name, 'w')
        subprocess.Popen(cmd_txt.split(' '), stdout=stdoutf)

