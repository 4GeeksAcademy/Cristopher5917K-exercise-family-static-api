"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as error:
        return jsonify("No se encontraron contactos"),400

@app.route('/member', methods =['POST'])
def  post_members():
    try:
        body = request.json
        if type(body) == dict:
            if body.get("first_name") == None or body.get("age") == None or body.get("lucky_numbers")==None:
                return jsonify("Invalid operation"),400

            else:
               result = jackson_family.add_member(body)
               if result == True:
                    return jsonify([]),200
        else:
            return jsonify("Invalid Body"),400

    except Exception as error:
        return jsonify("Se tumbo el servidor:("),500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        result = jackson_family.delete_member(member_id)
        if result is None:
            return jsonify({"message":"family member not found"}),404
        return jsonify({"done":True}),200 

    except Exception as error:
        print(error)
        return jsonify("The server encounters an error"),500

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        member = jackson_family.get_member(member_id)
        return jsonify(member),200
    except Exception as error:
        return jsonify("The server found an error"), 500

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
