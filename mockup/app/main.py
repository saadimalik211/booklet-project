from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import Optional, Dict
from worker.tasks import generate_book_task

app = FastAPI()


class GenerateRequest(BaseModel):
    customer_id: str
    book_id: str
    spreadsheet_tab_map: Optional[Dict[str, str]] = None


@app.post("/books/{book_id}/generate")
async def generate(book_id: str, req: GenerateRequest, spreadsheet: Optional[UploadFile] = None):
    upload_path: Optional[str] = None
    if spreadsheet is not None:
        upload_path = f"/tmp/{spreadsheet.filename}"
        content = await spreadsheet.read()
        with open(upload_path, "wb") as file_handle:
            file_handle.write(content)
    job = generate_book_task.delay(req.customer_id, book_id, upload_path)
    return {"job_id": str(job)}
