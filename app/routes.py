from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import db
from models import Usuario, Correo
from forms import LoginForm, RegistroForm
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from views import contacto_view

from app_factory import create_app

main = Blueprint('main', __name__)

def init_routes(app):
    # print("Initializing routes...")
    # app.register_blueprint(main)
    main.add_url_rule('/contacto', view_func=contacto_view)

@main.route('/')
def index():
    data = {
        'titulo': 'Index',
        'encabezado': 'Bienvenido(a)'
    }
    return render_template('index.html', data=data)

@main.route('/login', methods=['GET', 'POST'])
def login():
    data = {'titulo': 'Login'}
    form = LoginForm()
    if request.method == 'POST':
        username_or_correo = form.username_or_correo.data
        password = form.password.data
        user = Usuario.query.filter_by(username=username_or_correo).first()
        if user is None:
            user = Usuario.query.filter_by(correo=username_or_correo).first()
        if user and user.verificar_contraseña(password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', data=data, form=form)

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    data = {'titulo': 'Registro'}
    form = RegistroForm()
    if form.validate_on_submit():
        username = form.username.data
        nombre = form.nombre.data
        correo = form.correo.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password == confirm_password:
            user = Usuario.query.filter_by(username=username).first()
            correo_existe = Usuario.query.filter_by(correo=correo).first()
            if user is not None:
                form.username.errors.append('El nombre de usuario ya existe')
            if correo_existe is not None:
                form.correo.errors.append('El correo electrónico ya existe')
            if user is None and correo_existe is None:
                user = Usuario(username=username, nombre=nombre, correo=correo, contraseña=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                flash('Registro exitoso', 'success')
                return redirect(url_for('login'))
        else:
            flash('Las contraseñas no coinciden', 'error')
    return render_template('registro.html', data=data, form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has salido de la sesión correctamente', 'success')
    return redirect(url_for('index'))

@main.route('/holaMundo')
def hola_mundo():
    return "Hola, Mundo"

@main.route("/eliminar_correo/<int:id>")
def eliminar_correo(id):
    correo = Correo.query.get_or_404(id)
    db.session.delete(correo)
    db.session.commit()
    return redirect(url_for('correos'))

@main.route("/editar_correo/<int:id>", methods=["GET", "POST"])
def editar_correo(id):
    correo = Correo.query.get_or_404(id)
    if request.method == "POST":
        correo.nombre = request.form["nombre"]
        correo.correo = request.form["correo"]
        correo.mensaje = request.form["mensaje"]
        db.session.commit()
        return redirect(url_for('correos'))
    return render_template('editar_correo.html', correo=correo)

@main.route("/correos")
@login_required
def correos():
    data = {
        'titulo': 'Correos',
        'encabezado': 'Bienvenido(a)'
    }
    # Obtener todos los correos de la base de datos
    correos = Correo.query.all()
    if correos is None or len(correos) == 0:
        flash('No hay correos en la base de datos', 'info')
    # Renderizar la plantilla de correos
    return render_template('correos.html', correos=correos, data=data)

