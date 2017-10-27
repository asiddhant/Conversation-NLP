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
import copy

f=open("results.txt",'a')

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

def integralconvertor(x):
    return [int(i) for i in x]
    
# Loading Required Datasets
movies=pd.read_csv("movienames.csv",header=0,sep=",")
starcast=pd.read_csv("starcast.csv",header=0,sep=",")
common=pd.read_csv("common.csv",header=0,sep=",")
genres=pd.read_csv("genres.csv",header=0,sep=",")
genrelist=["adventure","animation","children","comedy","fantasy","romance","drama","action","crime",
           "thriller","horror","mystery","sci.fi","imax","documentary","war","musical","western","film.noir"]
conversation=pd.read_csv("session_02.csv",header=0,sep=",")

moviegenrereference=["this","that","it"]
actorreference=["his","her","hers","him","he","she"]
commonrefrence=["these","those","such"]
poscompwords=["more","better"]
negcompwords=["less","worse"]
common=pd.read_table('common.csv',sep=',',header=None)
common=common[0].tolist()
alpha=0.25
beta=0.25

# PreProcessing Datasets
movies.genre=map(separator,movies.genre)
movies.stars=map(separator,movies.stars)
starcast.genre=map(separator,starcast.genre)
starcast.movies=map(separator,starcast.movies)
starcast.genre=map(integralconvertor,starcast.genre)

# Score Matcher
def scorematcher(scores):
    thres=max(scores)*0.9
    return [index for index in range(len(scores)) if scores[index]>=thres]
    
# User Profiler
def userprofiler(userids,irec):
    irec=irec[0]
    users=pd.read_csv("users.csv")
    users=users[users.u_id.isin(userids)]
    users.pg=map(separator,users.pg)
    users.index=range(len(userids))
    imovie=movies[movies.movieid == irec]
    igenre=imovie.genre[imovie.index[0]]
    igenre=[i for i in range(19) if igenre[i]=="1"]
    if len(igenre)>3:
        igenre=igenre[0:3]
    if len(igenre)==1:
        igenre.insert(0,igenre[0])
        igenre.insert(0,igenre[0])
    if len(igenre)==2:
        igenre.insert(0,igenre[0])
    igenre=[genrelist[i] for i in igenre]
    istars=imovie.stars[imovie.index[0]]
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
#        if keysent.shape[0]>0:
#            sentiment_score=round((3+(list(keysent.sent_score)[keysent.shape[0]-1]))/2)
#        else:
#            sentiment_score=3
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
    for g in userprofiles.cg[userid]:
        if g in submoviegenre:
            score+=t1
        t1-=0.5
    for g in userprofiles.cg[0]:
        if g in submoviegenre:
            score+=t2
        t2-=0.5
    for s in userprofiles.ca[userid]:
        if s in submovie['stars']:
            score+=t3
        t3-=0.5
    for s in userprofiles.ca[0]:
        if s in submovie['stars']:
            score+=t4
        t4-=0.5
    for g in userprofiles.pg[userid]:
        if g in submoviegenre:
            score+=t5
        t5-=0.5
    expyear=2015-userprofiles.age[0]+18
    if expyear-submovie['year']<10:
        score+=1
    return score
    
