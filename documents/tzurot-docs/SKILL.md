---
name: tzurot-docs
description: Documentation maintenance for Tzurot v3 - Updating CURRENT_WORK.md, folder structure, and keeping docs current. Use at session end or when documentation needs updating.
lastUpdated: '2026-01-04'
---

# Tzurot v3 Documentation Maintenance

**Use this skill when:** Ending a session, completing a milestone, creating new documentation, or updating existing docs.

## Quick Reference

```markdown
# CURRENT_WORK.md format

> Last updated: YYYY-MM-DD

## Status: [Brief description of current focus]

**Current Phase**: [What you're actively working on]

**Recent Completion**: [Major milestone just finished]

## Active Work

[Details of current task]

## Planned Features (Priority Order)

[Upcoming work]
```

## Core Documentation Files

| File              | Purpose            | Update When                  |
| ----------------- | ------------------ | ---------------------------- |
| `CURRENT_WORK.md` | Active work status | Start/end session, milestone |
| `CLAUDE.md`       | Project guidelines | New patterns, conventions    |
| `ROADMAP.md`      | Planning roadmap   | Sprint changes               |
| GitHub Releases   | Version history    | Each release                 |

**Root files only:** README.md, CLAUDE.md, CURRENT_WORK.md, ROADMAP.md. Everything else → `docs/`

## Documentation Structure (Time-State Architecture)

```
docs/
├── reference/           # THE TRUTH - What currently exists
│   ├── architecture/    # Design decisions, system architecture
│   ├── deployment/      # Railway, infrastructure setup
│   ├── operations/      # Runbooks, backup procedures
│   ├── standards/       # Coding patterns, folder structure
│   ├── guides/          # Developer how-tos
│   ├── features/        # Feature documentation
│   ├── testing/         # Test procedures
│   ├── database/        # Schema documentation
│   └── templates/       # Reusable document templates
├── proposals/           # THE PLANS - What we want to build
│   ├── active/          # On roadmap, being worked on
│   └── backlog/         # Ideas not yet scheduled
├── incidents/           # Postmortems and lessons learned
└── migration/           # Active migration guides
```

## Decision Rules

| Question             | Answer                             |
| -------------------- | ---------------------------------- |
| Is it implemented?   | → `reference/`                     |
| Is it a plan/idea?   | → `proposals/` (active or backlog) |
| Is it done/obsolete? | → Extract learnings, then DELETE   |
| Is it an incident?   | → `incidents/`                     |

## Proposal Lifecycle

1. **New idea** → `proposals/backlog/`
2. **Scheduled for work** → Move to `proposals/active/`
3. **Implementation complete**:
   - Extract learnings to `reference/` docs or skills
   - Update incident docs if issues found
   - DELETE the proposal (git preserves history)

## Session Handoff Protocol

**At session end:**

1. Update CURRENT_WORK.md with progress
2. Delete obsolete docs (git history preserves them)
3. Update doc timestamps if modified

```bash
# Get current date
date +%Y-%m-%d

# Commit WIP if needed
git commit -m "wip: feature-name - progress description"
```

## Best Practices

### ✅ Do

- Use descriptive names: `memory-and-context-redesign.md`
- Update existing docs instead of creating new ones
- Use YYYY-MM-DD date format
- Link between related docs with relative paths
- Delete obsolete docs (git preserves history)
- Use frontmatter for dates, not filenames

### ❌ Don't

- Create documentation bloat (one topic = one doc)
- Let CURRENT_WORK.md get stale
- Create README files in every directory
- Document obvious things
- Keep archive folders (delete instead)
- Put dates in filenames

## Documentation Categories

| Type                   | Location                       | Purpose                   |
| ---------------------- | ------------------------------ | ------------------------- |
| Architecture decisions | `docs/reference/architecture/` | Why we built it this way  |
| Deployment guides      | `docs/reference/deployment/`   | Railway setup, operations |
| Development guides     | `docs/reference/guides/`       | How to do X               |
| Coding standards       | `docs/reference/standards/`    | Patterns to follow        |
| Active proposals       | `docs/proposals/active/`       | Currently being worked    |
| Future ideas           | `docs/proposals/backlog/`      | Not yet scheduled         |
| Post-mortems           | `docs/incidents/`              | Incident analysis         |

## GitHub Releases Format

```markdown
## What's Changed

### Added

- New feature X for doing Y

### Changed

- Improved performance of A by 50%

### Fixed

- Bug where X would fail under Y conditions

**Full Changelog**: https://github.com/lbds137/tzurot/compare/vX.X.X...vY.Y.Y
```

**Note:** This project uses GitHub Releases, NOT CHANGELOG.md.

## Anti-Patterns

| ❌ Don't                     | ✅ Do                            |
| ---------------------------- | -------------------------------- |
| Multiple docs for same topic | One comprehensive guide          |
| Stale CURRENT_WORK.md        | Update at session end            |
| README in every directory    | One main README                  |
| Document obvious things      | Document non-obvious             |
| Archive obsolete docs        | Delete (extract learnings first) |
| Date-stamped filenames       | Frontmatter dates                |

## Context Preservation

**For AI sessions, always check these at session start:**

1. CURRENT_WORK.md - What's happening now?
2. CLAUDE.md - What are the rules?
3. docs/README.md - What docs exist?

## Related Skills

- **tzurot-git-workflow** - Commit documentation updates
- **tzurot-council-mcp** - When to consult for doc structure
- **tzurot-architecture** - Document architectural decisions

## References

- Documentation structure: `docs/README.md`
- Current project status: `CURRENT_WORK.md`
- Project guidelines: `CLAUDE.md`
- Tech debt tracking: `docs/proposals/active/TECH_DEBT.md`
