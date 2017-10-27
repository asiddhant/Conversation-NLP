import numpy as np
import csv
import math
import pickle

def readUserMovieMapping():

	f = open('modelDump/'+'userMapping','rb');
	uMap = pickle.load(f);
	f.close();

	f = open('modelDump/'+'movieMapping','rb');
	mMap = pickle.load(f);
	f.close();

	return uMap,mMap

def readData(fileName):
	
	uMap = {}
	mMap = {}
	#tstart = time.time()
	reader = open(fileName,'r');
	# f = open(fileName,'r');
	# reader = csv.reader(f,delimiter="::");
	maxUser = 0;
	maxMovie = 0;
	ctr = 0;
	userList = {}
	movieList = {}
	time2000 = 60*60*24*365*30;
	for line in reader:
		ctr += 1;
		if ctr == 1:
			continue;

		lineVector = line.split(',');
		user = int(lineVector[0])
		movie = int(lineVector[1])
		ratingTime = int(lineVector[3])
		if ratingTime > time2000:
			if userList.has_key(user):
				userList[user] += 1
			else:
				userList[user] = 1

			if movieList.has_key(movie):
				movieList[movie] += 1
			else:
				movieList[movie] = 1

	reader.close();
	reader = open(fileName,'r');

	ctr = 0;
	for user in userList.keys():
		# if userList[user] > 250:
		ctr += 1;			
		uMap[user] = ctr;

	maxUser = ctr;
	ctr = 0;
	for movie in movieList.keys():
		# if movieList[movie] > 10:
		ctr += 1;			
		mMap[movie] = ctr;
		# else:
		# 	print movie,ctr

	# temp = [movieList[movie] for movie in movieList.keys() if movieList[movie] < 30]
	# print temp
	
	maxMovie =  ctr
	# ratingData is maxUser+1 because users are given IDs starting from 1 and I don't want to use -1 with userId everywhere I try to access them

	print maxUser,maxMovie
	# ratingData = np.zeros((maxUser+1,maxMovie+1))
	# print 'RatingData Size',ratingData.shape
	ctr = 0;
	ratingData = {}
	for line in reader:
		ctr += 1;
		if ctr == 1:
			continue;

		lineVector = line.split(',');
		user = int(lineVector[0])
		movie = int(lineVector[1])
		rating = float(lineVector[2]);
		if uMap.has_key(user) and mMap.has_key(movie):
			if ratingData.has_key(uMap[user]):
				ratingData[uMap[user]][mMap[movie]] = rating;
			else:
				ratingData[uMap[user]] = {}
				ratingData[uMap[user]][mMap[movie]] = rating;

	# for key in uMap.keys():
	# 	print key,uMap[key]
	# print '------------'
	# for key in mMap.keys():
	# 	print key,mMap[key]
	#dumpUserMovieMapping(uMap,mMap);
	return ratingData,maxUser,maxMovie

def getMovieData(fileName):

	uMap,mMap = readUserMovieMapping();
	reader 		= open(fileName,'r');
	reader = csv.reader(reader);
	movieList 	= {};
	ctr = 0
	for line in reader:
		ctr += 1
		if ctr ==1:
			continue;
		lineVector 	= line
		movieId 	= int(lineVector[0])
		movieName 	= lineVector[1]
		numRating 	= int(lineVector[3])
		movieYear 	= int(lineVector[4])
		avgRating 	= float(lineVector[5])
		temp 		= lineVector[6].split(' ');
		genreList=["adventure","animation","children","comedy","fantasy","romance","drama","action","crime", "thriller","horror","mystery","sci.fi","imax","documentary","war","musical","western","film.noir"]
		movieGenre  = []
		ctr = 0;
		for genre in temp:
			if genre.strip() == '1':
				movieGenre += [genreList[ctr]]
			ctr += 1

		temp = lineVector[7].split(' ');
		starList = []
		for star in temp:
			try:
				starList += [int(star)];
			except:
				pass

		if mMap.has_key(movieId):
			movieId = mMap[movieId];
			movieList[movieId] = {'name':movieName,'numRating':numRating,'avgRating':avgRating,'year':movieYear,'star':starList,'genre':movieGenre}
	
	return movieList;
 


