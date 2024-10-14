from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, DateField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length
import requests



class LoginForm(FlaskForm):
    csrf_token = HiddenField()
    username_or_correo = StringField('Usuario o correo electrónico', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

class RegistroForm(FlaskForm):
    csrf_token = HiddenField()
    username = StringField('Usuario', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    correo = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[DataRequired(), Regexp(r'^\d{9,15}$', message="Número de teléfono no válido. Debe contener entre 9 y 15 dígitos.")])
    documento_identidad = StringField('Documento de identidad', validators=[
        DataRequired(),
        Length(min=10, max=20, message="El documento de identidad debe tener entre 10 y 20 caracteres"),
        Regexp(r'^[A-Z0-9]+$', message="El documento de identidad solo puede contener letras mayúsculas y números")
    ])
    genero = SelectField('Género', choices=['Masculino', 'Femenino', 'Otro'], validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de nacimiento', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')
    
class EditarPerfilForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    correo = StringField('Correo electrónico', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    documento_identidad = StringField('Documento de identidad', validators=[DataRequired()])
    genero = StringField('Género', validators=[DataRequired()])
    submit = SubmitField('Guardar cambios')
    
class EditarDireccionForm(FlaskForm):
    calle = StringField('Calle', validators=[DataRequired()])
    numero = StringField('Número', validators=[DataRequired()])
    ciudad = StringField('Ciudad', validators=[DataRequired()])
    estado = StringField('Estado', validators=[DataRequired()])
    pais = StringField('País', validators=[DataRequired()])
    codigo_postal = StringField('Código postal', validators=[DataRequired()])
    submit = SubmitField('Guardar cambios')
    
class ModificarContraseñaForm(FlaskForm):
    contraseña_actual = PasswordField('Contraseña actual', validators=[DataRequired()])
    nueva_contraseña = PasswordField('Nueva contraseña', validators=[DataRequired()])
    confirmar_contraseña = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Modificar contraseña')
    
