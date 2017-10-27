import os
import pandas as pd

movies=pd.read_csv("movienames.csv",header=0,sep=",")
movies.index=movies['movieid']
for fn in os.listdir('.'):
    ffn=fn
    fn,ext = os.path.splitext(fn)
    if "_new" in fn:
        tmp=fn.find('_new')
        my=int(fn[tmp-4:tmp])
        mn=fn[0:tmp-5]
    else:
        tmp=len(fn)
        my=int(fn[tmp-4:tmp])
        mn=fn[0:tmp-5]
        
    movieids=movies.loc[(movies['title']==mn) & (movies['year']==my)].movieid 
    if len(movieids)==1:
        nn = str(int(movieids))
        nn = "".join([nn,ext])
        os.rename(ffn,nn)