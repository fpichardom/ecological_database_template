from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, BooleanField, TextAreaField,
                    SelectField, DecimalField, FormField, SubmitField)
from wtforms.fields.html5 import DateField
from wtforms_components import TimeField
from wtforms.validators import InputRequired, Length, Optional
from wtforms_alchemy import Unique
from .models import Transecto

### To enable wtforms_alchemy #######

#from wtforms_alchemy import model_form_factory
##############################################


##################################Forms#########################################

######## Standard Wtforms Forms ###############

class ParqueForm(FlaskForm):
    parque = StringField('Parque Urbano', validators=[InputRequired(), Length(max=100)])

class TransectoForm(FlaskForm):
    transecto = StringField('Transecto', validators=[InputRequired(), Length(max=50)])
    temporada = SelectField('Temporada', choices=[('seca', 'seca'), ('humeda', 'humeda')])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[Optional()])
    hora_inicial = TimeField('Hora Inicial', format='%H:%M', validators=[Optional()])
    hora_final = TimeField('Hora Final', format='%H:%M', validators=[Optional()])
    temperatura = DecimalField('Temperatura', validators=[Optional()])
    humedad = DecimalField('Humedad', validators=[Optional()])
    velocidad_viento = DecimalField('Velocidad Viento', validators=[Optional()])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])

class QuadratForm(FlaskForm):
    quadrat = StringField('Quadrat', validators=[InputRequired(), Length(max=10)])
    temperatura_suelo = DecimalField('Temperatura Suelo', validators=[Optional()])
    ramas = BooleanField('Ramas')
    profundidad_hojarasca = DecimalField('Profundidad Hojarasca', validators=[Optional()])




class TaxonQuadratForm(FlaskForm):
    #quadrat_id = IntegerField('Quadrat',validators=[InputRequired()])
    taxon_id = SelectField('Taxon', validators=[InputRequired()], coerce=int)
    abundancia = IntegerField('Abundancia', validators=[Optional()])
    vial = StringField('Vial', validators=[Length(max=3), Optional()])
    alfiler = IntegerField('Alfiler', validators=[Optional()])
    alcohol = IntegerField('Alcohol', validators=[Optional()])



class ParticipanteSubForm(FlaskForm):
    nombre = StringField('Nombre', validators=[InputRequired()])
    apellidos = StringField('Apellidos', validators=[InputRequired()])

class ParticipanteForm(FlaskForm):
    participante = FormField(ParticipanteSubForm)


class TaxonSubForm(FlaskForm):
    genero = StringField('Género', validators=[InputRequired(), Length(max=50)])
    especie = StringField('Especie', validators=[Optional(), Length(max=50)], default='sp.')
    sub_especie = StringField('Sub-especie', validators=[Optional(), Length(max=50)])
    autor = StringField('Autor', validators=[Optional, Length(max=100)])


class TaxonForm(FlaskForm):
    taxon = FormField(TaxonSubForm)


    #infra_rank = SelectField('Infra Rank', validators=[Optional()], choices=[('ssp.','ssp.'),()])
###########Wtforms-Alchemy forms#################

# BaseModelForm = model_form_factory(FlaskForm)

# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session

# class ParqueForm(ModelForm):
#     class Meta:
#         model = ParqueUrbano
# class TransectoForm(ModelForm):
#     class Meta:
#         model = Transecto
#         # field_args ={
#         #     'temporata':{
#         #         'validators':[Optional()],
#         #         'choices':[('seca', 'seca'), ('humeda', 'humeda')],
#         #         'coerce': str
#         #     }
#         # }
# class QuadratForm(ModelForm):
#     class Meta:
#         model = Quadrat
# # class TaxonQuadratForm(ModelForm):
# #     class Meta:
# #         model = TaxonQuadrat
# #         include = ['taxon_id']

# class TaxonForm(ModelForm):
#     class Meta:
#         model = Taxon

# class ParticipanteForm(ModelForm):
#     class Meta:
#         model = Participante



