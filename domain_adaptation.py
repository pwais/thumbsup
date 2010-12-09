'''Functions to prepare the domain adaptation experiments'''
from optparse import OptionParser
import random
import sys

def sample_category(data, category, N):
    '''extract a sample of N reviews from category'''
    pass

def relabel_dataset(dataset, label):
    '''change all the labels in dataset to match label'''
    for x in open(dataset).readlines():
        # relabel
        pass

def output_weight_file(alpha, ms, mt):
    '''produce a file with ms copies of (1-alpha) and mt copies of
    alpha. One weight per line. The output file is
    msS+mtT-alpha.wgt'''
    outfile = open("%sS+%sT-%s.wgt" % (ms, mt, alpha), 'w')
    source_weight = '%s\n' % (1-alpha)
    print >>outfile, source_weight*ms, # ',' to avoid extra newline
    target_weight = '%s\n' % alpha
    print >>outfile, target_weight*mt
    outfile.close()

def combine_domains(source, target, ms, mt):
    '''Produces a set with reviews from both domains with ms source
    reviews and mt target reviews.'''
    S = [r.strip() for r in open(source).xreadlines()]
    T = [r.strip() for r in open(target).xreadlines()]
    mS = random.sample(S, ms)
    mT = random.sample(T, mt)

    return mS + mT

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
    relabel_help='''Force all the examples to have the same
               label. Arguments: file newlabel. Useful to create input
               data for the linear classifier that learns the domain
               of a review. The error of this classifier is then used
               as an estimate of the distance between the
               distributions of the domains.'''
    parser.add_option('--relabel', nargs=2, help=relabel_help)
    alpha_help='''Expecify alpha to be used for the alpha-error. If
    this is epecified a .wgt file will be generated to pass to libsvm
    during training. Output saved in msS+mtT-alpha.wgt'''
    parser.add_option('-a', '--alpha', help=alpha_help)
    
    options, args = parser.parse_args()
    if options.combine:
        s,t = options.combine
        if not options.s or not options.t:
            print 'ms and mt are required when combining domains. See -h'
            sys.exit(1)
        ms, mt = int(options.s), int(options.t)
        outfile = open('%sS+%sT.csv' % (ms, mt), 'w')
        for x in combine_domains(s, t, ms, mt):
            print >>outfile, x
    elif options.relabel:
        file, newlabel = options.relabel
        relabel_dataset(file, newlabel)

    if options.alpha:
        if not options.s or not options.t:
            print 'ms and mt are required when generating a wieght file. See -h'
            sys.exit(1)
        ms, mt = int(options.s), int(options.t),
        output_weight_file(float(options.alpha), ms, mt)

