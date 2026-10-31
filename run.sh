#!/usr/bin/env bash
# Start Vigil with one command: sets up Python packages on first run, then opens the web page
set -e
cd "$(dirname "$0")"

if [ ! -d venv ]; then
  echo "First run: setting up (takes a minute)..."
  python3 -m venv venv
fi
venv/bin/python -m pip install --quiet --disable-pip-version-check -r requirements.txt

# macOS uses port 5000 for AirPlay, so default to 5077
PORT="${PORT:-5077}"
URL="http://127.0.0.1:$PORT"
echo "Vigil is running at $URL (press Ctrl+C to stop)"
( sleep 3; open "$URL" 2>/dev/null || xdg-open "$URL" 2>/dev/null || true ) &
PORT="$PORT" exec venv/bin/python src/deploy.py
