---
name: tempo
description: Switch operational tempo -- changes permission profile and interaction mode.
version: 0.1.0
execution-mode: side_effecting
meta-governance: config
argument-hint: "[recon | pair | glide | sprint | surge | overnight]"
category: fleet-ops
status: candidate
---
# Tempo Switch

### 0. Emit SKILL_INVOKE
Post SKILL_INVOKE to the bus before any stateful action.
```
Type: SKILL_INVOKE
To: all
Message: [skill=tempo] [mode=side_effecting] [args_hash=<sha256>] [session=<session_id>]
```
(The skill invocation runtime injects the caller's canonical identity as `from_id`.)

Switch the active operational tempo. This changes both your **permission profile** (what's auto-approved) and your **interaction mode** (how autonomous you are).

## Task

Argument: `$ARGUMENTS`

## Execution

1. If no argument is provided, print the tempo selection guide below and stop.
2. If an argument is provided, normalize it to lowercase and match against the 6 tempos.
3. Copy the matching profile to `settings.local.json`:
   ```bash
   cp ~/.claude/tempos/<TEMPO>.json ~/.claude/settings.local.json
   ```
4. Print the tempo card for the activated tempo.
5. Adopt the behavioral mode immediately for the rest of this session.

## Tempo Selection Guide

Print this when `[tempo]` is called with no arguments:

```
OPERATIONAL TEMPOS
==================

  [tempo] recon      Research only. No code changes. Read, explore, report.
  [tempo] pair       Collaborative. Propose before acting. Tight feedback loop.
  [tempo] glide      Rubber-stamp. Execute planned work, report after each step.
  [tempo] sprint     Full autonomy. Confirm plan once, then hands-off execution.
  [tempo] surge      Incident response. All resources on the critical path.
  [tempo] overnight  Async batch. Queue tasks, create PR, review in morning.

Current: [check settings.local.json to determine -- match against tempo profiles]
```

## Tempo Cards

### RECON
```
TEMPO: RECON
Permission tier: readonly (no git writes, no file edits)
Mode: Research only -- explore, analyze, report findings
DO: Read files, search code, run tests, query APIs, web research
DO NOT: Write files, edit code, create commits, push branches
Interaction: Deliver findings as a report. Let the human decide next action.
```

**Behavioral rules for RECON:**
- You MUST NOT use Write, Edit, or any file-mutating tools
- You MUST NOT run git add, git commit, git push, or any git write operations
- You MAY read files, search code, run tests (read-only), query web, use gh for reading
- Deliver all findings as structured reports
- End with recommendations, not actions

### PAIR
```
TEMPO: PAIR
Permission tier: standard (all Bash, no auto-Edit)
Mode: Collaborative -- propose before acting, tight feedback loop
DO: Propose approaches, show diffs before applying, ask for direction
DO NOT: Make large autonomous changes, skip human input on decisions
Interaction: Alternate moves. Agent proposes, human refines.
```

**Behavioral rules for PAIR:**
- Always propose your approach BEFORE implementing
- Show the specific changes you plan to make and wait for approval
- For architecture decisions, present options with trade-offs
- Keep changes small and incremental -- one logical step at a time
- Ask clarifying questions when requirements are ambiguous

### GLIDE
```
TEMPO: GLIDE
Permission tier: standard + Edit (file edits auto-approved)
Mode: Execute with rubber-stamp -- direction is clear, risk is low
DO: Execute planned work, report after each step, move fast on mechanical tasks
DO NOT: Make architecture decisions, change interfaces, refactor beyond scope
Interaction: Agent plans and executes. Human approves the overall direction.
```

**Behavioral rules for GLIDE:**
- Execute the work directly -- don't over-explain or over-plan
- Report concisely after completing each logical unit
- If you hit an unexpected decision point, pause and ask
- Good for: tests, docs, wiring, hardening, refactoring, lint fixes

### SPRINT
```
TEMPO: SPRINT
Permission tier: full (all Bash + Edit auto-approved)
Mode: Full autonomous execution -- confirm plan once, then hands-off
DO: Plan comprehensively, then execute all phases without stopping
DO NOT: Stop mid-execution for minor decisions, over-consult
Interaction: Human sets the goal. Agent delivers the result.
```

**Behavioral rules for SPRINT:**
- Present your full plan ONCE at the start, then execute without interruption
- Use parallel agents for independent work streams
- Ship the simplest thing that works
- Run tests and verify before reporting completion
- Post updates to the coordination bus for visibility

### SURGE
```
TEMPO: SURGE
Permission tier: full (all Bash + Edit auto-approved)
Mode: Incident response -- all resources converge on one critical issue
DO: Diagnose fast, fix fast, verify fast. Bias toward action.
DO NOT: Work on anything unrelated, gold-plate the fix, refactor
Interaction: Human triages. Agent fixes. Speed over elegance.
```

**Behavioral rules for SURGE:**
- Focus exclusively on the critical issue -- nothing else matters
- Diagnose root cause first, then apply the minimal fix
- Run tests immediately after fixing
- If the fix works, ship it. Clean up later.
- Post SITREP to bus after resolution

### OVERNIGHT
```
TEMPO: OVERNIGHT
Permission tier: full (all Bash + Edit auto-approved)
Mode: Async batch execution -- no human in the loop
DO: Execute all queued tasks, create PRs with summaries, batch results
DO NOT: Send messages, make irreversible infrastructure changes, deploy
Interaction: Human queues tasks before sleep. Agent delivers PRs in morning.
```

**Behavioral rules for OVERNIGHT:**
- Execute all tasks in priority order
- Create a PR for each logical unit of work with clear summary
- If blocked on a task, skip it and note the blocker -- don't wait
- Run full test suite before finalizing
- Post completion summary to coordination bus

## After Switching

After copying the profile and printing the tempo card, confirm:
```
Tempo switched to <TEMPO>. Permission profile updated.
Behavioral mode active for this session.
```

## Skill Chains

### Mandatory

- None — tempo is a meta-governance skill (Tier 2) that configures the session. No pre-chain needed. (Reclassified 2026-09-03 from "meta-skill" to "meta-governance: config" per meta-skill-doctrine.md — tempo does not invoke/compose other skills at runtime.)

### Advisory

- **After tempo switch**: `[bus]` (STATUS — announce new tempo for fleet visibility)

## Authority

- **T1 (TRUSTED)**: May switch tempo without restriction
- **T2 (Active/High)**: May switch to recon/pair/glide/sprint; surge/overnight require operator approval
- **T3 (Medium)**: May switch to recon/pair; glide/sprint/surge/overnight require operator approval
- **T4 (Probationary)**: May switch to recon only; all others BLOCKED
- **Operator**: Override any restriction
