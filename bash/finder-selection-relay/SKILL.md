---
name: finder-selection-relay
description: Build or operate a macOS menu-bar relay that turns the current Finder selection into prompt, note, ticket, or shell-ready context with clean paths and lightweight local metadata.
---

# Finder Selection Relay

Use this skill when the user wants a Mac menu-bar utility for taking the current Finder selection and handing it off cleanly without retyping paths, stripping Finder noise, or opening each file one by one.

## Core Workflow

- Read the current Finder selection as local file or folder paths and keep the interaction menu-bar first.
- Fall back to explicit local paths when the user already has them or Finder automation is unavailable.
- Format the selection into destination-ready output: prompt context, markdown notes, ticket bullets, shell-safe paths, or plain lists.
- Surface only lightweight local metadata that helps the handoff: item name, path, file or folder kind, parent folder, file extension, file size, and modified time when available.
- Keep the scope on selection handoff, not file contents, previews, indexing, or Finder replacement behavior.
- Treat large selections as a review problem first; if the user has selected too much, ask them to narrow the handoff instead of hiding truncation.

## Local Helper

Use `scripts/finder_selection_relay.py` when a deterministic local read is useful:

```bash
python skills/finder-selection-relay/scripts/finder_selection_relay.py current --format json
python skills/finder-selection-relay/scripts/finder_selection_relay.py current --format markdown
python skills/finder-selection-relay/scripts/finder_selection_relay.py copy --format prompt
python skills/finder-selection-relay/scripts/finder_selection_relay.py copy --format shell
python skills/finder-selection-relay/scripts/finder_selection_relay.py current ~/Desktop/mockup.png ~/Downloads/build.log --format markdown
printf '%s\n' ~/Desktop/mockup.png ~/Downloads/build.log | python skills/finder-selection-relay/scripts/finder_selection_relay.py current --stdin-paths --format shell
```

The helper uses macOS `osascript` to read the current Finder selection, and it can also format explicit local paths from arguments or standard input. Python filesystem metadata fills in the selected path details. It does not read file contents and does not use network access.

## Guardrails

- Do not claim file-content extraction, OCR, indexing, or semantic summaries; this skill is about the selected file and folder metadata only.
- If Finder selection access is blocked, explain the macOS automation permission path and offer the explicit-path fallback instead of inventing selected items.
- If there is no Finder selection, ask the user to select the files or folders first or pass explicit paths.
- Keep output formats short and ready for the next destination. Do not turn the relay into a full DAM, launcher, or Finder replacement.

## Prototype

The SwiftUI starter in `prototype/` sketches a compact status-item shell with a selection summary card, format shortcuts, a recent selection list, and one primary copy action. Use it as the top-level menu-bar layer for a real macOS target.
