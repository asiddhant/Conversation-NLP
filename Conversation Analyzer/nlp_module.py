# NLP_Module : This will serve as a relevance feedback mechanism for the group
# recommender system to tune the recommendations according to the current taste
# of the user without explicitly asking for feedback.

# This module uses Stanford Core NlP api's and the NLTK Package.

# Requirements
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
import Levenshtein
from stop_words import get_stop_words
import numpy as np
import requests
import os
from nltk.parse.stanford import StanfordParser
from nltk.parse.stanford import StanfordDependencyParser
import random

# Linking Stanford api's and Sentiment Analyzer api
java_path = "C:/Program Files (x86)/Java/jre1.8.0_91/bin/java.exe"
os.environ['JAVAHOME'] = java_path
parser=StanfordParser('C:/Users/asiddhan/Desktop/stanford-parser-full-2015-12-09/stanford-parser.jar',
                      'C:/Users/asiddhan/Desktop/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar')
dparser=StanfordDependencyParser('C:/Users/asiddhan/Desktop/stanford-parser-full-2015-12-09/stanford-parser.jar',
                                 'C:/Users/asiddhan/Desktop/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar')
wordnet_lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
url='http://text-processing.com/api/sentiment/'
stop_words=get_stop_words('en')

# Utiltiy Functions
def separator(x):
    if type(x)==str:
        return x.split()
    else:
        return []
    
# Loading Required Datasets
movies=pd.read_csv("movienames.csv",header=0,sep=",")
starcast=pd.read_csv("starcast.csv",header=0,sep=",")
common=pd.read_csv("common.csv",header=0,sep=",")
genres=pd.read_csv("genres.csv",header=0,sep=",")
genrelist=["adventure","animation","children","comedy","fantasy","romance","drama","action","crime",
           "thriller","horror","mystery","sci.fi","imax","documentary","war","musical","western","film.noir"]
conversation=pd.read_csv("session_01.csv",header=0,sep=",")

moviegenrereference=["this","that","it"]
actorreference=["his","her","hers","him","he","she"]
commonrefrence=["these","those","such"]
common=pd.read_table('common.csv',sep=',',header=None)

# PreProcessing Datasets
movies.genre=map(separator,movies.genre)
movies.stars=map(separator,movies.stars)
starcast.genre=map(separator,starcast.genre)
starcast.movies=map(separator,starcast.movies)


# User Profiler
def userprofiler(userids,irec):
    users=pd.read_csv("users.csv")
    users=users[users.u_id.isin(userids)]
    users.pg=map(separator,users.pg)
    users.index=range(len(userids))
    imovie=movies[movies.movieid == irec]
    igenre=imovie.genre[0]
    igenre=[i for i in range(19) if igenre[i]=="1"]
    if len(igenre)>3:
        igenre=igenre[0:3]
    if len(igenre)==1:
        igenre.insert(0,igenre[0])
        igenre.insert(0,igenre[0])
    if len(igenre)==2:
        igenre.insert(0,igenre[0])
    igenre=[genrelist[i] for i in igenre]
    istars=imovie.stars[0]
    if len(istars)>3:
        istars=istars[0:3]
    if len(istars)==1:
        istars.insert(0,istars[0])
        istars.insert(0,istars[0])
    if len(istars)==2:
        istars.insert(0,istars[0])
    if len(istars)==0:
        istars=['0','0','0']
    current={'cg': [igenre],
             'cm': [[irec,irec,irec]],
             'ca': [istars]}
    current=pd.DataFrame(current,index=range(len(userids)))
    users=pd.concat([users,current],axis=1)
    puserpg=[]
    for i in range(len(userids)):
        puserpg+=users.iloc[i,3]
    randIndex = random.sample(range(len(puserpg)), 3)
    puserpg = [puserpg[i] for i in randIndex]
    puser={'u_id':0,'sex':users.sex.mean(),'age':users.age.mean(),
           'pg': [puserpg], 'ca' :[users.iloc[0,4]], 'cg': [users.iloc[0,5]],
           'cm': [users.iloc[0,6]]}
    puser=pd.DataFrame(puser)
    users=users.append(puser)
    users.index=users.u_id
    return users

