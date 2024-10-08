# Importar las bibliotecas necesarias
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Importar el archivo de configuración de correo electrónico
from mail_config import MAIL_CONFIG
from forms import LoginForm, RegistroForm
from utils import bcrypt
from utils import db

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Configurar la clave secreta de la aplicación
app.config['SECRET_KEY'] = 'ADMIN123'

# Configurar la biblioteca de correo electrónico
app.config.update(MAIL_CONFIG)

# Crear una instancia de la biblioteca de SQLAlchemy
# db = SQLAlchemy(app)

# Crear una instancia de la biblioteca de correo electrónico
mail = Mail(app)

login_manager = LoginManager(app)

# Definir el modelo para almacenar los usuarios
class Usuario(db.Model, UserMixin):
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

# Definir el modelo para almacenar los correos
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

# Crear la base de datos y tablas
with app.app_context():
    print("Antes de crear las tablas")
    db.create_all()
    print("Después de crear las tablas")
    if db is None:
        print("Error: La base de datos no se ha inicializado correctamente")
        2

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Usuario, int(user_id))

@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = {'titulo': 'Login'}
    form = LoginForm()
    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        user = Usuario.query.filter_by(correo=correo).first()
        if user and user.verificar_contraseña(password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html', data=data, form=form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    data = {'titulo': 'Registro'}
    form = RegistroForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        correo = form.correo.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        if password == confirm_password:
            user = Usuario(nombre=nombre, correo=correo, contraseña=password)
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

# Definir las rutas de la aplicación
@app.route('/')
def index():
    # Datos para la plantilla
    data = {
        'titulo': 'Index',
        'encabezado': 'Bienvenido(a)'
    }
    # Renderizar la plantilla
    return render_template('index.html', data=data)

    # Datos para la plantilla
    data = {
        'titulo': 'Login',
        'encabezado': 'Iniciar sesión'
    }
    # Renderizar la plantilla
    return render_template('login.html', data=data)

@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    # Datos para la plantilla
    data = {
        'titulo': 'Contacto',
        'encabezado': 'Contacto'
    }
    
    # Procesar el formulario de contacto
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]
        
        # Crear un nuevo correo en la base de datos
        nuevo_correo = Correo(nombre=nombre, correo=correo, mensaje=mensaje)
        db.session.add(nuevo_correo)
        db.session.commit()
        
        # Crear un mensaje de correo electrónico
        msg = Message('Mensaje de contacto', sender=correo, recipients=['lobezno236@gmail.com'])
        # Agregar el cuerpo del mensaje
        msg.body = mensaje
        try:
            # Enviar el mensaje de correo electrónico
            mail.send(msg)
            # Imprimir un mensaje de éxito en la consola
            print('Mensaje enviado con éxito')
        except Exception as e:
            # Imprimir un mensaje de error en la consola si ocurre un error
            print(f'Error al enviar el mensaje: {e}')
            # Devolver un mensaje de error a la página de contacto
            return "Error al enviar el mensaje"
        
        # Devolver un mensaje de éxito a la página de contacto
        return render_template('enviado.html', data=data)
    
    # Renderizar la plantilla de contacto
    return render_template('contacto.html', data=data)

@app.route('/holaMundo')
def hola_mundo():
    # Devolver un mensaje de "Hola, Mundo"
    return "Hola, Mundo"

@app.route("/eliminar_correo/<int:id>")
def eliminar_correo(id):
    # Obtener el correo de la base de datos
    correo = Correo.query.get_or_404(id)
    
    # Eliminar el correo de la base de datos
    db.session.delete(correo)
    db.session.commit()
    
    # Redireccionar a la página de correos
    return redirect(url_for('correos'))

@app.route("/editar_correo/<int:id>", methods=["GET", "POST"])
def editar_correo(id):
    # Obtener el correo de la base de datos
    correo = Correo.query.get_or_404(id)
    
    # Procesar el formulario de edición
    if request.method == "POST":
        # Obtener los datos del formulario
        correo.nombre = request.form["nombre"]
        correo.correo = request.form["correo"]
        correo.mensaje = request.form["mensaje"]
        
        # Guardar los cambios en la base de datos
        db.session.commit()
        
        # Redireccionar a la página de correos
        return redirect(url_for('correos'))
    
    # Renderizar la plantilla de edición
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


# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=5005)