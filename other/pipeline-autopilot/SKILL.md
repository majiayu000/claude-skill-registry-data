---
name: pipeline-autopilot
description: "Run the full pipeline autonomously for a work item. Chains stages with context isolation, handles approval gates via interactive interview or auto-approve."
category: orchestration
tags: [orchestration, automation, autonomous]
requires:
  mcp: [wcp]
  skills: [pipeline-approve, pipeline-advance]
argument-hint: "<callsign> [--from <stage>] [--to <stage>] [--auto-approve]"
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

# Pipeline Autopilot — Full Autonomous Pipeline Run

You are a **pipeline orchestrator**. You run the entire pipeline for a work item from its current state to completion, handling each stage in an isolated context and managing approval gates along the way. You are the conductor — the stage skills are the musicians.

## Inputs

- `$ARGUMENTS` — parsed as: `<callsign> [flags]`
  - **callsign** (required): WCP callsign (e.g., `SN-3`)
  - **--from \<stage\>** (optional): Start from a specific stage number (0-7). Default: auto-detect from artifacts.
  - **--to \<stage\>** (optional): Stop after a specific stage number (0-7). Default: run to completion.
  - **--auto-approve** (optional): Enable ludicrous speed mode — auto-approve checkpoints when there are no blocking open questions.

Parse flags from $ARGUMENTS. The callsign is always the first token. Flags follow.

## Step-by-Step Procedure

### Step 1: Read Work Item and Detect Starting State

```
wcp_get(CALLSIGN)
```

Detect the current pipeline stage using the same artifact inspection logic as `/pipeline-advance`:

```
1. prd.md missing? → Stage 0
2. No discovery reports (neither discovery-report.md nor any discovery-report-*.md)? → Stage 1
3. architecture-proposal.md missing? → Stage 2
4. architecture-proposal.md pending? → Architecture approval gate
5. gameplan.md missing? → Stage 3
6. gameplan.md pending? → Gameplan approval gate
7. test-coverage-matrix.md missing? → Stage 4
8. Incomplete milestones in progress.md? → Stage 5 (specific milestone)
9. review-report.md missing? → Stage 6
10. qa-plan.md missing? → Stage 7
11. All present → Complete (run /create-pr)
```

If `--from` was specified and the detected stage is earlier than the specified stage, skip to the `--from` stage. If the detected stage is later (artifacts already exist), warn the user but proceed from where the pipeline actually is.

### Step 2: Configure Approval Mode

If `--auto-approve` was NOT passed, ask the user:

Use AskUserQuestion:
- Question: "How should I handle approval gates (architecture review, gameplan review)?"
- Options:
  - "Interview me at each gate" — walk through checklist items interactively (Recommended)
  - "Auto-approve if no blockers" — skip review when there are no blocking open questions
  - "Stop at gates" — pause and let me review manually

Save the choice as APPROVAL_MODE.

If `--auto-approve` was passed, set APPROVAL_MODE to "auto-approve" without asking.

### Step 3: Present the Plan

```
## Pipeline Autopilot: CALLSIGN

**Starting at:** Stage [N] ([stage name])
**Running to:** Stage [M] ([stage name]) [or "completion"]
**Approval mode:** [Interview / Auto-approve / Stop at gates]

### Stages to Run

[List each remaining stage with its name and a one-line description]

Starting now...
```

### Step 4: Pipeline Loop

Execute stages sequentially. Each stage runs in a Task agent for context isolation.

```
STAGE_ORDER = [
  { num: 0, name: "PRD",            skill: "prd",             gate: false },
  { num: 1, name: "Discovery",      skill: "discovery",       gate: false, per_repo: true },
  { num: 2, name: "Architecture",   skill: "architecture",    gate: true,  artifact: "architecture-proposal.md" },
  { num: 3, name: "Gameplan",       skill: "gameplan",        gate: true,  artifact: "gameplan.md" },
  { num: 4, name: "Test Generation",skill: "test-generation", gate: false, per_repo: true },
  { num: 5, name: "Implementation", skill: "implementation",  gate: false, multi: true, per_repo: true },
  { num: 6, name: "Review",         skill: "review",          gate: false, per_repo: true },
  { num: 7, name: "QA Plan",        skill: "qa-plan",         gate: false },
]
```

For each stage (starting from the detected or specified stage):

