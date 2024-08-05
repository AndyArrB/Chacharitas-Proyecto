from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileAllowed, FileRequired

from app import User
from app.models import DetalleTamaño, Categoria, Color, Marca, Genero, Material


class ProductoForm(FlaskForm):
    nombre_producto = StringField('Nombre del Producto', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio = IntegerField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    id_color = SelectField('Color', coerce=int, validators=[DataRequired()])
    id_categoria = SelectField('Categoría', coerce=int, validators=[DataRequired()])
    id_detalle_tamaños = SelectField('Detalle Tamaños', coerce=int, validators=[DataRequired()])
    id_marca = SelectField('Marca', coerce=int, validators=[DataRequired()])
    id_material = SelectField('Material', coerce=int, validators=[DataRequired()])
    id_genero = SelectField('Género', coerce=int, validators=[DataRequired()])
    imagen = FileField('Imagen del Producto', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Solo se permiten imágenes JPG y PNG')])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.id_color.choices = [(c.id, c.nombre_color) for c in Color.query.all()]
        self.id_categoria.choices = [(cat.id, cat.tipo_categoria) for cat in Categoria.query.all()]
        self.id_detalle_tamaños.choices = [(dt.id, dt.tamaño) for dt in DetalleTamaño.query.all()]
        self.id_marca.choices = [(m.id, m.nombre_marca) for m in Marca.query.all()]
        self.id_material.choices = [(mat.id, mat.nombre_material) for mat in Material.query.all()]
        self.id_genero.choices = [(g.id, g.nombre_genero) for g in Genero.query.all()]
