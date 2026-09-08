# GitHub Copilot prompt for KaagazEdge

Paste the block below into GitHub Copilot Chat at the repository root.

Build and complete the KaagazEdge Windows application in this repository.

Identity and contest
You are implementing KaagazEdge for Parth Pariwandh (B.E. Mechanical Engineering, Jadavpur University, Kolkata). Individual entry to the Snapdragon AI Lab Build and Present Challenge by Qualcomm. Solution Submission Round window: 04 September 2026 12:00 PM IST to 30 September 2026 11:59 PM IST. The proposed solution must be designed, developed, or intended to be optimised for Snapdragon powered HP PCs. Use AI models from Qualcomm AI Hub (and open source only where Hub does not cover a step). The work must be solely owned by the participant. English repository documentation.

One sentence product
KaagazEdge is an on device clerk that turns a photo of an Indian paper document plus optional spoken Hindi, Bengali, or English into a validated structured record, an Excel or PDF export, and an optional official letter draft, with no cloud inference in the default path.

Problem
MSME desks, college offices, and clinic counters in India still process GST invoices, challans, marksheets, and reports on paper. Connectivity is uneven. These pages contain personal and commercial data. Cloud OCR and chat tools create privacy, cost, and offline failures. A Snapdragon powered HP PC already has a Hexagon NPU (45 to 85 TOPS class), Oryon CPU, Adreno GPU, long battery, and a camera.

Users
Primary: MSME accounts clerk. Secondary: student academic office. Tertiary: clinic front desk. Accessibility: keyboard, large confirm buttons, English UI with Hindi and Bengali content support.

Hardware targets
HP OmniBook Ultra with Snapdragon X2 Plus, HP OmniBook 3 with Snapdragon X, HP EliteBook X G2q Snapdragon X2 class. Develop against Qualcomm AI Hub compile targets qualcomm-snapdragon-x-elite and qualcomm-snapdragon-x2-elite. x86 hosts may run UI plus stubs only.

Models you must wire (Qualcomm AI Hub names)
1. Speech to text: Whisper Small Quantized or Distil Whisper or Whisper Large V3 Turbo Quantized. Unit: NPU. Target: under 2 seconds per short voice note.
2. Document understanding: Qwen2.5 VL 7B Instruct or Intern 3.5 VL 2B. Unit: NPU. Target: under 4 seconds per 1080p page.
3. Structuring and drafting: Qwen3 1.7B or Qwen3 4B Instruct 2507 or Granite 4.0 Micro. Unit: NPU. Interactive tokens per second on device.
4. Optional readback: MeloTTS EN or PiperTTS EN.

Runtime
ONNX Runtime with QNN execution provider. Windows ML where it simplifies EP selection. Do not put generative decode on GPU unless NPU load requires overflow. CPU does UI, deskew, schema validation, SQLite, Excel export.

Functional scope to implement now
1. CLI already in app/main.py. Keep it working.
2. Add a local FastAPI plus simple HTML UI: upload image, upload or record audio, choose schema (invoice, marksheet), choose language en/hi/bn, extract, edit fields, confirm, save, export xlsx.
3. Add app/schemas/clinic_report.json and app/schemas/job_card.json following the existing invoice schema style.
4. Add schema validation with jsonschema.
5. Add confidence flags and needs_human_confirm.
6. Add docs for exporting each model with qai-hub / AI Hub Workbench, including chipset names and expected files under models/.
7. Add tests/test_schema.py and tests/test_pipeline_stub.py.
8. Add a PowerShell setup script scripts/setup_windows.ps1.
9. Keep airplane mode as default. Refuse network model calls when offline=True.
10. Write DEMO notes that can be performed in 180 seconds with WiFi off.

Evaluation criteria you must make visible in code comments and README
Technical Implementation: Hub models, QNN, NPU first, measured hooks for latency.
Application Use Case and Innovation: India paper plus Indic voice plus private clerk.
Deployment and Accessibility: single laptop install, three languages, MSME friendly UI.
Presentation and Documentation: README, ARCHITECTURE, DEMO_SCRIPT already exist. Keep them accurate.

Constraints
Do not invent fake NPU benchmark numbers. If artifacts are absent, stubs must say they are stubs.
Do not include confidential employer data or real Aadhaar, PAN, or patient pages.
Do not add analytics SDKs.
Keep original code MIT. Preserve third party licences.
Do not change the product name.
Prefer small files and clear modules over one large script.

Deliver after this prompt
Working UI on stubs, tests passing, model export instructions, and a short CHANGELOG of files you created.
