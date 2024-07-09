from flask import Blueprint
from models import admin_required
from flask import jsonify, request
import psycopg2
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import generate_password_hash
from config import *


#creation d'un blueprint
admin_db= Blueprint("admin", __name__)

@admin_db.route('/admin', methods=['GET'])
@admin_required
def admin():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Bienvenue, {current_user['username']}"}), 200



# Route pour register
@admin.route('/register', methods=['POST'])
@admin_required
def register():
    current_user = get_jwt_identity()
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

    return jsonify({'message': 'Registered successfully with',"user" : current_user[username]}), 200