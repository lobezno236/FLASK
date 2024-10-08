from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()

db = SQLAlchemy()

def init_db(app):
    global db
    print("Initializing db...")
    db = SQLAlchemy(app)
    print("db initialized:", db)
    print("db is None:", db is None)