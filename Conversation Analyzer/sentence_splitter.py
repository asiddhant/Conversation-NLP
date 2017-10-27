import pandas as pd
import nltk
import os
java_path = "C:/Program Files (x86)/Java/jre1.8.0_91/bin/java.exe"
os.environ['JAVAHOME'] = java_path
from nltk.parse.stanford import StanfordParser
parser=StanfordParser('C:/Users/asiddhan/Desktop/stanford-parser-full-2015-12-09/stanford-parser.jar',
                      'C:/Users/asiddhan/Desktop/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar')

subclause=['SBAR','SBARQ','SINV','SQ']
conjuction=['CC','CONJP']

clauselevel=['S','SBAR','SBARQ','SINV','SQ']
phraselevel=['NP','PP','ADJP']

sentokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
conversation=pd.read_csv('conjuctive.csv',sep=',')

for i in range(conversation.shape[0]):
    conversation['sentence'][i]=conversation['sentence'][i].replace('\xa0',' ')

sentences=conversation['sentence'].tolist()

splittedsentences=[]
for sentence in sentences:
    splittedsentences+=sentokenizer.tokenize(sentence)
sentences=splittedsentences

def sentenceformer(splitted,conjword,sentence):
    tagged=nltk.word_tokenize(sentence)
    tagged=nltk.pos_tag(tagged)
    chunkgram = r"""Chunk: {<NN\w?>*<PRP?>*<MD?>*<TO?>*<VB\w?>}"""
    chunkParser = nltk.RegexpParser(chunkgram)
    chunked=chunkParser.parse(tagged)
    for subtree in chunked.subtrees():
        if subtree.label()=="Chunk" :
            leaves=[leaf[0] for leaf in subtree.leaves()]
            mysent=' '.join(leaves)
            break
    if conjword == "but":
        for i in range(len(splitted)):
            if i>1:
                splitted[i]="^"+mysent+" "+splitted[i]
            else:
                splitted[i]=mysent+" "+splitted[i]
    else:
        for i in range(len(splitted)):
            splitted[i]=mysent+" "+splitted[i]
    return splitted
    
    
def sentencesplitter(ptree,sentence):
    splitted=[]
    for subtree in ptree:
        if type(subtree)==nltk.tree.Tree:
            label=subtree.label()
            if label in conjuction:
                if ptree.label() in clauselevel:
                    conjword=subtree.leaves()[0]
                    sentence=sentence.replace(conjword,".")
                    splitted=sentokenizer.tokenize(sentence)
                    print splitted
                else:
                    if ptree.label() in phraselevel:
                        conjword=subtree.leaves()[0]
                        splitted=[]
                        for sub in ptree:
                            if sub != subtree:
                                splitted+=[' '.join(sub.leaves())]
                        splitted=sentenceformer(splitted,conjword,sentence)
                        print splitted
            if len(splitted)==0:
                splitted=sentencesplitter(subtree,sentence)
    return splitted
                
splittedsentences=[]
for sentence in sentences:
    parsed=parser.raw_parse(sentence)
    for ptree in parsed:
        ptree.pretty_print()
        output=sentencesplitter(ptree,sentence)
        if len(output)==0:
            splittedsentences+=[sentence]
        else:
            splittedsentences+=output               