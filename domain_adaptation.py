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
    parser.add_option('--combine', nargs=4,
                      help='Combine source and target into one data set.' \
                          ' Arguments: sourcefile target ms mt')
    relabel_help='''Force all the examples to have the same
               label. Arguments: file newlabel. Useful to create input
               data for the linear classifier that learns the domain
               of a review. The error of this classifier is then used
               as an estimate of the distance between the
               distributions of the domains.'''
    parser.add_option('--relabel', nargs=2, help=relabel_help)
    
    options, args = parser.parse_args()
    if options.combine:
        s,t,ms,mt = options.combine
        for x in combine_domains(s, t, int(ms), int(mt)):
            print x
    elif options.relabel:
        file, newlabel = options.relabel
        relabel_dataset(file, newlabel)
