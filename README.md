# KaagazEdge

![Challenge](https://img.shields.io/badge/Snapdragon%20AI%20Lab-HP%20PCs-navy)
![Runtime](https://img.shields.io/badge/on%20device-Hexagon%20NPU-blue)
![Languages](https://img.shields.io/badge/Hindi%20%7C%20Bengali%20%7C%20English-private-green)

On device Indic document and voice clerk for Snapdragon powered HP PCs.

Challenge: Snapdragon AI Lab Build and Present Challenge  
Participant: Parth Pariwandh  
Affiliation: B.E. Mechanical Engineering, Jadavpur University, Kolkata  
Submission type: Individual

KaagazEdge turns a camera photo of an Indian paper record plus spoken Hindi, Bengali, or English into a structured, editable, private file. Inference is designed for the Qualcomm Hexagon NPU on Snapdragon X and Snapdragon X2 class HP PCs. No document image and no transcript is sent to a cloud API in the default path.

## What you can run today

The desk application, schemas, confirm step, letter draft, local store, and Excel export are implemented. Model inference uses labelled stubs until Qualcomm AI Hub artifacts are placed in `models/`.

```bash
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
5. A letter draft is filled from extracted fields.
6. The operator edits low confidence values and confirms.
7. Excel is written next to a local SQLite store.

## Target hardware

HP OmniBook Ultra with Snapdragon X2 Plus, HP OmniBook 3 with Snapdragon X, and HP EliteBook X G2q class Snapdragon X2 machines. Hexagon NPU runs Whisper, the document model, and the structuring model. Oryon CPU runs UI, schema checks, SQLite, and Excel.

## Licence

MIT for original application code. See LICENSE.
