stars=read.csv("asentences.csv",stringsAsFactors = FALSE)
stars=as.vector(as.matrix(stars[,3:6]))
stars=stars[-which(is.na(stars))]


naivestars=read.csv("naivestars.csv")
naivestars=as.vector(naivestars$naivestars)

chunkstars=read.csv("chunkstars.csv")
chunkstars=as.vector(chunkstars$chunkstars)

modelstars=read.csv("modelstars.csv")
modelstars=as.vector(modelstars$modelstars)

groundstars=read.csv("groundstars.csv")
groundstars=as.vector(groundstars$groundstars)

##P AND R

np=length(which(naivestars %in% stars))/length(naivestars)
nr=length(which(naivestars %in% stars))/length(stars)


##P AND R

cp=length(which(chunkstars %in% stars))/length(chunkstars)
cr=length(which(chunkstars %in% stars))/length(stars)

##P AND R

mp=length(which(modelstars %in% stars))/length(modelstars)
mr=length(which(modelstars %in% stars))/length(stars)

##P AND R

gp=length(which(groundstars %in% stars))/length(groundstars)
gr=length(which(groundstars %in% stars))/length(stars)

