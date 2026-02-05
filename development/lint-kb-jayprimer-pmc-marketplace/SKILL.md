---
name: lint-kb
description: |
  Validate and enforce KB documentation formats, completeness, and integrity.
  Checks recent docs (uncommitted or last N commits) against KB standards.

  CHECKS PERFORMED:
  1. FORMAT - Documents follow required templates (headers, sections)
  2. COMPLETENESS - Tickets/issues have all required files (1-5)
  3. INTEGRITY - All tickets in index.md, phases in roadmap.md
  4. PATTERNS - Have Status: open|resolved
  5. NAMING - Files follow conventions (verb-noun, feat-, comp-, etc.)

  Use when:
  - Before committing KB docs
  - After creating tickets/issues
  - Periodic maintenance
  - User says "lint kb", "check docs", "validate kb"
---

# Lint KB Documentation

Validate and enforce KB documentation formats, completeness, and integrity.

## Prerequisites

**ALWAYS run /pmc:kb first** to understand KB structure and formats.

## Check Modes

| Mode | Scope | Command |
|------|-------|---------|
| **Recent** | Uncommitted + last 3 commits | `/lint-kb` (default) |
| **Full** | All KB docs | `/lint-kb full` |
| **Tickets** | Only tickets/issues | `/lint-kb tickets` |

---

## Step 1: Identify Docs to Check

use /pmc:kb first. 

### Recent Mode (Default)

```bash
# Uncommitted changes
git status --porcelain .pmc/docs/

# Recently committed (last 3)
git log -3 --name-only --pretty=format: -- .pmc/docs/ | sort -u
```

### Full Mode

```
Glob: .pmc/docs/**/*.md
```

---

## Step 2: Ticket/Issue Completeness

### Required Files

Each ticket/issue directory MUST have these files:

| File | Required | Purpose |
|------|----------|---------|
| `1-definition.md` | Always | What: scope, success criteria |
| `2-plan.md` | Always | How: steps, decisions |
| `3-spec.md` | Always* | TDD: tests, edge cases |
| `4-progress.md` | In progress | Log: TDD cycles, notes |
| `5-final.md` | On completion | Done: status, learnings |

*`3-spec.md` may be minimal for trivial tickets (TDD: no in constraints).

### Check Procedure

```
Glob: .pmc/docs/tickets/T*/
```

For each directory:
1. List files present
2. Report missing required files
3. Check `5-final.md` has `Status: COMPLETE` or `Status: BLOCKED`

### Report Format

```
## Ticket Completeness

| Ticket | 1-def | 2-plan | 3-spec | 4-prog | 5-final | Status |
|--------|-------|--------|--------|--------|---------|--------|
| T00021 | OK    | OK     | OK     | OK     | OK      | COMPLETE |
| T00022 | OK    | OK     | MISSING| -      | -       | In Progress |
```

---

## Step 3: Index Integrity

### Tickets Index

```
Read: .pmc/docs/tickets/index.md
Glob: .pmc/docs/tickets/T*/
```

Check:
1. Every `T*/` directory has entry in index.md
2. No orphan entries (listed but directory missing)
3. Format: `T0000N Brief Title` (one per line)

### Roadmap Integrity

```
Read: .pmc/docs/3-plan/roadmap.md
```

Check:
1. **ALL active tickets appear in roadmap** (single or in phase)
2. Phase ticket references exist as directories
3. No stale references to archived tickets

**Critical:** Every ticket in `tickets/` (not archived) MUST be in roadmap.md - whether as a single item or within a phase.

### Report Format

```
## Index Integrity

### tickets/index.md
- Missing entries: T00023, T00024
- Orphan entries: none

### 3-plan/roadmap.md
- Stale reference: T00015 (archived)
- Missing from roadmap: T00021
```

---

## Step 4: Format Validation

**All format requirements are in [kb/references/](../kb/references/):**

| Document Type | Reference | Key Requirements |
|---------------|-----------|------------------|
| PRDs | [prd-format.md](../kb/references/prd-format.md) | Header, Overview/Scope, prefix (feat-/comp-/infra-) |
| SOPs | [sop-format.md](../kb/references/sop-format.md) | Header, Steps, verb-noun filename |
| Patterns | [pattern-format.md](../kb/references/pattern-format.md) | Status field (open/resolved), Problem section |
| Code Maps | [codemap-format.md](../kb/references/codemap-format.md) | Header, Last updated, Key Files |
| Tickets | [ticket-formats.md](../kb/references/ticket-formats.md) | All 5 docs with required sections |

Read the relevant reference file to understand what to validate.

### Report Format

```
## Format Validation

| File | Issue |
|------|-------|
| 4-patterns/caching.md | Missing Status field |
| 2-sop/deploy.md | Filename should be verb-noun |
| tickets/T00022/1-definition.md | Missing Scope section |
```

---

## Step 5: Fix or Report

### Auto-fixable Issues

Some issues can be auto-fixed:
- Add missing `Status: open` to patterns
- Add ticket to index.md
- Create stub files for missing ticket docs

### Manual Review Required

- Format violations in existing content
- Stale roadmap references
- Incorrect naming conventions

### How It Works

This is a **Claude-interpreted skill** (no CLI script). When invoked:

1. Claude reads this SKILL.md for validation rules
2. Claude performs checks using Glob/Grep/Read tools
3. Claude reports issues and can fix them on request

**Usage:**
```
/lint-kb              # Claude performs validation, reports issues
/lint-kb fix patterns # Claude fixes specific category
```

---

## Quick Checks

### One-liner Integrity Check

```bash
# Tickets not in index
comm -23 <(ls -1 .pmc/docs/tickets/ | grep '^T' | sort) \
         <(grep -oE 'T[0-9]+' .pmc/docs/tickets/index.md | sort)

# Patterns without Status
grep -L -i 'Status:' .pmc/docs/4-patterns/*.md
```

---

## Checklist

### Completeness
- [ ] All tickets have 1-definition.md
- [ ] All tickets have 2-plan.md
- [ ] All tickets have 3-spec.md (or TDD: no)
- [ ] Completed tickets have 5-final.md

### Integrity
- [ ] All tickets in index.md
- [ ] ALL active tickets in roadmap.md (single or in phase)
- [ ] No stale references to archived items

### Format
- [ ] PRDs have required sections
- [ ] SOPs follow verb-noun naming
- [ ] Patterns have Status field
- [ ] Code maps have Last updated
- [ ] Ticket definitions have Scope

---

## Example Run

```
$ /lint-kb

Checking KB documentation...

## Scope
- Mode: recent (uncommitted + last 3 commits)
- Files to check: 8

## Ticket Completeness

| Ticket | Files | Status |
|--------|-------|--------|
| T00021 | 5/5   | COMPLETE |
| T00022 | 2/5   | Missing: 3-spec, 4-progress, 5-final |

## Index Integrity

tickets/index.md:
- Missing: T00022

3-plan/roadmap.md:
- OK

## Format Validation

4-patterns/new-pattern.md:
- Missing: Status field (add "Status: open" or "Status: resolved")

## Summary
- Errors: 2
- Warnings: 1
- Auto-fixable: 1 (run with --fix)
```
