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
    

    '''for item in average:
        print(item)
    '''

    userQueryLiked, userQueryDisliked = generateLikedDislikeDictionary(usersIDs=usersIDs, queryIDs=queryIDs, utilityMatrix=utilityMatrix, averageRating=averageRating)
    #print(type(userQueryLiked))
    #print(averageRating[0])
    #print(userQueryLiked[100])
    #print(userQueryDisliked[100])

    similarity = jaccardSimilarity(likedQueries=userQueryLiked, dislikedQueries=userQueryDisliked,usersIDs=usersIDs)
    for item in range(len(similarity)):
        print(f'index: {item}, similarity: {similarity[item]}\n')
    

if __name__ == "__main__":
    main()