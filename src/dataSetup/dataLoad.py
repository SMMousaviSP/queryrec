import csv
import os


DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))


def loadUserSet(userSetPath=os.path.join(DATA_PATH, 'Smalldataset', 'userSet.csv')):
    usersIDs = []
    with open(userSetPath, 'r', newline='') as userSetFile:
        reader = csv.reader(userSetFile, delimiter=',')
        for id in reader:
            usersIDs.append(id[0])
        
    return usersIDs

def loadQueryIds(utilityMatrixPath=os.path.join(DATA_PATH, 'Smalldataset', 'utilityMatrix.csv')):
    queryIDs = []
    with open(utilityMatrixPath, 'r', newline='') as utilityMatrixFile:
        reader = csv.reader(utilityMatrixFile, delimiter=',')
        header = next(reader)
        queryIDs = header
        
    return queryIDs

def loadUtilityMatrix(utilityMatrixPath=os.path.join(DATA_PATH, 'Smalldataset', 'utilityMatrix.csv')):
    queryIDs = []
    data = []
    average = []
    userAverage = 0
    values = 0
    with open(utilityMatrixPath, 'r', newline='') as utilityMatrixFile:
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

