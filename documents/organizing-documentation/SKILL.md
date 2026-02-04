---
name: Organizing Documentation
description: Set up or reorganize project documentation using intent-based structure (BUILD/FIX/UNDERSTAND/LOOKUP)
when_to_use: when setting up new project docs, reorganizing chaotic documentation, improving doc discoverability, or onboarding reveals navigation problems
version: 1.0.0
---

# Organizing Documentation

## Overview

Transform documentation from content-type organization (architecture/, testing/, api/) to intent-based organization (BUILD/, FIX/, UNDERSTAND/, LOOKUP/).

**Announce at start:** "I'm using the organizing-documentation skill to structure these docs by developer intent."

## When to Use

- Setting up documentation for a new project
- Existing docs are hard to navigate
- New team members can't find what they need
- Same questions keep getting asked
- Docs exist but nobody reads them

## The Process

### Step 1: Audit Existing Documentation

List all docs and categorize by **actual developer intent**:

```markdown
| File | Current Location | Developer Intent | New Location |
|------|-----------------|------------------|--------------|
| architecture.md | docs/ | Understand system | UNDERSTAND/core-systems/ |
| testing-guide.md | docs/ | Build tests | BUILD/03-TEST/ |
| error-codes.md | docs/ | Quick lookup | LOOKUP/ |
| debugging-tips.md | docs/ | Fix problems | FIX/investigation/ |
```

**Key question:** "When would a developer reach for this doc?"

### Step 2: Create Directory Structure

```bash
mkdir -p docs/{BUILD/{00-START,01-DESIGN,02-IMPLEMENT,03-TEST,04-VERIFY},FIX/{symptoms,investigation,solutions},UNDERSTAND/{core-systems,evolution},LOOKUP}
```

### Step 3: Populate 00-START First

**Critical:** This is the entry point. Include:

1. **Prime directive** - Non-negotiable project rules
2. **Architecture overview** - High-level system map
3. **Coordinate systems/conventions** - Domain-specific foundations

Without 00-START, developers skip prerequisites.

### Step 4: Organize FIX by Symptoms

**Wrong:** Organize by root cause (memory-leaks/, type-errors/)
**Right:** Organize by what developer sees (visual-bugs/, test-failures/)

```
FIX/symptoms/
├── visual-bugs/
│   ├── rendering-wrong.md
│   └── layout-broken.md
├── test-failures/
│   └── passes-locally-fails-ci.md
└── performance/
    └── slow-startup.md
```

### Step 5: Create LOOKUP Quick References

**Rule:** < 30 seconds to find and use.

Good LOOKUP content:
- Keyboard shortcuts
- Command cheat sheets
- Error code tables
- ID registries
- One-page summaries

Bad LOOKUP content (move elsewhere):
- Tutorials (→ BUILD/02-IMPLEMENT)
- Explanations (→ UNDERSTAND)
- Debugging guides (→ FIX)

### Step 6: Build INDEX.md

Create master index with **purpose annotations**:

```markdown
## BUILD

| File | Title | Purpose |
|------|-------|---------|
| `00-START/prime-directive.md` | Prime Directive | Non-negotiable rules |
| `02-IMPLEMENT/patterns.md` | Code Patterns | How to implement features |
```

Purpose column is **mandatory** - it's the key to discoverability.

### Step 7: Add Redirects

Don't break existing links. Create README.md in old locations:

```markdown
# This content has moved

Documentation has been reorganized by developer intent.

- Architecture docs → `UNDERSTAND/core-systems/`
- Testing docs → `BUILD/03-TEST/`
- Quick references → `LOOKUP/`

See `docs/INDEX.md` for complete navigation.
```

## Checklist

- [ ] All docs audited and categorized by intent
- [ ] BUILD/00-START has prerequisites
- [ ] FIX organized by symptoms, not causes
- [ ] LOOKUP items are < 30 second lookups
- [ ] INDEX.md has purpose column
- [ ] Old locations have redirects
- [ ] Internal links verified

## Anti-Patterns

**Don't:**
- Create deep nesting (max 3 levels)
- Duplicate content across directories
- Put tutorials in LOOKUP
- Organize FIX by root cause
- Skip the INDEX.md

**Do:**
- Keep structure flat where possible
- Cross-reference between sections
- Update INDEX.md as docs change
- Test navigation with new team member

## Additional Patterns

### README-Per-Directory

Every directory needs README.md with consistent structure:
- Purpose statement
- "Use this when" section
- Navigation to contents
- Quick links to related sections

**Use template:** `${CLAUDE_PLUGIN_ROOT}templates/documentation-readme-template.md`

### Dual Navigation

Maintain parallel navigation:
- NAVIGATION.md - Task-based primary (80%)
- INDEX.md - Concept-based fallback (20%)

### Naming Conventions

- ALLCAPS for document types: SUMMARY.md, QUICK-REFERENCE.md
- Numeric prefixes for sequence: 00-START/, 01-DESIGN/
- Lowercase-dashes for content: api-patterns.md

### Progressive Disclosure

Provide multiple entry points by time budget:
- 5 min: TL;DR section
- 20 min: README + key sections
- 2 hours: Full documentation

### Role-Based Paths

Create reading paths for different roles with:
- Goal statement
- Reading order
- Time estimate
- Key takeaway

## Related Skills

For specific documentation tasks:

- **Research packages:** `${CLAUDE_PLUGIN_ROOT}skills/creating-research-packages/SKILL.md`
- **Debugging docs:** `${CLAUDE_PLUGIN_ROOT}skills/documenting-debugging-workflows/SKILL.md`
- **Quality gates:** `${CLAUDE_PLUGIN_ROOT}skills/creating-quality-gates/SKILL.md`

## References

- Standards: `${CLAUDE_PLUGIN_ROOT}standards/documentation-structure.md`
- README Template: `${CLAUDE_PLUGIN_ROOT}templates/documentation-readme-template.md`
- Research Package Template: `${CLAUDE_PLUGIN_ROOT}templates/research-package-template.md`
- Quick Reference Template: `${CLAUDE_PLUGIN_ROOT}templates/quick-reference-template.md`
- Symptom Debugging Template: `${CLAUDE_PLUGIN_ROOT}templates/symptom-debugging-template.md`
- Verification Checklist Template: `${CLAUDE_PLUGIN_ROOT}templates/verification-checklist-template.md`
