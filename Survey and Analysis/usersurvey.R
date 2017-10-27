users = read.csv("users.csv")
users$Name=as.character(users$Name)
users$Email=as.character(users$Email)

## Visualizing the Data
hist(users$Age)

for (i in 5:17){
  barplot(table(users[,i]),main=names(users)[i])
}
rm(i)

## Param1
p1data=users[,c(8:10)]
distances=dist(p1data,method = "euclidean")
clusterMovies = hclust(distances, method = "ward.D2") 
plot(clusterMovies)
clusterGroups = cutree(clusterMovies, k = 4)
tapply(users$Genre, clusterGroups, mean)
tapply(users$Actors, clusterGroups, mean)
tapply(users$Ratings, clusterGroups, mean)
tapply(users$Release.Year, clusterGroups, mean)


##Param2
p2data=users[,c(12:17)]
distances2=dist(p2data,method = "euclidean")
clusterMovies2 = hclust(distances2, method = "ward.D2") 
plot(clusterMovies2)
clusterGroups2 = cutree(clusterMovies2, k = 5)
tapply(users$ACF, clusterGroups2, mean)
tapply(users$CTM, clusterGroups2, mean)
tapply(users$AAS, clusterGroups2, mean)
tapply(users$H, clusterGroups2, mean)
tapply(users$RCD, clusterGroups2, mean)
tapply(users$WMF, clusterGroups2, mean)

##Param3
p3data=users[,c(8:17)]
distances3=dist(p3data,method = "euclidean")
clusterMovies3 = hclust(distances3, method = "ward.D2") 
plot(clusterMovies3)
clusterGroups3 = cutree(clusterMovies3, k = 3)
tapply(users$ACF, clusterGroups3, mean)
tapply(users$CTM, clusterGroups3, mean)
tapply(users$AAS, clusterGroups3, mean)
tapply(users$H, clusterGroups3, mean)
tapply(users$RCD, clusterGroups3, mean)
tapply(users$WMF, clusterGroups3, mean)
tapply(users$Genre, clusterGroups3, mean)
tapply(users$Actors, clusterGroups3, mean)
tapply(users$Ratings, clusterGroups3, mean)
tapply(users$Release.Year, clusterGroups3, mean)

fullusers=read.csv("ratings.csv")
