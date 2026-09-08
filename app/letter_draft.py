"""Local letter draft from a confirmed record. No network."""

from __future__ import annotations

from typing import Any


TEMPLATES = {
    "en": (
        "To whom it may concern,\n\n"
        "This note is generated on the local KaagazEdge clerk from a confirmed record.\n"
        "Document type: {document_type}\n"
        "Key fields: {fields}\n"
        "Voice note: {voice_notes}\n\n"
        "Please treat this as an operator-confirmed desk copy, not a legally attested original.\n\n"
        "Yours faithfully,\nKaagazEdge local clerk\n"
    ),
    "hi": (
        "Seva mein,\n\n"
        "Yeh patra sthanaya KaagazEdge clerk dwara pushti kiye gaye record se bana hai.\n"
        "Document type: {document_type}\n"
        "Key fields: {fields}\n"
        "Voice note: {voice_notes}\n\n"
        "Ise mool praman patra na maanein.\n\n"
        "Bhavadiya,\nKaagazEdge\n"
    ),
    "bn": (
        "Barabor,\n\n"
        "Ei chithi sthanio KaagazEdge clerk theke nishchit record diye toiri.\n"
        "Document type: {document_type}\n"
        "Key fields: {fields}\n"
        "Voice note: {voice_notes}\n\n"
        "Eti mul sonod noy.\n\n"
        "Dhonnobadante,\nKaagazEdge\n"
    ),
}


def draft_letter(record: dict[str, Any], language: str = "en") -> str:
    skip = {
        "document_type", "language", "confidence", "needs_human_confirm",
        "voice_notes", "schema_title", "offline", "device_target", "compute",
        "source_image", "image_meta", "validation_errors", "letter", "record_id",
    }
    fields = ", ".join(
        f"{key}={value}" for key, value in record.items() if key not in skip and value not in (None, "", [])
    )
    template = TEMPLATES.get(language, TEMPLATES["en"])
    return template.format(
        document_type=record.get("document_type", "record"),
        fields=fields or "none extracted",
        voice_notes=record.get("voice_notes") or "none",
    )
