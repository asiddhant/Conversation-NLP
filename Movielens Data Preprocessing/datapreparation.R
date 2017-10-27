movies=read.csv("movienames.csv",stringsAsFactors = FALSE)
stars=read.csv("starcast.csv",stringsAsFactors = FALSE)

nameidmapper=function(x){
  if(nchar(x)>0){
    a=as.numeric(stars$star_id[which(stars$stars==x)])
    if(length(a)==0)
      return(0)
    else
      return(a)
  }
  else
    return(0)
}

for (i in 26:31){
  for (j in 1:nrow(movies))
    movies[j,i]=nameidmapper(movies[j,i])
  print (i)
}

idmoviemapper=function(x){
  a=c()
  for( i in 26:31)
    a=c(a,movies$movieid[which(movies[,i]==x)])
  a=unique(a)
  return(paste(a,collapse = " "))
}

idratings=function(x){
  a=c()
  for( i in 26:31)
    a=c(a,movies$movieid[which(movies[,i]==x)])
  a=unique(a)
  ratings=sum(movies$ratings[which(movies$movieid %in% a)])/length(a)
  return(ratings)
}

idpop=function(x){
  a=c()
  for( i in 26:31)
    a=c(a,movies$movieid[which(movies[,i]==x)])
  a=unique(a)
  pop=sum(movies$num[which(movies$movieid %in% a)])
  return(pop)
}

idyear=function(x){
  a=c()
  for( i in 26:31)
    a=c(a,movies$movieid[which(movies[,i]==x)])
  a=unique(a)
  year=sum(movies$year[which(movies$movieid %in% a)])/length(a)
  return(round(year))
}

idgenre=function(x){
  b=rep(0,19)
  a=c()
  for( i in 26:31)
    a=c(a,movies$movieid[which(movies[,i]==x)])
  a=unique(a)
  for(j in a){
    for (i in 1:19){
      b[i]=b[i]+movies[which(movies$movieid==j),i+5]
    }
  }
  return(paste(b,collapse = ":")) 
}

stars$movies=sapply(stars$star_id,idmoviemapper)
stars$ratings=sapply(stars$star_id,idratings)
stars$pop=sapply(stars$star_id,idpop)
stars$year=sapply(stars$star_id,idyear)
stars$adventure=sapply(stars$star_id,idgenre)

for(i in 1:nrow(starcast)){
  b=starcast[i,9:27]
  b=paste(b,collapse=" ")
  starcast$genre[i]=b
}

for(i in 1:nrow(movienames)){
  b=movienames[i,7:12]
  b=b[b!=0]
  if(length(b)>0){
    b=unique(b)
    b=paste(b,collapse=" ")
    movienames$stars[i]=b
  }
}