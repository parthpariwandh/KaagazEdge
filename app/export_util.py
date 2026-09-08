"""Local export helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from openpyxl import Workbook


def to_xlsx(record: dict[str, Any], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    wb = Workbook()
    ws = wb.active
    ws.title = "KaagazEdge"
    ws.append(["Field", "Value"])
    for key, value in record.items():
        if key == "line_items":
            continue
        ws.append([key, str(value)])
    wb.save(dest)
    return dest
