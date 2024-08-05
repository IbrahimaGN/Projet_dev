from flask import jsonify, request
from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from user import user_bp
from config import get_db_connection
import psycopg2

# Fonction de décoration pour vérifier le rôle user
def user_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] == 'admin':
            return jsonify({"msg": "Acces interdit"}), 403
        return fn(*args, **kwargs)
    return wrapper

@user_bp.route('/propose_prompt', methods=['POST'])
@user_required
def propose_prompt():
    data = request.get_json()
    prompt_text = data.get('content')
    price = data.get('price')
    current_user = get_jwt_identity()
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
    

@user_bp.route('/vote_prompt/<int:id>', methods=['POST'])
@user_required
def vote_prompt(id):
    current_user = get_jwt_identity()

    # # Vérifier si l'utilisateur est administrateur
    # if current_user.get('role') == 'admin':
    #     return jsonify({"msg": "Vous n_etes pas autoriser a noter des prompts en tant qu'administrateur."}), 403
    vote = request.get_json().get('vote_value')
    #username = request.get_json().get('username')


    if vote in [1, -1]:
        return jsonify({"msg": "Vote invalide. Utilisez 1 pour un vote positif et -1 pour un vote negatif."}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter a la base de donnees'}), 500

    try:
        cur = conn.cursor()
        # Sélectionnez user_id depuis la table prompt
        cur.execute('''SELECT user_id FROM "prompt" WHERE id = %s''', (id,))
        result = cur.fetchone()
        if not result:
            return jsonify({"msg": "Prompt non trouve"}), 404
        prompt_user_id = result[0]

        if prompt_user_id == current_user['username']:
            return jsonify({"msg": "Vous ne pouvez pas voter pour votre propre prompt"}), 403

        # Sélectionnez group_id depuis la table User pour l'utilisateur du prompt
        cur.execute('''SELECT  group_id FROM "User" WHERE user_id = %s''', (prompt_user_id,))
        prompt_group_id = cur.fetchone()[0]

        # Sélectionnez group_id depuis la table User pour l'utilisateur actuel
        cur.execute('''SELECT group_id FROM "User" WHERE username = %s''', (current_user['username'],))
        user_group_id = cur.fetchone()[0]

        impact = 1
        if user_group_id == prompt_group_id:
            impact = 2  # Impact plus fort pour les membres du même groupe

        cur.execute('''INSERT INTO "Vote" (prompt_id, vote_value, impact, username) VALUES (%s, %s, %s, %s)''', (id, vote, impact, current_user['username']))


        # Calculer le score total du prompt
        cur.execute('''SELECT SUM(vote_value) FROM "Vote" WHERE prompt_id = %s''', (id,))
        total_score = cur.fetchone()[0]

        # Si aucun vote n'a été trouvé, définir total_score à 0
        if total_score is None:
            total_score = 0
            
        # Activer le prompt si le score total atteint 6 ou plus
        if total_score >= 6:
            cur.execute('''UPDATE "prompt" SET state = 'activer' WHERE id = %s''', (id,))
            conn.commit()

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"msg": "Vote enregistre avec succes"}), 200

    except psycopg2.Error as e:
        print(f"Une erreur s_est produite: {e}")
        return jsonify({"msg": "Erreur lors de l_enregistrement du vote", "error": str(e)}), 500




@user_bp.route('/rate_prompt/<int:id>', methods=['POST'])
@user_required
def rate_prompt(id):
    current_user = get_jwt_identity()

    # Vérifier si l'utilisateur est administrateur
    if current_user.get('role') == 'admin':
        return jsonify({"msg": "Vous n_etes pas autorise à noter des prompts en tant qu'administrateur."}), 403


    rating_value = request.get_json().get('rating_value')

    if rating_value < -10 or rating_value > 10:
        return jsonify({"msg": "La note doit etre comprise entre -10 et +10."}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter a la base de donnees'}), 500

    try:
        cur = conn.cursor()

        # Récupérer le prix actuel du prompt
        cur.execute('''SELECT price FROM "prompt" WHERE id = %s''', (id,))
        current_price = cur.fetchone()[0]

        # Récupérer le groupe du prompt
        cur.execute('''SELECT group_id FROM "User" WHERE user_id = (SELECT user_id FROM "prompt" WHERE id = %s)''', (id,))
        prompt_group_id = cur.fetchone()[0]

        # Récupérer le groupe de l'utilisateur courant
        cur.execute('''SELECT group_id FROM "User" WHERE username = %s''', (current_user["username"],))
        user_group_id = cur.fetchone()[0]

        # Calculer l'impact de la note en fonction du groupe
        if user_group_id == prompt_group_id:
            impact = 0.6  # Membre du même groupe
        else:
            impact = 0.4  # Membre extérieur au groupe

        # Insérer la note dans la table des notations
        cur.execute('''INSERT INTO "Rating" (prompt_id, rating_value, username, impact) VALUES (%s, %s, %s, %s)''', (id, rating_value, current_user['username'], impact))
        conn.commit()

        # Calculer la moyenne des notes pour le prompt
        cur.execute('''SELECT AVG(rating_value) FROM "Rating" WHERE prompt_id = %s''', (id,))
        average_rating = cur.fetchone()[0]

        # Mettre à jour le prix du prompt
        new_price = 1000 * (1 + average_rating)
        cur.execute('''UPDATE "prompt" SET price = %s WHERE id = %s''', (new_price, id))
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"msg": "Prompt noter avec succes", "new_price": new_price}), 200

    except psycopg2.Error as e:
        print(f"Une erreur s_est produite: {e}")
        return jsonify({"msg": "Erreur lors de la notation du prompt", "error": str(e)}), 500





@user_bp.route('/delete_prompt/<int:id>', methods=['DELETE'])
@user_required
def delete_prompt(id):
    current_user = get_jwt_identity()

    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter a la base de donnees'}), 500

    try:
        cur = conn.cursor()

        # Vérifier si le prompt existe et appartient à l'utilisateur
        cur.execute('''SELECT user_id, state FROM "prompt" WHERE id = %s''', (id,))
        result = cur.fetchone()
        if not result:
            return jsonify({"msg": "Prompt non trouvé"}), 404

        prompt_user_id, prompt_state = result

        # Vérifier si l'utilisateur courant est autorisé à supprimer ce prompt
        cur.execute('''SELECT user_id, username FROM "User" WHERE username = %s''', (current_user["username"],))
        username_result = cur.fetchone()
        if not username_result:
            return jsonify({"msg": "Utilisateur non trouve"}), 404
        
        username = username_result[0]  # Récupérer le nom d'utilisateur depuis le tuple

        if prompt_user_id != username:
            return jsonify({"msg": "Vous n_etes pas autorise a supprimer ce prompt"}), 403

        # Mettre à jour l'état du prompt à "À supprimer"
        if prompt_state != 'À supprimer':
            cur.execute('''UPDATE "prompt" SET state = 'À supprimer' WHERE id = %s''', (id,))
            conn.commit()

        cur.close()
        conn.close()

        return jsonify({"msg": "Demande de suppression du prompt enregistree avec succes"}), 200

    except psycopg2.Error as e:
        print(f"Une erreur s_est produite: {e}")
        return jsonify({"msg": "Erreur lors de la demande de suppression du prompt", "error": str(e)}), 500