def moviesextractor(postagged,userprofiles,userid):
    if len(postagged)==1 and len(postagged[0])<=4:
        return [],[]
    f.write(str(postagged))
    f.write("\n")
    movienames=[0]*len(movies['title'])
    for i in range(len(postagged)):
        for j in range(len(movies['title'])):
            li=len(postagged[i])
            lj=len(movies['title'][j])
            if li>5:
                if postagged[i] in movies['title'][j]:
                    movienames[j]=movienames[j]+ 2
                else:
                    dist=Levenshtein.distance(postagged[i],movies['title'][j]) - lj + li
                    if dist<2 and dist>-1:
                        movienames[j]=movienames[j]+ 1
            else:
                if postagged[i] in movies['title'][j]:
                    movienames[j]=movienames[j]+ 1
    if max(movienames):
        maxmatch=np.argwhere(movienames == np.amax(movienames)).flatten().tolist()
        if len(maxmatch)>1 and len(maxmatch)<15:
            submovies=movies.query(maxmatch)
            f.write(str(submovies.title))
            f.write("\n")
            scores=[max(movienames)]*submovies.shape[0]
            j=0
            for i in maxmatch:
                matched=" ".join([word for word in postagged if word in submovies.title[i]])
                scores[j]+=(alpha*submovieranker(submovies.query(i),userprofiles,userid)-beta*(abs(len(submovies.title[i])-len(matched))))
                j+=1
            f.write(str(scores))
            f.write("\n")    
            agreed=scorematcher(scores)
            eligible=[maxmatch[i] for i in agreed]
            f.write(str(list(submovies.query(eligible)['title'])))
            f.write("\n")
            return list(submovies.query(eligible)['movieid']),list(movies.query(maxmatch)['title'])
        elif len(maxmatch)==1:
            f.write(str(list(movies.query(maxmatch)['title'])))
            f.write("\n")
            return list(movies.query(maxmatch)['movieid']),list(movies.query(maxmatch)['title'])
        else:
            return [],[]
    else:
        return [],[]

def substarsranker(substar,userprofiles,userid):
    score=0
    t1=6
    t2=5
    t3=3
    t4=2.5
    for g in userprofiles.cg[userid]:
        score+=((t1*substar['genre'][genrelist.index(g)])/(sum(substar['genre'])))
        t1-=1
    for g in userprofiles.cg[0]:
        score+=((t1*substar['genre'][genrelist.index(g)])/(sum(substar['genre'])))
        t2-=1
    for s in userprofiles.cm[userid]:
        if s in substar['movies']:
            score+=t3
        t3-=0.5
    for s in userprofiles.cm[0]:
        if s in substar['movies']:
            score+=t4
        t4-=0.5
    if substar['pop']>100000:
        score+=2
    elif substar['pop']>10000:
        score+=1
    expyear=2015-userprofiles.age[0]+18
    if expyear-substar['year']<10:
        score+=1
    return score

def starsextractor(postagged,userprofiles,userid):
    if len(postagged)==1 and len(postagged[0])<=4:
        return [],[]
    f.write(str(postagged))
    f.write("\n")
    stars=[0]*len(starcast['mstars'])
    for i in range(len(postagged)):
        for j in range(len(starcast['mstars'])):
            li=len(postagged[i])
            lj=len(starcast['mstars'][j])
            if li>5:
                if postagged[i] in starcast['mstars'][j]:
                    stars[j]=stars[j]+ 2
                else:
                    dist=Levenshtein.distance(postagged[i],starcast['mstars'][j]) - lj + li
                    if dist<2 and dist>-1:
                        stars[j]=stars[j]+ 1
            else:
                if postagged[i] in starcast['mstars'][j]:
                    stars[j]=stars[j]+ 1
    if max(stars):
        maxmatch=np.argwhere(stars == np.amax(stars)).flatten().tolist()
        if len(maxmatch)>1 and len(maxmatch)<20:
            substars=starcast.query(maxmatch)
            f.write(str(substars.mstars))
            f.write("\n")
            scores=[max(stars)]*substars.shape[0]
            j=0
            for i in maxmatch:
                matched=" ".join([word for word in postagged if word in substars.mstars[i]])
                scores[j]+=(alpha*substarsranker(substars.query(i),userprofiles,userid)-beta*(abs(len(substars.mstars[i])-len(matched))))
                j+=1
            f.write(str(scores))
            f.write("\n")    
            agreed=scorematcher(scores)    
            eligible=[maxmatch[i] for i in agreed]
            f.write(str(list(substars.query(eligible)['star_id'])))
            f.write("\n")
            return list(substars.query(eligible)['star_id']),list(starcast.query(maxmatch)['mstars'])
        elif len(maxmatch)==1:
            f.write(str(list(starcast.query(maxmatch)['star_id'])))
            f.write("\n")
            return list(starcast.query(maxmatch)['star_id']),list(starcast.query(maxmatch)['mstars'])
        else:
            return [],[]
    else:
        return [],[]
    
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
    for i in range(len(postagged)):
        if postagged[i][1] == "JJR":
            return 1
    return 0
    
