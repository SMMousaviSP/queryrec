import csv
import random

from faker import Faker

# user entries is the number of users we want in the db
USER_ENTRIES = 200

USER_POSING_ENTRIES = 100

# entries of each parameter, like 10 different cities, 10 different ages..
TOTAL_ENTRIES = 10

# number of query entries
QUERY_ENTRIES = 400

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
    city_names=city_names
):
    with open('src\\dataset\\usersData.csv', 'w', newline='') as file:
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
def generate_user_set():
    with open('src\\dataset\\userSet.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        ids = []
        for i in range(0, USER_POSING_ENTRIES):
            ids.insert(0, i+USER_POSING_ENTRIES)
            writer.writerow(ids)
            ids.clear()


def generate_query_set(ids, names, surnames, heights, ages):
    with open('src\\dataset\\querySet.csv', 'w', newline='') as file:
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


def generate_utility_matrix():
    isEmpty = True
    with open('src\\dataset\\utilityMatrix.csv', 'w', newline='') as file:
        with open('src\\dataset\\querySet.csv',  'r', newline='') as myInput:
            reader = csv.reader(myInput, delimiter=',')
            writer = csv.writer(file)
            header = list(range(QUERY_ENTRIES))
            writer.writerow(header)
            for i in range(0, USER_POSING_ENTRIES):
                #ids of user set starts from USER_POSING_ENTRIES
                data = ['user'+str(i + USER_POSING_ENTRIES)]
                for row in reader:
                    isEmpty = True
                    if(i < 30): #make first 30 users like queries that have names that start with R or D or J or S
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'name' and item.split('=')[1].startswith(('R','r','D','d','J','j','S','s'))):
                                data.append(random.sample(range(70,100),1)[0])
                                isEmpty = False

                    elif(i >= 30 and i < 60): #make next 30 users dislike queries that have names that start with R or D or J or S
                        for item in row: #this only works on single params, doesn't work with AND
                            if(item.split('=')[0] == 'name' and item.split('=')[1].startswith(('R','r','D','d','J','j','S','s'))):
                                data.append(random.sample(range(0,40),1)[0])
                                isEmpty = False

                    elif(i >= 60 and i < 85): #make next 25 users like queries with age AND name starting with R or D or J or S
                        items = [item for item in row if item.startswith(('name','age'))] # have a list with the params we need
                        if(len(items) == 2): #check if we got the right amount of params
                            if(items[0].split('=')[1].startswith(('R','r','D','d','J','j','S','s')) and int(items[1].split('=')[1]) >= 36):
                                data.append(random.sample(range(70,100),1)[0])
                                isEmpty = False
                    
                    elif(i >= 60 and i < 85): #make next 25 users like queries with any city
                        items = [item for item in row if item.startswith(('city'))] # have a list with the params we need
                        if(len(items) == 1): #check if we got the right amount of params
                            data.append(random.sample(range(70,100),1)[0])
                            isEmpty = False

                    elif(i >= 85 and i < 95): #make next 10 users like queries with any city but dislike the ones with age
                        items = [item for item in row if item.startswith(('city','age'))] # have a list with the params we need
                        if(len(items) == 2): #check if we got the right amount of params
                            data.append(random.sample(range(0,30),1)[0])
                            isEmpty = False
                        else:
                            if(item.split('=')[0] == 'age'): #if only age, dislike
                                data.append(random.sample(range(0,30),1)[0])
                                isEmpty = False
                            else: #we have only city and they like any city
                                data.append(random.sample(range(50,100),1)[0])
                                isEmpty = False
                    
                    #elif(i >= 95 and i < USER_POSING_ENTRIES): this creates an user than never posed queries, no need for this as it's already done below for all the users
                        #data.append('')
                            
                    if(isEmpty): #if query was not posed add empty value
                        data.append('') #append empty element as the query was not posed before


                writer.writerow(data)
                data.clear()
                myInput.seek(0) #reset file pointer to begin
                #could also store the data in memory and iterate how many times we want instead of doing this, depends on the size, this always works.



def main():
    ids = generate_ids()
    names, surnames = generate_names_surnames()
    heights = generate_heights()
    ages = generate_age()
    #generate_people(ids, names, surnames, heights, ages)
    #generate_user_set()
    #generate_query_set(ids, names, surnames, heights, ages)
    generate_utility_matrix()


if __name__ == "__main__":
    main()
