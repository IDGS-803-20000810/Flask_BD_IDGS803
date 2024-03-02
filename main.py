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


@app.route("/index", methods=["GET", "POST"])
def index():
    alum_form = forms.UsersForm2(request.form)
    # if request.method == "POST" and alum_form.validate():
    if request.method == "POST":
        alum = Alumnos(nombre=alum_form.nombre.data,
                        apaterno=alum_form.apaterno.data,
                        email=alum_form.email.data)
        db.session.add(alum)
        db.session.commit()
        
    return render_template("index.html",form=alum_form)

@app.route("/eliminar",methods=["GET", "POST"])
def eliminar():
    alum_form=forms.UsersForm2(request.form)
    if request.method == "GET":
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum_form.id.data=request.args.get('id')
        alum_form.nombre.data=alum1.nombre
        alum_form.apaterno.data=alum1.apaterno
        alum_form.email.data=alum1.email
    if request.method == "POST" :
        id=alum_form.id.data
        alum=Alumnos.query.get(id)
        db.session.delete(alum)
        db.session.commit()
        return redirect('ABC_Completo')
    
    return render_template('eliminar.html',form=alum_form)

@app.route("/modificar",methods=["GET", "POST"])
def modificar():
    alum_form=forms.UsersForm2(request.form)
    if request.method == "GET":
        id=request.args.get('id')
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum_form.id.data=request.args.get('id')
        alum_form.nombre.data=alum1.nombre
        alum_form.apaterno.data=alum1.apaterno
        alum_form.email.data=alum1.email
    if request.method == "POST" :
        id=alum_form.id.data
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum1.nombre=alum_form.nombre.data
        alum1.apaterno=alum_form.apaterno.data
        alum1.email=alum_form.email.data
        db.session.add(alum1)
        db.session.commit()
        return redirect('ABC_Completo')
    
    return render_template('modificar.html',form=alum_form)
    
    

@app.route("/ABC_Completo", methods=["GET", "POST"])
def ABC_Completo():
    alum_form=forms.UsersForm2(request.form)
    alumno=Alumnos.query.all()
    return render_template('ABC_Completo.html',alumnos=alumno)

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
