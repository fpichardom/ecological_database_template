from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
import enum
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
#################### Tablas many to many y enum ###############################
class Temporada(enum.Enum):
    seca = "seca"
    humeda = "humeda"

especies = db.Table(
    'quadrat_especie',
    db.Column('quadrat_id', db.String(10), db.ForeignKey('quadrat.quadrat')),
    db.Column('especie_id', db.String(255), db.ForeignKey('taxon.nombre_cientifico'))
)
participantes = db.Table(
    'participante_transecto',
    db.Column('transecto_id', db.String(255), db.ForeignKey('transecto.transecto')),
    db.Column('participante_id', db.Integer, db.ForeignKey('participante.id'))
)
###################### Definicion de Tablas ########################

class ParqueUrbano(db.Model):
    __tablename__ = 'parque_urbano'
    parque = db.Column(db.String(255), primary_key=True)

class Transecto(db.Model):
    transecto = db.Column(db.String(255), primary_key=True)
    temporada = db.Column(db.Enum(Temporada))
    fecha = db.Column(db.Date())
    hora_inicial = db.Column(db.Time())
    hora_final = db.Column(db.Time())
    temperatura = db.Column(db.Float())
    humedad = db.Column(db.Float())
    velocidad_viento = db.Column(db.Float())
    observaciones = db.Column(db.Text())
    id_parque = db.Column(db.String(255), db.ForeignKey('parque_urbano.parque'))
    participantes = db.relationship(
        'Participante',
        secondary=participantes,
        backref=db.backref('transectos', lazy='dynamic')
    )

class Quadrat(db.Model):
    quadrat = db.Column(db.String(10), primary_key=True)
    transecto = db.Column(db.String(255), db.ForeignKey('transecto.transecto'), primary_key=True)
    temperatura_suelo = db.Column(db.Float())
    ph_suelo = db.Column(db.Float())
    ramas = db.Column(db.Boolean())
    profundidad_hojarasca = db.Column(db.Float)
    especies = db.relationship(
        'Taxon',
        secondary=especies,
        backref=db.backref('quadrats', lazy='dynamic')
    )
class Taxon(db.Model):
    nombre_cientifico = db.Column(db.String(10), primary_key=True)
    genero = db.Column(db.String(255))
    especie = db.Column(db.String(255))
    autor = db.Column(db.String(255))
    def __init__(self, genero, especie=""):
        self.genero = genero
        self.especie = especie
        self.nombre_cientifico = " ".join(self.genero, self.especie).strip()

class Participante(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(255))
    Apellidos = db.Column(db.String(255))


if __name__ == '__main__':
    app.run()
