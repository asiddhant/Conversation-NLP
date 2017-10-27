from nltk.tag.stanford import StanfordNERTagger
st = StanfordNERTagger('C:/Users/asiddhan/Downloads/stanford-ner-2015-12-09/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'C:/Users/asiddhan/Downloads/stanford-ner-2015-12-09/stanford-ner-2015-12-09/stanford-ner.jar',
					   encoding='utf-8')
import nltk
import os
java_path = "C:/Program Files (x86)/Java/jre1.8.0_91/bin/java.exe"
os.environ['JAVAHOME'] = java_path

import pandas as pd

sentences = pd.read_csv("starnames.csv",header=0,sep=",")
for i in range(sentences.shape[0]):
    sentences['sentence'][i]=sentences['sentence'][i].replace('\xa0',' ')

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
        if item[0] not in [",","."]:
            word+=[item[0]]
            postag+=[item[1]]
    leng=len(word)
    tempdataset={'s_id':[s_id]*leng,
                 'w_id':range(leng),
                 'word':word,
                 'postag':postag}
    tempdataset=pd.DataFrame(tempdataset)
    nerdataset=nerdataset.append(tempdataset)

stanfordnerdataset={'s_id':[],
                    'w_id':[],
                    'word':[],
                    'nertag':[]}
stanfordnerdataset=pd.DataFrame(stanfordnerdataset)

s_id=0
for sentence in sentences['sentence']:
#    if s_id % 2:
#        sentence=sentence.lower()
    s_id+=1
    tokens = nltk.word_tokenize(sentence)
    postagged = nltk.pos_tag(tokens)
    word=[]
    for item in postagged:
        if item[0] not in [",","."]:
            word+=[item[0]]
    output=st.tag(word)
    word=[]
    nertag=[]
    for item in output:
        word+=[item[0]]
        nertag+=[item[1]]
    leng=len(word)
    tempdataset={'s_id':[s_id]*leng,
                 'w_id':range(leng),
                 'word':word,
                 'nertag':nertag}
    tempdataset=pd.DataFrame(tempdataset)
    stanfordnerdataset=stanfordnerdataset.append(tempdataset) 

stanfordnerdataset2.to_csv("stanfordnerdataset2.csv",sep=",")    
nerdataset.to_csv("nerdataset.csv",sep=",")

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
        vectorlist+=[[-999]*300]

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