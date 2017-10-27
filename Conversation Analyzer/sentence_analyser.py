import nltk
import pandas as pd
import Levenshtein
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import numpy as np
import requests

stop_words=get_stop_words('en')

conversation=['I want to watch Titanic with you honey',
              'Terminator is also a very good movie',
              'I dont like Action movies',
              'You said you liked Steven Spienberg',
              'We can watch Avatar. I love that blue guy',
              'Avatar seems fine to me. I love adventure.']
              
common=pd.read_table('common.csv',sep=',',header=None)
common=common[0].tolist()       
genres=pd.read_table('genres.csv',sep=',')
movienames=pd.read_table('movienames.csv',sep=',')
starcast=pd.read_table('starcast.csv',sep=',')

wordnet_lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
url='http://text-processing.com/api/sentiment/'

def relevantwords(wordset):
    relwords=[]
    for i in range(len(wordset)):
        if wordset[i][1] in ['NNP','NNPS','NN','NNS']:
            relwords=relwords+[wordset[i][0]]
    return relwords

def genreextractor(sentence):
    genrelist=[]
    for i in range(genres.shape[0]):
        if genres['sub.genre'][i] in sentence:
            genrelist=genrelist+[genres['genre'][i]]
    return genrelist

def sentimentanalyzer(sentence):
    payload = {'text': sentence}
    out=requests.post(url, data=payload).text
    neg_score=float(out[out.find("neg")+6:out.find("neg")+10])
    pos_score=float(out[out.find("pos")+6:out.find("pos")+10])
    neutral_score=float(out[out.find("neutral")+10:out.find("neutral")+14])
    return(pos_score,neg_score,neutral_score)
    



#Add Context & Leveshtien Distance
def starsextractor(wordset):
    stars=[0]*len(starcast['mstars'])
    for i in range(len(wordset)):
        for j in range(len(starcast['mstars'])):
            li=len(wordset[i])
            lj=len(starcast['mstars'][j])
            if li>7:
                dist=Levenshtein.distance(wordset[i],starcast['mstars'][j]) - max(li,lj) + min(li,lj)
                if dist<2 and dist>-1:
                    stars[j]=stars[j]+1
            else:
                if wordset[i] in starcast['mstars'][j]:
                    stars[j]=stars[j]+1
    if max(stars):
        maxmatch=np.argwhere(stars == np.amax(stars)).flatten().tolist()[0]
        return [starcast.query(maxmatch)['stars']]
    else:
        return []

#Add Context
def movieextractor(wordset):
    movies=[0]*len(movienames['title'])
    for i in range(len(wordset)):
        for j in range(len(movienames['title'])):
            li=len(wordset[i])
            lj=len(movienames['title'][j])
            if li>7:
                dist=Levenshtein.distance(wordset[i],movienames['title'][j]) - max(li,lj) + min(li,lj)
                if dist<2 and dist>-1:
                    movies[j]=movies[j]+1
            else:
                if wordset[i] in movienames['title'][j]:
                    movies[j]=movies[j]+1
    if max(movies):
        maxmatch=np.argwhere(movies == np.amax(movies)).flatten().tolist()[0]
        return [movienames.query(maxmatch)['title']]
    else:
        return []
        
def processlanguage(sentence):
    try:
        sentence=sentence.lower()
        genre=genreextractor(sentence)
        tokens=nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokens)
        tagged = relevantwords(tagged)
        tagged = [item for item in tagged if item not in genre+stop_words]
        for i in range(len(tagged)):
            tagged[i]=wordnet_lemmatizer.lemmatize(tagged[i])
        tagged = [item for item in tagged if item not in common]
        movies = movieextractor(tagged)
        tagged = [item for item in tagged if item not in movies]
        stars = starsextractor(tagged)
        pos_score,neg_score,neutral=sentimentanalyzer(sentence)
        keys=movies+genre+stars
        table={'key':keys,
               'pos_score':[pos_score]*len(keys),
               'neg_score':[neg_score]*len(keys),
               'neutral':[neutral]*len(keys)}
        table=pd.DataFrame(table)
        return table
        
    except Exception, e:
        print str(e)

table={'key':[],
       'pos_score':[],
       'neg_score':[],
       'neutral':[]}
table=pd.DataFrame(table)

for sentence in conversation:
    table=table.append(processlanguage(sentence))