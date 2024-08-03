from flask_security import RegisterForm
from flask_security.forms import EqualTo
from wtforms import StringField, SelectField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers
from flask_babel import _
from app.models import Calle, Colonia, Municipio

class ExtendedRegisterForm(RegisterForm):
    us_phone_number = StringField(_("Phone Number"), [DataRequired()])
    numero_interior = StringField('Número Interior', validators=[DataRequired()])
    numero_exterior = StringField('Número Exterior', validators=[DataRequired()])
    calle = SelectField('Calle', choices=[], validators=[DataRequired()])
    colonia = SelectField('Colonia', choices=[], validators=[DataRequired()])
    municipio = SelectField('Municipio', choices=[], validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        self.calle.choices = [(c.id, c.nombre_calle) for c in Calle.query.all()]
        self.colonia.choices = [(c.id, c.nombre_colonia) for c in Colonia.query.all()]
        self.municipio.choices = [(m.id, m.nombre_municipio) for m in Municipio.query.all()]

    def validate_us_phone_number(form, field):
        if len(field.data) > 16:
            raise ValidationError(_('Número demasiado largo'))
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError(_('Número inválido'))
        except:
            input_number = phonenumbers.parse("+52" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError(_('Número inválido'))