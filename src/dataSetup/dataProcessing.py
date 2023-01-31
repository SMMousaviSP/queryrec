import copy


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


def queryBasedCF(utilityMatrix, queriesToPredict, querySimilarity, topNQueries, fillNotPredictable):
    # Dictionary of users and their predicted ratings along with the similarity
    # values of the similar queries used in prediction
    predictedRatings = {}
    notAbleToPredict = 0
    for user, queries in queriesToPredict.items():
        for query in queries:
            # Getting the similar queries to the `query` we are predicting
            try:
                similarQueries = querySimilarity[query]
            # If the query is not in the dictionary, it means it has no similar queries
            except KeyError:
                continue
            # Sorting the similar queries by their similarity
            sortedSimilarQueries = sorted(
                similarQueries.items(),
                key=lambda x: x[1],
                reverse=True
            )[1:] # Removing the query itself from the list

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
                # If the user has rated the similar query, and similarity is
                # greater than zero, use it to predict the rating
                if(rating and similarity):
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
            else:
                notAbleToPredict += 1
                prediction = fillNotPredictable(user, query)
                try:
                    predictedRatings[user][query] = (prediction, [0] * topNQueries)
                # If it is the first time we are saving a prediction for the user,
                # create a new dictionary for them
                except KeyError:
                    predictedRatings[user] = {query: (prediction, [0] * topNQueries)}
    print(f"Not able to predict {notAbleToPredict} ratings")
    return predictedRatings


def userBasedCF(utilityMatrix, queriesToPredict, userSimilarity, topNUsers, fillNotPredictable):
    # Dictionary of users and their predicted ratings along with the similarity
    # values of the similar queries used in prediction
    predictedRatings = {}
    notAbleToPredict = 0
    for user, queries in queriesToPredict.items():
        for query in queries:
            # Getting the similar users to the `user`
            try:
                similarUsers = userSimilarity[user]
            # If the user is not in the dictionary, it means it has no similar users
            except KeyError:
                continue
            # Sorting the similar users by their similarity
            sortedSimilarUsers = sorted(
                similarUsers.items(),
                key=lambda x: x[1],
                reverse=True
            )[1:] # Removing the user itself from the list

            foundedSimilarUsers = 0
            # List of similarity values of the similar users used in prediction,
            # we use this list later on to know how reliable the prediction is and
            # compare it to other prediction methods
            listOfSimilarities = []
            weightedSum = 0
            sumOfWeights = 0
            # Getting the top N similar users
            for similarUser, similarity in sortedSimilarUsers:
                # Getting the query's rating from the similar user
                rating = utilityMatrix[similarUser][query]
                # If the similar user has rated the query and the similarity of
                # similar user is greater than 0, use it to predict the rating
                if(rating and similarity):
                    weightedSum += similarity * rating
                    sumOfWeights += similarity
                    listOfSimilarities.append(similarity)
                    foundedSimilarUsers += 1
                # If we have found the top N similar queries, stop searching
                if(foundedSimilarUsers == topNUsers):
                    break
            # If we were able to find at least one similar query, predict the rating
            if(foundedSimilarUsers > 0):
                # Check if we were able to find top N similar queries, otherwise fill
                # list of similarities with zeros, this is done so that we can compare
                # the prediction with other prediction methods. The more zeros we have
                # in the list, the less reliable the prediction is.
                if(foundedSimilarUsers < topNUsers):
                    listOfSimilarities += [0] * (topNUsers - foundedSimilarUsers)
                prediction = weightedSum / sumOfWeights
                try:
                    predictedRatings[user][query] = (prediction, listOfSimilarities)
                # If it is the first time we are saving a prediction for the user,
                # create a new dictionary for them
                except KeyError:
                    predictedRatings[user] = {query: (prediction, listOfSimilarities)}
            else:
                notAbleToPredict += 1
                prediction = fillNotPredictable(user, query)
                try:
                    predictedRatings[user][query] = (prediction, [0] * topNUsers)
                # If it is the first time we are saving a prediction for the user,
                # create a new dictionary for them
                except KeyError:
                    predictedRatings[user] = {query: (prediction, [0] * topNUsers)}
    print(f"Not able to predict {notAbleToPredict} ratings")
    return predictedRatings


def fillUtilityMatrix(utilityMatrix, predictions, inplace=False):
    if not inplace:
        utilityMatrix = copy.deepcopy(utilityMatrix)
    for user, queries in predictions.items():
        for query, (prediction, _) in queries.items():
            utilityMatrix[user][query] = prediction
    if not inplace:
        return utilityMatrix


def topKQueriesNotPosed(predictions, userId, k):
    user_predictions = predictions[userId]
    sorted_predictions = sorted(user_predictions.items(), key=lambda x: x[1][0], reverse=True)[:k]
    return [(query, prediction) for query, (prediction, _) in sorted_predictions]


def topKQueriesFromUtilityMatrix(utilityMatrix, userId, k):
    user_ratings = utilityMatrix[userId]
    sorted_ratings = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)[:k]
    return [(query, rating) for query, rating in sorted_ratings]
