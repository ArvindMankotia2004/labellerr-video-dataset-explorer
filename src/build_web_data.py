"""
build_web_data.py
------------------
Exports the parsed dataset as web/data.json, which the static web UI
(web/index.html) fetches at load time. Keeping this as a separate,
explicit build step (rather than having the browser parse CSV) keeps
the web page dependency-free -- it's plain HTML/CSS/JS with no CSV
parsing library required.

Run directly:
    python3 -m src.build_web_data
"""
from __future__ import annotations

import json
from pathlib import Path

from . import loader

OUT_PATH = Path(__file__).resolve().parent.parent / "web" / "data.json"


def main() -> None:
    clips = loader.load_clips()
    OUT_PATH.write_text(json.dumps(clips, indent=2))
    print(f"Wrote {len(clips)} clip(s) to {OUT_PATH}")


if __name__ == "__main__":
    main()
