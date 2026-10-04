---
name: fleet-trail-verification
description: How fleet-ops verifies audit trails during review — what to check, what constitutes a complete trail, and how to distinguish real work from paperwork
user-invocable: false
---

# Trail Verification

## Why This Matters

The trail is how the fleet proves work was done properly. Without trail
verification, reviews become rubber stamps. A task with "code looks fine"
is not reviewed — it's waved through.

The trail tells you: who did what, when, in what order, with what inputs.
If the trail is incomplete, the review cannot be thorough.

## What a Complete Trail Looks Like

### Required Events (all task types)
1. **Task created** — who created it, with what fields
2. **Task accepted** — agent accepted with a plan
3. **Progress updates** — readiness changes with explanations
4. **Commits** — conventional format, linked to task
5. **Task completed** — summary of what was done

### Required Events (stories and above)
6. **Contributions received** — design_input, qa_test_definition, security_requirement
7. **Contributions consumed** — evidence that inputs were used (referenced in plan, commits)
8. **Readiness gates** — 50% checkpoint, 90% gate request

### Required Events (review tasks)
9. **Review started** — reviewer acknowledged the task
10. **Review criteria checked** — each criterion evaluated
11. **Decision recorded** — approved/rejected with specific reasoning

## How to Verify

### Step 1: Reconstruct
Use the trail-reconstructor sub-agent:
```
Launch trail-reconstructor with task_id
```
This returns a chronological event list without bloating your context.

### Step 2: Check Completeness
Against the checklist above. Mark each event as:
- PRESENT — event exists in trail
- MISSING — event should exist but doesn't
- SUSPICIOUS — event exists but timing or content is unusual

### Step 3: Check Authenticity
- **Timing:** Are events in logical order? (Can't have commits before acceptance)
- **Content:** Do commit messages match the plan? Do progress updates describe real work?
- **Contributions:** Did the agent actually reference contributions in their work?
  (Check commit diffs — does the code follow architect's design input?)
- **Stage compliance:** Did the task move through stages in order?
  (conversation → analysis → investigation → reasoning → work)

### Step 4: Assess Quality
A complete trail with garbage content is still a bad trail:

| Quality Signal | Good | Bad |
|---------------|------|-----|
| Plan | References verbatim, maps to contributions | "Will implement the feature" |
| Progress | Specific: "auth middleware done, JWT signing with RS256" | "Making progress" |
| Commits | Conventional format, meaningful messages | "WIP", "fix", "update" |
| Completion | Explains what, why, how to verify | "Done" |

## Trail Gaps That Block Approval

These gaps mean you CANNOT approve:
1. No plan accepted — agent skipped planning
2. No contributions — agent worked without required inputs
3. No tests — engineer skipped verification
4. No commit trail — no evidence of incremental work
5. Stage jumps — task went from conversation to work (skipped analysis/investigation)

## Trail Gaps That Warn But Don't Block

These gaps warrant a note but not rejection:
1. Missing 50% checkpoint — informational, not structural
2. Sparse progress updates — preference, not requirement
3. Contribution tasks exist but trail event not recorded — check if
   contribution actually exists in task context

## The Distinction: Real Work vs Paperwork

A trail exists to prove real work happened. If you find yourself checking
boxes without examining content, you're doing paperwork, not verification.

Real verification: "The plan references architect's design for repository
pattern. The commits show a RepositoryBase class. The test files test
the repository. The security contribution said 'validate inputs at
boundary' — the commit adds input validation at the API layer."

Paperwork: "Plan exists. Commits exist. Tests exist. Approved."

## Group Call

```
ops_real_review(task_id, trail_data, criteria)
```
The review group call includes trail verification as step 3 of the
10-step review protocol.
