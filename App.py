from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration de la base de données PostgreSQL
app.config['DATABASE'] = {
    'dbname': 'api_rest',
    'user': 'api_rest',
    'password': 'ibou1999',
    'host': 'localhost',
    'port': 5432
}

# Configuration de JWT
app.config['JWT_SECRET_KEY'] = 'votre_clé_secrète' # Changez ceci par une clé secrète sécurisée
jwt = JWTManager(app)


def get_db_connection():
    conn = psycopg2.connect(**app.config['DATABASE'])
    return conn


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    role = request.json.get('role', 'user')  # Par défaut, le rôle est 'user'

    hashed_password = generate_password_hash(password)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Nom d'utilisateur déjà pris"}), 400

    cursor.execute(
        'INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)',
        (username, hashed_password, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"msg": "Utilisateur créé avec succès"}), 201



@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash, role FROM users WHERE username = %s', (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user is None or not check_password_hash(user[1], password):
        return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401

    access_token = create_access_token(identity={"username": username, "role": user[2]})
    return jsonify(access_token=access_token)



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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO prompts (content, status, user_id) VALUES (%s, %s, (SELECT id FROM users WHERE username = %s))',
        (content, 'pending', current_user['username'])
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"msg": "Prompt créé avec succès"}), 201

if __name__ == '__main__':
    app.run()
