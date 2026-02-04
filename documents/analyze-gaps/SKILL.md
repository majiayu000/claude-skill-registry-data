---
name: analyze-gaps
description: Analyze gaps between codebase and PRD documentation, generate discrepancies report. Use this skill when you need to sync documentation with implementation, find undocumented features, or identify unbuilt requirements.
---

# Analyze Gaps

Compares codebase implementation against PRD documents to identify discrepancies and generate a structured report.

## When to Use

- Before updating PRD docs to reflect implementation
- Before creating new tickets for unbuilt features
- When codebase and documentation may be out of sync
- As first step in sync-prd or sync-planning workflows

## Workflow

### Step 1: Fresh Start

Remove existing discrepancies report to start fresh:

```bash
rm -f docs/1-prd/99-discrepancies.md
```

Initialize new report with header:

```markdown
# Discrepancies Report (In Progress)

Generated: {date}
Focus: {area or 'all'}
Status: ANALYZING

## Notes
(Working notes captured during analysis)
```

### Step 2: Analyze Codebase

Explore the project structure to understand current implementation:

1. Explore project structure (src/, lib/, etc.)
2. Identify main features and modules implemented
3. Note APIs, data models, integrations present
4. Document patterns and conventions used

**Update 99-discrepancies.md** with findings as you go:
- Add discovered modules/features under Notes
- Track code paths and entry points
- Note patterns that may not be in PRD

If a focus area is specified, concentrate analysis on that area.

### Step 3: Analyze PRD

Read all PRD documents under `docs/1-prd/` (excluding 99-discrepancies.md):

1. List all documented features and requirements
2. Note expected behaviors and specifications
3. Identify assumptions or constraints mentioned

**Update 99-discrepancies.md** iteratively:
- Cross-reference PRD items against codebase notes
- Mark items as you compare them
- Add preliminary gap observations

### Step 4: Find Gaps

Compare codebase with PRD to identify discrepancies:

| Gap Type | Description | Action Needed |
|----------|-------------|---------------|
| `IMPLEMENTED_NOT_DOCUMENTED` | Feature exists in code but not in PRD | Update PRD |
| `DOCUMENTED_NOT_IMPLEMENTED` | PRD describes feature not yet built | Create ticket |
| `DIVERGED` | Implementation differs from PRD spec | Align (either direction) |
| `OUTDATED` | PRD describes old/changed behavior | Update PRD |

**Update 99-discrepancies.md** as gaps are found:
- Categorize each gap by type
- Add code location and PRD file references
- Note specific discrepancy details
- Record recommended action

### Step 5: Finalize Report

Transform working notes in `99-discrepancies.md` into final structured report.

Update status from `ANALYZING` to `COMPLETE` and reorganize content:

```markdown
# Discrepancies Report

Generated: {date}
Focus: {area or 'all'}
Status: COMPLETE

## Summary
- Total gaps: N
- IMPLEMENTED_NOT_DOCUMENTED: N
- DOCUMENTED_NOT_IMPLEMENTED: N
- DIVERGED: N
- OUTDATED: N

## IMPLEMENTED_NOT_DOCUMENTED
(Features in code but not in PRD - need PRD update)

### Feature Name
- **Code location:** path/to/code
- **Details:** description
- **Recommended action:** Add to PRD

## DOCUMENTED_NOT_IMPLEMENTED
(PRD features not yet built - need tickets)

### Feature Name
- **PRD file:** docs/1-prd/feature.md
- **Details:** description
- **Recommended action:** Create ticket T0000N

## DIVERGED
(Implementation differs from spec - need alignment)

### Feature Name
- **Code location:** path/to/code
- **PRD file:** docs/1-prd/feature.md
- **Details:** how they differ
- **Recommended action:** Update PRD or implementation

## OUTDATED
(PRD describes old behavior - need PRD update)

### Feature Name
- **PRD file:** docs/1-prd/feature.md
- **Details:** what changed
- **Recommended action:** Update PRD
```

## Output

After running this skill:
- Previous `docs/1-prd/99-discrepancies.md` is removed (fresh start)
- New report is built iteratively during analysis
- Final report has `Status: COMPLETE` when done
- Report is ready for consumption by:
  - `sync-prd` skill (handles IMPLEMENTED_NOT_DOCUMENTED, DIVERGED, OUTDATED)
  - `sync-planning` skill (handles DOCUMENTED_NOT_IMPLEMENTED)

## Intermediate States

The report transitions through states:
1. `Status: ANALYZING` - Working notes being captured
2. `Status: COMPLETE` - Final structured report ready

## Example Usage

```
User: Analyze gaps in the authentication module
Assistant: [Uses analyze-gaps skill with focus_area="auth"]
```

```
User: Find discrepancies between code and PRD
Assistant: [Uses analyze-gaps skill]
```
