---
name: feat-quick
description: >
  Use when the user wants a small, well-bounded change done now without a plan file — a
  bugfix, config change, rename, doc update or simple refactor touching 1–5 files — 'corrigir
  rapidinho', 'quick fix no X', 'renomear Y'. Presents a mini-plan, implements after approval,
  verifies and commits. Do NOT use for more than 5 files, architectural decisions, migrations
  or new UI flows (use feat-feature / feat-backend / feat-frontend).
metadata:
  version: 3.2.1
---

# Quick task (no plan file)

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. **Assess (silent)** — read the project instructions file (`references/project-files.md`)
   and `.planning/feat/codebase.md` if present. Eligible only if ≤5 files and no
   architectural decision, schema migration or new UI flow; otherwise say which skill to use
   and stop.
3. **Mini-plan (gate)** — present and wait for approval:
   ```
   📋 Quick Task
   Objective: {1 sentence}
   Files: {list with action}
   Approach: {2-3 sentences}
   Verification: {real command(s)}
   Proceed? (y/n)
   ```
4. **Implement** following the project conventions. Anything unexpected (a 6th file, a
   dependency, a design decision) → stop and escalate to the right planning skill.
5. **Verify** — the commands declared in the project instructions file (Commands/Quality);
   otherwise detect the toolchain and run its lint + tests. Never chain unrelated toolchains
   with `||`. UI change → verify it with `playwright-cli` in the session `feat-quick`, run from a scratch
   evidence directory outside the project, when available (`references/testing.md`); record
   `NOT_RUN` otherwise. Before committing, `git status --porcelain` must show only the approved
   files — delete tool side effects, never commit them.
6. **Commit** only the files of the approved mini-plan, with a Conventional Commit, after lint
   and tests pass. On the default branch, ask first.
7. **Record** (audit on): `sh "<plugin-root>/scripts/audit-log.sh" event quick "" completed <commit> "<files>"`.
8. **Result**:
   ```
   ✅ Quick task complete
   Done: {what changed}
   Verification: {command → exit code}
   Commit: {hash} {message}
   ```

## Prohibitions

- Never execute without mini-plan approval.
- Never touch more than 5 files — escalate instead.
- Never commit without lint + tests passing.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
