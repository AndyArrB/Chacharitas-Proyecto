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

app = Flask(__name__)
app.config.from_object("app.config")

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
    num_int: Mapped[str] = mapped_column(nullable=True)
    num_ext: Mapped[str] = mapped_column(nullable=False)
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