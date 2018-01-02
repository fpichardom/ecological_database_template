from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, BooleanField, TextAreaField,
                     SelectField, DecimalField, FormField, SubmitField,
                     FieldList, SelectMultipleField)
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
    parque = StringField('Level 1 Locality', validators=[InputRequired(), Length(max=100)])
    submit = SubmitField('Add')

class TransectoForm(FlaskForm):
    transecto = StringField('Level 2 Locality', validators=[InputRequired(), Length(max=50)])
    temporada = SelectField('Season', choices=[("", ""), ('wet', 'wet'), ('dry', 'dry')])
    fecha = DateField('Date', format='%Y-%m-%d', validators=[Optional()])#, description="yyyy-mm-dd"
    hora_inicial = TimeField('Start Time', format='%H:%M', validators=[Optional()],description="HH:MM")
    hora_final = TimeField('End Time', format='%H:%M', validators=[Optional()])#, description="HH:MM"
    temperatura = DecimalField('Temperature', validators=[Optional()])
    humedad = DecimalField('Humidity', validators=[Optional()])
    velocidad_viento = DecimalField('Wind Speed', validators=[Optional()])
    observaciones = TextAreaField('Observations', validators=[Optional()])
    participantes = SelectMultipleField('Agents', validators=[Optional()], coerce=int)
    #participantes = FieldList(SelectField('Participante',choices=None), min_entries=2)
    submit = SubmitField('Add')

class QuadratForm(FlaskForm):
    quadrat = StringField('Level 3 Locality', validators=[InputRequired(), Length(max=10)])
    temperatura_suelo = DecimalField('Soil Temperature', validators=[Optional()])
    ramas = BooleanField('Branches')
    profundidad_hojarasca = DecimalField('Leaf Litter Depth', validators=[Optional()])
    submit = SubmitField('Add')



class TaxonQuadratForm(FlaskForm):
    #quadrat_id = IntegerField('Quadrat',validators=[InputRequired()])
    taxon_id = SelectField('Taxon', validators=[InputRequired()], coerce=int)
    abundancia = IntegerField('Abundance', validators=[Optional()])
    vial = StringField('Vial', validators=[Length(max=3), Optional()])
    alfiler = IntegerField('Pinned', validators=[Optional()])
    alcohol = IntegerField('Wet Collection', validators=[Optional()])



class ParticipanteSubForm(FlaskForm):
    nombre = StringField('Name', validators=[InputRequired(), Length(max=10)])
    apellidos = StringField('Lastname', validators=[InputRequired()])

    # Fix problems with the csrf token in subforms
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(ParticipanteSubForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

class ParticipanteForm(FlaskForm):
    agent = FormField(ParticipanteSubForm)
    submit = SubmitField("Add agent")

class TaxonSubForm(FlaskForm):
    genero = StringField('Genus', validators=[InputRequired(), Length(max=50)])
    especie = StringField('Specific Epithet', validators=[Optional(), Length(max=50)], default='sp.')
    sub_especie = StringField('Infra-specific Epithet', validators=[Optional(), Length(max=50)])
    autor = StringField('Author', validators=[Optional(), Length(max=100)])

    # Fix problem with csrf token in subforms
    def __init__(self, csrf_enabled=False, *args, **kwargs):
        super(TaxonSubForm, self).__init__(csrf_enabled=csrf_enabled, *args, **kwargs)

class TaxonForm(FlaskForm):
    taxon = FormField(TaxonSubForm)
    submit = SubmitField('Add taxon')

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



