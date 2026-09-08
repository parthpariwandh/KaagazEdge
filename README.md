# KaagazEdge

On device Indic document and voice clerk for Snapdragon powered HP PCs.

**Challenge:** Snapdragon AI Lab Build and Present Challenge  
**Participant:** Parth Pariwandh  
**Affiliation:** B.E. Mechanical Engineering, Jadavpur University, Kolkata  
**Submission type:** Individual

KaagazEdge turns a camera photo of an Indian paper record (GST invoice, challan, marksheet, clinic report, handwritten job card) plus spoken Hindi, Bengali, or English into a structured, editable, private file. Inference is designed to run on the Qualcomm Hexagon NPU of Snapdragon X and Snapdragon X2 class HP PCs. No document image and no transcript is sent to a cloud API in the default path.

## Why this exists

Indian MSME desks, college offices, and clinic counters still live on paper. Connectivity is uneven. Documents carry personal and commercial data that should not leave the laptop. Cloud OCR and chat tools fail that constraint. A Snapdragon powered HP PC already has a high TOPS NPU, long battery life, and a camera. KaagazEdge uses that hardware as a private clerk.

## What the product does

1. Capture a page from the webcam or an image file.
2. Optionally record a voice note in English, Hindi, or Bengali.
3. Run document understanding on the NPU to recover fields, stamps, totals, and layout.
4. Transcribe speech on the NPU with a Qualcomm AI Hub Whisper model.
5. Merge vision and speech into a validated JSON schema.
6. Let the user confirm or correct fields locally.
7. Export Excel, CSV, or a printable PDF. Draft a short official letter if asked.
8. Store records in a local database. Airplane mode is a first class demo.

## Target device

Designed, developed, and intended for Snapdragon powered HP PCs, including:

* HP OmniBook Ultra with Snapdragon X2 Plus
* HP OmniBook 3 with Snapdragon X
* HP EliteBook X G2q class Snapdragon X2 machines

Primary compute for models: Qualcomm Hexagon NPU via ONNX Runtime QNN execution provider and Windows ML. Oryon CPU handles UI, file I/O, and schema validation. Adreno GPU handles camera preview and PDF raster only.

## Qualcomm AI Hub models in the design

Speech to text: Whisper Small Quantized, Distil Whisper, or Whisper Large V3 Turbo Quantized on NPU.
Document understanding: Qwen2.5 VL Instruct or Intern 3.5 VL 2B on NPU.
Structuring and drafts: Qwen3 1.7B or Qwen3 4B Instruct, Granite 4.0 Micro on NPU.
Optional spoken readback: MeloTTS EN or PiperTTS EN.

Exact compiled artifacts are obtained with Qualcomm AI Hub Workbench targeting Snapdragon X Elite and Snapdragon X2 Elite chipsets.

## Quick start (Windows on Snapdragon)

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m app.main --offline
```

## Intellectual property

Original product design and application code in this repository are owned by Parth Pariwandh. Qualcomm AI Hub models and other third party components remain under their own licences.

## Licence

MIT for original application code. See LICENSE.
