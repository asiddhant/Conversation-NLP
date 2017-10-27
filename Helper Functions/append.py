import numpy as np
import csv
import math
import pickle
surveyweight=0.6;
for user in userPreference.keys():
    for genre in genreList:
        if userPreference[user]['genre'][genre]['score']==0:
            userPreference[user]['genre'][genre]['score']=userAltPreference[user]['genre'][genre]
        else:
            userPreference[user]['genre'][genre]['score']=surveyweight*userAltPreference[user]['genre'][genre]+(1-surveyweight)*userPreference[user]['genre'][genre]['score']
    userPreference[user]['weights']=userAltPreference[user]['weights']
            