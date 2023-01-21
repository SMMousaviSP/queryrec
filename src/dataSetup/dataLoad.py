import csv
import os


DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

# function to convert user's rating to int or None if there is no rating
int_or_none = lambda x: int(x) if x else None


def loadUserSet(userSetPath=os.path.join(DATA_PATH, 'Smalldataset', 'userSet.csv')):
    usersIDs = []
    with open(userSetPath, 'r', newline='') as userSetFile:
        reader = csv.reader(userSetFile, delimiter=',')
        for id in reader:
            usersIDs.append(int(id[0]))

    return usersIDs

def loadQueryIds(utilityMatrixPath=os.path.join(DATA_PATH, 'Smalldataset', 'utilityMatrix.csv')):
    queryIDs = []
    with open(utilityMatrixPath, 'r', newline='') as utilityMatrixFile:
        reader = csv.reader(utilityMatrixFile, delimiter=',')
        header = next(reader)
        queryIDs = header

    return [int(i) for i in queryIDs]

def loadUtilityMatrix(utilityMatrixPath=os.path.join(DATA_PATH, 'Smalldataset', 'utilityMatrix.csv')):
    queryIDs = []
    data = []
    average = {}
    with open(utilityMatrixPath, 'r', newline='') as utilityMatrixFile:
        reader = csv.reader(utilityMatrixFile, delimiter=',')
        header = next(reader)
        queryIDs = [int(i) for i in header[1:]]

        for row in reader:
            userAverage = 0
            values = 0
            # convert ratings to int or None if there is no rating
            row = [int_or_none(i) for i in row]
            currentUserId = row[0]
            for rating in row[1:]:
                if(rating):
                    userAverage += rating
                    values += 1

            if(values == 0):
                average[currentUserId] = -1
            else:
                # Should it be integer?
                average[currentUserId] = (userAverage / values)

            data.append(row)

        return queryIDs, data, average
