import pymysql
import json
from pymysql import IntegrityError


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)
if connection.open:
    print("the connection is opened")

# inserting data into pokemon table
def insert_pokemon(id, name, height, weight):
    try:
        with connection.cursor() as cursor:
                query = f"INSERT INTO pokemon VALUES ({id}, \"{name}\", {height}, {weight})"
                cursor.execute(query)
                connection.commit() 

    except IntegrityError:
            return print("pokemon already exists in db"), 409

    except:
        print("Error")


# inserting data into pokemon_type table
def insert_pokemon_type(pokemon_id, type_name):
    try:
        with connection.cursor() as cursor:
            query = f"INSERT INTO pokemon_type VALUES ({pokemon_id}, \"{type_name}\")"
            cursor.execute(query)
            connection.commit()

    except IntegrityError:
            return print("pokemon_type already exists in db"), 409

    except:
        print("Error")


# inserting data into trainer table
def insert_trainer(name, town):
        try:
            with connection.cursor() as cursor:
                query = f"INSERT INTO trainer VALUES (\"{name}\", \"{town}\")"
                cursor.execute(query)
                connection.commit()

        except IntegrityError:
            return print("trainer already exists in db"), 409

        except:
            print("Error")


# inserting data into pokemon_trainer table
def insert_pokemon_trainer(trainer_name, pokemon_id):
    try:
        with connection.cursor() as cursor:
            query = f"INSERT INTO pokemon_trainer VALUES (\"{trainer_name}\", {pokemon_id})"
            cursor.execute(query)
            connection.commit()

    except IntegrityError:
            return print("pokemon-trainer already exists in db"), 409

    except:
        print("Error")


# opens json file and returns data
def open_file(file_name):
    with open(file_name) as file:
        pokemon_data = json.load(file)
        
        return pokemon_data


# in charge of inserting data to db tables
def insert_data():
    pokemon_data = open_file("pokemon_data.json")

    for item in pokemon_data:
        insert_pokemon(item["id"], item["name"], item["height"], item["weight"])
        types = item["type"]

        # type can be in a list or string, so if string we split to list
        if type(types) == str:
            types = types.split()

        for type_ in types:
            insert_pokemon_type(item["id"], type_)

        for trainer in item["ownedBy"]:
            insert_trainer(trainer["name"], trainer["town"])
            insert_pokemon_trainer(trainer["name"], item["id"])