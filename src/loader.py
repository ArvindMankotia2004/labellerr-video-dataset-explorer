"""
loader.py
---------
Parses the Kinetics-400 (validation split) label file into a list of
clean, readable clip records.

The upstream label format (one row per labeled clip) is:

    label,youtube_id,time_start,time_end,split,is_cc

  label        -> the human action / category, e.g. "archery"
  youtube_id   -> the 11-character YouTube video ID the clip was cut from
  time_start   -> clip start time in the source video, in seconds
  time_end     -> clip end time in the source video, in seconds
  split        -> which dataset split the row belongs to (train/val/test)
  is_cc        -> 1 if the source video was Creative-Commons licensed, else 0

This module turns each row into a dict with a computed duration and a
ready-to-click YouTube link, since those are the two pieces of metadata
the raw file doesn't give you directly.
"""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List, Optional, TypedDict

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_CSV = DATA_DIR / "kinetics400_val_sample.csv"


class Clip(TypedDict):
    label: str
    youtube_id: str
    youtube_url: str
    time_start: Optional[int]
    time_end: Optional[int]
    duration_seconds: Optional[int]
    split: str
    is_cc: str
    clip_id: str


def _to_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def load_clips(csv_path: Path = DEFAULT_CSV) -> List[Clip]:
    """Read the label CSV at csv_path and return a list of Clip dicts."""
    clips: List[Clip] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            start = _to_int(row.get("time_start", ""))
            end = _to_int(row.get("time_end", ""))
            duration = (end - start) if start is not None and end is not None else None
            youtube_id = row.get("youtube_id", "").strip()
            clip_id = (
                f"{youtube_id}_{start:06d}_{end:06d}"
                if start is not None and end is not None
                else youtube_id
            )
            clips.append(
                Clip(
                    label=row.get("label", "").strip(),
                    youtube_id=youtube_id,
                    youtube_url=f"https://www.youtube.com/watch?v={youtube_id}",
                    time_start=start,
                    time_end=end,
                    duration_seconds=duration,
                    split=row.get("split", "").strip(),
                    is_cc=row.get("is_cc", "").strip(),
                    clip_id=clip_id,
                )
            )
    return clips


def unique_labels(clips: Iterable[Clip]) -> List[str]:
    """Return the sorted, de-duplicated set of labels present in clips."""
    return sorted({c["label"] for c in clips})


def filter_clips(
    clips: Iterable[Clip],
    keyword: Optional[str] = None,
    label: Optional[str] = None,
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None,
) -> List[Clip]:
    """
    Filter clips by a free-text keyword (substring match on the label),
    an exact label/category, and/or a duration range in seconds.
    All filters are optional and combine with AND.
    """
    result = list(clips)
    if keyword:
        kw = keyword.lower()
        result = [c for c in result if kw in c["label"].lower()]
    if label:
        result = [c for c in result if c["label"] == label]
    if min_duration is not None:
        result = [
            c for c in result
            if c["duration_seconds"] is not None and c["duration_seconds"] >= min_duration
        ]
    if max_duration is not None:
        result = [
            c for c in result
            if c["duration_seconds"] is not None and c["duration_seconds"] <= max_duration
        ]
    return result
