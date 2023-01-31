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
    utilityMatrix = {}
    average = {}
    with open(utilityMatrixPath, 'r', newline='') as utilityMatrixFile:
        reader = csv.reader(utilityMatrixFile, delimiter=',')
        header = next(reader)
        queryIDs = header[1:]

        for row in reader:
            userAverage = 0
            values = 0
            # convert ratings to int or None if there is no rating
            row = [row[0]] + [int_or_none(i) for i in row[1:]]
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


def loadQuerySet(querySetPath=os.path.join(DATA_PATH, 'Smalldataset', 'querySet.csv')):
    queries = {}
    with open(querySetPath, 'r') as querySetFile:
        reader = csv.reader(querySetFile, delimiter=',')
        for query in reader:
            # Empty query? Move on
            if len(query) < 2:
                continue
            id = query[0]
            content = query[1:]
            queries[id] = {
                condition: value
                for condition, value in map(lambda x: x.split("="), content)
            }
    return queries
