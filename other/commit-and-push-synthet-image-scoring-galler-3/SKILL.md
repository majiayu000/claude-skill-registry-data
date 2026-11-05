---
name: commit-and-push
description: Use when the user asks to commit and push, publish, ship, or prepare a release commit. Guides staging only intended changes, writing a Conventional Commit, committing, and pushing to origin after verifying status and diff.
capability: "commit-and-push agent asset workflow"
side_effect_level: local_write
approval_required: false
requires_tools: "python scripts/harness.py; git; gh optional"
output_schema: "Inspect/verify report; commit/push only when explicitly executed"
risk_class: medium
---

# Commit and push (compiled harness)

Ship local work only when the user explicitly asks. Pair with `release-bump` when
`VERSION` / `CHANGELOG.md` were promoted.

## Invoke

```bash
# Dry-run inspect (default)
python scripts/harness.py --json

# Release prep: list + run framework verify
python scripts/harness.py --release --run-verify --json

# Only after explicit user request to commit/push:
python scripts/harness.py \
  --execute --commit -m "feat(scope): summary" --json
python scripts/harness.py --execute --push --json
```

## LLM judgment slots

- Draft Conventional Commit subject/body (`commit-conventions`).
- Prefer explicit path staging when unrelated dirty files exist (inspect `paths` first).

## Human / safety (enforced)

- Harness **defaults to dry-run**; `--execute` required for commit/push.
- Secret-looking paths (`.env`, `secrets.json`, keys) block staging.
- Never modify `.git/config`, never `--no-verify` unless user asked.
- Never force-push `main`/`master` unless user asked.
- Do not amend after a failed hook — new commit instead.

Resolve helper paths from this skill directory. Run project commands from the target workspace.