def conjunctivechecker(postagged):
    for i in range(len(postagged)-2):
        if postagged[i+1][1] == "CC":
            return 1
    return 0

def detpresence(postagged):
    for i in range(len(postagged)-2):
        if postagged[i+1][1] in ["DT","PRP"]:
            return 1
    return 0
    
def comparisonanalyzer(keysent,sentence,userprofiles,userid,tagged):
    
    if tagged[len(tagged)-1][1]=="JJR":
        if tagged[len(tagged)-1][1] in poscompwords:
            keysent,userprofiles=normalanalyzer(keysent,sentence,userprofiles,userid,tagged,"P")
            return keysent,userprofiles
        elif tagged[len(tagged)-1][1] in negcompwords:
            keysent,userprofiles=normalanalyzer(keysent,sentence,userprofiles,userid,tagged,"N")
            return keysent,userprofiles
    
    parts=[]
    temp=[]
    comp=[]
    for i in range(len(tagged)):
        if tagged[i][1]=="JJR":
            temp.append((tagged[i][0],tagged[i][1]))
            parts+=[temp]
            temp=[]
            comp+=[tagged[i][0]]
        else:
            temp.append((tagged[i][0],tagged[i][1]))
    parts+=[temp]
    
    if len(parts)>2 or len(parts)==1:
        return keysent,userprofiles
        
    p1=[a[0] for a in parts[0]]
    p1=" ".join(p1)

    p2=[a[0] for a in parts[1]]
    p2=" ".join(p2)
    
    if detpresence(parts[1]):
        if comp[0] in poscompwords:
            keysent,userprofiles=normalanalyzer(keysent,p2,userprofiles,userid,parts[1],"N")
            keysent,userprofiles=normalanalyzer(keysent,p1,userprofiles,userid,parts[0],"P")
        if comp[0] in negcompwords:
            keysent,userprofiles=normalanalyzer(keysent,p2,userprofiles,userid,parts[1],"P")
            keysent,userprofiles=normalanalyzer(keysent,p1,userprofiles,userid,parts[0],"N")
    else:
        if comp[0] in poscompwords:
            keysent,userprofiles=normalanalyzer(keysent,p1,userprofiles,userid,parts[0],"P")
            keysent,userprofiles=normalanalyzer(keysent,p2,userprofiles,userid,parts[1],"N")
        if comp[0] in negcompwords:
            keysent,userprofiles=normalanalyzer(keysent,p1,userprofiles,userid,parts[0],"N")
            keysent,userprofiles=normalanalyzer(keysent,p2,userprofiles,userid,parts[1],"P")
            
    return keysent,userprofiles
    
def verbpresence(tagged):
    for i in range(len(tagged)):
        if tagged[i][1] in ["VB","VBD","VBP","VBZ","VBN","VBG"]:
            return 1
    return 0
   
