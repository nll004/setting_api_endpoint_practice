"""Flask app for Cupcakes"""
from flask import Flask, jsonify, render_template, request
from models import db, connect_db, Cupcake, serialize

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def home():

    return render_template('index.html')


# ===================================================================================
# ------------------API ROUTES-------------------
# ===================================================================================

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    '''Get all cupcakes from database and serialize them into a list of dictionaries'''
    all_cupcakes = [serialize(cake) for cake in Cupcake.query.all()]

    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Take post data as json and store in database'''

    data = request.json

    new_cupcake = Cupcake(
        flavor = data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    cupcake = serialize(new_cupcake)
    return (jsonify(cupcake=cupcake), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["GET"])
def get_cupcake(cupcake_id):
    '''Get one cupcake by id'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake = serialize(cupcake)

    return jsonify(cupcake= cupcake)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def edit_cupcake(cupcake_id):
    '''Take cupcake info and edit it in database'''

    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image'] or None

    db.session.add(cupcake)
    db.session.commit()

    cupcake = serialize(cupcake)

    return (jsonify(cupcake= cupcake), 201)


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    '''Remove cupcake from database and return a json response notifying the client'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
