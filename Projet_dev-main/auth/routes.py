from flask import jsonify, request
from flask_jwt_extended import create_access_token
from auth import auth_bp
from config import *
import psycopg2
from werkzeug.security import check_password_hash




#login 
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Veuillez fournir un nom d\'utilisateur et un mot de passe'}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter à la base de donnees'}), 500
    
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
        print(f"Une erreur s_est produite: {e}")
        return jsonify({'message': 'Une erreur s\'est produite lors de la connexion'}), 500