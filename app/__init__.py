from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_security.models import fsqla_v3
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security
from flask_mail import Mail
from flask_babel import Babel

from app.forms.register import ExtendedRegisterForm
from app.config import *

# * Creamos la aplicación de Flask
app = Flask(__name__)

# * Realizamos todas las configuraciones necesarias
app.config.from_object("app.config")

# * Implementamos la conexión hacia nuestra base de datos
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
babel = Babel(app)

# * Inyectamos Flask-Security y Flask-Mail a nuestra base de datos
fsqla_v3.FsModels.set_db_info(db)
mail = Mail(app)


# * Generamos los modelos clave. Las requiere Flask-Security
class Role(db.Model, fsqla_v3.FsRoleMixin):
    pass


class User(db.Model, fsqla_v3.FsUserMixin):
    pass


# * Establecemos las clases que funcionarán como Usuarios y Roles
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

from sqlalchemy.exc import SQLAlchemyError

with app.app_context():
    db.create_all()
    try:

        admin_role = user_datastore.find_or_create_role("admin")
        root = user_datastore.find_user(username="root")

        if not root:
            root = user_datastore.create_user(username="root", password="root", us_phone_number="+524421941945", email="ayrtonsepch@gmail.com")
            db.session.commit()

        user_datastore.add_role_to_user(root, admin_role)

        db.session.commit()

    except SQLAlchemyError as e:
        print(f"Error al crear el usuario: {e}")
        db.session.rollback()

# * Implementamos Flask-Security a la app
security = Security(app, user_datastore, register_form=ExtendedRegisterForm, confirm_register_form=ExtendedRegisterForm)

from app import routes
