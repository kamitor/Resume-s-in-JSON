#!/usr/bin/env bash
# Manage the rxresume Podman stack
# Usage: ./rxresume.sh [up|down|status|logs]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_HOST="${DOCKER_HOST:-unix:///run/user/1000/podman/podman.sock}"
export DOCKER_HOST

cmd="${1:-status}"

case "$cmd" in
  up)
    echo "Starting rxresume stack..."
    systemctl --user start podman.socket 2>/dev/null || true
    podman compose -f "$SCRIPT_DIR/compose.yml" up -d
    echo ""
    echo "Waiting for health..."
    for i in $(seq 1 20); do
      if curl -sf http://127.0.0.1:3000/api/health > /dev/null 2>&1; then
        echo "rxresume is up → http://localhost:3000"
        break
      fi
      sleep 2
    done
    ;;
  down)
    podman compose -f "$SCRIPT_DIR/compose.yml" down
    echo "rxresume stopped."
    ;;
  status)
    if curl -sf http://127.0.0.1:3000/api/health > /dev/null 2>&1; then
      echo "rxresume is running → http://localhost:3000"
      curl -s http://127.0.0.1:3000/api/health | python3 -c "
import sys, json
h = json.load(sys.stdin)
print(f\"  database : {h['database']['status']} ({h['database']['latencyMs']}ms)\")
print(f\"  printer  : {h['printer']['status']}\")
print(f\"  storage  : {h['storage']['status']}\")
"
    else
      echo "rxresume is NOT running. Start with: ./rxresume.sh up"
    fi
    ;;
  logs)
    podman compose -f "$SCRIPT_DIR/compose.yml" logs --tail=50 -f
    ;;
  *)
    echo "Usage: $0 [up|down|status|logs]"
    exit 1
    ;;
esac
