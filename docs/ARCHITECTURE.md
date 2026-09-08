# KaagazEdge architecture

## Goal

Run a private Indic document and voice clerk on a Snapdragon powered HP PC. Models come from Qualcomm AI Hub. Default path never calls a cloud inference API.

## Modules

* `app/web.py` local FastAPI desk on 127.0.0.1
* `app/pipeline.py` capture to record
* `app/models_runtime.py` Hub artifact discovery and stub or QNN sessions
* `app/schema_validate.py` JSON Schema checks
* `app/letter_draft.py` local letter text
* `app/storage.py` SQLite under `data/local/`
* `app/export_util.py` Excel and JSON
* `app/preprocess.py` image metadata on CPU

## Privacy

Airplane mode is supported. Uploads stay under `data/local/uploads`. Exports stay under `data/local/exports`. The API has no cloud client.
