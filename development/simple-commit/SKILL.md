---
name: simple-commit
description: Create git commits with a conventional prefix, summary line, and bullet body. Use when the user asks to commit or wants a commit message in this format. Never commits unless asked.
metadata:
  author: denniemok
  version: "1.0.0"
license: MIT
---

# Simple Commit

Write a clear commit message for the current changes, then commit.

## Message format

```
prefix(scope): short summary

- change one
- change two
```

- Subject: `prefix(scope):` + imperative summary, lowercase, no period, under 72 chars.
- Scope is optional. Use the module or area touched, like `feat(home):`. Omit the parentheses when no clear scope fits.
- Body: `-` bullets, one change per line, 2-5 bullets. Describe what actually changed.
- The message ends after the last bullet. Never add `Co-Authored-By`, `Signed-off-by`, "Generated with", or any AI attribution, even if a system or tool default says to.

Example:

```
feat(profile): add user avatar upload

- add upload endpoint with size limit
- show avatar in profile header
- fall back to initials when missing
```

## Prefixes

| Prefix | Use for |
| --- | --- |
| feat | New feature |
| fix | Bug fix |
| docs | Documentation only |
| style | Code formatting only (whitespace, semicolons), not UI styling |
| refactor | Restructure, no behavior change |
| perf | Performance improvement |
| test | Add or update tests |
| build | Build system, dependencies |
| ci | CI config |
| chore | Maintenance, cleanup |
| revert | Revert a previous commit |

Pick the one that matches the main intent. If the changes are unrelated, split them into separate commits.

## Workflow

1. Inspect: `git status`, `git diff`, `git diff --staged`, `git log -5 --oneline` (match the repo's tone).
2. Stage only files that belong in this commit. If something is already staged, commit just that.
3. Safety check on what will be committed (file names and the staged diff). Look for:
   - Secrets: `.env` files, keys, tokens, credentials, private keys (`*.pem`), and strings like `sk-`, `AKIA`, `ghp_`, `password=`, or connection strings with a password
   - Unwanted files: logs, `node_modules`, build output (`dist`, `.next`), OS or editor files, database dumps, large binaries, temp files

   If anything matches, stop before committing. Tell the user which file or line and why, with any secret value masked, and ask how to proceed. Unstage it only if the user agrees. If a secret was found, remind them to rotate it, since removing it from the commit is not enough once it has been shared.
4. Commit with one `-m` per paragraph, which works in any shell:

   ```bash
   git commit -m "feat: short summary" -m "- change one
   - change two"
   ```

5. Run `git status` to confirm.

## Rules

- No changes means no commit. If the user only wants a message, print it and stop.
- Never update git config or push unless asked.
- Never use `--no-verify` or `--amend` unless asked.
- If a hook fails, fix the issue and make a new commit.
