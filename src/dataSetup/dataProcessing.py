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


def jaccardSimilarity(likedQueries, dislikedQueries):
    totalSimilarity = []
    index = 0

    #loop on all the ids of the users
    for (likeKey, dislikeKey) in itertools.zip_longest(likedQueries, dislikedQueries):
        userSimilarity = []
        #loop on every user on liked and disliked queries
        #make set of liked and disliked queries for each user
        likedSet1 = set(likedQueries[likeKey])
        dislikeSet1 = set(dislikedQueries[dislikeKey])

        # liked(user1) ∪ disliked(user1)
        union1 = likedSet1.union(dislikeSet1)
        #print(len(union1))

        #loop again on users from current user onward to compare
        for (likeKey2, dislikeKey2) in itertools.zip_longest(likedQueries, dislikedQueries):

            #make set of liked and disliked queries for each user to compare
            likedSet2 = set(likedQueries[likeKey2])
            dislikeSet2 = set(dislikedQueries[dislikeKey2])

            # liked(user2) ∪ disliked(user2)
            union2 = likedSet2.union(dislikeSet2)

            # [ liked(user1) ∩ liked(user2) ]
            likeIntersection = likedSet1.intersection(likedSet2)

            #[ disliked(user1) ∩ disliked(user2)]
            dislikeIntersection = dislikeSet1.intersection(dislikeSet2)

            # { [ liked(user1) ∩ liked(user2) ]  ∪ [ disliked(user1) ∩ disliked(user2)] } /
            # { [ liked(user1) ∪ liked(user2)    ∪   disliked(user1) ∪ disliked(user2)] }
            if(len(union1) > 0  or len(union2) > 0): #if there is at least one item in the union set(at least 1 query has been posed)
                userSimilarity.append(round(len(likeIntersection.union(dislikeIntersection)) / 
                                            len(union1.union(union2))
                                            ,2)
                                    )
                #to note that the diagonal will be full of 1 as each user perfectly equal to itself
            else: #union set is empty, no queries have ever been posed by the user
                #how do i act in this case? i think say they are completely different might backfire as we don't actually know if they are different
                userSimilarity.append(-1)

            
        #totalSimilarity[index] = userSimilarity
        totalSimilarity.append(userSimilarity) 
        index += 1
    return totalSimilarity

def getQueriesToPredict(utilityMatrix, queryIDs):
    # Dictionary of users and the queries they have not rated
    queriesToPredict = {}

    for row in utilityMatrix:
        currentUser = row[0]
        for rating, currentQuery in zip(row[1:], queryIDs):
            # Check if the user has not rated the query
            if(not rating):
                try:
                    queriesToPredict[currentUser].append(currentQuery)
                # If the user is not in the dictionary, add them
                except KeyError:
                    queriesToPredict[currentUser] = [currentQuery]

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
