from app.models import db, Municipio, Colonia, Calle, Direccion, Marca, Categoria, Genero, FormaPago, Color, \
    Material, TipoTamaño, DetalleTamaño, Producto, TipoSuscripcion, Suscripcion, Estatus, Pedido, DetallePedido
from sqlalchemy.exc import SQLAlchemyError

def setup_initial_data():
    try:
        genero1 = Genero(nombre_genero="Masculino")
        genero2 = Genero(nombre_genero="Femenino")

        db.session.add(genero1)
        db.session.add(genero2)
        db.session.commit()

        municipio1 = Municipio(nombre_municipio="Municipio1")
        municipio2 = Municipio(nombre_municipio="Municipio2")
        db.session.add(municipio1)
        db.session.add(municipio2)
        db.session.commit()

        colonia1 = Colonia(nombre_colonia="Colonia1", cp="12345", municipio_id=municipio1.id)
        colonia2 = Colonia(nombre_colonia="Colonia2", cp="67890", municipio_id=municipio2.id)
        db.session.add(colonia1)
        db.session.add(colonia2)
        db.session.commit()

        calle1 = Calle(nombre_calle="Calle1", colonia_id=colonia1.id)
        calle2 = Calle(nombre_calle="Calle2", colonia_id=colonia2.id)
        db.session.add(calle1)
        db.session.add(calle2)
        db.session.commit()

        direccion1 = Direccion(num_int="101", num_ext="123", calle_id=calle1.id)
        direccion2 = Direccion(num_int="202", num_ext="456", calle_id=calle2.id)
        db.session.add(direccion1)
        db.session.add(direccion2)
        db.session.commit()

    except SQLAlchemyError as e:
        print(f"Error al insertar registros: {e}")
        db.session.rollback()