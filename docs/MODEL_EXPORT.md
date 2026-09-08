# Qualcomm AI Hub export notes

Target devices: HP OmniBook Ultra with Snapdragon X2 Plus, HP OmniBook 3 with Snapdragon X, HP EliteBook X G2q class.

Chipset names in AI Hub: qualcomm-snapdragon-x-elite and qualcomm-snapdragon-x2-elite.

Models
* Speech: Whisper Small Quantized, Distil Whisper, Whisper Large V3 Turbo Quantized
* Vision: Qwen2.5 VL Instruct, Intern 3.5 VL 2B
* Language: Qwen3 1.7B, Qwen3 4B Instruct 2507, Granite 4.0 Micro
* Voice out: MeloTTS EN, PiperTTS EN

Prefer the Hub default that lists Hexagon NPU as the primary compute unit. Record compile job ID, inference time, and peak memory in docs/MEASUREMENTS.md. Do not invent numbers.
