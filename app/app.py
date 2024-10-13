from flask import Flask, render_template, redirect, url_for, request, flash, abort, jsonify, session, g
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from mail_config import MAIL_CONFIG
from forms import LoginForm, RegistroForm
from utils import bcrypt, db
from models import Usuario, Correo, Producto, Administrador
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, verify_jwt_in_request
from datetime import timedelta
import requests
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError, decode
from jwt.exceptions import PyJWTError
import os
import secrets
import re
from database import db
from views import contacto_view
from config import config
from app_factory import create_app

app = create_app()
app.config.from_object(config['development'])

app.config['APPLICATION_ROOT'] = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://lobezno236:Alamo2025@localhost/TIENDA 2025'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secrets.token_urlsafe(16)'
app.config['JWT_SECRET_KEY'] = 'secrets.token_urlsafe(16)'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_IDENTITY_CLAIM'] = 'identity'

csrf = CSRFProtect(app)
jwt = JWTManager(app)
app.config.update(MAIL_CONFIG)
mail = Mail(app)
db.init_app(app)
with app.app_context():
    db.create_all()

def get_usuario_actual():
    if 'access_token' in session:
        try:
            current_user_id = get_jwt_identity()
            user = Usuario.query.get(current_user_id)
            return user
        except PyJWTError:
            return None
    else:
        return None
    
@app.before_request
def before_request():
    if 'access_token' in session:
        headers = {'Authorization': 'Bearer ' + session['access_token']}
        request.headers = headers
        
@app.context_processor
def inject_user():
    if 'access_token' in session:
        try:
            verify_jwt_in_request()
            user = db.session.get(Usuario, get_jwt_identity())
            return dict(user=user)
        except PyJWTError:
            return dict(user=None)
    else:
        return dict(user=None)

