from flask_security import RegisterForm
from flask_security.forms import EqualTo
from wtforms import StringField, SelectField, HiddenField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers
from flask_babel import _
from app.models import Calle, Colonia, Municipio, Genero


class ExtendedRegisterForm(RegisterForm):
    us_phone_number = StringField(_("Numero telefónico"), [DataRequired()])
    num_int = IntegerField('Número Interior', validators=[])
    num_ext = IntegerField('Número Exterior', validators=[DataRequired()])
    id_calle = SelectField('Calle', choices=[], validators=[DataRequired()])
    colonia = SelectField('Colonia', choices=[], validators=[DataRequired()])
    municipio = SelectField('Municipio', choices=[], validators=[DataRequired()])
    id_genero = SelectField('Genero', choices=[], validators=[DataRequired()])
    def __init__(self, *args, **kwargs):
        super(ExtendedRegisterForm, self).__init__(*args, **kwargs)
        self.municipio.choices = [(m.id, m.nombre_municipio) for m in Municipio.query.all()]
        self.colonia.choices = [(c.id, c.nombre_colonia) for c in Colonia.query.all()]
        self.id_calle.choices = [(ca.id, ca.nombre_calle) for ca in Calle.query.all()]
        self.id_genero.choices = [(g.id, g.nombre_genero) for g in Genero.query.all()]

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


