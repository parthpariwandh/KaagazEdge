# KaagazEdge

On device Indic document and voice clerk for Snapdragon powered HP PCs.

**Challenge:** Snapdragon AI Lab Build and Present Challenge  
**Participant:** Parth Pariwandh  
**Affiliation:** B.E. Mechanical Engineering, Jadavpur University, Kolkata  
**Submission type:** Individual  
**Repository:** https://github.com/parthpariwandh/KaagazEdge

KaagazEdge turns a camera photo of an Indian paper record plus spoken Hindi, Bengali, or English into a structured, editable, private file. Inference is designed for the Qualcomm Hexagon NPU on Snapdragon X and Snapdragon X2 class HP PCs. No document image and no transcript is sent to a cloud API in the default path.

## What you can run today

The desk application, schemas, confirm step, letter draft, local store, and Excel export are implemented. Model inference uses labelled stubs until Qualcomm AI Hub artifacts are placed in `models/`. That is intentional. The product will not fake an NPU session.

```
python -m venv .venv
.venv/bin/activate
pip install -r requirements.txt
python samples/make_demo_invoice.py
python -m app.main --image samples/demo_invoice.png --schema invoice --language en --export exports/demo.xlsx
python -m app.main --serve
```

On Windows use `.venv\Scripts\activate`. Open `http://127.0.0.1:8080` for the local desk.

## Product flow

1. Capture a page from a photo file.
2. Optionally attach a voice note in English, Hindi, or Bengali.
3. Document understanding recovers fields for invoice, marksheet, clinic report, or workshop job card.
4. Speech recognition writes a transcript into the same record.
5. A letter draft is filled from extracted fields. When Hub artifacts exist, the compact LLM can refine that draft.
6. The operator edits low confidence values and confirms.
7. Excel is written next to a local SQLite store.

## Target hardware

Designed, developed, and intended for Snapdragon powered HP PCs:

* HP OmniBook Ultra with Snapdragon X2 Plus
* HP OmniBook 3 with Snapdragon X
* HP EliteBook X G2q class Snapdragon X2 machines

Hexagon NPU runs Whisper, the document VLM, and the structuring LLM. Oryon CPU runs UI, schema checks, SQLite, and Excel. Adreno GPU is reserved for preview and PDF raster.

## Qualcomm AI Hub models

Speech to text: Whisper Small Quantized, Distil Whisper, Whisper Large V3 Turbo Quantized on NPU.
Document understanding: Qwen2.5 VL Instruct or Intern 3.5 VL 2B on NPU.
Structuring and letter draft: Qwen3 1.7B, Qwen3 4B Instruct, or Granite 4.0 Micro on NPU.
Optional spoken readback: MeloTTS EN or PiperTTS EN.

Export steps live in `docs/MODEL_EXPORT.md`. Put compiled files in `models/` as described in `models/README.md`.

## Tests

```
python -m pytest tests -q
```

## Intellectual property

Original product design and application code are owned by Parth Pariwandh. Qualcomm AI Hub models and other third party components remain under their own licences.

## Licence

MIT for original application code. See LICENSE.
