#? Contiene la clase "Database", la cual abstrae todavía más la interacción con la base
#? de datos establecida por Flask-SQLAlchemy

from sqlalchemy import select, insert, delete, update, Table
from app import app
from app import db


class Database:

    #* Constructor. Aquí declaramos las propiedades de la clase
    #* las cuales serán las tablas de la base de datos.
    def __init__(self):
        self.database = db

        #* Cargamos la información de las tablas  de nuesta DB en la
        #* propiedad metadata que utiliza SQLAlchemy para saber los
        #* tipos de dato, foreign keys etc de cada tabla...
        with app.app_context():
            self.database.reflect()

        #* ... Y las asignamos como propiedades
        for table_name, table in self.database.metadata.tables.items():
            setattr(self, table_name, table)

    #* Sobrecarga del operador []. Nos permite acceder a las propiedades
    #* de la clase mediante corchetes. En vez de db.tabla, podemos usar
    #* db[tabla], lo que facilita el acceso dinámicamente.
    def __getitem__(self, table_name: str):
        try:
            return getattr(self, table_name)
        except:
            raise KeyError(f"La tabla {table_name} no existe!")

    #* Regresa todos los registros de una tabla
    def select_all(self, table: Table):
        stmt = select(table)
        result = self.database.session.execute(stmt)
        return result.all()

    #* Regresa una lista con el nombre de todas las columnas
    def select_columns(self, table: Table):
        columns = table.columns
        return list(columns.keys())

    #* Regresa una lista con el nombre de todas las tablas
    def select_tables(self):
        tables = self.database.metadata.tables
        return list(tables.keys())

    #* Inserta un registro
    def insert_into(self, table: Table = None, data: dict = None):
        print("Insertando....")
        stmt = insert(table).values(**data)     # Se utiliza ** para desempaquetar dicts
        self.database.session.execute(stmt)
        self.database.session.commit()

    #* Actualiza un registro
    def update_from(self, table: Table, registry_id: int, data: dict):
        print("Actualizando...")
        stmt = update(table).where(table.columns.id == registry_id).values(data)
        self.database.session.execute(stmt)
        self.database.session.commit()

    #* Elimina un registro
    def delete_from(self, table: Table, registry_id: int):
        print("Eliminando...")
        stmt = delete(table).where(table.columns.id == registry_id)
        self.database.session.execute(stmt)
        self.database.session.commit()

    #* Regresa datos relevantes de todas las columnas de cierta tabla
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

