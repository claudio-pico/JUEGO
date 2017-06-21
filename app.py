import os
OPENSHIFT_REPO_DIR = os.environ['OPENSHIFT_REPO_DIR']
os.chdir(OPENSHIFT_REPO_DIR)
OPENSHIFT_PYTHON_IP = os.environ['OPENSHIFT_PYTHON_IP']
OPENSHIFT_PYTHON_PORT = os.environ['OPENSHIFT_PYTHON_PORT']
VIRTUAL_ENV = os.environ['VIRTUAL_ENV']
program = os.path.join(VIRTUAL_ENV, 'bin', 'mod_wsgi-express')
os.execl(program, program, 'start-server', 'wsgi.py',
        '--server-root', '--log-to-terminal',
        '--host', OPENSHIFT_PYTHON_IP, '--port', OPENSHIFT_PYTHON_PORT)