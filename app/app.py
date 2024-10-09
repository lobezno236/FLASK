from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from mail_config import MAIL_CONFIG
from forms import LoginForm, RegistroForm
from utils import bcrypt, db
from models import Usuario, Correo, Producto
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from views import contacto_view
from config import config
from app_factory import create_app
import routes

app = create_app()
routes.init_routes(app)
app.config.from_object(config['development'])
print(app.url_map)


# Registro de la ruta principal
# app.register_blueprint(main, name='main_blueprint')

# Configuración de la base de datos
app.config['APPLICATION_ROOT'] = '/'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de la clave secreta
app.config['SECRET_KEY'] = 'secrets.token_urlsafe(16)'

# Configuración del correo electrónico
app.config.update(MAIL_CONFIG)

mail = Mail(app)

# Inicialización de la base de datos
db.init_app(app)
with app.app_context():
    db.create_all()
    
# Inicialización del sistema de autenticación
login_manager = LoginManager(app)

# Función para cargar el usuario actual
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

@app.route('/')
def index():
    data = {
        'titulo': 'Index',
        'encabezado': 'Bienvenido(a)'
    }
    return render_template('index.html', data=data)

@app.route('/contacto')
def contacto():
    data = {
        'titulo': 'Contacto',
        'encabezado': 'Bienvenido(a)'
    }
    return render_template('contacto.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = {'titulo': 'Login'}
    form = LoginForm()
    if request.method == 'POST':
        username_or_correo = form.username_or_correo.data
        user = Usuario.query.filter_by(username=username_or_correo).first()
        if user is None:
            user = Usuario.query.filter_by(correo=username_or_correo).first()
        if user:
            print("User found:", user.username)
            login_user(user)
            return redirect(url_for('index'))
        else:
            print("User   not found")
    return render_template('login.html', data=data, form=form)

@app.route('/test', methods=['GET', 'POST'])
def test():
    user = Usuario(username='test', nombre='Test User', correo='test@example.com', contraseña='tu_contraseña')
    password = 'tu_contraseña'
    if user.verificar_contraseña(password):
        return 'La contraseña es correcta'
    else:
        return 'La contraseña es incorrecta'

@app.route('/registro', methods=['GET', 'POST'])
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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has salido de la sesión correctamente', 'success')
    return redirect(url_for('index'))

@app.route('/holaMundo')
def hola_mundo():
    return "Hola, Mundo"

@app.route("/eliminar_correo/<int:id>")
def eliminar_correo(id):
    correo = Correo.query.get_or_404(id)
    db.session.delete(correo)
    db.session.commit()
    return redirect(url_for('correos'))

@app.route("/editar_correo/<int:id>", methods=["GET", "POST"])
def editar_correo(id):
    correo = Correo.query.get_or_404(id)
    if request.method == "POST":
        correo.nombre = request.form["nombre"]
        correo.correo = request.form["correo"]
        correo.mensaje = request.form["mensaje"]
        db.session.commit()
        return redirect(url_for('correos'))
    return render_template('editar_correo.html', correo=correo)

@app.route("/correos")
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

@app.route('/productos')
def productos():
    data = {
        'titulo': 'Productos',
        'encabezado': 'Productos'
    }
    productos = Producto.query.all()
    return render_template('productos.html', data=data, productos=productos)

@app.route('/productos/<int:id>/', methods=['GET'])
def producto_detalle_individual(id):
    data = {
        'titulo': 'Detalle del producto',
        'encabezado': 'Detalle del producto'
    }
    producto = Producto.query.get_or_404(id)
    return render_template('producto_detalle.html', producto=producto, data=data)

@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    data = {
        'titulo': 'Agregar producto',
        'encabezado': 'Agregar producto'
    }
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        categoria = request.form['categoria']
        imagen = request.form['imagen']
        
        nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, categoria=categoria, imagen=imagen)
        db.session.add(nuevo_producto)
        db.session.commit()
        
        return redirect(url_for('productos'))
    return render_template('agregar_producto.html', data=data)



def get_app():
    return app

# Ejecución de la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5005)