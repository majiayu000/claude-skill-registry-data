---
name: Validating Review Feedback
description: Validate code review feedback against implementation plan to prevent scope creep and derailment
when_to_use: when orchestrating plan execution with code review checkpoints, after receiving review feedback, before dispatching fixes to agents
related_skills: conducting-code-review
related_practices: code-review.md
version: 1.0.0
---

# Validating Review Feedback

## Overview

When orchestrating plan execution, code review feedback must align with the plan's goals. This workflow validates BLOCKING feedback against the plan, gets user decisions on misalignments, and annotates the review file to guide fixing agents.

**Core principle:** User decides scope changes, not the agent. Validate → Ask → Annotate.

**Announce at start:** "I'm using the validating-review-feedback skill to validate this review against the plan."

## The Workflow

### Phase 1: Parse Review Feedback

**Step 1: Read review file**
- Path provided by orchestrator
- Expected format: BLOCKING and NON-BLOCKING sections

**Step 2: Extract items**
- Parse all BLOCKING items into list
- Parse all NON-BLOCKING items (for awareness only)
- Preserve original wording and line numbers

### Phase 2: Validate Against Plan

**Step 1: Read plan file**
- Path provided by orchestrator
- Understand original scope and goals

**Step 2: Categorize each BLOCKING item**

For each BLOCKING item, determine:

- **In-scope**: Required by plan OR directly supports plan goals OR fixes bugs introduced while implementing plan
- **Out-of-scope**: Would require work beyond current plan (new features, refactoring unrelated code, performance optimizations not in plan)
- **Unclear**: Needs user judgment (edge cases, architectural decisions, ambiguous recommendations)

**Step 3: Document reasoning**

For each categorization, note brief reasoning:
- In-scope: "Task 3 requires auth validation"
- Out-of-scope: "SRP refactoring not in plan scope"
- Unclear: "Review recommends documentation alternative - needs user decision"

**Note on NON-BLOCKING items:** All NON-BLOCKING items are automatically marked [DEFERRED] without user consultation (see Phase 4 Step 3), as they are by definition not required for merge. User can choose to address them in a follow-up or ignore them entirely.

### Phase 3: Present Misalignments to User

**When:** Any BLOCKING items categorized as out-of-scope or unclear

**Step 1: Show misaligned items**

For each misaligned item:
```
BLOCKING Item: [exact text from review]
Categorization: [Out-of-scope / Unclear]
Reasoning: [why it doesn't clearly align with plan]
```

**Step 2: Ask user about each item**

Use AskUserQuestion for each misaligned BLOCKING item:

```
Question: "Should we address this BLOCKING issue in the current scope?"
Options:
  - "[FIX] Yes, fix now" (Add to current scope)
  - "[WONTFIX] No, reject feedback" (User disagrees with review)
  - "[DEFERRED] Defer to follow-up" (Valid but out of scope)
```

**Step 3: Check for plan revision**

If user selected [DEFERRED] for multiple items or items seem interconnected:
- Ask: "Do you want to revise the plan to accommodate these deferred items?"
- If yes: Set `plan_revision_needed` flag

### Phase 4: Annotate Review File

**Step 1: Add tags to BLOCKING items**

For each BLOCKING item in original review file:
- Prepend `[FIX]` if in-scope or user approved
- Prepend `[WONTFIX]` if user rejected
- Prepend `[DEFERRED]` if user deferred

**Step 2: Add clarifying notes**

For each tagged item, add Gatekeeper note explaining categorization:
- `(Gatekeeper: In-scope - {reasoning})`
- `(Gatekeeper: Out-of-scope - {reasoning})`
- `(Gatekeeper: User approved - {decision})`

**Step 3: Tag all NON-BLOCKING items**

- Prepend `[DEFERRED]` to all NON-BLOCKING items
- Add note: "(Gatekeeper: NON-BLOCKING items deferred by default)"

**Step 4: Write annotated review**

