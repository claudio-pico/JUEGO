# -*- coding: utf-8 -*-

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

#engine = sqlalchemy.create_engine("mysql+pymysql://root:@127.0.0.1/tesis?host=localhost?port=3306")
import conexion
conexionBD=conexion.Conexion()
print "voya crear conexion en modelo"
engine=conexionBD.engine()
Base = declarative_base()


# relaciones muchos a muchos
Pregunta_Respuesta = sqlalchemy.Table('Pregunta_Respuesta', Base.metadata,
                                      sqlalchemy.Column('id_preguntas', sqlalchemy.Integer, sqlalchemy.ForeignKey('Preguntas.id_preguntas')),
                                      sqlalchemy.Column('id_respuesta', sqlalchemy.Integer, sqlalchemy.ForeignKey('Respuestas.id_respuestas'))
                                      )


class Preguntas(Base):
    __tablename__ = 'Preguntas'
    id_preguntas = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_respuesta = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    pregunta = sqlalchemy.Column(sqlalchemy.String(120), nullable=False)
    id_categorias = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Categorias.id_categoria'))
    Respuestas = relationship("Respuestas", secondary=Pregunta_Respuesta) # ,backref="respuesta"
    # autores = relationship("Autor", secondary=autor_libro)

    def __init__(self, id_respuesta, pregunta,id_categorias):
        self.id_respuesta = id_respuesta
        self.pregunta = pregunta
        self.id_categorias = id_categorias



class Respuestas(Base):
    __tablename__ = 'Respuestas'
    id_respuestas = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    respuestas = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)

    def __init__(self, respuestas):
        self.respuestas = respuestas


class Categorias(Base):
    __tablename__ = 'Categorias'
    id_categoria = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    categoria = sqlalchemy.Column(sqlalchemy.String(120), nullable=False)
    aciertos = sqlalchemy.Column(sqlalchemy.Integer)
    total = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, categoria, aciertos, total):
        self.categoria = categoria
        self.aciertos = aciertos
        self.total = total

class Clientes(Base):
    __tablename__ = 'Clientes'
    id_cliente=sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    n_cliente = sqlalchemy.Column(sqlalchemy.BIGINT, nullable=False,unique=True)
    credito_cliente = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __init__(self, id_ciente, credito_cliente):
        self.id_ciente = id_ciente
        self.id_ciente = id_ciente
        self.credito_cliente = credito_cliente


class Usuarios(Base):
    __tablename__ = 'Usuarios'
    id_usuario = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_cliente = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Clientes.id_cliente'))
    nombre_usuario = sqlalchemy.Column(sqlalchemy.String(120), nullable=False)
    credito_usuario = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    def __init__(self, nombre_usuario, credito_usuario, id_cliente):
        #self.n_usuario = n_usuario
        self.nombre_usuario = nombre_usuario
        self.credito_usuario = credito_usuario
        self.id_cliente=id_cliente

class Facturas(Base):
    __tablename__ = 'Facturas'
    id_factura = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    id_cliente = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Clientes.id_cliente'))
    fecha_vencimiento = sqlalchemy.Column(sqlalchemy.String(120), nullable=False)
    fecha_emision = sqlalchemy.Column(sqlalchemy.String(120), nullable=False)
    monto = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    pagada= sqlalchemy.Column(sqlalchemy.String(12), nullable=False)
    mes_factura= sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('Meses.id_meses'))
    url_factura=sqlalchemy.Column(sqlalchemy.String(160), nullable=False)

    def __init__(self, id_factura, id_clente, fecha_vencimiento):
        #self.n_usuario = n_usuario
        self.id_factura = id_factura
        self.id_cliente = id_clente
        self.fecha_vencimiento=fecha_vencimiento

class Meses(Base):
    __tablename__ = 'Meses'
    id_meses=sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    mes_nombre = sqlalchemy.Column(sqlalchemy.String(64), nullable=False)

    def __init__(self, id_meses, mes_nombre):
        self.id_meses = id_meses
        self.mes_nombre = mes_nombre

class Administradores(Base):
    __tablename__ = 'Administradores'
    id_adm=sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    usuario_adm = sqlalchemy.Column(sqlalchemy.String(64), nullable=False,unique=True)
    contrasena_adm = sqlalchemy.Column(sqlalchemy.String(64), nullable=False)

    def __init__(self, usuario_adm, contrasena_adm):
        self.usuario_adm = usuario_adm
        self.contrasena_adm = contrasena_adm


Base.metadata.create_all(engine)

