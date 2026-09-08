from pathlib import Path
from PIL import Image
from app.letter_draft import draft_letter
from app.pipeline import KaagazPipeline


def test_pipeline_invoice_stub(tmp_path: Path):
    image = tmp_path / "page.png"
    Image.new("RGB", (800, 1100), color=(255, 255, 255)).save(image)
    pipe = KaagazPipeline(offline=True)
    record = pipe.run(str(image), None, "invoice", "en")
    assert record["document_type"] == "gst_invoice"
    assert record["offline"] is True
    assert record["compute"]["mode"] == "stub"
    assert record["needs_human_confirm"] is True
    assert "letter" in record


def test_pipeline_voice_only(tmp_path: Path):
    audio = tmp_path / "note.wav"
    audio.write_bytes(b"RIFF")
    pipe = KaagazPipeline(offline=True)
    record = pipe.run(None, str(audio), "job_card", "hi")
    assert "stub transcript" in record["voice_notes"]
    assert record["language"] == "hi"


def test_letter_languages():
    record = {"document_type": "gst_invoice", "supplier_name": "A", "voice_notes": ""}
    assert "To whom it may concern" in draft_letter(record, "en")
    assert draft_letter(record, "hi")
    assert draft_letter(record, "bn")
