---
name: granola
description: Use Granola MCPorter CLI to find meetings, notes, and transcripts or answer questions grounded in specific meetings.
---

# Granola

Run the generated `granola` CLI through Context Mode and its bounded runner:

```sh
node "$PI_CODING_AGENT_DIR/skills/granola/scripts/run.mjs" list-meetings --help
node "$PI_CODING_AGENT_DIR/skills/granola/scripts/run.mjs" query-granola-meetings --help
node "$PI_CODING_AGENT_DIR/skills/granola/scripts/run.mjs" get-meeting-transcript --help
```

Constrain discovery by date, participant, folder, or topic before reading meeting details.
Prefer `query-granola-meetings` for synthesis and use transcripts only when the request requires exact wording or detailed evidence.
Meeting notes and transcripts are private work data; return only the minimum excerpts needed and preserve citation links when available.
When Granola OAuth is unavailable, authenticate with `npx --yes mcporter@0.13.3 --config "$MCPORTER_CONFIG" auth granola`.

Refresh this generated wrapper with `nix run .#update-mcp-skills -- granola`, then run `nix run .#sync-agents`.
