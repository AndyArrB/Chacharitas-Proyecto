from flask import Flask
from flask_security.models import fsqla_v3
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security
from flask_mailman import Mail
from app.forms.register import ExtendedRegisterForm

from .config import *

# * Creamos la aplicación de Flask
app = Flask(__name__)

# * Realizamos todas las configuraciones necesarias
app.config.from_object("app.config")

# * Implementamos la conexión hacia nuestra base de datos
db = SQLAlchemy(app)
mail = Mail(app)
# * Inyectamos Flask-Security a nuestra base de datos
fsqla_v3.FsModels.set_db_info(db)


# * Generamos los modelos clave. Las requiere Flask-Security
class Role(db.Model, fsqla_v3.FsRoleMixin):
    pass

class User(db.Model, fsqla_v3.FsUserMixin):
    pass

# * Establecemos las clases que funcionarán como Usuarios y Roles
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# * Implementamos Flask-Security a la app
security = Security(app, user_datastore, register_form=ExtendedRegisterForm)



# * Generamos todos los modelos
with app.app_context():
    db.create_all()

from app import routes
