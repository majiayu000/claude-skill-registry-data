---
name: safe-ship
description: Ship local changes by inspecting dirty state, scoping the stage, running targeted validation, then committing, pushing, and checking remote gates. Use when the user asks to commit, push, ship, merge, deploy, or whether a diff is safe to push.
---

Inspect dirty state, stage only the requested scope, validate the touched surface, then commit, push, and verify the remote gate.

1. `git status --short --branch`, `git diff --stat`, `git diff --name-only`, `git log --oneline --decorate -5`.
2. Stage only the files for the asked fix. Stage the full dirty tree only when the user says `all` or `commit all`. Leave unrelated dirty files untouched and name them.
3. `git diff --check`, then the project format/lint/type/test/build commands that match the touched surface. Prefer targeted tests; widen when shared code, generated files, auth, payment, data, or routes changed.
4. Separate introduced failures from baseline noise. Local green is not a PR or deploy ready if GitHub, Vercel, or Netlify is the decisive gate.
5. Commit with a concise commitizen-style message. Push the correct branch.
6. Verify with `git status --short --branch`, `git rev-parse HEAD`, and the real external gate until it reaches the requested state or blocks.

Use `trash` for deletions. Quote paths that contain brackets. If generated files are a framework contract, check the sibling or starter repo before ignoring or committing them.

Finish with the SHA and branch, validation run, skipped or pending gates, and unrelated dirty files left alone.
