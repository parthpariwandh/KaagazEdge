# KaagazEdge architecture

## Goal

Run a private Indic document and voice clerk on a Snapdragon powered HP PC. Models come from Qualcomm AI Hub. Default path never calls a cloud inference API.

## Data flow

1. Camera or file picker supplies a page image.
2. Microphone or wav file supplies an optional voice note.
3. Image preprocessor corrects rotation and crops the page on CPU.
4. Document VLM runs on Hexagon NPU and returns candidate fields.
5. Whisper runs on Hexagon NPU and returns a transcript.
6. A compact LLM merges vision and speech into a JSON schema and can draft a short letter.
7. A validator flags low confidence fields for the human operator.
8. Local SQLite stores the accepted record.
9. Exporter writes Excel or PDF on disk.

## Heterogeneous compute

Capture and files run on the Oryon CPU. Camera preview and PDF raster run on the Adreno GPU. Whisper, the document VLM, and the structuring LLM run on the Hexagon NPU.

## Privacy

Airplane mode is supported. Logs do not write raw document pixels. The store lives under data/local/. Cloud fallback is off unless the operator explicitly enables a future hybrid mode.

## Windows packaging intent

Python 3.11 x64 on Windows on Arm. ONNX Runtime with QNN EP. Optional later wrap as an MSIX for HP OmniBook users.