Save back to same review file path with annotations.

Example annotated review:

```markdown
# Code Review - 2025-10-19

## Summary
Found 3 BLOCKING issues and 2 NON-BLOCKING suggestions.

## BLOCKING (Must Fix Before Merge)

### [FIX] Security vulnerability in auth endpoint
Missing input validation on user-provided email parameter allows potential injection attacks.
(Gatekeeper: In-scope - required by Task 2 auth implementation)

### [DEFERRED] SRP violation in data processing module
The processUserData function handles both validation and database writes.
(Gatekeeper: Out-of-scope - refactoring not in current plan)

### [FIX] Missing tests for preference storage
No test coverage for the new user preference persistence logic.
(Gatekeeper: In-scope - Task 3 requires test coverage)

## NON-BLOCKING (Can Be Deferred)

(Gatekeeper: All NON-BLOCKING items deferred by default)

### [DEFERRED] Ambiguous variable name in utils
The variable 'data' in formatUserData could be more descriptive like 'userData'.

### [DEFERRED] Consider extracting magic number
The timeout value 5000 appears in multiple places.
```

### Phase 5: Update Plan with Deferred Items

**When:** Any items marked [DEFERRED]

**Step 1: Check if plan has Deferred section**

- Read plan file
- Look for `## Deferred Items` section

**Step 2: Create or append to Deferred section**

Add to end of plan file:

```markdown
---

## Deferred Items

Items deferred during code review - must be reviewed before merge.

### From Batch N Review ({review-filename})
- **[DEFERRED]** {Item description}
  - Source: Task X
  - Severity: BLOCKING or NON-BLOCKING
  - Reason: {why deferred}
```

**Step 3: Save updated plan**

Write plan file with deferred items section.

### Phase 6: Return Summary

Provide summary to orchestrator:

```
Validation complete:
- {N} BLOCKING items marked [FIX] (ready for fixing agent)
- {N} BLOCKING items marked [DEFERRED] (added to plan)
- {N} BLOCKING items marked [WONTFIX] (rejected by user)
- {N} NON-BLOCKING items marked [DEFERRED]
- Plan revision needed: {yes/no}

Annotated review saved to: {review-file-path}
Plan updated with deferred items: {plan-file-path}
```

## Key Principles

| Principle | Application |
|-----------|-------------|
| **User decides scope** | Never auto-approve out-of-scope items, always ask |
| **Annotate in place** | Modify review file with tags, don't create new files |
| **Track deferrals** | All deferred items must go in plan's Deferred section |
| **Clear communication** | Tags ([FIX]/[WONTFIX]/[DEFERRED]) guide fixing agent |
| **No silent filtering** | User must explicitly decide on every misalignment |

## Error Handling

**Missing required inputs (plan or review path):**
- Error immediately with clear message: "Cannot validate without both plan file path and review file path"
- Do not attempt to proceed with partial inputs

**No BLOCKING items found:**
- Still tag all NON-BLOCKING as [DEFERRED]
- Return summary indicating clean review

**User marks all BLOCKING as [WONTFIX]:**
- Annotate review accordingly
- Return to orchestrator with plan_revision_needed suggestion
- Orchestrator should pause and ask user about plan validity

**Plan file not found:**
- Error immediately
- Cannot validate without plan context

**Review file not parseable:**
- Error immediately
- Show user the review file format issue

## Integration

**Called by:**
- Gatekeeper agent (enforces this workflow)
- /execute command (via Gatekeeper dispatch)

**Requires:**
- Plan file path (from orchestrator)
- Review file path (from code-review-agent agent)

**Produces:**
- Annotated review file (with [FIX]/[WONTFIX]/[DEFERRED] tags)
- Updated plan file (with Deferred Items section)
- Summary for orchestrator

## Test Scenarios

See `test-scenarios.md` for baseline and with-skill tests proving this workflow prevents scope creep and misinterpretation.
