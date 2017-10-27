def starsextractor(wordset):
    stars=[]
    i=' '.join(wordset)
    for j in starcast['mstars']:
        dist = Levenshtein.distance(i,j) - max(li,lj) + min(li,lj)
        if dist<2 and not j in stars:
            stars=stars+[j]
    return stars