import os
import sys

import simplejson

import config

ANEW_WORD_MAP = {}

# Try to load ANEW data
try:
    ANEW_WORD_MAP = simplejson.load(open(config.ANEW_WORD_MAP, 'rb'))
    print >>sys.stderr, "Loaded ANEW data from %s" % config.ANEW_WORD_MAP
except:
    print >>sys.stderr, "Failed to load ANEW data from %s" % config.ANEW_WORD_MAP
    raise

def weighted_freq_score(words, anew_key):
    """Computed weighted score.  See:
        "Measuring the Happiness of Large-Scale Written 
        Expression: Songs, Blogs, and Presidents" 
        Peter Sheridan Dodds and Christopher M. Danforth 

        http://www.springerlink.com/content/757723154j4w726k/fulltext.pdf
    """
    total_score = 0.0
    total_freq = 0
    for wd in words:
        wd = wd.lower()
        if wd in ANEW_WORD_MAP:
            total_score += ANEW_WORD_MAP[wd][anew_key]
            total_freq += 1
    if total_freq:
        return total_score / total_freq
    else:
        return 0.0
