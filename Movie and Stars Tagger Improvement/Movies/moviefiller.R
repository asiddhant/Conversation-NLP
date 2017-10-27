finaltest$pred=as.character(finaltest$pred)

preda1=c("NA",finaltest$pred[-length(finaltest$pred)])
finaltest$preda1=preda1
finaltest$preda1[finaltest$w_id==0]="NA"

predb1=c(finaltest$pred[-1],"NA")
finaltest$predb1=predb1
finaltest$predb1[finaltest$w_id!=0 & finaltest$flflag==1]="NA"

preda2=rep(NA,nrow(finaltest))
predb2=rep(NA,nrow(finaltest))

for(i in 1:nrow(finaltest)){
  if(i<=2){
    preda2[i]="NA"
  }
  if(i>2){
    preda2[i]=ifelse(finaltest$s_id[i]==finaltest$s_id[i-2],finaltest$pred[i-2],"NA")
  }
}

for(i in 1:nrow(finaltest)){
  if(i>(nrow(finaltest)-2)){
    predb2[i]="NA"
  }
  if(i<=(nrow(finaltest)-2)){
    predb2[i]=ifelse(finaltest$s_id[i]==finaltest$s_id[i+2],finaltest$pred[i+2],"NA")
  }
}

finaltest$preda2=preda2
finaltest$predb2=predb2

temptest=finaltest[,c(20,18,15,17,19)]
for(i in 1:nrow(temptest)){
  if (temptest$pred[i]=="O"){
    if ((temptest$preda2[i]=="B"|temptest$preda1[i]=="B") & (temptest$predb1[i]=="I"|temptest$predb2[i]=="I"))
      temptest$pred[i]="I"
  }
}

justforfun$modpred=temptest$pred
