from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def user_required(fn):
    @jwt_required()
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] != 'user':
            return jsonify({"msg": "Accès interdit"}), 403
        return fn(*args, **kwargs)
    return wrapper




#creation d'un blueprint
user= Blueprint("user", __name__)


@user.route('/user', methods=['GET'])
@jwt_required()
def user():
    current_user = get_jwt_identity()
    return jsonify({"msg": f"Bienvenue, {current_user['username']}"}), 200