from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

#################### Tablas many to many y enum class ###############################
class Temporada(enum.Enum):
    seca = "seca"
    humeda = "humeda"

participantes = db.Table(
    'participante_transecto',
    db.Column('transecto_id', db.String(255), db.ForeignKey('transecto.transecto')),
    db.Column('participante_id', db.Integer, db.ForeignKey('participante.id'))
)
###################### Definicion de Tablas ########################
class Taxon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_cientifico = db.Column(db.String(150), unique=True)
    genero = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(50))
    infra_rank = db.Column(db.String(10))
    sub_especie = db.Column(db.String(50))
    autor = db.Column(db.String(100))
    __table_args__ = tuple(db.UniqueConstraint('genero', 'especie', 'sub_especie',
                                      name='uix_Taxon_genero_especie_sub_especie'))
    #def __init__(self, genero):
        #self.genero = genero
        #self.especie = especie
    def build_sciname(self):
        if self.sub_especie:
            self.infra_rank = 'ssp.'
            subname = "'{}' '{}'".format('ssp.', self.sub_especie)
        else:
            subname = ""
        self.nombre_cientifico = " ".join([self.genero, self.especie, subname]).strip()

    def __repr__(self):
        return "<Taxon '{}'>".format(self.nombre_cientifico)

class TaxonQuadrat(db.Model):
    __tablename__ = 'taxon_quadrat'
    quadrat_id = db.Column(db.Integer, db.ForeignKey('quadrat.id'), primary_key=True)
    taxon_id = db.Column(db.Integer, db.ForeignKey('taxon.id'), primary_key=True,info={'form_field_class':SelectField})
    #info={'choices':[(taxon.id, taxon.nombre_cientifico) for taxon in Taxon.query.order_by('nombre_cientifico')]})
    abundancia = db.Column(db.Integer)
    vial = db.Column(db.String(3))
    alfiler = db.Column(db.Integer)
    alcohol = db.Column(db.Integer)
    quadrat = db.relationship(
        'Quadrat',
        backref='taxon_aso'
    )
    taxon = db.relationship(
        'Taxon',
        backref='quadrat_aso'
    )

class ParqueUrbano(db.Model):
    #__tablename__ = 'parque_urbano'

    id = db.Column(db.Integer, primary_key=True)
    parque = db.Column(db.String(100), unique=True)
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
    id = db.Column(db.Integer, primary_key=True)
    transecto = db.Column(db.String(50), unique=True, nullable=False)
    temporada = db.Column(db.Enum(Temporada), info={'coerce':str})
    fecha = db.Column(db.Date)
    hora_inicial = db.Column(db.Time)
    hora_final = db.Column(db.Time)
    temperatura = db.Column(db.Numeric(10, 2))
    humedad = db.Column(db.Numeric(10, 2))
    velocidad_viento = db.Column(db.Numeric(10, 2))
    observaciones = db.Column(db.Text)
    parque_id = db.Column(db.Integer, db.ForeignKey('parque_urbano.id'))

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

    #def __init__(self, transecto):
    #    self.transecto = transecto
    def __repr__(self):
        return "<Transecto '{}'>".format(self.transecto)

class Quadrat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quadrat = db.Column(db.String(10))
    temperatura_suelo = db.Column(db.Numeric(10, 2))
    ph_suelo = db.Column(db.Numeric(10, 2))
    ramas = db.Column(db.Boolean())
    profundidad_hojarasca = db.Column(db.Numeric(10, 2))
    transecto_id = db.Column(db.Integer, db.ForeignKey('transecto.id'))
    taxa = db.relationship(
        'Taxon',
        secondary='taxon_quadrat',
        viewonly=True
    )
    __table_args__ = tuple(db.UniqueConstraint('quadrat', 'transecto_id',
                                               name='uix_Taxon_genero_especie_sub_especie'))
    #def __init__(self, quadrat):
    #    self.quadrat = quadrat

    def __repr__(self):
        return "<Quadrat '{}'>".format(self.quadrat)


class Participante(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellidos = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellidos = apellido

    def __repr__(self):
        return "<'{}' '{}'>".format(self.nombre, self.apellidos)
        