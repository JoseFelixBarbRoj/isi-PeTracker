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
10. [Frontend Behaviour](#frontend-behaviour)

---

## Project Overview

PeTracker allows two types of accounts:

- **Users** – report a lost pet by uploading a photo and sharing their GPS location. The system classifies the dog breed automatically and stores the report.
- **Shelters** – register pets they have taken in, also with a photo and GPS location.

After a user submits a lost-pet report, the backend queries the shelter database for pets of the same predicted breed and returns a list of nearby matches, including distance (km), to help reunite pets with their owners. Shelters can also register pets and see nearby lost pets or other sheltered pets of the same breed in realtime.

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

The application is a **server-rendered Flask MVC app** with AJAX endpoints (`/predict` and `/report`) that return JSON data for map rendering and frontend functionality. All other pages are rendered via Jinja2 templates.

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
| `POST` | `/report` | `shelter` session | Upload pet image + coordinates → classify breed, save `ShelterReport`, return similar lost/protected pets |

### `/predict` — Request / Response (Users)

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
    "path_imagen": "static/uploads/juan/juan_2026...jpg"
  },
  "protegidos_similares": [
    {
      "raza": "Golden Retriever",
      "latitud": 40.42,
      "longitud": -3.71,
      "path_imagen": "/static/shelters_uploads/...",
      "protectora": "Refugio Madrid",
      "timestamp": "Mon, 23 Feb 2026 10:00:00 GMT",
      "distancia_km": 0.73
    }
  ]
}
```

### `/report` — Request / Response (Shelters)

**Request** (`multipart/form-data`): Same format as `/predict`.

**Response** (`application/json`): Returns the current shelter report, and lists of all overall lost pets and protected shelter pets.

```json
{
  "reporte_actual": {
    "raza": "Labrador",
    "latitud": 40.41,
    "longitud": -3.70,
    "fecha": "Mon, 23 Feb 2026 18:00:00 GMT",
    "protectora": "Veterinaria Madrid",
    "path_imagen": "static/shelters_uploads/..."
  },
  "perdidos": [
    {
      "raza": "Labrador",
      "latitud": 40.45,
      "longitud": -3.68,
      "path_imagen": "/static/uploads/...",
      "usuario": "roberto",
      "fecha": "Mon, 23 Feb 2026 10:00:00 GMT",
      "distancia_km": 5.12
    }
  ],
  "protegidos": [
    // Array of similar shelter reports
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
│   │   ├── login.html             # Login interface
│   │   ├── user.html              # User dashboard
│   │   └── shelter.html           # Shelter dashboard (veterinary clinic profile view)
│   └── static/
│       ├── main.js                # Frontend JS (AJAX, map rendering, notifications)
│       ├── styles.css
│       ├── stylesUser.css
│       ├── stylesShelter.css
│       ├── assets/                # Static images used in the frontend
│       ├── uploads/               # User-uploaded lost-pet images
│       └── shelters_uploads/      # Shelter-uploaded pet images
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

Create a `config.json` file in the root directory:

```json
{
  "db_user": "root",
  "db_password": "yourpassword"
}
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

---

## Frontend Behaviour

The frontend is implemented using Flask server-rendered templates (Jinja2) combined with a lightweight client-side script (`main.js`) responsible for handling user interaction, geolocation, and map rendering.

Static assets are stored in `frontend/static/` and include:

- `styles.css` – styling for the login interface  
- `stylesUser.css` – styling for the user dashboard  
- `stylesShelter.css` – styling for the shelter / veterinary dashboard  
- `main.js` – client-side logic for the user upload process and maps  

---

## User Interface

Three main HTML templates are currently implemented:

| Page | Purpose |
|------|----------|
| `login.html` | Unified login interface for both users and shelters |
| `user.html` | Dashboard for reporting lost pets (upload photo, get location) and visualizing matches on a map |
| `shelter.html` | Dedicated dashboard for shelters and veterinary clinics with a verified profile view, quick checklist for attending found pets, and map interface. Includes fields for adding pet reports to the system. |

The user interface is styled using dedicated CSS files and designed to be responsive for different screen sizes.

---

## Client-Side Logic (`main.js`)

The file `main.js` implements the main frontend behaviour for user reporting. It is executed after the page loads via the `DOMContentLoaded` event.

### Key Responsibilities

#### Notification Permission

At startup, the script requests browser notification permission using the Web Notification API, allowing for future real-time alerts.

#### Image Upload Handling

The upload interface supports click-to-select and drag-and-drop mechanics. It offers real-time image previews before submission. The **Analyze** button remains disabled until an image is securely selected, preventing empty/invalid requests.

#### Geolocation Retrieval & Submission

When the user submits the form, the script retrieves their precise geocoordinates using the browser's Geolocation API (`navigator.geolocation`). 

This data (Image, Latitude, and Longitude) is then cleanly bundled into a `FormData` object and transmitted securely to the `/predict` backend endpoint using the JavaScript `Fetch` API.

#### Map Rendering

Results returned from the backend are displayed dynamically using **Leaflet.js**.

The function `drawMap(data, maxDistance)`:
- Initializes an interactive Leaflet map centered at the user's location.
- Drops a distinct blue marker for the user's report.
- Plots red markers for all nearby matching shelter reports.
- Employs popups indicating the match's distance, shelter name, breed, date, and their captured image.

#### Distance Filtering

The UI enables real-time map filtering by distance (5 km, 10 km, 20 km, 50 km). Applying a filter seamlessly refreshes the map layer via client-side processing, presenting only shelter pets falling within the chosen radii without spamming backend endpoints.