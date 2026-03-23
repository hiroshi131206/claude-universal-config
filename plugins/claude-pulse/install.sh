#!/usr/bin/env bash
# claude-pulse installer for claude-universal-config
# Source: https://github.com/NoobyGains/claude-pulse (MIT)
#
# What this does:
#   1. Installs claude-pulse to ~/.claude-pulse
#   2. Adds the statusCommand to ~/.claude/settings.json
#   3. Installs /pulse command to ~/.claude/commands/pulse.md

set -e

echo "[claude-pulse] Installing..."

# Run the official installer
if command -v curl &>/dev/null; then
  curl -fsSL https://raw.githubusercontent.com/NoobyGains/claude-pulse/main/install.sh | sh
elif command -v wget &>/dev/null; then
  wget -qO- https://raw.githubusercontent.com/NoobyGains/claude-pulse/main/install.sh | sh
else
  echo "[claude-pulse] ERROR: curl or wget is required" >&2
  exit 1
fi

echo ""
echo "[claude-pulse] Done. Restart Claude Code and run /pulse to configure."
echo ""
echo "  Status bar shows:"
echo "  - Session usage  (5-hour block, % consumed)"
echo "  - Weekly usage   (rolling 7 days, with reset timer)"
echo "  - Context window (how full Claude's memory is)"
echo "  - Model name     (Opus 4.6 / Sonnet 4.6 etc.)"
echo "  - Effort level   (low / medium / high / max)"
echo "  - Worktree branch"
echo ""
echo "  Commands after restart:"
echo "  /pulse         — interactive setup wizard"
echo "  /pulse show    — preview all themes"
echo "  /pulse update  — update to latest version"
