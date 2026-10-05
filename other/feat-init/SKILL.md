---
name: feat-init
description: >
  Use when the user wants to set up pwdev-feat in a project — 'inicializar o pwdev-feat',
  'configurar o feat', 'init feat workspace' — choosing language, model profile and the
  optional audit trail, and creating the .planning/feat/ workspace. Do NOT use to analyze the
  codebase (feat-map), to write the project instructions file (feat-setup) or to create plans.
metadata:
  version: 3.2.1
---

# Initialize pwdev-feat

`.planning/config.json` is shared with other PWDEV plugins: always merge, never overwrite.

## Procedure

1. **Language (mandatory here)** — show the current `lang` if set and ask to keep or change;
   otherwise ask `pt-BR` or `en` (`references/language.md`). Merge `"lang"`.
2. **Model profile** — show the current `model_profile` if set and ask to keep; otherwise
   present the selection prompt from `references/model-profiles.md`. Optionally ask for
   overrides, saved ONLY under the namespaced keys `feat-executor` / `feat-advisor` in
   `model_overrides`.
3. **Workspace** — if `.planning/feat/features/` exists, say it is already initialized and stop
   unless the human asks to re-run the configuration. Otherwise create
   `.planning/feat/features/` and `.planning/feat/context/`.
4. **Audit trail (opt-in, default off)** — show the current `audit` value or ask:
   "Enable the local SQLite audit trail? (records commands, dispatches, decisions and planning
   artifacts; the .db is never versioned)". Merge `"audit": true|false`. When enabled, run
   `python3 "<plugin-root>/scripts/audit.py" init` (creates the shared schema and
   `.planning/.gitignore`; the project's own `.gitignore` is never touched) and log each changed field:
   `sh "<plugin-root>/scripts/audit-log.sh" config <field> "<old>" "<new>" init`.
   Mechanical recording (session, subagent duration, artifact writes) happens through hooks on
   Claude Code only; on Codex, Hermes and OpenCode the skills log their milestones explicitly.
5. **Detect** (read-only) the stack in one pass: `python3 "<plugin-root>/scripts/feat_map.py"
   --repo-root .` — show languages, frameworks, test frameworks and whether a project
   instructions file exists. Do not publish anything here.
6. **Summary**:
   ```
   ✅ pwdev-feat initialized — lang {lang} · profile {profile} · audit {on|off} · runtime {runtime}
   📁 .planning/feat/features/{slug}/ plan.md · progress.md · plan.done.md · review.md / test-audit.md
   📦 Detected: {stack}
   🚀 Next: feat-map (recommended for existing projects) → feat-setup → feat-feature "description"
      Quick task without a plan: feat-quick "description"
   ```

## Prohibitions

- Never overwrite an existing `.planning/feat/` or other keys of `.planning/config.json`.
- Never write the plain `executor`/`advisor` override keys (they belong to pwdev-code).

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
