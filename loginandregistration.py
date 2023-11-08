from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from datetime import datetime, timedelta
import sqlite3
import bcrypt

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your_secret_key"  
jwt = JWTManager(app)

def init_db():
    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user1 (firstname TEXT, lastname TEXT, gmail TEXT, password TEXT)")
    connection.commit()
    connection.close()
init_db()
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')

    if not firstname or not lastname or not email or not password or not confirm_password:
        return jsonify({"error": "All fields are required"}), 400

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user1 WHERE gmail=?", (email,))
    user = cursor.fetchone()

    if user:
        connection.close()
        return jsonify({"error": "Email already registered"}), 400

    cursor.execute("INSERT INTO user1 (firstname, lastname, gmail, password) VALUES (?, ?, ?, ?)", (firstname, lastname, email, password_hash))
    connection.commit()
    connection.close()

    return jsonify({"message": "Registration successful"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Both email and password are required"}), 400

    connection = sqlite3.connect("user_data.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM user1 WHERE gmail=?", (email,))
    user = cursor.fetchone()

    connection.close()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    stored_password_hash = user[3]

    if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
        token_payload = {
            'email': email,
            'exp': datetime.utcnow() + timedelta(days=1)  # Token expiration time
        }
        token = create_access_token(identity=token_payload)

        return jsonify({"message": "Login successful", "token": token})
    else:
        return jsonify({"error": "Invalid password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
