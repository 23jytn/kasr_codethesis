# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 07:43:50 2017

@author: DELL
"""
import time
import pandas as pd
from collections import OrderedDict
from similarity import similarity
from helpertools import helperTools
import pydoop.mapreduce.api as api


def main():
	start_time = time.time()
	obj1 = helperTools()
	obj = similarity()
	df = pd.read_csv("./yelp_academic_dataset_review.csv",nrows=3000)
	domainThesaurus = OrderedDict({"SERVICE":["SERVICE","WAITER","STAFF","SERVER"],"ROOM":["BED","ROOM","BATHROOM"],"SHOPPING":["MALL","SHOPPING","STORE","MARKET"],"CLEANLINESS":["DIRTY","GRUBBY","CLEAN","NEAT"],"FOOD":["EAT","DISHES","DINNER","FOOD","BREAKFAST","DELICIOUS","MEAL","RESTAURANT","LUNCH"],"VALUE":["PRICE","CHEAP","WORTH","MONEY","EXPENSIVE","PAY"],"TRANSPORTATION":["RELATEDWAY","STOP","TRANSPORTATION","BUS"],"FAMILY/FRIENDS":["MOTHER","FRIEND","FATHER","FAMILY","DAUGHTER","HUSBAND","CHILD","SON","KID","WIFE"],"LOCATION":["FAR","NEAR","LACATION"],"VIEW":["VIEW"],"QUIET":["QUIET"],"FITNESS":["POOL","FITNESS","GYM","SWIMMING","SPA"],"AIRPORT/TRAIN":["AIRPORT","TRAIN","AIRPORTTRAIN"],"WI-FI":["WI-FI","WI FI","WIFI"],"ENVIRONMENT":["MODERN","ENVIRONMENT","COMFORTABLE","CLASSICAL"],"BAR":["BAR","DRINKS","WINE"],"BEACH":["BEACH","SEA"]})

	#preferences = input("type your preferences :")
	preferences = open("./pref",'r').read()
	preferencesmap = obj1.determinePreferences(preferences)

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
	    
	l = {'business_id':idlist,'personalized rating':ratlist}
	datfr = pd.DataFrame(data=l)

	sorte = datfr.sort_values(['personalized rating'],ascending=False)
	#print(sorte.head())




class Mapper(api.Mapper):
    def map(self, context):
	main()
        for w in words:
            context.emit(w, 1)

class Reducer(api.Reducer):
    def reduce(self, context):
        s = sum(context.values)
        context.emit(context.key, s)