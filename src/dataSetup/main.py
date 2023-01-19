from dataProcessing import *
from dataLoad import *

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
    

    '''for item in averageRating:
        print(item)
    '''

    userQueryLiked, userQueryDisliked = generateLikedDislikeDictionary(usersIDs=usersIDs, queryIDs=queryIDs, utilityMatrix=utilityMatrix, averageRating=averageRating)
    #print(type(userQueryLiked))
    #print(averageRating[0])
    #print(userQueryLiked[100])
    #print(userQueryDisliked[100])

    itemLiked, itemDisliked = generateLikeDislikeDictForItems(usersIDs=usersIDs, queryIDs=queryIDs, utilityMatrix=utilityMatrix, averageRating=averageRating)
    #print(itemLiked)

    itemSimilarity = jaccardSimilarity(likedQueries=itemLiked, dislikedQueries=itemDisliked)
    '''for item in range(10):
        print(f'index: {item}, similarity: {itemSimilarity[item]}\n')
    '''

    similarity = jaccardSimilarity(likedQueries=userQueryLiked, dislikedQueries=userQueryDisliked)
    '''for item in range(len(similarity)):
        print(f'index: {item}, similarity: {similarity[item]}\n')
    '''

    queryToPredict = getQueriesToPredict(utilityMatrix=utilityMatrix, usersIDs=usersIDs)

    #print(queryToPredict)

    filledUtilityMatrix = userBasedCF(utilityMatrix=utilityMatrix, queriesToPredict=queryToPredict, usersSimilarity=similarity, usersIDs=usersIDs, topNusers=10, averageRating=averageRating)

    '''with open('fullMatrix.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        for row in filledUtilityMatrix:
            writer.writerow(row)
    '''
    

if __name__ == "__main__":
    main()