import secrets

class Config(object):
    SECRET_KEY = secrets.token_hex(16)
    DB_USERNAME = 'root'
    DB_PASSWORD = 'root'
    DB_LOCATION = 'flask-db'
    DB_DATABASE = 'users'