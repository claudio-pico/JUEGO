#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request, make_response
from flask import abort
from flask_httpauth import HTTPBasicAuth
from flask_cors import cross_origin, CORS

from controlador import seguridad

import constantes
auth = HTTPBasicAuth()

from controlador import controlador
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY']='SECRET_KEY'

@app.route("/"+constantes.version+"/token")
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
#trae Usuario(u) o Clientes(c) segun la variable pddo
@app.route("/"+constantes.version+'/usuarios')
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
@app.route("/"+constantes.version+'/preguntaRespuestas/<int:ctgoria>')
@auth.login_required
def preguntaRespuesta(ctgoria):
    data = controlador.GetPregunta(ctgoria)
    if data is None:
        abort(constantes.Not_Found)
    return jsonify(data)



#      "idPregunta": 1,"idRespuesta":1
#
#
@app.route("/"+constantes.version+'/preguntaRespuestas', methods=['PUT'])
@auth.login_required
def IngresaRespuesta():
    if (not request.json or not 'idPregunta' in request.json) or (not 'idRespuesta' in request.json):
        print("no trea el body")
        abort(constantes.badRequest)
    print request.json['idPregunta']
    usr = seguridad.verify_auth_token(request.args.get('token'), app.config['SECRET_KEY'])
    respuestaCredito=controlador.ingresarRespuesta(int(request.json['idPregunta']),int(request.json['idRespuesta']),int(usr['idCliente']),int(usr['idUsuario']))
    if respuestaCredito is None:
        abort(constantes.Not_Found)
    return jsonify(respuestaCredito)

@app.route("/"+constantes.version+'/facturas')
@auth.login_required
def facturas():
    usr = seguridad.verify_auth_token(request.args.get('token'), app.config['SECRET_KEY'])
    respuestaFacturas=controlador.GetFactura(usr['idCliente'])
    if respuestaFacturas is None:
        abort(constantes.Not_Found)
    return jsonify(respuestaFacturas)
# ---------------------------API para la web ---------------------------
@app.route("/"+constantes.version+'/categorias')
def categorias():
    categorias=controlador.GetCategorias()
    if categorias is None:
        abort(constantes.Not_Found)

    return jsonify(categorias)

@app.route("/"+constantes.version+'/respuestas')
def respuestas():
    respuestas=controlador.GetRespuestas()

    if respuestas is None:
        abort(constantes.Not_Found)
    return jsonify(respuestas)


#var String pregunta
#    Int categoria
#    rstCorrecta (id del array respuestas)
#    respuestas{idRespuestas: respuesta:}
@app.route("/"+constantes.version+'/pregunta', methods=['POST'])
def agregarPregunta():
    if ((not 'respuestas' in request.json or not 'pregunta' in request.json) or ((not 'categoria' in request.json) or (not 'rstCorrecta' in request.json))):
       abort(constantes.badRequest)
    respuestas=[]

    if len(request.json['respuestas'])==0:
        print "primera vald"
        abort(constantes.badRequest)

    for rsta in request.json['respuestas']:
        if rsta["idRespuesta"] is None:
            print "hola"
            rsta['idRespuesta']=controlador.SetRespuesta(rsta["respuesta"])
        respuestas.append(rsta)

    idCorrecta=respuestas[0]
    print idCorrecta
    respuesta=controlador.SetPregunta(request.json['pregunta'],int(idCorrecta["idRespuesta"]),int(request.json["categoria"]),respuestas)
    return jsonify(respuesta)

#pido repuestas de pregunta para update
@app.route("/"+constantes.version+'/respuestaCategoria/<int:idPregunta>')
def respuestaCategoria(idPregunta):
    data = controlador.GetRespuestasPorPregunta(idPregunta)
    if data is None:
        abort(constantes.Not_Found)
    return jsonify(data)


@app.route("/" + constantes.version + '/pregunta/<int:idPregunta>', methods=['DELETE'])
def respuestasDelete(idPregunta):
    respuesta=controlador.DeletePregunta(idPregunta)
    return jsonify(respuesta)\

@app.route("/" +constantes.version+ '/respuestasCategoria', methods=['PUT'])
def updatePregunta():
    if ((not 'idPregunta' in request.json or not 'respuestas' in request.json) or ((not 'rstCorrecta' in request.json) or (not 'ctgoria' in request.json))):
       abort(constantes.badRequest)
    respuestas=[];
    respuestas=request.json['respuestas'];
    print respuestas
    respuesta=controlador.updatePregunta(request.json['idPregunta'],request.json['ctgoria'],request.json['rstCorrecta'],respuestas)
    return jsonify(respuesta)

@app.route("/" + constantes.version + '/preguntas')
def getPreguntas():

    respuesta=controlador.GetPreguntas()
    return jsonify(respuesta)

@app.route("/" + constantes.version + '/autenticar', methods=['POST'])
def autenticar():
    if ((not 'usuario' in request.json or not 'contrasena' in request.json)):
        abort(constantes.badRequest)

    data=seguridad.validarUsuario(request.json['usuario'],request.json['contrasena'])
    if data is None:
        abort(constantes.Not_Found)
    return jsonify(data)

@app.errorhandler(constantes.Not_Found)
def not_found(error):
       return make_response(jsonify({'error':'Not Found'}),constantes.Not_Found)

@app.errorhandler(constantes.badRequest)
def not_found(error):
       return make_response(jsonify({'error':'Faltan Datos'}),constantes.Not_Found)

@app.errorhandler(constantes.invalidCredentials)
def not_found(error):
       return make_response(jsonify({'error':'Falla Validacion'}),constantes.Not_Found)

#if __name__ == "__main__":
    #app.run(debug=True,port=8088)
    #app.run(debug=True,host=constantes.ipadrres,port=8080)
