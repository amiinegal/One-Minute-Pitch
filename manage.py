from app import create_app
from flask_script import Manager,Server
from app.models import User,db,Pitch
from  flask_migrate import Migrate, MigrateCommand

app = create_app('production')
manager = Manager(app)
migrate = Migrate(app,db)

manager.add_command('server',Server)
manager.add_command('db',MigrateCommand)

# app = create_app('development')


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

#this decorator allows us to pass properties into my shell     
@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User=User,Pitch=Pitch)
if __name__ == '__main__':
    app.secret_key ='2042'
    manager.run()
