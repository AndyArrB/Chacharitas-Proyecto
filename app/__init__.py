from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_security.models import fsqla_v3, fsqla
from flask_security import SQLAlchemyUserDatastore, Security
from flask_mail import Mail
from flask_babel import Babel
from sqlalchemy.orm import mapped_column, Mapped

from app.forms.register import ExtendedRegisterForm
from app.config import *
from app.models import db, Municipio, Colonia, Calle, Direccion, Marca, Categoria, Genero, FormaPago, Color, \
    Material, TipoTamaño, DetalleTamaño, Producto, TipoSuscripcion, Suscripcion, Estatus, Pedido, DetallePedido

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
    nombre: Mapped[str] = mapped_column(nullable=False)
    apellido_paterno: Mapped[str] = mapped_column(nullable=False)
    apellido_materno: Mapped[str] = mapped_column(nullable=False)
    id_genero: Mapped[int] = mapped_column(db.ForeignKey('generos.id'), nullable=False)
    id_direccion: Mapped[int] = mapped_column(db.ForeignKey('direcciones.id'), nullable=False)
    genero = db.relationship('Genero', backref=db.backref('usuarios', cascade='all, delete-orphan'))
    direccion = db.relationship('Direccion', backref=db.backref('usuarios', cascade='all, delete-orphan'))


class Role(db.Model, fsqla_v3.FsRoleMixin):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)

from sqlalchemy.exc import SQLAlchemyError

with app.app_context():
    db.create_all()

    try:
        admin_role = user_datastore.find_or_create_role("admin")
        root = user_datastore.find_user(username="root")

        if not root:
            genero1 = Genero(nombre_genero="Masculino")
            genero2 = Genero(nombre_genero="Femenino")

            db.session.add(genero1)
            db.session.add(genero2)
            db.session.commit()

            municipio1 = Municipio(nombre_municipio="Municipio1")
            municipio2 = Municipio(nombre_municipio="Municipio2")
            db.session.add(municipio1)
            db.session.add(municipio2)
            db.session.commit()

            # Insert records into the 'colonias' table
            colonia1 = Colonia(nombre_colonia="Colonia1", cp="12345", municipio_id=municipio1.id)
            colonia2 = Colonia(nombre_colonia="Colonia2", cp="67890", municipio_id=municipio2.id)
            db.session.add(colonia1)
            db.session.add(colonia2)
            db.session.commit()

            # Insert records into the 'calles' table
            calle1 = Calle(nombre_calle="Calle1", colonia_id=colonia1.id)
            calle2 = Calle(nombre_calle="Calle2", colonia_id=colonia2.id)
            db.session.add(calle1)
            db.session.add(calle2)
            db.session.commit()

            # Insert records into the 'direcciones' table
            direccion1 = Direccion(num_int="101", num_ext="123", calle_id=calle1.id)
            direccion2 = Direccion(num_int="202", num_ext="456", calle_id=calle2.id)
            db.session.add(direccion1)
            db.session.add(direccion2)
            db.session.commit()

            root = user_datastore.create_user(
                username="root",
                password="root",
                us_phone_number="+524421941945",
                email="ayrtonsepch@gmail.com",
                nombre="Root",
                apellido_paterno="Admin",
                apellido_materno="User",
                id_genero=1,  # Assuming 1 is a valid id in the 'generos' table
                id_direccion=1  # Assuming 1 is a valid id in the 'direcciones' table
            )
            db.session.commit()

        user_datastore.add_role_to_user(root, admin_role)

    except SQLAlchemyError as e:
        print(f"Error al crear el usuario: {e}")
        db.session.rollback()

# * Implementamos Flask-Security a la app
security = Security(app, user_datastore, register_form=ExtendedRegisterForm, confirm_register_form=ExtendedRegisterForm)

from app import routes