movies=read.csv("movies.csv",stringsAsFactors = FALSE)
ratings=read.csv("ratings.csv",stringsAsFactors = FALSE)

movie_gmm=movies[,-c(2,23:32)]
movie_gmm$year=as.numeric(scale(movie_gmm$year))

group1=sample(1:1000,nrow(movies),replace=TRUE)
group2=sample(1:1000,nrow(movies),replace=TRUE)
group3=sample(1:1000,nrow(movies),replace=TRUE)
group1=group1/sum(group1)
group2=group2/sum(group2)
group3=group3/sum(group3)

g1=rep(0,19)
names(g1)=names(movie_gmm[3:21])
for (i in names(g1)){
  g1[i]=sum(movie_gmm[,i]*group1)
}

g2=rep(0,19)
names(g2)=names(movie_gmm[3:21])
for (i in names(g2)){
  g2[i]=sum(movie_gmm[,i]*group2)
}

g3=rep(0,19)
names(g3)=names(movie_gmm[3:21])
for (i in names(g3)){
  g3[i]=sum(movie_gmm[,i]*group3)
}
 