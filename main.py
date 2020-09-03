from db import insert_db
from db import pokemon_queries


if __name__ == '__main__':
    # insert_db.insert_data()
    print(pokemon_queries.get_heaviest_pokemon())
    print(pokemon_queries.find_by_type("grass"))
    # print(find_trainers("gengar"))
    # print(find_roster("Loga"))
    # print(get_most_owned_pokemon())