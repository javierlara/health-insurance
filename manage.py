import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from api import app
from api.db import Base

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, Base)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()