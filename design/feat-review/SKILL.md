---
name: feat-review
description: >
  Use when the user wants a code review of an explicit range or set of files — correctness,
  security, performance, conventions, tests — with stable findings (CR-nnn, BLOCKER..INFO) and
  rule citations — 'revisar os últimos commits', 'code review da feature X', 'review
  base..HEAD'. Plans a REPORT-mode review (no code changes, no commit). Do NOT use to fix code
  (feat-feature / feat-quick), to write tests (feat-test) or for UI/UX design critique.
metadata:
  version: 3.2.1
---

# Review plan

Plan type **review** — always executed in **REPORT** mode: findings only, no code change, no
commit. The review contract (scope, finding fields, severities, dimensions, verdict) is
`references/review.md`; read it before planning.

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. **Fix the scope** — resolve the argument into an explicit `BASE..TARGET` range:
   - a feature slug → `base_commit` from its `progress.md`/`plan.done.md` to `HEAD`;
   - "last N commits" → `HEAD~N..HEAD`; a branch → `$(git merge-base main <branch>)..<branch>`;
   - paths only → the range that last touched them, confirmed with the human.
   Record (audit on): `sh "<plugin-root>/scripts/audit-log.sh" event review "" scope <base>..<target>`.
   Build the package: `sh "<plugin-root>/scripts/review_package.sh" <base> <target>
   .planning/feat/features/{slug}/review [-- <paths>]`. Exit 2/3 (bad or empty range) → stop
   and ask; never widen the scope silently.
3. **Method** — follow `references/pwdevia-method.md` with `plan_type: review`:
   - Persona: senior code reviewer for the stack in `context/architecture.md`.
   - §3 lists the package files, the project instructions file, `context/conventions.md`,
     `context/concerns.md` and, when reviewing a feature, its `plan.md`.
   - §4 lists ONLY `.planning/feat/features/{slug}/review.md` (rendered from
     `templates/review-report.md`) — this is what puts the executor in REPORT mode. Do not name it
     `report.md`: some runtimes refuse subagent writes to report-like names.
   - §5: every finding has id, severity, `path:line`, rule citation, evidence and suggestion;
     the five dimensions are covered; lint/test commands run on the target and recorded.
4. After execution, when the verdict is `CHANGES_REQUESTED`, offer to turn the report's fix
   scope into a fix plan (`feat-feature` or `feat-quick`), citing the report in §3.

## Prohibitions

- Never fix code in a review plan, and never list project files in §4.
- Never skip the security dimension.
- Never rate a cosmetic issue above LOW, or a finding without a rule citation above LOW.
- Never move HEAD in the working checkout — use a temporary worktree to inspect other states.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
