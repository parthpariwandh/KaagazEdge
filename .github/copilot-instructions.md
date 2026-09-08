# Copilot instructions for KaagazEdge

You are building KaagazEdge, an on device Indic document and voice clerk for Snapdragon powered HP PCs. This repository is the individual submission of Parth Pariwandh, Jadavpur University, for the Snapdragon AI Lab Build and Present Challenge.

## Product rules

Default inference is local. Do not add cloud LLM or cloud OCR calls in the default path.
Target hardware is Snapdragon X and Snapdragon X2 HP PCs (OmniBook Ultra, OmniBook 3, EliteBook X G2q).
Use Qualcomm AI Hub models: Whisper family for ASR, Qwen2.5 VL or InternVL for documents, Qwen3 1.7B or 4B or Granite 4 Micro for structuring, optional MeloTTS or PiperTTS for readback.
Runtime is ONNX Runtime QNN EP and Windows ML. CPU is orchestration only.
Languages: English, Hindi, Bengali. Mixed pages are allowed.
Primary user: MSME accounts clerk in India. Secondary: student office and clinic desk.
Human confirm is mandatory when confidence is below 0.85.
Do not store secrets or personal sample documents that identify real people.

## Code rules

Keep the pipeline, model router, storage, and export modules separate.
Schemas live in app/schemas as JSON Schema files.
If Hub artifacts are missing, return honest stubs. Never fake a successful NPU session.
Python 3.11, type hints, UTF-8, Windows path friendly code.
No telemetry. No network in offline mode.

## When generating new files

Create tests for schema validation, a simple local web UI that can run without NPU artifacts, and a models/README that explains how to export each Hub model for Snapdragon X Elite and Snapdragon X2 Elite.
