---
name: hance
description: Apply cinematic film looks to images/video via the Hance CLI. Use when asked to grade, color, or "make it look like" film.
---

# /hance

A single entry point that routes to one of six subcommands: `setup`, `run`, `try`, `refine`, `batch`, `ui`.

## Routing

Pick the subcommand from the user's request. When in doubt, ask.

| User intent | Subcommand | Doc |
|---|---|---|
| "install hance" / "set up hance" | `setup` | `subcommands/setup.md` |
| "apply <preset> to <file>" / "grade with <preset>" | `run` | `subcommands/run.md` |
| "make this look like X" / "match this reference" / "show me some looks for this" | `try` | `subcommands/try.md` |
| "make this one look better" / "tune/refine this grade" / "more grain, warmer, etc." | `refine` | `subcommands/refine.md` |
| "apply X to all of these" / batch a folder | `batch` | `subcommands/batch.md` |
| "open the editor" / "open the UI" | `ui` | `subcommands/ui.md` |

## Runner selection (every subcommand)

Pick one runner per invocation, in order:

1. If `command -v bun` succeeds → use `bunx @orva-studio/hance` (preferred — fast cold-start, cached after first fetch).
2. Else if `command -v node` succeeds → use `npx @orva-studio/hance`.
3. Else → inform the user that a compiled binary is available for download from GitHub releases, but do **not** install it for them.

Runner priority: Bun (`bunx`), then Node (`npx`), then compiled binary as a last resort. Never install the binary for the user — just let them know it exists if they have neither Bun nor Node. Every subcommand must work on a fresh machine; `setup` only verifies runtime + ffmpeg and shows examples.

The compiled binary expects a `hance-gpu` sidecar alongside it; a bare `./hance` checkout without it fails with `ENOENT … hance-gpu`. This is why `bunx`/`npx` are preferred — they always work. When developing in this repo, run the source directly: `bun run packages/cli/src/cli.ts …`.

## Hard rules

- Never invent flags. Only use names listed in `hance --help` or `hance preset --help`.
- Never run a full video render to explore looks — use `hance preview` (still frame) for `try`.
- Windows is unsupported. If `uname -s` reports Windows, stop and tell the user.

## References

- `references/preset-index.md` — `presets/index.json` schema and rebuild contract.
- `references/compare-page.md` — `/compare` route query params and Edit hand-off.
- `references/grading.md` — how to judge and dial in a film look: the render→read→adjust loop, what makes a grade read as film, and common artifacts. Read before `refine`.
