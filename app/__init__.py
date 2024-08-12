from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_security.models import fsqla_v3, fsqla
from flask_security import SQLAlchemyUserDatastore, Security
from flask_mail import Mail
from flask_babel import Babel
from sqlalchemy import insert, text
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
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{MYSQL_USERNAME}:{MYSQL_ROOT_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}'

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
    num_int: Mapped[int] = mapped_column(nullable=True)
    num_ext: Mapped[int] = mapped_column(nullable=False)
    genero = db.relationship('Genero', backref=db.backref('usuarios', cascade='all, delete-orphan'))
    calle = db.relationship('Calle', backref=db.backref('usuarios', cascade='all, delete-orphan'))


class Role(db.Model, fsqla_v3.FsRoleMixin):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True)


user_datastore = SQLAlchemyUserDatastore(db, User, Role)

with app.app_context():
    # ! --------------------- Crear tablas --------------------------! #
    db.create_all()

    # ! --------------------- Crear triggers ------------------------! #
    trigger_names = [
        "after_user_insert", "limit_user_products", "after_detalle_pedido_insert", "update_fecha_renovacion",
        "log_cambios_producto", "lol"
    ]
    trigger_sqls = {
        "update_fecha_renovacion": """
            CREATE TRIGGER update_fecha_renovacion
            BEFORE UPDATE ON suscripciones
            FOR EACH ROW
            BEGIN
                IF NEW.id_tipo_suscripcion != 1 THEN
                    SET NEW.fecha_renovacion = DATE_ADD(NEW.fecha_inicio, INTERVAL 1 MONTH);
                ELSE
                    SET NEW.fecha_renovacion = NULL;
                END IF;
            END;
        """,
        "after_user_insert": """
            CREATE TRIGGER after_user_insert
            AFTER INSERT ON usuarios
            FOR EACH ROW
            BEGIN
                INSERT INTO suscripciones (fecha_inicio, fecha_renovacion, id_cliente, id_tipo_suscripcion)
                VALUES (CURRENT_DATE, NULL, NEW.id, 1);
            END;
        """,
        "limit_user_products": """
            CREATE TRIGGER limit_user_products
            BEFORE INSERT ON productos
            FOR EACH ROW
            BEGIN
                DECLARE product_count INT;
                SELECT COUNT(*) INTO product_count FROM productos WHERE id_usuario = NEW.id_usuario;
                IF (SELECT id_tipo_suscripcion FROM suscripciones WHERE id_cliente = NEW.id_usuario) = 1 AND product_count >= 3 THEN
                    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El usuario con suscripción ID 1 no puede tener más de 3 productos.';
                END IF;
            END;
        """,
        "after_detalle_pedido_insert": """
            CREATE TRIGGER after_detalle_pedido_insert
            AFTER INSERT ON detalles_pedidos
            FOR EACH ROW
            BEGIN
                UPDATE productos SET cantidad = cantidad - NEW.cantidad WHERE id = NEW.id_producto;
            END;
        """,
        "log_cambios_producto": """
            CREATE TABLE IF NOT EXISTS cambios_producto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_producto INT,
                cantidad_antigua INT,
                cantidad_nueva INT,
                fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        "lol": """
            CREATE TRIGGER log_cambios_producto
            AFTER UPDATE ON productos
            FOR EACH ROW
            BEGIN
                INSERT INTO cambios_producto (id_producto, cantidad_antigua, cantidad_nueva)
                VALUES (OLD.id, OLD.cantidad, NEW.cantidad);
            END;
        """
    }

    with db.engine.connect() as connection:
        for trigger_name in trigger_names:
            try:
                connection.execute(text(trigger_sqls[trigger_name]))
                print(f'Trigger {trigger_name} created successfully')
            except:
                print("....")

    # ! --------------------- Crear vistas ------------------------! #
    views_sql = {
        "Vista_Clientes_Suscripciones_Activas": """
            CREATE VIEW Vista_Clientes_Suscripciones_Activas AS
            SELECT
                u.username AS Nombre_Cliente,
                u.email AS Email_Cliente,
                ts.nombre_suscripcion AS Nombre_Suscripcion,
                ts.precio AS Precio_Suscripcion,
                s.fecha_inicio AS Fecha_Inicio_Suscripcion
            FROM usuarios u
            INNER JOIN suscripciones s ON s.id_cliente = u.id
            INNER JOIN tipo_suscripciones ts ON ts.id = s.id_tipo_suscripcion
            WHERE
                CURDATE() BETWEEN s.fecha_inicio AND s.fecha_renovacion
                AND ts.nombre_suscripcion IN ('Junior', 'VIP');
        """,
        "Vista_Productos_Por_Categoria": """
            CREATE VIEW Vista_Productos_Por_Categoria AS
            SELECT
                c.tipo_categoria AS Categoria,
                p.nombre_producto AS Nombre_Producto,
                p.precio AS Precio_Producto,
                p.cantidad AS Cantidad_Disponible
            FROM productos p
            INNER JOIN categorias c ON p.id_categoria = c.id
            ORDER BY c.tipo_categoria ASC;
        """,
        "Vista_Ventas_Por_Cliente": """
            CREATE VIEW Vista_Ventas_Por_Cliente AS
            SELECT
                u.username AS Nombre_Cliente,
                p.fecha AS Fecha_Pedido,
                SUM(dp.cantidad * pr.precio) AS Total_Ventas
            FROM usuarios u
            INNER JOIN pedidos p ON p.id_cliente = u.id
            INNER JOIN detalles_pedidos dp ON dp.id_pedido = p.id
            INNER JOIN productos pr ON dp.id_producto = pr.id
            WHERE p.fecha BETWEEN '2023-01-01' AND '2024-12-31'
            GROUP BY u.username, p.fecha;
        """,
        "Vista_Pedidos_Pendientes_Entrega": """
            CREATE VIEW Vista_Pedidos_Pendientes_Entrega AS
            SELECT
                p.id AS Numero_Pedido,
                e.nombre AS Estatus_Pedido,
                pr.nombre_producto AS Producto,
                u.username AS Nombre_Cliente,
                p.fecha AS Fecha_Pedido
            FROM pedidos p
            INNER JOIN usuarios u ON p.id_cliente = u.id
            INNER JOIN detalles_pedidos dp ON dp.id_pedido = p.id
            INNER JOIN productos pr ON dp.id_producto = pr.id
            INNER JOIN estatus e ON p.id_estatus = e.id
            WHERE e.nombre = 'En Proceso';
        """,
        "Vista_Categorias_Con_Mas_Productos_Vendidos": """
            CREATE VIEW Vista_Categorias_Con_Mas_Productos_Vendidos AS
            SELECT
                c.tipo_categoria AS Categoria,
                COUNT(dp.id_producto) AS Total_Productos_Vendidos
            FROM productos pr
            INNER JOIN categorias c ON pr.id_categoria = c.id
            INNER JOIN detalles_pedidos dp ON dp.id_producto = pr.id
            GROUP BY c.tipo_categoria
            ORDER BY Total_Productos_Vendidos DESC;
        """
    }

    with db.engine.connect() as connection:
        for view_name, view_sql in views_sql.items():
            try:
                connection.execute(text(view_sql))
                print(f'View {view_name} created successfully')
            except Exception as e:
                print(f"....")

# ! --------------------- Crear registros base ------------------------! #
    try:
        for model, records in data.items():
            if model.__name__ == 'Producto':
                continue
            if not db.session.query(model).count():
                print("Evaluando a ", model)
                db.session.execute(insert(model), records)
        db.session.commit()

        admin_role = user_datastore.find_or_create_role("admin")
        root = user_datastore.find_user(username="root")

        if not root:
            root = user_datastore.create_user(
                username="root",
                password="root",
                us_phone_number="+524421941945",
                email="ayrtonsepch@gmail.com",
                id_genero=1,
                id_calle=1,
                num_int=None,
                num_ext=111
            )
            user_datastore.add_role_to_user(root, admin_role)
            db.session.commit()
            print("Usuario root creado con exito!")

        root_andy = user_datastore.find_user(username="andy")

        if not root_andy:
            root_andy = user_datastore.create_user(
                username="andy",
                password="andy",
                us_phone_number="+524421941943",
                email="arredondo.bal2020@gmail.com",
                id_genero=2,
                id_calle=12,
                num_int=None,
                num_ext=111
            )
            print("Usuario Andy creado con exito!")

        user_datastore.add_role_to_user(root_andy, admin_role)
        db.session.commit()
        additional_users = [
            {"username": "juan", "password": "password1", "us_phone_number": "+524421941946",
             "email": "juan@example.com", "id_genero": 1, "id_calle": 1, "num_int": 2, "num_ext": 112},
            {"username": "paola", "password": "password2", "us_phone_number": "+524421941947",
             "email": "paola@example.com", "id_genero": 2, "id_calle": 30, "num_int": None, "num_ext": 321},
            {"username": "carlos", "password": "password3", "us_phone_number": "+524421941948",
             "email": "carlos@example.com", "id_genero": 1, "id_calle": 11, "num_int": 32, "num_ext": 110},
            {"username": "maria", "password": "password4", "us_phone_number": "+524421941949",
             "email": "maria@example.com", "id_genero": 2, "id_calle": 16, "num_int": None, "num_ext": 642},
            {"username": "luis", "password": "password5", "us_phone_number": "+524421941950",
             "email": "luis@example.com", "id_genero": 1, "id_calle": 26, "num_int": 1, "num_ext": 143},
            {"username": "ana", "password": "password6", "us_phone_number": "+524421941951",
             "email": "ana@example.com", "id_genero": 1, "id_calle": 28, "num_int": 1, "num_ext": 16},
            {"username": "pedro", "password": "password7", "us_phone_number": "+524421941952",
             "email": "pedro@example.com", "id_genero": 1, "id_calle": 29, "num_int": None, "num_ext": 246},
            {"username": "sofia", "password": "password8", "us_phone_number": "+524421941953",
             "email": "sofia@example.com", "id_genero": 1, "id_calle": 27, "num_int": 14, "num_ext": 2346}
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

security = Security(app, user_datastore, register_form=ExtendedRegisterForm, confirm_register_form=ExtendedRegisterForm)

from app import routes
