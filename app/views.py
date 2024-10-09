from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import db
from models import Usuario, Correo
from forms import LoginForm, RegistroForm
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message, Mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

def contacto_view(mail):
    data = {
        'titulo': 'Contacto',
        'encabezado': 'Contacto'
    }
    if request.method == "POST":
        nombre = request.form["nombre"]
        correo = request.form["correo"]
        mensaje = request.form["mensaje"]
        nuevo_correo = Correo(nombre=nombre, correo=correo, mensaje=mensaje)
        db.session.add(nuevo_correo)
        db.session.commit()
        msg = Message('Mensaje de contacto', sender=correo, recipients=['lobezno236@gmail.com'])
        msg.body = mensaje
        try:
            mail.send(msg)
            print('Mensaje enviado con éxito')
        except Exception as e:
            print(f'Error al enviar el mensaje: {e}')
            return "Error al enviar el mensaje"
        return render_template('enviado.html', data=data)
    return render_template('contacto.html', data=data)