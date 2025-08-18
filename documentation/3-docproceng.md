# Document Processing Engine – Python Implementation

## Responsibilities
- Compile ordered pages into a single PDF.
- Merge static PDFs with dynamic ones.
- Fill in PDF forms with customer attributes.
- Resolve choosable pages based on attributes.
- Extract specific tabs from Excel files and render them as PDF pages.
- Produce a final downloadable PDF.

---

## Core Processing Steps

1. **Load Book Definition**
   - Query DB for the book’s ordered pages.
   - For each page, determine its type (static, form, choosable, Excel).

2. **Resolve Page Data**
   - **Static Page** → Fetch and append PDF.
   - **PDF Form (Fillable)** → Fill fields with customer attributes, flatten PDF, append.
   - **Choosable Page** → Check customer attribute → Insert correct PDF.
   - **Excel Page** → Extract specified tab → Convert to PDF page → Append.

3. **Assemble Final Document**
   - Sequentially merge all page PDFs into a single PDF.
   - Add metadata (title, customer info, generation date).
   - Save and provide link to user.

---

## PDF Handling (Python)

- PyPDF2 → Merge/split, metadata, page operations.
- ReportLab → Render new PDF pages (text, images, tables).
- pdfrw or borb → Optional: form reading/writing/filling.
- Optional: WeasyPrint when rendering HTML→PDF (e.g., Excel tab rendered as HTML).

**Recommendation**
- Use PyPDF2 + ReportLab as the default.
- Add borb for richer form support if needed.

---

## Excel Handling (Python)

1. **Reading Excel**
   - openpyxl (load workbook, select tab, read cells)
   - pandas (optional convenience over tabular data)

2. **Converting Excel Tab → PDF**
   - Convert worksheet to HTML (via pandas `to_html`) → render to PDF (WeasyPrint), or
   - Render with ReportLab directly (tables, styles), or
   - Use LibreOffice headless for pixel-perfect conversion:
     - `libreoffice --headless --convert-to pdf input.xlsx --outdir output`

**Recommendation**
- openpyxl → pandas → ReportLab for flexible layout.
- Use LibreOffice headless only if exact Excel fidelity is required.

---

## Workflow Orchestration (Python)

- **Synchronous (small jobs)**: Process within request lifecycle (FastAPI/Flask).
- **Asynchronous (recommended)**: Submit job to Celery worker, notify user on completion.
  - Broker: Redis or RabbitMQ
  - Result backend: Redis or database
  - Notification: WebSocket, polling endpoint, or email

---

## Example Implementation (Python)

```python
from pathlib import Path
from typing import Dict, List, Optional
from PyPDF2 import PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import openpyxl
import io

class Page:
    def __init__(self, type: str, filepath: Optional[str] = None, tab_name: Optional[str] = None):
        self.type = type
        self.filepath = filepath
        self.tab_name = tab_name

class Book:
    def __init__(self, id: str, pages: List[Page]):
        self.id = id
        self.pages = pages

def fill_pdf_form(src_pdf: str, data: Dict[str, str]) -> bytes:
    # Option A: pdfrw/borb to set form fields then return flattened bytes
    # Placeholder: render data onto a fresh canvas and overlay if no forms exist
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    # ... drawString/image as needed using `data` ...
    c.showPage()
    c.save()
    return buf.getvalue()

def excel_tab_to_pdf(xlsx_path: str, tab: str) -> bytes:
    # Option A: render with ReportLab directly
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    ws = wb[tab]

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    y = 750
    for row in ws.iter_rows(values_only=True):
        line = " | ".join("" if v is None else str(v) for v in row)
        c.drawString(36, y, line[:110])
        y -= 14
        if y < 36:
            c.showPage()
            y = 750
    c.showPage()
    c.save()
    return buf.getvalue()

def generate_book(customer: Dict, book: Book, spreadsheet: Optional[str] = None) -> str:
    merger = PdfMerger()

    for page in book.pages:
        if page.type == "static":
            merger.append(page.filepath)

        elif page.type == "pdf_form":
            filled = fill_pdf_form(page.filepath, customer.get("attributes", {}))
            tmp = io.BytesIO(filled)
            merger.append(tmp)

        elif page.type == "choosable":
            # Resolve `page.filepath` by customer attributes (implementation-specific)
            merger.append(page.filepath)

        elif page.type == "excel":
            assert spreadsheet and page.tab_name
            tab_pdf_bytes = excel_tab_to_pdf(spreadsheet, page.tab_name)
            tmp = io.BytesIO(tab_pdf_bytes)
            merger.append(tmp)

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{customer['id']}_{book.id}.pdf"
    with open(output_file, "wb") as f:
        merger.write(f)
    merger.close()

    return str(output_file)
```

---

## Operational Concerns

- Logging each step with correlation IDs (customer_id, book_id).
- Idempotency: deduplicate requests or version outputs.
- Storage: write to local in dev; S3/GCS/Azure in prod with signed URLs.
- Security: sanitize uploads, restrict file types, size limits, virus scanning if required.


