---
name: pick-mood
description: Pick the best `./songs/<mood>/` folder for a clip's background music. Reads the clip transcript and asks Claude to choose one mood label from the live list of mood subfolders. Emits a one-line mood string for bg-music to use as its category argument. Falls back to "ALL SONGS" on any failure.
allowed-tools: Bash
user-invocable: true
---

# pick-mood

Background music shouldn't be random. This skill reads a clip's transcript
and picks one of the existing `./songs/<mood>/` folders to source from. The
mood list is generated live from the filesystem — add or rename a folder
under `./songs/` and the next run will offer it.

## Invoke

```
.claude/skills/pick-mood/pick-mood.sh <clip_transcript.json> <out.txt>
```

- `input` — clip-local word-timed transcript JSON
- `out` — written with a single line: the chosen mood folder name (or
  `ALL SONGS` as a safe fallback)

## How

- Lists subdirectories of `$SHORTS_ROOT/songs/` (skipping dotfiles).
- Builds a prompt with the available moods and the clip transcript.
- Calls `claude -p --output-format text`.
- Parser strips quoting/whitespace and validates the reply against the
  live mood list. Any miss → `ALL SONGS`.

## Caveats

- All songs in the library are instrumental, so the mood label is judged
  purely on emotional/energetic fit with the clip's content — not lyrics.
- Cached by transcript mtime.
