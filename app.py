from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)  # To allow cross-origin requests from frontend

# MongoDB Connection
client = MongoClient("mongodb+srv://shreeyasoma345:admin@cluster1.bkfxexf.mongodb.net/")
db = client["dashboard_app"]
collection = db["users_data"]  # ✅ Correct collection name

# GET all users
@app.route("/users", methods=["GET"])
def get_users():
    users = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ID
    return jsonify(users)

# POST: Add a new user
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "User added successfully"}), 201

# PUT: Update user by email
@app.route("/users/<email>", methods=["PUT"])
def update_user(email):
    data = request.json
    result = collection.update_one({"email": email}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "User updated successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

# DELETE: Delete user by email
@app.route("/users/<email>", methods=["DELETE"])
def delete_user(email):
    result = collection.delete_one({"email": email})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"message": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
