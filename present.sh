#!/usr/bin/env bash
# Launch the Urumuri site for live presentation.
# Usage: ./present.sh [port]

set -e

PORT="${1:-8765}"
DIR="$(cd "$(dirname "$0")" && pwd)"
URL="http://localhost:${PORT}/index.html"

cd "$DIR"

# Reuse an existing server on this port if one is already running.
if lsof -i ":${PORT}" -sTCP:LISTEN -t >/dev/null 2>&1; then
  echo "Server already running on port ${PORT}"
else
  echo "Starting server on port ${PORT}..."
  python3 -m http.server "$PORT" >/dev/null 2>&1 &
  SERVER_PID=$!
  sleep 1
  echo "Server started (PID ${SERVER_PID})"
fi

echo ""
echo "  Urumuri presentation"
echo "  --------------------"
echo "  URL:  ${URL}"
echo "  Tips: Full-screen your browser (F11 / Ctrl+Cmd+F)"
echo "        Read PRESENTATION-SCRIPT.md for the walkthrough"
echo ""

# Open in default browser (macOS, Linux, WSL-friendly).
if command -v open >/dev/null 2>&1; then
  open "$URL" || true
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" || true
else
  echo "Open this URL manually: ${URL}"
fi
