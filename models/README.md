# Model artifacts

Keep compiled Qualcomm AI Hub files in this folder.

Until those files exist, KaagazEdge runs in stub mode. The UI, schemas, confirm step, and Excel export still work. The product will not pretend a cloud call is an NPU session.

1. Create a Qualcomm ID and open Qualcomm AI Hub Workbench.
2. Compile Whisper, the document VLM, and the compact LLM for qualcomm-snapdragon-x-elite and qualcomm-snapdragon-x2-elite.
3. Copy ONNX or serialized QNN binaries here.
4. Restart the desk. `/api/health` should report mode qnn when artifacts are discovered.
