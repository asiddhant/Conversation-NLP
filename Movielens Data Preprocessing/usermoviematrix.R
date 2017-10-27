movies=read.csv("movies.csv",stringsAsFactors = FALSE)
ratings=read.csv("ratings.csv",stringsAsFactors = FALSE)

ratings=subset(ratings,ratings$movieId %in% movies$movieid)
usercount= as.data.frame.table(table(ratings$userId))
usercount = usercount[order(-usercount$Freq),]

ratings=subset(ratings,ratings$userId %in% usercount$Var1[1:80000])

usercount = usercount[1:80000,]

#80000 Users & 14000 Movies
usermovie=matrix(data=NA,nrow=80000,ncol=13786)
rownames(usermovie)=usercount$Var1
colnames(usermovie)=movies$movieid


for(i in 1:nrow(ratings)){
  usermovie[toString(ratings$userId[i]),toString(ratings$movieId[i])]=ratings$rating[i]
}