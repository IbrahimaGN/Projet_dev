#from models import *



from flask import Flask
from flask_jwt_extended import JWTManager
from config import *
from admin import admin_bp
from auth import auth_bp
from connect import connect_bp
#from prompts import prompts_bp

app = Flask(__name__)
app.config.from_object(Config)


jwt = JWTManager(app)

# Enregistrer les Blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(connect_bp, url_prefix='/connect')
#app.register_blueprint(prompts_bp, url_prefix='/prompts')


if __name__ == '__main__':
    app.run(debug=True)
