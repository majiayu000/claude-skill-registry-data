---
name: download-landing-pad
description: Triage recent macOS downloads with a menu-bar staging surface that lists the newest files, supports safe rename or move actions, and keeps reveal, copy-path, and routing choices in one stop.
---

# Download Landing Pad

Use this skill when the user wants a practical Mac-first utility for keeping fresh downloads from disappearing into Finder clutter before they get renamed, routed, or pasted somewhere useful.

## Core Workflow

- Start by listing the newest files in `~/Downloads` so the handoff is based on the real queue, not memory.
- Surface file kind, age, size, and source hint first; that is usually enough to decide whether the next step is rename, reveal, move, or upload.
- Keep rename and move actions explicit. Preview the destination or filename before applying it.
- Treat the menu-bar surface as a staging pad, not a full file manager or background sync daemon.
- Keep the last dispatch visible so the user knows which file actually left Downloads and where it went.

## Local Helper

Use `scripts/download_landing_pad.py` when a deterministic local Downloads relay is useful:

```bash
python skills/download-landing-pad/scripts/download_landing_pad.py doctor --format markdown
python skills/download-landing-pad/scripts/download_landing_pad.py list --format plain
python skills/download-landing-pad/scripts/download_landing_pad.py brief --format markdown
python skills/download-landing-pad/scripts/download_landing_pad.py rename latest --name launch-brief.pdf
python skills/download-landing-pad/scripts/download_landing_pad.py move latest --to ~/Desktop/LaunchAssets
python skills/download-landing-pad/scripts/download_landing_pad.py reveal latest
python skills/download-landing-pad/scripts/download_landing_pad.py copy-path latest
```

Run `doctor` first when the Downloads path, Finder reveal, copy-path support, or source metadata looks unreliable.
The helper reads the local Downloads folder, uses `mdls` when available to infer a source hint, suggests deterministic destination lanes by file type, and renders plain text, markdown, prompt, or JSON output. It does not use network access. Rename and move stay in dry-run mode until `--yes` is passed.

## Guardrails

- Do not invent a background watcher, cloud sync, or file-history service the Mac does not already provide.
- Never rename or move files implicitly. Show the target first and require explicit confirmation for the write.
- If the Downloads folder is missing or inaccessible, stop and explain the local boundary instead of pretending the queue is empty.
- If the source hint is unavailable, say so; do not guess a browser or website.
- Keep the readiness path visible when metadata, reveal, or clipboard support is degraded so the user knows which local tool is missing.

## Prototype

The SwiftUI starter in `prototype/` sketches a menu-bar shell with a recent-arrivals lane, a readiness strip, a rename dock, and quick routing chips for the selected file. Use it as the top-level macOS layer when the user wants more than a one-off script run.

## Resources

- `scripts/download_landing_pad.py`: local downloads queue helper for readiness checks, listing, briefing, rename, move, reveal, and copy-path actions
- `prototype/`: menu-bar-first SwiftUI starter for a compact download staging utility
