"""KaagazEdge inference orchestration.

Real NPU sessions are loaded when compiled Qualcomm AI Hub artifacts
are present under ./models. Otherwise the pipeline returns structured
stubs so the UI and schema path can be developed on any PC.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.models_runtime import ModelRouter


SCHEMA_DIR = Path(__file__).parent / "schemas"


class KaagazPipeline:
    def __init__(self, offline: bool = True) -> None:
        self.offline = offline
        self.router = ModelRouter(offline=offline)

    def available_schemas(self) -> list[str]:
        return sorted(p.stem for p in SCHEMA_DIR.glob("*.json"))

    def load_schema(self, name: str) -> dict[str, Any]:
        path = SCHEMA_DIR / f"{name}.json"
        if not path.exists():
            raise FileNotFoundError(name)
        return json.loads(path.read_text(encoding="utf-8"))

    def run(
        self,
        image_path: str | None,
        audio_path: str | None,
        schema_name: str,
        language: str = "en",
    ) -> dict[str, Any]:
        schema = self.load_schema(schema_name)
        vision = self.router.document_fields(image_path, schema_name, language) if image_path else {}
        speech = self.router.transcribe(audio_path, language) if audio_path else ""
        merged = self.router.structure(vision, speech, schema, language)
        merged["language"] = language
        merged["offline"] = self.offline
        merged["device_target"] = "Snapdragon powered HP PC"
        return merged
