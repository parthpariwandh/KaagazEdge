"""Model router for Qualcomm AI Hub artifacts on Snapdragon HP PCs."""

from __future__ import annotations

from pathlib import Path
from typing import Any


MODELS_DIR = Path("models")


class ModelRouter:
    def __init__(self, offline: bool = True) -> None:
        self.offline = offline
        self.has_npu_artifacts = any(MODELS_DIR.glob("*.onnx")) if MODELS_DIR.exists() else False

    def transcribe(self, audio_path: str, language: str) -> str:
        if not self.has_npu_artifacts:
            return (
                f"[stub transcript language={language} file={Path(audio_path).name}] "
                "Please post the CGST and SGST lines and mark this as paid after export."
            )
        raise NotImplementedError("Load Whisper QNN session from models/ when artifacts are exported.")

    def document_fields(self, image_path: str, schema_name: str, language: str) -> dict[str, Any]:
        if not self.has_npu_artifacts:
            if schema_name == "invoice":
                return {
                    "document_type": "gst_invoice",
                    "supplier_name": "Sample Traders Kolkata",
                    "invoice_number": "INV-2026-0142",
                    "invoice_date": "2026-09-01",
                    "grand_total": 11800.0,
                    "currency": "INR",
                    "confidence": 0.42,
                    "source_image": Path(image_path).name,
                    "language": language,
                }
            return {
                "document_type": schema_name,
                "confidence": 0.3,
                "source_image": Path(image_path).name,
                "language": language,
            }
        raise NotImplementedError("Load VLM QNN session from models/ when artifacts are exported.")

    def structure(
        self,
        vision: dict[str, Any],
        speech: str,
        schema: dict[str, Any],
        language: str,
    ) -> dict[str, Any]:
        record = dict(vision)
        record["voice_notes"] = speech
        record.setdefault("confidence", 0.4)
        record["schema_title"] = schema.get("title", "")
        record["needs_human_confirm"] = record.get("confidence", 0) < 0.85
        record["language"] = language
        return record
