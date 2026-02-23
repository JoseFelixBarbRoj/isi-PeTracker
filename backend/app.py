from pathlib import Path
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

from model import predict

def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2*atan2(sqrt(a), sqrt(1-a))
        return R * c
    
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
        
class LostReport(db.Model):
        __tablename__ = "perros_perdidos"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        path_imagen = db.Column(db.String(255), nullable=False)
        raza = db.Column(db.String(50), nullable=False)
        latitud = db.Column(db.Float, nullable=False)
        longitud = db.Column(db.Float, nullable=False)
        fecha = db.Column(db.DateTime, default=datetime.now())
        username = db.Column(db.String(50), nullable=False)
        
class ShelterReport(db.Model):
        __tablename__ = "perros_acogidos"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        path_imagen = db.Column(db.String(255), nullable=False)
        raza = db.Column(db.String(50), nullable=False)
        latitud = db.Column(db.Float, nullable=False)
        longitud = db.Column(db.Float, nullable=False)
        fecha = db.Column(db.DateTime, default=datetime.now())
        protectora = db.Column(db.String(50), nullable=False)
        
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


@app.route("/predict", methods=["POST"])
def predict_image():
    if not session or session["account_type"] != "user":
        return jsonify({"error": "Unauthorized"}), 401

    username = session["nombre"]
    file = request.files["imagen"]
    original_name = secure_filename(file.filename)
    user_folder = UPLOAD_FOLDER / username
    user_folder.mkdir(exist_ok=True, parents=True)
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    suffix = Path(original_name).suffix
    stem = Path(original_name).stem       
    unique_filename = f"{stem}_{timestamp_str}{suffix}"
    file_path = user_folder / unique_filename
    file.save(file_path)

    latitude = float(request.form.get("latitud"))
    longitude = float(request.form.get("longitud"))
    category = predict(file_path)  

    db.session.add(LostReport(
        path_imagen=f"/static/uploads/{username}/{unique_filename}",
        raza=category,
        latitud=float(latitude),
        longitud=float(longitude),
        username=username
    ))
    db.session.commit()
    report = {
        "raza": category,
        "latitud": latitude,
        "longitud": longitude,
        "fecha": timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "username": session["nombre"],
        "path_imagen": f"static/uploads/{username}/{unique_filename}"
    }
    protected_reports = db.session.query(ShelterReport).all()
    nearby_protected = [
    {
        "category": r.raza,
        "latitude": r.latitud,
        "longitude": r.longitud,
        "relative_path": r.path_imagen,
        "shelter_name": r.protectora,
        "timestamp":  r.fecha.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "distancia_km": haversine(latitude, longitude, float(r.latitud), float(r.longitud))
    }
    for r in protected_reports
    if r.raza == category]
    return jsonify({
        "reporte_usuario": report,
        "protegidos_similares": nearby_protected
    })
    
if __name__ == "__main__":
    app.run(debug=True)