def conjunctiveanalyzer(keysent,sentence,userprofiles,userid,tagged):        
    parts=[]
    temp=[]
    conj=[]
    for i in range(len(tagged)):
        if tagged[i][1]=="CC":
            parts+=[temp]
            temp=[]
            conj+=[tagged[i][0]]
        else:
            temp.append((tagged[i][0],tagged[i][1]))
    parts+=[temp]
    
    for sen in parts:
        csentence=[a[0] for a in sen]
        csentence=" ".join(csentence)
        if verbpresence(sen):
            if comparisonchecker(sen):
                for word in poscompwords:
                    if word in csentence:
                        keysent,userprofiles=normalanalyzer(keysent,csentence,userprofiles,userid,sen,"P")
                        break
                for word in negcompwords:
                    if word in csentence:
                        keysent,userprofiles=normalanalyzer(keysent,csentence,userprofiles,userid,sen,"N")
                        break
            else:
                keysent,userprofiles=normalanalyzer(keysent,csentence,userprofiles,userid,sen)
        else:
            if parts.index(sen)==0:
                keysent,userprofiles=normalanalyzer(keysent,csentence,userprofiles,userid,sen)
            else:
                if conj[parts.index(sen)-1].lower()=="but":
                    keysent,userprofiles=normalanalyzer(keysent,csentence,userprofiles,userid,sen,"R")
                else:
                    keysent,userprofiles=normalanalyzer(keysent,csentence,userprofiles,userid,sen)
    
    return keysent,userprofiles

def tagfinder(keys,exmovies,exgenre,exstars):
    #tag=keys
    tag = copy.deepcopy(keys)
    for i in range(len(keys)):
        if keys[i] in exmovies:
            tag[i]="m"
        elif keys[i] in exgenre:
            tag[i]="g"
        elif keys[i] in exstars:
            tag[i]="s"
    return tag
    
def normalanalyzer(keysent,sentence,userprofiles,userid,tagged,sentmod="0"):
    sentencelower=sentence.lower()
    exgenre=genreextractor(sentencelower)
    relwords=relevantwords(tagged)
    relwords = [item.lower() for item in relwords if item.lower() not in exgenre+stop_words]
#    for i in range(len(relwords)):
#        relwords[i]=porter_stemmer.stem_word(relwords[i])
    relwords = [item.lower() for item in relwords if item.lower() not in common]
    exmovies=[]
    exstars=[]
    exmoviesn=[]
    exstarsn=[]
    if relwords:
        exmovies,exmoviesn= moviesextractor(relwords,userprofiles,userid)
        if exmovies:
            relwords = [item for item in relwords if item not in list(movies.title[movies.movieid==exmovies[0]])[0]]
            exstars,exstarsn = starsextractor(relwords,userprofiles,userid)
        else:
            exstars,exstarsn = starsextractor(relwords,userprofiles,userid)
            
    detwords=[]    
    
    if not exgenre and not exmovies and not exstars:
        for i in range(len(tagged)):
            if tagged[i][1] in ['PRP','DT']:
                detwords=detwords+[tagged[i][0]]
    
    zprev=0
    for word in detwords:
        word=word.lower()
        if word in moviegenrereference:
            zprev=1
            i=1
            while i<=min(10,keysent.shape[0]):
                if keysent.iloc[keysent.shape[0]-i,2]=="m":
                    exmovies+=[keysent.iloc[keysent.shape[0]-i,0]]
                    break
                elif keysent.iloc[keysent.shape[0]-i,2]=="g":
                    exgenre+=[keysent.iloc[keysent.shape[0]-i,0]]
                    break
                else:
                    i+=1
        elif word in actorreference:
            zprev=1
            i=1
            while i<=min(10,keysent.shape[0]):
                if keysent.iloc[keysent.shape[0]-i,2]=="s":
                    exstars+=[keysent.iloc[keysent.shape[0]-i,0]]
                    break
                else:
                    i+=1
        elif word in commonrefrence:
            i=1
            zprev=1
            if keysent.iloc[keysent.shape[0]-1,2]=="s":
                exstars+=[keysent.iloc[keysent.shape[0]-i,0]]
            elif keysent.iloc[keysent.shape[0]-1,2]=="m":
                exmovies+=[keysent.iloc[keysent.shape[0]-i,0]]
            else:
                exgenre+=[keysent.iloc[keysent.shape[0]-i,0]]
    
    f.write(str(detwords))
    f.write("\n")
    f.write(str(exmovies))
    f.write("\n")
    f.write(str(exgenre))
    f.write("\n")
    f.write(str(exstars))
    f.write("\n")
    
    print sentence
    
    for gs in exgenre:
        sentence=sentence.lower().replace(gs,'genre')
    
    for msn in exmoviesn:
        nameparts=msn.split()
        for namepart in nameparts:
            sentence=sentence.lower().replace(namepart,'movie')
        
    print sentence
    
    sentimentscore=sentimentanalyzer(sentence,keysent)
    ##Add the sentmod thing here 
    if sentmod=="R":
        sentimentscore=5-sentimentscore
    elif sentmod=="N":
        sentimentscore=min(1,sentimentscore-2)
    elif sentmod=="P":
        sentimentscore=max(5,sentimentscore+2)
    
    
    
    if "why" in sentence.lower():
        sentimentscore=5-sentimentscore
        
    
    if(exmovies):
        extm=userprofiles.cm[userid]
        for exmovie in exmovies:    
            extm.insert(0,exmovie)
        extm=extm[0:3]
        userprofiles.set_value(userid,'cm',extm[0:3])
        userprofiles.set_value(0,'cm',extm[0:3])
    if(exgenre):
        extg=userprofiles.cg[userid]
        for exgen in exgenre: 
            extg.insert(0,exgen)
        extg=extg[0:3]
        userprofiles.set_value(userid,'cg',extg[0:3])
        userprofiles.set_value(0,'cg',extg[0:3])
    if(exstars):
        exts=userprofiles.ca[userid]
        for exstar in exstars:
            exts.insert(0,exstar)
        exts=exts[0:3]
        userprofiles.set_value(userid,'ca',exts[0:3])
        userprofiles.set_value(0,'ca',exts[0:3])
    
    

    keys=exmovies+exgenre+exstars
    watched=pastchecker(sentencelower,tagged)
    if len(keys)==0:
        return keysent,userprofiles
    else:
        table={'key':map(str,keys),
               'tag':tagfinder(keys,exmovies,exgenre,exstars),
               'sent_score':[sentimentscore]*len(keys),
               'watched':[watched]*len(keys),
               'userid':[str(userid)]*len(keys),
               'zprev':[zprev]*len(keys)}
        table=pd.DataFrame(table)
        keysent = keysent.append(table)
        return keysent,userprofiles
    
