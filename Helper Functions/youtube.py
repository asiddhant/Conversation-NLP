import urllib
import urllib2
from bs4 import BeautifulSoup
import pandas as pd

movies=pd.read_csv("movienames.csv",header=0,sep=",")

def linkfinder(query):
    textToSearch = query + ' trailer'
    query = urllib.quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib2.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html,"lxml")
    links=[]
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        links+=['https://www.youtube.com' + vid['href']]
    return links[0]
    
movielinks=[]
for i in range(2733,movies.shape[0]):
    try:
        mov=movies.iloc[i]
        mname=mov.org_title
        myear=mov.year
        query = mname +' '+str(myear)
        movielinks+=[linkfinder(query)]
        if i%10==0:
            print i
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        movielinks+=["NA"]
        print "kuch nahi mila"
        if i%10==0:
            print i

movielinksdf=pd.DataFrame(movielinks)