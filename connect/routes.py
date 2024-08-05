from flask import  jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from connect import connect_bp


@connect_bp.route('/connect', methods=['GET'])
@jwt_required()
def connect():
    current_user = get_jwt_identity()
    if current_user['role'] == 'admin':
        return jsonify({"msg": f"Bienvenue, {current_user['username']} (Admin)"}), 200
    else:
        return jsonify({"msg": f"Bienvenue, {current_user['username']} (User)"}), 200