#Sentiment Analyzer
def sentimentanalyzer(sentence,keysent):
    payload = {'text': sentence}
    out=requests.post(url, data=payload).text
    neg_score=float(out[out.find("neg")+6:out.find("neg")+10])
    pos_score=float(out[out.find("pos")+6:out.find("pos")+10])
    #neutral_score=float(out[out.find("neutral")+10:out.find("neutral")+14])
    if pos_score>0.7:
        sentiment_score=5
    elif pos_score>0.5 and neg_score<0.3:
        sentiment_score=4
    elif pos_score<0.3 and neg_score>0.7:
        sentiment_score=1
    elif pos_score<0.3 and neg_score>0.5:
        sentiment_score=2
    else:
        if keysent.shape[0]>0:
            sentiment_score=round((3+(keysent.sentscore[keysent.shape[0]-1]))/2)
        else:
            sentiment_score=3
    return(sentiment_score)

# Keyword Extractors
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
    
def submovieranker(submovie,userprofiles,userid):
    score=0
    t1=2
    t2=1.5
    t3=3
    t4=2.5
    t5=1
    submoviegenre=[genrelist[i] for i in range(len(genrelist)) if submovie['genre'][i]]
    for g in userprofiles.cg.iloc[userid]:
        if g in submoviegenre:
            score+=t1
        t1-=0.5
    for g in userprofiles.cg.iloc[0]:
        if g in submoviegenre:
            score+=t2
        t2-=0.5
    for s in userprofiles.ca.iloc[userid]:
        if s in submovie['stars']:
            score+=t3
        t3-=0.5
    for s in userprofiles.ca.iloc[0]:
        if s in submovie['stars']:
            score+=t4
        t4-=0.5
    for g in userprofiles.pg.iloc[userid]:
        if g in submoviegenre:
            score+=t5
        t5-=0.5
    expyear=2015-userprofiles.age.iloc[0]+18
    if expyear-submovie['year']<10:
        score+=1
    return score
    
def moviesextractor(postagged,userprofiles,userid):
    movienames=[0]*len(movies['title'])
    for i in range(len(postagged)):
        for j in range(len(movies['title'])):
            li=len(postagged[i])
            lj=len(movies['title'][j])
            if li>5:
                if postagged[i] in movies['title'][j]:
                    movienames[j]=movienames[j]+ 2
                else:
                    dist=Levenshtein.distance(postagged[i],movies['title'][j]) - max(li,lj) + min(li,lj)
                    if dist<2 and dist>-1:
                        movienames[j]=movienames[j]+ 1
            else:
                if postagged[i] in movies['title'][j]:
                    movienames[j]=movienames[j]+ 1
    print max(movienames)                
    if max(movienames):
        maxmatch=np.argwhere(movienames == np.amax(movienames)).flatten().tolist()
        submovies=movies.query(maxmatch)
        scores=[max(movienames)]*submovies.shape[0]
        j=0
        for i in maxmatch:
            scores[j]+=submovieranker(submovies.query(i),userprofiles,userid)
            j+=1
        print scores
        eligible=[maxmatch[i] for i in range(len(scores)) if scores[i]>6]
        return list([submovies.query(eligible)['movieid']])
    else:
        return []

