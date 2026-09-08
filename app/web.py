"""Local web desk. Binds to localhost. Does not call cloud models."""

from __future__ import annotations

import shutil
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.export_util import to_xlsx
from app.pipeline import KaagazPipeline
from app.schema_validate import available_schemas
from app.storage import LocalStore

ROOT = Path(__file__).resolve().parent.parent
UPLOADS = ROOT / "data" / "local" / "uploads"
EXPORTS = ROOT / "data" / "local" / "exports"
TEMPLATES = Path(__file__).resolve().parent / "templates"
STATIC = Path(__file__).resolve().parent / "static"

UPLOADS.mkdir(parents=True, exist_ok=True)
EXPORTS.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="KaagazEdge", docs_url=None, redoc_url=None)
if STATIC.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC)), name="static")

pipe = KaagazPipeline(offline=True)
store = LocalStore()


def _save_upload(upload: UploadFile | None, prefix: str) -> str | None:
    if upload is None or not upload.filename:
        return None
    suffix = Path(upload.filename).suffix or ".bin"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    dest = UPLOADS / f"{prefix}_{stamp}{suffix}"
    with dest.open("wb") as handle:
        shutil.copyfileobj(upload.file, handle)
    return str(dest)


@app.get("/", response_class=HTMLResponse)
def home() -> HTMLResponse:
    page = TEMPLATES / "index.html"
    return HTMLResponse(page.read_text(encoding="utf-8"))


@app.get("/api/health")
def health() -> dict:
    return {
        "product": "KaagazEdge",
        "offline": True,
        "schemas": available_schemas(),
        "compute": pipe.router.runtime_banner(),
    }


@app.post("/api/extract")
async def extract(
    schema_name: str = Form("invoice"),
    language: str = Form("en"),
    image: UploadFile | None = File(default=None),
    audio: UploadFile | None = File(default=None),
) -> dict:
    if schema_name not in available_schemas():
        raise HTTPException(status_code=400, detail="Unknown schema")
    if language not in {"en", "hi", "bn"}:
        raise HTTPException(status_code=400, detail="Language must be en, hi, or bn")
    image_path = _save_upload(image, "page")
    audio_path = _save_upload(audio, "voice")
    if not image_path and not audio_path:
        raise HTTPException(status_code=400, detail="Attach a page photo or a voice note")
    record = pipe.run(image_path, audio_path, schema_name, language)
    record["record_id"] = store.save(schema_name, record)
    return record


@app.post("/api/confirm")
async def confirm(payload: dict) -> dict:
    schema_name = payload.get("schema_name") or "invoice"
    record = payload.get("record") or payload
    record["needs_human_confirm"] = False
    record["confirmed"] = True
    record["record_id"] = store.save(schema_name, record)
    export_path = EXPORTS / f"kaagazedge_{record['record_id']}.xlsx"
    to_xlsx(record, export_path)
    record["export_path"] = str(export_path)
    return record


@app.get("/api/export/{record_id}")
def export_file(record_id: int) -> FileResponse:
    path = EXPORTS / f"kaagazedge_{record_id}.xlsx"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Export not found. Confirm the record first.")
    return FileResponse(path, filename=path.name)


@app.get("/api/records")
def records() -> dict:
    return {"items": store.list_recent(25)}
