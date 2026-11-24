# ReportBox API – Test Catalog (FastAPI)

Backend for the Test catalog feature of ReportBox: full CRUD lifecycle for lab tests,
with automated integration tests.

## Stack
FastAPI · SQLAlchemy 2 · Pydantic v2 · SQLite · pytest + TestClient

## Run
```
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy pydantic pytest httpx
python run.py
```
API docs: http://127.0.0.1:8000/docs

## Endpoints
| Method | Path | Description | Success | Errors |
|---|---|---|---|---|
| POST | /tests | Create a lab test | 201 | 409 duplicate code, 422 invalid |
| GET | /tests | List all tests | 200 | – |
| GET | /tests/{id} | Get one test | 200 | 404 |
| PATCH | /tests/{id} | Update some fields | 200 | 404, 422 |
| DELETE | /tests/{id} | Delete a test | 204 | 404 |

## Integration tests
```
python -m pytest -v
```
Tests use a separate in-memory database (dependency override), so the real database is never touched.

| # | Test | Expected |
|---|---|---|
| 1 | Full lifecycle: create → get → list → update → delete → get | 201, 200, 200, 200, 204, 404 |
| 2 | List is empty at start | 200, [] |
| 3 | Duplicate code | 409 |
| 4 | Negative price | 422 |
| 5 | Lowercase code | 422 |
| 6 | Missing name | 422 |
| 7 | Get missing test | 404 |
| 8 | Update missing test | 404 |
| 9 | Update with invalid price | 422 |
| 10 | Delete missing test | 404 |