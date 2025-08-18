from typing import Optional, Dict
from pathlib import Path
import io
from PyPDF2 import PdfMerger
from .models import Book
from .pdf import fill_pdf_form
from .excel import excel_tab_to_pdf


def generate_book(customer: Dict[str, object], book: Book, spreadsheet: Optional[str] = None) -> str:
    merger = PdfMerger()

    for page in book.pages:
        if page.type == "static" and page.filepath is not None:
            merger.append(page.filepath)
        elif page.type == "pdf_form" and page.filepath is not None:
            filled_bytes = fill_pdf_form(page.filepath, customer.get("attributes", {}))
            merger.append(io.BytesIO(filled_bytes))
        elif page.type == "choosable" and page.filepath is not None:
            merger.append(page.filepath)
        elif page.type == "excel":
            if spreadsheet is None or page.tab_name is None:
                raise ValueError("Excel page requires spreadsheet path and tab name")
            pdf_bytes = excel_tab_to_pdf(spreadsheet, page.tab_name)
            merger.append(io.BytesIO(pdf_bytes))

    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{customer['id']}_{book.id}.pdf"
    with open(output_path, "wb") as file_handle:
        merger.write(file_handle)
    merger.close()
    return str(output_path)
