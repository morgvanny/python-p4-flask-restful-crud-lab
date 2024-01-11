#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import Plant, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plants.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):
    def get(self):
        return make_response([plant.to_dict() for plant in Plant.query.all()], 200)

    def post(self):
        data = request.get_json()
        plant = Plant()
        for attr in data:
            setattr(plant, attr, data[attr])

        db.session.add(plant)
        db.session.commit()
        return make_response(plant.to_dict(), 201)


api.add_resource(Plants, "/plants")


class PlantById(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = Plant.query.get(id)
        data = request.get_json()
        for attr in data:
            setattr(plant, attr, data[attr])

        db.session.add(plant)
        db.session.commit()

        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.get(id)
        db.session.delete(plant)
        db.session.commit()
        return make_response("", 204)


api.add_resource(PlantById, "/plants/<int:id>")


@app.route("/")
def home():
    return make_response({"message": "Welcome to my plant website"}, 200)


if __name__ == "__main__":
    app.run(port=5555, debug=True)


# Create
#    POST /plants
# Read
#  Index
#    GET /plants
#  Single Plant
#    GET /plants/<int:id>
# Update
#    PATCH/PUT /plants/<int:id>
# Destroy
#    DELETE /plants/<int:id>
