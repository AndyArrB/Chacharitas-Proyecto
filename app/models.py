from datetime import date
from flask_security.models import fsqla_v3
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Municipio(db.Model):
    __tablename__ = 'municipios'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_municipio: Mapped[str] = mapped_column(db.String(50), nullable=False)

class Colonia(db.Model):
    __tablename__ = 'colonias'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_colonia: Mapped[str] = mapped_column(db.String(50), nullable=False)
    cp: Mapped[str] = mapped_column(db.String(10), nullable=False)
    municipio_id: Mapped[int] = mapped_column(db.ForeignKey('municipios.id'), nullable=False)
    municipio = db.relationship('Municipio', backref=db.backref('colonias', cascade='all, delete-orphan'))

class Calle(db.Model):
    __tablename__ = 'calles'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_calle: Mapped[str] = mapped_column(db.String(100), nullable=False)
    colonia_id: Mapped[int] = mapped_column(db.ForeignKey('colonias.id'), nullable=False)
    colonia = db.relationship('Colonia', backref=db.backref('calles', cascade='all, delete-orphan'))

class Marca(db.Model):
    __tablename__ = 'marcas'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_marca: Mapped[str] = mapped_column(db.String(50), nullable=False)

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo_categoria: Mapped[str] = mapped_column(db.String(50), nullable=False)

class Genero(db.Model):
    __tablename__ = 'generos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_genero: Mapped[str] = mapped_column(db.String(50), nullable=False)

class FormaPago(db.Model):
    __tablename__ = 'formas_pagos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_forma: Mapped[str] = mapped_column(db.String(50), nullable=False)

class Color(db.Model):
    __tablename__ = 'colores'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_color: Mapped[str] = mapped_column(db.String(50), nullable=False)

class Material(db.Model):
    __tablename__ = 'materiales'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_material: Mapped[str] = mapped_column(db.String(50), nullable=False)

class TipoTamaño(db.Model):
    __tablename__ = 'tipo_tamaños'
    id: Mapped[int] = mapped_column(primary_key=True)
    tipo_tamaño: Mapped[str] = mapped_column(db.String(50), nullable=False)

class DetalleTamaño(db.Model):
    __tablename__ = 'detalle_tamaños'
    id: Mapped[int] = mapped_column(primary_key=True)
    id_tipo_tamaño: Mapped[int] = mapped_column(db.ForeignKey('tipo_tamaños.id'), nullable=False)
    tamaño: Mapped[str] = mapped_column(db.String(50), nullable=False)
    tipo_tamaño = db.relationship('TipoTamaño', backref=db.backref('detalle_tamaños', cascade='all, delete-orphan'))

class Producto(db.Model):
    __tablename__ = 'productos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_producto: Mapped[str] = mapped_column(db.String(100), nullable=False)
    cantidad: Mapped[int] = mapped_column(nullable=False)
    precio: Mapped[float] = mapped_column(nullable=False)
    id_color: Mapped[int] = mapped_column(db.ForeignKey('colores.id'), nullable=False)
    id_categoria: Mapped[int] = mapped_column(db.ForeignKey('categorias.id'), nullable=False)
    id_detalle_tamaños: Mapped[int] = mapped_column(db.ForeignKey('detalle_tamaños.id'), nullable=False)
    id_marca: Mapped[int] = mapped_column(db.ForeignKey('marcas.id'), nullable=False)
    id_material: Mapped[int] = mapped_column(db.ForeignKey('materiales.id'), nullable=False)
    id_genero: Mapped[int] = mapped_column(db.ForeignKey('generos.id'), nullable=False)
    id_usuario: Mapped[int] = mapped_column(db.ForeignKey('usuarios.id'), nullable=False)
    color = db.relationship('Color', backref=db.backref('productos', cascade='all, delete-orphan'))
    categoria = db.relationship('Categoria', backref=db.backref('productos', cascade='all, delete-orphan'))
    detalle_tamaño = db.relationship('DetalleTamaño', backref=db.backref('productos', cascade='all, delete-orphan'))
    marca = db.relationship('Marca', backref=db.backref('productos', cascade='all, delete-orphan'))
    material = db.relationship('Material', backref=db.backref('productos', cascade='all, delete-orphan'))
    genero = db.relationship('Genero', backref=db.backref('productos', cascade='all, delete-orphan'))
    usuario = db.relationship('User', backref=db.backref('productos', cascade='all, delete-orphan'))

class TipoSuscripcion(db.Model):
    __tablename__ = 'tipo_suscripciones'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_suscripcion: Mapped[str] = mapped_column(db.String(50), nullable=False)
    precio: Mapped[float] = mapped_column(nullable=False)

class Suscripcion(db.Model):
    __tablename__ = 'suscripciones'
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha_inicio: Mapped[date] = mapped_column(nullable=False)
    fecha_renovacion: Mapped[date] = mapped_column(nullable=False)
    id_cliente: Mapped[int] = mapped_column(db.ForeignKey('usuarios.id'), nullable=False)
    id_tipo_suscripcion: Mapped[int] = mapped_column(db.ForeignKey('tipo_suscripciones.id'), nullable=False)
    cliente = db.relationship('User', backref=db.backref('suscripciones', cascade='all, delete-orphan'))
    tipo_suscripcion = db.relationship('TipoSuscripcion', backref=db.backref('suscripciones', cascade='all, delete-orphan'))

class Estatus(db.Model):
    __tablename__ = 'estatus'
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(db.String(50), nullable=False)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[date] = mapped_column(nullable=False)
    id_cliente: Mapped[int] = mapped_column(db.ForeignKey('usuarios.id'), nullable=False)
    id_estatus: Mapped[int] = mapped_column(db.ForeignKey('estatus.id'), nullable=False)
    id_forma_pago: Mapped[int] = mapped_column(db.ForeignKey('formas_pagos.id'), nullable=False)
    cliente = db.relationship('User', backref=db.backref('pedidos', cascade='all, delete-orphan'))
    estatus = db.relationship('Estatus', backref=db.backref('pedidos', cascade='all, delete-orphan'))
    forma_pago = db.relationship('FormaPago', backref=db.backref('pedidos', cascade='all, delete-orphan'))

class DetallePedido(db.Model):
    __tablename__ = 'detalles_pedidos'
    id: Mapped[int] = mapped_column(primary_key=True)
    cantidad: Mapped[int] = mapped_column(nullable=False)
    id_producto: Mapped[int] = mapped_column(db.ForeignKey('productos.id'), nullable=False)
    id_pedido: Mapped[int] = mapped_column(db.ForeignKey('pedidos.id'), nullable=False)
    producto = db.relationship('Producto', backref=db.backref('detalles_pedidos', cascade='all, delete-orphan'))
    pedido = db.relationship('Pedido', backref=db.backref('detalles_pedidos', cascade='all, delete-orphan'))