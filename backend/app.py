from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, 
                template_folder=Path("../frontend/templates"),
                static_folder=Path("../frontend/static"))

app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:1234@localhost:3306/perros_app"  #Sustituir por user_password de mysql
    )
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
with app.app_context():
        db.create_all()

class User(db.Model):
        __tablename__ = "usuarios"

        nombre = db.Column(db.String(50), primary_key=True)
        contraseña_hash = db.Column(db.String(255), nullable=False)
        
class Shelter(db.Model):
        __tablename__ = "protectoras"

        nombre = db.Column(db.String(50), primary_key=True)
        contraseña_hash = db.Column(db.String(255), nullable=False)
        
app.secret_key = "secret-key"  # Provisional

UPLOAD_FOLDER = Path(__file__).parent.parent / "frontend" / "static" / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True, parents=True)
SHELTER_UPLOAD_FOLDER = Path(__file__).parent.parent / "frontend" / "static" / "shelter_uploads"
SHELTER_UPLOAD_FOLDER.mkdir(exist_ok=True, parents=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SHELTER_UPLOAD_FOLDER"] = SHELTER_UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    nombre = request.form.get("nombre")
    password = request.form.get("password")

    if not nombre or not password:
        return render_template("login.html", error="Usuario/Contraseña incorrectos")

    user = User.query.filter_by(nombre=nombre).first()
    if user and user.contraseña_hash == password:
        session["logged_in"] = True
        session["account_type"] = "user"
        session["nombre"] = user.nombre
        return redirect(url_for("user_dashboard"))

    shelter = Shelter.query.filter_by(nombre=nombre).first()
    if shelter and shelter.contraseña_hash == password:
        session["logged_in"] = True
        session["account_type"] = "shelter"
        session["nombre"] = shelter.nombre
        return redirect(url_for("shelter_dashboard"))

    return render_template("login.html", error="Invalid username or password")

@app.route("/user")
def user_dashboard():
    if session.get("account_type") != "user":
        return redirect(url_for("index"))
    return render_template("user.html", nombre=session["nombre"])


@app.route("/shelter")
def shelter_dashboard():
    if session.get("account_type") != "shelter":
        return redirect(url_for("index"))
    return render_template("shelter.html", nombre=session["nombre"])

@app.route("/logout")
def logout():
    session.clear() 
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

