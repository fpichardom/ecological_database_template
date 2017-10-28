from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()

#################### Tablas many to many y enum class ###############################
class Temporada(enum.Enum):
    seca = "seca"
    humeda = "humeda"

participantes = db.Table(
    'participante_transecto',
    db.Column('transecto_id', db.Integer, db.ForeignKey('transecto.transecto')),
    db.Column('participante_id', db.Integer, db.ForeignKey('participante.id'))
)
###################### Definicion de Tablas ########################
class Taxon(db.Model):
    __tablename__ = 'taxon'

    id = db.Column(db.Integer, primary_key=True)
    nombre_cientifico = db.Column(db.String(150), unique=True)
    genero = db.Column(db.String(50), nullable=False)
    especie = db.Column(db.String(50))
    infra_rank = db.Column(db.String(10))
    sub_especie = db.Column(db.String(50))
    autor = db.Column(db.String(100))

    #Constraint taxa to have a unique name until the level of subspecies
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
    
    abundancia = db.Column(db.Integer)
    vial = db.Column(db.String(3)) # Vial code
    alfiler = db.Column(db.Integer)
    alcohol = db.Column(db.Integer)

    #Foreign keys and relationships
    quadrat_id = db.Column(db.Integer, db.ForeignKey('quadrat.id'), primary_key=True)
    taxon_id = db.Column(db.Integer, db.ForeignKey('taxon.id'), primary_key=True)#,info={'form_field_class':SelectField}
    #info={'choices':[(taxon.id, taxon.nombre_cientifico) for taxon in Taxon.query.order_by('nombre_cientifico')]})
    
    quadrat = db.relationship(
        'Quadrat',
        backref='taxon_aso'
    )
    taxon = db.relationship(
        'Taxon',
        backref='quadrat_aso'
    )

class ParqueUrbano(db.Model):
    __tablename__ = 'parque_urbano'

    id = db.Column(db.Integer, primary_key=True)
    parque = db.Column(db.String(100), unique=True)

    #Relationships
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
    __tablename__ ='transecto'

    id = db.Column(db.Integer, primary_key=True)
    transecto = db.Column(db.String(50), unique=True, nullable=False)
    temporada = db.Column(db.Enum(Temporada))#for Wtforms-Alchemy model, info={'coerce':str}
    fecha = db.Column(db.Date)
    hora_inicial = db.Column(db.Time)
    hora_final = db.Column(db.Time)
    temperatura = db.Column(db.Numeric(10, 2))
    humedad = db.Column(db.Numeric(10, 2))
    velocidad_viento = db.Column(db.Numeric(10, 2))
    observaciones = db.Column(db.Text)

    #Foreign keys and relationships
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
    __tablename__ = 'quadrat'
    id = db.Column(db.Integer, primary_key=True)
    quadrat = db.Column(db.String(10))
    temperatura_suelo = db.Column(db.Numeric(10, 2))
    ph_suelo = db.Column(db.Numeric(10, 2))
    ramas = db.Column(db.Boolean())
    profundidad_hojarasca = db.Column(db.Numeric(10, 2))

    #Foreign keys and relationships
    transecto_id = db.Column(db.Integer, db.ForeignKey('transecto.id'))
    taxa = db.relationship(
        'Taxon',
        secondary='taxon_quadrat',
        viewonly=True
    )

    #def __init__(self, quadrat):
    #    self.quadrat = quadrat

    #Constrait only if the quadrat name is unique for the transect
    __table_args__ = tuple(db.UniqueConstraint(
        'quadrat', 'transecto_id', name='uix_Quadrat_quadrat_transecto_id'))
    
    def __repr__(self):
        return "<Quadrat '{}'>".format(self.quadrat)


class Participante(db.Model):
    __tablename__='participante'

    id = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellidos = db.Column(db.String(255), nullable=False)

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellidos = apellido

    # Constraint only for small applications where names of participants are expected to be unique
    __table_args__ = tuple(db.UniqueConstraint(
        'nombre', 'apellido', name='uix_Participante_nombre_apellido'))
    
    def __repr__(self):
        return "<'{}' '{}'>".format(self.nombre, self.apellidos)
        