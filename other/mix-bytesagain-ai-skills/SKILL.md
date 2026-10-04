---
name: "Mix"
description: "Record, search, and analyze music and audio sessions with playback tracking. Use when logging audio sessions, searching metadata, analyzing listening data."
version: "1.0.0"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["audio", "music", "mix", "production", "creative"]
---

# Mix

Mix makes music & audio simple. Record, search, and analyze your data with clear terminal output.

## Why Mix?

- Works entirely offline — your data never leaves your machine
- Simple command-line interface, no GUI needed
- Export to JSON, CSV, or plain text anytime
- Automatic history and activity logging

## Getting Started

```bash
# See what you can do
mix help

# Check current status
mix status

# View your statistics
mix stats
```

## Commands

| Command | What it does |
|---------|-------------|
| `mix run` | Run |
| `mix check` | Check |
| `mix convert` | Convert |
| `mix analyze` | Analyze |
| `mix generate` | Generate |
| `mix preview` | Preview |
| `mix batch` | Batch |
| `mix compare` | Compare |
| `mix export` | Export |
| `mix config` | Config |
| `mix status` | Status |
| `mix report` | Report |
| `mix stats` | Summary statistics |
| `mix export` | <fmt>       Export (json|csv|txt) |
| `mix search` | <term>      Search entries |
| `mix recent` | Recent activity |
| `mix status` | Health check |
| `mix help` | Show this help |
| `mix version` | Show version |
| `mix $name:` | $c entries |
| `mix Total:` | $total entries |
| `mix Data` | size: $(du -sh "$DATA_DIR" 2>/dev/null | cut -f1) |
| `mix Version:` | v2.0.0 |
| `mix Data` | dir: $DATA_DIR |
| `mix Entries:` | $(cat "$DATA_DIR"/*.log 2>/dev/null | wc -l) total |
| `mix Disk:` | $(du -sh "$DATA_DIR" 2>/dev/null | cut -f1) |
| `mix Last:` | $(tail -1 "$DATA_DIR/history.log" 2>/dev/null || echo never) |
| `mix Status:` | OK |
| `mix [Mix]` | run: $input |
| `mix Saved.` | Total run entries: $total |
| `mix [Mix]` | check: $input |
| `mix Saved.` | Total check entries: $total |
| `mix [Mix]` | convert: $input |
| `mix Saved.` | Total convert entries: $total |
| `mix [Mix]` | analyze: $input |
| `mix Saved.` | Total analyze entries: $total |
| `mix [Mix]` | generate: $input |
| `mix Saved.` | Total generate entries: $total |
| `mix [Mix]` | preview: $input |
| `mix Saved.` | Total preview entries: $total |
| `mix [Mix]` | batch: $input |
| `mix Saved.` | Total batch entries: $total |
| `mix [Mix]` | compare: $input |
| `mix Saved.` | Total compare entries: $total |
| `mix [Mix]` | export: $input |
| `mix Saved.` | Total export entries: $total |
| `mix [Mix]` | config: $input |
| `mix Saved.` | Total config entries: $total |
| `mix [Mix]` | status: $input |
| `mix Saved.` | Total status entries: $total |
| `mix [Mix]` | report: $input |
| `mix Saved.` | Total report entries: $total |

## Data Storage

All data is stored locally at `~/.local/share/mix/`. Each action is logged with timestamps. Use `export` to back up your data anytime.

## Feedback

Found a bug or have a suggestion? Let us know: https://bytesagain.com/feedback/

---
Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
