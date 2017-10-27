dataset=read.csv("dataset.csv",stringsAsFactors = FALSE)
datasettag=read.csv("tagdataset.csv",stringsAsFactors = FALSE)

## Feature Extraction
poswordcount=rep(0,nrow(dataset))
negwordcount=rep(0,nrow(dataset))
queswordpres=rep(0,nrow(dataset))
negationcount=rep(0,nrow(dataset))

poswords=read.csv("poswords.csv",header = FALSE)
poswords=as.vector(poswords$V1)

negwords=read.csv("negwords.csv",header = FALSE)
negwords=as.vector(negwords$V1)

negationwords=c("not","n't","never","don't","won't","'nt","but","despite","though")

for (i in 1:nrow(dataset)){
  temp=subset(datasettag,datasettag$s_id==i)
  for (j in 1:nrow(temp)){
    if(tolower(temp$word[j]) %in% poswords)
      poswordcount[i]=poswordcount[i]+1
    if(tolower(temp$word[j]) %in% negwords)
      negwordcount[i]=negwordcount[i]+1
    if(tolower(temp$word[j]) %in% c("why","what"))
      queswordpres[i]=1
    if(tolower(temp$word[j]) %in% negationwords)
      negationcount[i]=negationcount[i]+1
  }
}

dataset$poswordcount=poswordcount
dataset$negwordcount=negwordcount
dataset$queswordpres=queswordpres
dataset$negationcount=negationcount

intentionword=rep(0,nrow(dataset))
verbword=rep(0,nrow(dataset))

intention=c("want","desire","plan","will","hope","'ll","need")
verb=c(synonyms("watch","VERB"),synonyms("finish","VERB"))

for (i in 1:nrow(dataset)){
  temp=subset(datasettag,datasettag$s_id==i)
  for (j in 1:nrow(temp))
    if(tolower(temp$word[j]) %in% intention)
      intentionword[i]=intentionword[i]+1
    if(tolower(temp$word[j]) %in% verb)
      verbword[i]=verbword[i]+1
}

dataset$intentionword=intentionword
dataset$verbword=verbword

