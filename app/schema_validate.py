"""JSON Schema checks for extracted records."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

SCHEMA_DIR = Path(__file__).parent / "schemas"


def load_schema(name: str) -> dict[str, Any]:
    path = SCHEMA_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Unknown schema: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def available_schemas() -> list[str]:
    return sorted(p.stem for p in SCHEMA_DIR.glob("*.json"))


def validate_record(name: str, record: dict[str, Any]) -> list[str]:
    schema = load_schema(name)
    validator = Draft202012Validator(schema)
    return [f"{'/'.join(str(p) for p in err.path) or 'root'}: {err.message}" for err in validator.iter_errors(record)]
