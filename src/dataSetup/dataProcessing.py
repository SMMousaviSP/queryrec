import itertools
import random

def generateLikedDislikeDictionary(usersIDs, queryIDs, utilityMatrix, averageRating):
    # Dictionary of users and their liked and disliked queries
    userQueryLikedDict = {key: [] for key in usersIDs}
    userQueryDislikedDict = {key: [] for key in usersIDs}

    # Dictionary of queries and the users who liked and disliked them
    queryUserLikedDict = {key: [] for key in queryIDs}
    queryUserDislikedDict = {key: [] for key in queryIDs}

    for row in utilityMatrix:
        currentUser = row[0]
        for rating, currentQuery in zip(row[1:], queryIDs):
            # Check if the user has rated the query
            if(rating):
                if(rating >= averageRating[currentUser]):
                    userQueryLikedDict[currentUser].append(queryIDs[currentQuery])
                    queryUserLikedDict[currentQuery].append(currentUser)
                else:
                    userQueryDislikedDict[currentUser].append(queryIDs[currentQuery])
                    queryUserDislikedDict[currentQuery].append(currentUser)

    return (
        userQueryLikedDict,
        userQueryDislikedDict,
        queryUserLikedDict,
        queryUserDislikedDict
    )


def jaccardSimilarity(likedQueries, dislikedQueries, ids):
    similarities = {}

    for id1 in ids:
        similarities[id1] = {}
        for id2 in ids:
            liked_dict1 = set(likedQueries.get(id1, []))
            disliked_dict1 = set(dislikedQueries.get(id1, []))
            liked_dict2 = set(likedQueries.get(id2, []))
            disliked_dict2 = set(dislikedQueries.get(id2, []))

            liked_intersection = liked_dict1.intersection(liked_dict2)
            disliked_intersection = disliked_dict1.intersection(disliked_dict2)

            liked_union = liked_dict1.union(liked_dict2)
            disliked_union = disliked_dict1.union(disliked_dict2)

            # (liked(dict1) ∩ liked(dict2)) ∪ (disliked(dict1) ∩ disliked(dict2))
            # This is the numerator of jaccard similarity
            union_of_intersections = liked_intersection.union(disliked_intersection)

            # (liked(dict1) ∪ liked(dict2)) ∪ (disliked(dict1) ∪ disliked(dict2))
            # This is the denominator of jaccard similarity
            union_of_unions = liked_union.union(disliked_union)
            
            try:
                jaccard_similarity = len(union_of_intersections) / len(union_of_unions)
            # If union_of_unions is zero, it means all of the sets were empty
            except ZeroDivisionError:
                jaccard_similarity = 0
            similarities[id1][id2] = jaccard_similarity
    
    return similarities


def getQueriesToPredict(utilityMatrix):
    # Dictionary of users and the queries they have not rated
    queriesToPredict = {}

    for userId, ratings in utilityMatrix.items():
        for queryId, rating in ratings.items():
            # Check if the user has not rated the query
            if(not rating):
                try:
                    queriesToPredict[userId].append(queryId)
                # If the user is not in the dictionary, add them
                except KeyError:
                    queriesToPredict[userId] = [queryId]

    return queriesToPredict


