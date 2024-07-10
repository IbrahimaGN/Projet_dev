from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from user import user_bp
from config import get_db_connection
import psycopg2

@user_bp.route('/propose_prompt', methods=['POST'])
@jwt_required()
def propose_prompt():
    data = request.get_json()
    prompt_text = data.get('content')
    price = data.get('price')
    #current_user = get_jwt_identity()
    #user_id = current_user['id']

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Could not connect to the database'}), 500

    try:
        cur = conn.cursor()
        cur.execute('''INSERT INTO prompt (content, price, state) VALUES (%s, %s, %s)''', (prompt_text, price, 'pending'))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Prompt proposer avec succes'}), 201
    except psycopg2.Error as e:
        print(f"An error occurred: {e}")
        return jsonify({'message': 'Erreur lors de la proposition du prompt'}), 500