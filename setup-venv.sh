#!/bin/bash

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

[ -d "$SCRIPT_DIR/venv" ] && echo "🚨 Seems $SCRIPT_DIR/venv already exists!"

set -e

python3 -m venv "$SCRIPT_DIR/venv"
echo "✅ created at $SCRIPT_DIR/venv"

echo "👉 Installing pip3 requirements..."
$SCRIPT_DIR/venv/bin/pip3 install -r $SCRIPT_DIR/requirements.txt
echo "✅ requirements done"