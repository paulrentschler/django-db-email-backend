"""
Creating standalone Django apps is a PITA because you're not in a project, so
you don't have a settings.py file.  I can never remember to define
DJANGO_SETTINGS_MODULE, so I run these commands which get the right env
automatically.
"""
import functools
import os

from fabric.api import local as _local

try:
    import south
except ImportError:
    south = None

NAME = os.path.basename(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(__file__))
APP_NAME = 'db_email_backend'

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_app.settings'
os.environ['PYTHONPATH'] = os.pathsep.join([ROOT, ])

_local = functools.partial(_local, capture=False)

def manage(cmd):
    """Update a testing database"""
    _local('django-admin.py {}'.format(cmd))


def shell():
    """Start a Django shell with the test settings."""
    _local('django-admin.py shell')


def test(test_case=''):
    """Run the test suite."""
    _local('django-admin.py test {}'.format(test_case))


def test_coverage():
    _local('coverage run --source={} --omit=*/migrations/*.py '
           '$(which django-admin.py) test'.format(APP_NAME))


def serve():
    """Start the Django dev server."""
    _local('django-admin.py runserver')


def syncdb():
    """Create a database for testing in the shell or server."""
    if south:
        _local('django-admin.py syncdb')
    else:
        _local('django-admin.py migrate')


def schema(initial=False):
    """Create a schema migration for any changes."""
    if south:
        if initial:
            _local('django-admin.py schemamigration {} --initial'.format(APP_NAME))
        else:
            _local('django-admin.py schemamigration {} --auto'.format(APP_NAME))
    else:
            _local('django-admin.py makemigrations')

def migrate(app_name='', migration=''):
    """Update a testing database"""
    _local('django-admin.py migrate {} {}'.format(APP_NAME, migration))