@app.route('/')
def index():
    data = {'titulo': 'Index', 'encabezado': 'Bienvenido(a)'}
    current_user = None
    try:
        current_user = get_usuario_actual()
    except RuntimeError:
        pass
    return render_template('index.html', data=data, current_user=current_user)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    data = {'titulo': 'Registro'}
    form = RegistroForm()
    if form.validate_on_submit():
        username = form.username.data
        nombre = form.nombre.data
        apellido = form.apellido.data
        correo = form.correo.data
        telefono = form.telefono.data
        documento_identidad = form.documento_identidad.data
        genero = form.genero.data
        fecha_nacimiento = form.fecha_nacimiento.data
        password = form.password.data

        user = Usuario(username=username, nombre=nombre, apellido=apellido, correo=correo, telefono=telefono, documento_identidad=documento_identidad, genero=genero, fecha_nacimiento=fecha_nacimiento, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso', 'success')
        return redirect(url_for('login_cliente'))
    return render_template('registro.html', data=data, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_cliente():
    form = LoginForm()
    if form.validate_on_submit():
        username_or_correo = form.username_or_correo.data
        password = form.password.data
        user = Usuario.query.filter_by(username=username_or_correo).first()
        if user is None:
            user = Usuario.query.filter_by(correo=username_or_correo).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            session['access_token'] = access_token
            return redirect(url_for('cliente_dashboard'))
        else:
            flash('Credenciales incorrectas', 'error')
            return render_template('login.html', form=form)
    else:
        if form.errors:
            flash('Error al validar el formulario', 'error')
        data = {'titulo': 'Login', 'encabezado': 'Iniciar sesión'}
        return render_template('login.html', form=form, data=data)
    
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def cliente_dashboard():
    try:
        # Obtener el ID del usuario actual
        current_user_id = get_jwt_identity()
        print(f"Current user ID: {current_user_id}")  # Add a print statement to check the user ID

        # Verificar si el usuario existe
        user = db.session.get(Usuario, current_user_id)
        if not user:
            return jsonify({'error': 'usuario no encontrado'}), 404

        # Definir la data para la plantilla
        data = {
            'titulo': 'Dashboard del cliente',
            'encabezado': 'Bienvenido(a) al dashboard'
        }

        # Devolver una página HTML protegida
        return render_template('cliente_dashboard.html', user=user, data=data)
    except Exception as e:
        # Manejar cualquier excepción que ocurra
        print(f"Error: {e}")  # Add a print statement to check the error message
        return jsonify({'error': 'Error al obtener el ID del usuario'}), 500

@app.route('/ordenes', methods=['GET'])
@jwt_required()
def ordenes():
    data = {
        'titulo': 'Dashboard del cliente',
        'encabezado': 'Bienvenido(a) al dashboard'
    }
    return render_template('ordenes.html', data=data)

@app.route('/autentificacion', methods=['GET'])
@jwt_required()
def autentificacion():
    data = {
        'titulo': 'Dashboard del cliente',
        'encabezado': 'Bienvenido(a) al dashboard'
    }
    return render_template('autentificacion.html', data=data)

@app.route('/tarjeta_credito', methods=['GET'])
@jwt_required()
def tarjeta_credito():
    data = {
        'titulo': 'Dashboard del cliente',
        'encabezado': 'Bienvenido(a) al dashboard'
    }
    return render_template('tarjeta_credito.html', data=data)

@app.route('/agregar_tarjeta_credito', methods=['GET'])
@jwt_required()
def agregar_tarjeta_credito():
    data = {
        'titulo': 'Dashboard del cliente',
        'encabezado': 'Bienvenido(a) al dashboard'
    }
    return render_template('agregar_tarjeta_credito.html', data=data)

@app.route('/direcciones', methods=['GET'])
@jwt_required()
def direcciones():
    data = {
        'titulo': 'Dashboard del cliente',
        'encabezado': 'Bienvenido(a) al dashboard'
    }
    return render_template('direcciones.html', data=data)

@app.route('/agregar_direccion', methods=['GET'])
@jwt_required()
def agregar_direccion():
    data = {
        'titulo': 'Dashboard del cliente',
        'encabezado': 'Bienvenido(a) al dashboard'
    }
    return render_template('agregar_direccion.html', data=data)

@app.route('/logout')
@jwt_required()
def logout():
    # Aquí puedes eliminar el token de la sesión si es necesario
    session.pop('access_token', None)  # Esto eliminará el token de acceso de la sesión
    # Redirigir a la página de inicio o a otra página que desees
    return redirect(url_for('index'))  # Cambia 'index' por el nombre de la función de la ruta a la que deseas redirigir

@app.route('/contacto')
def contacto():
    data = {'titulo': 'Contacto', 'encabezado': 'Bienvenido(a)'}
    return render_template('contacto.html', data=data)

@app.route("/correos")
@jwt_required()
def correos():
    data = {
        'titulo': 'Correos',
        'encabezado': 'Bienvenido(a)'
    }
    # Obtener todos los correos de la base de datos
    correos = Correo.query.all()
    if correos is None or len(correos) == 0:
        return jsonify({'message': 'No hay correos en la base de datos'}), 200
    return render_template('correos.html', correos=correos, data=data)

@app.route("/eliminar_correo/<int:id>")
@jwt_required()
def eliminar_correo(id):
    correo = Correo.query.get_or_404(id)
    db.session.delete(correo)
    db.session.commit()
    return jsonify({'message': 'Correo eliminado correctamente'}), 200

@app.route("/editar_correo/<int:id>", methods=["GET", "POST"])
@jwt_required()
def editar_correo(id):
    correo = Correo.query.get_or_404(id)
    if request.method == "POST":
        correo.nombre = request.form["nombre"]
        correo.correo = request.form["correo"]
        correo.mensaje = request.form["mensaje"]
        db.session.commit()
        return jsonify({'message': 'Correo editado correctamente'}), 200
    return render_template('editar_correo.html', correo=correo)


def get_app():
    return app

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5005)