"""Shared filesystem primitives; callers own their concurrency policy."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any


def atomic_write_text(path: Path, content: str) -> None:
    """Replace text only after a complete, flushed UTF-8 write succeeds.

    The temporary file lives beside the target for same-filesystem replacement.
    Register it before writing so every failure path can clean it up.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent,
            prefix=f".{path.name}.", suffix=".tmp", delete=False,
        ) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(content)
            temp_file.flush()
            os.fsync(temp_file.fileno())
        os.replace(temp_path, path)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def atomic_write_json(path: Path, data: Any) -> None:
    """Atomically serialize and replace a JSON file."""
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
