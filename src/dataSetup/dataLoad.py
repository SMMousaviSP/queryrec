import csv
import os

import pandas as pd


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
    utilityMatrix = {}
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
            ratings = row[1:]
            for rating in ratings:
                if(rating):
                    userAverage += rating
                    values += 1

            if(values == 0):
                average[currentUserId] = -1
            else:
                # Should it be integer?
                average[currentUserId] = (userAverage / values)

            utilityMatrix[currentUserId] = {
                queryId: rating
                for queryId, rating in zip(queryIDs, ratings)
            }

        return queryIDs, utilityMatrix, average


def getUniqueValues(datasetPath=os.path.join(DATA_PATH, 'Smalldataset', 'usersData.csv')):
    # Get unique values for each column with their number of occurrences
    df = pd.read_csv(datasetPath)
    uniqueValues = {}
    for column in df.columns:
        if column != 'id':
            uniqueValues[column] = df[column].value_counts().to_dict()
    return uniqueValues
