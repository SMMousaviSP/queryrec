import math


def findQueriesWithSameCondition(queries, condition):
    """
    Find queries with same condition.
    """
    if len(condition) != 1:
        raise ValueError('Condition must have exactly one key-value pair')
    condition = list(condition.items())[0]
    queryList = []

    for queryId, query in queries.items():
        if condition in query.items():
            queryList.append({queryId: query})
    return queryList


def breakDownQueryToSingleCondition(query):
    # break down query dictionary to a list of dictionaries with single key and value
    queryList = []
    for key, value in query.items():
        queryList.append({key: value})
    return queryList


def findMinimumCount(query, uniqueValues):
    # find minimum count of a single condition
    singleConditionList = breakDownQueryToSingleCondition(query)
    minimumCount = math.inf
    for query in singleConditionList:
        for key, value in query.items():
            try:
                count = uniqueValues[key][value]
                if count < minimumCount:
                    minimumCount = count
            except KeyError:
                pass
    if minimumCount == math.inf:
        minimumCount = -1
    return minimumCount


def averageQueryRating(queryId, utilityMatrix):
    # calculate average rating for a query
    ratingSum = 0
    weight = 0
    for _, ratings in utilityMatrix.items():
        try:
            ratingSum += ratings[queryId]
            weight += 1
        except KeyError:
            pass
        except TypeError:
            pass
    return ratingSum / weight


def calculateGeneralUtility(query, utilityMatrix, queries, uniqueValues):
    weight = 0
    utility = 0
    singleConditionList = breakDownQueryToSingleCondition(query)
    for singleCondition in singleConditionList:
        single_utility = 0
        single_weight = 0
        sameConditionQueries = findQueriesWithSameCondition(queries, singleCondition)
        for sameCondition in sameConditionQueries:
            queryId, sameConditionQuery = list(sameCondition.items())[0]
            minimumCount = findMinimumCount(sameConditionQuery, uniqueValues)
            if minimumCount != -1:
                single_weight += minimumCount / len(sameConditionQuery)
                single_utility += (
                    averageQueryRating(queryId, utilityMatrix)
                    *
                    # This is the weight of the query. It is divided by the
                    # number of conditions in the query to make sure that
                    # the weight of a query with more conditions is lower
                    (minimumCount / len(sameConditionQuery))
                )
        if single_weight != 0:
            utility += single_utility / single_weight
            weight += 1
    if weight != 0:
        return utility / weight
    return -1
