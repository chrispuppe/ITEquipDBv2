from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from config import SQLALCHEMY_DATABASE_URI
from run import app
from app import db #from app.basemodels import db

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()