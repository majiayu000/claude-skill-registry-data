---
name: prd-audit
description: >
  Use when the user asks about the pwdev-prd audit trail — 'auditoria do prd', 'eventos',
  'decisões registradas', 'audit report', 'exportar relatório de auditoria' — querying the
  shared SQLite database read-only (summary, events, decisions, artifacts, stats, export,
  query).
metadata:
  version: 3.0.0
---

# PRD audit trail

## Role
Utility command that queries the SQLite audit database (`.planning/pwdev-audit.db`) and presents results in readable format.

## How data gets here (v2.0)
Recording is deterministic — no inline INSERTs:
- **Plugin hooks** (`hooks/hooks.json` → `scripts/audit-hook.sh`): session
  start/stop and `.planning/` artifact writes, with `session_id`.
- **Commands** call `scripts/audit-log.sh` at milestones (`event`) and for
  configuration changes (`config` → `config_changes` table).
Schema reference: `<plugin-root>/references/audit-schema.md`.
The database is SHARED with pwdev-code/pwdev-feat — filter this plugin's rows
with `WHERE plugin='pwdev-prd'`.

## Pre-check

1. Read `.planning/config.json` — if `audit` is not `true`, stop with:
   - PT-BR: `Trilha de auditoria nao esta ativada. Execute /pwdev-prd:init para habilitar.`
   - EN: `Audit trail is not enabled. Run /pwdev-prd:init to enable it.`

2. Check if database exists:
   ```bash
   [ -f ".planning/pwdev-audit.db" ] || echo "NOT_FOUND"
   ```
   If NOT_FOUND, stop with:
   - PT-BR: `Banco de auditoria nao encontrado em .planning/pwdev-audit.db`
   - EN: `Audit database not found at .planning/pwdev-audit.db`

3. Verify `sqlite3` is available:
   ```bash
   command -v sqlite3 >/dev/null 2>&1 || echo "NO_SQLITE3"
   ```
   If NO_SQLITE3, stop with:
   - PT-BR: `sqlite3 nao encontrado. Instale o SQLite para usar este comando.`
   - EN: `sqlite3 not found. Install SQLite to use this command.`

## STEP 0 — Language
Follow `<plugin-root>/references/language.md` (resolve `lang` from
`.planning/config.json`; ask only if unset).

## STEP 1 — Parse Sub-command

Parse `the arguments` to determine the sub-command:

| Argument | Action |
|----------|--------|
| (empty) or `summary` | Go to STEP 2 — Summary Dashboard |
| `events` | Go to STEP 3 — Event Log |
| `decisions` | Go to STEP 4 — Decision Log |
| `artifacts` | Go to STEP 5 — Artifact Tracker |
| `stats` | Go to STEP 6 — Statistics |
| `export` | Go to STEP 7 — Export PDF Report |
| `query <SQL>` | Go to STEP 8 — Custom Query |

If unrecognized, show help:
```markdown
## /pwdev-prd:audit

Available sub-commands:

  summary    — Dashboard with key metrics and recent activity (default)
  events     — Full event log with filters
  decisions  — All architectural/product decisions with rationale
  artifacts  — Files tracked by the framework
  stats      — Command frequency, durations, phase distribution
  export     — Generate a full PDF audit report
  query <SQL> — Run a custom SQL query against the audit database

Examples:
  /pwdev-prd:audit
  /pwdev-prd:audit events
  /pwdev-prd:audit decisions
  /pwdev-prd:audit stats
  /pwdev-prd:audit export
  /pwdev-prd:audit query "SELECT * FROM events WHERE action='failed'"
```

---

## STEP 2 — Summary Dashboard (default)

Run the following queries:

