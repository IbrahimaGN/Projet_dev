from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from admin import admin_bp
from config import get_db_connection
from functools import wraps
import psycopg2
from werkzeug.security import generate_password_hash

# Fonction de décoration pour vérifier le rôle admin
def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({"msg": "Accès interdit"}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/create_user', methods=['POST'])
@admin_required
def create_user():
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



@admin_bp.route('/create_group', methods=['POST'])
@admin_required
def create_group():
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


@admin_bp.route('/validate_prompt/<int:id>', methods=['POST'])
@admin_required
def validate_prompt(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE prompt SET state = %s WHERE id = %s', ('active', id))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"msg": "Prompt validé"}), 200

@admin_bp.route('/delete_prompt/<int:id>', methods=['DELETE'])
@admin_required
def delete_prompt(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM prompts WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"msg": "Prompt supprimé"}), 200



@admin_bp.route('/view_all_prompts', methods=['GET'])
@admin_required
def view_all_prompts():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter à la base de données'}), 500

    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM prompt')
        prompts = cur.fetchall()
        cur.close()
        conn.close()

        return jsonify(prompts), 200

    except psycopg2.Error as e:
        print(f"Une erreur s'est produite: {e}")
        return jsonify({"msg": "Erreur lors de la récupération des prompts", "error": str(e)}), 500