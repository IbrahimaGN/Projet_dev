from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from config import *

import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash, check_password_hash



# Route pour register
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    email = data['email']
    role = data['role']
    group_id = data['group_id']

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Could not connect to the database'}), 500
    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO "User" (username, password, email, role, group_id) VALUES (%s, %s, %s, %s, %s)''', (username, hashed_password, email, role, group_id))
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'An error occurred while registering'}), 500

    return jsonify({'message': 'Registered successfully'}), 200

@app.route('/register1', methods=['POST'])
def register_group():
    data = request.get_json()
    group_name = data.get('group_name')

    if not group_name:
        return jsonify({"msg": "Le nom du groupe est requis"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter à la base de données'}), 500

    try:
        cur = conn.cursor()
        cur.execute('INSERT INTO "Group" (group_name) VALUES (%s)', (group_name,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"msg": "Groupe creer avec succes"}), 201

    except psycopg2.Error as e:
        print(f"Une erreur s'est produite: {e}")
        return jsonify({"msg": "Erreur lors de la création du groupe", "error": str(e)}), 500


#login 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Veuillez fournir un nom d\'utilisateur et un mot de passe'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter à la base de données'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('''SELECT password FROM "User" WHERE username = %s''', (username,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[0], password):
            # Ici, vous pouvez inclure plus d'informations dans le token JWT si nécessaire
            access_token = create_access_token(identity={'username': username, 'role': 'admin'})
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'message': 'Identifiants invalides'}), 401

    except psycopg2.Error as e:
        print(f"Une erreur s'est produite: {e}")
        return jsonify({'message': 'Une erreur s\'est produite lors de la connexion'}), 500

def admin_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"msg": "Accès interdit"}), 403
        return fn(*args, **kwargs)
    return wrapper



@app.route('/admin', methods=['GET'])
@admin_required
def admin():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Bienvenue, {current_user['username']}"}), 200



@app.route('/user', methods=['GET'])
@jwt_required()
def user():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Bienvenue, {current_user['username']}"}), 200


# Exemple d'une route pour ajouter un prompt
@app.route('/prompts', methods=['POST'])
@jwt_required()
def create_prompt():
    current_user = get_jwt_identity()
    content = request.json.get('content')

    if not content:
        return jsonify({"msg": "Le contenu est requis"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = sql.SQL(
            'INSERT INTO prompt (content, price, state, user_id) '
            'VALUES (%s, %s, %s, (SELECT user_id FROM "User" WHERE username = %s))'
        )
        cursor.execute(query, (content, 1000, 'pending', current_user['username']))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        return jsonify({"msg": "Erreur lors de la création du prompt", "error": str(e)}), 500

    return jsonify({"msg": "Prompt créé avec succès"}), 201


