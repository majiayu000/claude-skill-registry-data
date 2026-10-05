---
name: prd-init
description: >
  Use when the user wants to set up pwdev-prd in a project — 'inicializar o pwdev-prd', 'init
  prd', 'configurar PRDs' — creating the .planning/prds/ workspace and choosing language and the
  optional SQLite audit trail. Do NOT use to write a PRD (prd-create).
metadata:
  version: 3.0.0
---

# Initialize pwdev-prd

## STEP 0 — Language Configuration

This is the initialization command, so language setup is **mandatory** here (not silent).

1. Read `.planning/config.json` — if `lang` already exists, show current setting and ask:
   ```
   Idioma atual / Current language: {lang}
   Deseja manter? / Keep it? (y/n)
   ```
   If yes → proceed. If no → go to step 2.

2. If no config or user wants to change, **always ask explicitly**:
   ```
   Em qual idioma deseja trabalhar? / Which language would you like to use?

   1. Portugues (PT-BR)
   2. English (EN)
   ```
   Wait for the user's response.

3. Save the choice to `.planning/config.json`:
   - If file exists, merge the `lang` field (do not overwrite other fields).
   - If file does not exist, create it:
     ```json
     {
       "lang": "pt-BR"
     }
     ```

4. Confirm:
   - `pt-BR`: "Idioma definido: **Portugues (PT-BR)**"
   - `en`: "Language set: **English (EN)**"

All subsequent output in this command must follow the resolved language.

Technical terms (API, CRUD, REST, endpoint) always stay in English regardless of language choice.

## STEP 0.1 — Model Profile (informational only)

The interview runs inline on the session model, and the only subagent
(`pwdev-prd:roadmap`) declares `model: inherit` — pwdev-prd never resolves a model. Do NOT configure
`model_profile` here:

- If `.planning/config.json` already has `model_profile` (set by pwdev-code
  or pwdev-feat), leave it untouched — it belongs to plugins with subagents.
- If it's absent, skip silently — nothing in this plugin reads it.

## STEP 1 — Check if already initialized

```bash
if [ -d ".planning/prds" ]; then
  echo "ALREADY_INITIALIZED"
  ls .planning/prds/ 2>/dev/null
else
  echo "NEW"
fi
```

If already initialized:
```
⚠️ pwdev-prd already initialized.
   Workspace: .planning/prds/
   Existing PRDs: [list]
   Use /pwdev-prd:create to start a new PRD.
```

## STEP 2 — Create workspace

```bash
mkdir -p .planning/prds
```

## STEP 2.1 — Audit Trail (opt-in, disabled by default)

The audit trail records all commands, decisions, and artifacts in a local SQLite database.
It is **disabled by default** and the database file is **never versioned** (added to `.gitignore`).

1. Read `.planning/config.json` — if `audit` field already exists, show current setting and ask:
   - PT-BR: `Trilha de auditoria atual: {enabled/disabled}. Deseja manter? (s/n)`
   - EN: `Current audit trail: {enabled/disabled}. Keep it? (y/n)`
   If yes → proceed (skip to step 3 if disabled). If no → go to step 2.

2. If no config or user wants to change, ask:

   **PT-BR:**
   ```
   Deseja ativar a trilha de auditoria SQLite? (registra comandos, decisoes e artefatos)
   O arquivo .db nao e versionado (adicionado ao .gitignore).

   1. Sim — ativar auditoria
   2. Nao — desativar (padrao)

   Escolha (1-2, padrao: 2):
   ```

   **EN:**
   ```
   Enable SQLite audit trail? (records commands, decisions, and artifacts)
   The .db file is not versioned (added to .gitignore).

   1. Yes — enable audit
   2. No — disable (default)

   Choose (1-2, default: 2):
   ```

3. Save the choice to `.planning/config.json` — merge `"audit": true` or `"audit": false`.

4. If audit is **enabled** and `sqlite3` is available:

   ```bash
   if command -v sqlite3 >/dev/null 2>&1 && [ ! -f ".planning/pwdev-audit.db" ]; then
     sqlite3 .planning/pwdev-audit.db "
       CREATE TABLE IF NOT EXISTS events (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           timestamp TEXT NOT NULL DEFAULT (datetime('now')),
           session_id TEXT, plugin TEXT NOT NULL, command TEXT NOT NULL,
           agent TEXT, model TEXT, phase TEXT, action TEXT NOT NULL,
           target TEXT, detail TEXT, duration_ms INTEGER
       );
       CREATE TABLE IF NOT EXISTS decisions (
           id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER REFERENCES events(id),
           timestamp TEXT NOT NULL DEFAULT (datetime('now')), phase TEXT NOT NULL,
           decision TEXT NOT NULL, rationale TEXT, alternatives TEXT, reversible INTEGER DEFAULT 1
       );
       CREATE TABLE IF NOT EXISTS artifacts (
           id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER REFERENCES events(id),
           path TEXT NOT NULL, type TEXT NOT NULL, phase TEXT, status TEXT DEFAULT 'active',
           created_at TEXT NOT NULL DEFAULT (datetime('now')), archived_at TEXT
       );
       CREATE TABLE IF NOT EXISTS config_changes (
           id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL DEFAULT (datetime('now')),
           field TEXT NOT NULL, old_value TEXT, new_value TEXT NOT NULL, changed_by TEXT
       );
       CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
       CREATE INDEX IF NOT EXISTS idx_events_plugin ON events(plugin);
       CREATE INDEX IF NOT EXISTS idx_events_command ON events(command);
     "
   fi
   ```

   (Full schema reference: `<plugin-root>/references/audit-schema.md`.
   The database is SHARED with pwdev-code/pwdev-feat — any plugin's init may
   create it. Once the DB exists, recording is automatic via the plugin's
   hooks — no inline INSERTs.)

   Ensure `.planning/pwdev-audit.db` is in `.gitignore`:
   ```bash
   if ! grep -q "pwdev-audit.db" .gitignore 2>/dev/null; then
     printf '\n# PWDEV audit trail (not versioned)\n.planning/pwdev-audit.db\n.planning/pwdev-audit.db-journal\n.planning/pwdev-audit.db-wal\n.planning/.audit-tmp/\n' >> .gitignore
   fi
   ```

   Log the initialization event and config changes (best-effort):
   ```bash
   sh "<plugin-root>/scripts/audit-log.sh" event init "" completed .planning/prds/ ""
   sh "<plugin-root>/scripts/audit-log.sh" config lang "$OLD_LANG" "$NEW_LANG" init
   sh "<plugin-root>/scripts/audit-log.sh" config audit "$OLD_AUDIT" "$NEW_AUDIT" init
   ```

5. If audit is **disabled**, skip silently. Confirm:
   - PT-BR: `Trilha de auditoria: **{ativada/desativada}**`
   - EN: `Audit trail: **{enabled/disabled}**`

## STEP 3 — Summary

```
✅ pwdev-prd initialized

📁 Workspace created:
  .planning/prds/           # PRDs will be stored here
    └── {slug}/
        ├── PRD.md           # Structured PRD document
        └── prd.json         # Optional JSON export

🚀 Next steps:
  /pwdev-prd:create "feature or system description"
  /pwdev-prd:list                → View existing PRDs
```

## Prohibitions
- NEVER overwrite existing `.planning/prds/` without confirmation

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
