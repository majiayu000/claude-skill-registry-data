---
name: skillset-smoke-test
description: Run and evaluate the Skillset smoke test (aliases, sets, and skill invocation) and interpret its JSON reports. Use this when validating $skill/$set behavior or checking Claude Code/Codex headless runs.
---

# Skillset Smoke Test Runner

Keep this skill self-contained. If you need more detail, read `REFERENCE.md`.

## Prereqs

- Ensure `bun` is available.
- For full runs, ensure `claude` and `codex` CLIs are installed and authenticated.
- Run from the repo root so the smoke test can find `scripts/skillset-smoke.ts`.

## Run the smoke test

- Prefer the repo script so results are structured and gitignored.
- Quick smoke (hook-only):
  - `bun run test:smoke:ci`
- Hook-only (CLI mode):
  - `bun run test:smoke:cli`
- Full run (hook + Claude + Codex):
  - `bun run test:smoke`

## Options

- `--tools hook,claude,codex` to limit which tools run.
- `--hook-mode ci|cli` to choose the hook path (repeatable or comma-separated).
- `--no-clean` to preserve the sandbox workspace and XDG dirs.
- `--clean-all` to wipe all smoke test artifacts (workspace + reports).
- `--strict` to exit non-zero if any step fails.

## Environment overrides

- `SKILLSET_SMOKE_CLAUDE_CMD` (default: `claude`)
- `SKILLSET_SMOKE_CLAUDE_ARGS` (extra args)
- `SKILLSET_SMOKE_CODEX_CMD` (default: `codex`)
- `SKILLSET_SMOKE_CODEX_ARGS` (extra args)

## Interpret results

- Reports live under `.skillset-smoke/reports/<runId>/report.json`.
- Check `steps[*].status` and `steps[*].details.evidence` for sentinel hits.
- When a step fails, inspect its `stdoutPath`/`stderrPath` for errors.
  - Hook steps are labeled `hook-ci` and `hook-cli`.
  - The smoke test cleans by default; re-run with `--no-clean` to keep state for debugging.

## Triage checklist

Use this checklist in order when a run fails or evidence is missing:

1. Open the report JSON and find the first `steps[*].status !== "ok"`.
2. If `stdoutPath`/`stderrPath` exist, read them for the error message.
3. Confirm the workspace and XDG paths in the report (they must be under `.skillset-smoke/`).
4. If a tool step is `skipped`, verify the CLI is installed and auth is valid.
5. If `hook` evidence is missing for a set, confirm the set resolves in `set-load` and re-run `--tools hook` to isolate hook output issues.
6. If sentinels are missing for skills, confirm the smoke test created fixtures in `.skillset-smoke/workspace/.claude/skills`.
7. Re-run with `--tools hook` to isolate local resolution issues before retrying full runs.

## Notes

- Outputs are stored under `.skillset-smoke/` and are gitignored.
- If the `.codex/skills` symlink is missing, re-create it to mirror this skill.
