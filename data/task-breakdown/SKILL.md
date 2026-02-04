---
name: task-breakdown
description: Use when converting architecture plans into implementation phases. Creates independent, bite-sized phase files that can be executed separately.
---

# Task Breakdown Skill

## Overview

Transform architecture plans into **independent implementation phases**. Each phase is a separate file that can be executed without waiting for other phases.

**Core principle:** Independent phases first, dependent phases last.

## When to Use

- After architecture plan is approved
- Converting design to executable phases
- Planning incremental implementation
- Enabling parallel work streams

## Phase-Based Output Structure

```
plans/sessions/{session}/plans/
├── implementation.md              # Master index (lightweight)
├── phases/
│   ├── phase-01-foundation.md     # Independent - implement first
│   ├── phase-02-core-models.md    # Independent - implement first
│   ├── phase-03-api-routes.md     # Independent - implement first
│   ├── phase-04-ui-components.md  # Depends on models
│   └── phase-05-integration.md    # Depends on all above
```

## The Iron Law: Independence Ordering

```
INDEPENDENT PHASES → TOP (implement first)
DEPENDENT PHASES → BOTTOM (implement last)
```

**Why?** Independent phases can be:
- Implemented in parallel by multiple agents
- Verified without waiting for other phases
- Rolled back without breaking other phases

## Quick Reference: Phase Types

| Type | Description | Position |
|------|-------------|----------|
| **Foundation** | Config, utils, types | Top (first) |
| **Core** | Models, services | Top |
| **Feature** | Specific functionality | Middle |
| **Integration** | Connecting components | Bottom |
| **Polish** | Tests, docs, cleanup | Bottom (last) |

## Implementation.md Format

The master file is **lightweight** - just an index:

```markdown
# Implementation Plan: [Feature]

**Session:** {session-id}
**Status:** Proposed | In Progress | Completed

## Phase Summary

| Phase | Name | Status | Dependencies |
|-------|------|--------|--------------|
| 1 | Foundation | Pending | None |
| 2 | Core Models | Pending | None |
| 3 | API Routes | Pending | None |
| 4 | UI Components | Pending | Phase 2 |
| 5 | Integration | Pending | Phase 1-4 |

## Execution Order

**Can implement in parallel:**
- Phase 1, 2, 3 (no dependencies)

**Must wait:**
- Phase 4 → after Phase 2
- Phase 5 → after all phases

## Phase Files

- [Phase 1: Foundation](phases/phase-01-foundation.md)
- [Phase 2: Core Models](phases/phase-02-core-models.md)
- [Phase 3: API Routes](phases/phase-03-api-routes.md)
- [Phase 4: UI Components](phases/phase-04-ui-components.md)
- [Phase 5: Integration](phases/phase-05-integration.md)
```

## Individual Phase File Format

Each phase file is **self-contained**:

```markdown
# Phase [N]: [Phase Name]

**Dependencies:** None | Phase [X], [Y]
**Can Start:** Immediately | After Phase [X]
**Estimated Tasks:** [N]

## Objective

[One sentence: what this phase accomplishes independently]

## Entry Criteria

- [ ] [What must be true before starting]

## Tasks

### Task [N.1]: [Task Name]
**Size:** XS | S | M | L
**File:** `path/to/file.ts`

[Task details using task-template.md format]

---

### Task [N.2]: [Task Name]
...

## Exit Criteria

- [ ] All tasks complete
- [ ] Verification passes
- [ ] No impact on other phases

## Verification

```bash
# Phase-specific verification
[commands]
```
```

## Dependency Sorting Algorithm

**Step 1:** List all components from architecture
**Step 2:** For each component, identify what it imports/uses
**Step 3:** Score by dependency count:
- 0 dependencies = Phase 1 (top)
- 1-2 dependencies = Phase 2-3 (middle)
- 3+ dependencies = Last phases (bottom)

**Step 4:** Within same dependency count, order by:
1. Config/Types first (foundational)
2. Services/Models second
3. Controllers/UI third
4. Integration/E2E last

## Task Criteria (Unchanged)

Tasks within phases must be:

| Criterion | Description |
|-----------|-------------|
| **Single-concern** | One logical change |
| **Verifiable** | Clear success criteria |
| **Bounded** | Defined start/end |
| **Sized** | XS, S, M, L (no XL) |

**Rule:** XL tasks must be split further.

## File Operations

| Action | Format |
|--------|--------|
| CREATE | `path/to/new/file` + pattern to follow |
| MODIFY | `path/to/file` + line range + before/after |
| DELETE | `path/to/file` + reason + dependency check |
| MOVE | `from` → `to` + import updates |

## Verification Per Task

| Type | Command | Use Case |
|------|---------|----------|
| Type Check | `npm run typecheck` | TypeScript |
| Lint | `npm run lint` | Style |
| Unit Test | `npm test -- [pattern]` | Logic |
| Build | `npm run build` | Compilation |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| One massive implementation.md | Split into phase files |
| Dependent phases at top | Reorder: independent first |
| Phase depends on multiple others | Move to bottom |
| XL tasks | Break into S/M tasks |
| Vague verification | Specific commands |

## Output Checklist

Before presenting plan:
- [ ] Implementation.md is index-only (< 50 lines)
- [ ] Each phase has separate file
- [ ] Independent phases listed first
- [ ] Dependent phases at bottom
- [ ] Each phase is self-contained
- [ ] Tasks are appropriately sized
- [ ] Verification commands provided
