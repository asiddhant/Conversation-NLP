users=read.csv("users.csv",stringsAsFactors = FALSE)


cleaner=function(x){
  gsub("[^a-zA-Z0-9 ]","",x)
}

users$Name=sapply(users$Name,cleaner)
users$Age=as.numeric(sapply(users$Age,cleaner))
users$Gender=as.factor(sapply(users$Gender,cleaner))

users$pref=NA
for (i in 1:nrow(users)){
  temp=names(which.max(users[i,12:17]))
  users$pref[i]=genrenames[temp]
}

usersuse=users[,c(1,5,4,18)]
usersuse$Gender=ifelse(usersuse$Gender=="M",1,0)
