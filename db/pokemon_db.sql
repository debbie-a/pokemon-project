DROP Database pokemon
CREATE DATABASE pokemon

USE pokemon;


CREATE TABLE pokemon (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    height INT,
    weight INT
)

CREATE TABLE  pokemon_type (
    pokemon_id INT,
    type VARCHAR(20),

    PRIMARY KEY(type, pokemon_id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
)

CREATE TABLE trainer (
    name VARCHAR(20) PRIMARY KEY,
    town VARCHAR(20)
)

CREATE TABLE pokemon_trainer (
    trainer_name VARCHAR(20),
    pokemon_id INT,

    PRIMARY KEY(trainer_name, pokemon_id),
    FOREIGN KEY(trainer_name) REFERENCES trainer(name),
    FOREIGN key(pokemon_id) REFERENCES pokemon(id)
)
