from os import path
db_path = path.join(path.dirname(__file__), 'proyecto-hormigas.db')
db_uri = 'sqlite:///{}'.format(db_path)

basedir = path.abspath(path.dirname(__file__))
class Config(object):
    SECRET_KEY = 'AFC8B45DFABF55383348BFFC2F7D6'
    SQLALCHEMY_DATABASE_URI = db_uri
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
