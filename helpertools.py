# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 05:29:26 2017

@author: DELL
"""
#!/usr/bin/env python


from math import *
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


class helperTools():
    def determinePreferences(self,preferences):
        preferencesMap = {}
        for things in  preferences.split(","):
            things = things.split(":")
            preferencesMap[things[0]]=things[1]
        return preferencesMap
        
    def preprocess(self,review):
        htmlremoved = BeautifulSoup(review,'lxml').get_text()
        word_list = htmlremoved.split(" ")
        filtered_words = [word for word in word_list if word not in stopwords.words('english')]
        stemmer = PorterStemmer()
        singles = [stemmer.stem(plural) for plural in filtered_words]
        return singles 
        
        
    def keywordExtraction(self,reviewset,domainThesaurus):
        keywordset={}
        for keys in domainThesaurus:
            count = 0
            for word in domainThesaurus[keys]:
                if word in reviewset:
                    count = count+1
            if count != 0:
                keywordset[keys]=count
        return keywordset
    def square_rooted(self,x):
        return round(sqrt(sum([a*a for a in x])),3)
        
    def cosine_similarity(self,x,y):
        numerator = sum(a*b for a,b in zip(x,y))
        denominator = self.square_rooted(x)*self.square_rooted(y)
        return round(numerator/float(denominator),3)
        
        #print cosine_similarity([3, 45, 7, 2], [2, 54, 13, 15]) 
             
    def jaccard_similarity(self,x,y):
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality/float(union_cardinality)
        #print jaccard_similarity([0,1,2,5,6],[0,2,3,5,7,9]) 
        
    
    def rating(self,df):
        # weighted average rating formula (sales["Current_Price"] * sales["Quantity"]).sum() / sales["Quantity"].sum
        av_rating =  df['stars'].sum()/len(df['stars'])
	if df['similarity'].sum() != 0:
       		weighted_rating = av_rating + float(( df['similarity'] * (df['stars']-av_rating)).sum() / df['similarity'].sum())
  	else:
		weighted_rating = av_rating
	return round(weighted_rating,1)
    
