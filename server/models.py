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
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # add relationship
    rpizzas = db.relationship("RestaurantPizza", back_populates="restaurant")
    #pizza = association_proxy("rpizzas", "pizzas")

    # add serialization rules
    serialize_rules = ("rpizzas", "-rpizzas.restaurants")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address
        }

    def __repr__(self):
        return f"<Restaurant {self.name}>"


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)

    # add relationship
    rest_pizzas = db.relationship("RestaurantPizza", back_populates="pizza")
    #restaurant = association_proxy("rest_pizzas", "restaurants")

    # add serialization rules
    serialize_rules = ("rest_pizzas", "-rest_pizzas.pizzas")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "ingredients": self.ingredients
        }

    def __repr__(self):
        return f"<Pizza {self.name}, {self.ingredients}>"


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    # add relationships
    restaurant = db.relationship("Restaurant", back_populates="rpizzas")
    pizza = db.relationship("Pizza", back_populates="rest_pizzas")
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id", ondelete='CASCADE'))
    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))


    # add serialization rules
    serialize_rules = ("-restaurants", "-pizzas")

    # add validation
    @validates('price')
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError(["Price must be between 1 and 30"])
        return price
    
    def to_dict(self):
        return {
            "id": self.id,
            "price": self.price,
            "pizza": self.pizza.to_dict() if self.pizza else None,
            "pizza_id": self.pizza_id,
            "restaurant": self.restaurant.to_dict() if self.restaurant else None,
            "restaurant_id": self.restaurant_id
        }

    def __repr__(self):
        return f"<RestaurantPizza ${self.price}>"
