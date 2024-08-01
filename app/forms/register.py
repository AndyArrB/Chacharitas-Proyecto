from flask_security import RegisterForm
from flask_security.forms import EqualTo
from wtforms import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers
from flask_babel import _

class ExtendedRegisterForm(RegisterForm):
    us_phone_number = StringField(_("Phone Number"), [DataRequired()])

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