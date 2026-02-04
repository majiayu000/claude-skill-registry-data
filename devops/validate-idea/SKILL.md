---
name: validate-idea
description: Evaluate a single idea and decide to accept or reject it. Used internally by /validate-ideas or when the user mentions a specific idea number.
---

# Validate Idea

Evaluate a pending idea and decide whether to accept or reject it.

## Instructions

When validating idea #N:

### Step 1 - Fetch the Idea

```bash
gh issue view N --repo jmlweb/tooling --json number,title,body,labels
```

Verify it has the `idea:pending` label. If not, inform user.

### Step 2 - Analyze the Idea

Evaluate against project context:

1. Read relevant files:
   - `README.md`, `AGENTS.md` for project goals
   - Existing packages and their purpose

2. Check for duplicates:
   - Search existing issues for similar concepts
   - Check if functionality already exists in codebase

3. Assess feasibility:
   - Technical complexity
   - Dependencies required
   - Integration with existing architecture

### Step 3 - Estimate Effort and Impact

**Effort levels:**

| Level  | Time     | Scope                            |
| ------ | -------- | -------------------------------- |
| Low    | <2 hours | Single file, minimal testing     |
| Medium | 2-8 hrs  | Multiple files, moderate testing |
| High   | >8 hours | Significant changes, extensive   |

**Impact levels:**

| Level  | Description                              |
| ------ | ---------------------------------------- |
| Low    | Nice to have, minimal user benefit       |
| Medium | Noticeable improvement, moderate benefit |
| High   | Game changer, significant benefit        |

### Step 4 - Apply Decision

**If ACCEPTED:**

```bash
gh issue edit N --repo jmlweb/tooling \
  --remove-label "idea:pending" \
  --add-label "idea:accepted,effort:medium,impact:high"

gh issue comment N --repo jmlweb/tooling --body "## Validation: ACCEPTED

**Effort:** [level] | **Impact:** [level]

**Reasoning:** [Why accepted]

*Ready for /feed-backlog*"
```

**If REJECTED:**

```bash
gh issue edit N --repo jmlweb/tooling \
  --remove-label "idea:pending" \
  --add-label "idea:rejected"

gh issue comment N --repo jmlweb/tooling --body "## Validation: REJECTED

**Reason:** [Why rejected]"

gh issue close N --repo jmlweb/tooling
```

## Decision Guidelines

**Accept when:** High impact + low effort, aligns with goals, solves pain point

**Reject when:** Low ROI, out of scope, duplicates, infeasible
