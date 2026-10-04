---
name: coding-task-templates
description: Structured task templates for agent coding work. Use when creating, assigning, or executing coding tasks that need clear structure, deliverables, and verification steps. Covers implementation, error analysis, fixes, and refactoring workflows with timeouts, checkpoints, and rollback plans.
---

# Coding Task Templates

Structured templates for consistent task execution across agents.

## ⚠️ Agenten-Limitierungen (kritisch seit 2026-04-26)

**Kontextfenster überlastet bei >2 Dateien oder >500 Code-Zeilen.**

Agenten (Softeware, Sir Stern) produzieren leere/abgebrochene Ergebnisse bei zu großen Tasks.

### Regeln:
1. **Max. 2 Dateien pro Task** — bei mehr: Splitte in Sub-Tasks
2. **Max. 500 Code-Zeilen pro Task** — bei mehr: Phase aufteilen
3. **Keine Phase mit >3 Fixes** — bei mehr: Neue Phase starten
4. **Timeout an Task-Größe anpassen:**
   - Micro-Fix (1 Datei, <50 Zeilen): 5 Min
   - Klein (1-2 Dateien, <200 Zeilen): 10 Min
   - Mittel (2 Dateien, <500 Zeilen): 20 Min
   - Groß (>2 Dateien oder >500 Zeilen): AUFSPLITTEN

### Warum das wichtig ist:
- Agenten lesen Dateien → Kontextfenster füllt sich
- Bei Überlastung: Output wird leer oder Timeout
- Besser: 10 kleine Tasks die funktionieren als 1 großer der scheitert

---

## Quick Select

Choose template based on task type:

| Task Type | Template File | Use When |
|-----------|---------------|----------|
| Implementation | [TEMPLATE_IMPLEMENTATION.md](references/TEMPLATE_IMPLEMENTATION.md) | Building new features |
| Error Analysis | [TEMPLATE_ERROR_ANALYSIS.md](references/TEMPLATE_ERROR_ANALYSIS.md) | Debugging, understanding failures |
| Fix After Analysis | [TEMPLATE_FIX.md](references/TEMPLATE_FIX.md) | Applying known fixes |
| Refactor | [TEMPLATE_REFACTOR.md](references/TEMPLATE_REFACTOR.md) | Restructuring code |
| Cody Multi-Phase | [TEMPLATE_CODY.md](references/TEMPLATE_CODY.md) | Complex multi-phase tasks |

## Common Rules (All Templates)

### Timeouts
- Max 5 minutes per phase/sub-task
- Save checkpoint, report status, continue

### Checkpoints
- Save intermediate state after each deliverable
- Never keep everything in memory until the end

### Decision Gates
- If unclear: pause and ask, don't guess
- Document assumptions if decision required

### Rollback
- Always have a way back
- Test rollback before destructive changes

### Verification
- Syntax check: `python3 -m py_compile <file>`
- Import test: `python3 -c "from module import Class"`
- Run tests if available

## Usage

1. Read appropriate template based on task type
2. Fill in `{PLACEHOLDERS}` with concrete values
3. Execute task following template structure
4. Create status file as specified
5. Report completion with summary