# Sentence Analyzer
def sentenceanalyzer(keysent,sentence,userprofiles,userid):
    tokens = nltk.word_tokenize(sentence)
    postagged = nltk.pos_tag(tokens)
    
    f.write(str(postagged))
    f.write("\n")
#    parsedstr=parser.raw_parse(sentence)
#    for parsed in parsedstr:
#        parsed.pretty_print()
    if conjunctivechecker(postagged)==1:
        keysent,userprofiles=conjunctiveanalyzer(keysent,sentence,userprofiles,userid,postagged)
    elif comparisonchecker(postagged)==1:
        keysent,userprofiles=comparisonanalyzer(keysent,sentence,userprofiles,userid,postagged)
    else:
        keysent,userprofiles=normalanalyzer(keysent,sentence,userprofiles,userid,postagged)
    return keysent,userprofiles
    
# Main Function
def mainfunction():
    
    userids = [1000004,1000008,1000009]
    irec=[296,1,2]
    userprofiles=userprofiler(userids,irec)
    keysent={'key':irec,
             'tag':["m"]*3,
             'sent_score':[3]*3,
             'watched':[0]*3,
             'userid':[0]*3,
             'zprev':[0]*3}
    keysent=pd.DataFrame(keysent)
    for i in range(conversation.shape[0]):
        userid=conversation.u_id[i]
        f.write(conversation.sentence[i])
        f.write("\n")
        keysent,userprofiles=sentenceanalyzer(keysent,conversation.sentence[i],userprofiles,userid)
        f.write("\n")
        print i
    f.close()
    print keysent
    keysent.to_csv("session_02results.csv",sep=",")
