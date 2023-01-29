import csv
import random
import os

from faker import Faker


# user entries is the number of users we want in the db
USER_ENTRIES = 200


# entries of each parameter, like 10 different cities, 10 different ages..
TOTAL_ENTRIES = 10


city_names = [
    "Trento",
    "Bolzano",
    "Verona",
    "Brescia",
    "Milano",
    "Bologna",
    "Torino",
    "Venezia",
    "Bergamo",
    "Rovereto"]


def generate_ids():
    return list(range(USER_ENTRIES))


def generate_names_surnames():
    faker = Faker('en_US')
    names = [faker.unique.first_name() for i in range(TOTAL_ENTRIES)]
    surnames = [faker.unique.last_name() for i in range(TOTAL_ENTRIES)]
    return names, surnames


def generate_heights():
    return random.sample(range(150, 200), TOTAL_ENTRIES)


def generate_age():
    return random.sample(range(30, 50), TOTAL_ENTRIES)


def generate_people(
    ids,
    names,
    surnames,
    heights,
    ages,
    dataPath,
    city_names=city_names
):
    usersDataPath = os.path.join(dataPath, 'usersData.csv')
    with open(usersDataPath, 'w', newline='') as file:
        header = ['id', 'name', 'surname', 'height', 'age', 'city']
        writer = csv.writer(file)
        writer.writerow(header)
        for i in range(0, USER_ENTRIES):
            data = [
                ids[i],
                random.sample(names, 1)[0],
                random.sample(surnames, 1)[0],
                random.sample(heights, 1)[0],
                random.sample(ages, 1)[0],
                random.sample(city_names, 1)[0]
            ]
            writer.writerow(data)

'''
generates the user set, the ids start from the number of users we have in the DB onward
this is done to show that the users that pose the queries are not necessarily the ones stored in the DB
'''
def generate_user_set(USER_POSING_ENTRIES, dataPath):
    userSetPath = os.path.join(dataPath, 'userSet.csv')
    with open(userSetPath, 'w', newline='') as file:
        writer = csv.writer(file)
        ids = []
        for i in range(0, USER_POSING_ENTRIES):
            ids.insert(0, i+USER_POSING_ENTRIES)
            writer.writerow(ids)
            ids.clear()


def generate_query_set(ids, names, surnames, heights, ages, QUERY_ENTRIES, dataPath):
    querySetPath = os.path.join(dataPath, 'querySet.csv')
    with open(querySetPath, 'w', newline='') as file:
        writer = csv.writer(file)

        for i in range(0, QUERY_ENTRIES):
            empty_query = True
            data = [i]
            
            random_choice_for_params = random.randrange(0,100)
            # 50% chance to have name in query
            if(random_choice_for_params <= 50):
                data.append('name='+random.sample(names, 1)[0])
                empty_query = False

            random_choice_for_params = random.randrange(0,100)
            # 40% chance to have surname in query
            if(random_choice_for_params <= 40):
                data.append('surname='+random.sample(surnames, 1)[0])
                empty_query = False

            random_choice_for_params = random.randrange(0,100)
            # 30% chance to have height in query
            if(random_choice_for_params <= 30):
                data.append('height='+str(random.sample(heights, 1)[0]))
                empty_query = False
                    

            random_choice_for_params = random.randrange(0,100)
            # 50% chance to have age in query
            if(random_choice_for_params <= 50):
                data.append('age='+str(random.sample(ages, 1)[0]))
                empty_query = False

            random_choice_for_params = random.randrange(0,100)
            # 50% chance to have age in query
            if(random_choice_for_params <= 50):
                data.append('city='+str(random.sample(city_names, 1)[0]))
                empty_query = False

            # if the query was empty, fill with all the params(least probable scenario to happen)
            if(empty_query):
                data.append('name='+random.sample(names, 1)[0])
                data.append('surname='+random.sample(surnames, 1)[0])
                data.append('height='+str(random.sample(heights, 1)[0]))
                data.append('age='+str(random.sample(ages, 1)[0]))
                data.append('city='+str(random.sample(city_names, 1)[0]))

            writer.writerow(data)
            data.clear()


