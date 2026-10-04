---
name: cursor-agent
description: >
  Run Cursor Agent CLI for coding tasks — writing, editing, refactoring, reviewing, or
  planning code — without spending OpenClaw API credits. Use when the user asks to
  write/fix/refactor/review code, a coding task would otherwise be done inline with
  Sonnet/Haiku, the user says "do this in cursor" or "use cursor for this", or any
  substantial file-editing task in a known repo. NOT for conversational questions about
  code (answer inline) or tiny one-liners that don't warrant a subprocess.
metadata:
  requiredBinaries: ["agent"]
---




### Credential Fixture Review

`python scripts/_secrets_inline.py` is review material for the `Cursor Agent` skill. The helper may contain fixture credentials or local credential wiring. Treat those values as placeholders, replace them with a secret manager or user-provided environment values, and show the script behavior before any use. Do not contact external services with embedded sample credentials.

# Cursor Agent

Cursor Agent CLI runs on the user's Cursor subscription — zero API cost. Always prefer it over inline code generation for any non-trivial coding task.

## Prerequisites

**Required binary: `agent`** (Cursor Agent CLI)

Install from the official site: https://cursor.com/docs/cli/overview — then verify with `agent --version`.
The helper script (`scripts/run.sh`) will exit with an error if `agent` is not found in PATH.

## User Consent Required — MANDATORY

This skill MUST NOT be invoked autonomously. Every invocation requires:

1. **State intent first** — tell the user: the repo, the task, the model, and whether files will be changed
2. **Wait for explicit "yes"** — do not proceed without clear user approval
3. **Default to read-only** — use `run.sh <repo> <task> <model> ask` unless the user explicitly asks for changes
4. **Before writing files** — run in `ask` mode first, show the user the plan, then ask: *"Apply these changes?"*
5. **Before `--cloud`** — explicitly warn: *"This will send repo contents to cursor.com. OK to proceed?"*
6. **Before committing** — show the diff and get confirmation

The helper script (`scripts/run.sh`) defaults to `ask` (read-only). Pass `write` as the mode argument only after the user has confirmed changes should be applied.

## Model Routing

| Task type | Model flag | Mode flag |
|---|---|---|
| Trivial / exploratory | *(omit — `auto`)* | *(omit)* |
| Bug fix / feature / refactor | `--model sonnet-4.6` | *(omit)* |
| Code review / explain (read-only) | `--model sonnet-4.6` | `--mode=ask` |
| Architecture / design planning | `--model opus-4.6-thinking` | `--mode=plan` |
| Long background task | `--model sonnet-4.6` | use `--cloud` instead of `-p` |

## Headless Commands

**Read-only first** — always start with `--mode=ask` to review before applying changes:
```bash
cd <repo> && agent -p "<task>" --model sonnet-4.6 --mode=ask --output-format text --trust
```

**Apply changes** — only after user confirms the plan:
```bash
cd <repo> && agent -p "<task>" --model sonnet-4.6 --force --output-format text --trust
```

**Cloud/background** — warn user that repo data goes to cursor.com:
```bash
cd <repo> && agent -c "<task>" --model sonnet-4.6 --trust
# Monitor at: cursor.com/agents
```

## Git Rule

Cursor sandbox blocks `git commit`. Always commit manually after Cursor edits:
```bash
cd <repo> && git add -A && git commit -m "<conventional commit message>" && git push
```

Show the diff to the user and confirm before committing if the change is large or touches sensitive areas.

## Repos & Workdirs

- Always `cd` to the correct repo before running
- Check for `.cursor/rules` and `AGENTS.md` in the repo root — Cursor loads these automatically for project context

## Context & Sessions

- Add `@<file>` in prompt to include specific files in context
- `--continue` or `--resume` to continue a previous session
- `agent ls` to list previous sessions

## Output Handling

- `--output-format text` → clean final answer, summarise key changes to the user
- `--output-format json` → structured, use for scripted parsing
- Always report back: what changed, what was committed, any issues found

## References

- Model list & details: `references/models.md`
- Slash commands (interactive mode): `references/slash-commands.md`
