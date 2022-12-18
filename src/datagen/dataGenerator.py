import csv
import random

from faker import Faker

# user entries is the number of users we want in the db
USER_ENTRIES = 10
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
    city_names=city_names
):
    with open('users.csv', 'w') as file:
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


def main():
    ids = generate_ids()
    names, surnames = generate_names_surnames()
    heights = generate_heights()
    ages = generate_age()
    generate_people(ids, names, surnames, heights, ages)


if __name__ == "__main__":
    main()
