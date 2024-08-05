import urllib

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_security.models import fsqla_v3, fsqla
from flask_security import SQLAlchemyUserDatastore, Security
from flask_mail import Mail
from flask_babel import Babel
from sqlalchemy import insert
from sqlalchemy.orm import mapped_column, Mapped
from app.forms.register import ExtendedRegisterForm
from app.config import *
from app.models import db
from app.registries import data
from sqlalchemy.exc import SQLAlchemyError
from os import getenv
from dotenv import load_dotenv

load_dotenv()
MYSQL_ROOT_PASSWORD = getenv("MYSQL_ROOT_PASSWORD")
MYSQL_DATABASE = getenv("MYSQL_DATABASE")
MYSQL_HOST = getenv("MYSQL_HOST") or "localhost"
MYSQL_USERNAME = getenv("MYSQL_USERNAME") or "root"

app = Flask(__name__)
app.config.from_object("app.config")

if getenv("DOCKER") == "on":
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{MYSQL_ROOT_PASSWORD}@db/{MYSQL_DATABASE}'
else:
    #* Configuramos la conexión de la app hacia la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'



db.init_app(app)
bootstrap = Bootstrap5(app)
babel = Babel(app)
mail = Mail(app)

fsqla.FsModels.set_db_info(db, "usuarios", "roles")

class User(db.Model, fsqla_v3.FsUserMixin):
    __tablename__ = 'usuarios'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_genero: Mapped[int] = mapped_column(db.ForeignKey('generos.id'), nullable=False)
    id_calle: Mapped[int] = mapped_column(db.ForeignKey('calles.id'), nullable=False)
    num_int: Mapped[str] = mapped_column(db.String(50), nullable=True)  # Specify length for VARCHAR
    num_ext: Mapped[str] = mapped_column(db.String(50), nullable=False)  # Specify length for VARCHAR
    genero = db.relationship('Genero', backref=db.backref('usuarios', cascade='all, delete-orphan'))
    calle = db.relationship('Calle', backref=db.backref('usuarios', cascade='all, delete-orphan'))


class Role(db.Model, fsqla_v3.FsRoleMixin):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

with app.app_context():
    db.create_all()

    try:
        # Insert initial data if not already present
        for model, records in data.items():
            if model.__name__ == 'Producto':
                continue
            if not db.session.query(model).count():
                print("Evaluando a ", model)
                db.session.execute(insert(model), records)
        db.session.commit()

        # Create root user and assign admin role if not already present
        admin_role = user_datastore.find_or_create_role("admin")
        root = user_datastore.find_user(username="root")

        if not root:
            root = user_datastore.create_user(
                username="root",
                password="root",
                us_phone_number="+524421941945",
                email="ayrtonsepch@gmail.com",
                id_genero=1,  # Assuming 1 is a valid id in the 'generos' table
                id_calle=1,
                num_int=None,
                num_ext="111"
            )
            user_datastore.add_role_to_user(root, admin_role)
            db.session.commit()

        additional_users = [
            {"username": "juan", "password": "password1", "us_phone_number": "+524421941946",
             "email": "juan@example.com", "id_genero": 1, "id_calle": 1, "num_int": 2, "num_ext": "112"},
            {"username": "paola", "password": "password2", "us_phone_number": "+524421941947",
             "email": "paola@example.com", "id_genero": 2, "id_calle": 30, "num_int": None, "num_ext": "321"},
            {"username": "carlos", "password": "password3", "us_phone_number": "+524421941948",
             "email": "carlos@example.com", "id_genero": 1, "id_calle": 11, "num_int": 32, "num_ext": "110"},
            {"username": "maria", "password": "password4", "us_phone_number": "+524421941949",
             "email": "maria@example.com", "id_genero": 2, "id_calle": 16, "num_int": None, "num_ext": "642"},
            {"username": "luis", "password": "password5", "us_phone_number": "+524421941950",
             "email": "luis@example.com", "id_genero": 1, "id_calle": 26, "num_int": 1, "num_ext": "143"},
            {"username": "ana", "password": "password6", "us_phone_number": "+524421941951",
             "email": "ana@example.com", "id_genero": 1, "id_calle": 28, "num_int": 1, "num_ext": "16"},
            {"username": "pedro", "password": "password7", "us_phone_number": "+524421941952",
             "email": "pedro@example.com", "id_genero": 1, "id_calle": 29, "num_int": None, "num_ext": "246"},
            {"username": "sofia", "password": "password8", "us_phone_number": "+524421941953",
             "email": "sofia@example.com", "id_genero": 1, "id_calle": 27, "num_int": 14, "num_ext": "2346"}
        ]

        for user_data in additional_users:
            existing_user = user_datastore.find_user(email=user_data["email"])
            if not existing_user:
                user = user_datastore.create_user(**user_data)
                user_datastore.add_role_to_user(user, admin_role)
        db.session.commit()

        for model, records in data.items():
            if model.__name__ != 'Producto':
                continue
            if not db.session.query(model).count():
                print("Evaluando a ", model)
                db.session.execute(insert(model), records)
        db.session.commit()

    except SQLAlchemyError as e:
        print(f"Error al insertar datos: {e}")
        db.session.rollback()

# * Implementamos Flask-Security a la app
security = Security(app, user_datastore, register_form=ExtendedRegisterForm, confirm_register_form=ExtendedRegisterForm)

from app import routes