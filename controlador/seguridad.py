#!/usr/bin/env python
# -*- coding: utf-8 -*-

import modelo
from itsdangerous import Serializer
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


def generate_auth_token(usuario,idCliente,key, expiration=600000000):
    s = Serializer(key,expires_in=expiration)
    usr =modelo.findUsuariobyNombreNcliente(idCliente,usuario)
    if usr is None:
        return
    token=s.dumps({'idUsuario': usr.Usuarios.id_usuario, 'idCliente': usr.Clientes.id_cliente})
    jsonLog = {"token": token}
    return jsonLog

#@staticmethod
def verify_auth_token(token,key):
    s = Serializer(key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user = modelo.findUsuariobyId(data['idUsuario'])
    return {"idUsuario": user.id_usuario,"idCliente":user.id_cliente}

def validarUsuario(usuario, contrasena):
    print usuario
    print contrasena
    adm=modelo.findAdministradores(usuario,contrasena)
    if adm is None:
     return {"success": 'false'}

    return {"success":'true'}