# PeTracker — Agent Contract

> This file defines the behavioral, architectural, and safety constraints
> for AI coding agents working on this repository.
>
> This file is PRESCRIPTIVE.
> Do not duplicate descriptive documentation from PROJECT.md here.
>
> If you modify architecture, invariants, or core conventions,
> you MUST update this file.

---

# 1. Core Architectural Invariants

The system is a:

- Server-rendered Flask MVC application
- MySQL-backed relational system via SQLAlchemy
- ML-powered classification backend using PyTorch
- Single JSON API endpoint (`/predict`)
- Otherwise fully Jinja2-rendered

Do NOT convert this project into:
- A SPA frontend
- A REST-heavy API architecture
- A microservice architecture
- A different ORM
- A different web framework

Incremental improvement is allowed.
Architectural replacement is NOT.

---

# 2. Separation of Responsibilities

## Backend (`backend/`)
Responsible for:
- Routing
- Session/auth handling
- ORM models
- Haversine distance calculation
- ML inference orchestration

## Frontend (`frontend/`)
Responsible for:
- Rendering UI
- Triggering `/predict` via AJAX
- Displaying map results
- Sorting/filtering by distance client-side

The backend MUST NOT:
- Sort shelter matches by distance unless explicitly required
- Perform frontend rendering logic in JSON routes

The frontend MUST NOT:
- Recompute breed classification
- Reimplement distance logic

---

# 3. Database Rules

1. Do NOT rename ORM columns without a migration strategy.
2. Do NOT change primary keys.
3. Do NOT silently change column types.
4. There are currently NO foreign keys — relationships are enforced in application logic.
5. If foreign keys are introduced, update both PROJECT.md and this file.

Passwords are currently stored in plain text.
If hashing is introduced:
- Use a standard secure method (e.g., Werkzeug or bcrypt)
- Update authentication logic consistently
- Update this document

---

# 4. ML Inference Rules

- Class ordering is derived from `data.csv`.
- Changing class order WITHOUT retraining is forbidden.
- `best.pth` must match the class list.
- `predict(image_path)` must return `str | None`.

Current known limitation:
- Model is reloaded on every inference call.
If you optimize this (recommended), ensure:
- Thread safety
- No global CUDA side effects
- Startup-time load only once

Do NOT:
- Hardcode class names
- Patch `IDX_TO_CLASSNAME` manually
- Change image normalization without retraining

---

# 5. Session & Auth Rules

Session keys:
- `logged_in`
- `account_type`
- `nombre`

All protected routes MUST:
- Guard using `session.get("account_type")`
- Redirect or return 401/403 consistently

Never trust frontend-provided identity fields.
Use session state only.

---

# 6. File Upload & Storage Rules

Uploads must:
- Use timestamp-based naming
- Avoid overwriting files
- Store relative static paths in DB
- Ensure directories exist before saving

Do NOT:
- Store absolute system paths in the database
- Trust file extensions without validation
- Allow path traversal

---

# 7. Code Modification Principles

When modifying code:

1. Prefer minimal, surgical changes.
2. Avoid refactoring unrelated files.
3. Do not rename files without reason.
4. Maintain current folder structure.
5. Avoid introducing new dependencies unless justified.
6. Keep Python ≥ 3.12 compatibility.

If adding dependencies:
- Update `pyproject.toml`
- Mention installation requirement

---

# 8. Adding Features

When adding a feature:

- Follow existing session-guard patterns.
- Maintain MVC separation.
- Avoid business logic in templates.
- Keep ML logic inside `model.py` or inference module.
- Keep DB logic inside SQLAlchemy models.

If the feature:
- Changes data shape → update PROJECT.md.
- Changes architecture → update this file.
- Changes API contract → update both.

---

# 9. Performance Constraints

Current bottlenecks:
- Model reload per request.
- No DB indexing optimization.
- No pagination on queries.

Permitted improvements:
- Load model once at startup.
- Add DB indexes.
- Add pagination.
- Add caching layer (in-memory only).

Not permitted:
- External distributed caching.
- Architecture rewrite.

---

# 10. Safety Constraints

Never:
- Introduce eval/exec.
- Disable CSRF/session safety mechanisms.
- Expose raw stack traces in production mode.
- Log plaintext passwords.

---

# 11. Testing Expectations

If modifying:
- `/predict`
- ORM models
- Authentication logic
- ML inference logic

You must:
- Ensure no regression in JSON contract.
- Maintain backward compatibility unless explicitly instructed.

---

# 12. When To Update This File

Update this file ONLY when:

- Architecture changes
- Security model changes
- Database invariants change
- ML pipeline structure changes
- Core conventions change

Do NOT update this file for:
- UI tweaks
- CSS changes
- Minor bug fixes
- Template text changes

---

# Guiding Principle

Preserve stability.
Improve incrementally.
Do not introduce hidden architectural shifts.