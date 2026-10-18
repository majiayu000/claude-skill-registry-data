---
name: render-loop
description: Project-local dev feedback loop for the session-export renderer. Use when asked to check, fix, or improve how a Claude Code / Codex session renders in the exported HTML — e.g. "check the rendering of tool call X around Y, see session <uuid>". Exports the session to HTML, screenshots the relevant card with headless Chrome so the result can be viewed, then guides editing skills/session-export and re-validating.
---

# render-loop

A self-checking loop for developing this repo's exporter. It lets you **see**
what the HTML actually renders (via a headless-Chrome screenshot you can open
with the Read tool), fix the renderer, and re-validate — without leaving the
session.

This skill is repo-local (`.claude/skills/render-loop/`) and not shareable: it
hard-codes this repo's layout (`skills/session-export/`) and assumes Google
Chrome + Node 18+.

## The loop

When the user points at a rendering concern and a session (e.g. *"the rendering
of TaskGet looks like raw JSON, see session 2e875f45…"*):

1. **Locate & classify the session.** A session id is a UUID. Claude sessions
   live under `~/.claude/projects/**/<uuid>.jsonl`; Codex rollouts under
   `~/.codex/sessions/**/rollout-*<uuid>*.jsonl`. If it's a Codex rollout, use
   `--codex`. You can pass a full path instead of an id.

2. **Inspect the raw record first.** Find the relevant `tool_use` / message in
   the jsonl to learn the exact input/result shape before changing code:
   ```
   grep -n '"name":"TaskGet"' <session.jsonl>   # or node one-liner to dump the block
   ```

3. **Export + screenshot the card.** From the repo root:
   ```
   .claude/skills/render-loop/render.sh <uuid-or-path> [--codex] --find "<text near the card>"
   ```
   `--find` text should be something visible in that card (a tool name, an arg,
   a phrase). It prints `HTML:` and `PNG:` paths. **Read the PNG** to view the
   current rendering. (Omit `--find` for a full-page capture, height-capped.)

4. **Diagnose.** Compare what you see against what the user wants. The renderer
   is `skills/session-export/template.js` (shared client renderer — tool cards
   live in the `renderToolCall` switch; entry/role logic in `renderEntry`/
   `renderRun`). Parsing/normalization is `export.js` (Claude) and
   `codex-export.js` (Codex); shared redaction in `redact.js`.

5. **Fix** the JS (usually a `case` in the `renderToolCall` switch, or a helper).

6. **Re-render & validate.** Re-run the same `render.sh …` command, Read the new
   PNG, and confirm it matches the requested outcome. Iterate steps 4–6 until
   it's right. Also run the cheap sanity check after edits:
   ```
   node -e 'const h=require("./skills/session-export/template.js")();const m=h.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);new Function(m[1]);console.log("ok")'
   ```

7. **Report** the change and offer to commit (template work currently lives on
   the `codex-export` branch).

## Tools in this skill

- `render.sh <session> [--codex] [--find "text"] [--index N]` — export then
  screenshot in one step (most common entry point).
- `shoot.js <file.html> [--find "text" | --selector css] [--index N] [--full]
  [--out png]` — screenshot any already-exported HTML. Drives Chrome over the
  DevTools Protocol with Node's built-in WebSocket (no npm deps); expands all
  collapsible cards, then crops to the matched element (or full page, capped at
  4000px). Override the browser with `CHROME_BIN`.

## Notes

- Exported HTML lands in the repo root (`claude-session-*` / `codex-session-*`,
  both gitignored); the PNG goes to `$TMPDIR/render-loop.png`. Both are scratch.
- `--find` matches the first card (`.tool`, `.askq`, `.subagent`, `.context`,
  `.command`, `.entry`) containing the text; use `--index N` to disambiguate.
- **Self-improving:** if the loop exposes a gap — `shoot.js` can't target what
  you need, a new card type isn't matchable, the diagnosis was slow — improve
  `shoot.js` / this `SKILL.md` as part of the task so the next loop is sharper.
