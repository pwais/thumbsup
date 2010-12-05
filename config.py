
SPELLCHECKER_TEXT = "external/big.txt"

SVM_LEARN_BIN_PATH = "external/svm_light/svm_learn"
SVM_CLASSIFY_BIN_PATH = "external/svm_light/svm_classify"

AZ_PRODUCTS_CSV = "external/amazon/productsTableCSV.csv"
AZ_CATEGORIES_CSV = "external/amazon/categoriesTableCSV.csv"

YELP_CATEGORIES_JSON = "external/yelp/yelp_category_dag.json"
YELP_BUSINESSES_JSON = "external/yelp/biz_dump_11-4-2010.json"

ANEW_WORD_MAP = "external/ANEW_word_map.json"

# Consider a review with useful vote percentile >= (<=) the below
# threshold a member of the positive (negative) useful class.  These thresholds
# are used so that we train on only extreme examples
USEFUL_MIN_PERCENTILE = 75
NONUSEFUL_MAX_PERCENTILE = 5

YELP_TYPOS_PATH = "external/yelp_typo_features.json"
AZ_TYPOS_PATH = "external/amazon_typo_features.json"

YELP_IDF_PATH = "external/yelp_idf_map.json"
AZ_IDF_PATH = "external/yelp_idf_map.json"
