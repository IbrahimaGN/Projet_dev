from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from prompt import prompt_bp
from config import *
from psycopg2 import sql
from functools import wraps



# Fonction de décoration pour vérifier le rôle admin
def user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            return jsonify({"msg": "Acces interdit"}), 403
        return fn(*args, **kwargs)
    return wrapper


# Exemple d'une route pour ajouter un prompt
@prompt_bp.route('/create_prompt', methods=['POST'])
@user_required
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
        return jsonify({"msg": "Erreur lors de la creation du prompt", "error": str(e)}), 500

    return jsonify({"msg": "Prompt creer avec succes"}), 201
