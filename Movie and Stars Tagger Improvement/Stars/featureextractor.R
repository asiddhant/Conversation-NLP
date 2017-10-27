poswords=read.csv("poswords.csv",header = FALSE,stringsAsFactors = FALSE)
negwords=read.csv("negwords.csv",header = FALSE,stringsAsFactors = FALSE)
words=c(poswords$V1,negwords$V1)
dataset=read.csv("datasetn.csv",stringsAsFactors = FALSE)

word2vec=dataset[,c(8:307)]
dataset=dataset[,-c(8:307)]

## First/Last Word Tagger
dataset$flflag=0
first=which(dataset$w_id==0)
last=first-1
last=c(last[-1],nrow(dataset))
dataset$flflag[c(first,last)]=1


## Windowed postags
postaga1=c("NA",dataset$postag[-length(dataset$postag)])
dataset$postaga1=postaga1
dataset$postaga1[dataset$w_id==0]="NA"

postagb1=c(dataset$postag[-1],"NA")
dataset$postagb1=postagb1
dataset$postagb1[dataset$w_id!=0 & dataset$flflag==1]="NA"

postaga2=rep(NA,nrow(dataset))
postagb2=rep(NA,nrow(dataset))

for(i in 1:nrow(dataset)){
  if(i<=2){
    postaga2[i]="NA"
  }
  if(i>2){
    postaga2[i]=ifelse(dataset$s_id[i]==dataset$s_id[i-2],dataset$postag[i-2],"NA")
  }
}

for(i in 1:nrow(dataset)){
  if(i>(nrow(dataset)-2)){
    postagb2[i]="NA"
  }
  if(i<=(nrow(dataset)-2)){
    postagb2[i]=ifelse(dataset$s_id[i]==dataset$s_id[i+2],dataset$postag[i+2],"NA")
  }
}

dataset$postaga2=postaga2
dataset$postagb2=postagb2

dataset=subset(dataset,select=c(s_id,w_id,word,postagb2,postagb1,postag,postaga1,postaga2,flflag,count,tag,stannertag))




setDict("C:/Program Files (x86)/WordNet/2.1/dict")
Sys.setenv(WNHOME = "C:/Program Files (x86)/WordNet/2.1") 
library(wordnet)
library(SnowballC)

## More Features - Intention Word
intwords=rep(NA,nrow(dataset))

for (i in 1:nrow(word2vec)){
  numbag=min(dataset$w_id[i],4)
  bag=c()
  for (j in 1:numbag)
    bag=c(bag,wordStem(tolower(dataset$word[i-j])))
  if(any(bag %in% words))
    intwords[i]=1
}
intwords[is.na(intwords)]=0

## More Features - Sentiment Word
sentwords=rep(NA,nrow(dataset))
temp=which(dataset$w_id==0)
temp=c(temp[-1],nrow(dataset)+1)
temp=temp-1
wordnum=dataset$w_id[temp]+1

for (i in 1:nrow(dataset)){
  sid=dataset$s_id[i]
  numbag=min(4,wordnum[sid]-dataset$w_id[i]-1)
  bag=c()
  for (j in 1:numbag)
    bag=c(bag,wordStem(tolower(dataset$word[i+j])))
  if(any(bag %in% words))
    sentwords[i]=1
  print (i)
}
sentwords[is.na(sentwords)]=0

finwords=as.integer(intwords|sentwords)
dataset$finwords=finwords

notapp=which(word2vec$X0==0)
for (i in notapp){
  tag=dataset$postag[i]
  subd=which(dataset$postag==tag)
  word2vec[i,]=apply(word2vec[subd,],2,mean)
}

library(gdata)
keep(dataset,word2vec,sure=TRUE)

library(qdapDictionaries)
abc=read.csv("a.csv",header = FALSE)
is.word  <- function(x) x %in% abc$V1

dataset$naivetag=ifelse((dataset$postag %in% c("NN","NNP","NNS","NNPS") & !is.word(tolower(dataset$word))),"P","O")