```bash
# Total events
sqlite3 .planning/pwdev-audit.db "SELECT COUNT(*) FROM events;"

# Events by action
sqlite3 .planning/pwdev-audit.db "SELECT action, COUNT(*) as count FROM events GROUP BY action ORDER BY count DESC;"

# Last 10 events
sqlite3 -header -column .planning/pwdev-audit.db "SELECT timestamp, plugin, command, agent, action, target FROM events ORDER BY timestamp DESC LIMIT 10;"

# Total decisions
sqlite3 .planning/pwdev-audit.db "SELECT COUNT(*) FROM decisions;"

# Active artifacts count
sqlite3 .planning/pwdev-audit.db "SELECT COUNT(*) FROM artifacts WHERE status='active';"

# Failed commands (if any)
sqlite3 -header -column .planning/pwdev-audit.db "SELECT timestamp, plugin, command, detail FROM events WHERE action='failed' ORDER BY timestamp DESC LIMIT 5;"

# Config changes count
sqlite3 .planning/pwdev-audit.db "SELECT COUNT(*) FROM config_changes;"
```

Present as:
```markdown
## Audit Trail — Summary

**Total events:** N | **Decisions:** N | **Active artifacts:** N | **Config changes:** N

### Events by Action
| Action | Count |
|--------|-------|
| completed | N |
| started | N |
| ... | ... |

### Last 10 Events
| Timestamp | Plugin | Command | Agent | Action | Target |
|-----------|--------|---------|-------|--------|--------|
| ... | ... | ... | ... | ... | ... |

### Failed Commands (last 5)
[None | table]
```

---

## STEP 3 — Event Log

```bash
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT id, timestamp, plugin, command, agent, model, phase, action, target,
         SUBSTR(detail, 1, 80) as detail_preview
  FROM events
  ORDER BY timestamp DESC
  LIMIT 50;
"
```

Present as a formatted table. If there are more than 50 events, note:
- PT-BR: `Mostrando os 50 eventos mais recentes. Use /pwdev-prd:audit query para consultas customizadas.`
- EN: `Showing the 50 most recent events. Use /pwdev-prd:audit query for custom queries.`

---

## STEP 4 — Decision Log

```bash
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT d.id, d.timestamp, d.phase, d.decision, d.rationale,
         d.alternatives, CASE d.reversible WHEN 1 THEN 'Yes' ELSE 'No' END as reversible
  FROM decisions d
  ORDER BY d.timestamp DESC;
"
```

Present as:
```markdown
## Decisions

| # | Timestamp | Phase | Decision | Rationale | Alternatives | Reversible |
|---|-----------|-------|----------|-----------|--------------|------------|
| ... | ... | ... | ... | ... | ... | ... |
```

If no decisions, note:
- PT-BR: `Nenhuma decisao registrada na trilha de auditoria.`
- EN: `No decisions recorded in the audit trail.`

---

## STEP 5 — Artifact Tracker

```bash
# Active artifacts grouped by type
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT type, COUNT(*) as count
  FROM artifacts
  WHERE status='active'
  GROUP BY type
  ORDER BY count DESC;
"

# Full artifact list
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT id, path, type, phase, status, created_at, archived_at
  FROM artifacts
  ORDER BY created_at DESC;
"
```

Present as:
```markdown
## Artifacts

### By Type
| Type | Count |
|------|-------|
| ... | ... |

### All Artifacts
| Path | Type | Phase | Status | Created | Archived |
|------|------|-------|--------|---------|----------|
| ... | ... | ... | ... | ... | ... |
```

---

## STEP 6 — Statistics