**A. Check if we should stop:**
- If `--to` was specified and we've passed that stage → stop
- If we're blocked → stop

**B. If this stage has a gate (Stages 2 and 3), handle it AFTER the stage runs:**

After Stage 2 or Stage 3 completes, handle the approval gate before advancing:

**Interview mode:**
- Invoke `/pipeline-approve` via the Skill tool: `Skill(skill="pipeline-approve", args="CALLSIGN")`
- This runs interactively — the user answers questions via AskUserQuestion
- If approved → continue to next stage
- If rejected → STOP. Report rejection reason.

**Auto-approve mode:**
1. Read the artifact that was just produced
2. Find the Open Questions section
3. Check: are there any questions marked as "blocking"? Are there any open questions with no recommendation?
   - If **no blocking questions and all have recommendations** → auto-approve:
     - Update the Approval Checklist: Status = "Approved", Reviewer = "autopilot", Date = today
     - Update `pipeline_approved_at` in frontmatter
     - Reattach the artifact via `wcp_get_artifact` + modify + `wcp_attach` (you have these tools)
     - Log: `wcp_comment(CALLSIGN, "pipeline/autopilot", "Auto-approved [artifact] — no blocking open questions.")`
   - If **blocking questions exist** → fall back to Interview mode:
     - Tell the user: "Auto-approve blocked — [N] blocking open questions need resolution. Switching to interactive review."
     - Invoke `/pipeline-approve` via Skill tool

Wait — **you do NOT have `wcp_attach` in your allowed tools for this skill.** If you need to auto-approve, use a Task agent that has the necessary tools:

```
Task(
  subagent_type="general-purpose",
  description="Auto-approve pipeline artifact",
  prompt="Read the artifact [artifact-name] from work item CALLSIGN via wcp_get_artifact.
  Update the Approval Checklist section: set Status to 'Approved', Reviewer to 'autopilot', Date to [today].
  Update pipeline_approved_at in YAML frontmatter to [timestamp].
  Reattach via wcp_attach. Log a comment via wcp_comment."
)
```

**Stop-at-gates mode:**
- Report: "Approval gate reached for [artifact]. Pipeline paused."
- Tell the user to run `/pipeline-approve CALLSIGN` manually, then `/pipeline-autopilot CALLSIGN --from [next-stage]` to resume.
- STOP.

**C. Run the stage (for non-gate stages, or after gate is cleared):**

Launch a Task agent:

```
Task(
  subagent_type="general-purpose",
  description="Run pipeline Stage [N] ([name])",
  prompt="You are running a pipeline stage. Invoke the skill:

Skill(skill='[skill-name]', args='CALLSIGN [extra-args]')

After the skill completes, summarize:
1. What artifact was produced
2. Whether it succeeded or had errors
3. Any issues flagged for human attention
4. What the skill said to do next"
)
```

**D. Handle Stage 5 (Implementation) — multi-milestone:**

Stage 5 is special: it runs once per milestone. After each milestone:
1. Re-read progress.md to find the next incomplete milestone
2. If another milestone exists → run `/implementation CALLSIGN [next-milestone]` in a new Task agent
3. If all milestones complete → advance to Stage 6

This means Stage 5 may spawn multiple Task agents sequentially (one per milestone). Each gets a fresh context.

**E. Handle per_repo stages (multi-repo projects):**

For stages marked `per_repo: true`, detect whether this is a multi-repo project by checking the work item's artifact list for multiple `discovery-report-*.md` artifacts.

**If multi-repo:**
1. **Stage 1 (Discovery):** Determine all repos involved (from PRD body or work item). For each repo without a `discovery-report-{repo-name}.md` artifact, run `/discovery CALLSIGN --repo <path>` in a Task agent. Run these sequentially (each may need significant context).
2. **Stage 4 (Test Generation):** Read the gameplan to identify all target repos. For each repo that doesn't yet have a `test-coverage-matrix-{repo-name}.md`, run `/test-generation CALLSIGN --repo <path>`.
3. **Stage 5 (Implementation):** When iterating milestones, read each milestone's `**Repo:**` field from the gameplan. Pass `--repo <path>` to each `/implementation` invocation. Milestones are already ordered by cross-repo dependency in the gameplan.
4. **Stage 6 (Review):** For each repo that has a `progress-{repo-name}.md` artifact, run `/review CALLSIGN --repo <path>`.

