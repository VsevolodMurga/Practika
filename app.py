from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import functools

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "123456"
jwt = JWTManager(app)

users = {
    "admin": {"password": "adminpass", "role": "Admin"},
    "user": {"password": "userpass", "role": "User"},
}

data = []

@app.route("/login", methods=["POST"])
def login():
    login_data = request.json
    username = login_data.get("username")
    password = login_data.get("password")

    user = users.get(username)
    if user and user["password"] == password:
        access_token = create_access_token(identity={"username": username, "role": user["role"]})
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid credentials"}), 401

def role_required(required_role):
    """Декоратор для перевірки ролі користувача"""
    def wrapper(fn):
        @functools.wraps(fn)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            user = get_jwt_identity()
            if user["role"] != required_role:
                return jsonify({"msg": "Access denied"}), 403
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper

@app.route("/")
def home():
    return "API is running!", 200

@app.route("/admin", methods=["GET"])
@role_required("Admin")
def admin_panel():
    return jsonify({"msg": "Welcome, Admin!"}), 200

@app.route("/items", methods=["GET"])
@jwt_required()
def get_items():
    return jsonify(data), 200

@app.route("/items", methods=["POST"])
@role_required("Admin")
def create_item():
    new_item = request.json
    data.append(new_item)
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["GET"])
@jwt_required()
def get_item(item_id):
    if 0 <= item_id < len(data):
        return jsonify(data[item_id]), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/items/<int:item_id>", methods=["PATCH"])
@role_required("Admin")
def update_item(item_id):
    if 0 <= item_id < len(data):
        data[item_id].update(request.json)
        return jsonify(data[item_id]), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/items/<int:item_id>", methods=["DELETE"])
@role_required("Admin")
def delete_item(item_id):
    if 0 <= item_id < len(data):
        deleted = data.pop(item_id)
        return jsonify(deleted), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)