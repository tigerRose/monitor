#!/usr/bin/env python
import os
from app import create_app, db
from app.models import User, Role, ProjectInfo, AnalogInfo, DigitInfo
from app.monitor import monitor_run, monitor_test
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from gevent import monkey
monkey.patch_all()
import gevent
from gevent import pywsgi

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, ProjectInfo=ProjectInfo,\
            AnalogInfo=AnalogInfo, DigitInfo=DigitInfo)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    g1 = gevent.spawn(monitor_run)
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    g2 = gevent.spawn(server.serve_forever)
    #g2 = gevent.spawn(manager.run)
    #g2 = gevent.spawn(monitor_run)
    g1.join()
    g2.join()
