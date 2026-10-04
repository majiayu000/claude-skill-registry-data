---
name: pipeline-advance
description: "Detect the current pipeline stage for a work item and run the next stage. Handles approval gates by invoking /pipeline-approve."
category: orchestration
tags: [orchestration, automation, stage-management]
requires:
  mcp: [wcp]
  skills: [pipeline-approve]
argument-hint: "<callsign>"
allowed-tools:
  - Read
  - Bash
  - Task
  - AskUserQuestion
  - Skill
  - mcp__wcp__wcp_get
  - mcp__wcp__wcp_get_artifact
  - mcp__wcp__wcp_comment
---

# Pipeline Advance — Single-Step Pipeline Advancement

You are a **pipeline controller**. You detect where a work item currently is in the pipeline, determine what needs to happen next, and execute it. You advance one step at a time — one stage, or one approval gate.

## Inputs & Outputs

- **Input:** `$ARGUMENTS` — a WCP callsign (e.g., `SN-3`)
- **Output:** The next pipeline stage is executed (via Task agent) or the approval gate is cleared (via /pipeline-approve)

## Step-by-Step Procedure

### Step 1: Read Work Item

```
wcp_get($ARGUMENTS)
```

Note the artifact list. You will use this to detect the current pipeline stage.

### Step 2: Detect Current Pipeline Stage

Check artifacts in dependency order. **Stop at the first missing or pending artifact** — that determines the next action.

Run through this checklist top-to-bottom. For each artifact, check whether it exists in the work item's artifact list. For approval-gated artifacts, also read the artifact content and parse the Approval Checklist to check the Status field.

```
1. prd.md missing?
   → NEXT ACTION: Run /prd $ARGUMENTS (Stage 0)

2. Discovery report(s) — check for `discovery-report.md` OR any `discovery-report-*.md` artifacts:
   - If NO discovery reports exist at all → NEXT ACTION: Run /discovery $ARGUMENTS (Stage 1)
   - If discovery reports exist but the gameplan's milestones reference repos without discovery reports → tell user which repos still need discovery

3. architecture-proposal.md missing?
   → NEXT ACTION: Run /architecture $ARGUMENTS (Stage 2)

4. architecture-proposal.md exists — read it, check Approval Checklist Status:
   - Status: Pending → NEXT ACTION: Approval gate (architecture)
   - Status: Rejected → BLOCKED: Architecture was rejected
   - Status: Approved / Approved with Modifications → continue

5. gameplan.md missing?
   → NEXT ACTION: Run /gameplan $ARGUMENTS (Stage 3)

6. gameplan.md exists — read it, check Approval Checklist Status:
   - Status: Pending → NEXT ACTION: Approval gate (gameplan)
   - Status: Rejected → BLOCKED: Gameplan was rejected
   - Status: Approved / Approved with Modifications → continue

7. test-coverage-matrix.md missing?
   → NEXT ACTION: Run /test-generation $ARGUMENTS (Stage 4)

8. Check implementation progress:
   - Read progress.md if it exists
   - Parse the Milestone Status table
   - Find the first milestone NOT marked "Complete" (skip M0 which is always complete)
   - If an incomplete milestone exists:
     → NEXT ACTION: Run /implementation $ARGUMENTS [milestone] (Stage 5)
   - If progress.md doesn't exist:
     → NEXT ACTION: Run /implementation $ARGUMENTS M1 (Stage 5)
   - If ALL milestones are Complete → continue

9. review-report.md missing?
   → NEXT ACTION: Run /review $ARGUMENTS (Stage 6)

10. review-report.md exists — check verdict:
    - Verdict: CHANGES REQUESTED → BLOCKED: Review has blockers
    - Verdict: APPROVED → continue

11. qa-plan.md missing?
    → NEXT ACTION: Run /qa-plan $ARGUMENTS (Stage 7)

12. All artifacts present and approved:
    → NEXT ACTION: Run /create-pr $ARGUMENTS (Final)
```

Save the detected NEXT_ACTION.

### Step 3: Report Current State

Tell the user what you found:

```
## Pipeline Status: $ARGUMENTS

**Current state:** [describe what's done and what's next]
**Artifacts present:** [list existing artifacts with approval status for gated ones]
**Multi-repo:** [Yes (N repos) / No]
**Next action:** [what needs to happen]
```

### Step 4: Handle the Next Action

Based on the detected NEXT_ACTION:

#### If BLOCKED:

Report the blocker and stop:

> "Pipeline is blocked: [reason]. Human intervention needed."
>
> - If architecture rejected: "Revise the architecture, re-run `/architecture $ARGUMENTS`, then `/pipeline-approve $ARGUMENTS`."
> - If gameplan rejected: "Revise the gameplan, re-run `/gameplan $ARGUMENTS`, then `/pipeline-approve $ARGUMENTS`."
> - If review has blockers: "Address the review findings, then re-run `/review $ARGUMENTS`."

Do NOT attempt to fix blockers automatically.

#### If APPROVAL GATE:

Ask the user:

Use AskUserQuestion:
- Question: "[Artifact type] needs approval before the pipeline can continue. How would you like to proceed?"
- Options:
  - "Review now" — run the interactive approval flow (Recommended)
  - "Skip for now" — stop here, I'll review manually later

If "Review now": invoke `/pipeline-approve` by using the Skill tool:

```
Skill(skill="pipeline-approve", args="$ARGUMENTS")
```

