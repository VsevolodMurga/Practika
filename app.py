from flask import Flask, request, jsonify

app = Flask(__name__)

data = []

@app.route("/")
def home():
    return "API is running!", 200

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(data), 200

@app.route("/items", methods=["POST"])
def create_item():
    new_item = request.json
    data.append(new_item)
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    if 0 <= item_id < len(data):
        return jsonify(data[item_id]), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    if 0 <= item_id < len(data):
        data[item_id].update(request.json)
        return jsonify(data[item_id]), 200
    return jsonify({"error": "Item not found"}), 404

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    if 0 <= item_id < len(data):
        deleted = data.pop(item_id)
        return jsonify(deleted), 200
    return jsonify({"error": "Item not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)