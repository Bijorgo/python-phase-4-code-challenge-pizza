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
            response = []
            for restaurant in data:
                response.append({
                    "address": data.address,
                    "id": data.id,
                    "name": data.name
                })
                return make_response({"restaurants": response}, 200)
        else:
            return make_response({"message": "No restaurants found"}, 404)
    except Exception as esc:
        return make_response({"error": str(esc)}, 500)
    
#app.get("/restaurants/int:id")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
