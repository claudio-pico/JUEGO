import os
OPENSHIFT_PYTHON_IP = os.environ['OPENSHIFT_PYTHON_IP']
OPENSHIFT_PYTHON_PORT = os.environ['OPENSHIFT_PYTHON_PORT']
OPENSHIFT_PYTHON_DIR = os.environ['OPENSHIFT_PYTHON_DIR']
SERVER_ROOT = os.path.join(OPENSHIFT_PYTHON_DIR, 'run', 'mod_wsgi')
VIRTUAL_ENV = os.environ['VIRTUAL_ENV']
program = os.path.join(VIRTUAL_ENV, 'bin', 'mod_wsgi-express')
os.execl(program, program, 'start-server', 'wsgi.py',
        '--server-root', SERVER_ROOT, '--log-to-terminal',
        '--host', OPENSHIFT_PYTHON_IP, '--port', OPENSHIFT_PYTHON_PORT)