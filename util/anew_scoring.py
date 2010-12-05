import os
import sys

import simplejson

import config

# Map of wd -> ANEW data, e.g.
#"dollar": {
#    "valence_mean": 7.4699999999999998, 
#    "arousal_mean": 6.0700000000000003, 
#    "dominance_std": 2.4199999999999999, 
#    "valence_std": 1.72, 
#    "dominance_mean": 6.3300000000000001, 
#    "arousal_std": 2.6699999999999999, 
#    "word_freq": 46
#  }, 
ANEW_WORD_MAP = {}

# Try to load ANEW data
try:
    ANEW_WORD_MAP = simplejson.load(open(config.ANEW_WORD_MAP, 'rb'))
    print >>sys.stderr, "Loaded ANEW data from %s" % config.ANEW_WORD_MAP
except:
    print >>sys.stderr, "Failed to load ANEW data from %s" % config.ANEW_WORD_MAP
    raise

ANEW_KEY_TO_MIN_MAX = dict((k, [100, -100]) for k in ANEW_WORD_MAP.values()[0].keys())
for wd, key_to_score in ANEW_WORD_MAP.iteritems():
    for key, score in key_to_score.iteritems():
        ANEW_KEY_TO_MIN_MAX[key][0] = min(score, ANEW_KEY_TO_MIN_MAX[key][0])
        ANEW_KEY_TO_MIN_MAX[key][1] = max(score, ANEW_KEY_TO_MIN_MAX[key][1])

ANEW_MIN_HIGH_VALENCE = 5.0
ANEW_MAX_LOW_VALENCE = 3.0
ANEW_HIGH_VALENCE_WORDS = frozenset(wd for wd, data in ANEW_WORD_MAP.iteritems()
                                       if data['valence_mean'] >= ANEW_MIN_HIGH_VALENCE)
ANEW_LOW_VALENCE_WORDS = frozenset(wd for wd, data in ANEW_WORD_MAP.iteritems()
                                      if data['valence_mean'] <= ANEW_MAX_LOW_VALENCE)

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

def weighted_normalized_freq_score(words, anew_key):
    """Normalized version of the above function"""
    min, max = ANEW_KEY_TO_MIN_MAX[anew_key]
    total_score = 0.0
    total_freq = 0
    for wd in words:
        wd = wd.lower()
        if wd in ANEW_WORD_MAP:
            total_score += ANEW_WORD_MAP[wd][anew_key] + min / max
            total_freq += 1
    if total_freq:
        return total_score / total_freq
    else:
        return 0.0
