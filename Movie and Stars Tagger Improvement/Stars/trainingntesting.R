#DataPreparation

for (i in c(4:9,11:14)){
  dataset[,i]=as.factor(dataset[,i])
}
rm(i)


library(randomForest)

split=41:124
split=sort(split)
traindata=subset(dataset,dataset$s_id %in% split)
testdata=subset(dataset,!dataset$s_id %in% split)
library(randomForest)
model_RF=randomForest(tag~.,data = traindata[,-c(1:3)],ntree=500,mtry=4)
output=predict(model_RF,newdata = testdata)
table(output,testdata$tag)
testdata$pred=output

split=c(1:40,81:124)
split=sort(split)
traindata=subset(dataset,dataset$s_id %in% split)
testdata2=subset(dataset,!dataset$s_id %in% split)
library(randomForest)
model_RF=randomForest(tag~.,data = traindata[,-c(1:3)],ntree=500,mtry=4)
output=predict(model_RF,newdata = testdata2)
table(output,testdata2$tag)
testdata2$pred=output

split=1:80
split=sort(split)
traindata=subset(dataset,dataset$s_id %in% split)
testdata3=subset(dataset,!dataset$s_id %in% split)
library(randomForest)
model_RF=randomForest(tag~.,data = traindata[,-c(1:3)],ntree=500,mtry=4)
output=predict(model_RF,newdata = testdata3)
table(output,testdata3$tag)
testdata3$pred=output

finaltest=rbind(testdata,testdata2,testdata3)

justforfun = finaltest[,c(1,2,3,14,12,15,11)]
names(justforfun)=c(names(justforfun)[1:4],"stanfordtag","modeltag","groundtruth")
write.csv(justforfun,"finaloutput.csv",row.names = FALSE)
