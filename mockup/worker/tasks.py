from typing import Optional, Dict
from worker.celery_app import celery_app
from doc_engine.generator import generate_book as run_generate_book
from doc_engine.models import Book, Page


@celery_app.task
def generate_book_task(customer_id: str, book_id: str, spreadsheet_path: Optional[str] = None) -> str:
    customer: Dict[str, object] = {"id": customer_id, "attributes": {}}
    # Placeholder: construct a minimal empty Book. Integrate real DB lookups later.
    book = Book(id=book_id, pages=[])
    return run_generate_book(customer, book, spreadsheet_path)
