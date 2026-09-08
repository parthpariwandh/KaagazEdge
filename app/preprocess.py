"""CPU-side image helpers. No model inference here."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from PIL import Image


def inspect_image(path: str | Path) -> dict[str, Any]:
    image_path = Path(path)
    with Image.open(image_path) as img:
        img.load()
        width, height = img.size
        mode = img.mode
    return {
        "path": str(image_path),
        "name": image_path.name,
        "width": width,
        "height": height,
        "mode": mode,
        "megapixels": round((width * height) / 1_000_000, 3),
    }
