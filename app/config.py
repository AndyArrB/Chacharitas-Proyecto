# * Flask: Activa el modo desarrollador por defecto
DEBUG = True

# * Flask: Son claves necesarias para la protección contra CSRF
SECRET_KEY = "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
SECURITY_PASSWORD_SALT = "146585145368132386173505678016728509634"

# * Flask-Security: Las cookies de usuario solo se envian si el sitio
# * quien la creó inicia la solicitud
REMEMBER_COOKIE_SAMESITE = "strict"
SESSION_COOKIE_SAMESITE = "strict"
UPLOAD_FOLDER = 'app/static/images'

# * Flask-Security: Permite asignar roles a usuarios
SECURITY_USERNAME_ENABLE = True
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_JOIN_USER_ROLES = True

# * Flask-Mail:
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "axolotlscriptjs@gmail.com"
MAIL_PASSWORD = "gvig lznc gufh fgac"
MAIL_DEFAULT_SENDER = "axolotlscriptjs@gmail.com"

SECURITY_EMAIL_SENDER = "axolotlscriptjs@gmail.com"
SECURITY_REGISTERABLE = True
SECURITY_CONFIRMABLE = True
SECURITY_RECOVERABLE = True
SECURITY_AUTO_LOGIN_AFTER_CONFIRM = True

LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}
BABEL_DEFAULT_LOCALE = 'es'
BABEL_DEFAULT_TIMEZONE = 'UTC'
SECURITY_I18N_DIRNAME = ["builtin", "translations/es_ES/LC_MESSAGES"]


#SECURITY_REGISTER_USER_TEMPLATE = "dummy.html"
#SECURITY_POST_REGISTER_VIEW = "dummy.html"
#SECURITY_REGISTER_URL = "dummy.html"
#SECURITY_USERNAME_REQUIRED = True