---
description: Run the auditor agent against recent work or a specific file/task
argument-hint: "[scope]"
allowed-tools:
  - Read
  - Agent
  - Write
  - Edit
---

Delegate a quality review to the auditor agent.

## Steps

### Step 1: Determine scope

If the user provided a specific scope (file, task, or area):
- Use that as the audit target

If no scope provided:
- Default to "today's work" — read the daily note for context

### Step 2: Select audit tier

| Tier | When | Depth |
|------|------|-------|
| T1 | Daily wrap-up, quick check | Scan for obvious issues, 2-3 min |
| T2 | After completing a feature or multi-step task | Check completeness, consistency, side effects |
| T3 | Weekly review, after major changes | Full regression check, knowledge-base sweep |
| T4 | Monthly or after system changes | Deep infrastructure audit, cross-file coherence |

Default to T2 for explicit `/audit` calls.

### Step 3: Delegate to auditor

Spawn the auditor agent with the appropriate tier and scope:

```
Agent(auditor): [Tier] audit of [scope].

Context:
- [Brief description of what was done]
- [Key files involved]

Check for:
1. Completeness — were all requirements met?
2. Consistency — do changes align with existing patterns?
3. Side effects — did changes break anything downstream?
4. Knowledge — are there learnings to promote or nominate?

Report findings as PASS/WARN/FAIL with specific file:line references.
```

### Step 4: Process results

- **PASS**: Log success, note any suggestions
- **WARN**: Log warnings, add to daily note
- **FAIL**: Log failures, add to incident log, create corrective tasks on Task Board

### Step 5: Update logs

Append audit results to daily note under a new section:
```markdown
## Audit — HH:MM (T[tier])
- Result: [PASS/WARN/FAIL]
- Findings: [bullets]
- Actions: [any corrective tasks created]
```