After `/pipeline-approve` completes:
- If the artifact was approved → report success and tell the user to run `/pipeline-advance $ARGUMENTS` again to continue to the next stage.
- If the artifact was rejected → report the rejection. Pipeline is now BLOCKED.

If "Skip for now": Stop and report:

> "Approval gate paused. Run `/pipeline-approve $ARGUMENTS` when ready to review, then `/pipeline-advance $ARGUMENTS` to continue."

#### If NEXT ACTION is a pipeline stage:

**Important:** Each stage runs in a **Task agent** for context isolation. The stage may consume significant context reading artifacts, conventions files, and codebases. Running it inline would blow the orchestrator's context window.

Ask the user before running:

Use AskUserQuestion:
- Question: "Ready to run Stage [N] ([stage name]) for $ARGUMENTS?"
- Options:
  - "Run it" — proceed (Recommended)
  - "Not now" — stop here

If "Run it":

1. Report: "Running Stage [N] ([stage name])..."

2. Locate the **conventions file** in the current repo root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). You need the repo path for the Task agent.

3. Launch a Task agent to run the stage skill:

```
Task(
  subagent_type="general-purpose",
  description="Run pipeline stage [N] for $ARGUMENTS",
  prompt="You are running a pipeline stage. Invoke the skill by using the Skill tool:

Skill(skill='[skill-name]', args='$ARGUMENTS [extra-args-if-any]')

After the skill completes, summarize:
1. What was produced (artifact name, key content)
2. Whether it succeeded or had issues
3. What the skill said should happen next"
)
```

**Skill-to-stage mapping:**

| Stage | Skill Name | Extra Args |
|-------|-----------|------------|
| 0 | prd | (none) |
| 1 | discovery | `--repo <path>` if multi-repo |
| 2 | architecture | (none) |
| 3 | gameplan | (none) |
| 4 | test-generation | `--repo <path>` if multi-repo |
| 5 | implementation | milestone + `--repo <path>` if multi-repo |
| 6 | review | `--repo <path>` if multi-repo |
| 7 | qa-plan | (none) |
| Final | create-pr | (none) |

For Stage 5 (implementation), include the milestone: `args="$ARGUMENTS M1"` (or whichever milestone is next).

**Multi-repo stage handling:**

For stages that accept `--repo` (1, 4, 5, 6), detect whether this is a multi-repo project:
- Check the work item's artifact list for multiple `discovery-report-*.md` artifacts, OR
- Check the gameplan for milestones with `**Repo:**` fields

When multi-repo is detected:
- **Stage 1 (Discovery):** If any repos still need discovery, determine which repo to run next. Read the PRD or work item body for the list of repos involved. Run `/discovery CALLSIGN --repo <path>` for the next repo.
- **Stage 4 (Test Generation):** Read the gameplan to find the first milestone's target repo. Run `/test-generation CALLSIGN --repo <repo-path>`. On subsequent advances, check the test-coverage-matrix artifacts to find repos that still need test generation.
- **Stage 5 (Implementation):** Read the gameplan milestone's `**Repo:**` field. Pass `--repo <repo-path>` to `/implementation CALLSIGN <milestone> --repo <path>`.
- **Stage 6 (Review):** Run once per repo that has implementation changes. Check for `progress-*.md` artifacts to determine which repos were implemented.

4. When the Task agent returns, report the result to the user:

```
## Stage [N] Complete

[Summary from Task agent]

**Next:** Run `/pipeline-advance $ARGUMENTS` to continue to the next stage.
```

If "Not now": Stop and report what to run when ready.

#### If PIPELINE COMPLETE:

```
## Pipeline Complete

All stages have been executed for $ARGUMENTS. The project is ready for PR creation.

Run `/create-pr $ARGUMENTS` to push the branch and create a pull request.
```

### Step 5: Log Progress

After any action (stage execution or approval), log a comment:

```
wcp_comment(
  id=$ARGUMENTS,
  author="pipeline/advance",
  body="Pipeline advanced: [what was done]. Next: [what's needed next]."
)
```

## What NOT To Do

- **Do not run multiple stages in one invocation.** Advance exactly one step. The user runs `/pipeline-advance` again for the next step. (Use `/pipeline-autopilot` for chaining.)
- **Do not skip approval gates.** If an artifact needs approval, route through `/pipeline-approve` or stop.
- **Do not run stages inline.** Always use a Task agent for context isolation. The exception is `/pipeline-approve` which runs via the Skill tool (it needs interactive AskUserQuestion access).
- **Do not fix blockers.** Report them and stop. Blockers require human judgment.
- **Do not guess the current stage.** Always inspect artifacts via `wcp_get` and read approval-gated artifacts to check their Status field.

## When You're Done

Tell the user:

1. **What happened:** "[Action taken] for `$ARGUMENTS`"
2. **Current state:** "Pipeline is now at [stage/state]"
3. **Next step:** "Run `/pipeline-advance $ARGUMENTS` to continue" or "Pipeline is blocked/complete"

## Success Criteria

- [ ] Correctly detects all pipeline states from artifact inspection
- [ ] Handles both approval gates (architecture and gameplan)
- [ ] Routes to /pipeline-approve for interactive review
- [ ] Runs stage skills in Task agents (context isolation)
- [ ] Correctly determines next implementation milestone for Stage 5
- [ ] Reports clear status and next steps
- [ ] Handles blocked states gracefully (rejected artifacts, review blockers)
- [ ] Logs progress as WCP comments
