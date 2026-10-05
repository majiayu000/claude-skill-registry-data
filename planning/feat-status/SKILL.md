---
name: feat-status
description: >
  Use when the user asks for the state of pwdev-feat plans — 'status do feat', 'quais planos
  estão pendentes', 'show feature status' — listing pending, complete, with-caveats, failed and
  resumable plans plus codebase-context health. Read-only. Do NOT use to execute (feat-exec) or
  query the audit trail (feat-audit).
metadata:
  version: 3.2.1
---

# Feature status (read-only)

1. **Language** — resolve `lang` (`references/language.md`).
2. Run `python3 "<plugin-root>/scripts/feat_state.py" list` and
   `python3 "<plugin-root>/scripts/feat_map.py" --repo-root . --staleness`.
3. Present:
   ```
   📊 pwdev-feat status
   Pending: {N} | Complete: {N} | With caveats: {N} | Failed: {N} | Resumable: {N}
   Codebase context: {fresh at <commit> | stale (<N> files changed) | missing}
   Instructions file: {present | missing → feat-setup}

   Pending:      {slug} ({type}, {mode})       → feat-exec {slug}
   Resumable:    {slug} (step {n})             → feat-exec {slug} --resume
   Complete:     {slug} ✅
   With caveats: {slug} ⚠️  .planning/feat/features/{slug}/plan.done.md
   Failed:       {slug} ❌                      → feat-exec {slug}

   👉 Next: {the most useful next action}
   ```
   Show the runtime's own invocation form for commands (`/pwdev-feat:exec`, `$feat-exec`,
   `/feat-exec`...) — `references/runtime.md`.

Never modify files in this skill.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
