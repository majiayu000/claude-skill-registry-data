---
name: drift-check
category: cadence
description: >
  Compares stated priorities against where time and effort actually went, and produces
  a strategy drift report. Uses git log, vault priorities, and project docs to detect
  misalignment. Use when the user says "drift check", "am I on track", "priority alignment",
  "where did my time go", "strategy drift", or wants to audit focus vs intention.
---

# Drift Check

Detect when effort drifts from stated priorities.

## Workflow

1. **Identify stated priorities** — Find the user's declared priorities from:
   - Most recent `weekly-plan.md` or `weekly-review-*.md` in the vault
   - Any `PRIORITIES.md`, `GOALS.md`, or pinned notes
   - Sprint/milestone definitions
   - If none found, ask the user to state their top 3-5 priorities

2. **Measure actual effort** — Analyze where time actually went:
   - `git log --since="[period]" --stat` across all repos under `~/broomva/`
   - Count commits, lines changed, and files touched per project
   - Check vault note creation/modification dates and volumes
   - Look at conversation logs if available

3. **Map effort to priorities** — For each stated priority:
   - **Aligned effort**: commits/notes that directly serve this priority
   - **Tangential effort**: related but not directly advancing the goal
   - **Unrelated effort**: work that doesn't map to any stated priority

4. **Calculate drift score** — Per priority:
   - `alignment_ratio = aligned_effort / total_effort`
   - Flag priorities with < 20% of total effort as **neglected**
   - Flag work areas with > 20% effort but no matching priority as **drift**

5. **Produce drift report**

## Output Format

```markdown
## Drift Check — [Period: start → end]

### Stated Priorities
1. [Priority] — alignment: [HIGH/MEDIUM/LOW] ([X]% of effort)
2. [Priority] — alignment: [HIGH/MEDIUM/LOW] ([X]% of effort)
3. [Priority] — alignment: [HIGH/MEDIUM/LOW] ([X]% of effort)

### Effort Distribution
| Area | Commits | Files | Lines | % of Total | Maps to Priority |
|------|---------|-------|-------|-----------|-----------------|
| [repo/project] | N | N | N | X% | Priority #N / DRIFT |

### Drift Alerts
- **Neglected**: [Priority] — only [X]% effort, expected more
- **Drift**: [Area] consumed [X]% effort but isn't a stated priority
- **Overinvested**: [Priority] — [X]% effort vs [Y]% importance

### Recommendations
1. [Concrete suggestion to realign]
2. [Concrete suggestion to realign]
```

## Configuration

- **Default period**: last 7 days
- **Repos to scan**: all directories under `~/broomva/` with `.git`
- **Vault path**: `~/broomva-vault/`

## Behavior

- Be honest but not judgmental — drift happens, the goal is awareness
- Distinguish intentional pivots from unconscious drift
- If the user says "I intentionally shifted to X", acknowledge and update the drift calculation
- Suggest saving the report to `vault/reviews/drift-check-[YYYY-MM-DD].md`
