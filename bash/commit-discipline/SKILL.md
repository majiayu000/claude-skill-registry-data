---
name: commit-discipline
description: |
  Use this skill before creating any git commit. Triggers include:
  "ready to commit", "let me commit", "git commit", "stage the changes",
  "what should I include in this commit", "let's commit this", "time to commit".
  Always apply before staging files or running git commit.
---

# Commit Discipline

Enforces atomic commits, Conventional Commits format, and pre-commit verification.

## Pre-flight checks (run before staging)

1. **Verify you're not on `main`:**
   ```bash
   git branch --show-current
   ```
   If `main` → STOP. Create a feature branch: `git checkout -b <type>/<phase>-<short-name>`
   (e.g. `chore/phase1-bootstrap`, `feat/harness-sampler`).

2. **Check the diff size:** `git diff --stat` — target ≤ 300 changed lines; split by concern if larger.

3. **Tick TODO items:** if this commit completes a `docs/TODO.md` checkbox, tick it in the same commit.

4. **Docstrings:** any new public function/class has a docstring (params, returns, raises).

## Commit message format (Conventional Commits)

```
<type>(<scope>): <subject>

<optional body explaining WHY, referencing TODO ids>

<optional footer (Co-Authored-By, Closes #N)>
```

- **Types:** `feat | fix | docs | refactor | test | chore | perf | style | ci`
- **Scopes (HW5):** `harness | runners | metrics | economics | roofline | plotting | shared | cli | scripts | config | docs | ci`
- **Subject:** ≤ 72 chars, imperative, no trailing period.

Every commit authored in this repo ends with the agent co-author trailer when the agent did the work:
```
Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

## Pre-commit hooks (`.pre-commit-config.yaml`, run automatically)

- `ruff check --fix`, `ruff-format`, `mypy --strict src/`
- `scripts/check_file_sizes.py`, `scripts/check_anti_patterns.py`
- (`scripts/check_no_hardcoded.py` is added in Phase 3, once config exists.)

If any fail, the commit aborts. Read the output, fix, re-stage, re-commit. **Never `--no-verify`**
unless a documented emergency is recorded in `docs/PROMPTS.md`.

## Anti-patterns to refuse

- WIP / unfinished work to `main` → feature branch instead.
- Vague messages ("update", "fixes") → require a Conventional Commit.
- Refactor bundled with a feature → split.
- Secrets, `.env`, model weights (`*.safetensors`/`*.gguf`), leaked paths, or `AI Agent` authors.

## Verify before signaling success

`git log -1 --format=fuller` — confirm author/committer, subject format, and intended file list.
