users$Cluster1=as.factor(users$Cluster1)
users$Cluster2=as.factor(users$Cluster2)
users$Cluster3=as.factor(users$Cluster3)

combinations=combn(users$UserId,3)

groupmatrix=matrix(NA,nrow=ncol(combinations),ncol=25)
groupmatrix=as.data.frame(groupmatrix)
names(groupmatrix)=c("m1","m2","m3","groupavg","groupcount","prefvar","genrevar","domvar","expvar","countvar",
                     tolower(names(users)[6:17]),"clus1var","clus2var","clus3var")

for(i in 1:nrow(groupmatrix)){
  usergroup=users[users$UserId %in% combinations[,i],]
  groupmatrix$m1[i]=usergroup$UserId[1]
  groupmatrix$m2[i]=usergroup$UserId[2]
  groupmatrix$m3[i]=usergroup$UserId[3]
  groupmatrix$groupavg[i]=sum(usergroup$AvgRating*usergroup$MovieCount)/sum(usergroup$MovieCount)
  groupmatrix$groupcount[i]=mean(usergroup$MovieCount)
  groupmatrix$prefvar[i]=mean(dist(usergroup[,c(8:11)]))
  groupmatrix$genrevar[i]=mean(dist(usergroup[,12:17]))
  groupmatrix$domvar[i]=var(usergroup$Domination)
  groupmatrix$expvar[i]=var(usergroup$Noofmovies)
  groupmatrix$countvar[i]=var(usergroup$MovieCount)
  groupmatrix[i,11:22]=as.numeric(sapply(usergroup[,6:17],mean))
  groupmatrix$clus1var[i]=length(unique(usergroup$Cluster1))
  groupmatrix$clus2var[i]=length(unique(usergroup$Cluster2))
  groupmatrix$clus3var[i]=length(unique(usergroup$Cluster3))
  print(i)
}

## Picking Up 12 Groups
