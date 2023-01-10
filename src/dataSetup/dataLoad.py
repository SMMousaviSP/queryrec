import csv
import itertools

def loadUserSet():
    usersIDs = []
    with open('..\\..\\data\\Smalldataset\\userSet.csv', 'r', newline='') as userSetFile:
        reader = csv.reader(userSetFile, delimiter=',')
        for id in reader:
            usersIDs.append(id[0])
        
    return usersIDs

def loadQueryIds():
    queryIDs = []
    with open('..\\..\\data\\Smalldataset\\utilityMatrix.csv', 'r', newline='') as utilityMatrixFile:
        reader = csv.reader(utilityMatrixFile, delimiter=',')
        header = next(reader)
        queryIDs = header
        
    return queryIDs

def loadUtilityMatrix():
    queryIDs = []
    data = []
    average = []
    userAverage = 0
    values = 0
    with open('..\\..\\data\\Smalldataset\\utilityMatrix.csv', 'r', newline='') as utilityMatrixFile:
        reader = csv.reader(utilityMatrixFile, delimiter=',')
        header = next(reader)
        queryIDs = header

        for row in reader:
            for item in row:
                if(not(item.startswith('u')) and item != ''):
                    userAverage += int(item)
                    values += 1

            if(values == 0):
                average.append(-1)
            else:
                average.append(int(userAverage / values))

            userAverage = 0
            values = 0
            data.append(row)
        
        return queryIDs, data, average


def generateLikedDislikeDictionary(usersIDs, queryIDs, utilityMatrix, averageRating):
    #userQueryLikedsDict = dict.fromkeys(int(usersIDs))
    #userQueryDislikedsDict = dict.fromkeys(int(usersIDs))
    userQueryLikedsDict = {}
    userQueryDislikedsDict = {}
    for item in usersIDs:
        if int(item) not in userQueryLikedsDict:
            userQueryLikedsDict[int(item)] = []
    
    #print(userQueryLikedsDict)

    for item in usersIDs:
        if int(item) not in userQueryDislikedsDict:
            userQueryDislikedsDict[int(item)] = []
    #print(userQueryDislikedsDict)

    currentUser = 0
    currentQuery = 0

    for row in utilityMatrix:
        for item in row[1:]:
            if(item != ''):
                if(int(item) >= averageRating[currentUser]):
                    #print(item)
                    userQueryLikedsDict[int(usersIDs[0]) + currentUser].append(queryIDs[currentQuery])
                else:
                    #print(item)
                    userQueryDislikedsDict[int(usersIDs[0]) + currentUser].append(queryIDs[currentQuery])
            currentQuery += 1

        currentUser += 1
        currentQuery = 0

    return userQueryLikedsDict, userQueryDislikedsDict


def jaccardSimilarity(likedQueries, dislikedQueries, usersIDs):
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
    


                






def main():
    usersIDs = loadUserSet()
    #print(usersIDs)
    #queryIDs = loadQueryIds()
    #print(queryIDs)
    queryIDs, utilityMatrix, averageRating = loadUtilityMatrix()
    #print(queryIDs)
    #print(averageRating)
    '''for item in utilityMatrix:
        print(item)
    '''

    '''for item in average:
        print(item)
    '''

    userQueryLiked, userQueryDisliked = generateLikedDislikeDictionary(usersIDs=usersIDs, queryIDs=queryIDs, utilityMatrix=utilityMatrix, averageRating=averageRating)
    #print(type(userQueryLiked))
    #print(averageRating[0])
    #print(userQueryLiked[100])
    #print(userQueryDisliked[100])

    similarity = jaccardSimilarity(likedQueries=userQueryLiked, dislikedQueries=userQueryDisliked,usersIDs=usersIDs)
    '''for item in range(len(similarity)):
        print(f'index: {item}, similarity: {similarity[item]}\n')
    '''




if __name__ == "__main__":
    main()
