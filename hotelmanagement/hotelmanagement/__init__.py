from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "31231287@jashdlaksnaisdn&223"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12052001Li@localhost/hotelmanagerment?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
cloudinary.config(
    cloud_name='vantai125',
    api_key='275713422948189',
    api_secret='40uKksVvrmRfoqJwYpBNnhM_S90'
)
login = LoginManager(app=app)