def substarsranker(substar,userprofiles,userid):
    score=0
    t1=6
    t2=5
    t3=3
    t4=2.5
    for g in userprofiles.cg.iloc[userid]:
        score+=(t1*substar['genre'][genrelist.index[g]])/sum(substar['genre'])
        t1-=1
    for g in userprofiles.cg.iloc[0]:
        score+=(t1*substar['genre'][genrelist.index[g]])/sum(substar['genre'])
        t2-=1
    for s in userprofiles.cm.iloc[userid]:
        if s in substar['movies']:
            score+=t3
        t3-=0.5
    for s in userprofiles.cm.iloc[0]:
        if s in substar['movies']:
            score+=t4
        t4-=0.5
    if substar['pop']>100000:
        score+=2
    elif substar['pop']>10000:
        score+=1
    expyear=2015-userprofiles.age.iloc[0]+18
    if expyear-substar['year']<10:
        score+=1
    return score

def starsextractor(postagged,userprofiles,userid):
    stars=[0]*len(starcast['mstars'])
    for i in range(len(postagged)):
        for j in range(len(starcast['mstars'])):
            li=len(postagged[i])
            lj=len(starcast['mstars'][j])
            if li>5:
                if postagged[i] in starcast['mstars'][j]:
                    stars[j]=stars[j]+ 2
                else:
                    dist=Levenshtein.distance(postagged[i],starcast['mstars'][j]) - max(li,lj) + min(li,lj)
                    if dist<2 and dist>-1:
                        stars[j]=stars[j]+ 1
            else:
                if postagged[i] in starcast['mstars'][j]:
                    stars[j]=stars[j]+ 1
    print max(stars)                
    if max(stars):
        maxmatch=np.argwhere(stars == np.amax(stars)).flatten().tolist()
        substars=starcast.query(maxmatch)
        scores=[max(stars)]*substars.shape[0]
        j=0
        for i in maxmatch:
            scores[j]+=substarsranker(substars.query(i),userprofiles,userid)
            j+=1
        print scores
        eligible=[maxmatch[i] for i in range(len(scores)) if scores[i]>6]
        return list([substars.query(eligible)['star_id']])
    else:
        return []
    
# Different Sentiment Keyword Matchers
def pastchecker(sentence,postagged):
    sentimentverbs=["like","love","hate"]
    negativewords=["not","never"]
    for i in range(len(postagged)):
        if postagged[i][1] in ["VBN","VBD"]:
            obj=porter_stemmer.stem_word(postagged[i][0])
            if obj in sentimentverbs:
                return 1
            else:
                for word in negativewords:
                    if word in sentence:
                        return 0
                    else:
                        return 1            
    return 0

def comparisonchecker(postagged):
#    for i in range(len(postagged)):
#        if postagged[i][1] == "JJR":
#            return 1
    return 0
    
def conjunctivechecker(postagged):
#    for i in range(len(postagged)-2):
#        if postagged[i+1][1] == "CC":
#            return 1
    return 0

def comparisonanalyzer(sentence,userprofiles,userid):
    
    return userprofiles
   
def conjunctiveanalyzer(sentence,userprofiles,userid):
    
    return userprofiles

def tagfinder(keys,movies,genres,stars):
    tag=keys
    for i in range(len(keys)):
        if keys[i] in movies:
            tag[i]="m"
        elif keys[i] in genres:
            tag[i]="g"
        elif keys[i] in stars:
            tag[i]="s"
    return tag
    
