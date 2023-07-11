SECRET_KEY = 'SDJKFKLASDJFKLSJADFKL'
DB_HOST = ''
DB_PORT = 3306
DB_NAME = ''
DB_USER = ''
DB_PWD  = ''
TEMPLATES_AUTO_RELOAD = True
try:
    from projects.local_settings import *
except ImportError:
    pass
SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
SQLALCHEMY_ECHO = True