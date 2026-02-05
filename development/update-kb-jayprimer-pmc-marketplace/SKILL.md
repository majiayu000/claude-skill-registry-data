---
name: update-kb
description: |
  Synchronize knowledge base documentation with current codebase implementation.
  Performs full, incremental, or targeted audits of source code and updates
  code maps, PRDs, patterns, SOPs, and user-facing docs to match reality.

  Use when:
  - After major refactors
  - Periodic maintenance (monthly)
  - Before starting new phase of work
  - When docs feel stale
  - User says "update kb", "sync docs", "audit docs"
---

# Update KB Docs from Codebase

Synchronize knowledge base documentation with current codebase implementation.

## Prerequisites

**ALWAYS run /pmc:kb first** to understand KB structure and document formats.

## Audit Types

| Type | Scope | When to Use |
|------|-------|-------------|
| **Full** | Read all source files, create/update all code maps | First time, major version, annual |
| **Incremental** | Compare git diff since last anchor, update affected docs | After feature work, monthly |
| **Targeted** | Focus on specific area (e.g., just CLI or just dashboard) | After focused changes |

## Full Audit Procedure

### Step 0: Record Anchor Point

```bash
git rev-parse HEAD
git log -1 --format="%H %s (%ai)"
```

Create audit notes file: `.pmc/docs/6-references/audit-{date}.md`

```markdown
# Code Audit Notes - {date}

**Anchor Commit:** `{hash}` - "{message}" ({date})
**Status:** In Progress

## Files Read
(track as you go)

## Features Discovered
(update incrementally)
```

**Decision:** Always record anchor for future incremental audits.

### Step 1: Inventory All Source Files

```
Glob: src/**/*.py  (or appropriate pattern for your codebase)
```

Group by area (example for Python):
- Core (engine, models, parser, context, config)
- Executors/Handlers
- Storage/Database
- API/CLI
- UI/Dashboard

### Step 2: Read ALL Files (Full Audit)

**Critical:** For full audit, read every file. Do not sample or infer.

Read in parallel where possible. Update audit notes incrementally:

```markdown
### {Area} ({n}/{total} read)

| File | Lines | Features Identified |
|------|-------|---------------------|
| file.py | 123 | Feature1, Feature2 |
```

**Decision:** Reading is non-negotiable for full audit. Sampling leads to gaps.

### Step 3: Compile Feature List

After reading all files, create comprehensive feature list organized by functional area.

### Step 4: Determine Code Maps Needed

```
Glob: .pmc/docs/5-code-maps/*.md
```

For each feature area, decide:
- **Update** existing code map if it exists but is outdated
- **Create** new code map if area is undocumented
- **Skip** if trivial or internal-only

**Decision:** Feature-based approach (not file-based) ensures user-relevant documentation.

### Step 5: Create/Update Code Maps

For each code map:
1. Read existing (if updating)
2. Write comprehensive documentation
3. Include: files, line numbers, key functions, data flow
4. Mark audit date in file

**Format:** See [kb/references/codemap-format.md](../kb/references/codemap-format.md)

### Step 6: Update Audit Notes

Mark audit as complete:
- Change status to "Complete"
- Add recommendations section
- Note any issues found

---

## Phase 2: PRD & Pattern Consistency

After code maps are current, verify other docs match reality.

### Step 1: Audit PRDs

```
Glob: .pmc/docs/1-prd/*.md
```

For each PRD:
1. Read the PRD
2. Compare features listed vs code maps
3. Mark as: current, outdated, or deprecated
4. **Update PRD if features are implemented** - don't just note discrepancies

### Step 2: Audit Patterns

```
Glob: .pmc/docs/4-patterns/*.md
```

For each pattern:
1. Check `Status: open` patterns - still valid?
2. Check `Status: resolved` patterns - solution still applies?
3. Ensure all patterns have explicit `Status: open | resolved`
4. Look for new patterns from code (workarounds, edge cases)

---

## Phase 3: User-Facing Docs

### Step 1: Update 8-users/

Source: CLI help, README, code map features

- `personas.md` - Who uses this?
- `use-cases.md` - Common scenarios
- `faq.md` - Questions answered in sessions

### Step 2: Review SOPs

```
Glob: .pmc/docs/2-sop/*.md
```

For each SOP:
1. Verify commands still exist (check against code maps)
2. Update paths/options if changed
3. Update historical status if resolved (e.g., "tracked for Phase X" → "Fixed in Phase Y")
4. Add new SOPs for undocumented workflows

---

## Incremental Audit Procedure

### Step 1: Find Changes Since Last Anchor

```bash
git log --oneline {last-anchor}..HEAD
git diff --name-only {last-anchor}..HEAD -- src/
```

### Step 2: Read Changed Files Only

Focus on files that changed. Update affected code maps.

### Step 3: Record New Anchor

Update audit notes with new anchor commit.

---

## Key Learnings

1. **Commit anchor is mandatory** - enables incremental audits
2. **Audit notes go in `6-references/`** - permanent record
3. **Full audit = read ALL files** - no sampling
4. **Feature-based code map organization** - not file-based
5. **Update docs immediately** - don't just note discrepancies
6. **Check Glob paths carefully** - they can fail silently
7. **PRDs should match implemented features** - not aspirational ones
8. **All patterns need explicit Status** - open or resolved
9. **Verify command references** - against code maps
10. **Update historical status** - when issues are resolved

## Checklist

- [ ] Record anchor commit
- [ ] Create audit notes file
- [ ] Read all source files (full) or changed files (incremental)
- [ ] Update/create code maps
- [ ] Audit PRDs against code maps
- [ ] Audit patterns (ensure Status field)
- [ ] Update user docs (8-users/)
- [ ] Review SOPs for outdated commands
- [ ] Mark audit complete
- [ ] Commit changes
