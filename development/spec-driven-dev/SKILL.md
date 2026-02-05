---
name: spec-driven-dev
description: |
  Spec-Driven Development (SDD) agent for maintaining synchronized specifications, code, and documentation.
  Core principle: "1 Todo = 1 Commit = 1 Spec Update".

  Use this skill when:
  - Starting a new feature or task that needs specification
  - Implementing code based on existing specifications
  - Validating that code matches specifications
  - Updating CHANGELOG.md with changes
  - Managing PRD/specification documents
  - Ensuring traceability between requirements and implementation

  Triggers: "spec", "specification", "PRD", "requirements", "SDD", "spec-driven"
---

# Spec-Driven Development (SDD)

## Core Principle

**1 Todo = 1 Commit = 1 Spec Update**

Every task must:
1. Have a corresponding specification entry
2. Result in a focused commit
3. Update relevant documentation

## Workflow

### Phase 1: Specification

Before writing code, create or update the specification:

```
docs/
  PRD.md           # Product Requirements Document
  specs/
    feature-x.md   # Feature-specific specifications
  CHANGELOG.md     # All changes tracked here
```

### Phase 2: Implementation

1. Read the relevant spec from `docs/specs/`
2. Create focused todo items (1 todo = 1 atomic change)
3. Implement following the spec exactly
4. Validate implementation matches spec

### Phase 3: Documentation Sync

After each implementation:
1. Update CHANGELOG.md with the change
2. Update spec if implementation revealed necessary changes
3. Commit with message referencing the spec

## File Structure

### PRD.md Template

```markdown
# Product Requirements Document

## Overview
[Brief description]

## Goals
- Goal 1
- Goal 2

## Features
### Feature A
- **Status**: [Planned | In Progress | Done]
- **Spec**: [Link to detailed spec]
- **Priority**: [High | Medium | Low]

## Non-Goals
[What this project will NOT do]
```

### Feature Spec Template

See [references/spec-template.md](references/spec-template.md) for the full template.

### CHANGELOG.md Format

```markdown
# Changelog

## [Unreleased]

### Added
- Feature description (spec: feature-x.md)

### Changed
- Change description

### Fixed
- Fix description
```

## Commands

### Create New Spec
When user says "create spec for X":
1. Generate spec from template
2. Save to `docs/specs/X.md`
3. Add entry to PRD.md
4. Create initial CHANGELOG entry

### Implement from Spec
When user says "implement X" or "build X":
1. Read `docs/specs/X.md`
2. Break into atomic todos
3. For each todo:
   - Implement the change
   - Validate against spec
   - Update CHANGELOG.md
   - Commit with spec reference

### Validate Spec
When user says "validate spec" or "check spec compliance":
1. Read current spec
2. Analyze implemented code
3. Report discrepancies
4. Suggest spec or code updates

## Validation Script

Use [scripts/validate_spec.py](scripts/validate_spec.py) to check:
- All features in PRD have specs
- All specs have implementation status
- CHANGELOG entries exist for completed features
- Code files reference their specs

## Best Practices

1. **Atomic Changes**: Each todo should be completable in one commit
2. **Spec First**: Always update spec before major implementation changes
3. **Traceability**: Every commit message should reference the relevant spec
4. **Living Documentation**: Specs evolve with the code, not after

## Context Preservation

To prevent information loss during Auto-Compact:
- All decisions documented in specs
- Rationale included in CHANGELOG
- Git history provides complete audit trail
