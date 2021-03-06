from webapp import app
from webapp.models import (
    db,
    Taxon,
    Transecto,
    ParqueUrbano,
    Participante,
    Quadrat,
    TaxonQuadrat
)
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('server', Server())
manager.add_command('db', MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        Taxon=Taxon,
        Transecto=Transecto,
        ParqueUrbano=ParqueUrbano,
        Participante=Participante,
        Quadrat=Quadrat,
        TaxonQuadrat=TaxonQuadrat
    )
if __name__ == "__main__":
    manager.run()
