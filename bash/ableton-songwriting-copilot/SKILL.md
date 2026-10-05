---
name: ableton-songwriting-copilot
description: "Use when helping a songwriter or music producer operate ChordChemist with Ableton Live and Max for Live: preparing the local web app, OpenAI Realtime voice, SQLite songs, Ableton/M4L bridge, writing or firing MIDI clips in Live, diagnosing no-sound/permission/mic/API-key/bridge issues, or planning ChordChemist-to-Ableton production workflows. Do not use for generic music advice that does not involve ChordChemist, Ableton, Max for Live, Realtime, or the local M4L bridge."
---

# Ableton Songwriting Copilot

## Core Model

Treat ChordChemist as the songwriting companion, Ableton Live as the sound/playback environment, and Max for Live as the narrow local bridge. Keep OpenAI keys and Realtime sessions in the browser/server app; keep Ableton mutations behind explicit bridge commands and user intent.

## Available Scripts

- `scripts/check-stack.sh` — Checks local app, API key presence, SQLite, bridge, Max Library assets, M4L device presence, and Ableton process status.

Prerequisites:

- Bash, curl, git, Python 3, and standard macOS shell tools.
- No Bun/Bunx dependency for this skill.
- Use `scripts/check-stack.sh --help` before changing flags.
- Use `scripts/check-stack.sh --json` when the result needs to be parsed by an agent or piped into another command.

## Workflow

1. Classify the task:
   - **Setup/readiness**: app URL, `.env`, OpenAI key, SQLite, bridge server, M4L poller, Ableton slot.
   - **Realtime voice**: browser WebRTC, macOS microphone permission, `/api/realtime/session`, transcript/consent behavior.
   - **Ableton export/playback**: highlighted slot, M4L device, instrument after the bridge, write/fire/stop clips.
   - **Songwriting**: chords, melody, arrangement, vocal adaptation, audition decisions.
   - **Implementation**: code, docs, M4L assets, tests, packaging.
2. For setup/debug/Ableton work, read `references/chordchemist-m4l-runbook.md`.
3. Run `scripts/check-stack.sh` before claiming local readiness, unless the user only wants conceptual advice.
4. For deterministic harmony/melody answers, use `$chordchemist-composer` when available. Do not invent ChordChemist CLI results.
5. For browser UI work, use the Browser/in-app browser on the local URL. For Ableton or Max UI work, use Computer Use and begin with `get_app_state`.
6. Before mutating Ableton, confirm the user asked to send/write/play/stop in Live, or that the current task clearly implies it.
7. Verify with concrete evidence: local status JSON, bridge `/health`, M4L poller count, successful command result, visible Live meters/audio, or test output.

## Production Guardrails

- Do not print API keys. Report only present/missing.
- Do not move Realtime microphone capture into Max for Live.
- Do not auto-play, overwrite clips, or perform destructive melody actions without user intent or consent gates.
- When `Permission denied` appears on Realtime, check macOS microphone permission for Codex/Chrome before blaming OpenAI.
- When Live is silent, check instrument placement and `midiin -> midiout` pass-through before changing music.
- When bridge commands time out, check for stale Max editor pollers and restart `npm run live-bridge` before rewriting code.

## Script

Use the local stack checker from any directory:

```bash
scripts/check-stack.sh
```

Useful flags:

```bash
scripts/check-stack.sh --help
scripts/check-stack.sh --json
scripts/check-stack.sh --repo /path/to/chord-chemist
scripts/check-stack.sh --app-url http://localhost:8080 --bridge-url http://127.0.0.1:53873
```

Exit codes:

- `0`: success.
- `1`: general runtime error.
- `2`: invalid arguments.

## Completion Criteria

- For readiness: identify the app URL, OpenAI key status, SQLite DB path, bridge status, poller count, and Ableton/M4L next action.
- For Realtime: confirm API key and browser/server status, then resolve mic permission or report the remaining OS/browser step.
- For Ableton playback: confirm clip write result and either visible meters/audio or the specific missing piece.
- For implementation changes: run the repo’s relevant checks and update M4L/realtime docs when behavior changes.
