---
name: name-short
description: Sanitize a generated title into a filesystem-safe filename for the final saved short. Reads the title text emitted by generate-title and prints a kebab-case `.mp4` filename. Pure string op — no Claude call.
---

# name-short

Turn a title like `"SIMON SINEK: THE ADVICE YOU NEED"` into
`simon-sinek-the-advice-you-need.mp4`. Used by the orchestrator
right before `save-local` so shorts land with real names instead of
`short_01.mp4`.

## Inputs
- `title_file`: path to the title text file written by generate-title
- `out_file` (optional): where to write the resulting filename string

## Output
Prints the kebab-cased `<slug>.mp4` filename to stdout. If `out_file`
is given, also writes it there.

## Rules
- lowercase
- non-alnum → `-`
- collapse repeats, strip leading/trailing `-`
- cap stem length at 80 chars
- fallback to `short` if empty after sanitizing
