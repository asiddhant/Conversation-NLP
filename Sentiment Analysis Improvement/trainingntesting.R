dataset=read.csv("dataset.csv",stringsAsFactors = FALSE)

#DataPreparation

for (i in c(10,14:16)){
  dataset[,i]=as.factor(dataset[,i])
}
rm(i)


library(caret)

trControl = trainControl(method = "repeatedcv",number = 4,repeats = 10)
tuneGrid =  expand.grid(interaction.depth = c(1,3), n.trees = c(1,2,3)*50,shrinkage = c(0.1,0.2), n.minobsinnode = c(10,20,40))
model_GBM = train(groundtruth~.,
                 data = dataset[,-c(1,2,15)],
                 method="gbm",
                 tuneGrid=tuneGrid,
                 trControl=trControl)

shuffler=sample(1:300)
dataset=dataset[shuffler,]

split=101:300
traindata=subset(dataset,dataset$s_id %in% split)
testdata=subset(dataset,!dataset$s_id %in% split)
library(randomForest)
model_RFt=randomForest(groundtruth~.,data = traindata[,-c(1:2,15)],ntree=500,mtry=4)
output=predict(model_RFt,newdata = testdata)
table(output,testdata$groundtruth)
testdata$pred=output

split=c(1:100,201:300)
traindata=subset(dataset,dataset$s_id %in% split)
testdata2=subset(dataset,!dataset$s_id %in% split)
library(randomForest)
model_RFt=randomForest(groundtruth~.,data = traindata[,-c(1:2,15)],ntree=500,mtry=4)
output=predict(model_RFt,newdata = testdata2)
table(output,testdata2$groundtruth)
testdata2$pred=output

split=1:200
traindata=subset(dataset,dataset$s_id %in% split)
testdata3=subset(dataset,!dataset$s_id %in% split)
library(randomForest)
model_RFt=randomForest(groundtruth~.,data = traindata[,-c(1:2,15)],ntree=500,mtry=4)
output=predict(model_RFt,newdata = testdata3)
table(output,testdata3$groundtruth)
testdata3$pred=output

finaltest=rbind(testdata,testdata2,testdata3)
table(finaltest$groundtruth,finaltest$pred)

