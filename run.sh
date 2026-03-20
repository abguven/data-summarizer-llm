#!/usr/bin/env bash
# Quick launcher for Data Summarizer for LLMs
# Usage: ./run.sh [--demo]
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if [[ "$1" == "--demo" ]]; then
    echo "Copying sample data to data/input/..."
    cp tests/data/sample.csv data/input/sample.csv
    cp tests/data/sample.json data/input/sample.json
    echo "Sample files ready."
fi

echo ""
echo "Running Data Summarizer..."
echo "  Input:  $(pwd)/data/input/"
echo "  Output: $(pwd)/data/output/"
echo ""

docker compose up --pull always

echo ""
echo "Done! Open data/output/ to see your summaries."
