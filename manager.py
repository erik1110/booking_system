from flask_script import Manager

from app.views import app
from db import dbhelper

manager = Manager(app)

@manager.command
def create_tables():
    dbhelper.create_tables()

@manager.command
def load_data():
    dbhelper.load_data()

if __name__ == '__main__':
    manager.run()
