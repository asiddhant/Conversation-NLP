import pandas as pd
import nltk

sentences=pd.read_csv("sentences.csv",header=0,sep=",")

#Feature Engineering

nerdataset={'s_id':[],
            'w_id':[],
            'word':[],
            'postag':[]}
nerdataset=pd.DataFrame(nerdataset)

s_id=0
for sentence in sentences['sentence']:
    s_id+=1
    tokens = nltk.word_tokenize(sentence)
    postagged = nltk.pos_tag(tokens)
    word=[]
    postag=[]
    for item in postagged:
        if item not in [",","."]:
            word+=[item[0]]
            postag+=[item[1]]
    leng=len(word)
    tempdataset={'s_id':[s_id]*leng,
                 'w_id':range(leng),
                 'word':word,
                 'postag':postag}
    tempdataset=pd.DataFrame(tempdataset)
    nerdataset=nerdataset.append(tempdataset)
    
nerdataset.to_csv("dataset.csv",sep=",")

from gensim.models import Word2Vec       
model = Word2Vec.load("300features_40minwords_10context")

vectorlist=[]
for word in nerdataset["word"]:
    word=word.lower()
    if word=="gon":
        word="going"
    elif word=="na":
        word="going"
    
    word=word.replace("'","")
    
    if word in model.index2word:
        vectorlist+=[model[word].tolist()]
    else:
        vectorlist+=[[0]*300]

nerdataset.index=range(nerdataset.shape[0])
a=pd.DataFrame(vectorlist)
a.index=range(a.shape[0])
b=pd.concat([nerdataset,a],axis=1)

countlist=[]
for word in nerdataset["word"]:
    word=word.lower()
    if word=="gon":
        word="going"
    elif word=="na":
        word="going"
    
    word=word.replace("'","")
    
    if word in model.index2word:
        wordobj=model.vocab[word]
        countlist+=[wordobj.count]
    else:
        countlist+=[0]

ax=pd.DataFrame(countlist)
nerdataset.index=range(nerdataset.shape[0])
bx=pd.concat([nerdataset,ax],axis=1)