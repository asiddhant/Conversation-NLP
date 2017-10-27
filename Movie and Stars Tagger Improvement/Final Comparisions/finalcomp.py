import pandas as pd
import Levenshtein
import numpy as np

msent=pd.read_csv("msentences.csv",header=0,sep=",")
asent=pd.read_csv("asentences.csv",header=0,sep=",")

moutp=pd.read_csv("mfinaloutput.csv",header=0,sep=",")
aoutp=pd.read_csv("afinaloutput.csv",header=0,sep=",")

movies=pd.read_csv("movienames.csv",header=0,sep=",")
starcast=pd.read_csv("starcast.csv",header=0,sep=",")

mp1=0.9
mp2=0.2

sp1=0.9
sp2=0.2

def scorematcher(scores):
    thres=max(scores)*mp1
    return [index for index in range(len(scores)) if scores[index]>=thres]

def moviesextractor(postagged):
    if len(postagged)==1 and len(postagged[0])<=4:
        return []
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
            scores=[max(movienames)]*submovies.shape[0]
            j=0
            for i in maxmatch:
                matched=" ".join([word for word in postagged if word in submovies.title[i]])
                scores[j]+=(-mp2*(abs(len(submovies.title[i])-len(matched))))
                j+=1
            agreed=scorematcher(scores)
            eligible=[maxmatch[i] for i in agreed]
            return list(submovies.query(eligible)['movieid'])
        elif len(maxmatch)==1:
            return list(movies.query(maxmatch)['movieid'])
        else:
            return []
    else:
        return []
        
def starsextractor(postagged):
    if len(postagged)==1 and len(postagged[0])<=4:
        return []
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
            scores=[max(stars)]*substars.shape[0]
            j=0
            for i in maxmatch:
                matched=" ".join([word for word in postagged if word in substars.mstars[i]])
                scores[j]+=(-sp2*(abs(len(substars.mstars[i])-len(matched))))
                j+=1
            agreed=scorematcher(scores)    
            eligible=[maxmatch[i] for i in agreed]
            return list(substars.query(eligible)['star_id'])
        elif len(maxmatch)==1:
            return list(starcast.query(maxmatch)['star_id'])
        else:
            return []
    else:
        return []

def wordextractor(pdobj,column):
    main=[]
    temp=[]
    pdobj.index=range(pdobj.shape[0])
    for i in range(pdobj.shape[0]):
        if pdobj[column][i]=="P":
            temp+=[pdobj['word'][i].lower()]
        elif pdobj[column][i]=="O":
            main+=[temp]
            temp=[]
    main+=[temp]
    main=[item for item in main if item]
    
# Second Approach    
#    main=[]
#    pdobj.index=range(pdobj.shape[0])
#    for i in range(pdobj.shape[0]):
#        if pdobj[column][i]=="I":
#            main+=[pdobj['word'][i].lower()]
    
    return main
        
        

naivemovies=[]
chunkmovies=[]
modelmovies=[]
groundmovies=[]
for i in range(1,msent.shape[0]+1):
    sentnc=moutp[moutp.s_id==i]
    naiveoutput=wordextractor(sentnc,'naivetag')
    chunkoutput=wordextractor(sentnc,'chunktag')
    modeloutput=wordextractor(sentnc,'modeltag')
    groundoutput=wordextractor(sentnc,'groundtruth')
    
    for naiveitem in naiveoutput:
        naivemovies+=moviesextractor(naiveitem)
    for chunkitem in chunkoutput:
        chunkmovies+=moviesextractor(chunkitem)
    for modelitem in modeloutput:
        modelmovies+=moviesextractor(modelitem)
    for grounditem in groundoutput:
        groundmovies+=moviesextractor(grounditem)
            

naivestars=[]
stanfordstars=[]
modelstars=[]
groundstars=[]
for i in range(1,asent.shape[0]+1):
    sentnc=aoutp[aoutp.s_id==i]
    naiveoutput=wordextractor(sentnc,'naivetag')
    stanfordoutput=wordextractor(sentnc,'stanfordtag')
    modeloutput=wordextractor(sentnc,'modeltag')
    groundoutput=wordextractor(sentnc,'groundtruth')
    
    for naiveitem in naiveoutput:
        naivestars+=starsextractor(naiveitem)
    for stanforditem in stanfordoutput:
        stanfordstars+=starsextractor(stanforditem)
    for modelitem in modeloutput:
        modelstars+=starsextractor(modelitem)
    for grounditem in groundoutput:
        groundstars+=starsextractor(grounditem)
            
naivemovies=pd.DataFrame(naivemovies)
naivemovies.to_csv("naivemovies.csv",sep=",")
chunkmovies=pd.DataFrame(chunkmovies)
chunkmovies.to_csv("chunkmovies.csv",sep=",")
modelmovies=pd.DataFrame(modelmovies)
modelmovies.to_csv("modelmovies.csv",sep=",")
groundmovies=pd.DataFrame(groundmovies)
groundmovies.to_csv("groundmovies.csv",sep=",")

naivestars=pd.DataFrame(naivestars)
naivestars.to_csv("naivestars.csv",sep=",")
stanfordstars=pd.DataFrame(stanfordstars)
stanfordstars.to_csv("stanfordstars.csv",sep=",")
modelstars=pd.DataFrame(modelstars)
modelstars.to_csv("modelstars.csv",sep=",")
groundstars=pd.DataFrame(groundstars)
groundstars.to_csv("groundstars.csv",sep=",")
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    