def normalanalyzer(keysent,sentence,userprofiles,userid,tagged):
    sentencelower=sentence.lower()
    genre=genreextractor(sentencelower)
    postagged = [item for item in tagged if item not in genre+stop_words]
    for i in range(len(postagged)):
        postagged[i]=wordnet_lemmatizer.lemmatize(postagged[i])
    postagged = [item for item in postagged if item not in common]
    movies = moviesextractor(postagged,userprofiles,userid)
    postagged = [item for item in tagged if item not in movies]
    stars = starsextractor(postagged,userprofiles,userid)

    detwords=[]    
    
    if not genre and not movies and not stars:
        for i in range(len(tagged)):
            if tagged[i][1] in ['PRP','DT']:
                detwords=detwords+[tagged[i][0]]
    
    for word in detwords:
        if word in moviegenrereference:
            i=1
            while i<=10:
                if keysent.iloc[keysent.shape[0]-i,1]=="m":
                    movies+=keysent.iloc[keysent.shape[0]-i,0]
                    break
                elif keysent.iloc[keysent.shape[0]-i,1]=="g":
                    genre+=keysent.iloc[keysent.shape[0]-i,0]
                    break
                else:
                    i+=1
        elif word in actorreference:
            i=1
            while i<=10:
                if keysent.iloc[keysent.shape[0]-i,1]=="s":
                    stars+=keysent.iloc[keysent.shape[0]-i,0]
                    break
                else:
                    i+=1
        elif word in commonrefrence:
            if keysent.iloc[keysent.shape[0]-1,1]=="s":
                stars+=keysent.iloc[keysent.shape[0]-i,0]
            elif keysent.iloc[keysent.shape[0]-1,1]=="m":
                movies+=keysent.iloc[keysent.shape[0]-i,0]
            else:
                genre+=keysent.iloc[keysent.shape[0]-i,0]

    sentimentscore=sentimentanalyzer(sentence,keysent)
    
    if(movies):
        ext=userprofiles.cm[userprofiles.u_id==userid][0]
        for movie in movies:    
            ext.insert(0,movie)
        ext=ext[0:3]
        userprofiles.set_value(userid,'cm',ext)
        userprofiles.set_value(0,'cm',ext)
    if(genre):
        ext=userprofiles.cg[userprofiles.u_id==userid][0]
        for gen in genre: 
            ext.insert(0,gen)
        ext=ext[0:3]
        userprofiles.set_value(userid,'cg',ext)
        userprofiles.set_value(0,'cg',ext)
    if(stars):
        ext=userprofiles.cm[userprofiles.u_id==userid][0]
        for star in stars:
            ext.insert(0,star)
        ext=ext[0:3]
        userprofiles.set_value(userid,'ca',ext)
        userprofiles.set_value(0,'ca',ext)
    
    keys=movies+genre+stars
    watched=pastchecker(sentence,tagged)
    if len(keys)==0:
        return keysent,userprofiles
    else:
        table={'key':keys,
               'tag':tagfinder(keys),
               'sent_score':[sentimentscore]*len(keys),
               'watched':[watched]*len(keys),
               'userid':[userid]*len(keys)}
        table=pd.DataFrame(table)
        if keysent.shape[1] != 0:
            keysent = pd.concat([keysent,table],axis=1)
        else:
            keysent = table
        return keysent,userprofiles
    
# Sentence Analyzer
def sentenceanalyzer(keysent,sentence,userprofiles,userid):
    tokens=nltk.word_tokenize(sentence)
    postagged = nltk.pos_tag(tokens)
    parsedstr=parser.raw_parse(sentence)
    for parsed in parsedstr:
        parsed.pretty_print()
    if comparisonchecker(postagged)==1:
        keysent,userprofiles=comparisonanalyzer(keysent,sentence,userprofiles,userid,postagged,parsed)
    elif conjunctivechecker(postagged)==1:
        keysent,userprofiles=conjunctiveanalyzer(keysent,sentence,userprofiles,userid,postagged,parsed)
    else:
        keysent,userprofiles=normalanalyzer(keysent,sentence,userprofiles,userid,postagged)            
    return keysent,userprofiles
    
# Main Function
def mainfunction():
    userids = [1,3]
    irec=296
    userprofiles=userprofiler(userids,irec)
    keysent={'key':[],
             'tag':[],
             'sent_score':[],
             'watched':[],
             'userid':[]}
    keysent=pd.DataFrame(keysent)
    for i in range(conversation.shape[0]):
        userid=conversation.u_id[i]
        keysent,userprofiles=sentenceanalyzer(keysent,conversation.sentence[i],userprofiles,userid)
    print keysent
    