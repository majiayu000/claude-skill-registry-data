---
name: plan-document-lifecycle
description: Lifecycle management of plan documents from creation to automatic cleanup after merge. Use when creating, referencing, or cleaning up plans.
---

# Plan Document Lifecycle

## Instructions

### Lifecycle stages

**Creation** → **Active** → **Cleanup**

### Creation (Step 1)
- File: `.plan/{{feature_name}}_plan.md`
- Purpose: Implementation direction, progress tracking

### Active (Steps 2-9)
- All phases reference plan
- Remains unchanged (initial direction)
- Guides implementation

### Cleanup (After merge)
- Trigger: Merge to main complete
- Timing: Immediately, first of 4-step cleanup
- Command: `rm .plan/{{feature_name}}_plan.md`
- Scope: Only merged feature's plan

### Selective cleanup

**Delete:** Merged feature's plan only
**Preserve:** Concurrent work plans
**Protection:** Never delete other plans

## Example

```bash
# Before merge
ls .plan/
# feature-a_plan.md
# feature-b_plan.md

# Merge feature-a complete
rm .plan/feature-a_plan.md

# After
ls .plan/
# feature-b_plan.md  ← Preserved
```

## Workflow

```
Create plan
    ↓
Phases reference plan
    ↓
Merge complete
    ↓
Delete plan (cleanup Step 1)
```

## Plan Document Structure

<!-- CUSTOMIZE: Adjust based on project needs -->

**Recommended sections:**

```markdown
# {{Feature Name}} Implementation Plan

## Overview
- Purpose: {{Why this feature}}
- Scope: {{What's included/excluded}}
- Dependencies: {{Required features/systems}}

## Phases

### Phase 1: {{Phase Name}} ({{Estimated Time}})
**Deliverable:** {{What gets built}}
**Test Criteria:** {{How to verify}}
**Success Criteria:**
- [ ] {{Criterion 1}}
- [ ] {{Criterion 2}}

### Phase 2-N: ...
(Repeat structure)

## Risk Assessment
- **{{Risk Type}}**: {{Description}} → Mitigation: {{Strategy}}

## Architecture Changes
- {{Component}}: {{Change description}}

## Security Considerations
- {{Concern}}: {{How addressed}}

## Testing Strategy
- Unit tests: {{Coverage}}
- Integration tests: {{Scenarios}}
- Performance tests: {{Criteria}}

## Rollback Plan
- {{How to undo changes if needed}}
```

## Multi-Team Coordination

**Scenario:** Multiple teams/features in parallel

```bash
# Team A working on feature-x
.plan/feature-x_plan.md

# Team B working on feature-y
.plan/feature-y_plan.md

# Team C working on bug-fix-z
.plan/bug-fix-z_plan.md

# Team A merges feature-x
rm .plan/feature-x_plan.md  ← Only delete this one

# Teams B and C continue working
ls .plan/
# feature-y_plan.md
# bug-fix-z_plan.md
```

## Plan Updates Policy

**Immutability Principle:** Plans should remain largely unchanged after Step 2.5 approval.

**When updates are allowed:**
- **Discovered risks:** Append to Risk Assessment section
- **Scope clarification:** Add notes, but don't change approved phases
- **Dependencies found:** Document in Dependencies section

**Format for updates:**
```markdown
## Updates Log

### {{Date}} - {{Reason}}
- {{What changed}}
- {{Why it changed}}
- User approval: {{Yes/No}}
```

**When NOT to update:**
- Don't change approved Phase structure
- Don't remove success criteria
- Don't delete risk assessments

**Instead:** Document deviations and get user approval if significant

---

**For detailed lifecycle, see [reference.md](reference.md)**
**For more examples, see [examples.md](examples.md)**
