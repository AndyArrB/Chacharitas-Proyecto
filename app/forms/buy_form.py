from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Regexp
from datetime import datetime
from app.models import Producto  # Assuming Producto is the model for products

class PaymentForm(FlaskForm):
    card_number = StringField('Número de tarjeta', validators=[DataRequired(), Length(min=16, max=16),
                                                               Regexp(r'^\d{16}$',
                                                                      message="El número de tarjeta debe contener solo números.")])
    card_holder = StringField('Titular de la tarjeta', validators=[DataRequired(), Length(max=100)])

    # Select fields for expiration date
    current_year = datetime.now().year
    month_choices = [(str(i), f'{i:02d}') for i in range(1, 13)]
    year_choices = [(str(i), str(i)) for i in range(current_year, current_year + 11)]

    expiration_month = SelectField('Mes de Expiración', choices=month_choices, validators=[DataRequired()])
    expiration_year = SelectField('Año de Expiración', choices=year_choices, validators=[DataRequired()])

    cvv = IntegerField('CVV', validators=[DataRequired(), NumberRange(min=100, max=999)])
    amount = IntegerField('Amount', validators=[DataRequired()])
    submit = SubmitField('Realizar compra')

    def __init__(self, id_producto, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        product = Producto.query.get(id_producto)
        if product:
            self.amount.validators.append(NumberRange(min=1, max=product.cantidad))