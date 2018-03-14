# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer
from helpertools import helperTools
from nltk.stem.porter import PorterStemmer


class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer,self).build_analyzer()
        #english_stemmer = nltk.stem.SnowballStemmer('english')      
        english_stemmer = PorterStemmer()
        return lambda doc:(english_stemmer.stem(w) for w in analyzer(doc))

class similarity():
    def approximate_similarity(self,preferencesmap,df):
        obj = helperTools()
        lis = preferencesmap.keys()
        line = ""
        similaritylist = []
        for elements in lis:
            line = line+" "+elements
        linewrds = obj.preprocess(line)
        for review in df['text']:
            review = obj.preprocess(review)
            similaritylist.append(obj.jaccard_similarity(review,linewrds))
        return similaritylist
        
    def exact_similarity(self,preferencesmap,df):
        obj = helperTools()
        vectorizer = StemmedTfidfVectorizer(min_df=1,stop_words='english')
        vectorized = vectorizer.fit_transform(df['text'])
        lis = preferencesmap.keys()
        line = ""
        for elements in lis:
            line = line+" "+elements.strip()
            #print(line)
        x = vectorizer.transform([line])
        xar = []
        for el in x.toarray():
            xar = el
        coslist = []
        for p in vectorized:
            par = []
            for el in p.toarray():
                par = el
            result = obj.cosine_similarity(xar,par)
            coslist.append(result)  
        return coslist
        #print(df.head())