def getContentBasedPreference(ratingData,movieData):
	uMap,mMap = readUserMovieMapping(); surveyweight=0.6;

	# ratingData,maxUser,maxMovie = readData(ratingFileName)
	genreList =["adventure","animation","children","comedy","fantasy","romance","drama","action","crime", "thriller","horror","mystery","sci.fi","imax","documentary","war","musical","western","film.noir"];
	f = open('data/users.csv');
	reader = csv.reader(f);

	userAltPreference = {}
	sCtr = 0
	for line in reader:
		sCtr += 1;
		if sCtr == 1:
			continue;
		userId = int(line[0]); userId = uMap[userId];      
	
		userAltPreference[userId] = {}
		userAltPreference[userId]['weights'] = {}
		userAltPreference[userId]['genre'] = {}

		weightNormaliser = 0.0;
		userAltPreference[userId]['weights']['genre'] 	= int(line[7]);
		weightNormaliser += int(line[7])
		userAltPreference[userId]['weights']['star'] 	= int(line[8]);
		weightNormaliser += int(line[8])
		userAltPreference[userId]['weights']['ratings'] = int(line[9])
		weightNormaliser += int(line[9])
		for key in userAltPreference[userId]['weights'].keys():
			userAltPreference[userId]['weights'][key] = userAltPreference[userId]['weights'][key]/weightNormaliser;

		genreNormaliser = 0.0 
		# ACF
		userAltPreference[userId]['genre']["animation"] = int(line[11])
		genreNormaliser += int(line[11])
		userAltPreference[userId]['genre']["children"] 	= int(line[11])
		genreNormaliser += int(line[11])
		userAltPreference[userId]['genre']["fantasy"] 	= int(line[11])
		genreNormaliser += int(line[11])
		# CTM
		userAltPreference[userId]['genre']["crime"] 	= int(line[12])
		genreNormaliser += int(line[12])
		userAltPreference[userId]['genre']["thriller"] 	= int(line[12])
		genreNormaliser += int(line[12])
		userAltPreference[userId]['genre']["mystery"] 	= int(line[12])
		genreNormaliser += int(line[12])
		# AAS
		userAltPreference[userId]['genre']["adventure"] = int(line[13])
		genreNormaliser += int(line[13])
		userAltPreference[userId]['genre']["action"] 	= int(line[13])
		genreNormaliser += int(line[13])
		userAltPreference[userId]['genre']["sci.fi"] 	= int(line[13])
		genreNormaliser += int(line[13])
		# H
		userAltPreference[userId]['genre']["horror"] 	= int(line[14])
		genreNormaliser += int(line[14])
		# RCD
		userAltPreference[userId]['genre']["romance"] 	= int(line[15])
		genreNormaliser += int(line[15])
		userAltPreference[userId]['genre']["comedy"] 	= int(line[15])
		genreNormaliser += int(line[15])
		userAltPreference[userId]['genre']["drama"] 	= int(line[15])
		genreNormaliser += int(line[15])
		# WWMF
		userAltPreference[userId]['genre']["war"] 		= int(line[16])
		genreNormaliser += int(line[16])
		userAltPreference[userId]['genre']["musical"] 	= int(line[16])
		genreNormaliser += int(line[16])
		userAltPreference[userId]['genre']["western"] 	= int(line[16])
		genreNormaliser += int(line[16])
		userAltPreference[userId]['genre']["film.noir"]	= int(line[16])
		genreNormaliser += int(line[16])

		userAltPreference[userId]['genre']["imax"] 		= 3;
		genreNormaliser += 3
		userAltPreference[userId]['genre']["documentary"] 	= 2;
		genreNormaliser += 2

		for key in userAltPreference[userId]['genre'].keys():
			userAltPreference[userId]['genre'][key] = userAltPreference[userId]['genre'][key] /float(genreNormaliser);

		for key in userAltPreference[userId]['genre'].keys():
			print userId,key,"{0:.3f}".format(userAltPreference[userId]['genre'][key])
#			try:
#				print userId,key,"{0:.3f}".format(userPreference[userId]['genre'][key]['score'])
#			except:
#				print "-->",userId,key

		# print userId,"{0.:3f}".format(userAltPreference[userId]['genre']);
		# print userId,"{0.:3f}".format(userPreference[userId]['genre']);

