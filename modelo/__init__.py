# -*- coding: utf-8 -*-
from modelo import Categorias, Pregunta_Respuesta,Preguntas, Respuestas, Usuarios, Clientes
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import conexion
print "voy a crear otra conexion"
session=modelo.conexionBD.Session()



def findUsuario(idCliente, idUsuarios):
       busqueda =session.query(Usuarios, Clientes).filter(Clientes.id_cliente==idCliente).filter(Usuarios.id_usuario==idUsuarios, Usuarios.id_cliente==Clientes.id_cliente).first()
       return busqueda

def findUsuariobyId(idUsuario):
    busqueda = session.query(Usuarios).filter(Usuarios.id_usuario == idUsuario).first()
    return busqueda

def findUsuariobyNombreNcliente(nCliente,usuario):
    print usuario
    busqueda = session.query(Usuarios,Clientes).filter(Clientes.n_cliente==nCliente).filter(Usuarios.nombre_usuario == usuario, Usuarios.id_cliente==Clientes.id_cliente).first()
    print busqueda
    return busqueda

def findCliente(idCliente):
        busqueda=session.query(Usuarios,Clientes).filter(Clientes.id_cliente == idCliente).filter(Usuarios.id_cliente==Clientes.id_cliente).all()
        return busqueda

def findPregunta( idpta, ctgoria):
    busqueda=session.query(Preguntas).filter(Preguntas.id_preguntas==idpta ,Preguntas.id_categorias!=ctgoria).first()
    return busqueda

def findRespuestas(pregunta):
   busqueda = session.query(Respuestas).filter(Preguntas.Respuestas).filter(Preguntas.id_preguntas==pregunta).all()
   return busqueda

def findRespuestaCorrecta(idPregunta, idRespuesta):
    busqueda = session.query(Preguntas).filter(Preguntas.id_preguntas == idPregunta,Preguntas.id_respuesta==idRespuesta).first()
    return busqueda


def commit():
   update = session.commit()
   return update
