from flask import Flask, request, redirect, render_template
from db import pokemon_queries
from db import insert_db
import json
import requests
from flask_mail import Mail, Message
import local_settings
from PIL import Image, ImageOps
import os.path
from PIL import Image


app = Flask(__name__, static_url_path='', static_folder='templates', template_folder='templates')
mail = Mail(app)


@app.route('/sanity')
def sanity():
    return "Server up and running"


# home
@app.route('/')
def pokemon_home_page():
    return redirect('/home_page.html')


# get 
@app.route('/pokemons')
def track_pokemon_data():
    
    pokemon_to_track_trainers = request.args.get('pokemon')
    trainer_to_track_pokemons = request.args.get('trainer')
    type_to_track_pokemons = request.args.get('type')
    results = []

    # trainer by pokemon
    if pokemon_to_track_trainers:
        result = pokemon_queries.find_trainers(pokemon_to_track_trainers)
        # return json.dumps([x["trainer_name"] for x in result]), 200
        results = [x["trainer_name"] for x in result] if [x["trainer_name"] for x in result] else "no results found"
        return render_template('/poke_return_page.html', name = results, the_url= ''), 200

    # pokemon by trainer
    elif trainer_to_track_pokemons:
        result = pokemon_queries.find_roster(trainer_to_track_pokemons)
        # return json.dumps([x["name"] for x in result]), 200
        results = [x["name"] for x in result] if [x["name"] for x in result] else "no results found"
        return render_template('/poke_return_page.html', name = results, the_url= ''), 200
        
    
    # pokemon by type
    elif type_to_track_pokemons:
        result = pokemon_queries.find_by_type(type_to_track_pokemons)
        # return json.dumps([x["name"] for x in result]), 200
        results = [x["name"] for x in result] if [x["name"] for x in result] else "no results found"
        return render_template('/poke_return_page.html', name = results, the_url= ''), 200
        
    else:
        #return json.dumps("Error invalid syntax"), 400
        return render_template('/poke_return_page.html', name = "invalid input", the_url= ''), 400


# add
@app.route('/pokemons', methods=["POST"])
def add_pokemon():
    pokemon = request.get_json()

    if not pokemon.get("id") or not pokemon.get("name") or not pokemon.get("height") or not pokemon.get("height") or not pokemon.get("type"):
        return json.dumps("invalid pokemon data"), 400

    try:
        insert_db.insert_pokemon(pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
        # type can be in a list or string, so if string we split to list
        types = pokemon["type"]
        if type(types) == str:
            types = types.split()

        for type_ in types:
            insert_db.insert_pokemon_type(pokemon["id"], type_)

        name = pokemon["name"]
        return json.dumps(f"added {name} to pokemon table"), 200


    except:
        return json.dumps("pokemon already exists"), 409


# update
@app.route('/pokemons/<pokemon_name>', methods=["PUT"])
def update_types(pokemon_name):
    # get pokemons' id by its name
    pokemon_id = pokemon_queries.get_id(pokemon_name) 
    if not pokemon_id:
        return json.dumps("Error invalid pokemon name"), 400


    URL = 'https://pokeapi.co/api/v2/pokemon/{pokemon_name}'
    pokemon_data = requests.get(url = URL, verify = False).json()

    types = [type["type"]["name"] for type in pokemon_data["types"]]

    # pokemons' types that are already updated
    pokemon_types = pokemon_queries.get_types(pokemon_name)
    pokemon_types = [x["type"] for x in pokemon_types]


    for type_ in types:
        if type_ not in pokemon_types:
            insert_db.insert_pokemon_type(pokemon_id, type_)
            
    return json.dumps(f"updated types for pokemon: {pokemon_name}"), 200
    

# delete
@app.route('/pokemons/<pokemon>/<trainer>', methods=['DELETE'])
def delete(pokemon, trainer):
    try:
        pokemon_queries.delete_pokemon_of_trainer(pokemon, trainer)
        return json.dumps(f"deleted {pokemon} that belonged to {trainer}")

    except:
        return json.dumps("Error: invalid pokemon or trainer"), 400 




##############  Pokie Selfie ##############
# cool app: snap a selfie with a pokemon of your choice! get it via email!!!

# embeds a pokemon to a selfie pic
def embed_pictures(selfie_picture, pokemon_picture, path):
    #add border
    im = ImageOps.expand(selfie_picture, border=40, fill='gold')
    #add logo
    logo = Image.open('templates/poke_logo.png')
    img_w, img_h = im.size
    logo_w, logo_h = logo.size
    logo = logo.resize((logo_w//4, logo_h//4))
    logo_w, logo_h = logo.size
    offset = (img_w // 2 - logo_w // 2, 0)
    im.paste(logo, offset, mask = logo)
    #add selected pokemon
    poke_w, poke_h = pokemon_picture.size
    pokemon = pokemon_picture.resize((poke_w // 3, poke_h // 3))
    poke_w, poke_h = pokemon.size
    offset2 = (20, img_h - poke_h)
    im.paste(pokemon, offset2)
    im.save(path)


#pokeSelfie
@app.route('/pokemons/pokeSelfies')
def poke_selfie():
    pokemon_name = request.args.get('pokemon')
    email = request.args.get('email')

    if not pokemon_name or not email:
        return render_template('/poke_selfie2.html', name = "invalid input", the_url= ''), 400
        
    # path to downlods folder in pc where server is running
    selfie_picture = Image.open("C:\\Users\\1\\Downloads\selfie.png")

    try:
        # path to folder with all pokemon images
        pokemon_path = os.path.join("images", f'{pokemon_name}.jpg')
        pokemon_picture = Image.open(pokemon_path)

        # path to folder where the ready pokeSelfies are stored
        pokeSelfie_path = os.path.join("pokieSelfies", f'{email}.png')
        embed_pictures(selfie_picture, pokemon_picture, pokeSelfie_path)

        # delete selfie from downlowds
        os.remove("C:\\Users\\1\\Downloads\selfie.png")

    except FileNotFoundError:
        return render_template('/poke_return_page.html', name = "invalid pokemon to snap a selfie with", the_url= ''),


     # configuration of mail 
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'pokeselfie.pokemon@gmail.com'
    # keep in seperate module my passworrd for security reasons...
    app.config['MAIL_PASSWORD'] = local_settings.MAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app) 

    try:
       
        with mail.connect() as conn:
            message = f"this is your very cool pokeSelfie with {pokemon_name}"
            subject = "PokeSelfie"


            msg = Message('PokieSelfie', sender = 'pokeselfie.pokemon@gmail.com', recipients = [email])
            msg.body = f"Your selfie from PokeSelfie with {pokemon_name}"
            with app.open_resource(pokeSelfie_path) as fp:
                msg.attach(f"pokeSelfieWith_{pokemon_name}.png", "image/png", fp.read())

            conn.send(msg)
            # delete pokeSelfie from local storage
            os.remove(pokeSelfie_path)

            return render_template('/poke_return_page.html', name = "Your PokeSelfie is on its way", the_url= ''), 200

    except ConnectionRefusedError:
        return render_template('/poke_return_page.html', name = "error sending email", the_url= ''), 505
        
    


if __name__ == '__main__':
    app.run(port=3000)