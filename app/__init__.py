#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import json, Flask, jsonify, request, make_response, redirect
from flask import abort
from flask_httpauth import HTTPBasicAuth

from controlador import seguridad

import constantes
auth = HTTPBasicAuth()

from controlador import controlador
app = Flask(__name__)

app.config['SECRET_KEY']='SECRET_KEY'

@app.route('/token')
def loguin():
    usuario=request.args.get('usuario')
    idCliente = request.args.get('cliente')
    if usuario is None or idCliente is None:
        abort(constantes.badRequest)
    token = seguridad.generate_auth_token(usuario,idCliente,app.config['SECRET_KEY'])
    if token is None:
        abort(constantes.Not_Found)
    return jsonify(token)

@auth.verify_password
def verify_token(username, client_password):
    token=request.args.get('token')
    if token is None:
        abort(constantes.badRequest)
    user = seguridad.verify_auth_token(token, app.config['SECRET_KEY'])
    if not user:
        return False
    else:
        return True

@app.route('/usuarios')
@auth.login_required
def usuarios():
    pedido = request.args.get('pddo')
    if pedido is None:
        abort(constantes.badRequest)

    usr=seguridad.verify_auth_token(request.args.get('token'),app.config['SECRET_KEY'])
    if pedido=='c':
        data = controlador.GetUsuarios(usr['idCliente'])
    elif pedido=='u':
        data = controlador.GetUsuario(usr['idCliente'], usr['idUsuario'])
    else:
        abort(constantes.badRequest)
    if data is None:
        abort(constantes.Not_Found)
    return jsonify(data)


#se envia la categoria para no repetir con la pregunta anterior
@app.route('/preguntaRespuestas/<int:ctgoria>')
@auth.login_required
def preguntaRespuesta(ctgoria,rstaAnterior=None):
    print "acaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print rstaAnterior
    data = controlador.GetPregunta(ctgoria,rstaAnterior)
    if data is None:
        abort(constantes.Not_Found)
    return jsonify(data)



#      "idPregunta": 1,"idRespuesta":1,"Categoria":1
#
#
@app.route('/preguntaRespuestas', methods=['PUT'])
@auth.login_required
def IngresaRespuesta():
    if (not request.json or not 'idPregunta' in request.json) or (not 'idRespuesta' in request.json) or (not 'Categoria' in request.json):
        abort(constantes.badRequest)
    usr = seguridad.verify_auth_token(request.args.get('token'), app.config['SECRET_KEY'])
    estadoRsta=controlador.ingresarRespuesta(int(request.json['idPregunta']),int(request.json['idRespuesta']),int(usr['idCliente']),int(usr['idUsuario']))
    if estadoRsta is None:
        abort(constantes.Not_Found)
    print estadoRsta
    return preguntaRespuesta(request.json['Categoria'],estadoRsta)


@app.errorhandler(constantes.Not_Found)
def not_found(error):
       return make_response(jsonify({'error':'Not Found'}),constantes.Not_Found)

@app.errorhandler(constantes.badRequest)
def not_found(error):
       return make_response(jsonify({'error':'Faltan Datos'}),constantes.Not_Found)

@app.errorhandler(constantes.invalidCredentials)
def not_found(error):
       return make_response(jsonify({'error':'Falla Validacion'}),constantes.Not_Found)

if __name__ == "__main__":
    app.run(debug=True,port=8088)
    #app.run(debug=True,host='192.168.1.34',port=8088)
