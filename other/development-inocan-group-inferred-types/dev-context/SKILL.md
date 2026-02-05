---
name: dev-context
description: Context architecture skill for aligning work. Use when starting new features, making architectural decisions, or setting up implementation work. Generates interconnected ADR/Design/Spec/Plan scaffolding that agents can navigate and humans can enrich.
---

# Dev Context (Lean)

Set up working context for GitHub issues. Create formal ADRs when needed.

## Two Modes

### Mode 1: Issue Working Space (Default)

**Trigger**: "Set up context for issue #115", "Create working space for feature X"

**Creates**:
```
docs/issues/{num}-{short-name}/
├── README.md   # Status, GH link, quick reference
├── plan.md     # Implementation approach
└── notes.md    # Working notes (starts empty)
```

**Process**:
1. Create folder `docs/issues/{num}-{short-name}/`
2. Generate README.md with issue link and status
3. Generate plan.md with implementation approach
4. Create empty notes.md for working notes
5. Return file paths

**README.md template**:
```markdown
# Issue #{num}: {Title}

**GitHub**: {link}
**Status**: In Progress
**Created**: {date}

## Overview
{Brief description from issue}

## Related
- Plan: [plan.md](./plan.md)
- Notes: [notes.md](./notes.md)
```

**plan.md template**:
```markdown
# Implementation Plan: {Title}

## Approach
{High-level approach}

## Tasks
- [ ] {Task 1}
- [ ] {Task 2}
- [ ] {Task 3}

## Files to Modify
- {file 1}
- {file 2}

## Notes
{Implementation notes as work progresses}
```

---

### Mode 2: Architecture Decision Record (ADR)

**Trigger**: "Create ADR for choosing X over Y", "Document the decision about Z"

**Creates**:
```
docs/adr/{NNN}-{decision-name}.md
```

**Process**:
1. Find next ADR number (glob `docs/adr/*.md`, or start at 001)
2. Create `docs/adr/` directory if needed
3. Generate ADR from template in `references/templates/adr.md`
4. Return file path

**When to use ADRs**:
- Major architectural decisions (database choice, framework selection)
- Decisions that will be questioned later ("why did we do it this way?")
- Decisions with significant tradeoffs worth documenting
- NOT for routine implementation choices

**Note**: Most decisions don't need formal ADRs. They get captured in devlogs and synthesized into `docs/moc/decisions.md` during periodic maintenance. Use ADRs sparingly for decisions that truly warrant formal documentation.

---

## What This Skill Does NOT Do

This lean version intentionally omits:

| Old Feature | Why Removed | Alternative |
|-------------|-------------|-------------|
| PRD generation | GitHub issue IS the PRD | Write clear issues |
| Design docs per feature | Only major systems need design docs | `docs/design/` for systems |
| Spec docs | Plan IS the spec | Use plan.md |
| Cross-reference ceremony | Overkill for most work | Keep it simple |

---

## Quick Reference

| Request | Mode | Output |
|---------|------|--------|
| "Set up context for issue #115" | Issue | `docs/issues/115-*/` |
| "Create working space for auth" | Issue | `docs/issues/{num}-auth/` |
| "Create ADR for X vs Y decision" | ADR | `docs/adr/NNN-*.md` |
| "Document decision about caching" | ADR | `docs/adr/NNN-*.md` |

---

## Lifecycle

### Issue Working Space
1. **Create** when starting multi-session work
2. **Update** plan.md and notes.md as you work
3. **Extract** patterns to `ai_docs/` if reusable
4. **Delete** folder when issue closes

### ADRs
1. **Create** for major decisions
2. **Never edit** once accepted (write new ADR if decision changes)
3. **Reference** from `docs/moc/decisions.md` for discoverability

---

## Part of the dev-* Family

| Skill | Purpose |
|-------|---------|
| `dev-context` | Set up working space, create ADRs |
| `dev-explore` | Generate/update MOC documentation |
| `dev-reports` | Write devlogs and status reports |
| `dev-inquiry` | Technical investigation and spikes |

---

## See Also

- `docs/issues/README.md` - Working space conventions
- `ai_docs/maintenance-workflows.md` - When to extract patterns
- `docs/moc/decisions.md` - Synthesized decision history
