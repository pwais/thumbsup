import os

from domain_adaptation import *

def combine_domains_test():
    source = 'first source\nsecond source'
    target = 'first target\nsecond target'
    # produce files
    sfile = 'sfile.txt'
    tfile = 'tfile.txt'
    print >>open(sfile, 'w'), source
    print >>open(tfile, 'w'), target
    # test
    assert len(combine_domains(sfile, tfile, 1, 1)) == 2
    # clean up
    os.remove(sfile)
    os.remove(tfile)

if __name__ == '__main__':
    combine_domains_test()
