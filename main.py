from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Café TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


def jsonify_cafe(cafe):
    return jsonify(
        id=cafe.id,
        name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        seats=cafe.seats,
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        has_sockets=cafe.has_sockets,
        can_take_calls=cafe.can_take_calls,
        coffee_price=cafe.coffee_price
    )


@app.route("/random")
def random():
    all_cafes = db.session.query(Cafe).all()
    random_cafe = choice(all_cafes)
    return jsonify_cafe(random_cafe)


@app.route("/all")
def all_cafe():
    all_cafes = db.session.query(Cafe).all()
    jsonify_cafes = [jsonify_cafe(cafe).json for cafe in all_cafes]
    return jsonify(cafes=jsonify_cafes)


@app.route("/search")
def search():
    all_cafes = db.session.query(Cafe).filter(Cafe.location == request.args["area"]).all()
    jsonify_cafes = [jsonify_cafe(cafe).json for cafe in all_cafes]
    print(jsonify_cafes)
    return jsonify(cafes=jsonify_cafes)


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    cafe.coffee_price = request.args["pc"]
    db.session.commit()
    return jsonify({'success': 'Cafe updated successfully'})


@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if request.args["api_key"] == "TopSecretAPIKey":
        db.session.delete(cafe)
        db.session.commit()
    return jsonify({'success': 'Cafe updated successfully'})


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_cafe = Cafe(
            id=request.form.get("id"),

            img_url="null",

            has_sockets=1,
            has_toilet=1,
            has_wifi=1,
            can_take_calls=1,
            seats=20,

            name=request.args["name"],
            map_url=request.args["url"],
            location=request.args["loc"],
            coffee_price=request.args["cp"],
        )
        db.session.add(new_cafe)
        db.session.commit()

        return {
            "response": "Success! New cafe added.",
            "cafe": {
                "name": request.args["name"],
                "location": request.args["loc"],
                "coffee price": request.args["cp"],
                "url": request.args["url"],
            }
        }
    else:
        return {"response": "bad request. Nothing added."}


# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
