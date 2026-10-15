---
name: ux-audit
description: Audit UX patterns for quality — navigation, flows, feedback, consistency, cognitive load, context
version: 1.0.0
execution-mode: advisory
argument-hint: <path> (defaults to $PROJECT_ROOT/dashboard/web/)
category: fleet-ops
status: candidate
---
# UX Audit

Score UX patterns against the vibe-coded → engineered spectrum.
Complements `[ui-audit]` (visual/technical) with behavioral/experiential analysis.

## Usage

```bash
[ux-audit]                          # Audit the dashboard
[ux-audit] $PROJECT_ROOT/dashboard/web/components/  # Specific directory
```

## Execution

### 1. Resolve target path
Default: `$PROJECT_ROOT/dashboard/web/`
If `$ARGUMENTS` provided, use that path.

### 2. Run the audit engine

```bash
python3 -c "
from your_project.modules.domain.ux_arbiter import run_audit
result = run_audit('TARGET_PATH')
print(result.summary)
print()
for f in result.findings:
    icon = 'PASS' if f.score == 2 else ('WARN' if f.score == 1 else 'FAIL')
    print(f'  [{icon}] {f.criterion}: {f.message}')
    if f.evidence:
        print(f'         Evidence: {f.evidence}')
print()
print(f'Files scanned: {result.files_scanned}')
"
```

### 3. Format output

```
UX Audit | <target> | Grade <X> (<score>/<max>)
═══════════════════════════════════════════════

## Score Breakdown
| Category        | Score | Max | Status |
|-----------------|-------|-----|--------|
| Navigation      | X     | 8   | ✓/⚠/✗  |
| Flow            | X     | 10  | ✓/⚠/✗  |
| Feedback        | X     | 8   | ✓/⚠/✗  |
| Consistency     | X     | 6   | ✓/⚠/✗  |
| Cognitive Load  | X     | 6   | ✓/⚠/✗  |
| Context         | X     | 8   | ✓/⚠/✗  |

## Failures / Warnings / Passing
(same format as [ui-audit])

## Paired Scores (if both audits run)
| Arbiter | Grade | Score |
|---------|-------|-------|
| UI      | X     | X/60  |
| UX      | X     | X/46  |
| Combined| X     | X/106 |
```

## Categories Explained

- **Navigation**: Can users find things? Breadcrumbs, sidebar, search, routing depth.
- **Flow**: Can users DO things? Progressive disclosure, drill-down, pagination, confirmations.
- **Feedback**: Does the system TELL users what happened? Toasts, progress, optimistic updates, undo.
- **Consistency**: Is it the SAME everywhere? Naming, component reuse, data fetching patterns.
- **Cognitive Load**: Is it SIMPLE? Component size, conditional complexity, information grouping.
- **Context**: Does it EXPLAIN itself? Tooltips, help text, labels, onboarding.
