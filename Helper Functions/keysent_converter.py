import os
import pandas as pd

movies=pd.read_csv("movienames.csv")
stars=pd.read_csv("starcast.csv")

for fn in os.listdir('.'):
    ffn,ext = os.path.splitext(fn)
    if "keysent" in ffn:
        df=pd.read_csv(fn,sep=",",header=0)
        for i in range(df.shape[0]):
            key=df.key[i]
            tag=df.tag[i]
            if tag=="m":
                try:
                    keyword=movies.title[movies.movieid==int(key)].tolist()[0]
                    df.key[i]=keyword
                except:
                    print "hagdiya"
                    df.key[i]="hagdiya"
            if tag=="s":
                try:
                    keyword=stars.stars[stars.star_id==int(key)].tolist()[0]
                    df.key[i]=keyword
                except:
                    print "hagdiya"
                    df.key[i]="hagdiya"
        df.to_csv(fn,sep=",",index=False)
