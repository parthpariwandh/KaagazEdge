"""KaagazEdge local API and CLI entrypoint."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.export_util import to_xlsx
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
    record_id = store.save(args.schema, record)
    record["record_id"] = record_id
    if args.export:
        to_xlsx(record, Path(args.export))
    return record


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="KaagazEdge on device clerk")
    parser.add_argument("--image", help="Path to document photo")
    parser.add_argument("--audio", help="Path to voice note")
    parser.add_argument("--schema", default="invoice", help="invoice or marksheet")
    parser.add_argument("--language", default="en", help="en, hi, or bn")
    parser.add_argument("--export", help="Optional xlsx path")
    parser.add_argument("--offline", action="store_true", default=True)
    return parser


if __name__ == "__main__":
    parsed = build_parser().parse_args()
    print(json.dumps(run_once(parsed), ensure_ascii=False, indent=2))
