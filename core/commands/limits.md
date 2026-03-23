# Limits Command

Show current Claude Code usage limits and context window status.

## What to Display

Run the following and report the results to the user:

```bash
# Check if claude-pulse is installed
if [ -f "$HOME/.claude-pulse/claude_status.py" ]; then
  python "$HOME/.claude-pulse/claude_status.py" --plain 2>/dev/null || echo "claude-pulse installed but could not fetch data"
else
  echo "claude-pulse not installed"
fi
```

If claude-pulse is not installed, show this instead:

```bash
# Fallback: read local usage data from Claude Code's JSONL files
python3 - <<'EOF'
import json, os, glob
from datetime import datetime, timezone

projects_dir = os.path.expanduser("~/.claude/projects")
if not os.path.exists(projects_dir):
    print("No usage data found (~/.claude/projects not found)")
    exit()

files = glob.glob(f"{projects_dir}/**/*.jsonl", recursive=True)
total_input = total_output = total_cache = msg_count = 0

for f in files:
    try:
        with open(f) as fp:
            for line in fp:
                try:
                    obj = json.loads(line)
                    usage = obj.get("usage") or obj.get("message", {}).get("usage", {})
                    if usage:
                        total_input  += usage.get("input_tokens", 0)
                        total_output += usage.get("output_tokens", 0)
                        total_cache  += usage.get("cache_read_input_tokens", 0)
                        msg_count    += 1
                except:
                    pass
    except:
        pass

print(f"Messages logged : {msg_count}")
print(f"Input tokens    : {total_input:,}")
print(f"Output tokens   : {total_output:,}")
print(f"Cache read      : {total_cache:,}")
print(f"Total tokens    : {total_input + total_output:,}")
print()
print("For real-time session/weekly limits, install claude-pulse:")
print("  bash plugins/claude-pulse/install.sh")
EOF
```

## Context Window Status

To check how full the current context window is, tell the user:
- The statusline (bottom of Claude Code) shows context % if claude-pulse is installed
- Alternatively: the conversation length can be estimated from the current session

## Install Prompt

If claude-pulse is not installed, suggest:
```
To get real-time session limits, weekly quota, and context window in the status bar:
  bash plugins/claude-pulse/install.sh
Then restart Claude Code and run /pulse to configure.
```
