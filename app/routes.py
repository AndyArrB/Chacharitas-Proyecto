from flask import render_template, request, jsonify
from flask_security import roles_required

from app import app
from app.database import Database
from app.forms.modal_form import generate_dynamic_form

# * Instancia para el contacto con nuestra base de datos
db = Database()

# * Para llenar las opciones en el <navbar> lateral
tables = db.select_tables()


# * APP ------------------------------------------------------------------------------

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
    products = db.select_all(table=db["productos"])
    genders = db.select_all(table=db["generos"])
    categories = db.select_all(table=db["categorias"])
    return render_template("shop.html", products=products, genders=genders, categories=categories)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/shop-single")
def shop_single():
    return render_template("shop-single.html")

    # ? Rutas complejas. Se encargan del filtrado del front.


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

        filtered_products = db.select_filtered_products(price_ranges=price_ranges, categories=categories,
                                                        genders=genders, sort_by=sort_by)
        try:
            products_json = jsonify(filtered_products)
            return products_json
        except Exception as e:
            print(f"Error converting products to JSON: {e}")
            return jsonify({"error": "Error converting products to JSON"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# * CRUD -----------------------------------------------------------------------------

# ? Establece las rutas de nuestro servidor. Todas las peticiones de la página se
# ? redirigen aquí

# ? Rutas principales. Estas son las que responden ante las solicitudes HTTP
# ? del cliente.

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
@roles_required("admin")
def body(table):
    table_body = db.select_all(table=db[table])
    table_body = [row._asdict() for row in table_body]
    return table_body


@app.route("/data/<table>/columns", methods=["GET"])
@roles_required("admin")
def columns(table):
    table_columns = db.select_columns(table=db[table])
    print(table_columns)
    return table_columns
