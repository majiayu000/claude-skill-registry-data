---
name: git-commit-checklist
description: Verify scope, checks, and local policy before committing.
---

# Git commit checklist

Read applicable `AGENTS.md` and their declared adapter alias, otherwise
`.agents/skills/git-commit-checklist/SKILL.md` from the repository root if present.
Local policy overrides these defaults; do not reload an already-read adapter or canonical skill.

Use before every commit. Read local `AGENTS.md`, contribution guidance, and hook
output first; they own commit format, required trailers, file-size limits, and validation commands.

1. Inspect `git status` and the complete diff. Stage only files that implement the accepted task.
2. Confirm new or changed source and test files meet local size, formatting, and generated-file
   policy. Do not commit credentials, build outputs, editor state, or unrelated changes.
3. Run focused tests and required local checks. Record any permitted skipped check and why.
4. Use the repository's conventional subject and required body/trailers. If code was extracted,
   record the required provenance in the commit body.
5. Re-read the staged diff and commit message before committing. Do not amend another author's
   work or rewrite history unless local policy and explicit authorization allow it.

Local instructions or the consumer wrapper own: branch names, file-size budgets, commit
conventions, pull-request templates, and push commands.

When an authorized rebase push may race another writer, capture the remote tip before fetching and
push with an exact expected-tip lease. A lease against a freshly fetched tracking ref can overwrite
the concurrent change it was meant to protect.
