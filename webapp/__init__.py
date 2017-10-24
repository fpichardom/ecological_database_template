from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory
from wtforms import SelectField, StringField, FormField
from flask_bootstrap import Bootstrap
from wtforms import (StringField, IntegerField, BooleanField, TextAreaField,
                    SelectField, DecimalField)
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, Optional, InputRequired
from config import Config
import enum
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
Bootstrap(app)
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
    temporada = db.Column(db.Enum(Temporada), info = {'coerce':str})
    fecha = db.Column(db.Date)
    hora_inicial = db.Column(db.Time)
    hora_final = db.Column(db.Time)
    temperatura = db.Column(db.Numeric(10,2))
    humedad = db.Column(db.Numeric(10,2))
    velocidad_viento = db.Column(db.Numeric(10,2))
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
    temperatura_suelo = db.Column(db.Numeric(10,2))
    ph_suelo = db.Column(db.Numeric(10,2))
    ramas = db.Column(db.Boolean())
    profundidad_hojarasca = db.Column(db.Numeric(10,2))
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
        



##################################Forms#########################################

###########Wtforms-Alchemy forms#################

BaseModelForm = model_form_factory(FlaskForm)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

class ParqueForm(ModelForm):
    class Meta:
        model = ParqueUrbano
class TransectoForm(ModelForm):
    class Meta:
        model = Transecto
        # field_args ={
        #     'temporata':{
        #         'validators':[Optional()],
        #         'choices':[('seca', 'seca'), ('humeda', 'humeda')],
        #         'coerce': str
        #     }
        # }
class QuadratForm(ModelForm):
    class Meta:
        model = Quadrat
# class TaxonQuadratForm(ModelForm):
#     class Meta:
#         model = TaxonQuadrat
#         include = ['taxon_id']

class TaxonForm(ModelForm):
    class Meta:
        model = Taxon

class ParticipanteForm(ModelForm):
    class Meta:
        model = Participante

class ParticipanteSubForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired()])
    apellidos = StringField('Apellidos', validators=[InputRequired()])

class ParticipanteForm(FlaskForm):
    participante = FormField(ParticipanteSubForm)

########Wtforms Forms ###############

# class TransectoForm(FlaskForm):
#     transecto = StringField('Transecto', validators=[DataRequired(), Length(max=10)])
#     temporada = SelectField('Temporada', choices=[('seca', 'seca'), ('humeda', 'humeda')])
#     fecha = DateField('Fecha', format='%Y-%m-%d', validators=[Optional()])
#     hora_inicial = TimeField('Hora Inicial', format='%H:%M', validators=[Optional()])
#     hora_final = TimeField('Hora Final', format='%H:%M', validators=[Optional()])
#     temperatura = DecimalField('Temperatura', validators=[Optional()])
#     humedad = DecimalField('Humedad', validators=[Optional()])
#     velocidad_viento = DecimalField('Velocidad Viento', validators=[Optional()])
#     observaciones = TextAreaField('Observaciones', validators=[Optional()])

class TaxonQuadratForm(FlaskForm):
    #quadrat_id = IntegerField('Quadrat',validators=[DataRequired()])
    taxon_id = SelectField('Taxon', validators=[DataRequired()], coerce=int)
    abundancia = IntegerField('Abundancia', validators=[Optional()])
    vial = StringField('Vial', validators=[Length(max=3)])
    alfiler = IntegerField('Alfiler', validators=[Optional()])
    alcohol = IntegerField('Alcohol', validators=[Optional()])

# class QuadratForm(FlaskForm):
#     quadrat = StringField('Quadrat', validators=[DataRequired(), Length(max=10)])
#     temperatura_suelo = DecimalField('Temperatura Suelo', validators=[Optional()])
#     ramas = BooleanField('Ramas')
#     profundidad_hojarasca = DecimalField('Profundidad Hojarasca', validators=[Optional()])

# class ParqueForm(FlaskForm):
#     parque = StringField('Parque Urbano', validators=[DataRequired(), Length(max=100)])

####################### Views #####################
@app.route('/', methods=['GET', 'POST'])
#@app.route('/parque_urbano')
def home():
    form = ParqueForm()
    if form.validate_on_submit():
        new_parque = ParqueUrbano(form.parque.data)
        db.session.add(new_parque)
        db.session.commit()
    parques = ParqueUrbano.query.all()
    return render_template(
        'parque.html',
        parques=parques,
        form=form)

