#!/usr/bin/env bash
# run.sh
#
# Default (no args): builds web/data.json from the dataset and starts a
# local static web server so you can search & filter it in a browser.
#
#     ./run.sh
#     -> open http://localhost:8000 in your browser
#
# CLI mode: prints a filtered summary table straight to the terminal,
# no browser / server needed. Any extra flags are forwarded to
# `python3 -m src.cli` (see `./run.sh --cli --help` for all options).
#
#     ./run.sh --cli
#     ./run.sh --cli --search archery
#     ./run.sh --cli --label "air drumming" --min-duration 8
#     ./run.sh --cli --list-labels
#
# The web server's port can be overridden: PORT=9000 ./run.sh

set -euo pipefail
cd "$(dirname "$0")"

if [[ "${1:-}" == "--cli" ]]; then
  shift
  python3 -m src.cli "$@"
  exit 0
fi

echo "Building web/data.json from the dataset..."
python3 -m src.build_web_data

PORT="${PORT:-8000}"
echo ""
echo "Starting local web server on http://localhost:${PORT}"
echo "Open that URL in your browser to search & filter the dataset."
echo "(Run './run.sh --cli' instead for a terminal-only summary.)"
echo "Press Ctrl+C to stop."
echo ""
cd web
exec python3 -m http.server "${PORT}"