```bash
# Command frequency
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT command, COUNT(*) as runs
  FROM events
  WHERE action='completed'
  GROUP BY command
  ORDER BY runs DESC;
"

# Average duration per command (when available)
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT command, COUNT(*) as runs,
         ROUND(AVG(duration_ms)/1000.0, 1) as avg_sec,
         ROUND(MIN(duration_ms)/1000.0, 1) as min_sec,
         ROUND(MAX(duration_ms)/1000.0, 1) as max_sec
  FROM events
  WHERE duration_ms IS NOT NULL AND action='completed'
  GROUP BY command
  ORDER BY avg_sec DESC;
"

# Events by phase
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT phase, COUNT(*) as count
  FROM events
  WHERE phase IS NOT NULL
  GROUP BY phase
  ORDER BY count DESC;
"

# Events by plugin
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT plugin, COUNT(*) as count
  FROM events
  GROUP BY plugin
  ORDER BY count DESC;
"

# Activity timeline (events per day, last 14 days)
sqlite3 -header -column .planning/pwdev-audit.db "
  SELECT DATE(timestamp) as day, COUNT(*) as events
  FROM events
  WHERE timestamp >= datetime('now', '-14 days')
  GROUP BY day
  ORDER BY day DESC;
"

# Success rate
sqlite3 .planning/pwdev-audit.db "
  SELECT
    ROUND(100.0 * SUM(CASE WHEN action='completed' THEN 1 ELSE 0 END) / COUNT(*), 1) as success_pct,
    SUM(CASE WHEN action='completed' THEN 1 ELSE 0 END) as completed,
    SUM(CASE WHEN action='failed' THEN 1 ELSE 0 END) as failed
  FROM events
  WHERE action IN ('completed', 'failed');
"
```

Present as:
```markdown
## Statistics

### Command Frequency
| Command | Runs |
|---------|------|
| ... | ... |

### Performance (avg duration)
| Command | Runs | Avg (s) | Min (s) | Max (s) |
|---------|------|---------|---------|---------|
| ... | ... | ... | ... | ... |

### Events by Phase
| Phase | Count |
|-------|-------|
| ... | ... |

### Events by Plugin
| Plugin | Count |
|--------|-------|
| ... | ... |

### Activity (last 14 days)
| Day | Events |
|-----|--------|
| ... | ... |

### Success Rate
**N%** (N completed / N failed)
```

---

## STEP 7 — Export PDF Report

Generate a comprehensive audit report as PDF.

### STEP 7.1 — Check Dependencies

```bash
command -v python3 >/dev/null 2>&1 && python3 -c "import weasyprint" 2>/dev/null && echo "WEASYPRINT_OK"
command -v python3 >/dev/null 2>&1 && python3 -c "import markdown" 2>/dev/null && echo "MARKDOWN_OK"
command -v pandoc >/dev/null 2>&1 && echo "PANDOC_OK"
command -v wkhtmltopdf >/dev/null 2>&1 && echo "WKHTMLTOPDF_OK"
```

Determine the PDF generation strategy based on available tools (in priority order):

1. **pandoc** (preferred) — `pandoc` available
2. **weasyprint** — `python3` + `weasyprint` + `markdown` available
3. **wkhtmltopdf** — `wkhtmltopdf` available
4. **None** — fallback to Markdown export only

If no PDF tool is available, inform:
- PT-BR: `Nenhuma ferramenta de PDF encontrada. Gerando relatorio em Markdown. Para PDF, instale: pandoc (recomendado), weasyprint, ou wkhtmltopdf.`
- EN: `No PDF tool found. Generating Markdown report. For PDF, install: pandoc (recommended), weasyprint, or wkhtmltopdf.`

### STEP 7.2 — Collect All Data

Run all queries from STEP 2 (Summary), STEP 3 (Events), STEP 4 (Decisions), STEP 5 (Artifacts), and STEP 6 (Statistics) and store results.

Additionally, collect project metadata:
```bash
# Project name (from git or directory)
basename "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Current date
date +"%Y-%m-%d %H:%M"

# Total time span of audit data
sqlite3 .planning/pwdev-audit.db "SELECT MIN(timestamp) || ' to ' || MAX(timestamp) FROM events;"

# Git branch
git branch --show-current 2>/dev/null
```

### STEP 7.3 — Generate Markdown Report

Write the full report to `.planning/audit-report.md`:

