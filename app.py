import re
import hashlib
import json
import secrets

from flask import Flask, request, jsonify

app = Flask(__name__)

db_pth = "../users" # path to users on remote


def hash(user, passw, salt):
    prep = lambda user, passw, sal: ((user + passw ).encode() + sal)
    encoded_prep = prep(user, passw, salt)
    hashed = (hashlib.sha256(encoded_prep)).hexdigest()
    return hashed



def user_exists(user):
    with open(db_pth, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {}

        if user in data:
            return True
        else:
            return False


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'user' not in data:
        return jsonify({'Error': 'User field is missing'}), 400
    if 'pass' not in data:
        return jsonify({'Error': 'Password field is missing'}), 400
    if not user_exists(data['user']):
        return jsonify({'Error': 'User does not exist'}), 404
    
    else:
        # Retrieve salt from the database
        with open(db_pth, 'r') as file:
            db_data = json.load(file)
            salt = db_data[data['user']]['salt']

        # Hash the provided password with the retrieved salt
        hashed_pass = hash(data['user'], data['pass'], salt)

        # Compare the hashed password with the one stored in the database
        if secrets.compare_digest(hashed_pass, db_data[data['user']]['token']):
            return jsonify({'Message': 'Login successful'}), 200
        else:
            return jsonify({'Error': 'Incorrect password'}), 401



if __name__ == '__main__':
    app.run(debug=True, port=5002)
    #add port=##### to change the port the api uses