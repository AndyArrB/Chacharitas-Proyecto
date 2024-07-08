from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired, ValidationError
import phonenumbers

class ExtendedRegisterForm(RegisterForm):
    us_phone_number = StringField("Phone Number", [DataRequired()])
    username = StringField("Username", [DataRequired()])

    def validate_us_phone_number(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+52"+field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')

