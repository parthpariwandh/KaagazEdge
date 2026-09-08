"""Model router for Qualcomm AI Hub artifacts on Snapdragon HP PCs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

MODELS_DIR = Path("models")

DEMO_INVOICE = {
    "document_type": "gst_invoice",
    "supplier_name": "Sample Traders Kolkata",
    "supplier_gstin": "19AAAAA0000A1Z5",
    "buyer_name": "Riverside Workshop",
    "invoice_number": "INV-2026-0142",
    "invoice_date": "2026-09-01",
    "place_of_supply": "West Bengal",
    "taxable_value": 10000.0,
    "cgst": 900.0,
    "sgst": 900.0,
    "igst": 0.0,
    "grand_total": 11800.0,
    "currency": "INR",
    "confidence": 0.62,
}
DEMO_MARKSHEET = {
    "document_type": "marksheet",
    "student_name": "A. Banerjee",
    "roll_number": "JU/ME/23/0142",
    "institution": "Jadavpur University",
    "board_or_university": "Jadavpur University",
    "examination": "B.E. Mechanical Semester Review",
    "year": "2026",
    "result": "Pass",
    "confidence": 0.58,
}
DEMO_CLINIC = {
    "document_type": "clinic_report",
    "patient_label": "Desk copy only",
    "facility": "Neighbourhood Diagnostics",
    "report_date": "2026-09-02",
    "test_name": "Routine panel",
    "finding_summary": "Operator must confirm printed values before filing.",
    "doctor_name": "Not extracted",
    "confidence": 0.51,
}
DEMO_JOB = {
    "document_type": "job_card",
    "workshop_name": "Campus workshop",
    "machine_name": "Lathe station 3",
    "asset_tag": "ME-LAT-03",
    "fault_description": "Belt slip reported on morning shift",
    "spares_needed": "Drive belt, lock washers",
    "safety_notes": "Isolate power before opening the guard",
    "confidence": 0.55,
}
DEMOS = {
    "invoice": DEMO_INVOICE,
    "marksheet": DEMO_MARKSHEET,
    "clinic_report": DEMO_CLINIC,
    "job_card": DEMO_JOB,
}


class ModelRouter:
    def __init__(self, offline: bool = True) -> None:
        self.offline = offline
        self.has_npu_artifacts = self._discover_artifacts()

    def _discover_artifacts(self) -> bool:
        if not MODELS_DIR.exists():
            return False
        return any(MODELS_DIR.glob("*.onnx")) or any(MODELS_DIR.glob("*.bin"))

    def runtime_banner(self) -> dict[str, Any]:
        return {
            "npu_artifacts_present": self.has_npu_artifacts,
            "mode": "qnn" if self.has_npu_artifacts else "stub",
            "offline": self.offline,
            "target": "Snapdragon powered HP PC",
        }

    def transcribe(self, audio_path: str, language: str) -> str:
        name = Path(audio_path).name
        if not self.has_npu_artifacts:
            spoken = {
                "en": "Please post CGST and SGST and mark this paid after export.",
                "hi": "CGST aur SGST chadha dein aur export ke baad payment ankita karein.",
                "bn": "CGST o SGST bosan, export er por porishod chinhito korun.",
            }.get(language, "")
            return f"[stub transcript language={language} file={name}] {spoken}"
        raise NotImplementedError("Attach Whisper QNN session when Hub artifacts are in models/.")

    def document_fields(self, image_path: str, schema_name: str, language: str) -> dict[str, Any]:
        base = dict(DEMOS.get(schema_name, {"document_type": schema_name, "confidence": 0.3}))
        base["language"] = language
        base["source_image"] = Path(image_path).name
        if not self.has_npu_artifacts:
            base["extraction_mode"] = "stub"
            return base
        raise NotImplementedError("Attach document VLM QNN session when Hub artifacts are in models/.")

    def structure(self, vision: dict[str, Any], speech: str, schema: dict[str, Any], language: str) -> dict[str, Any]:
        record = dict(vision)
        record["voice_notes"] = speech
        record.setdefault("confidence", 0.4)
        record["schema_title"] = schema.get("title", "")
        record["needs_human_confirm"] = float(record.get("confidence") or 0) < 0.85
        record["language"] = language
        record["compute"] = self.runtime_banner()
        return record
