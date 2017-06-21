import os
import constantes
from app import app as application

if __name__ == '__main__':

    ip = os.environ.get('OPENSHIFT_PYTHON_IP', constantes.ipadrres)
    port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', 8080))

    # Para detalhae melhor os Logs no OpenShift
    application.config['PROPAGATE_EXCEPTIONS'] = True

    application.run(ip,port)