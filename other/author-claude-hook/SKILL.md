---
name: author-claude-hook
description: >-
  Write a new Claude Code hook script for this repo following its established conventions, then wire it into
  claude/settings.json and give the user the settings snippet. Use when the user says "criar um hook", "fazer um
  hook que", "create a hook", "comando para colar no settings", or describes an automated behavior that should fire
  on a tool call / session event (PreToolUse, PostToolUse, SessionStart, Stop, UserPromptSubmit, SubagentStart/Stop).
license: CC-BY-4.0
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: 1.0.0
---

# Author a Claude Code Hook

Create a hook that matches the existing ~40 hooks in `hooks/scripts/`, wire it in `claude/settings.json`, add an eval.

## Phase 1 — Understand the trigger

Clarify with the user (use `grilling` if ambiguous):

- **Event**: `PreToolUse` (can block/allow), `PostToolUse` (inject context after), `SessionStart`, `Stop`, `UserPromptSubmit`, `SubagentStart`/`SubagentStop`, `PreCompact`.
- **Matcher**: tool regex (`Edit|Write`, `Bash`, `Read`) or `""` for all.
- **Effect**: inject `additionalContext` (most common), or gate a tool (`exit 2` = deny, with reason on stderr).
- **Dedup need**: should it re-announce every call, or back off (`NOTIFY_EVERY` pattern)?

Read 1–2 nearby hooks of the same event type before writing (`dir_context_refs.py` for PreToolUse+context, `impact_surface_hint.py` for PostToolUse+context, `protect_files.py` for gating, `start_context.py` for SessionStart).

## Phase 2 — Write the script

Follow `references/conventions.md` exactly: shebang `#!/usr/bin/python3`, `utils` import via `sys.path`, `get_hooks_logger("Name")`, read stdin with a `MAX_STDIN` cap, parse JSON defensively (exit 0 on any failure), use `get_by_key` for payload access, resolve project via `CLAUDE_PROJECT_DIR` env, wrap `main()` in `try/except logger.exception; sys.exit(0)`. A hook must never crash the tool call — every failure path is `sys.exit(0)`.

Output shape for context injection:

```python
json.dumps({"hookSpecificOutput": {
    "hookEventName": "PreToolUse",  # match the actual event
    "additionalContext": json.dumps({...})
}})
```

Save to `hooks/scripts/<snake_name>.py`, `chmod +x`.

## Phase 3 — Wire settings.json

Add the hook command under the right event/matcher block in `claude/settings.json`, using `$CLAUDE_PROJECT_DIR/.claude/hooks/scripts/<name>.py` (that is the deployed path — `.claude/` symlinks to the repo). Place it near sibling hooks of the same purpose. Keep the `log_hooks.py` entry last in its block.

Give the user the exact JSON snippet to paste, showing the full event block with the new entry in place.

## Phase 4 — Eval

Add `hooks/evals/<name>.json` (`mode`: `stdout` for context hooks, `exit_code` for gating hooks) with cases covering: the happy path (`expect_output: true` + `expect_pattern`), non-matching tool (no output), missing `file_path`/field (no output), malformed JSON (`raw_stdin`), empty stdin. Run `python3 hooks/evals/eval.py hooks/evals/<name>.json` and confirm all pass.

## Delivery

Report: hook path, the settings.json snippet (verbatim), eval result. One or two lines on what it does. Do not paste the full script body into chat.

## Reference files

- `references/conventions.md` — the exact boilerplate skeleton, `utils` helpers available, output shapes for each event, the dedup/back-off pattern, gating (`exit 2`) pattern, and the "never crash the tool call" rule.

---

_Traceability: recurring across 16+ session prompts ("criar um hook que…", "comando para colar no settings", "fazer um hook equivalente em python") and 29 `fix(hooks)` commits (Jul–Aug 2026) fixing the same classes of mistake — wrong env var for project root, missing dedup, matcher not covering `AskUserQuestion`, non-atomic cache writes, silent exceptions. Sources: `~/.claude/projects/-home-ronnas-develop-personal-AI-pair-programming/*.jsonl`, git log._
