import os
import pandas as pd

dflist=[]
#Put Path Name Here
path="C:\\Users\\asiddhan\\Desktop\\Combiner\\"
for fn in os.listdir(path):
    ffn,ext = os.path.splitext(fn)
    if ext==".csv" and "session" not in ffn:
        dflist+=[pd.read_csv(fn,header=0,sep=",")]

alldf=dflist[0]
i=1
while i < len(dflist):
    alldf=alldf.append(dflist[i])
    i+=1
    
    
alldf=alldf.sort_values(by='timestamp')
alldf=alldf[['s_id','u_id','sentence']]
alldf.s_id=range(1,alldf.shape[0]+1)

alldf.to_csv(path+"session.csv",index=False,sep=",")