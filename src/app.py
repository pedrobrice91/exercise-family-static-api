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
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    print(members)
    return jsonify(members)
   
    
@app.route('/member', methods=['POST'])
def method_post():   
    request_body = request.json
    jackson_family.add_member(request_body)
    return jsonify(request_body)
    
@app.route('/member/<int:id>', methods=['GET', 'DELETE'])
def get_member_by_id(id):
    if request.method == 'GET':
        member = jackson_family.get_member(id)
        return jsonify(member)
    elif request.method == 'DELETE': 
        members = jackson_family.delete_member(id)
        return jsonify(members)


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)