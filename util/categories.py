import csv
import os
import sys
from collections import defaultdict

import simplejson

import config

# Try to load Yelp category data
YELP_CATEGORY_DATA = {'parent_map': {}, 'child_map': {}}
try:
    YELP_CATEGORY_DATA = simplejson.load(open(config.YELP_CATEGORIES_JSON, 'rb'))
    print >>sys.stderr, "Successfully loaded Yelp category data from %s" % config.YELP_CATEGORIES_JSON
except:
    print >>sys.stderr, "Could not load Yelp category data from %s" % config.YELP_CATEGORIES_JSON
    raise

# Try loading Amazon category data
AZ_CATEGORY_DATA = {'parent_map': defaultdict(set), 
                    'child_map': defaultdict(set),
                    'id_to_alias': {}}
try:
    for category_entry in csv.DictReader(open(config.AZ_CATEGORIES_CSV, 'rb')):
        AZ_CATEGORY_DATA['id_to_alias'][str(category_entry['id'])] = category_entry['name']
        lineage_seq = category_entry['lineage'].split(" > ")
        
        # Build the parent and child maps
        root = lineage_seq[0]
        AZ_CATEGORY_DATA['parent_map'][root] = set()
        parent = root
        for child in lineage_seq[1:]:
            if parent == child:
                continue # Amazon data has "Science > Astronomy > Astronomy"
            AZ_CATEGORY_DATA['parent_map'][child].add(parent)
            AZ_CATEGORY_DATA['child_map'][parent].add(child)
            parent = child
    print >>sys.stderr, "Successfully loaded Amazon category data from %s" % config.AZ_CATEGORIES_CSV
except:
    print >>sys.stderr, "Could not load Amazon category data from %s" % config.AZ_CATEGORIES_CSV
    raise

YELP_ROOTS = [cat for cat in YELP_CATEGORY_DATA['parent_map'].iterkeys()
                  if len(YELP_CATEGORY_DATA['parent_map'][cat]) == 0]

AMAZON_ROOTS = [cat for cat in AZ_CATEGORY_DATA['parent_map'].iterkeys()
                  if len(AZ_CATEGORY_DATA['parent_map'][cat]) == 0]

def get_yelp_roots_for_cat(cat):
    """Return a list of root categories for `cat`"""
    return __bfs_find_roots(cat, YELP_CATEGORY_DATA['parent_map'])

def get_amazon_roots_for_cat(cat):
    """Return a list of root categories for `cat`"""
    return __bfs_find_roots(cat, AZ_CATEGORY_DATA['parent_map'])

def get_amazon_roots_for_cat_id(cat_id):
    """Return a list of root categories for category ID `cat`"""
    return __bfs_find_roots(AZ_CATEGORY_DATA['id_to_alias'][str(cat_id)], 
                            AZ_CATEGORY_DATA['parent_map'])

def __bfs_find_roots(cat, parent_map, cat_to_roots_cache={}):
    """Use BFS on the `parent_map` to find root categories that are ancestors
    of `cat`.  Cache results in `cat_to_roots_cache`; this function is memoized."""
    if cat in cat_to_roots_cache:
        return cat_to_roots_cache[cat]
    
    roots = []
    q = [cat]
    while q:
        c = q.pop(0)
        if len(parent_map[c]) == 0:
            roots.append(c)
        q.extend(parent_map[c])
    
    cat_to_roots_cache[cat] = roots
    return roots
