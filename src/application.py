from flask import Flask, render_template, url_for, request, flash, redirect, sessions, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from funciones import *
import json

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


items = [
    {
        'id_item': 1,
        'sku': '0001',
        'description': 'Laptop Hp Pavilion',
        'price': 500,
        'stock': 10,
        'maintenance_fee': 7,
        'id_category': 1,
        'id_product_detail': 1
    },
    {
        'id_item': 2,
        'sku': '0002',
        'description': 'Laptop Dell inspiron',
        'price': 680,
        'stock': 9,
        'maintenance_fee': 7,
        'id_category': 1,
        'id_product_detail': 1
    },
]


# Obtener todos los items
@app.route('/', methods=['GET'])
def get_items():
    return jsonify(items)

# Obtener un item por su ID


@app.route('/inventory/<int:id_item>', methods=['GET'])
def get_item(id_item):
    item = next((item for item in items if item['id_item'] == id_item), None)
    if item:
        return jsonify(items)
    return jsonify({'message': 'item no encontrado'}), 404

# Agregar un nuevo item


@app.route('/addItem', methods=['POST'])
def add_item():
    new_item = {
        'id_item': len(items) + 1,
        'sku': request.json['sku'],
        'description': request.json['description'],
        'price': request.json['price'],
        'stock': request.json['stock'],
        'maintenance_fee': request.json['maintenance_fee'],
        'id_category': request.json['id_category'],
        'id_product_detail': request.json['id_product_detail']
    }
    items.append(new_item)
    return jsonify({'message': 'item agregado', 'item': new_item}), 201

# Actualizar un libro existente


@app.route('/inventory/<int:id_item>', methods=['PUT'])
def update_item(id_item):
    item = next((item for item in items if item['id_item'] == id_item), None)
    if item:
        item['title'] = request.json['title']
        item['author'] = request.json['author']
        return jsonify({'message': 'Libro actualizado', 'item': item})
    return jsonify({'message': 'Libro no encontrado'}), 404

# Eliminar un libro


@app.route('/inventory/<int:id_item>', methods=['DELETE'])
def delete_item(id_item):
    item = next((item for item in items if item['id_item'] == id_item), None)
    if item:
        items.remove(item)
        return jsonify({'message': 'item eliminado'})
    return jsonify({'message': 'item no encontrado'}), 404


# Iniciar sesion
@app.route("/signIn", methods=["POST", "GET"])
def signIn():
    if request.method == 'POST':
        # obtenemos valores del formulario
        username = request.form.get("username")
        password = request.form.get("password")

        if not request.form.get("username"):
            flash('Ingrese un nombre de usuario')
            return redirect("/signIn")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Ingrese una contraseña')
            return redirect("/signIn")

        user = db.execute(
            "SELECT * FROM users WHERE username = '"+str(username)+"'").fetchall()

        # Ensure username exists and password is correct
        if len(user) != 1 or not check_password_hash(user[0][2], password):
            flash('Nombre de usuario ó contraseña Incorrecta')
            return redirect("/signIn")

        # Remember which user has logged in
        session["id_user"] = user[0][0]
        session["username"] = username
        # session["role_user"] = user[0][5]
        return redirect('/')

    else:
        return render_template("signIn.html", ruta="Login")

# registro de nuevo usuario


@app.route("/signUp", methods=["POST", "GET"])
def signUp():
    if request.method == 'POST':
        # obtenemos valores del formulario
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        country = request.form.get("country")
        city = request.form.get("city")
        age = request.form.get("age")
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")

        if not request.form.get("name"):
            flash('Ingrese su nombre')
            return redirect("/signUp")

        if not request.form.get("lastname"):
            flash('Ingrese su apellido')
            return redirect("/signIn")

        if not request.form.get("country"):
            flash('Seleccione un pais de origen')
            return redirect("/signIn")

        if not request.form.get("email"):
            flash('Ingrese un email')
            return redirect("/signIn")

        if not request.form.get("username"):
            flash('Ingrese un nombre de usuario')
            return redirect("/signIn")

        if not request.form.get("username"):
            flash('Ingrese un nombre de usuario')
            return redirect("/signUp")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Ingrese una contraseña')
            return redirect("/signUp")

        user = db.execute(
            "SELECT * FROM users WHERE username = '"+str(username)+"'").fetchall()

        eml = db.execute(
            "SELECT * FROM users WHERE email = '"+str(email)+"'").fetchall()

        if len(user) > 0:
            flash('El nombre de usuario ingresado ya existe')
            return redirect("/signUp")

        elif len(user) > 0:
            flash('la dirección de correo electronico ingresada ya esta en uso')
            return redirect("/signUp")
        else:
            # Query database for person
            db.execute("INSERT INTO person (name,lastname,age,email,country,city) VALUES ('"+str(name) +
                       "','"+str(lastname)+"',"+str(age)+",'"+str(email)+"','"+str(country)+"','"+str(city)+"')")
            db.commit()
            # Query selection id person
            user = db.execute(text(
                "SELECT * FROM person WHERE email = '"+email+"'")).fetchall()

            # Query database for users
            db.execute(text("INSERT INTO users (username,password,id_person,id_role) VALUES ('" +
                       str(username)+"','"+str(password)+"',"+str(user[0][0])+",2)"))
            db.commit()

            flash('¡Cuenta creada exitosamente!')
            # Redirect user to login page
            return redirect("/signIn")

    else:
        return render_template("signUp.html", ruta="registro")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
