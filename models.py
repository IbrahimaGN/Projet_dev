
# # Exemple d'une route pour ajouter un prompt
# @app.route('/prompts', methods=['POST'])
# @jwt_required()
# def create_prompt():
#     current_user = get_jwt_identity()
#     content = request.json.get('content')

#     if not content:
#         return jsonify({"msg": "Le contenu est requis"}), 400

#     try:
#         conn = get_db_connection()
#         cursor = conn.cursor()
#         query = sql.SQL(
#             'INSERT INTO prompt (content, price, state, user_id) '
#             'VALUES (%s, %s, %s, (SELECT user_id FROM "User" WHERE username = %s))'
#         )
#         cursor.execute(query, (content, 1000, 'pending', current_user['username']))
#         conn.commit()
#         cursor.close()
#         conn.close()
#     except Exception as e:
#         return jsonify({"msg": "Erreur lors de la création du prompt", "error": str(e)}), 500

#     return jsonify({"msg": "Prompt créé avec succès"}), 201


