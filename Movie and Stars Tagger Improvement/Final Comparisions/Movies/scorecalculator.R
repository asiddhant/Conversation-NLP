movies=read.csv("msentences.csv",stringsAsFactors = FALSE)
movies=as.vector(as.matrix(movies[,3:10]))
movies=movies[-which(is.na(movies))]


naivemovies=read.csv("naivemovies.csv")
naivemovies=as.vector(naivemovies$naivemovies)

chunkmovies=read.csv("chunkmovies.csv")
chunkmovies=as.vector(chunkmovies$chunkmovies)

modelmovies=read.csv("modelmovies.csv")
modelmovies=as.vector(modelmovies$modelmovies)

groundmovies=read.csv("groundmovies.csv")
groundmovies=as.vector(groundmovies$groundmovies)

##P AND R

np=length(which(naivemovies %in% movies))/length(naivemovies)
nr=length(which(naivemovies %in% movies))/length(movies)


##P AND R

cp=length(which(chunkmovies %in% movies))/length(chunkmovies)
cr=length(which(chunkmovies %in% movies))/length(movies)

##P AND R

mp=length(which(modelmovies %in% movies))/length(modelmovies)
mr=length(which(modelmovies %in% movies))/length(movies)

##P AND R

gp=length(which(groundmovies %in% movies))/length(groundmovies)
gr=length(which(groundmovies %in% movies))/length(movies)

