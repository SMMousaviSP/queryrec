import random


def generateLikedDislikedDictionary(usersIDs, queryIDs, utilityMatrix, averageRating):
    # Dictionary of users and their liked and disliked queries
    userQueryLikedDict = {key: [] for key in usersIDs}
    userQueryDislikedDict = {key: [] for key in usersIDs}

    # Dictionary of queries and the users who liked and disliked them
    queryUserLikedDict = {key: [] for key in queryIDs}
    queryUserDislikedDict = {key: [] for key in queryIDs}

    for userId, ratings in utilityMatrix.items():
        for queryId, rating in ratings.items():
            # Check if the user has rated the query
            if(rating):
                # Check if the user has liked or disliked the query by comparing
                # the rating to the average rating of the user
                if(rating >= averageRating[userId]):
                    userQueryLikedDict[userId].append(queryId)
                    queryUserLikedDict[queryId].append(userId)
                else:
                    userQueryDislikedDict[userId].append(queryId)
                    queryUserDislikedDict[queryId].append(userId)

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


def queryBasedCF(utilityMatrix, queriesToPredict, querySimilarity, topNQueries):
    # Dictionary of users and their predicted ratings along with the similarity
    # values of the similar queries used in prediction
    predictedRatings = {}
    for user, queries in queriesToPredict.items():
        for query in queries:
            # Getting the similar queries to the `query` we are predicting
            try:
                similarQueries = querySimilarity[query]
            # If the query is not in the dictionary, it means it has no similar queries
            except KeyError:
                continue
            # Sorting the similar queries by their similarity
            sortedSimilarQueries = sorted(similarQueries.items(), key=lambda x: x[1], reverse=True)

            foundedSimilarQueries = 0
            # List of similarity values of the similar queries used in prediction,
            # we use this list later on to know how reliable the prediction is and
            # compare it to other prediction methods
            listOfSimilarities = []
            weightedSum = 0
            sumOfWeights = 0
            # Getting the top N similar queries
            for similarQuery, similarity in sortedSimilarQueries:
                # Getting the user's rating for the similar query
                rating = utilityMatrix[user][similarQuery]
                # If the user has rated the similar query, use it to predict the rating
                if(rating):
                    weightedSum += similarity * rating
                    sumOfWeights += similarity
                    listOfSimilarities.append(similarity)
                    foundedSimilarQueries += 1
                # If we have found the top N similar queries, stop searching
                if(foundedSimilarQueries == topNQueries):
                    break
            # If we were able to find at least one similar query, predict the rating
            if(foundedSimilarQueries > 0):
                # Check if we were able to find top N similar queries, otherwise fill
                # list of similarities with zeros, this is done so that we can compare
                # the prediction with other prediction methods. The more zeros we have
                # in the list, the less reliable the prediction is.
                if(foundedSimilarQueries < topNQueries):
                    listOfSimilarities += [0] * (topNQueries - foundedSimilarQueries)
                prediction = weightedSum / sumOfWeights
                try:
                    predictedRatings[user][query] = (prediction, listOfSimilarities)
                # If it is the first time we are saving a prediction for the user,
                # create a new dictionary for them
                except KeyError:
                    predictedRatings[user] = {query: (prediction, listOfSimilarities)}
    return predictedRatings


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
