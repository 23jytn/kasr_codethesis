#!/usr/bin/env python



import time
import pandas as pd
from collections import OrderedDict
from similarity import similarity
from helpertools import helperTools
import pydoop.mapreduce.api as api
import pandas as pd

def main():
	start_time = time.time()
	obj1 = helperTools()
	obj = similarity()
	df = pd.read_csv("/home/hadoop/50reviews.csv")
	domainThesaurus = OrderedDict({"SERVICE":["SERVICE","WAITER","STAFF","SERVER"],"ROOM":["BED","ROOM","BATHROOM"],"SHOPPING":["MALL","SHOPPING","STORE","MARKET"],"CLEANLINESS":["DIRTY","GRUBBY","CLEAN","NEAT"],"FOOD":["EAT","DISHES","DINNER","FOOD","BREAKFAST","DELICIOUS","MEAL","RESTAURANT","LUNCH"],"VALUE":["PRICE","CHEAP","WORTH","MONEY","EXPENSIVE","PAY"],"TRANSPORTATION":["RELATEDWAY","STOP","TRANSPORTATION","BUS"],"FAMILY/FRIENDS":["MOTHER","FRIEND","FATHER","FAMILY","DAUGHTER","HUSBAND","CHILD","SON","KID","WIFE"],"LOCATION":["FAR","NEAR","LACATION"],"VIEW":["VIEW"],"QUIET":["QUIET"],"FITNESS":["POOL","FITNESS","GYM","SWIMMING","SPA"],"AIRPORT/TRAIN":["AIRPORT","TRAIN","AIRPORTTRAIN"],"WI-FI":["WI-FI","WI FI","WIFI"],"ENVIRONMENT":["MODERN","ENVIRONMENT","COMFORTABLE","CLASSICAL"],"BAR":["BAR","DRINKS","WINE"],"BEACH":["BEACH","SEA"]})

	#preferences = input("type your preferences :")
	preferences = open("/home/hadoop/Documents/pref",'r').read()
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



def mapper(_, text, writer):
	main()
	writer.emit('a','1')

def reducer(word, icounts, writer):
    	writer.emit('b',"1")





