#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

@app.get("/restaurants")
def get_restaurants():
    try:
        data = Restaurant.query.all() # Get all restaurants
        if data:
            response = [restaurant.to_dict() for restaurant in data] # Return array of restaurants
            return make_response({"restaurants": response}, 200) # Sucess
        else:
            return make_response({"message": "No restaurants found"}, 404) # Not Found
    except Exception as esc:
        return make_response({"error": str(esc)}, 500) # Internal Server Error
    
@app.get("/restaurants/int:id")
def get_rest_by_id():
    # if restaurant exists
        # return JSON data
    # if not exist
        # {"error": "Restaurant not found"}, 404 # Not Found
    pass

@app.delete("/restaurants/int:id")
def delete_rest():
    # if rest exists
        # remove from database
        # remove junctions ( a restaurantPizza belongs to a Restaurant)
            # Consider setting up cascase deltes in models
    # if not exists
        # return JSON data {"error": "Restaurant not found"}, 404 # Not Found
    pass

@app.get("/pizzas")
def get_all_pizzas():
    try:
        data = Pizza.query.all() # Get all pizzas
        if data:
            response = [pizza.todict() for pizza in data] # Return array of pizzas
            return make_response({"pizzas": response}, 200) # Success
        else:
            return make_response({"message": "No pizzas found"}, 404) # Not Found
    except Exception as esc:
        return make_response({"error": str(esc)}, 500) # Internal Server Error

@app.post("/restaurant_pizzas")
def add_junction():
    # create new RestaurantPizza associating existing Pizza and Restaurant
    # body of request has object:
        # price
        # pizza_id
        # restaurant_id
    # if sucessfully created, 
        # return JSON data related to RestaurantPizza
    # if not sucessfully created due to validation error
        # return JSON data "errors": ["validation errors"], CODE?   
    pass

if __name__ == "__main__":
    app.run(port=5555, debug=True)
