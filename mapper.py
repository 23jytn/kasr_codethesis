#!/usr/bin/env python


import time
import pandas as pd
from collections import OrderedDict
from similarity import similarity
from helpertools import helperTools
import sys

start_time = time.time()
obj1 = helperTools()
obj = similarity()

df = pd.read_csv("/home/hadoop/50review.csv")
domainThesaurus = OrderedDict({"SERVICE":["SERVICE","WAITER","STAFF","SERVER"],"ROOM":["BED","ROOM","BATHROOM"],"SHOPPING":["MALL","SHOPPING","STORE","MARKET"],"CLEANLINESS":["DIRTY","GRUBBY","CLEAN","NEAT"],"FOOD":["EAT","DISHES","DINNER","FOOD","BREAKFAST","DELICIOUS","MEAL","RESTAURANT","LUNCH"],"VALUE":["PRICE","CHEAP","WORTH","MONEY","EXPENSIVE","PAY"],"TRANSPORTATION":["RELATEDWAY","STOP","TRANSPORTATION","BUS"],"FAMILY/FRIENDS":["MOTHER","FRIEND","FATHER","FAMILY","DAUGHTER","HUSBAND","CHILD","SON","KID","WIFE"],"LOCATION":["FAR","NEAR","LACATION"],"VIEW":["VIEW"],"QUIET":["QUIET"],"FITNESS":["POOL","FITNESS","GYM","SWIMMING","SPA"],"AIRPORT/TRAIN":["AIRPORT","TRAIN","AIRPORTTRAIN"],"WI-FI":["WI-FI","WI FI","WIFI"],"ENVIRONMENT":["MODERN","ENVIRONMENT","COMFORTABLE","CLASSICAL"],"BAR":["BAR","DRINKS","WINE"],"BEACH":["BEACH","SEA"]})

#preferences = input("type your preferences :")

f = open("/home/hadoop/Documents/pref",'r')
preferences = f.read()
preferences = preferences.strip()
#print(preferences)
f.close()

preferencesmap = obj1.determinePreferences(preferences)
#print(preferencesmap)
similarity = 'cosine'

#APPROXIMATE SIMILARITY COMPUTATION

if similarity=='jaccard':#!
    df['similarity']=obj.approximate_similarity(preferencesmap,df)

#EXACT SIMILARITY COMPUTATION

elif similarity=='cosine':
    df['similarity']=obj.exact_similarity(preferencesmap,df)

idlist = []
ratlist = []

for ids in df.business_id.unique():
    d = df[df.business_id == ids]
    Sorted = d.sort_values(['similarity'], ascending=False)
    f = Sorted[:5]
    rat = obj1.rating(f) 
    idlist.append(ids)
    ratlist.append(rat)

#print(df['similarity'])
#print(df['stars'])
#for ids,rat in zip(idlist,ratlist):
#	print("%s\t%s"%(ids,rat))
l = {'business_id':idlist,'personalized rating':ratlist}

datfr = pd.DataFrame(data=l)
sorte = datfr.sort_values(['personalized rating'],ascending=False)
lis1 = []
lis2 = []

for vals in sorte['business_id']:
	lis1.append(vals)
for vals in sorte['personalized rating']:
	lis2.append(vals)


for x,y in zip(lis1,lis2):
	print("%s\t%s"%(x,y))
#print(sorte.head())

#print("--- %s seconds ---" % (time.time() - start_time))

sys.stdout.flush()
