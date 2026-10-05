---
name: feat-map
description: >
  Use when the user wants the existing codebase analyzed for planning — 'mapear o código',
  'analisar o projeto', 'atualizar o contexto', 'map codebase' — or when a planning skill
  reports a missing or stale map. Runs a deterministic read-only evidence scan and writes
  codebase.md plus the architecture, conventions, testing and concerns context documents under
  .planning/feat/. Do NOT use for code review (feat-review), architecture decisions, or writing
  the project instructions file (feat-setup).
metadata:
  version: 3.2.1
---

# Map the codebase

Contract: `references/mapping.md`. The scanner owns traversal, secret exclusion and
determinism; you own interpretation and the context documents. Read-only on source code.

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. **Scan** — `python3 "<plugin-root>/scripts/feat_map.py" --repo-root . --write`. Report the
   `source_commit`, the previous map's staleness and `excluded_sensitive`. Commands in the
   output are evidence only — never run them.
3. **Interpret** — sample 2–3 representative files per module kind (entry points, a
   controller/handler, a service, a model, a component, a test) and read the style and test
   configs listed by the scan. Read the project instructions file if present. Do not read the
   whole repository.
4. **Dependency audit (optional)** — ask the human before running `npm audit` /
   `composer audit` / equivalent (they may hit the network). Declined → record `n/a`.
5. **Write** from `templates/context/*.md` and `templates/codebase.md`, keeping headings and
   keys; every claim cites its evidence path(s) and a confidence:
   - `.planning/feat/context/architecture.md`, `conventions.md`, `testing.md` (including
     `tests_dir`, `e2e_scenarios_dir`, `e2e_generated_dir` and the real commands),
     `concerns.md`;
   - `.planning/feat/codebase.md` — the one-screen index (kept for 2.x compatibility).
6. Record: `sh "<plugin-root>/scripts/audit-log.sh" event map "" completed .planning/feat/context/`.
7. **Summary**:
   ```
   🗺️ Codebase mapped at {short commit}
   Stack: {summary} | Pattern: {pattern} ({confidence})
   Size: {N} files, {N} modules | Tests: {frameworks} ({N} files) | E2E: {playwright|none}
   Risk areas: {top 3}
   📁 .planning/feat/codebase.md + context/{architecture,conventions,testing,concerns}.md
   👉 Next: feat-setup (if no project instructions file) or feat-feature "description"
   ```

## Prohibitions

- Never modify project source files — the only writes are under `.planning/feat/`.
- Never read secrets (the scanner skips them; do not open them by hand either) or copy any
  secret value into the documents.
- Never state a convention without an evidence path.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
