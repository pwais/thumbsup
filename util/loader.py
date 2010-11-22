# helper functions and data structures to load all training and
# validation data
from config import *
import csv
import pdb

import simplejson

# key: id
# values: dicts with amazonprice
AZ_PRODUCTS = {}

# key: id
# values: dicts with avgprice
AZ_CATEGORIES = {}

# key: Business ID
# value: biz info
YELP_BUSINESSES = {}

def load_az_products():
    """Loads the products into AZ_PRODUCTS: a two layer
    dictionary. Assumes amazon data"""
    global AZ_PRODUCTS
    if AZ_PRODUCTS:
        return
    fields = [('amazonprice',float)]
    for az_product in csv.DictReader(open(AZ_PRODUCTS_CSV)):
        product = {}
        for key,t in fields:
            product[key] = t(az_product[key])
        AZ_PRODUCTS[int(az_product['id'])] = product

def load_yelp_bizes():
    """Loads the yelp biz data into global YELP_BUSINESES"""
    global YELP_BUSINESSES
    if YELP_BUSINESSES:
        return
    bizes = simplejson.load(open(YELP_BUSINESSES_JSON))
    YELP_BUSINESSES = dict((biz['id'], dict((k, v) for (k, v) in biz.iteritems()
                                            if k != 'id'))
                           for biz in bizes)

