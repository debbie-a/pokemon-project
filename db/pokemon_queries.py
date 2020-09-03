import pymysql


connection = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    db="pokemon",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)


# returns the heaviest pokemon
def get_heaviest_pokemon():
    try:
        with connection.cursor() as cursor:
            query = "SELECT name FROM pokemon WHERE weight = (SELECT MAX(weight) FROM pokemon)"
            cursor.execute(query)
            result = cursor.fetchall()
            
            return result
    except:
        print("DB Error")


#  receives a pokemon type, and returns all of the pokemon names with that type
def find_by_type(type):
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT pokemon.name
            FROM pokemon JOIN  pokemon_type
            WHERE pokemon.id = pokemon_type.pokemon_id
            AND pokemon_type.type = '\{type}\'"""
            cursor.execute(query)
            result = cursor.fetchall()

            return result
    except:
        print("DB Error")



# receives the name of a pokemon, and returns the names of all the trainers that own it
def find_trainers(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT trainer_name
            FROM pokemon JOIN  pokemon_trainer
            WHERE pokemon.id = pokemon_trainer.pokemon_id AND name = \'{pokemon_name}\'"""
            cursor.execute(query)
            result = cursor.fetchall()

            return result
    except:
        print("DB Error")


#  receives the name of a trainer, and returns the names of all the pokemon he or she owns
def find_roster(trainer_name):
    try:
        with connection.cursor() as cursor:
            query = f"""SELECT name
            FROM pokemon JOIN  pokemon_trainer
            WHERE pokemon.id = pokemon_trainer.pokemon_id AND trainer_name = \'{trainer_name}\'"""
            cursor.execute(query)
            result = cursor.fetchall()

            return result
    except:
        print("DB Error")


# receives the name of a pokemon, and returns the the types of this pokemon
def get_types(pokemon_name):
    try:
        with connection.cursor() as cursor:
            query = f"SELECT type FROM pokemon_type WHERE pokemon_id = (SELECT id FROM pokemon WHERE name = \'{pokemon_name}\')"
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except:
        print("DB Error")


# receives the name of a pokemon, and returns its ID
def get_id(pokemon_name):
    try:
         with connection.cursor() as cursor:
            query = f"SELECT id FROM pokemon WHERE name = \"{pokemon_name}\""
            cursor.execute(query)
            result = cursor.fetchall()
            return result
    except:
        print("DB Error")


# deletes a trainer's pokemon
def delete_pokemon_of_trainer(pokemon_name, trainer_name):
    try:
        with connection.cursor() as cursor:
            query = f"""DELETE
            FROM pokemon_trainer
            WHERE trainer_name = \'{trainer_name}\' AND pokemon_id = (SELECT id FROM pokemon WHERE name = \'{pokemon_name}\');"""
            cursor.execute(query)
            result = cursor.fetchall()

            return result
    except:
        print("DB Error")


# finds the most owned pokemon
def get_most_owned_pokemon():
    try:
        with connection.cursor() as cursor:
            query = """SELECT pokemon.name, COUNT(*) as trainers
            FROM pokemon JOIN  pokemon_trainer
            ON pokemon.id = pokemon_trainer.pokemon_id
            GROUP BY pokemon.id
            ORDER BY trainers DESC;"""
            cursor.execute(query)
            result = cursor.fetchall()
            max_result = result[0].get("trainers")
            max_pokemons = []
            for item in result:
                if item.get("trainers") == max_result:
                    max_pokemons.append(item.get("name"))
                else:
                    break

            return max_pokemons
    except:
        print("DB Error")