def generate_utility_matrix(dataPath, QUERY_ENTRIES, USER_POSING_ENTRIES):
    isEmpty = True
    utilityMatrixPath = os.path.join(dataPath, 'utilityMatrix.csv')
    querySetPath = os.path.join(dataPath, 'querySet.csv')
    with open(utilityMatrixPath, 'w', newline='') as file:
        with open(querySetPath,  'r', newline='') as myInput:
            reader = csv.reader(myInput, delimiter=',')
            writer = csv.writer(file)
            header = ['user_id'] + list(range(QUERY_ENTRIES))
            writer.writerow(header)
            for i in range(0, USER_POSING_ENTRIES):
                #ids of user set starts from USER_POSING_ENTRIES
                data = [i + USER_POSING_ENTRIES]
                for row in reader:
                    poseQuery = random.randint(1,10)
                    poseBiasedQuery = random.choice((True, False))
                    isEmpty = True
                    if(i < 30): #make first 30 users like queries that have names that start with R or D or J or S
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'name' and item.split('=')[1].startswith(('R','r','D','d','J','j','S','s'))):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(70,100),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                    elif(i >= 30 and i < 60): #make next 30 users dislike queries that have names that start with R or D or J or S
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'name' and item.split('=')[1].startswith(('R','r','D','d','J','j','S','s'))):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(1,40),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                    elif(i >= 60 and i < 85): #make next 25 users like queries with age AND name starting with R or D or J or S
                        items = [item for item in row if item.startswith(('name','age'))] # have a list with the params we need
                        if(len(items) == 2): #check if we got the right amount of params
                            if(items[0].split('=')[1].startswith(('R','r','D','d','J','j','S','s')) and int(items[1].split('=')[1]) >= 36):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(70,100),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False
                    
                    elif(i >= 60 and i < 85): #make next 25 users like queries with any city
                        items = [item for item in row if item.startswith(('city'))] # have a list with the params we need
                        if(len(items) == 1): #check if we got the right amount of params
                            if(poseBiasedQuery):
                                data.append(random.sample(range(70,100),1)[0])
                            else:
                                data.append('')

                            isEmpty = False

                    elif(i >= 85 and i < 95): #make next 10 users like queries with any city but dislike the ones with age
                        items = [item for item in row if item.startswith(('city','age'))] # have a list with the params we need
                        if(len(items) == 2 and poseBiasedQuery): #check if we got the right amount of params
                            data.append(random.sample(range(1,30),1)[0])
                            isEmpty = False
                        else:
                            if(poseBiasedQuery):
                                if(item.split('=')[0] == 'age'): #if only age, dislike
                                    data.append(random.sample(range(1,30),1)[0])
                                else: #we have only city and they like any city
                                    data.append(random.sample(range(50,100),1)[0])
                            else:
                                data.append('')

                            isEmpty = False


                    #----------------------- START OF MEDIUM DATASET --------------------------------------------
                    #skip from 95 to 100 as we want to have some empty users even for the smallest database which has 100 users
                    elif(i >= 100 and i < 125): #make next 25 users like queries with city starting with r and t AND height higher than 180
                        items = [item for item in row if item.startswith(('city','height'))] # have a list with the params we need
                        if(len(items) == 2): #check if we got the right amount of params
                            if(items[0].split('=')[1].startswith(('R','r','T','t')) and int(items[1].split('=')[1]) >= 180):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(60,100),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False
                    
                    elif(i >= 125 and i < 145): #make next 20 users like queries with city starting with r and t AND age lower than 30
                        items = [item for item in row if item.startswith(('city','age'))] # have a list with the params we need
                        if(len(items) == 2): #check if we got the right amount of params
                            if(items[0].split('=')[1].startswith(('R','r','T','t')) and int(items[1].split('=')[1]) <= 30):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(60,100),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                    elif(i >= 145 and i < 175): #make next 30 users dilike queries with age lower than 45
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'age' and int(item.split('=')[1]) <= 45):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(1,40),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False
                            elif(item.split('=')[0] == 'age' and int(item.split('=')[1]) > 45): #and like queries with age higher that 45
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(50,90),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                    elif(i >= 175 and i < 195): #make next 20 users like queries with age lower than 45
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'age' and int(item.split('=')[1]) <= 45):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(50,90),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False
                            elif(item.split('=')[0] == 'age' and int(item.split('=')[1]) > 45): #and dislike queries with age higher that 45
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(10,40),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False


                    
                    #----------------------- START OF LARGE DATASET --------------------------------------------
                    elif(i >= 200 and i < 240): #make next 40 users like queries with names and surnames starting with letters
                        items = [item for item in row if item.startswith(('name','surname'))] # have a list with the params we need
                        if(len(items) == 2): #check if we got the right amount of params
                            if(items[0].split('=')[1].startswith(('D','d','A','a', 'R', 'r', 'C', 'c')) and items[1].split('=')[1].startswith(('D','d','A','a', 'R', 'r', 'C', 'c'))):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(60,100),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                            else:#if queries names or surnames don't start with any of the letters, dislike
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(10,50),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                    elif(i >= 240 and i < 300): #make next 60 users dislike all the queries with any city
                        items = [item for item in row if item.startswith(('city'))] # have a list with the params we need
                        if(len(items) == 1): #check if we got the right amount of params
                            if(poseBiasedQuery):
                                data.append(random.sample(range(1,50),1)[0])
                            else:
                                data.append('')

                            isEmpty = False

                    elif(i >= 300 and i < 350): #make next 50 users like queries with name starting with 
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'name' and item.split('=')[1].startswith(('R','r','E','e','A','a','N','n'))):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(70,100),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                    elif(i >= 350 and i < 390): #make next 40 users dislike cities that start with R 
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'city' and item.split('=')[1].startswith(('R','r',))):
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(1,50),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                            elif(item.split('=')[0] == 'city' and item.split('=')[1].startswith(('T','t',))):# and like all cities starting with T
                                if(poseBiasedQuery):
                                    data.append(random.sample(range(60,100),1)[0])
                                else:
                                    data.append('')

                                isEmpty = False

                    #keep a total of 30 new users that are unbiased and have only random ratings




                    
                    #elif(i >= 95 and i < USER_POSING_ENTRIES): this creates an user than never posed queries, no need for this as it's already done below for all the users
                        #data.append('')
                            
                    if(isEmpty): #if query was not posed add empty value
                        #add query to generate randomness while keeping bias as it might add only queries that are not part of the bias
                        if(poseQuery == 5):
                            data.append(random.randint(1,100))
                        else:
                            data.append('') #append empty element as the query was not posed before


                writer.writerow(data)
                data.clear()
                myInput.seek(0) #reset file pointer to begin
                #could also store the data in memory and iterate how many times we want instead of doing this, depends on the size, this always works.

