import pandas as pd
import nltk
import requests

sentences=pd.read_csv("sentimentdataset.csv",header=0,sep=",",encoding="latin-1")
url='http://text-processing.com/api/sentiment/'
mapping={'neg':-1,'pos':1,'neu':0}

for i in range(sentences.shape[0]):
    sentences['sentence'][i]=sentences['sentence'][i].replace('\xa0',' ')

nltkpos=[]
nltkneg=[]
nltkntl=[]
nltklab=[]
count=0
for sentence in sentences['sentence']:
    payload = {'text': sentence}
    out=requests.post(url, data=payload).text
    nltkneg+=[float(out[out.find("neg")+6:out.find("neg")+10])]
    nltkpos+=[float(out[out.find("pos")+6:out.find("pos")+10])]
    nltkntl+=[float(out[out.find("neutral")+10:out.find("neutral")+14])]
    templab=out[out.find("label")+9:out.find("label")+12]
    nltklab+=[mapping[templab]]
    count+=1
    if not count%10:
        print count/3 , ' % Complete'
    
nltkout={'nltklab':nltklab,
         'nltkpos':nltkpos,
         'nltkneg':nltkneg,
         'nltkntl':nltkntl}
nltkout=pd.DataFrame(nltkout)
nltkout.index=range(nltkout.shape[0])
sentences.index=range(sentences.shape[0])
sentences=pd.concat([nltkout,sentences],axis=1)

from textblob import TextBlob

blobsub=[]
blobpol=[]
count=0
for sentence in sentences['sentence']:
    blob = TextBlob(sentence)
    blobsub += [blob.subjectivity]
    blobpol += [blob.polarity]
    count+=1
    print count
    if not count%10:
        print count/3 , ' % Complete'
        
blobout={'blobsub':blobsub,
         'blobpol':blobpol}

blobout=pd.DataFrame(blobout)
blobout.index=range(blobout.shape[0])
sentences.index=range(sentences.shape[0])
sentences=pd.concat([sentences,blobout],axis=1)


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
        word+=[item[0]]
        postag+=[item[1]]
    leng=len(word)
    tempdataset={'s_id':[s_id]*leng,
                 'w_id':range(leng),
                 'word':word,
                 'postag':postag}
    tempdataset=pd.DataFrame(tempdataset)
    nerdataset=nerdataset.append(tempdataset)


