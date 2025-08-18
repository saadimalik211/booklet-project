from typing import Dict
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
import io


def fill_pdf_form(src_pdf: str, data: Dict[str, object]) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    y_position = 750
    for key, value in data.items():
        c.drawString(36, y_position, f"{key}: {value}")
        y_position -= 14
        if y_position < 36:
            c.showPage()
            y_position = 750
    c.showPage()
    c.save()
    return buffer.getvalue()
