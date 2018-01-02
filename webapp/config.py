import os
##For SQLITE
#db_path = os.path.join(path.dirname(__file__), 'proyecto-hormigas.db')
#db_uri = 'sqlite:///{}'.format(db_path)
#basedir = path.abspath(path.dirname(__file__))
## for MYSQL
db_uri = os.environ.get('FLASKDB')

class Config(object):
    SECRET_KEY = 'AFC8B45DFABF55383348BFFC2F7D6'
    SQLALCHEMY_DATABASE_URI = db_uri
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
