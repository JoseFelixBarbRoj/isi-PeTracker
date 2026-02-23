# PeTracker — Agent Context

> This file provides a concise, authoritative reference for AI coding assistants working on this codebase.
> Read this before touching any file. Keep it updated when you make structural changes.

---

## Project Purpose

**PeTracker** is a server-rendered Flask web application that helps reunite lost pets with their owners.

- **Users** upload a photo and share their GPS location. The ML model classifies the dog/cat breed and the backend returns nearby shelter matches for the same breed.
- **Shelters** register pets they have taken in, with a photo and GPS coordinates.

---

## Repository Layout

```
ISITest/
├── backend/
│   ├── app.py              # Flask app: routes, ORM models, Haversine helper
│   ├── model.py            # ML inference wrapper — exposes predict(image_path) -> str
│   └── inference/
│       ├── efficientnet_v2_s.py   # EfficientNetV2 model class (PyTorch)
│       ├── dataset.py             # PetDataset (torch.utils.data.Dataset)
│       ├── trainer.py             # Training loop
│       ├── train_model.py         # Training entry-point (run as a module)
│       ├── metrics.py             # accuracy helper
│       ├── data/
│       │   └── data.csv           # CSV with 'class' column → 18 breed labels
│       └── models/
│           └── best.pth           # Trained EfficientNetV2-S weights
├── frontend/
│   ├── templates/                 # Jinja2 HTML templates
│   │   ├── login.html             # Root login page
│   │   ├── choose_login.html      # Choose user vs shelter
│   │   ├── user_login.html
│   │   ├── shelter_login.html
│   │   ├── user.html              # User dashboard (AJAX predict trigger)
│   │   ├── shelter.html           # Shelter dashboard
│   │   ├── upload.html
│   │   ├── shelter_report.html
│   │   └── shelter_map.html
│   └── static/
│       ├── main.js                # AJAX calls, map rendering (Leaflet)
│       ├── styles.css
│       ├── stylesUser.css
│       ├── stylesShelter.css
│       ├── uploads/               # Auto-created; stores user-uploaded images
│       └── shelter_uploads/       # Auto-created; stores shelter-uploaded images
├── testing/
├── pyproject.toml                 # Package: "petracker", Python ≥ 3.12
└── PROJECT.md                     # Detailed human-readable documentation
```

---

## Running the App

```bash
# Start the development server
cd backend
python app.py          # http://127.0.0.1:5000  (debug mode)
```

```bash
# Train the model from scratch
python -m backend.inference.train_model
```

> **Prerequisite**: MySQL must be running at `localhost:3306` with a schema named `perros_app`.
> SQLAlchemy creates tables automatically on first startup.

---

## Tech Stack

| Layer | Library / Tool |
|---|---|
| Web framework | Flask |
| ORM | Flask-SQLAlchemy |
| Database | MySQL via PyMySQL |
| ML | PyTorch + torchvision (EfficientNetV2-S) |
| Image decoding | OpenCV (`cv2.IMREAD_COLOR_RGB`) |
| Data | Pandas, NumPy |
| Python version | ≥ 3.12 |
| Package build | Hatchling (`pyproject.toml`) |

---

## Database (MySQL — `perros_app`)

Connection string (edit in `backend/app.py`):
```python
"mysql+pymysql://<user>:<password>@localhost:3306/perros_app"
```

### ORM Models → Tables

| SQLAlchemy Model | Table | PK | Notable Columns |
|---|---|---|---|
| `User` | `usuarios` | `nombre` (VARCHAR 50) | `contraseña_hash` |
| `Shelter` | `protectoras` | `nombre` (VARCHAR 50) | `contraseña_hash` |
| `LostReport` | `mascotas_perdidas` | `id` (AUTO INCREMENT) | `path_imagen`, `raza`, `latitud`, `longitud`, `fecha`, `username` |
| `ShelterReport` | `mascotas_acogidas` | `id` (AUTO INCREMENT) | `path_imagen`, `raza`, `latitud`, `longitud`, `fecha`, `protectora` |

> ⚠️ Passwords are stored as **plain text** in `contraseña_hash`. Do not assume hashing is in place.

---

## Routes

| Method | Path | Session Required | Purpose |
|---|---|---|---|
| `GET` | `/` | — | Render login page |
| `POST` | `/login` | — | Authenticate; redirect to `/user` or `/shelter` |
| `GET` | `/user` | `account_type == "user"` | User dashboard |
| `GET` | `/shelter` | `account_type == "shelter"` | Shelter dashboard |
| `GET` | `/logout` | — | Clear session, redirect to `/` |
| `POST` | `/predict` | `account_type == "user"` | Upload image + coords → classify, save `LostReport`, return JSON matches |

