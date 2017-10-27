import pandas as pd
from bs4 import BeautifulSoup  
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from sklearn.ensemble import RandomForestClassifier

wordnet_lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()
train=pd.read_csv("labeledTrainData.tsv",header=0,
                      delimiter="\t",quoting=3)
    
def review_to_words(raw_review):
    example1=BeautifulSoup(raw_review)               
    letters_only=re.sub("[^a-zA-Z]",
                        " ",
                        example1.get_text())
    lower_case=letters_only.lower()
    words=lower_case.split()
    words=[w for w in words if not w in stopwords.words("english")]

    for i in range(len(words)):  
        words[i]=wordnet_lemmatizer.lemmatize(words[i])
    
    return(" ".join(words))
    
num_reviews=train["review"].size
clean_train_reviews=[]

for i in xrange(0,num_reviews):
    if( (i+1)%1000 == 0 ):
        print "Review %d of %d\n" % ( i+1, num_reviews )
    clean_train_reviews.append(review_to_words(train["review"][i]))

vectorizer = CountVectorizer(analyzer="word",
                             tokenizer=None,
                             preprocessor=None,
                             stop_words=None,
                             max_features=5000)
                             
train_data_features=vectorizer.fit_transform(clean_train_reviews)
train_data_features=train_data_features.toarray()

vocab = vectorizer.get_feature_names()
dist=np.sum(train_data_features,axis=0)
for tag, count in zip(vocab, dist):
    print count, tag    

forest=RandomForestClassifier(n_estimators=100)
forest=forest.fit(train_data_features,train["sentiment"])


test=pd.read_csv("testData.tsv",header=0,delimiter="\t",
                 quoting=3)
num_reviews = len(test["review"])
clean_test_reviews = [] 

for i in xrange(0,num_reviews):
    if( (i+1) % 1000 == 0 ):
        print "Review %d of %d\n" % (i+1, num_reviews)
    clean_review = review_to_words( test["review"][i] )
    clean_test_reviews.append( clean_review )

test_data_features = vectorizer.transform(clean_test_reviews)
test_data_features = test_data_features.toarray()

result = forest.predict(test_data_features)
output = pd.DataFrame( data={"id":test["id"], "sentiment":result} )
output.to_csv( "Bag_of_Words_model.csv", index=False, quoting=3 )