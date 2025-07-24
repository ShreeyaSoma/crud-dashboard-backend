from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
import traceback

app = Flask(__name__)
CORS(app)

# MongoDB connection setup
try:
    client = MongoClient("mongodb+srv://shreeyasoma345:admin@cluster1.bkfxexf.mongodb.net/")
    db = client["crud_data_app"]  # ✅ updated DB name
    collection = db["users_data"]  # ✅ updated collection name
    print("✅ Connected to MongoDB Atlas (crud_data_app.users_data)")
except Exception as e:
    print("❌ Failed to connect to MongoDB Atlas")
    print(traceback.format_exc())

# Helper: Serialize MongoDB document
def serialize_user(user):
    return {
        "id": str(user.get("_id")),
        "name": user.get("name", ""),
        "email": user.get("email", "")
    }

# Read All Users
@app.route("/users", methods=["GET"])
def get_users():
    try:
        users = list(collection.find())
        print("📥 Users fetched:", users)
        return jsonify([serialize_user(user) for user in users])
    except Exception as e:
        print("❌ Error in GET /users:", traceback.format_exc())
        return jsonify({"error": "Failed to fetch users"}), 500

# Create/Add User
@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.get_json()
        user = {"name": data["name"], "email": data["email"]}
        result = collection.insert_one(user)
        return jsonify({"id": str(result.inserted_id)}), 201
    except Exception as e:
        print("❌ Error in POST /users:", traceback.format_exc())
        return jsonify({"error": "Insert failed"}), 500

# Delete User by ID
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count:
            return jsonify({"message": "Deleted"}), 200
        else:
            return jsonify({"error": "Not found"}), 404
    except Exception as e:
        print("❌ Error in DELETE /users:", traceback.format_exc())
        return jsonify({"error": "Delete failed"}), 500

# Main
if __name__ == "__main__":
    app.run(debug=True)
