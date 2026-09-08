"""Local record store. Nothing is uploaded."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DB_PATH = Path("data/local/kaagazedge.db")


class LocalStore:
    def __init__(self, path: Path = DB_PATH) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._init()

    def _init(self) -> None:
        with sqlite3.connect(self.path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT NOT NULL,
                    schema_name TEXT NOT NULL,
                    payload TEXT NOT NULL
                )
                """
            )

    def save(self, schema_name: str, payload: dict) -> int:
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "INSERT INTO records (created_at, schema_name, payload) VALUES (?, ?, ?)",
                (
                    datetime.now(timezone.utc).isoformat(),
                    schema_name,
                    json.dumps(payload, ensure_ascii=False),
                ),
            )
            return int(cur.lastrowid)
