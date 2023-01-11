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

