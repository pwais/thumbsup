"""Script to run all classifier experiments (using weka) for a single CSV data file"""

import subprocess
import sys

JAVA_CMD = "java -cp external/weka/weka.jar:external/weka/libsvm.jar"

WEKA_CLASSIFIER_CMDS = {
    'adaboost': 
        "weka.classifiers.meta.AdaBoostM1 -D -x 5 -i -k -classifications weka.classifiers.evaluation.output.prediction.PlainText -t %s -d %s",
    'svm_linear': 
        "weka.classifiers.functions.LibSVM -D -x 5 -i -k -K 0 -t %s -d %s",
    'svm_poly': 
        "weka.classifiers.functions.LibSVM -D -x 5 -i -k -K 1 -D 4 -t %s -d %s",
    'svm_rbf': 
        "weka.classifiers.functions.LibSVM -D -x 5 -i -k -K 3 -t %s -d %s",
    'naive_bayes': 
        "weka.classifiers.bayes.NaiveBayes -D -x 5 -i -k -threshold-file bayes_threshes.csv -t %s -d %s",
}

if __name__ == '__main__':
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    for classifier_name, cmd_txt in WEKA_CLASSIFIER_CMDS.iteritems():
        output_file_name = "%s_%s" % (output_file, classifier_name)
        txt_out_name = "%s_%s_stdout" % (output_file, classifier_name)
        
        cmd_txt = cmd_txt % (input_file, output_file)
        
        full_cmd = "%s %s" % (JAVA_CMD, cmd_txt)
        
        print "Running: %s" % full_cmd
        if not subprocess.check_call(full_cmd.split(' ')):
            break
