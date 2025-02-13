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
app.config['JSON_COMPACT'] = False

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
    
@app.get("/restaurants/<int:id>")
def get_rest_by_id(id):
    try:
        restaurant = Restaurant.query.filter_by(id=id).first()
        if restaurant:
            response = restaurant.to_dict()
            response["restaurant_pizzas"] = [
                {
                    "id": rp.id,
                    "price": rp.price,
                    "restaurant_id": rp.restaurant_id,
                    "pizza_id": rp.pizza_id,
                    "pizza": rp.pizza.to_dict()
                }
                for rp in restaurant.rest_pizzas
            ]
            return make_response(response, 200)
        else:
            return make_response({"error": "Restaurant not found"}, 404)
    except Exception as esc:
        return make_response({"error": str(esc)}, 500)

@app.delete("/restaurants/<int:id>")
def delete_rest(id):
    try:
        restaurant = Restaurant.query.get(id)
        if restaurant:
            # Delete associated restaurant pizzas
            for rp in restaurant.rest_pizzas:
                db.session.delete(rp)
            db.session.delete(restaurant)
            db.session.commit()
            return make_response({}, 204)  # No content
        else:
            return make_response({"error": "Restaurant not found"}, 404)
    except Exception as esc:
        return make_response({"error": str(esc)}, 500)


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
    try:
        data = request.get_json()
        price = data.get("price")
        pizza_id = data.get("pizza_id")
        restaurant_id = data.get("restaurant_id")

        # Check if pizza and restaurant exist
        pizza = Pizza.query.get(pizza_id)
        restaurant = Restaurant.query.get(restaurant_id)

        if not pizza or not restaurant:
            return make_response({"error": "Pizza or Restaurant not found"}, 404)

        # Create the new RestaurantPizza object
        try:
            new_rp = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
            db.session.add(new_rp)
            db.session.commit()

            # Return created data
            return make_response({
                "id": new_rp.id,
                "price": new_rp.price,
                "restaurant_id": new_rp.restaurant_id,
                "pizza_id": new_rp.pizza_id,
                "pizza": pizza.to_dict(),
                "restaurant": restaurant.to_dict()
            }, 201)
        except ValueError as e:
            return make_response({"errors": [str(e)]}, 400)

    except Exception as esc:
        return make_response({"error": str(esc)}, 500)


if __name__ == "__main__":
    app.run(port=5555, debug=True)
