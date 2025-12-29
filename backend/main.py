from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # allow requests from Express

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask Backend"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
