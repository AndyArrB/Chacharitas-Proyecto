import os

from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user
from flask_mail import Message
from flask_security import roles_required, send_mail, hash_password
from sqlalchemy import and_, or_
from werkzeug.utils import secure_filename

from app import app, User
from app import mail
from app.database import Database
from app.forms.modal_form import generate_dynamic_form
from app.forms.product_form import ProductoForm
from app.forms.buy_form import PaymentForm
from app.models import Colonia, Calle, Municipio, Categoria, Producto, Genero, TipoTamaño, TipoSuscripcion, Estatus, \
    FormaPago, Pedido, Color, DetalleTamaño, Marca, Material

# * Instancia para el contacto con nuestra base de datos
db = Database()


# * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -
# * APP ----------------------------------------------------------------------------*
# * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -

# ? Establece las rutas que le dan vida al frontend y al ruteo
# ? de todo este

# ? Rutas sencillas, por lo general solo redirigen.
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/shop")
def shop():
    category_filter = request.args.get('category')
    category = Categoria.query.filter_by(tipo_categoria=category_filter).first()

    products = Producto.query \
        .join(User, Producto.id_usuario == User.id) \
        .join(Calle, User.id_calle == Calle.id) \
        .join(Colonia, Calle.colonia_id == Colonia.id) \
        .join(Municipio, Colonia.municipio_id == Municipio.id) \
        .all()

    genders = Genero.query.all()
    categories = Categoria.query.all()

    if category:
        products = [product for product in products if product.id_categoria == category.id]

    return render_template("shop.html", products=products, genders=genders, categories=categories)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']

        html_body = render_template("email_template.html", nombre=nombre, correo=correo, asunto=asunto, mensaje=mensaje)

        msg = Message(subject=asunto,
                      sender=("Chacharitas", correo),
                      recipients=['axolotlscriptjs@gmail.com'],
                      body=f"Nombre: {nombre}\nCorreo: {correo}\n\nMensaje:\n{mensaje}",
                      html=html_body)

        try:
            mail.send(msg)
            flash('Correo enviado exitosamente.', 'success')
        except Exception as e:
            flash(f'Error al enviar el correo: {str(e)}', 'danger')

        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route("/shop-single/<int:id>")
def shop_single(id):

    product = Producto.query \
        .join(User, Producto.id_usuario == User.id) \
        .join(Calle, User.id_calle == Calle.id) \
        .join(Colonia, Calle.colonia_id == Colonia.id) \
        .join(Municipio, Colonia.municipio_id == Municipio.id) \
        .join(Color, Producto.id_color == Color.id) \
        .join(DetalleTamaño, Producto.id_detalle_tamaños == DetalleTamaño.id) \
        .filter(Producto.id == id) \
        .first()

    return render_template("shop-single.html", product=product)

@app.route("/payment/<int:id>")
def buy(id):

    form = PaymentForm()
    product = Producto.query \
        .join(User, Producto.id_usuario == User.id) \
        .join(Calle, User.id_calle == Calle.id) \
        .join(Colonia, Calle.colonia_id == Colonia.id) \
        .join(Municipio, Colonia.municipio_id == Municipio.id) \
        .join(Color, Producto.id_color == Color.id) \
        .join(DetalleTamaño, Producto.id_detalle_tamaños == DetalleTamaño.id) \
        .filter(Producto.id == id) \
        .first()

    render_template("payment.html", comprar_form=form, product=product)

    # ? Rutas complejas. Se encargan del filtrado del front.


