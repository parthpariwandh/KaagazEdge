"""KaagazEdge CLI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.export_util import to_json, to_xlsx
from app.pipeline import KaagazPipeline
from app.storage import LocalStore


def run_once(args: argparse.Namespace) -> dict:
    pipe = KaagazPipeline(offline=args.offline)
    record = pipe.run(
        image_path=args.image,
        audio_path=args.audio,
        schema_name=args.schema,
        language=args.language,
    )
    store = LocalStore()
    record["record_id"] = store.save(args.schema, record)
    if args.export:
        dest = Path(args.export)
        if dest.suffix.lower() == ".json":
            to_json(record, dest)
        else:
            to_xlsx(record, dest)
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KaagazEdge on device clerk")
    parser.add_argument("--image", help="Path to document photo")
    parser.add_argument("--audio", help="Path to voice note")
    parser.add_argument("--schema", default="invoice", help="invoice, marksheet, clinic_report, job_card")
    parser.add_argument("--language", default="en", help="en, hi, or bn")
    parser.add_argument("--export", help="Optional xlsx or json path")
    parser.add_argument("--offline", action="store_true", default=True)
    parser.add_argument("--serve", action="store_true", help="Start the local web desk")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    return parser


if __name__ == "__main__":
    parsed = build_parser().parse_args()
    if parsed.serve:
        import uvicorn
        from app.web import app

        uvicorn.run(app, host=parsed.host, port=parsed.port, log_level="info")
    else:
        print(json.dumps(run_once(parsed), ensure_ascii=False, indent=2))
