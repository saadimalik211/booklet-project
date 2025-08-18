# Backend – Architecture and Components

## Overview
Backend provides APIs, persistence, file storage access, and an asynchronous document processing engine to generate final PDF booklets.

- Language/Runtime: Python 3
- API Framework: FastAPI
- Worker/Queue: Celery + Redis/RabbitMQ
- Database/ORM: PostgreSQL + SQLAlchemy + Alembic
- PDF/Excel: PyPDF2, ReportLab, openpyxl (WeasyPrint/borb optional)
- Storage: Local (dev), S3/GCS/Azure (prod via signed URLs)

---

## Core Components

### API Server (FastAPI)
- Pydantic schemas for request/response validation
- Routers for auth, customers, books, pages, uploads, jobs
- Dependency injection (DB session, auth user)
- Error handling and OpenAPI docs
- CORS and basic rate limiting

### Authentication & Authorization
- OAuth2/JWT (access/refresh tokens)
- Role-based permissions (admin vs standard)
- Middleware/Deps for protecting routes

### Database & ORM
- PostgreSQL with SQLAlchemy models and Alembic migrations
- Transactions for multi-step writes
- Indices on common lookup keys (customer_id, book_id)

### File Storage
- Dev: local filesystem
- Prod: S3 (or equivalent) with signed URLs, per-tenant prefixes, lifecycle policies
- Upload validation (type/size), checksum (MD5/SHA-256), optional AV scan

### Document Processing Engine (Worker)
- PDF merging/form-filling via PyPDF2 (+ ReportLab overlay)
- Excel tab rendering via openpyxl → ReportLab (HTML→PDF optional via WeasyPrint)
- Deterministic pipeline: resolve pages → render/compose → output PDF
- Temp file/stream management and cleanup

### Asynchronous Job Queue
- Celery tasks: generate_book, cleanup, (optional: preview/thumbnail)
- Status lifecycle: queued → running → done | error
- Progress reporting via DB/Redis; retries with backoff

### Observability
- Structured logging with correlation IDs (request_id, job_id)
- Metrics (request latency, job durations, error rates)
- Health/readiness endpoints
- Optional tracing via OpenTelemetry

### Security
- Strict MIME/extension checks, file size caps
- Path traversal protection, sandboxed temp dirs
- Signed URL expiry and least-privilege IAM for storage
- Input validation for all endpoints

---

## Baseline API Endpoints

- Auth
  - POST `/auth/login` – issue tokens
  - POST `/auth/refresh` – refresh token
  - POST `/auth/logout`

- Customers
  - GET/POST `/customers`
  - GET/PUT/DELETE `/customers/{customer_id}`
  - GET/POST `/customers/{customer_id}/attributes`

- Books
  - GET/POST `/books`
  - GET/PUT/DELETE `/books/{book_id}`

- Pages
  - GET/POST `/books/{book_id}/pages`
  - GET/PUT/DELETE `/books/{book_id}/pages/{page_id}`

- Uploads
  - POST `/uploads` (PDF/XLSX)
  - GET `/uploads/{upload_id}` (metadata)

- Generation
  - POST `/books/{book_id}/generate` (body: customer_id, optional spreadsheet upload)
  - GET `/jobs/{job_id}` (status)
  - GET `/downloads/{file_id}` (signed URL/proxy)

---

## Minimal Data Model

- customers(id, name, created_at)
- customer_attributes(id, customer_id, key, value, year, quarter)
- books(id, name, description)
- pages(id, book_id, type, order_index, config_json, upload_id)
- page_conditions(id, page_id, attribute_key, attribute_value, target_upload_id)
- uploads(id, file_path, file_type, size, uploaded_by, uploaded_at, checksum)
- jobs(id, type, status, input_json, output_file_id, error, created_at, updated_at)

Notes:
- `pages.type ∈ {static, pdf_form, choosable, excel}`
- `config_json` carries per-page config (e.g., tab name for excel, form field mapping)
- `page_conditions` used to resolve choosable pages from attributes

---

## Document Generation Flow

1. API receives POST `/books/{book_id}/generate` with `customer_id` (and spreadsheet upload if needed)
2. Validate inputs → enqueue Celery task → return `job_id`
3. Worker loads book/pages and customer attributes
4. Resolve choosable pages using `page_conditions` + attributes
5. For each page:
   - static → append PDF
   - pdf_form → fill fields (overlay/flatten) then append
   - excel → render worksheet tab to PDF page and append
6. Merge to final PDF; write to storage; record output as `uploads` entry
7. Update job status to `done` (or `error` with details)
8. Client polls `GET /jobs/{job_id}`; on done, fetch `GET /downloads/{file_id}`

---

## Backend Project Structure (suggested)

- app/
  - main.py (FastAPI init)
  - routers/ (auth, customers, books, pages, uploads, jobs)
  - schemas/ (Pydantic models)
  - deps.py (DB session, auth deps)
- domain/
  - models.py (SQLAlchemy)
  - repositories/ (DB access)
  - services/ (business logic)
- worker/
  - celery_app.py
  - tasks.py (generate_book, etc.)
- doc_engine/
  - pdf.py (form filling/overlay)
  - excel.py (tab → PDF)
  - generator.py (orchestrates merge)
- infra/
  - db.py (engine/session)
  - storage.py (local/S3)
  - settings.py (BaseSettings)
  - logging.py
- migrations/ (Alembic)
- output/ (local dev output)

---

## Configuration & Secrets

- Pydantic BaseSettings (env-driven):
  - DATABASE_URL, CELERY_BROKER_URL, CELERY_RESULT_BACKEND
  - STORAGE_BUCKET, STORAGE_PREFIX, SIGNED_URL_TTL
  - JWT_SECRET, JWT_EXPIRES_IN
- Separate profiles for dev/stage/prod; `.env` only for local

---

## Running Locally (dev)

1) Create venv and install deps
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r mockup/requirements.txt`

2) Start API
- `uvicorn mockup.app.main:app --reload`

3) Start worker
- `export CELERY_BROKER_URL=redis://localhost:6379/0`
- `export CELERY_RESULT_BACKEND=redis://localhost:6379/1`
- `celery -A mockup.worker.celery_app.celery_app worker --loglevel=INFO`

4) Storage
- Dev: files written to `output/`
- Prod: configure S3/GCS and signed URLs
