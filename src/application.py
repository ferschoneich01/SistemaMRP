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

#
@app.route("/signIn")
def signIn():

    return render_template("login.html", ruta="Login")


@app.route("/sub")
def sub():
    return render_template("subIndex.html", ruta="sub")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)