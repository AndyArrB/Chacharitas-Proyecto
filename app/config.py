# * Flask: Activa el modo desarrollador por defecto
DEBUG = True

# * Flask: Son claves necesarias para múltiples aspectos
SECRET_KEY = "pf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
SECURITY_PASSWORD_SALT = "146585145368132386173505678016728509634"

# * Las cookies de usuario solo se envian si el sitio quien la creó
# * inicia la solicitud
REMEMBER_COOKIE_SAMESITE = "strict"
SESSION_COOKIE_SAMESITE = "strict"

# * La conexión con la cual se inicializa la base de datos
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://@localhost/Chacharitas_2?trusted_connection=yes&driver=ODBC+Driver+18+for+SQL+Server&Encrypt=no"

# *
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

#SECURITY_REGISTER_USER_TEMPLATE = "dummy.html"
#SECURITY_POST_REGISTER_VIEW = "dummy.html"
#SECURITY_REGISTER_URL = "dummy.html"
#SECURITY_USERNAME_REQUIRED = True