# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas
MONGO_URI = "mongodb+srv://shreeyasoma345:admin@cluster1.bkfxexf.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["dashboard_app"]
collection = db["users"]

# Serialize MongoDB document to JSON
def serialize_user(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }

# Get all users
@app.route("/users", methods=["GET"])
def get_users():
    users = collection.find()
    return jsonify([serialize_user(user) for user in users]), 200

# Add a new user
@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    result = collection.insert_one(data)
    new_user = collection.find_one({"_id": result.inserted_id})
    return jsonify(serialize_user(new_user)), 201

# Update user
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})
    if result.modified_count == 0:
        return jsonify({"error": "User not found or no change"}), 404
    updated_user = collection.find_one({"_id": ObjectId(user_id)})
    return jsonify(serialize_user(updated_user)), 200

# Delete user
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(port=5000)