def generateSmallDataset(ids, names, surnames, heights, ages, USER_POSING_ENTRIES, QUERY_ENTRIES, dataPath):
    dataPath = os.path.join(dataPath, 'smallDataset')
    if not os.path.exists(dataPath):
        os.makedirs(dataPath)
    generate_people(ids, names, surnames, heights, ages, dataPath=dataPath)
    generate_user_set(USER_POSING_ENTRIES=USER_POSING_ENTRIES, dataPath=dataPath)
    generate_query_set(ids, names, surnames, heights, ages, QUERY_ENTRIES, dataPath=dataPath)
    generate_utility_matrix(dataPath=dataPath, QUERY_ENTRIES=QUERY_ENTRIES,USER_POSING_ENTRIES=USER_POSING_ENTRIES)

def generateMediumDataset(ids, names, surnames, heights, ages, USER_POSING_ENTRIES, QUERY_ENTRIES, dataPath):
    dataPath = os.path.join(dataPath, 'mediumDatasets')
    if not os.path.exists(dataPath):
        os.makedirs(dataPath)

    #generate medium dataset doubling the users posing the queries
    userBasedDatapath = os.path.join(dataPath, 'double_the_userSet')
    if not os.path.exists(userBasedDatapath):
        os.makedirs(userBasedDatapath)
    generate_people(ids, names, surnames, heights, ages, dataPath=userBasedDatapath)
    generate_user_set(USER_POSING_ENTRIES=USER_POSING_ENTRIES*2, dataPath=userBasedDatapath)
    generate_query_set(ids, names, surnames, heights, ages, QUERY_ENTRIES, dataPath=userBasedDatapath)
    generate_utility_matrix(dataPath=userBasedDatapath, QUERY_ENTRIES=QUERY_ENTRIES,USER_POSING_ENTRIES=USER_POSING_ENTRIES*2)

    #generate medium dataset doubling queries posed by the users
    queryBasedDatapath = os.path.join(dataPath, 'double_the_querySet')
    if not os.path.exists(queryBasedDatapath):
        os.makedirs(queryBasedDatapath)
    generate_people(ids, names, surnames, heights, ages, dataPath=queryBasedDatapath)
    generate_user_set(USER_POSING_ENTRIES=USER_POSING_ENTRIES, dataPath=queryBasedDatapath)
    generate_query_set(ids, names, surnames, heights, ages, QUERY_ENTRIES*2, dataPath=queryBasedDatapath)
    generate_utility_matrix(dataPath=queryBasedDatapath, QUERY_ENTRIES=QUERY_ENTRIES*2,USER_POSING_ENTRIES=USER_POSING_ENTRIES)