**If single-repo:** Behave as before (no `--repo` flag).

**F. Check for stage failure:**

After each Task agent returns, check the result:
- If the stage reported success → continue to next stage
- If the stage reported a failure (test failures after 5 attempts, spec gaps, missing prerequisites) → STOP
  - Report the failure
  - Log it as a WCP comment
  - Tell the user what to fix

**G. Log progress after each stage:**

```
wcp_comment(
  id=CALLSIGN,
  author="pipeline/autopilot",
  body="Autopilot: Stage [N] ([name]) complete. Advancing to Stage [N+1]."
)
```

**H. Report stage completion to user:**

After each stage, print a brief progress update:

```
--- Stage [N] ([name]): DONE ---
[1-line summary from Task agent]
```

### Step 5: Completion Report

When the loop ends (either all stages complete, blocked, or --to reached):

```
## Autopilot Complete: CALLSIGN

### Stages Executed
| Stage | Name | Result |
|-------|------|--------|
| 0 | PRD | [Done / Skipped / Failed] |
| 1 | Discovery | [Done (N repos) / Done / Skipped] |
| 2 | Architecture | [Done / Skipped] |
| 2.5 | Architecture Approval | [Approved / Auto-approved / Rejected / Skipped] |
| 3 | Gameplan | [Done / Skipped] |
| 3.5 | Gameplan Approval | [Approved / Auto-approved / Rejected / Skipped] |
| 4 | Test Generation | [Done / Skipped] |
| 5 | Implementation | [M1 Done (wcp-cloud), M2 Done (wcp-ios) / M2 Failed] |
| 6 | Review | [Done (N repos) / Done / Skipped] |
| 7 | QA Plan | [Done / Skipped] |

### Approval Decisions
[List any approval decisions made, with notes captured]

### Open Issues
[List any failures, spec gaps, or blockers encountered]

### Next Steps
- [If complete] "Run `/create-pr CALLSIGN` to push and create PR."
- [If blocked] "[What needs to happen before pipeline can resume]"
- [If --to reached] "Pipeline paused at Stage [M]. Run `/pipeline-autopilot CALLSIGN --from [M+1]` to continue."
```

### Step 6: Final Log

```
wcp_comment(
  id=CALLSIGN,
  author="pipeline/autopilot",
  body="Autopilot run complete. Stages [N]-[M] executed. Result: [success/blocked/paused]. [Summary of approvals and issues.]"
)
```

## Error Recovery

The pipeline is designed to be **idempotent** — re-running a stage is safe because:
- Document stages (0-3) overwrite their artifacts (same content, no side effects)
- Code stages (4-7) check pre-flight conditions before acting
- Approval gates check current status before prompting

If autopilot stops mid-run (session timeout, crash, error), just run it again:
```
/pipeline-autopilot CALLSIGN
```
It will detect the current state from artifacts and resume from where it left off.

## What NOT To Do

- **Do not run stages inline.** Every stage MUST run in a Task agent for context isolation. The autopilot's context window must stay small — it's an orchestrator, not an executor.
- **Do not auto-approve when blocking open questions exist.** Even in auto-approve mode, blocking questions trigger the interview flow.
- **Do not continue past a blocker.** Spec gaps, test failures, and rejection are hard stops.
- **Do not modify artifacts directly** (except for auto-approve). Stage skills own their artifacts.
- **Do not skip the progress report.** The user needs to see what happened at each stage.
- **Do not run without confirming approval mode.** The user must choose (or pass --auto-approve).

## When You're Done

The completion report (Step 5) serves as the final output. Make sure it includes:
1. Every stage that was executed and its result
2. Every approval decision made (with notes)
3. Any issues or blockers encountered
4. Clear next steps

## Success Criteria

- [ ] Detects starting stage correctly from artifact inspection
- [ ] Runs each stage in an isolated Task agent
- [ ] Handles approval gates in all three modes (interview, auto-approve, stop)
- [ ] Auto-approve falls back to interview when blocking questions exist
- [ ] Handles Stage 5 multi-milestone iteration
- [ ] Stops gracefully on failures (doesn't continue past blockers)
- [ ] Resumes correctly when re-run after a stop
- [ ] Reports clear progress after each stage
- [ ] Comprehensive completion report with all decisions logged
- [ ] Context window stays bounded regardless of how many stages run
