#!/usr/bin/env python
# -*- coding: utf-8 -*-
import modelo
import random
import constantes


def GetUsuario(idCliente, idUsuario):
   usuario = {}
   busquedaUsuario = modelo.findUsuario(idCliente, idUsuario)
   if busquedaUsuario is None:
       return
   usuario["nombre"] = busquedaUsuario.Usuarios.nombre_usuario
   usuario["creditoUsuario"] = busquedaUsuario.Usuarios.credito_usuario
   creditoCliente = {"creditoCliente": busquedaUsuario.Clientes.credito_cliente}
   jsonUsuario = {"Usuarios": usuario, "Cliente": creditoCliente}
   return jsonUsuario

def GetUsuarios(idCliente):
   listaUsuarios = []
   busquedaCliente = modelo.findCliente(idCliente)
   if len(busquedaCliente) is 0:
      return
   for usuarioM in busquedaCliente:
       usuario={}
       #usuario["nCliente"] = usuarioM.Clientes.n_cliente
       #usuario["nUsuario"] = usuarioM.Usuarios.id_usuario
       usuario["nombre"] = usuarioM.Usuarios.nombre_usuario
       usuario["creditoUsuario"] = usuarioM.Usuarios.credito_usuario

       listaUsuarios.append(usuario)

   creditoCliente={"creditoCliente":usuarioM.Clientes.credito_cliente}
   jsonUsuario = {"Usuarios": listaUsuarios, "Cliente":creditoCliente}
   return jsonUsuario

def GetPregunta(ctgoria):
    preguntaRespuesta=[]
    respuestas=[]

    idpta=random.randint(constantes.min,constantes.max)
    sqlPregunta = modelo.findPregunta(idpta,ctgoria)

    if sqlPregunta is None:
       return GetPregunta(ctgoria)
    pregunta={}
    pregunta["idPregunta"]=sqlPregunta.id_preguntas
    pregunta["pregunta"] = unicode(str(sqlPregunta.pregunta),errors='ignore')
    pregunta["idCategoria"] = sqlPregunta.id_categorias
    sqlRespuesta=modelo.findRespuestas(sqlPregunta.id_preguntas)
    for resp in sqlRespuesta:
        respuesta={}
        respuesta["id_respuesta"]=resp.id_respuestas
        respuesta["respuesta"]=resp.respuestas
        respuestas.append(respuesta)
    preguntaRespuesta.append(pregunta)
    preguntaRespuesta.append(respuestas)
    jsonUsuario = {"pregunta":pregunta,"respuestas":respuestas}
    return jsonUsuario

def ingresarRespuesta(idPregunta,idRespuesta,idCliente,idUsuario):
    pregunta=modelo.findRespuestaCorrecta(idPregunta)
    respuestaCreditos={};
    usuario = modelo.findUsuario(idCliente, idUsuario)
    if usuario is None:
        return "no econtro u"

    respuestaCreditos["creditoUsuario"] = usuario.Usuarios.credito_usuario
    respuestaCreditos["creditoCliente"] = usuario.Clientes.credito_cliente
    respuestaCreditos["idRsp"] = pregunta.id_respuesta

    if pregunta.id_respuesta!=idRespuesta:
        respuestaCreditos["rstaAnterior"]=constantes.Incorrecto

    else:
        usuario.Usuarios.credito_usuario= usuario.Usuarios.credito_usuario+constantes.puntosRespuestas
        usuario.Clientes.credito_cliente= usuario.Clientes.credito_cliente+constantes.puntosRespuestas
        modelo.commit()
        respuestaCreditos["rstaAnterior"] = constantes.Correcto

    return respuestaCreditos














