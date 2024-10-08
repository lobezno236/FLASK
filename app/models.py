from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from utils import bcrypt, db
from werkzeug.security import generate_password_hash, check_password_hash

print("db in models.py:", db)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contraseña = db.Column(db.String(128), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, nombre, correo, contraseña):
        self.nombre = nombre
        self.correo = correo
        self.contraseña = generate_password_hash(contraseña)

    def verificar_contraseña(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)

    def __repr__(self):
        return f'Usuario({self.nombre}, {self.correo})'
    
