import io
import openpyxl
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER


def excel_tab_to_pdf(xlsx_path: str, tab: str) -> bytes:
    workbook = openpyxl.load_workbook(xlsx_path, data_only=True)
    worksheet = workbook[tab]

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    y_position = 750
    for row in worksheet.iter_rows(values_only=True):
        line = " | ".join("" if cell is None else str(cell) for cell in row)
        c.drawString(36, y_position, line[:110])
        y_position -= 14
        if y_position < 36:
            c.showPage()
            y_position = 750
    c.showPage()
    c.save()
    return buffer.getvalue()
