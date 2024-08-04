# ? Contiene la clase "Database", la cual abstrae todavía más la interacción con la base
# ? de datos establecida por Flask-SQLAlchemy

from sqlalchemy import select, insert, delete, update, Table, Column
from app import app, User
from app import db
from app.models import Calle, Colonia, Municipio


class Database:

    # * Constructor. Aquí declaramos las propiedades de la clase
    # * las cuales serán las tablas de la base de datos.
    def __init__(self):
        self.database = db

        # * Cargamos la información de las tablas  de nuesta DB en la
        # * propiedad metadata que utiliza SQLAlchemy para saber los
        # * tipos de dato, foreign keys etc de cada tabla...
        with app.app_context():
            self.database.reflect()

        # * ... Y las asignamos como propiedades
        for table_name, table in self.database.metadata.tables.items():
            setattr(self, table_name, table)

    # * Sobrecarga del operador []. Nos permite acceder a las propiedades
    # * de la clase mediante corchetes. En vez de db.tabla, podemos usar
    # * db[tabla], lo que facilita el acceso dinámicamente.
    def __getitem__(self, table_name: str):
        try:
            return getattr(self, table_name)
        except:
            raise KeyError(f"La tabla {table_name} no existe!")

    # ! Funcionalidades genéricas de CRUD
    # * Regresa todos los registros de una tabla
    def select_all(self, table: Table):
        stmt = select(table)
        result = self.database.session.execute(stmt)
        return result.all()

    # * Regresa una lista con el nombre de todas las columnas
    def select_columns(self, table: Table):
        columns = table.columns
        return list(columns.keys())

    # * Regresa una lista con el nombre de todas las tablas
    def select_tables(self):
        tables = self.database.metadata.tables
        return list(tables.keys())

    # * Inserta un registro
    def insert_into(self, table: Table = None, data: dict = None):
        print("Insertando....")
        stmt = insert(table).values(**data)  # Se utiliza ** para desempaquetar dicts
        self.database.session.execute(stmt)
        self.database.session.commit()

    # * Actualiza un registro
    def update_from(self, table: Table, registry_id: int, data: dict):
        print("Actualizando...")
        stmt = update(table).where(table.columns.id == registry_id).values(data)
        self.database.session.execute(stmt)
        self.database.session.commit()

    # * Elimina un registro
    def delete_from(self, table: Table, registry_id: int):
        print("Eliminando...")
        stmt = delete(table).where(table.columns.id == registry_id)
        self.database.session.execute(stmt)
        self.database.session.commit()

    # * Regresa datos relevantes de todas las columnas de cierta tabla
    def select_columns_data(self, table: Table):
        table_info = {}

        for column in table.columns:
            table_info[column.name] = {
                "name": str(column.name),
                "type": str(column.type),
                "nullable": column.nullable,
                "default": str(column.default.arg) if column.default is not None else None,
                "primary_key": column.primary_key,
                "foreign_key": list(column.foreign_keys)
            }

        return table_info

    # ! Funcionalidades especializadas a la app
    def select_filtered_products(self, price_ranges=None, categories=None, genders=None, sort_by=None):
        from sqlalchemy import or_, and_

        products_table = self.database.metadata.tables['productos']

        filters = []
        if price_ranges:
            price_filters = []
            for pr in price_ranges:
                if pr == 1:
                    price_filters.append(and_(products_table.c.precio >= 0, products_table.c.precio <= 50))
                elif pr == 2:
                    price_filters.append(and_(products_table.c.precio >= 50, products_table.c.precio <= 100))
                elif pr == 3:
                    price_filters.append(and_(products_table.c.precio >= 100, products_table.c.precio <= 150))
                elif pr == 4:
                    price_filters.append(products_table.c.precio >= 150)
            filters.append(or_(*price_filters))
        if categories:
            category_filters = [products_table.c.id_categoria == cat for cat in categories]
            filters.append(or_(*category_filters))
        if genders:
            gender_filters = [products_table.c.id_genero == gen for gen in genders]
            filters.append(or_(*gender_filters))

        print("----Pre orderby-----", sort_by)
        if sort_by == 2:
            print("Hey")
            stmt = select(products_table) \
                .join(User, products_table.c.id_usuario == User.id) \
                .join(Calle, User.id_calle == Calle.id) \
                .join(Colonia, Calle.colonia_id == Colonia.id) \
                .join(Municipio, Colonia.municipio_id == Municipio.id) \
                .where(and_(*filters)) \
                .order_by(products_table.c.nombre_producto)
        elif sort_by == 3:
            stmt = select(products_table) \
                .join(User, products_table.c.id_usuario == User.id) \
                .join(Calle, User.id_calle == Calle.id) \
                .join(Colonia, Calle.colonia_id == Colonia.id) \
                .join(Municipio, Colonia.municipio_id == Municipio.id) \
                .where(and_(*filters)) \
                .order_by(products_table.c.precio)
        else:
            stmt = select(products_table) \
                .join(User, products_table.c.id_usuario == User.id) \
                .join(Calle, User.id_calle == Calle.id) \
                .join(Colonia, Calle.colonia_id == Colonia.id) \
                .join(Municipio, Colonia.municipio_id == Municipio.id) \
                .where(and_(*filters))

        print(f"Constructed query: {str(stmt)}")

        result = self.database.session.execute(stmt)
        products = [dict(row._mapping) for row in result]
        print(products)
        return products
