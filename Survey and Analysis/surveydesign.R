movies=read.csv("movies.csv",stringsAsFactors = FALSE)
movies2=read.csv("movies2.csv",stringsAsFactors = FALSE)
movies2=subset(movies2,movies2$movieId %in% movies$movieid)


movies=movies[order(movies$movieid),]
movies2=movies2[order(movies2$movieId),]

movies$genre=movies2$genres
rm(movies2)


movies2=subset(movies,movies$year>1970 & movies$num>4000 & movies$ratings>2)


crithrimys = subset(movies2,movies2$crime==1 | movies2$thriller==1 | movies2$mystery==1)
crithrimys=crithrimys[,-c(1,4:25,30:31)]
write.csv(crithrimys,"crithrimis.csv",row.names = FALSE)

romcomdram = subset(movies2,movies2$romance==1 | movies2$comedy==1 | movies2$drama==1)
romcomdram=romcomdram[,-c(1,4:25,30:31)]
write.csv(romcomdram,"romcomdram.csv",row.names = FALSE)

anichilfan = subset(movies2,movies2$animation==1 | movies2$children==1 | movies2$fantasy==1)
anichilfan=anichilfan[,-c(1,4:25,30:31)]
write.csv(anichilfan,"anichilfan.csv",row.names = FALSE)

horror = subset(movies2,movies2$horror==1)
horror =horror[,-c(1,4:25,30:31)]
write.csv(horror,"horror.csv",row.names = FALSE)

advactsci = subset(movies2,movies2$adventure==1 | movies2$action==1 | movies2$sci.fi==1)
advactsci = advactsci [,-c(1,4:25,30:31)]
write.csv(advactsci,"advactsci.csv",row.names = FALSE)

muswarwes = subset(movies2,movies2$war==1 | movies2$western==1 | movies2$musical==1 | movies2$film.noir==1)
muswarwes = muswarwes[,-c(1,4:25,30:31)]
write.csv(muswarwes,"muswarwes.csv",row.names = FALSE)

