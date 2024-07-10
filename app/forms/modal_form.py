# ? Función que se encarga de generar una clase de FlaskWTF con los <input>
# ? y <select> correctos de acorde a las necesidades de cada tabla

from flask_wtf import FlaskForm
from wtforms.fields.choices import SelectField  # <select>
from wtforms.fields.datetime import DateField  # <input type="datetime">
from wtforms.fields.numeric import IntegerField, DecimalField  # <input type="number">
from wtforms.fields.simple import StringField  # <input type="text">
from wtforms.fields.simple import SubmitField  # <input type="button">
from wtforms.validators import DataRequired, Length  # Validación del formulario

from app.database import Database

from typing import List, Dict, Any  # Validación de datos y documentación
from re import findall  # Expresiones regulares


# * Función que genera clases (formularios de Flask-WTF) dinámicamente
def generate_dynamic_form(table_columns_data: Dict[str, Any], table_columns: List[str],
                          db: Database):
    # * Los <input> dependerán del tipo de columna.
    fields = {column: get_field_class(table_columns_data[column], column, db) for column in table_columns[1:]}
    fields['submit'] = SubmitField("Insertar")
    return type("DynamicForm", (FlaskForm,), fields)


# * Define si cada columna debe de recibir datos por un <input> o un <select>.
# * En caso de ser por un <input>, tambien define cuál tipo.
def get_field_class(column_data, column, db):
    # * Si la columna tiene una llave foránea, crea un <select>
    if len(column_data["foreign_key"]) > 0:

        # * Para hacer la FK subscripteable
        foreign_keys = list(column_data["foreign_key"])

        # * Extraemos el nombre de la tabla referenciada y su contenido
        foreign_table = foreign_keys[0].column.table.name
        foreign_table_body = db.select_all(db[foreign_table])

        # * Las elecciones que tendrá el usuario en el <select>
        choices = []

        for registry in foreign_table_body:
            choice_value = registry[0]  # ? El valor "real" a subir en el form será el id
            choice_show_name = registry[1]  # ? El nombre o valor con el que se muestra en front
            choice = (choice_value, f"id: {choice_value} ({choice_show_name})")
            choices.append(choice)

        return SelectField(column, choices=choices, validators=[DataRequired()])

    # * Si la columna no es una llave foránea, crea un <input> de acuerdo
    # * al tipo de dato de la columna dentro de la base de datos.

    float_types = ["FLOAT", "REAL", "DOUBLE PRECISION", "DECIMAL", "NUMERIC"]
    date_types = ["DATE", "DATETIME"]

    if "INTEGER" in column_data["type"]:
        return IntegerField(column, validators=[DataRequired()])
    elif any(float_type in column_data["type"] for float_type in float_types):
        return DecimalField(column, validators=[DataRequired()])
    elif any(date_type in column_data["type"] for date_type in date_types):
        return DateField(column, validators=[DataRequired()])
    else:
        numbers = findall(r'\d+', column_data["type"])
        max_length = int(''.join(numbers)) if numbers else 0
        return StringField(column, validators=[DataRequired(), Length(max=max_length)])


