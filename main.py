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

participantes = db.Table(
    'participante_transecto',
    db.Column('transecto_id', db.String(255), db.ForeignKey('transecto.transecto')),
    db.Column('participante_id', db.Integer, db.ForeignKey('participante.id'))
)
###################### Definicion de Tablas ########################


class ParqueUrbano(db.Model):
    __tablename__ = 'parque_urbano'
    parque = db.Column(db.String(255), primary_key=True)
    transectos = db.relationship(
        'Transecto',
        backref='parque',
        lazy='dynamic'
    )
    def __init__(self, parque):
        self.parque = parque
    def __repr__(self):
        return "<Parque '{}'>".format(self.parque)

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
    parque_id = db.Column(db.String(255), db.ForeignKey('parque_urbano.parque'))
    quadrats_tr = db.relationship(
        'Quadrat',
        backref='transecto',
        lazy='dynamic'
    )
    participantes = db.relationship(
        'Participante',
        secondary=participantes,
        backref=db.backref('transectos', lazy='dynamic')
    )

    def __init__(self, transecto):
        self.transecto = transecto
    def __repr__(self):
        return "<Transecto '{}'>".format(self.transecto)

class Quadrat(db.Model):
    quadrat = db.Column(db.String(10), primary_key=True)
    transecto_id = db.Column(db.String(255), db.ForeignKey('transecto.transecto'), primary_key=True)
    temperatura_suelo = db.Column(db.Float())
    ph_suelo = db.Column(db.Float())
    ramas = db.Column(db.Boolean())
    profundidad_hojarasca = db.Column(db.Float)
    taxa = db.relationship(
        'TaxonQuadrat',
        backref='quadrat',
        lazy='dynamic'
    )

    def __init__(self, transecto, quadrat):
        self.transecto = transecto
        self.quadrat = quadrat

    def __repr__(self):
        return "<Quadrat '{0}'-'{1}>".format(self.transecto, self.quadrat)

class Taxon(db.Model):
    nombre_cientifico = db.Column(db.String(10), primary_key=True)
    genero = db.Column(db.String(255))
    especie = db.Column(db.String(255))
    autor = db.Column(db.String(255))
    quadrats = db.relationship(
        'TaxonQuadrat',
        backref='taxon',
        lazy='dynamic'
    )
    def __init__(self, genero, especie=""):
        self.genero = genero
        self.especie = especie
        self.nombre_cientifico = " ".join([self.genero, self.especie]).strip()

    def __repr__(self):
        return "<Taxon '{}'>".format(self.nombre_cientifico)

class TaxonQuadrat(db.Model):
    __tablename__ = 'taxon_quadrat'
    quadrat_id = db.Column(db.String(10), db.ForeignKey('quadrat.quadrat'), primary_key=True)
    taxon_id = db.Column(db.String(255), db.ForeignKey('taxon.nombre_cientifico'), primary_key=True)
    abundancia = db.Column(db.Integer())
    quadrat = db.relationship(
        'Quadrat',
        backref='taxa',
        lazy='dynamic'
    )
    taxon = db.relationship(
        'Taxon',
        backref='quadrats'
    )

class Participante(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(255))
    apellidos = db.Column(db.String(255))

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellidos = apellido

    def __repr__(self):
        return "<'{}' '{}'>".format(self.nombre, self.apellidos)

if __name__ == '__main__':
    app.run()
