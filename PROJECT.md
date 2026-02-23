# PeTracker

> A web application that helps locate lost pets by combining GPS-based reporting with AI-powered dog breed classification.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Technology Stack](#technology-stack)
4. [Database Schema](#database-schema)
5. [API & Routes](#api--routes)
6. [ML Pipeline](#ml-pipeline)
7. [Project Structure](#project-structure)
8. [Installation & Setup](#installation--setup)
9. [Running the Application](#running-the-application)

---

## Project Overview

PeTracker allows two types of accounts:

- **Users** – report a lost pet by uploading a photo and sharing their GPS location. The system classifies the dog breed automatically and stores the report.
- **Shelters** – register pets they have taken in, also with a photo and GPS location.

After a user submits a lost-pet report, the backend queries the shelter database for pets of the same predicted breed and returns a list of nearby matches, including distance (km), to help reunite pets with their owners.

---

## Architecture

```
Browser
  │
  ▼
Flask (app.py)
  ├── Jinja2 Templates  (frontend/templates/)
  ├── Static Assets     (frontend/static/)
  ├── SQLAlchemy ORM    ──► MySQL DB (perros_app)
  └── ML Inference      ──► model.py ──► EfficientNetV2 (best.pth)
```

The application is a **server-rendered Flask MVC app** with one AJAX endpoint (`/predict`) that returns JSON. All other pages are rendered via Jinja2 templates.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Web framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | MySQL (via PyMySQL) |
| ML framework | PyTorch + torchvision |
| Image processing | OpenCV (`opencv-python`) |
| Data manipulation | Pandas, NumPy |
| Packaging | Hatchling (`pyproject.toml`) |
| Python version | ≥ 3.12 |

---

## Database Schema

The database name is **`perros_app`**, configured via MySQL at `localhost:3306`.

### `usuarios` — Regular Users

| Column | Type | Constraints |
|---|---|---|
| `nombre` | VARCHAR(50) | **PRIMARY KEY** |
| `contraseña_hash` | VARCHAR(255) | NOT NULL |

> Mapped by SQLAlchemy model `User`.

---

### `protectoras` — Animal Shelters

| Column | Type | Constraints |
|---|---|---|
| `nombre` | VARCHAR(50) | **PRIMARY KEY** |
| `contraseña_hash` | VARCHAR(255) | NOT NULL |

> Mapped by SQLAlchemy model `Shelter`.

---

### `mascotas_perdidas` — Lost Pet Reports (submitted by users)

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | **PRIMARY KEY**, AUTO INCREMENT |
| `path_imagen` | VARCHAR(255) | NOT NULL — relative URL to the uploaded image |
| `raza` | VARCHAR(50) | NOT NULL — breed predicted by the ML model |
| `latitud` | FLOAT | NOT NULL |
| `longitud` | FLOAT | NOT NULL |
| `fecha` | DATETIME | DEFAULT `datetime.now()` |
| `username` | VARCHAR(50) | NOT NULL — name of the reporting user |

> Mapped by SQLAlchemy model `LostReport`.

---

### `mascotas_acogidas` — Shelter-Registered Pets

| Column | Type | Constraints |
|---|---|---|
| `id` | INTEGER | **PRIMARY KEY**, AUTO INCREMENT |
| `path_imagen` | VARCHAR(255) | NOT NULL — relative URL to the uploaded image |
| `raza` | VARCHAR(50) | NOT NULL — breed predicted by the ML model |
| `latitud` | FLOAT | NOT NULL |
| `longitud` | FLOAT | NOT NULL |
| `fecha` | DATETIME | DEFAULT `datetime.now()` |
| `protectora` | VARCHAR(50) | NOT NULL — name of the shelter |

> Mapped by SQLAlchemy model `ShelterReport`.

---

## API & Routes

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/` | None | Render login page |
| `POST` | `/login` | None | Authenticate user or shelter; redirect to dashboard |
| `GET` | `/user` | `user` session | Render user dashboard |
| `GET` | `/shelter` | `shelter` session | Render shelter dashboard |
| `GET` | `/logout` | Any | Clear session and redirect to login |
| `POST` | `/predict` | `user` session | Upload pet image + coordinates → classify breed, save `LostReport`, return nearby shelter matches as JSON |

### `/predict` — Request / Response

**Request** (`multipart/form-data`):

| Field | Type | Description |
|---|---|---|
| `imagen` | File | Pet photo |
| `latitud` | String (float) | Reporter's GPS latitude |
| `longitud` | String (float) | Reporter's GPS longitude |

**Response** (`application/json`):

```json
{
  "reporte_usuario": {
    "raza": "Golden Retriever",
    "latitud": 40.4168,
    "longitud": -3.7038,
    "fecha": "Mon, 23 Feb 2026 18:00:00 GMT",
    "username": "juan",
    "path_imagen": "static/uploads/juan/photo_20260223_180000.jpg"
  },
  "protegidos_similares": [
    {
      "raza": "Golden Retriever",
      "latitud": 40.42,
      "longitud": -3.71,
      "path_imagen": "/static/shelter_uploads/...",
      "protectora": "Refugio Madrid",
      "timestamp": "Mon, 23 Feb 2026 10:00:00 GMT",
      "distancia_km": 0.73
    }
  ]
}
```

Distance is computed with the **Haversine formula** (Earth radius = 6371 km).

---

## ML Pipeline

### Model

- **Architecture**: `EfficientNetV2-S` (torchvision pretrained backbone) with a custom classification head:
  ```
  EfficientNetV2-S → ReLU → Dropout(0.1) → Linear(1000 → num_classes)
  ```
- **Classes**: 18 dog and cat breeds, loaded at startup from `backend/inference/data/data.csv`.
- **Saved weights**: `backend/inference/models/best.pth`.

### Inference (`model.py` → `predict(image_path)`)

1. Load `best.pth` onto CPU or CUDA.
2. Read image with OpenCV (RGB), normalize to `[0, 1]`.
3. Run forward pass; argmax of softmax gives the predicted class index.
4. Map index → breed name via `IDX_TO_CLASSNAME` dict.

### Training (`backend/inference/train_model.py`)

- Input images resized to `224 × 224`.
- Augmentations: random horizontal/vertical flip, colour jitter.
- Optimiser: Adam, lr = 0.001; Loss: CrossEntropyLoss.
- 100 epochs; best checkpoint saved to `backend/inference/models/`.

---

## Project Structure

```
ISITest/
├── backend/
│   ├── app.py                     # Flask application, routes, ORM models
│   ├── model.py                   # ML inference wrapper (predict function)
│   └── inference/
│       ├── efficientnet_v2_s.py   # EfficientNetV2 model definition
│       ├── dataset.py             # PetDataset (PyTorch Dataset)
│       ├── trainer.py             # Training loop
│       ├── train_model.py         # Training entry point
│       ├── metrics.py             # Accuracy function
│       ├── data/
│       │   └── data.csv           # Class labels CSV
│       └── models/
│           └── best.pth           # Trained model weights
├── frontend/
│   ├── templates/
│   │   ├── login.html
│   │   ├── user.html              # User dashboard
│   │   ├── shelter.html           # Shelter dashboard
│   │   ├── upload.html
│   │   ├── shelter_report.html
│   │   ├── shelter_map.html
│   │   ├── choose_login.html
│   │   ├── user_login.html
│   │   └── shelter_login.html
│   └── static/
│       ├── main.js                # Frontend JS (AJAX, map rendering)
│       ├── styles.css
│       ├── stylesUser.css
│       ├── stylesShelter.css
│       ├── uploads/               # User-uploaded lost-pet images (auto-created)
│       └── shelter_uploads/       # Shelter-uploaded pet images
├── testing/
├── pyproject.toml                 # Package metadata & dependencies
└── README.md
```

---

## Installation & Setup

> Requires **Python 3.12+** and a running **MySQL** instance.

### 1. Clone the repository

```bash
git clone https://github.com/JoseFelixBarbRoj/GSI.git
cd GSI
```

### 2. Create and activate a virtual environment *(recommended)*

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### 3. Install the package

```bash
# End users
pip install .

# Developers (editable mode)
pip install -e .
```

### 4. Configure the database

Edit the connection string in `backend/app.py`:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://<user>:<password>@localhost:3306/perros_app"
)
```

Create the `perros_app` schema in MySQL before running the app; SQLAlchemy will create the tables automatically on first startup.

### 5. Place the trained model weights

Copy `best.pth` to:

```
backend/inference/models/best.pth
```

---

## Running the Application

```bash
cd backend
python app.py
```

The server starts in debug mode at `http://127.0.0.1:5000`.

### Training the model from scratch

```bash
python -m backend.inference.train_model
```

Ensure `backend/inference/data/data.csv` and the corresponding image dataset are present before running.
