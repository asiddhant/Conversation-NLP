movienames=read.csv("movienames.csv")
movienames$title=sapply(movienames$title,tolower)


removestopwords=function(x){
  words = unlist(strsplit(x, " ", fixed = TRUE))
  pos=which(words %in% stopwords(kind="en"))
  if(length(pos)>0)
    words = words[-pos]
  key=paste(words, collapse=" ")
  return(key)
}

movienames$titlekey=sapply(movienames$title,removestopwords)

removenonascii = function(x){
  gsub("[^[:alnum:] ]", "", x)
}

movienames$title=sapply(movienames$title,removenonascii)


genre$sub.genre=sapply(genre$sub.genre,tolower)
genre$genre=sapply(genre$genre,tolower)

stars=read.csv("starcast.csv",stringsAsFactors = FALSE)
stars$mstars=sapply(stars$stars,tolower)
stars$mstars=sapply(stars$mstars,removenonascii)
stars=stars[-which(stars$noofmovies<2),]
write.csv(stars,"starcast.csv",row.names = FALSE)
