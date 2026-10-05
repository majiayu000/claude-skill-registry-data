---
name: feat-audit
description: >
  Use when the user wants to query the local pwdev audit trail — 'ver auditoria', 'relatório de
  auditoria', 'audit stats', 'exportar auditoria em PDF' — summary, events, decisions,
  artifacts, statistics, a Markdown/PDF export or a custom read-only SELECT. Do NOT use to
  enable the audit (feat-init) or for plan status (feat-status).
metadata:
  version: 3.2.1
---

# Audit trail

Schema and recording model: `references/audit-schema.md`. The database is shared with other
PWDEV plugins; filter with `--plugin pwdev-feat` when the human wants only this plugin.

## Procedure

1. **Language** — resolve `lang` (`references/language.md`).
2. Map the argument to one command and run it from the project root:

   | Argument | Command |
   |---|---|
   | (empty) / `summary` | `python3 "<plugin-root>/scripts/audit.py" summary` |
   | `events [plugin]` | `... events [--plugin <plugin>] [--limit N]` |
   | `decisions` / `artifacts` / `stats` | `... decisions` / `... artifacts` / `... stats` |
   | `export` | `... export --pdf` (Markdown always; PDF only when pandoc exists) |
   | `query <SQL>` | `... query "<SQL>"` |

3. Exit 2 (`AUDIT_DISABLED` / `AUDIT_DB_MISSING`) → tell the human to enable it with
   `feat-init`. Exit 1 (`REJECTED` / `SQL_ERROR`) → show the message; only a single
   read-only SELECT is accepted and the database is opened read-only.
4. Present the Markdown output as is, translating only the headings when `lang` is `pt-BR`.
   Unknown argument → list the commands above.

Never write to the audit database from this skill.

Language: resolve `lang` per `references/language.md` before any human-facing output. Safety: never read or expose `.env*` (except `.env.example`/`.template`/`.sample`), keys, certificates or credentials — `references/safety.md`. Paths `references/`, `scripts/`, `templates/`, `schemas/` are relative to the plugin root (`references/runtime.md`).
