"""KaagazEdge inference orchestration."""

from __future__ import annotations

from typing import Any

from app.letter_draft import draft_letter
from app.models_runtime import ModelRouter
from app.preprocess import inspect_image
from app.schema_validate import available_schemas, load_schema, validate_record


class KaagazPipeline:
    def __init__(self, offline: bool = True) -> None:
        self.offline = offline
        self.router = ModelRouter(offline=offline)

    def available_schemas(self) -> list[str]:
        return available_schemas()

    def run(
        self,
        image_path: str | None,
        audio_path: str | None,
        schema_name: str,
        language: str = "en",
        draft: bool = True,
    ) -> dict[str, Any]:
        if schema_name not in available_schemas():
            raise ValueError(f"Unsupported schema: {schema_name}")
        schema = load_schema(schema_name)
        vision: dict[str, Any] = {}
        image_meta = None
        if image_path:
            image_meta = inspect_image(image_path)
            vision = self.router.document_fields(image_path, schema_name, language)
        speech = self.router.transcribe(audio_path, language) if audio_path else ""
        merged = self.router.structure(vision, speech, schema, language)
        merged["language"] = language
        merged["offline"] = self.offline
        merged["device_target"] = "Snapdragon powered HP PC"
        if image_meta:
            merged["image_meta"] = image_meta
        merged["validation_errors"] = validate_record(schema_name, _schema_view(merged, schema))
        if merged["validation_errors"]:
            merged["needs_human_confirm"] = True
        if draft:
            merged["letter"] = draft_letter(merged, language)
        return merged


def _schema_view(record: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    properties = schema.get("properties", {})
    return {key: record[key] for key in properties if key in record}