### `/predict` Contract

**Request** (`multipart/form-data`):

| Field | Type |
|---|---|
| `imagen` | File (image) |
| `latitud` | String (float) |
| `longitud` | String (float) |

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

Distance is computed using the **Haversine formula** (R = 6371 km) in `haversine()` inside `app.py`.

---

## ML Pipeline

### Model: `EfficientNetV2-S`

- Defined in `backend/inference/efficientnet_v2_s.py`.
- Custom head: `EfficientNetV2-S → ReLU → Dropout(0.1) → Linear(1000 → num_classes)`.
- **18 classes** (dog and cat breeds) loaded from `backend/inference/data/data.csv` (`class` column, sorted, deduplicated).
- Weights file: `backend/inference/models/best.pth`.

### Inference (`model.py → predict(image_path)`)

1. Load weights onto CPU or CUDA.
2. Read image with `cv2.IMREAD_COLOR_RGB`, normalize to `[0, 1]` (`/= 255.0`).
3. Forward pass → softmax → argmax → map to breed string via `IDX_TO_CLASSNAME`.
4. Returns the predicted breed name as a `str` (or `None` if the image cannot be read).

> ⚠️ The model is **reloaded from disk on every call** to `predict()`. For production, load it once at startup.

### Training

- Entry point: `python -m backend.inference.train_model`
- Images resized to `224 × 224`; augmentations: random H/V flip, colour jitter.
- Optimiser: Adam (lr=0.001), Loss: CrossEntropyLoss, 100 epochs.
- Best checkpoint saved to `backend/inference/models/`.

---

## Session & Auth

Session keys set on login:

| Key | Value |
|---|---|
| `logged_in` | `True` |
| `account_type` | `"user"` or `"shelter"` |
| `nombre` | Username / shelter name |

Routes guard with `session.get("account_type") != "user"` (redirect to `/`) or return 401/403 JSON for `/predict`.

> `app.secret_key` is `"secret-key"` — marked provisional in source. Use an environment variable in production.

---

## File Upload Convention

- User images saved to: `frontend/static/uploads/<username>/<stem>_<YYYYMMDD_HHMMSS><ext>`
- Stored path in DB: `/static/uploads/<username>/<filename>`
- Shelter images saved to: `frontend/static/shelter_uploads/`
- Stored path in DB: `/static/shelter_uploads/<filename>`

Both directories are created automatically with `mkdir(exist_ok=True, parents=True)`.

---

## Key Gotchas & Conventions

1. **`app.py` must be run from `backend/`** — relative path resolution for templates, static files, and model weights depends on the CWD.
2. **`model.py` uses `backend.inference.efficientnet_v2_s`** — this import only works when the project root is on `sys.path` (i.e., when run as a package or with `pip install -e .`).
3. **MySQL schema must exist** before first run; tables are auto-created by SQLAlchemy (`db.create_all()`).
4. **`best.pth` is not version-controlled** — you must place it manually at `backend/inference/models/best.pth`.
5. **No password hashing** — `contraseña_hash` stores plain-text passwords. Add hashing before any real deployment.
6. **No foreign keys** — relationships between tables (`username` in `mascotas_perdidas`, `protectora` in `mascotas_acogidas`) are enforced in application logic only, not at the DB level.
7. **Shelter match is breed-exact** — `/predict` queries `ShelterReport.query.filter_by(raza=category)`. All matching-breed shelters are returned regardless of distance; the caller's JS must sort/filter by `distancia_km`.
8. **`data.csv` drives class ordering** — the `IDX_TO_CLASSNAME` dict is built by sorting unique values of the `class` column. Any reordering of classes in the CSV without retraining will break predictions.

---

## Development Checklist (for AI agents)

- [ ] Do not change column names in ORM models without a matching MySQL migration.
- [ ] Any new route should mirror the existing session-guard pattern.
- [ ] If you add a breed / modify `data.csv`, retrain the model — do not patch `IDX_TO_CLASSNAME` manually.
- [ ] Keep template folder (`frontend/templates/`) and static folder (`frontend/static/`) paths consistent with the `Flask(...)` constructor in `app.py`.
- [ ] Run `pip install -e .` after adding new dependencies to `pyproject.toml`.
