from database import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


print("Iniciando Modelos...")


class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    documento_identidad = db.Column(db.String(20), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False, default='cliente')
    fecha_registro = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __init__(self, username, nombre, apellido, correo, telefono, documento_identidad, genero, fecha_nacimiento, password):
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.telefono = telefono
        self.documento_identidad = documento_identidad
        self.genero = genero
        self.fecha_nacimiento = fecha_nacimiento
        self.set_password(password)

    def set_password(self, contraseña):
        self.password = bcrypt.generate_password_hash(contraseña).decode('utf-8')

    def check_password(self, contraseña):
        return bcrypt.check_password_hash(self.password, contraseña)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'telefono': self.telefono,
            'documento_identidad': self.documento_identidad,
            'genero': self.genero,
            'fecha_nacimiento': self.fecha_nacimiento,
            'rol': self.rol,
            'fecha_registro': self.fecha_registro
        }

    def __repr__(self):
        return f'Usuario({self.username}, {self.nombre}, {self.correo})'

class Administrador(Usuario):
    def __init__(self, username, nombre, correo, contraseña):
        super().__init__(username, nombre, correo, contraseña)
        self.rol = 'administrador'

    def get_id(self):
        return self.id

    def crear_usuario(self, username, nombre, correo, contraseña, rol='cliente'):
        nuevo_usuario = Usuario(username, nombre, correo, contraseña)
        nuevo_usuario.rol = rol
        db.session.add(nuevo_usuario)
        db.session.commit()
        return nuevo_usuario

    def editar_usuario(self, user_id, username, nombre, correo, rol=None):
        user = Usuario.query.get(user_id)
        if user:
            user.username = username
            user.nombre = nombre
            user.correo = correo

            if rol:
                user.rol = rol
            db.session.commit()
            return user
        return None

    def eliminar_usuario(self, user_id):
        user = Usuario.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    def crear_producto(self, nombre, descripcion, precio, categoria, imagen):
        nuevo_producto = Producto(nombre, descripcion, precio, categoria, imagen)
        db.session.add(nuevo_producto)
        db.session.commit()
        return nuevo_producto

    def editar_producto(self, product_id, nombre, descripcion, precio, categoria, imagen):
        product = Producto.query.get(product_id)
        if product:
            product.nombre = nombre
            product.descripcion = descripcion
            product.precio = precio
            product.categoria = categoria
            product.imagen = imagen
            db.session.commit()
            return product
        return None

    def eliminar_producto(self, product_id):
        product = Producto.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False

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


class Direcciones(db.Model):
    __tablename__ = 'direcciones'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    user = db.relationship('Usuario', backref=db.backref('direcciones', lazy=True))
    calle = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(20), nullable=False)
    ciudad = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    pais = db.Column(db.String(50), nullable=False)
    codigo_postal = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'Direcciones({self.calle}, {self.numero}, {self.ciudad}, {self.estado}, {self.pais}, {self.codigo_postal})'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'calle': self.calle,
            'numero': self.numero,
            'ciudad': self.ciudad,
            'estado': self.estado,
            'pais': self.pais,
            'codigo_postal': self.codigo_postal
        }