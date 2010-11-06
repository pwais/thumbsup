# helper functions and data structures to load all training and
# validation data
from config import *
import csv
import pdb

# key: id
# values: dicts with amazonprice
AZ_PRODUCTS = {}

# key: id
# values: dicts with avgprice
AZ_CATEGORIES = {}

def load_products():
    '''Loads the products into AZ_PRODUCTS: a two layer dictionary'''
    if AZ_PRODUCTS:
        return
    keys = ['amazonprice']
    for az_product in csv.DictReader(open(AZ_PRODUCTS_CSV)):
        product = {}
        for key in keys:
            product[key] = az_product[key]
        AZ_PRODUCTS[az_product['id']] = product

def load_categories():
    pass
