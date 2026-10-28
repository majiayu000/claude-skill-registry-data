---
name: implement
description: Default workflow for building or changing code end to end — explore, plan with todos, make small verified edits, run diagnostics/build/tests, and summarise. USE WHEN the user asks to add a feature, change behaviour, "build", "implement", "make it do X", "wire up", or hands over a plan/design to execute.
---

# Implement

Goal: working, verified code that looks like the rest of the project — no half-finished steps, no claims without proof.

## 1. Orient (read before you write)
- Open the relevant area: `grep_search` / `find_symbol` for the feature's nouns, then `read_file` the files you will edit **in full or in large ranges** — never edit a file you haven't read.
- Note the local conventions (naming, imports style, error handling, logging, tests location) and the build/test commands (package manifest scripts, Makefile, CI config). Save stable ones with `memory_save` if not already in memory.
- If a design doc or requirements file exists for this work, read it first and follow it.

## 2. Plan
- For anything beyond a two-line fix call `manage_todos` with concrete steps ("Add `parseRange()` to src/util.ts", "Wire into handler", "Unit tests", "Build + lint", "Summary"). Mark items `in_progress` / `done` as you go — the user watches the list.
- Prefer a vertical slice that works end to end over finishing one layer completely.

## 3. Edit
- Use `edit_file` with precise `old_text` anchors (include 2–3 unchanged lines of context); use `write_file` only for new files.
- Small, idiomatic changes. Reuse existing helpers. Match formatting exactly (indentation, quotes, semicolons, trailing commas).
- Keep behaviour changes minimal and intentional; don't refactor unrelated code, rename things, or add comments/docstrings to code you didn't change.
- Handle errors at the boundaries the codebase already uses; don't add defensive code for impossible cases.
- Security: validate external input, never build shell/SQL/HTML from untrusted strings, never hard-code secrets, keep dependencies you add minimal and well-known.

## 4. Verify after every meaningful step
- `get_diagnostics` on each edited file — fix every new error and warning you introduced.
- Run the project's build / typecheck / lint via `run_command` (e.g. `npm run build`, `tsc --noEmit`, `cargo check`, `go vet`, `python -m pyflakes`). Then the relevant tests (narrow first: one file/test, then the suite).
- For UI work: start/reuse the dev server, then `browser_inspect` the page (it reports console errors, failed requests and layout problems) and fix what it finds; `open_browser` to show the user.
- If something fails, read the real error, form a hypothesis, fix, re-run. Don't retry the same thing hoping for a different result; don't "fix" by deleting tests or weakening assertions.

## 5. Finish
- All todos `done` (or explicitly `skipped` with a reason).
- Summary in chat (short): what changed (file list with one phrase each), how it was verified (commands + result), anything left open or worth a follow-up. Mention any assumption you made.

## Rules
- Don't stop at "here's how you could do it" — do it. The task is complete only when the code runs and verification passed.
- One concise `ask_user` question if blocked by a genuine decision; otherwise make the sensible choice and state it in the summary.
- Never fabricate output. If a command can't run here, say so.