#	f = open('modelDump/userContentPreference','wb')
#	pickle.dump(userPreference, f)
#	f.close();

	userPreference = {}
	maxUserStar = 20
         
	for user in userAltPreference.keys():
		for movie in ratingData[user].keys():
			movieGenreList = movieData[movie]['genre'];
			moviestarList  = movieData[movie]['star'];

			if userPreference.has_key(user):
				for star in moviestarList:
					if userPreference[user]['star'].has_key(star):
						userPreference[user]['star'][star]['ratings'] += [ratingData[user][movie]]
					else:
						userPreference[user]['star'][star] = {}
						userPreference[user]['star'][star]['ratings'] = [ratingData[user][movie]]

				for movieGenre in movieGenreList:
					userPreference[user]['genre'][movieGenre]['ratings'] += [ratingData[user][movie]]

			else:
				userPreference[user] = {}
				userPreference[user]['genre'] 	= {}
				userPreference[user]['star'] 	= {}

				for star in moviestarList:
					userPreference[user]['star'][star] = {}
					userPreference[user]['star'][star]['ratings'] = [ratingData[user][movie]]

				for genre in genreList:
					userPreference[user]['genre'][genre] = {} 
					userPreference[user]['genre'][genre]['ratings'] = [] # List of ratings

				for movieGenre in movieGenreList:
					userPreference[user]['genre'][movieGenre]['ratings'] += [ratingData[user][movie]]


		# Calculating star preferences of user
		ctr = 0.0
		meanNumStarRating = 0.0
		for star in userPreference[user]['star'].keys():
			if len(userPreference[user]['star'][star]['ratings']) > 0:
				meanNumStarRating += len(np.array(userPreference[user]['star'][star]['ratings']))
				ctr += 1

		meanNumStarRating /= ctr;
		for star in userPreference[user]['star'].keys():
			if len(userPreference[user]['star'][star]['ratings']) > 0:
				tempMeanRating 	= np.mean(np.array(userPreference[user]['star'][star]['ratings']))
				tempNumRating 	= len(userPreference[user]['star'][star]['ratings'])
				userPreference[user]['star'][star]['score'] 		= tempMeanRating*( 1 - math.exp(-1*tempNumRating/float(meanNumStarRating)));
				# print user,star,'star',userPreference[user]['star'][star]['score'],tempMeanRating,math.exp(-1*tempNumRating/float(meanNumStarRating)),tempNumRating,meanNumStarRating
			else:
				userPreference[user]['star'][star]['score'] 		= 0

			del userPreference[user]['star'][star]['ratings']

		sortedList = sorted(userPreference[user]['star'].iteritems(), key = lambda (key,val):val['score'] , reverse = True)
		ctr = 0
		# print user , len(sortedList)
		starTotalScore = 0.0
		for (key,val) in sortedList:
			ctr += 1
			if ctr > maxUserStar:
				del userPreference[user]['star'][key];
			else:
				# print key,val
				starTotalScore += userPreference[user]['star'][key]['score']
				pass

		for star in userPreference[user]['star'].keys():
			userPreference[user]['star'][star]['score'] /= starTotalScore;
			# print user,'-->',userPreference[user]['star'][star]['score']

		# sortedList = sorted(userPreference[user]['star'].iteritems(), key = lambda (key,val):val['score'] , reverse = True)
		# print '-->',user , len(sortedList)

		# Calculating movie preference for user
		meanNumGenreRating = 0.0;
		ctr = 0;
		for movieGenre in genreList:
			if len(userPreference[user]['genre'][movieGenre]['ratings']) > 0:
				meanNumGenreRating 	+= len(userPreference[user]['genre'][movieGenre]['ratings']);
				ctr += 1;

		meanNumGenreRating /= ctr;

		genreTotalScore = 0.0
		for movieGenre in genreList:
			if len(userPreference[user]['genre'][movieGenre]['ratings']) > 0:
				tempMeanRating 	= np.mean(np.array(userPreference[user]['genre'][movieGenre]['ratings']))
				tempNumRating 	= len(userPreference[user]['genre'][movieGenre]['ratings']);
				userPreference[user]['genre'][movieGenre]['score'] 		= tempMeanRating*( 1 -  math.exp(-1*tempNumRating/float(meanNumGenreRating)));
				# print user,movieGenre,'genre',userPreference[user]['genre'][movieGenre]['score']
			else:
				userPreference[user]['genre'][movieGenre]['score'] 		= 0;

			genreTotalScore += userPreference[user]['genre'][movieGenre]['score'];
			del userPreference[user]['genre'][movieGenre]['ratings']

		for movieGenre in genreList:
			userPreference[user]['genre'][movieGenre]['score'] /= genreTotalScore;
			# print user,'-->',userPreference[user]['genre'][movieGenre]['score']

		for user in userPreference.keys():
			for genre in genreList:
                		if userPreference[user]['genre'][genre]['score']==0:
                                 userPreference[user]['genre'][genre]['score']=userAltPreference[user]['genre'][genre]
                                 else:
                                 userPreference[user]['genre'][genre]['score']=surveyweight*userAltPreference[user]['genre'][genre]+(1-surveyweight)*userPreference[user]['genre'][genre]['score']
    		userPreference[user]['weights']=userAltPreference[user]['weights']
   
   
	
	return userPreference
 
def main():
    movieData = getMovieData('movienames.csv');
    ratingData,maxUser,maxMovie = readData('ratings.csv')
    userpref=getContentBasedPreference(ratingData,movieData)