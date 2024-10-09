from flask import Flask
from flask_mail import Mail
from mail_config import MAIL_CONFIG

mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.update(MAIL_CONFIG)
    mail.init_app(app)
    return app