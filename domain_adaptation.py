'''Functions to prepare the domain adaptation experiments'''
from __future__ import with_statement

from optparse import OptionParser
import os
import random
import subprocess
import sys
import csv

def sample_category(data, category, N):
    '''extract a sample of N reviews from category'''
    pass

def relabel_and_combine(domain0, domain1):
    '''change all the labels in dataset to match label'''
    reader0 = csv.DictReader(open(domain0))
    fieldnames = sorted(reader0.fieldnames) # force label to be at the end
    outcsv = open('relabeled.csv', 'w')
    print >>outcsv, ','.join(fieldnames)
    writer = csv.DictWriter(outcsv, fieldnames)
    # relabel domain 0
    for r in reader0:
        r['label_useful_extreme_percentile'] = 0
        writer.writerow(r)
    # relabel domain 1
    reader1 = csv.DictReader(open(domain0))
    for r in reader1:
        r['label_useful_extreme_percentile'] = 1
        writer.writerow(r)

def output_weight_file(alpha, ms, mt, fpath=None):
    '''produce a file with ms copies of (1-alpha) and mt copies of
    alpha. One weight per line. The output file is
    msS+mtT-alpha.wgt'''
    if fpath is None:
        fpath = "%sS+%sT-%s.wgt" % (ms, mt, alpha)
    outfile = open(fpath, 'w')
    source_weight = '%s\n' % (1-alpha)
    print >>outfile, source_weight*ms, # ',' to avoid extra newline
    target_weight = '%s\n' % alpha
    print >>outfile, target_weight*mt
    outfile.close()

def combine_domains(S, T, ms, mt):
    '''Produces a set with reviews from both domains with ms source
    reviews and mt target reviews.'''
    mS = random.sample(open(S).readlines()[1:], ms)
    mT = random.sample(open(T).readlines()[1:], mt)

    return mS + mT

ALPHAS = [x*0.05 for x in xrange(20)]
M_Ts = [250, 500, 1000, 2000]
M_Ss = [250, 500, 1000, 2000]
SVM_CMD = "external/libsvm-weights-3.0/svm-train -v 5 -t 0 -W %s %s"

def run_translate_to_svm(infile_path):
    outfile_path = "%s.svm_problem" % infile_path.split('.')[0]
    translate_cmd = "python features_to_svm_problem.py label_useful_extreme_percentile"
    subprocess.check_call(translate_cmd.split(' '), stdin=open(infile_path), stdout=open(outfile_path, 'w'))
    return outfile_path

def run_auto_experiment(options):
    s,t = options.combine
    header = open(s).readlines()[0].strip()
    
    def run_one_experiment(options, ms, mt, alpha):
        with open(os.path.join(options.auto, '%sS+%sT.csv' % (ms, mt)), 'w') as f:
            print >>f, header
            for line in combine_domains(s, t, ms, mt):
                print >>f, line.strip()
            f.flush()
            svm_input_file_path = run_translate_to_svm(f.name)
        
        weightpath = os.path.join(options.auto, '%sS+%sT-%s.wgt' % (ms, mt, alpha))
        output_weight_file(alpha, ms, mt, fpath=weightpath)

        svm_results_path = os.path.join(options.auto, '%sS+%sT-%s.results' % (ms, mt, alpha))        
        svm_cmd = SVM_CMD % (weightpath, svm_input_file_path)
        subprocess.check_call(svm_cmd.split(' '), stdout=open(svm_results_path, 'w'))

    ms = 2500
    for mt in M_Ts:
        for alpha in ALPHAS:
            run_one_experiment(options, ms, mt, alpha)
    

    mt = 2500
    for ms in M_Ss:
        for alpha in ALPHAS:
            run_one_experiment(options, ms, mt, alpha)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--combine', nargs=2,
                      help='Combine source and target into one data set.' \
                          ' Arguments: sourcefile targetfile.' \
                          ' Options -s and -t are required with this.' \
                          ' Output saved to msS+mtT.csv')
    parser.add_option('-s',
                      help='Number of examples from the source domain')
    parser.add_option('-t',
                      help='Number of examples from the target domain')
    relabel_help='''Combine both domains changing the label to 0 for
               the first domain and 1 for the second one. Arguments:
               domain0.csv domain1.csv. Useful to create input data
               for the linear classifier that learns the domain of a
               review. The error of this classifier is then used as an
               estimate of the distance between the distributions of
               the domains.'''
    parser.add_option('--relabel', nargs=2, help=relabel_help)
    alpha_help='''Expecify alpha to be used for the alpha-error. If
    this is epecified a .wgt file will be generated to pass to libsvm
    during training. Output saved in msS+mtT-alpha.wgt'''
    parser.add_option('-a', '--alpha', help=alpha_help)
    parser.add_option('--auto', default=None,
        help="Automatically generate a bunch of combined files for "
             "default experiment parameters in the given directory.")
    
    options, args = parser.parse_args()
    if options.auto is not None and options.combine:
        run_auto_experiment(options)
    elif options.combine:
        s,t = options.combine
        if not options.s or not options.t:
            print 'ms and mt are required when combining domains. See -h'
            sys.exit(1)
        ms, mt = int(options.s), int(options.t)
        outfile = open('%sS+%sT.csv' % (ms, mt), 'w')
        # print header first. don't use csv dict reader to make it
        # simpler
        header = open(s).readlines()[0].strip()
        print >>outfile, header
        for x in combine_domains(s, t, ms, mt):
            print >>outfile, x.strip()
    elif options.relabel:
        domain0, domain1 = options.relabel
        relabel_and_combine(domain0, domain1)

    if options.alpha:
        if not options.s or not options.t:
            print 'ms and mt are required when generating a wieght file. See -h'
            sys.exit(1)
        ms, mt = int(options.s), int(options.t),
        output_weight_file(float(options.alpha), ms, mt)

