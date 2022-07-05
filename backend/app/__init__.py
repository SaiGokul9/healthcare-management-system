from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS

from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {"origins": "*"}})
db = SQLAlchemy(app)
engine = db.engine
migrate = Migrate(app,db)
login = LoginManager(app)
conn = engine.connect()

from app import routes, models