from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)


class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    # add relationship
    rpizzas = db.relationship("RestaurantPizzas", back_populates="restaurants")
    pizza = association_proxy("rpizzas", "pizzas")

    # add serialization rules
    serialize_rules = ("rpizzas", "-rpizzas.restaurants")

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    rest_pizzas = db.relationship("RestaurantPizzas", back_populates="pizzas")
    restaurant = association_proxy("rest_pizzas", "restaurants")

    # add serialization rules
    serialize_rules = ("rest_pizzas", "-rest_pizzas.pizzas")

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurants = db.relationship("Restaurant", back_populates="rpizzas")
    pizzas = db.relationship("Pizzas", back_populates="rest_pizzas")
    restaurants_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    pizzas_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))


    # add serialization rules
    serialize_rules = ("-restaurants", "-pizzas")

    # add validation
    @validates("price")
    def validate_price(self, key, value):
        if not (1 < value < 30):
            raise ValueError(f"{key} must be between 1 and 30")


    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
