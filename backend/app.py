import json
from pathlib import Path
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

import torch
from backend.inference.efficientnet_v2_s import EfficientNetV2
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

from backend.model import predict

def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0
        lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
        c = 2*atan2(sqrt(a), sqrt(1-a))
        return R * c
    
if not Path("config.json").exists():
    raise FileNotFoundError("No se encontró el archivo de configuración 'config.json' en el directorio raíz del proyecto.")

with open("config.json") as f:
    config = json.load(f)
    
app = Flask(__name__, 
                template_folder=Path("../frontend/templates"),
                static_folder=Path("../frontend/static"))

app.secret_key = f"{config['secret_key']}"

app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{config['db_user']}:{config['db_password']}@localhost:3306/perros_app"
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
        __tablename__ = "mascotas_perdidas"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        path_imagen = db.Column(db.String(255), nullable=False)
        raza = db.Column(db.String(50), nullable=False)
        latitud = db.Column(db.Float, nullable=False)
        longitud = db.Column(db.Float, nullable=False)
        fecha = db.Column(db.DateTime, default=datetime.now())
        username = db.Column(db.String(50), nullable=False)
        
class ShelterReport(db.Model):
        __tablename__ = "mascotas_acogidas"

        id = db.Column(db.Integer, primary_key=True, autoincrement=True)
        path_imagen = db.Column(db.String(255), nullable=False)
        raza = db.Column(db.String(50), nullable=False)
        latitud = db.Column(db.Float, nullable=False)
        longitud = db.Column(db.Float, nullable=False)
        fecha = db.Column(db.DateTime, default=datetime.now())
        protectora = db.Column(db.String(50), nullable=False)

UPLOAD_FOLDER = Path(__file__).parent.parent / "frontend" / "static" / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True, parents=True)
SHELTER_UPLOAD_FOLDER = Path(__file__).parent.parent / "frontend" / "static" / "shelters_uploads"
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
    username = session.get("nombre")
    if not username:
        return jsonify({"error": "Invalid session"}), 401
    
    if session.get("account_type") != "user":
        return jsonify({"error": "Unauthorized"}), 403
    
    if "imagen" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    if not request.form.get("latitud") or not request.form.get("longitud"):
        return jsonify({"error": "Missing coordinates"}), 400

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
    category = predict(app.config['MODEL'], file_path, app.config['DEVICE'])  

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
    
    protected_reports = ShelterReport.query.filter_by(raza=category).all()
    
    nearby_protected = [
    {
        "raza": r.raza,
        "latitud": r.latitud,
        "longitud": r.longitud,
        "path_imagen": r.path_imagen,
        "protectora": r.protectora,
        "timestamp":  r.fecha.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "distancia_km": haversine(latitude, longitude, float(r.latitud), float(r.longitud))
    }
    for r in protected_reports]
    
    return jsonify({
        "reporte_usuario": report,
        "protegidos_similares": nearby_protected
    })
    
@app.route("/report", methods=["POST"])
def report_protected_pet():
    shelter = session.get("nombre")
    if not shelter:
        return jsonify({"error": "Invalid session"}), 401
    
    if session.get("account_type") != "shelter":
        return jsonify({"error": "Unauthorized"}), 403
    
    if "imagen" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    if not request.form.get("latitud") or not request.form.get("longitud"):
        return jsonify({"error": "Missing coordinates"}), 400

    file = request.files["imagen"]
    original_name = secure_filename(file.filename)
    shelter_folder = SHELTER_UPLOAD_FOLDER / shelter
    shelter_folder.mkdir(exist_ok=True, parents=True)
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
    suffix = Path(original_name).suffix
    stem = Path(original_name).stem       
    unique_filename = f"{stem}_{timestamp_str}{suffix}"
    file_path = shelter_folder / unique_filename
    file.save(file_path)

    latitude = float(request.form.get("latitud"))
    longitude = float(request.form.get("longitud"))
    category = predict(app.config['MODEL'], file_path, app.config['DEVICE']) 
    
    protected = ShelterReport.query.all()
    protected_reports = [
    {
        "raza": r.raza,
        "latitud": r.latitud,
        "longitud": r.longitud,
        "path_imagen": r.path_imagen,
        "protectora": r.protectora,
        "fecha":  r.fecha.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "distancia_km": haversine(latitude, longitude, float(r.latitud), float(r.longitud))
    }
    for r in protected]
        
    db.session.add(ShelterReport(
        path_imagen=f"/static/shelters_uploads/{shelter}/{unique_filename}",
        raza=category,
        latitud=float(latitude),
        longitud=float(longitude),
        protectora=shelter
    ))
    db.session.commit()
    
    current_report = {
        "raza": category,
        "latitud": latitude,
        "longitud": longitude,
        "fecha": timestamp.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "protectora": session["nombre"],
        "path_imagen": f"static/shelters_uploads/{shelter}/{unique_filename}"
    }
    
    lost = LostReport.query.all()
    
    lost_reports = [
    {
        "raza": r.raza,
        "latitud": r.latitud,
        "longitud": r.longitud,
        "path_imagen": r.path_imagen,
        "usuario": r.username,
        "fecha":  r.fecha.strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "distancia_km": haversine(latitude, longitude, float(r.latitud), float(r.longitud))
    }
    for r in lost]
    
    return jsonify({
        "reporte_actual":  current_report,
        "perdidos": lost_reports,
        "protegidos": protected_reports
    })
    
@app.route("/shelter/maps", methods=["GET"])
def shelter_maps():
    shelter = session.get("nombre")
    if not shelter:
        return jsonify({"error": "Invalid session"}), 401

    if session.get("account_type") != "shelter":
        return jsonify({"error": "Unauthorized"}), 403

    protected_reports = ShelterReport.query.filter_by(protectora=shelter).all()
    return jsonify({
        "protegidos": [
            {
                "raza": r.raza,
                "latitud": r.latitud,
                "longitud": r.longitud,
                "path_imagen": r.path_imagen,
                "protectora": r.protectora,
                "fecha": r.fecha.strftime("%a, %d %b %Y %H:%M:%S GMT")
            }
            for r in protected_reports
        ],
        "perdidos": [
            {
                "raza": r.raza,
                "latitud": r.latitud,
                "longitud": r.longitud,
                "path_imagen": r.path_imagen,
                "usuario": r.username,
                "fecha": r.fecha.strftime("%a, %d %b %Y %H:%M:%S GMT")
            }
            for r in LostReport.query.all()
        ]
    })

if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = EfficientNetV2(num_classes=18)
    model_path = Path(__file__).parent / 'inference' / 'models' / 'best.pth'
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    app.config['MODEL'] = model
    app.config['DEVICE'] = device
    app.run(debug=True)