---
name: commit
description: Verify, record and commit the current session's work — checks green first, PROGRESS updated, message via -F. Use when the user asks to commit; if they say "commit and push", chain into /push afterwards.
user-invocable: true
allowed-tools: Bash, Read, Edit, Write, Glob, Grep
---

# /commit — Verify, record, commit

Commit the session's work the way this repo requires: proven green, recorded
in the live PROGRESS log, message written to a file. **This app places real
orders with real money — a commit that overstates what it contains is the
exact failure the rules exist to prevent.**

## Steps

### 1. See what actually changed

```powershell
git status --short
git diff HEAD --stat
```

Read the list. If it contains changes you didn't make this session, stop and
tell the user what you found — never sweep in someone else's work silently.
If a frozen close-path file (`close_trade.py`, `partial_close.py`) or
anything under `services/trading|risk|broker` changed, confirm `/safe-change`
was followed and say so in the message.

### 2. Prove it green — scaled to what changed

- **Any code, test, or tools change** → `python -m tools.checks all` must
  pass (suite + all gates, ~6–8 min). Never edit tracked files while it
  runs. Paste the tail into the active pack's `PROGRESS.md` verification log.
- **Docs/skills only** → `python -m tools.checks gates` (~25s, includes the
  doc-links check) is sufficient. Say in the commit message that the change
  is docs-only.

A failing check stops the commit. Never `--no-verify`, never lower a
baseline to get green, never commit "just this once" on red.

### 3. Update the live records

- The active pack's `PROGRESS.md`: flip task rows, add the verification-log
  entry (real output, not a claim).
- If the change taught something non-obvious → the relevant
  `docs/system/domains/<domain>/` file, same commit.
- If the change invalidated a number/claim a skill quotes → fix that skill,
  same commit.

### 4. Commit — message via file, always

PowerShell 5.1 mangles multiline `-m`. Write the message to a scratch file
and use `-F`:

```powershell
git add -A          # or stage selectively if the tree mixes concerns
git commit -F <path-to-message-file>
git status --short  # must be clean (or intentionally holding back files)
```

`docs/todo/`, `docs/simon-handover/` and `docs/reviews/` (so PROGRESS.md
too) belong to the private notes repo, which plain `git` ignores. Commit them
separately with `git private add -A todo simon-handover reviews`,
`git private commit -F <msgfile>` and `git private push`. See CLAUDE.md,
"Private notes".

Message shape: one imperative subject line; a body saying what shipped, what
was deliberately NOT done, and the checks result. Never mention which AI
model made the change. Separate restructuring commits from behaviour
commits — if both happened, commit them separately.

### 5. Offer or chain the push

If the user asked to "commit and push", invoke `/push` now. Otherwise end by
telling the user the commit hash and that `/push` publishes it.

## Never

- commit on a red check, or skip step 2 because "it's small"
- bundle unrelated concerns into one commit to save time
- claim a task Done in PROGRESS without the demo/sign-off it requires
- commit secrets, `config.yaml`, `*.db`, licence keys (`.gitignore` covers
  these — but look at `git status` anyway)