```markdown
# Audit Trail Report

**Project:** {project_name}
**Branch:** {branch}
**Generated:** {current_date}
**Period:** {first_event_date} to {last_event_date}
**Language:** {lang}

---

## 1. Executive Summary

- **Total events:** {count}
- **Total decisions:** {count}
- **Active artifacts:** {count}
- **Configuration changes:** {count}
- **Success rate:** {pct}% ({completed} completed / {failed} failed)

### Events by Action
| Action | Count |
|--------|-------|
{rows}

---

## 2. Activity Timeline (last 14 days)

| Day | Events |
|-----|--------|
{rows}

---

## 3. Event Log (last 50)

| # | Timestamp | Plugin | Command | Agent | Phase | Action | Target |
|---|-----------|--------|---------|-------|-------|--------|--------|
{rows}

---

## 4. Decisions

| # | Timestamp | Phase | Decision | Rationale | Alternatives | Reversible |
|---|-----------|-------|----------|-----------|--------------|------------|
{rows}

---

## 5. Artifacts

### By Type
| Type | Count |
|------|-------|
{rows}

### All Artifacts
| Path | Type | Phase | Status | Created |
|------|------|-------|--------|---------|
{rows}

---

## 6. Statistics

### Command Frequency
| Command | Runs |
|---------|------|
{rows}

### Performance
| Command | Runs | Avg (s) | Min (s) | Max (s) |
|---------|------|---------|---------|---------|
{rows}

### Events by Phase
| Phase | Count |
|-------|-------|
{rows}

### Events by Plugin
| Plugin | Count |
|--------|-------|
{rows}

---

## 7. Failed Commands

| Timestamp | Plugin | Command | Agent | Detail |
|-----------|--------|---------|-------|--------|
{rows}

---

## 8. Configuration Change History

| Timestamp | Field | Old Value | New Value | Changed By |
|-----------|-------|-----------|-----------|------------|
{rows}

---

*Report generated by /pwdev-prd:audit export*
```

### STEP 7.4 — Convert to PDF

Based on the available tool detected in STEP 7.1:

**Option 1 — pandoc:**
```bash
pandoc .planning/audit-report.md \
  -o .planning/audit-report.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=2cm \
  -V fontsize=10pt \
  -V mainfont="Inter" \
  --highlight-style=tango \
  2>/dev/null || \
pandoc .planning/audit-report.md \
  -o .planning/audit-report.pdf \
  -V geometry:margin=2cm \
  -V fontsize=10pt \
  2>/dev/null
```

If `pdflatex` is not available, try with `wkhtmltopdf` engine:
```bash
pandoc .planning/audit-report.md \
  -o .planning/audit-report.pdf \
  --pdf-engine=wkhtmltopdf \
  2>/dev/null
```

**Option 2 — weasyprint:**
```bash
python3 -c "
import markdown, weasyprint

with open('.planning/audit-report.md', 'r') as f:
    md_content = f.read()

html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

styled_html = '''<!DOCTYPE html>
<html><head><meta charset=\"utf-8\">
<style>
  body { font-family: Inter, system-ui, sans-serif; font-size: 10pt; margin: 2cm; color: #1a1a1a; line-height: 1.5; }
  h1 { font-size: 20pt; border-bottom: 2px solid #333; padding-bottom: 8px; }
  h2 { font-size: 14pt; color: #333; margin-top: 24px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }
  h3 { font-size: 11pt; color: #555; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 9pt; }
  th { background: #f4f4f5; font-weight: 600; text-align: left; padding: 6px 10px; border: 1px solid #ddd; }
  td { padding: 5px 10px; border: 1px solid #eee; }
  tr:nth-child(even) { background: #fafafa; }
  code { background: #f4f4f5; padding: 1px 4px; border-radius: 3px; font-size: 9pt; }
  hr { border: none; border-top: 1px solid #eee; margin: 20px 0; }
  strong { color: #111; }
</style>
</head><body>''' + html + '</body></html>'

weasyprint.HTML(string=styled_html).write_pdf('.planning/audit-report.pdf')
"
```

