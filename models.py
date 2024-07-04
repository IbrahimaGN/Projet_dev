from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Connect to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="api_rest",
            user="api_rest",
            password="ibou1999"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"An error occurred: {e}")
        return None

# Route pour register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    role = data['role']
    #group_id = data['group_id']

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Could not connect to the database'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO "User" (username, password, email, role) VALUES (%s, %s, %s, %s)''', (username, hashed_password, email, role))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An error occurred while registering'}), 500

    return jsonify({'message': 'Registered successfully'}), 200

# Route pour login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Could not connect to the database'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('''SELECT password FROM "User" WHERE username = %s''', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An error occurred while logging in'}), 500

    if user and check_password_hash(user[0], password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Lancer l'app
if __name__ == '__main__':
    app.run(debug=True)


