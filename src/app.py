from flask import Flask, jsonify, render_template, redirect, request, url_for
from pymongo import MongoClient
import json
import os 
from dotenv import load_dotenv

load_dotenv()


MONGO_URL = "mongodb+srv://yash0001:pass%40123@cluster0.dibg0ip.mongodb.net/?appName=Clus"
client = MongoClient(MONGO_URL)
db = client['my_database']
collection = db['submission']

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def get_data():
    file_path = 'data.json'
    
    if not os.path.exists(file_path):
        return jsonify([]) 

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def index():
    error = request.args.get('error')
    
    return render_template('index.html', error=error)

@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('user_data')
    file_path = 'data.json'
    
    if not user_input:
        return redirect(url_for('index', error="Input cannot be empty"))
    
    try:
        # 1. Save to MongoDB Atlas
        collection.insert_one({"content": user_input})

        # 2. Save to data.json
        current_data = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    current_data = json.load(f)
                except:
                    current_data = []

        current_data.append(user_input)
        
        with open(file_path, 'w') as f:
            json.dump(current_data, f, indent=4)

        return redirect(url_for('success'))

    except Exception as e:
        return redirect(url_for('index', error=str(e)))

@app.route('/success')
def success():
    return "<h1>Data submitted successfully</h1><p><a href='/'>Go Back</a></p>"

if __name__ == '__main__':
    
    app.run(port=5000, debug=True)