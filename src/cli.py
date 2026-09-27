"""
cli.py
------
Command-line summary & search tool for the Kinetics-400 (val) dataset.

Examples
--------
    python3 -m src.cli
        Print a summary table of the first 40 clips.

    python3 -m src.cli --search archery
        Only show clips whose label contains "archery".

    python3 -m src.cli --label "air drumming" --min-duration 8
        Exact-match a label, plus a minimum clip duration.

    python3 -m src.cli --list-labels
        List every unique action label in the dataset.

    python3 -m src.cli --search cream --export-json out.json
        Filter, print, and also write the filtered results as JSON.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import loader


def _print_table(clips, limit: int) -> None:
    if not clips:
        print("No clips match your filter.")
        return

    shown = clips[:limit]
    headers = ["#", "Label", "YouTube ID", "Start(s)", "End(s)", "Duration(s)", "Split"]
    rows = [
        [
            str(i),
            c["label"],
            c["youtube_id"],
            str(c["time_start"]),
            str(c["time_end"]),
            str(c["duration_seconds"]),
            c["split"],
        ]
        for i, c in enumerate(shown, start=1)
    ]

    widths = [len(h) for h in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    def fmt(row):
        return " | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(row))

    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt(row))

    remaining = len(clips) - len(shown)
    if remaining > 0:
        print(f"\n... and {remaining} more row(s) not shown. "
              f"Use --limit to show more, or narrow your filter.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarize and search the Kinetics-400 (val) action-label dataset."
    )
    parser.add_argument("--search", "-s", help="Keyword to search for within the label (substring match)")
    parser.add_argument("--label", "-l", help="Exact label/category to filter to")
    parser.add_argument("--min-duration", type=int, help="Minimum clip duration in seconds")
    parser.add_argument("--max-duration", type=int, help="Maximum clip duration in seconds")
    parser.add_argument("--limit", type=int, default=40, help="Max rows to print (default: 40)")
    parser.add_argument("--list-labels", action="store_true", help="List every unique label and exit")
    parser.add_argument("--export-json", metavar="PATH", help="Also write the filtered results as JSON to PATH")
    return parser


def main(argv=None) -> None:
    args = build_parser().parse_args(argv)
    clips = loader.load_clips()

    if args.list_labels:
        for label in loader.unique_labels(clips):
            print(label)
        return

    filtered = loader.filter_clips(
        clips,
        keyword=args.search,
        label=args.label,
        min_duration=args.min_duration,
        max_duration=args.max_duration,
    )

    print(f"{len(filtered)} of {len(clips)} total clips match your filter.\n")
    _print_table(filtered, limit=args.limit)

    if args.export_json:
        out_path = Path(args.export_json)
        out_path.write_text(json.dumps(filtered, indent=2))
        print(f"\nWrote {len(filtered)} clip(s) to {out_path}")


if __name__ == "__main__":
    main()
