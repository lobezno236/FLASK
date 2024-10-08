# Importar las bibliotecas necesarias para crear la aplicación Flask y enviar correos electrónicos
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
import sys
sys.path.append('..')
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

# MODELOS CREADOS EN ARCHIVOS
from mail_config import MAIL_CONFIG
import models
from forms import RegistroForm

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

app.config.update(MAIL_CONFIG)

# Configurar la URI de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensajes.db'

# Crear una instancia de la biblioteca de correo electrónico
mail = Mail(app)

# Crear una instancia de la base de datos
db = SQLAlchemy(app)

# Definir la tabla de la base de datos
class Mensaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'Mensaje({self.nombre}, {self.correo}, {self.mensaje})'

# Crear la base de datos y la tabla
with app.app_context():
    db.create_all()
    
# Definir la ruta para la página de inicio
@app.route('/')
def index():
    # Crear un diccionario con los datos que se utilizarán en la página de inicio
    data={
        'titulo':'Index',
        'encabezado':'Bienvenido(a)'
    }
    # Renderizar la página de inicio con los datos del diccionario
    return render_template('index.html', data=data)

# Definir la ruta para el registro de usuarios
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        # Código para registrar el usuario
        return redirect(url_for('login'))
    return render_template('registro.html', form=form)

# Definir la ruta para la página de contacto
@app.route("/contacto", methods=["GET", "POST"])
def contacto():
    # Verificar si se ha enviado un formulario desde la página de contacto
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]
        
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
        
        # Crear un nuevo mensaje en la base de datos
        nuevo_mensaje = Mensaje(nombre=nombre, correo=correo, mensaje=mensaje)
        db.session.add(nuevo_mensaje)
        db.session.commit()
        
        # Devolver un mensaje de éxito a la página de contacto
        return render_template('enviado.html')
    
    # Crear un diccionario con los datos que se utilizarán en la página de contacto
    data = {
        'titulo': 'Contacto',
        'encabezado': 'Contacto'
    }
    # Renderizar la página de contacto con los datos del diccionario
    return render_template('contacto.html', data=data)

# Definir la ruta para la página de correos
@app.route('/correos')
def correos():
    # Obtener todos los correos de la base de datos
    correos = Mensaje.query.all()
    # Renderizar la página de correos con los correos obtenidos
    return render_template('correos.html', correos=correos)

# Definir la ruta para eliminar un correo
@app.route('/eliminar-correo/<int:id>')
def eliminar_correo(id):
    # Obtener el correo de la base de datos
    correo = Mensaje.query.get(id)
    # Eliminar el correo de la base de datos
    db.session.delete(correo)
    db.session.commit()
    # Redireccionar a la página de correos
    return redirect(url_for('correos'))

# Definir la ruta para editar un correo
@app.route('/editar-correo/<int:id>', methods=['GET', 'POST'])
def editar_correo(id):
    # Obtener el correo de la base de datos
    correo = Mensaje.query.get(id)
    if request.method == 'POST':
        # Actualizar el correo en la base de datos
        correo.nombre = request.form['nombre']
        correo.correo = request.form['correo']
        correo.mensaje = request.form['mensaje']
        db.session.commit()
        # Redireccionar a la página de correos
        return redirect(url_for('correos'))
    # Renderizar la página de edición de correos
    return render_template('editar_correo.html', correo=correo)

# Definir la ruta para la página de "Hola, Mundo"
@app.route('/holaMundo')
def hola_mundo():
    # Devolver un mensaje de "Hola, Mundo"
    return "Hola, Mundo"

# Verificar si el archivo se está ejecutando directamente
if __name__ == '__main__':
    # Agregar la ruta para la página de inicio
    app.add_url_rule('/',view_func=index)
    # Ejecutar la aplicación en modo de depuración
    app.run(debug=True, port=5005)