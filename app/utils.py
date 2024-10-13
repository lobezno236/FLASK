from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import requests

bcrypt = Bcrypt()

db = SQLAlchemy()

def init_db(app):
    global db
    print("Initializing db...")
    db = SQLAlchemy(app)
    print("db initialized:", db)
    print("db is None:", db is None)
    
def contacto(mail, correo, mensaje):
    msg = Message('Mensaje de contacto', sender=correo, recipients=['lobezno236@gmail.com'])
    msg.body = mensaje
    try:
        mail.send(msg)
        print('Mensaje enviado con éxito')
    except Exception as e:
        print(e)
        