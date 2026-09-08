"""Local export helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from openpyxl import Workbook


SKIP = {"letter", "image_meta", "compute", "validation_errors"}


def to_xlsx(record: dict[str, Any], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "KaagazEdge"
    ws.append(["Field", "Value"])
    for key, value in record.items():
        if key in SKIP:
            continue
        if isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        ws.append([key, str(value)])
    if record.get("letter"):
        ws2 = wb.create_sheet("Letter")
        ws2.append(["Draft letter"])
        ws2.append([record["letter"]])
    wb.save(dest)
    return dest


def to_json(record: dict[str, Any], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return dest