def generateLargeDataset(ids, names, surnames, heights, ages, USER_POSING_ENTRIES, QUERY_ENTRIES, dataPath):
    dataPath = os.path.join(dataPath, 'largeDatasets')
    if not os.path.exists(dataPath):
        os.makedirs(dataPath)

    #generate medium dataset doubling the users posing the queries
    userBasedDatapath = os.path.join(dataPath, 'quadruple_the_userSet')
    if not os.path.exists(userBasedDatapath):
        os.makedirs(userBasedDatapath)
    generate_people(ids, names, surnames, heights, ages, dataPath=userBasedDatapath)
    generate_user_set(USER_POSING_ENTRIES=USER_POSING_ENTRIES*4, dataPath=userBasedDatapath)
    generate_query_set(ids, names, surnames, heights, ages, QUERY_ENTRIES, dataPath=userBasedDatapath)
    generate_utility_matrix(dataPath=userBasedDatapath, QUERY_ENTRIES=QUERY_ENTRIES,USER_POSING_ENTRIES=USER_POSING_ENTRIES*4)

    #generate medium dataset doubling queries posed by the users
    queryBasedDatapath = os.path.join(dataPath, 'quadruple_the_querySet')
    if not os.path.exists(queryBasedDatapath):
        os.makedirs(queryBasedDatapath)
    generate_people(ids, names, surnames, heights, ages, dataPath=queryBasedDatapath)
    generate_user_set(USER_POSING_ENTRIES=USER_POSING_ENTRIES, dataPath=queryBasedDatapath)
    generate_query_set(ids, names, surnames, heights, ages, QUERY_ENTRIES*4, dataPath=queryBasedDatapath)
    generate_utility_matrix(dataPath=queryBasedDatapath, QUERY_ENTRIES=QUERY_ENTRIES*4,USER_POSING_ENTRIES=USER_POSING_ENTRIES)



def main():
    ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    # Create env folder if it doesn't exist
    if not os.path.exists(ENV_PATH):
        os.makedirs(ENV_PATH)

    USER_POSING_ENTRIES = 100

    # number of query entries
    QUERY_ENTRIES = 400

    ids = generate_ids()
    names, surnames = generate_names_surnames()
    heights = generate_heights()
    ages = generate_age()

    generateSmallDataset(ids=ids, names=names, surnames=surnames, heights=heights, ages=ages, USER_POSING_ENTRIES=USER_POSING_ENTRIES, QUERY_ENTRIES=QUERY_ENTRIES, dataPath=ENV_PATH)
    generateMediumDataset(ids=ids, names=names, surnames=surnames, heights=heights, ages=ages, USER_POSING_ENTRIES=USER_POSING_ENTRIES, QUERY_ENTRIES=QUERY_ENTRIES, dataPath=ENV_PATH)
    generateLargeDataset(ids=ids, names=names, surnames=surnames, heights=heights, ages=ages, USER_POSING_ENTRIES=USER_POSING_ENTRIES, QUERY_ENTRIES=QUERY_ENTRIES, dataPath=ENV_PATH)

if __name__ == "__main__":
    main()
