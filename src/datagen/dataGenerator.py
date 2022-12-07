import csv, string, random, time, sys, io
from faker import Faker

#user entries is the number of users we want in the db
USER_ENTRIES = 10
#entries of each parameter, like 10 different cities, 10 different ages..
TOTAL_ENTRIES = 10
city_names = {"Trento", "Bolzano", "Verona", "Brescia", "Milano", "Bologna", "Torino", "Venezia", "Bergamo", "Rovereto"}

#ids not used, just use the index of the for as i
IDs_set = set()

def generate_ids():
    while(len(IDs_set) < TOTAL_ENTRIES):
        IDs_set.add(random.sample(range(1,TOTAL_ENTRIES), TOTAL_ENTRIES))
    return IDs_set

def generate_names_surnames():
    fake = Faker('en_US')
    nameSet = set()
    surnameSet = set()
    while(len(nameSet) < TOTAL_ENTRIES and len(surnameSet) < TOTAL_ENTRIES):
        mystring = fake.name().split()
        name = mystring[0]
        nameSet.add(name)

        surname = mystring[1]
        surnameSet.add(surname)

    return nameSet, surnameSet


def generate_heights():
    heights_set = set()
    while(len(heights_set) < TOTAL_ENTRIES):
        height = random.sample(range(150,200), 1)
        heights_set.add(height[0])

    return heights_set


def generate_age():
    age_set = set()
    while(len(age_set) < TOTAL_ENTRIES):
        age = random.sample(range(30,50), 1)
        age_set.add()


def generate_people(names, surnames, heights):
    with open('users.csv','w') as file:
        header = ['id', 'name', 'surname', 'height', 'age', 'city']
        writer = csv.writer(file)
        writer.writerow(header)
        for i in range(0,USER_ENTRIES):
            data = [i, random.sample(names,1), random.sample(surnames,1), random.sample(heights,1), random.sample(city_names,1)]
            writer.writerow(data)




def main():

    names, surnames = generate_names_surnames()
    heights = generate_heights()
    generate_people(names,surnames,heights)
    

main()