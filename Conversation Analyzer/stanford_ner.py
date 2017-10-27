st = StanfordNERTagger('C:/Users/asiddhan/Downloads/stanford-ner-2015-12-09/stanford-ner-2015-12-09/classifiers/english.all.3class.distsim.crf.ser.gz',
					   'C:/Users/asiddhan/Downloads/stanford-ner-2015-12-09/stanford-ner-2015-12-09/stanford-ner.jar',
					   encoding='utf-8')

import os
java_path = "C:/Program Files (x86)/Java/jre1.8.0_91/bin/java.exe"
os.environ['JAVAHOME'] = java_path

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize

def extractor(sentence,splitted):
    words=nltk.word_tokenize(sentence)
    extracted=[]
    for word in words:
        for sentence in splitted:
            if not word in sentence:
                extracted+=[word]
    return ' '.join(extracted)