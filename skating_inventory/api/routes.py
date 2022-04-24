from flask import Blueprint, request, jsonify
from skating_inventory.helpers import token_required
from skating_inventory.models import db, User, Skate, skate_schema, skates_schema


api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'some': 'value'}

# Create skate endpoint
@api.route('/skates', methods= ['POST'])
@token_required
def create_skate(current_user_token):
    deck_brand = request.json['deck_brand']
    grip_tape = request.json['grip_tape']
    trucks = request.json['trucks']
    wheels = request.json['wheels']
    bearings = request.json['bearings']
    hardware = request.json['hardware']
    price = request.json['price']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    skate = Skate(deck_brand, grip_tape, trucks, wheels, bearings, hardware, price, user_token = user_token)

    db.session.add(skate)
    db.session.commit()

    response = skate_schema.dump(skate)
    return jsonify(response)

# Retrieve all skate endpoints
@api.route('/skates', methods = ['GET'])
@token_required
def get_skates(current_user_token):
    owner = current_user_token.token
    skates = Skate.query.filter_by(user_token = owner).all()
    response = skates_schema.dump(skates)
    return jsonify(response)

# Retrieve One Drone Endpoint
@api.route('/skates/<id>', methods = ['GET'])
@token_required
def get_skate(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        skate = Skate.query.get(id)
        response = skate_schema.dump(skate)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401

# Update skate endpoint
@api.route('/skates/<id>', methods = ['POST', 'PUT'])
@token_required 
def update_skate(current_user_token, id):
    skate = Skate.query.get(id) #grab skate instance

    skate.deck_brand = request.json['deck_brand']
    skate.grip_tape = request.json['grip_tape']
    skate.trucks = request.json['trucks']
    skate.wheels = request.json['wheels']
    skate.bearings = request.json['bearings']
    skate.hardware = request.json['hardware']
    skate.price = request.json['price']
    skate.user_token = current_user_token.token

    db.session.commit()
    response = skate_schema.dump(skate)
    return jsonify(response)


#Delete skate endpoint
@api.route('/skates/<id>', methods = ['DELETE'])
@token_required
def delete_skate(current_user_token, id):
    skate = Skate.query.get(id)
    db.session.delete(skate)
    db.session.commit()
    response = skate_schema.dump(skate)
    return jsonify(response)