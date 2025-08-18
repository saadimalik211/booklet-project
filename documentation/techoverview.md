# Booklet PDF Maker – Technical Architecture (Python Stack)

## System Components

### 1. **Frontend (Web UI)**
- **Responsibilities**
  - Manage Customers, Attributes, and Books.
  - Page editor for defining Books and ordering Pages.
  - File upload interface for PDFs and Excel spreadsheets.
  - Trigger Book generation & download final PDF.
- **Tech Stack**
  - React
  - Tailwind CSS
  - Auth via JWT / OAuth2

---

### 2. **Backend (API Layer)**
- **Responsibilities**
  - CRUD for Customers, Attributes, Books, Pages.
  - Store mappings for Choosable Pages and Attribute rules.
  - Orchestrate PDF merging, form field population, Excel parsing.
  - Expose REST/GraphQL endpoints.
- **Tech Stack (Python)**
  - FastAPI (async, OpenAPI docs) or Django REST Framework
  - PDF: PyPDF2 + ReportLab (+ borb/pdfrw for complex forms)
  - Excel: openpyxl (+ pandas optional)
  - Auth: OAuth2 Password/JWT (FastAPI), or Django Auth/JWT

---

### 3. **Document Processing Engine**
- **Responsibilities**
  - Generate Books into final PDFs (merge static + dynamic).
  - Populate form fields and render Excel worksheets.
  - Queue long-running jobs; provide status tracking.
- **Tech Stack (Python)**
  - Celery + Redis/RabbitMQ (worker + broker)
  - HTML→PDF: WeasyPrint (optional) or ReportLab direct rendering
  - Headless LibreOffice (optional) for Excel→PDF fidelity

---

### 4. **Database**
- **Responsibilities**
  - Persist Customers, Attributes (versioned year+quarter), Books, Pages, metadata.
  - Store references to uploaded files.
- **Schema (simplified)**
  - `customers(id, name, created_at)`
  - `customer_attributes(id, customer_id, key, value, year, quarter)`
  - `books(id, name, description)`
  - `pages(id, book_id, type, order_index, config_json)`
  - `uploads(id, file_path, file_type, uploaded_by, uploaded_at)`
- **Tech Stack**
  - PostgreSQL
  - SQLAlchemy (or Django ORM) + Alembic migrations

---

### 5. **File Storage**
- **Responsibilities**
  - Store static PDFs, Excel uploads, generated books.
  - Secure access for downloads.
- **Options**
  - Local (dev)
  - Cloud: AWS S3 / GCS / Azure Blob (signed URLs)

---

### 6. **Authentication & Authorization**
- **Responsibilities**
  - Secure access for users.
  - Role-based permissions (Admin vs. Standard).
- **Stack**
  - FastAPI OAuth2 + JWT (PyJWT), or Django + DRF SimpleJWT

---

### 7. **Deployment & Infrastructure**
- **Responsibilities**
  - Containerized services (API + Worker + Redis + DB).
  - CI/CD pipeline; observability.
- **Stack**
  - Docker + Docker Compose / Kubernetes
  - CI/CD: GitHub Actions / GitLab CI
  - Monitoring: Prometheus + Grafana
  - Logging: OpenTelemetry + Loki/ELK

---

## High-Level Flow

1. User selects Customer + Book; uploads spreadsheet if required.
2. API validates inputs; enqueues Celery job with `customer_id`, `book_id`, `upload_id`.
3. Worker loads definitions, generates in order, writes final PDF to storage.
4. API exposes job status and download link when complete.

---

## Example Endpoints (FastAPI)

- `POST /books/{book_id}/generate` → enqueues job; returns `job_id`
- `GET /jobs/{job_id}` → status: queued | running | done | error
- `GET /downloads/{file_id}` → signed URL or proxy download

---

## Key Considerations
- **Scalability**: Horizontal worker pool; backpressure on queue.
- **Extensibility**: Pluggable page types via strategy pattern.
- **Auditability**: Persist generation logs, inputs, and output metadata.
- **Versioning**: Books and attributes snapshot per generation request.


