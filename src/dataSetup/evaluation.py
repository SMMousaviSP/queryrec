import random


def getQueriesForEvaluation(utilityMatrix, percentage, removeFromUtilityMatrix=False, seed=None):
    # Dictionary of users and the queries they have not rated
    queriesForEvaluation = {}

    # Set the seed for the random number generator if provided
    if(seed):
        random.seed(seed)

    for userId, ratings in utilityMatrix.items():
        for queryId, rating in ratings.items():
            # Check if the user has not rated the query
            if(rating):
                if random.random() < percentage:
                    # Remove the query from the utility matrix if specified
                    if(removeFromUtilityMatrix):
                        utilityMatrix[userId][queryId] = None
                    try:
                        queriesForEvaluation[userId][queryId] = rating
                    # If the user is not in the dictionary, add them
                    except KeyError:
                        queriesForEvaluation[userId] = {queryId: rating}

    return queriesForEvaluation


def prepareQueriesForPrediction(queries):
    return {
        userId: [queryId for queryId in ratings.keys()]
        for userId, ratings in queries.items()
    }


def getPredictionsAndActualRatings(predictions, actualRatings):
    predictionsList = []
    ActualRatingsList = []

    for userId, ratings in predictions.items():
        for queryId, rating in ratings.items():
            predictionsList.append(rating[0])
            ActualRatingsList.append(actualRatings[userId][queryId])
    return predictionsList, ActualRatingsList


def rootMeanSquaredError(list1, list2):
    # Throw an error if the lists are not the same length
    if len(list1) != len(list2):
        raise ValueError("Lists must be the same length")
    return (sum((x - y) ** 2 for x, y in zip(list1, list2)) / len(list1)) ** 0.5
