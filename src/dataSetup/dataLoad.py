import csv

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


def generateLikedDislikeSet(usersIDs, queryIDs, utilityMatrix, averageRating):
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

    userQueryLiked, userQueryDisliked = generateLikedDislikeSet(usersIDs=usersIDs, queryIDs=queryIDs, utilityMatrix=utilityMatrix, averageRating=averageRating)
    print(averageRating[0])
    print(userQueryLiked[100])
    print(userQueryDisliked[100])



if __name__ == "__main__":
    main()
