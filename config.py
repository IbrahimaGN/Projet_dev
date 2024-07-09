from flask import Flask
from flask_jwt_extended import JWTManager
import psycopg2



app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = b'\xd3\x9e0\x8a\xb6j_v\xc8\x91\xc2A\x11w)\xd0@\x0e\x12\n\xac\t\xfb)'  
jwt = JWTManager(app)

# Connect to the database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="api_rest",
            user="api_rest",
            password="ibou1999"
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"An error occurred: {e}")
        return None