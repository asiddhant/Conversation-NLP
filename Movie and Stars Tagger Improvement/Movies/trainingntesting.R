#DataPreparation

for (i in c(4:10,12:14)){
  dataset[,i]=as.factor(dataset[,i])
}
rm(i)


library(randomForest)

split=sample(1:max(dataset$s_id),80)
split=sort(split)
traindata=subset(dataset,dataset$s_id %in% split)
testdata=subset(dataset,!dataset$s_id %in% split)

model_RF=randomForest(tag~.,data = traindata[,-c(1:3)],ntree=500,mtry=4)
output=predict(model_RF,newdata = testdata)