def itemBasedCF(utilityMatrix, queriesToPredict, itemSimilarity, usersIDs, topNitems, averageRating):
    baseline = int(min(usersIDs))

    for user in queriesToPredict:
        if(len(queriesToPredict[user]) > 0):

            for query in queriesToPredict[user]:
                topNindexes = sorted(range(len(itemSimilarity[query])), key = lambda sub: itemSimilarity[sub])[-topNitems:]
                #make new suggestion
                suggestedResult = 0
                #new users make a new weight sum
                weightsSum = 0

                for similarIndex in topNindexes:
                    weight = itemSimilarity[query][similarIndex]
                    rating = utilityMatrix[user - baseline][similarIndex + 1] 

                    if(rating != ''):
                        #print(f'rating: {rating}\nsimilarity: {weight}\nuserIndex: {similarIndex}\nuser: {user}\nqueryID: {query}\n')
                        suggestedResult += weight * int(rating)
                    
                        weightsSum += weight

                if(weightsSum > 0):
                    #print('why would i be here?')
                    #print(f'query: {query}\nMainUserID: {user}\ntotal: {suggestedResult}\ntotalWeight: {weightsSum}\n')
                    suggestedResult /= weightsSum
                    utilityMatrix[user - baseline][query + 1] = int(suggestedResult)

                #if no similar user has rated the query and we know the average of the user, use that to predict the rating
                elif(averageRating[user - baseline] > 0):
                    #print('made the average\n')
                    #print(f'query: {query}\nMainUserID: {user}\ntotal: {suggestedResult}\ntotalWeight: {weightsSum}\n')
                    utilityMatrix[user - baseline][query + 1] = averageRating[user - baseline]


                #if user has never rated any query, has average = -1, and if no similar user has rated the query, we use the random value approach
                else:
                    #print('random value')
                    #print(f'query: {query}\nMainUserID: {user}\ntotal: {suggestedResult}\ntotalWeight: {weightsSum}\n')
                    utilityMatrix[user - baseline][query + 1] = random.randint(0,100)
                    #should update the average of the user, but not sure if worth it


def userBasedCF(utilityMatrix, queriesToPredict, usersSimilarity, usersIDs, topNusers, averageRating): 
    #first id of the userSet
    baseline = int(min(usersIDs))

    #for all the users with queries to predict(in our case all users)
    for user in queriesToPredict:

        #check if user some queries that need prediction
        if(len(queriesToPredict[user]) > 0):

            #get index of the N most similar users
            topNindexes = sorted(range(len(usersSimilarity[user - baseline])), key = lambda sub: usersSimilarity[sub])[-topNusers:]
            #print(f'similarity: {usersSimilarity[user - baseline]}\n')
            #print(f'top indexes: {topNindexes}\n')
            #print(f'query to predict: {queriesToPredict[user]}\n')
            #for each query to predict per user
            for query in queriesToPredict[user]:

                #make new suggestion
                suggestedResult = 0
                #new users make a new weight sum
                weightsSum = 0

                #loop on top N similar users
                for similarIndex in topNindexes:
                    #take the weighted average of the results of the other users
                    #suggestion = similarity(weight) * rating of the user 
                    #query + 1 as we have the id and we suppose the queries are ordered in the matrix and first column(0) is for user id so query 0 is in index 1 
                    weight = usersSimilarity[user - baseline][similarIndex]
                    rating = utilityMatrix[similarIndex][query +1]

                    #print(f'weight: {weight}\n')

                    if(rating != ''):
                        #print(f'rating: {rating}\nsimilarity: {weight}\nuserIndex: {similarIndex}\nuser: {user}\nqueryID: {query}\n')
                        suggestedResult += weight * int(rating)
                    
                        weightsSum += weight

                
                #get the weighted average as suggestion
                #if there is at least a similar user that rated the query calculate it
                if(weightsSum > 0):
                    #print('why would i be here?')
                    #print(f'query: {query}\nMainUserID: {user}\ntotal: {suggestedResult}\ntotalWeight: {weightsSum}\n')
                    suggestedResult /= weightsSum
                    utilityMatrix[user - baseline][query + 1] = int(suggestedResult)

                #if no similar user has rated the query and we know the average of the user, use that to predict the rating
                elif(averageRating[user - baseline] > 0):
                    #print('made the average\n')
                    #print(f'query: {query}\nMainUserID: {user}\ntotal: {suggestedResult}\ntotalWeight: {weightsSum}\n')
                    utilityMatrix[user - baseline][query + 1] = averageRating[user - baseline]


                #if user has never rated any query, has average = -1, and if no similar user has rated the query, we use the random value approach
                else:
                    #print('random value')
                    #print(f'query: {query}\nMainUserID: {user}\ntotal: {suggestedResult}\ntotalWeight: {weightsSum}\n')
                    utilityMatrix[user - baseline][query + 1] = random.randint(0,100)
                    #should update the average of the user, but not sure if worth it

    return utilityMatrix
