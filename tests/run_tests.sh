#!/bin/bash
# Usage: ./tests/run_tests.sh [image]
#
# Without argument : pulls and tests the published image from Docker Hub
# With argument    : tests the specified local image (e.g. data-summarizer:local)
#
# Examples:
#   ./tests/run_tests.sh                        # test published image
#   ./tests/run_tests.sh data-summarizer:local  # test a local build

set -e

IMAGE="${1:-abguven/data-summarizer:latest}"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEST_OUTPUT="$ROOT_DIR/tests/output"

echo "=== Image: $IMAGE ==="

echo ""
echo "=== Run container with test data ==="
mkdir -p "$TEST_OUTPUT"
chmod 777 "$TEST_OUTPUT"
rm -f "$TEST_OUTPUT"/*.md

# MSYS_NO_PATHCONV=1 prevents Git Bash from converting Unix paths to Windows paths
MSYS_NO_PATHCONV=1 docker run --rm \
  -v "$ROOT_DIR/tests/data:/app/data/input:ro" \
  -v "$TEST_OUTPUT:/app/data/output" \
  "$IMAGE"

echo ""
echo "=== Validate output ==="
python "$ROOT_DIR/tests/test_output.py" "$TEST_OUTPUT"
