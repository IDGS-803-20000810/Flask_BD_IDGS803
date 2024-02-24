from flask import Flask, request, render_template, Response, g, redirect
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
import forms

from models import db
from models import Alumnos

app = Flask(__name__)
app.secret_key = "esta es la clave secreta"
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/index")
def index():
    escuela = "UTL"
    alumnos = ["Mario", "Pedro", "Luis", "Dario"]
    return render_template("index.html", escuela=escuela, alumnos=alumnos)


@app.route("/alumnos", methods=["GET", "POST"])
def alum():

    nom = ""
    apaterno = ""
    amaterno = ""
    alum_form = forms.UsersForm(request.form)
    if request.method == "POST" and alum_form.validate():
        nom = alum_form.nombre.data
        apaterno = alum_form.apaterno.data
        amaterno = alum_form.amaterno.data

        mensaje = "Bienvenido {}".format(nom)
        # flash(mensaje)

        # print("Nombre: {}".format(nom))
        # print("Apellido Paterno: {}".format(apaterno))
        # print("Apellido Materno: {}".format(amaterno))

    return render_template(
        "alumnos.html", form=alum_form, nom=nom, apa=apaterno, ama=amaterno
    )

if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
