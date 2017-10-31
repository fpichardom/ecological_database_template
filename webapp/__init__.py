from flask import Flask, render_template, request, redirect, url_for, flash
from .config import Config
from .models import(
    db, Taxon, TaxonQuadrat, ParqueUrbano, Transecto,
    Quadrat, Participante
)
from webapp.forms import(
    ParqueForm, TransectoForm, QuadratForm,
    TaxonQuadratForm, ParticipanteForm, TaxonForm, TaxonSubForm)

from flask_bootstrap import Bootstrap
from wtforms.validators import ValidationError
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
#@app.route('/parque_urbano')
def home():
    form = ParqueForm()
    parques = ParqueUrbano.query.all()
    if form.validate_on_submit():
        new_parque = ParqueUrbano(form.parque.data)

        try:
            db.session.add(new_parque)
            db.session.commit()
            return redirect(url_for('home'))
        except IntegrityError:
            form.parque.errors.append('Already exists')
            db.session.rollback()
            
    
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
   
        try:
            db.session.add(new_tr)
            db.session.commit()
            return redirect(url_for('transectos',parque_id=parque_id))
        except IntegrityError:
            form.transecto.errors.append('Ya existe')
            db.session.rollback()
            
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

        try:
            db.session.add(new_qdt)
            db.session.commit()
            return redirect(url_for('quadrats',tr_id=tr_id))
        except IntegrityError:
            db.session.rollback()
            form.quadrat.errors.append('Already exists on {}'.format(transecto.transecto))
            

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
    asos = TaxonQuadrat.query.filter_by(quadrat_id=qdt_id).all()
    #taxa = Taxon.query.all()
    if form.validate_on_submit():
        new_bind = TaxonQuadrat()
        new_bind.quadrat_id = qdt_id
        new_bind.taxon_id = form.taxon_id.data
        new_bind.abundancia = form.abundancia.data
        new_bind.vial = form.vial.data.upper()
        new_bind.alfiler = form.alfiler.data
        new_bind.alcohol = form.alcohol.data
        if not TaxonQuadrat.query.filter_by(quadrat_id=qdt_id, taxon_id=form.taxon_id.data).first():
            db.session.add(new_bind)
            db.session.commit()
            return redirect(url_for('quadrat',qdt_id=qdt_id))

    return render_template(
        'quadrat.html',
        form=form,
        quadrat=quadrat,
        asos=asos
    )

@app.route('/taxa', methods=['GET', 'POST'])
def taxon():
    form = TaxonForm()
    taxa = Taxon.query.order_by('nombre_cientifico').all()


    if form.validate_on_submit():
        new_taxon = Taxon()
        new_taxon.genero = form.taxon.data['genero']
        new_taxon.especie = form.taxon.data['especie']
        new_taxon.sub_especie = form.taxon.data['sub_especie']
        new_taxon.autor = form.taxon.data['autor']        
        new_taxon.build_sciname()

        try:
            db.session.add(new_taxon)
            db.session.commit()
            return redirect(url_for('taxon'))
        except IntegrityError:
            db.session.rollback()
            flash(' Taxon already exists','danger')
    
    return render_template(
        'taxa.html',
        taxa=taxa,
        form=form
    )

@app.route('/participantes', methods=['GET', 'POST'])
def participantes():

    form = ParticipanteForm()
    participantes = Participante.query.order_by('nombre').all()
    resp =''
    if form.validate_on_submit():
        resp = form.participante.data
        new_parti = Participante()
        new_parti.nombre = form.participante.data['nombre']
        new_parti.apellidos = form.participante.data['apellidos']
        
        try:
            db.session.add(new_parti)
            db.session.commit()
            return redirect(url_for('participantes'))
        except IntegrityError:
            db.session.rollback()
            flash(' Agent already exists','danger')

       # new_parti = form.participante.data
        #return new_parti
        #db.session.add(new_parti)
        #db.session.commit()
        return render_template(
        'participantes.html',
        participantes=participantes,
        form=form,resp=resp)
        #return redirect(url_for('participantes'))
    
    return render_template(
        'participantes.html',
        participantes=participantes,
        form=form,resp=resp
    )
if __name__ == '__main__':
    app.run()
