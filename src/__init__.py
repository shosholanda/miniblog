from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Información para conectar a una Base de datos
# Deben coincidir las credenciales
DATABASE_USER = "root"
DATABASE_PASSWORD = "1234"
IP_ADDRESS = "127.0.0.1"
PORT = 3306
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{IP_ADDRESS}:{PORT}/posts"

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SECRET_KEY'] = '$up3r_$3cr31_43y'
app.config['UPLOAD_FOLDER'] = './src/static/img/post/'


db = SQLAlchemy(app)


from src.controller.auth import auth
from src.controller.home import home
from src.controller.profile import profile

app.register_blueprint(auth)
app.register_blueprint(home)
app.register_blueprint(profile)

with app.app_context():
    db.create_all()

