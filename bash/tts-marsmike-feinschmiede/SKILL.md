---
name: tts
description: Convert text to speech with ElevenLabs voiceover. Use when generating speech audio or browsing available voices.
---

# feinklang — ElevenLabs voiceover

`feinklang` is a command on your PATH — no file paths, no `cd`, no
`${CLAUDE_PLUGIN_ROOT}`. Requires `ELEVENLABS_API_KEY` (an export, or a line in
`~/.env`). Default voice: **Hale**.

## Quick Start

```
feinklang tts --text "Hello, this is a test." --out voiceover.mp3
```

See [`references/parameters.md`](references/parameters.md) for all flags, models, and format options.

## Synthesize speech

Key options: `--voice-id` (name or ID), `--model-id`, `--format`, `--stability`,
`--similarity-boost`, `--speed`, `--play`. Write outputs into the project
(e.g. a beats directory under `${CLAUDE_PROJECT_DIR}`) so downstream plugins
can consume them.

## Browse voices

```bash
feinklang voices                          # all voices
feinklang voices --category professional  # cloned | professional | premade
feinklang voices --search Mike            # search by name
```

## For other plugins (capability hand-off)

Call `feinklang tts --text "…" --out <project-path>` and read the resulting
file. Do **not** reference feinklang's internal files; the CLI is the entire
contract. If `feinklang` is not on PATH, ask the user for the audio instead.

## References

- [`references/parameters.md`](references/parameters.md) — full flag reference, models, output formats, and examples
