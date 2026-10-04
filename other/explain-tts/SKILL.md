---
name: explain-tts
description: Speak short styled explanations aloud through the homelab Kokoro TTS server, playing on the primary Mac. Powers the /explain-brief, /explain-simply, /explain-mild, /explain-quick, /explain-status, /explain-options, and /explain-help commands.
---

# explain-tts

Portable spoken-explanation skill. Synthesis goes direct to the homelab Kokoro server
(OpenAI-compatible API, URL baked into `lib/config.sh`, no env vars required). The audio
response returns to the client that issued the command and plays locally. SSH forwarding to
the Mac is an explicit opt-in fallback only (`EXPLAIN_TTS_REMOTE_FALLBACK=1`).

## Command dispatch

Resolve the requested variant, then act exactly as specified. `${ARGUMENTS:-}` is any trailing
text after the command name.

| Invocation | Do this |
|---|---|
| `/explain-brief <topic>` | Write a <=80-word neutral spoken script, then `$SKILL/bin/tts-say --preset brief "<script>"` |
| `/explain-simply <topic>` | Write a <=120-word plain-language (ELI5) script, then run with `--preset simply` |
| `/explain-mild <topic>` | Write a <=150-word measured walkthrough, then run with `--preset mild` |
| `/explain-quick <topic>` | Write a <=25-word headline answer, then run with `--preset quick` |
| `/explain-status` | Run `$SKILL/bin/tts-selftest` and summarize its report |
| `/explain-options` (bare) | Run `$SKILL/bin/tts-options` and render the table it prints |
| `/explain-options k=v ...` | Run `$SKILL/bin/tts-options k=v ...`; report accepted updates or validation errors |
| unknown `/explain-*` or `/explain-help` | Render the dispatch table above verbatim |

If the invocation carries no topic (`${ARGUMENTS:-}` empty), ask what to explain ONLY when no
obvious subject exists in the current conversation; otherwise explain the most recent
assistant answer at the preset's length.

## Writing the spoken script (script-first presets)

- Kokoro has no prosody markup. Differentiation comes from what you WRITE, plus voice/speed.
- Strip markdown: no code fences, bullets, bold, links. Describe code verbally ("the retry
  function returns nil on timeout").
- Expand acronyms on first use ("A P I", "S Q L"), then may use them plainly.
- Never exceed the preset word cap; the script enforces caps mechanically, but you should hit
  them naturally.
- Tone: quick=headline fact; brief=neutral summary; simply=a curious beginner could follow;
  mild=careful measured walkthrough with caveats.

## Hard rules

- ALWAYS foreground: never call tts-say with background execution; a bounded foreground call
  is the contract (background TTS causes notification loops).
- Fail-soft: scripts are time-bounded and exit 0 even when the server or Mac is unreachable.
  A silent failure with a history row is success for this skill; never retry in a loop.
- One topic per call. For long explanations synthesize the capped script, not the whole text.

## Options

`voice` (e.g. `af_heart` or blend `af_heart+af_bella(3)`), `speed` (0.5-2.0),
`mute_until` (epoch seconds). Persisted atomically in
`~/.config/explain-tts/options.env`; survives skill re-import/update because it lives outside
the managed tree. Host-specific URL overrides also belong there via `config.sh`.

Playback adapters: macOS `afplay`; Linux `paplay`, `pw-play`, `mpv`, or `ffplay` (first
available); Windows-compatible shells use PowerShell `SoundPlayer` when available.

## Debugging order

See `references/tts-pipeline.md`: health probe, voices, history board, transport check.

## Importing on another client

Run `bin/install-explain-tts` from this bundle. It copies the shared transport and all seven
alias skills into `~/.agents/skills`, which jcode and Claude Code both discover. The installer
does not copy host options or overrides. After import, use `/explain-help` to confirm the alias
registry and `/explain-status` to confirm Kokoro reachability.
