import os
import csv
import simplejson


yelp_data = simplejson.load(open('external/yelp/review_dump_11-4-2010.json'))


rc = 0
amazon_data = []
for r in csv.DictReader(open('external/amazon/reviewsTableCSV.csv')):
    amazon_data.append(r)
    rc += 1
    if rc > 15000:
	break

amz_useful = [int(r['useful'] or 0) for r in amazon_data]
yelp_useful = [r['u_count'] for r in yelp_data]


import matplotlib.pyplot as plt

plt.figure(1)

n, bins, patches = plt.hist(amz_useful, 50, facecolor='green', alpha=0.75)
plt.xlabel('Number of Useful Votes')
plt.ylabel('Number of Reviews')
plt.title(r'Distribution of Votes over Amazon Reviews')


plt.figure(2)

n, bins, patches = plt.hist(yelp_useful, 50, facecolor='red', alpha=0.75)
plt.xlabel('Number of Useful Votes')
plt.ylabel('Number of Reviews')
plt.title(r'Distribution of Votes over Yelp Reviews')


plt.show()