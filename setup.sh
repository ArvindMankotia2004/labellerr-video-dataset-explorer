#!/usr/bin/env bash
# setup.sh
#
# This project uses only the Python 3 standard library (csv, json,
# http.server, unittest) -- no pip packages are required, so there is
# nothing to install. This script just verifies Python 3 is present
# and prints its version, so you know setup actually succeeded.

set -euo pipefail

echo "Checking for python3..."
if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 was not found on PATH." >&2
  echo "Please install Python 3.8+ and re-run this script." >&2
  exit 1
fi

PY_VERSION="$(python3 --version)"
echo "Found: ${PY_VERSION}"
echo "No external packages required (standard library only)."
echo "Setup complete. Run ./run.sh to start."