@app.route('/transectos/<int:parque_id>', methods=['GET', 'POST'])
def transectos(parque_id):
    form = TransectoForm()
    #form.temporada.choices=[('seca','seca'),('humeda','humeda')]
    transectos = Transecto.query.filter_by(parque_id=parque_id)
    parque = ParqueUrbano.query.get_or_404(parque_id)

    if form.validate_on_submit():
        new_tr = Transecto()
        #new_tr = Transecto(form.transecto.data)
        new_tr.parque_id = parque_id
        new_tr.transecto = form.transecto.data
        new_tr.temporada = form.temporada.data
        new_tr.fecha = form.fecha.data
        new_tr.hora_inicial = form.hora_inicial.data
        new_tr.hora_final = form.hora_final.data
        new_tr.temperatura = form.temperatura.data
        new_tr.humedad = form.humedad.data
        new_tr.velocidad_viento = form.velocidad_viento.data
        new_tr.observaciones = form.observaciones.data

        db.session.add(new_tr)
        db.session.commit()

    return render_template(
        'transectos.html',
        transectos=transectos,
        parque=parque,
        form=form)

@app.route('/quadrats/<int:tr_id>', methods=['GET','POST'])
def quadrats(tr_id):
    form = QuadratForm()
    quadrats = Quadrat.query.filter_by(transecto_id=tr_id)
    transecto = Transecto.query.get(tr_id)
    parque = transecto.parque

    if form.validate_on_submit():
        new_qdt = Quadrat()
        new_qdt.transecto_id = tr_id
        new_qdt.quadrat = form.quadrat.data
        new_qdt.temperatura_suelo = form.temperatura_suelo.data
        new_qdt.ramas = form.ramas.data
        new_qdt.profundidad_hojarasca = form.profundidad_hojarasca.data

        db.session.add(new_qdt)
        db.session.commit()


    return render_template(
        'quadrats.html',
        quadrats=quadrats,
        transecto=transecto,
        parque=parque,
        form=form)

@app.route('/quadrat/<int:qdt_id>', methods=['GET', 'POST'])
def quadrat(qdt_id):
    form = TaxonQuadratForm()
    form.taxon_id.choices = [(taxon.id, taxon.nombre_cientifico) for taxon in Taxon.query.order_by('nombre_cientifico')]
    quadrat = Quadrat.query.get_or_404(qdt_id)
    #taxa = Taxon.query.all()
    if form.validate_on_submit():
        new_bind = TaxonQuadrat()
        new_bind.quadrat_id = qdt_id
        new_bind.taxon_id = form.taxon_id.data
        new_bind.abundancia = form.abundancia.data
        new_bind.vial = form.vial.data.upper()
        new_bind.alfiler = form.alfiler.data
        new_bind.alcohol = form.alcohol.data
        if not TaxonQuadrat.query.filter_by(quadrat_id=qdt_id, taxon_id=form.taxon_id.data).all():
            db.session.add(new_bind)
            db.session.commit()
    asos = TaxonQuadrat.query.filter_by(quadrat_id=qdt_id).all()
    return render_template(
        'quadrat.html',
        form=form,
        quadrat=quadrat,
        asos=asos
    )

@app.route('/taxa', methods=['GET', 'POST'])
def taxon():
    form = TaxonForm()
    if form.validate_on_submit():
        new_taxon = Taxon()
        new_taxon.genero = form.genero.data
        new_taxon.especie = form.especie.data
        new_taxon.sub_especie = form.sub_especie.data
        new_taxon.build_sciname()
        db.session.add(new_taxon)
        db.session.commit()
    taxa = Taxon.query.order_by('nombre_cientifico').all()
    return render_template(
        'taxa.html',
        taxa=taxa,
        form=form
    )

@app.route('/participantes', methods=['GET', 'POST'])
def participante():
    form = ParticipanteForm()
    if form.validate_on_submit():
        #new_parti = Participante()
        new_parti = form.participante.data
        return new_parti
        #db.session.add(new_parti)
        #db.session.commit()
    participantes = Participante.query.order_by('nombre').all()
    return render_template(
        'participantes.html',
        participantes=participantes,
        form=form
    )
if __name__ == '__main__':
    app.run()
