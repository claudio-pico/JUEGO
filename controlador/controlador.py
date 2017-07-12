#!/usr/bin/env python
# -*- coding: utf-8 -*-
import modelo
import random
import constantes
from modelo import Preguntas
from modelo import Respuestas


def GetUsuario(idCliente, idUsuario):
   usuarios =[]
   usuario={}
   busquedaUsuario = modelo.findUsuario(idCliente, idUsuario)
   if busquedaUsuario is None:
       return
   usuario["nombre"] = busquedaUsuario.Usuarios.nombre_usuario
   usuario["creditoUsuario"] = busquedaUsuario.Usuarios.credito_usuario
   creditoCliente = {"creditoCliente": busquedaUsuario.Clientes.credito_cliente}
   usuarios.append(usuario)
   jsonUsuario = {"Usuarios": usuarios, "Cliente": creditoCliente}
   return jsonUsuario

def GetUsuarios(idCliente):
   listaUsuarios = []
   busquedaCliente = modelo.findCliente(idCliente)
   if len(busquedaCliente) is 0:
      return
   for usuarioM in busquedaCliente:
       usuario={}
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
    sqlPregunta = modelo.findPreguntabyIDandCategoria(idpta, ctgoria)

    if sqlPregunta is None:
       return GetPregunta(ctgoria)
    pregunta={}
    pregunta["idPregunta"]=sqlPregunta.id_preguntas
    pregunta["pregunta"] = unicode(str(sqlPregunta.pregunta),errors='ignore')
    pregunta["idCategoria"] = sqlPregunta.id_categorias
    sqlRespuesta=modelo.findRespuestasandPreguntabyIdpregunta(sqlPregunta.id_preguntas)
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
    pregunta=modelo.findPreguntaCategoriasbyId(idPregunta)
    respuestaCreditos={};
    usuario = modelo.findUsuario(idCliente, idUsuario)
    if usuario is None:
        return "no econtro u"

    respuestaCreditos["creditoUsuario"] = usuario.Usuarios.credito_usuario
    respuestaCreditos["creditoCliente"] = usuario.Clientes.credito_cliente
    respuestaCreditos["idRsp"] = pregunta.Preguntas.id_respuesta
    print pregunta.Categorias.total;
    if pregunta.Preguntas.id_respuesta!=idRespuesta:
        respuestaCreditos["rstaAnterior"]=constantes.Incorrecto
        pregunta.Categorias.total = pregunta.Categorias.total + 1;
        modelo.commit()
    else:
        usuario.Usuarios.credito_usuario= usuario.Usuarios.credito_usuario+constantes.puntosRespuestas
        usuario.Clientes.credito_cliente= usuario.Clientes.credito_cliente+constantes.puntosRespuestas
        pregunta.Categorias.aciertos = pregunta.Categorias.aciertos +constantes.uno;
        pregunta.Categorias.total = pregunta.Categorias.total + 1;
        pregunta.Categorias.aciertos = pregunta.Categorias.aciertos + 1;
        modelo.commit()
        respuestaCreditos["rstaAnterior"] = constantes.Correcto

    return respuestaCreditos


def GetFactura(idCliente):
   listaFacturas =[]
   estadoCliente={}
   busquedaFacturas = modelo.findFacturas(idCliente)
   if busquedaFacturas is None:
       return

   sumarMonto=0
   vencimiento=""
   for resp in busquedaFacturas:
       factura = {}
       factura["mes"] = resp.Meses.mes_nombre
       factura["emision"] = resp.Facturas.fecha_emision
       factura["url"] = resp.Facturas.url_factura
       listaFacturas.append(factura)

       if resp.Facturas.pagada==constantes.no:
           sumarMonto=sumarMonto+resp.Facturas.monto
           vencimiento=resp.Facturas.fecha_vencimiento
   estadoCliente["monto"] = sumarMonto
   estadoCliente["vencimiento"]=vencimiento
   jsonUsuario = {"monto":sumarMonto,"vencimiento":vencimiento,"Facturas":listaFacturas}
   return jsonUsuario

def GetCategorias():
    categorias =[]
    busquedaCategorias = modelo.findCategorias()
    if busquedaCategorias is None:
        return
    for ctg in busquedaCategorias:
        categoria = {}
        categoria["idCategoria"] = ctg.id_categoria
        categoria["nombre"] = ctg.categoria
        categoria["aciertos"] = ctg.aciertos
        categoria["total"] =ctg.total
        categorias.append(categoria)

    jsonCategorias = {"categorias":categorias}
    return jsonCategorias

def GetRespuestas():
    respuestas=[]
    busquedaRespuesta= modelo.findRespuestas()
    if busquedaRespuesta is None:
        return

    for rsta in busquedaRespuesta:
        respuesta = {}
        respuesta["idRespuesta"] = rsta.id_respuestas
        respuesta["respuesta"] = rsta.respuestas
        respuestas.append(respuesta)

    jsonRespuestas = {"respuestas":respuestas}

    return jsonRespuestas

def SetPregunta(pregunta,respCorrecta,idCategoria,rstas):
   p= Preguntas(respCorrecta,pregunta,idCategoria);

   for r in rstas:
       respuesta=modelo.findRespuestasListbyId(r["idRespuesta"])
       p.Respuestas.append(respuesta)

   modelo.addCommit(p)
   return {"estado":"OK"}

def SetRespuesta(respuesta):
   r= Respuestas(respuesta);
   modelo.addCommit(r)
   return r.id_respuestas



