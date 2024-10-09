from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, UserMixin

print("Iniciando Modelos...")
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    contraseña_hash = db.Column(db.String(128), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, username, nombre, correo, contraseña):
        self.username = username
        self.nombre = nombre
        self.correo = correo
        self.contraseña_hash = generate_password_hash(contraseña)

    def __repr__(self):
        return f'Usuario({self.username}, {self.nombre}, {self.correo})'

class Correo(db.Model):

    # Nombre de la tabla en la base de datos
    __tablename__ = 'correo'
    
    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    # Representación del objeto como cadena
    def __repr__(self):
        return f'Correo({self.nombre}, {self.correo}, {self.mensaje})'
    
class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    imagen = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'Producto({self.nombre}, {self.descripcion}, {self.precio}, {self.categoria}, {self.imagen})'