**Option 3 — wkhtmltopdf:**
```bash
python3 -c "
import markdown

with open('.planning/audit-report.md', 'r') as f:
    md_content = f.read()

html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

styled_html = '''<!DOCTYPE html>
<html><head><meta charset=\"utf-8\">
<style>
  body { font-family: Inter, system-ui, sans-serif; font-size: 10pt; margin: 0; color: #1a1a1a; line-height: 1.5; }
  h1 { font-size: 20pt; border-bottom: 2px solid #333; padding-bottom: 8px; }
  h2 { font-size: 14pt; color: #333; margin-top: 24px; border-bottom: 1px solid #ddd; padding-bottom: 4px; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 9pt; }
  th { background: #f4f4f5; font-weight: 600; text-align: left; padding: 6px 10px; border: 1px solid #ddd; }
  td { padding: 5px 10px; border: 1px solid #eee; }
  tr:nth-child(even) { background: #fafafa; }
</style>
</head><body>''' + html + '</body></html>'

with open('.planning/audit-report.html', 'w') as f:
    f.write(styled_html)
" && wkhtmltopdf --quiet --margin-top 20mm --margin-bottom 20mm --margin-left 20mm --margin-right 20mm .planning/audit-report.html .planning/audit-report.pdf && rm -f .planning/audit-report.html
```

**Fallback — Markdown only:**
Skip PDF generation. The `.planning/audit-report.md` file is still available.

### STEP 7.5 — Confirm Output

Check if PDF was generated:
```bash
[ -f ".planning/audit-report.pdf" ] && echo "PDF_OK" || echo "PDF_FAIL"
```

If PDF_OK:
- PT-BR: `Relatorio de auditoria gerado com sucesso:`
- EN: `Audit report generated successfully:`

```markdown
  - PDF: .planning/audit-report.pdf
  - Markdown: .planning/audit-report.md
```

If PDF_FAIL (but Markdown exists):
- PT-BR: `Falha ao gerar PDF. Relatorio disponivel em Markdown: .planning/audit-report.md`
- EN: `PDF generation failed. Report available as Markdown: .planning/audit-report.md`

Ensure both files are in `.gitignore`:
```bash
if ! grep -q "audit-report" .gitignore 2>/dev/null; then
  printf '\n# Audit reports (not versioned)\n.planning/audit-report.md\n.planning/audit-report.pdf\n' >> .gitignore
fi
```

---

## STEP 8 — Custom Query

Extract the SQL from `the arguments` after `query `.

**Safety rules (ALL must pass — otherwise reject as a read-only violation):**
1. Trim whitespace; strip at most ONE trailing `;`.
2. The remaining SQL must start with `SELECT` (case-insensitive).
3. Reject if it still CONTAINS `;` anywhere (multi-statement injection,
   e.g. `SELECT 1; DELETE FROM events`).
4. Reject if it contains `ATTACH` or `PRAGMA` (case-insensitive).

Rejection message:
- PT-BR: `Apenas consultas SELECT (statement unico) sao permitidas. O banco de auditoria e somente leitura.`
- EN: `Only single-statement SELECT queries are allowed. The audit database is read-only.`

Execute:
```bash
sqlite3 -header -column .planning/pwdev-audit.db "<USER_SQL>"
```

Present the raw result in a formatted table. If the query fails, show the SQLite error message.

### Quick Reference (show with results)

```markdown
### Tables: events, decisions, artifacts, config_changes

**events columns:** id, timestamp, session_id, plugin, command, agent, model, phase, action, target, detail, duration_ms
**decisions columns:** id, event_id, timestamp, phase, decision, rationale, alternatives, reversible
**artifacts columns:** id, event_id, path, type, phase, status, created_at, archived_at
**config_changes columns:** id, timestamp, field, old_value, new_value, changed_by
```

(Queries are not self-logged — the plugin's Stop hook already records the turn.)

Language: resolve `lang` per `references/language.md` before any human-facing output. Paths `<plugin-root>/...`, `references/`, `scripts/`, `templates/` are relative to the plugin root; tool names, subagent dispatch and the command form to show the user depend on the runtime (`references/runtime.md`).
