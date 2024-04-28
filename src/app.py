"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, UserPeopleFavorite, UserPlanetFavorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))

    return jsonify(all_users), 200

# This endpoint gets all the people in the database
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    serialized_people_list = list(map(lambda People: People.serialize(), people))
    
    return jsonify(serialized_people_list), 200

# This endpoint gets a person by id number
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get_or_404(people_id)
    
    return jsonify(person.serialize()), 200

# This endpoint adds a person to the database
@app.route('/people', methods=['POST'])
def add_person():

    request_body = request.get_json()
    person = People(name=request_body["name"], height=request_body["height"], weight=request_body["weight"], gender=request_body["gender"])
    db.session.add(person)
    db.session.commit()

    return f"The person {request_body['name']} was added to the database", 200

# This endpoint gets all the planets in the database
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    serialized_planets_list = list(map(lambda Planets: Planets.serialize(), planets))
    
    return jsonify(serialized_planets_list), 200

# This endpoint adds a planet to the database
@app.route('/planets', methods=['POST'])
def add_planet():

    request_body = request.get_json()
    planet = Planets(name=request_body["name"], climate=request_body["climate"], terrain=request_body["terrain"], resources=request_body["resources"])
    db.session.add(planet)
    db.session.commit()

    return f"The planet {request_body['name']} was added to the database", 200

# This endpoint gets a planet by id number
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get_or_404(planet_id)
    
    return jsonify(planet.serialize()), 200

# This endpoint gets all of a users favorites
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    # Get user_id from request or session, assuming it's available
    user_id = request.json.get('user_id')  # Assuming user_id is passed in the request JSON

    # Check if user_id is provided
    if user_id is None:
        return jsonify({"error": "User ID is required."}), 400
    
    # Query user
    user = User.query.get(user_id)

    # Check if user exists
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    # Query user's favorites
    favorites = user.favorites
    
    # Serialize favorites
    serialized_favorites = [favorite.serialize() for favorite in favorites]
    
    return jsonify(serialized_favorites), 200

# Adds user's favorite people
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    # grabs the user id from the request body
    user_id = request.json.get('user_id')

    user = User.query.get(user_id)
    person = People.query.get(people_id)

    favorite_relation = UserPeopleFavorite(user_id=user_id, people_id=people_id)
    db.session.add(favorite_relation)
    db.session.commit()

    return jsonify({"message": f"Added {person.name} to favorites for user {user.name}"}), 200

# Adds user's favorite planets
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planets(planet_id):
    # grabs the user id from the request body
    user_id = request.json.get('user_id')

    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    favorite_relation = UserPlanetFavorite(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite_relation)
    db.session.commit()

    return jsonify({"message": f"Added {planet.name} to favorites for user {user.name}"}), 200

# Endpoint to delete a favorite planet for the current user
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    # Get user_id from request or session, assuming it's available
    user_id = request.json.get('user_id')  # Assuming user_id is passed in the request JSON
    
    # Check if user_id is provided
    if user_id is None:
        return jsonify({"error": "User ID is required."}), 400
    
    # Query user
    user = User.query.get(user_id)
    
    # Check if user exists
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    # Query the favorite planet to be deleted
    favorite_planet = Planets.query.get(planet_id)
    
    # Check if the favorite planet exists
    if favorite_planet is None:
        return jsonify({"error": "Favorite planet not found."}), 404
    
    # Check if the favorite planet is actually a favorite of the user
    if favorite_planet not in user.planet_favorites:
        return jsonify({"error": "Planet is not a favorite of the user."}), 400
    
    # Remove the planet from the user's favorite planets
    user.planet_favorites.remove(favorite_planet)
    db.session.commit()
    
    return jsonify({"message": f"Favorite planet {favorite_planet.name} deleted for user {user.name}"}), 200

# Endpoint to delete a favorite people for the current user
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_person(people_id):
    # Get user_id from request or session, assuming it's available
    user_id = request.json.get('user_id')  # Assuming user_id is passed in the request JSON
    
    # Check if user_id is provided
    if user_id is None:
        return jsonify({"error": "User ID is required."}), 400
    
    # Query user
    user = User.query.get(user_id)
    
    # Check if user exists
    if user is None:
        return jsonify({"error": "User not found."}), 404
    
    # Query the favorite person to be deleted
    favorite_person = People.query.get(people_id)
    
    # Check if the favorite person exists
    if favorite_person is None:
        return jsonify({"error": "Favorite person not found."}), 404
    
    # Check if the favorite person is actually a favorite of the user
    if favorite_person not in user.people_favorites:
        return jsonify({"error": "Person is not a favorite of the user."}), 400
    
    # Remove the person from the user's favorite people
    user.people_favorites.remove(favorite_person)
    db.session.commit()
    
    return jsonify({"message": f"Favorite person {favorite_person.name} deleted for user {user.name}"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