@app.route("/upload", methods=["GET", "POST"])
def upload():
    form = ProductoForm()
    if form.validate_on_submit():
        # Create a new Producto instance
        new_producto = Producto(
            nombre_producto=form.nombre_producto.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data,
            id_color=form.id_color.data,
            id_categoria=form.id_categoria.data,
            id_detalle_tamaños=form.id_detalle_tamaños.data,
            id_marca=form.id_marca.data,
            id_material=form.id_material.data,
            id_genero=form.id_genero.data,
            id_usuario=current_user.id  # Set the current user's ID
        )

        # Add to the database to get the product ID
        db.database.session.add(new_producto)
        db.database.session.commit()

        # Handle file upload
        file = form.imagen.data
        filename = secure_filename(file.filename)
        new_filename = f"p-{new_producto.id}.{filename.rsplit('.', 1)[1].lower()}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))

        # Update the product record with the new image filename
        new_producto.imagen = new_filename
        db.database.session.commit()
        return redirect(url_for('shop'))

    return render_template('upload.html', producto_form=form)


@app.route("/filter-products")
def filter_products():
    try:
        # * Obtenemos todos los IDs de los checkboxes seleccionados.
        # * Todo viene desde la URL como string, por lo que se tiene que
        # * convertir.
        price_ranges = request.args.getlist('price_range')
        price_ranges = [int(pr) for pr in price_ranges]

        categories = request.args.getlist('category')
        categories = [int(cat) for cat in categories]

        genders = request.args.getlist('gender')
        genders = [int(gen) for gen in genders]

        sort_by = int(request.args.get('sort_by'))

        filters = []
        if price_ranges:
            price_filters = []
            for pr in price_ranges:
                if pr == 1:
                    price_filters.append(and_(Producto.precio >= 0, Producto.precio <= 50))
                elif pr == 2:
                    price_filters.append(and_(Producto.c.precio >= 50, Producto.precio <= 100))
                elif pr == 3:
                    price_filters.append(and_(Producto.c.precio >= 100, Producto.precio <= 150))
                elif pr == 4:
                    price_filters.append(Producto.precio >= 150)
            filters.append(or_(*price_filters))
        if categories:
            category_filters = [Producto.id_categoria == cat for cat in categories]
            filters.append(or_(*category_filters))
        if genders:
            gender_filters = [Producto.id_genero == gen for gen in genders]
            filters.append(or_(*gender_filters))

        query = db.database.session.query(Producto, User, Calle, Colonia, Municipio) \
            .join(User, Producto.id_usuario == User.id) \
            .join(Calle, User.id_calle == Calle.id) \
            .join(Colonia, Calle.colonia_id == Colonia.id) \
            .join(Municipio, Colonia.municipio_id == Municipio.id) \
            .filter(and_(*filters)) \

        if sort_by != 1:
            query = query.order_by(Producto.nombre_producto if sort_by == 2 else Producto.precio)

        products = query.all()
        products_dict = []
        for product_tuple in products:
            product_dict = {}
            for obj in product_tuple:
                product_dict[obj.__class__.__name__] = {col.name: getattr(obj, col.name) for col in
                                                        obj.__table__.columns}
            products_dict.append(product_dict)

        print(products_dict)

        try:
            products_json = jsonify(products_dict)
            return products_json
        except Exception as e:
            print(f"Error converting products to JSON: {e}")
            return jsonify({"error": "Error converting products to JSON"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_colonias/<int:municipio_id>', methods=['GET'])
def get_colonias(municipio_id):
    colonias = Colonia.query.filter_by(municipio_id=municipio_id).order_by(Colonia.nombre_colonia).all()
    colonias_list = [(colonia.id, colonia.nombre_colonia) for colonia in colonias]
    return jsonify(colonias_list)


@app.route('/get_calles/<int:colonia_id>', methods=['GET'])
def get_calles(colonia_id):
    calles = Calle.query.filter_by(colonia_id=colonia_id).order_by(Calle.nombre_calle).all()
    calles_list = [(calle.id, calle.nombre_calle) for calle in calles]
    return jsonify(calles_list)


# * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -
# * CRUD ----------------------------------------------------------------------------*
# * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -
# ? Establece las rutas de nuestro servidor. Todas las peticiones de la página se
# ? redirigen aquí

# ? Rutas principales. Estas son las que responden ante las solicitudes HTTP
# ? del cliente.

# * Para llenar las opciones en el <navbar> lateral
tables = db.select_tables()


@app.route("/index/<table>", methods=["GET", "POST"])
@roles_required("admin")
def index_crud(table):
    if request.method == "GET":
        if table in tables:
            # * Para el llenado del <table> y el <modal>
            table_columns = db.select_columns(table=db[table])
            table_columns_data = db.select_columns_data(db[table])

            # * Genera un formulario (clase) de FlaskWTF dinámicamente con las
            # * propiedades adecuadas por cada columna de la tabla. Este se
            # * insertará dentro del <modal>
            ModalForm = generate_dynamic_form(table_columns_data=table_columns_data, table_columns=table_columns, db=db)

            # * Instancia de la clase generada
            modal_form = ModalForm()

            return render_template('index-crud.html', tables=tables,
                                   modal_form=modal_form), 200
        else:
            return "lol"

    elif request.method == "POST":
        if table in tables:
            data = request.json
            data.pop("csrf_token", None)
            db.insert_into(table=db[table], data=data)
            return jsonify({"message": f"Registro con el id {id} actualizado con éxito"}), 200


@app.route("/index/<table>/<int:id>", methods=["DELETE", "PUT"])
@roles_required("admin")
def delete(table, id):
    if request.method == "DELETE":
        if table in tables:
            db.delete_from(table=db[table], registry_id=id)
            return jsonify({"message": f"Registro con el id {id} eliminado con éxito"}), 200

    elif request.method == "PUT":
        if table in tables:
            data = request.json
            data.pop("csrf_token", None)
            db.update_from(table=db[table], data=data, registry_id=id)
            return jsonify({"message": f"Registro con el id {id} actualizado con éxito"}), 200

    # ? Rutas que devuelven información relevante en JSON.
    # ? Su uso radica solo para la renderización de la tabla.


@app.route("/data/<table>/body", methods=["GET"])
# @roles_required("admin")
def body(table):
    table_body = db.select_all(table=db[table])
    table_body = [row._asdict() for row in table_body]

    # Define a mapping of table names to their corresponding field updates
    table_updates = {
        'colonias': {'municipio_id': lambda id: Municipio.query.get(id).nombre_municipio},
        'calles': {'colonia_id': lambda id: Colonia.query.get(id).nombre_colonia},
        'detalle_tamaños': {'id_tipo_tamaño': lambda id: TipoTamaño.query.get(id).tipo_tamaño},
        'suscripciones': {
            'id_cliente': lambda id: User.query.get(id).username,
            'id_tipo_suscripcion': lambda id: TipoSuscripcion.query.get(id).nombre_suscripcion
        },
        'pedidos': {
            'id_cliente': lambda id: User.query.get(id).username,
            'id_estatus': lambda id: Estatus.query.get(id).nombre,
            'id_forma_pago': lambda id: FormaPago.query.get(id).nombre_forma
        },
        'detalles_pedidos': {
            'id_producto': lambda id: Producto.query.get(id).nombre_producto,
            'id_pedido': lambda id: Pedido.query.get(id).fecha
        },
        'productos' : {
            'id_color': lambda id: Color.query.get(id).nombre_color,
            'id_categoria': lambda id: Categoria.query.get(id).tipo_categoria,
            'id_detalle_tamaños': lambda id: DetalleTamaño.query.get(id).tamaño,
            'id_marca': lambda id: Marca.query.get(id).nombre_marca,
            'id_material': lambda id: Material.query.get(id).nombre_material,
            'id_genero': lambda id: Genero.query.get(id).nombre_genero,
            'id_usuario': lambda id: User.query.get(id).username,
        }
    }

    # Apply the updates based on the table name
    for registry in table_body:
        if table in table_updates:
            for field, update_func in table_updates[table].items():
                registry[field] = update_func(registry[field])

    print(table_body)

    return table_body


@app.route("/data/<table>/columns", methods=["GET"])
@roles_required("admin")
def columns(table):
    table_columns = db.select_columns(table=db[table])
    print(table_columns)
    return table_columns


# * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -
# * EXTRAS -------------------------------------------------------------------------*
# * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * - * -

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
