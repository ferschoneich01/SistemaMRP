from flask import Flask, render_template, url_for, request, flash, redirect, sessions
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


# ruta principal


@app.route("/")
def index():
    return render_template("index.html", ruta="inicio")

# ruta informacion

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

#registro
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

        if not request.form.get("username"):
            flash('Ingrese un nombre de usuario')
            return redirect("/signUn")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Ingrese una contraseña')
            return redirect("/signUn")

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
        return render_template("signIn.html", ruta="registro")


@app.route("/sub")
def sub():
    return render_template("subIndex.html", ruta="sub")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
