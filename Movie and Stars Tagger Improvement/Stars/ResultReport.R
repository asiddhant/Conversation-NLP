penalmat=matrix(c(0,1,2,1,0,1,2,1,0),nrow=3,ncol = 3,byrow = TRUE)
## Text Blob Results
blobtable=table(dataset$groundtruth,dataset$bloblab)
bacc=sum(diag(blobtable))/nrow(dataset)
bpns=sum(blobtable*penalmat)/nrow(dataset)

## NLTK Results
nltktable=table(dataset$groundtruth,dataset$nltklab)
nacc=sum(diag(nltktable))/nrow(dataset)
npns=sum(nltktable*penalmat)/nrow(dataset)

## Model Results
modeltable=table(dataset$groundtruth,dataset$modeloutput)
macc=sum(diag(modeltable))/nrow(dataset)
mpns=sum(modeltable*penalmat)/nrow(dataset)