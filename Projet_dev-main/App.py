from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from config import *
from admin import admin_bp
from user import user_bp
from auth import auth_bp
from connect import connect_bp
from prompt import prompt_bp

app = Flask(__name__)
app.config.from_object(Config)



@app.route('/consulter/<int:id>', methods=['GET'])
def get_prompt(id):
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter a la base de donnees'}), 500

    try:
        cur = conn.cursor()
        cur.execute('''SELECT id, content, price FROM "prompt" WHERE id = %s''', (id,))
        prompt = cur.fetchone()
        cur.close()
        conn.close()

        if not prompt:
            return jsonify({"msg": "Prompt non trouvé"}), 404

        prompt_data = {
            "id": prompt[0],
            "content": prompt[1],
            "price": prompt[2]
        }
        return jsonify(prompt_data), 200

    except psycopg2.Error as e:
        print(f"Une erreur s_est produite: {e}")
        return jsonify({"msg": "Erreur lors de la recuperation du prompt", "error": str(e)}), 500


@app.route('/buy/<int:id>', methods=['POST'])
def buy_prompt(id):
    # Vérifiez les détails d'achat du prompt ici, comme la gestion de la transaction
    # Cette fonction pourrait nécessiter des détails supplémentaires comme l'adresse de livraison, etc.
    return jsonify({"msg": f"Achat du prompt avec l'ID {id} effectuer avec succes"}), 200



@app.route('/prompts', methods=['GET'])
def get_prompts():
    conn = get_db_connection()
    if conn is None:
        return jsonify({'message': 'Impossible de se connecter à la base de données'}), 500

    try:
        cur = conn.cursor()
        cur.execute('''SELECT id, content, price FROM "prompt"''')
        prompts = cur.fetchall()
        cur.close()
        conn.close()

        prompt_list = []
        for prompt in prompts:
            prompt_list.append({
                "id": prompt[0],
                "content": prompt[1],
                "price": prompt[2]
            })
        return jsonify(prompt_list), 200

    except psycopg2.Error as e:
        print(f"Une erreur s'est produite: {e}")
        return jsonify({"msg": "Erreur lors de la récupération des prompts", "error": str(e)}), 500

# @app.route('/search', methods=['GET'])
# def search_prompts():
#     keyword = request.args.get('keyword')

#     conn = get_db_connection()
#     if conn is None:
#         return jsonify({'message': 'Impossible de se connecter à la base de données'}), 500

#     try:
#         cur = conn.cursor()
#         # Recherche de prompts par contenu ou mots-clés
#         cur.execute('''SELECT id, content, price FROM "prompt" WHERE content ILIKE %s''', ('%' + keyword + '%',))
#         prompts = cur.fetchall()
#         cur.close()
#         conn.close()

#         if not prompts:
#             return jsonify({"msg": "Aucun prompt trouver pour ce mot_cle"}), 404

#         prompt_list = [{
#             "id": prompt[0],
#             "content": prompt[1],
#             "price": prompt[2]
#         } for prompt in prompts]

#         return jsonify(prompt_list), 200

#     except psycopg2.Error as e:
#         print(f"Une erreur s'est produite: {e}")
#         return jsonify({"msg": "Erreur lors de la recherche de prompts", "error": str(e)}), 500




jwt = JWTManager(app)

# Enregistrer les Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(connect_bp, url_prefix='/connect')
app.register_blueprint(prompt_bp, url_prefix='/prompt')


if __name__ == '__main__':
    app.run(debug=True)
