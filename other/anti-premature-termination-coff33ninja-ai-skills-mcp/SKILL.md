---
name: anti-premature-termination
description: Prevents declaring a task complete before it's actually done. Enforces explicit completion criteria, verification steps, and receipt-based confirmation.
---

# Anti-Premature Termination Skill

## Problem

Agents say "done" when they're not done. The prose claims success, but the tool call failed, or the output wasn't verified, or only half the task was completed.

This is the **Acknowledgment-Action Gap**: saying "I've updated the file" and actually updating it are separate forward passes with no invariant holding them together. The model can narrate success it hasn't produced.

Also covers **premature termination** — the agent stops after the first plausible-looking result without verifying all requirements were met.

## Detection triggers

Activate when:
- About to say "done", "completed", "finished", "all set"
- About to declare success after a single tool call
- The task has multiple steps and you've only done one
- A tool call returned an error but you're tempted to proceed anyway
- You're summarizing what was done without checking the actual receipts

## Protocol

### 1. Receipts over narration
Before saying anything is done:
- Check the tool call receipt (did the edit actually succeed?)
- Read the file back (does the content match what was intended?)
- Run the relevant command (does it compile/run/pass?)

If you cannot verify, say: "I attempted X but I can't confirm it succeeded — please check."

### 2. Completion criteria
Before starting a task, list what "done" means:
- What specific outputs are expected?
- What tests should pass?
- What files should be modified?
- What should the user be able to do afterward?

Only declare completion when ALL criteria are met.

### 3. Multi-step tasks
For tasks with 2+ steps:
- After each step, verify before moving to the next
- Do not batch confirm ("steps 1-3 are done, moving to 4")
- If step 2 depends on step 1, verify step 1's output before writing step 2

### 4. Error handling
If a step fails:
- Do NOT say it's done and move on
- Do NOT silently retry with the same approach
- Tell the user what failed, what was attempted, and what the error was

### 5. Final check before declaring done
Ask:
1. Did I actually do everything the user asked?
2. Can I prove it with a file read, test output, or command result?
3. Would a reviewer looking at my trace agree this is complete?

If answer to any is "no", do not declare done.

## When NOT to use
- Exploratory research tasks where "done" is inherently fuzzy
- User explicitly says "just try it, no need to verify"
- Tasks where the tool result is the completion proof (e.g., API returns a success ID)

## Bundled Script

Copy `check-completion.ps1` to your project's `.ai_scripts/` directory:

```powershell
cp <skill-path>/anti-premature-termination/scripts/check-completion.ps1 .ai_scripts/
```

Scans a TODO.md and reports incomplete items — use before declaring a task done:

```powershell
.ai_scripts\check-completion.ps1 -TodoFile .ai_scripts\TODO.md
.ai_scripts\check-completion.ps1 -TodoFile TODO.md -TaskDescription "deploy"
```

## Cross-references

- **self-validate** — Run validation as part of completion verification criteria.

- **project-backup-status** — Backup before changes is a completion criterion.

- **anti-tool-sprawl** — Premature termination is often caused by tool sprawl wasting context.
- **release-changelog** — Do not declare a release complete until tags are pushed, CI passes, and versioned docs are synced. These are hard completion criteria.
- **skill-loader** — Apply the capped selection policy when deciding which verification and tracking skills should also be active for completion criteria enforcement.
- **test-driven-development** — Passing tests are explicit completion criteria. Do not declare done until tests pass.
- **code-review** — Passing code review is a completion gate. Do not declare done until review findings are resolved.
- **incremental-implementation** — Each slice merged is a completion milestone. Do not declare the feature done until all slices are merged.
- **adr-and-documentation** — Documentation updates are a completion criterion. Do not declare done until ADRs and docs are updated.
- **receiving-code-review** — Review feedback must be resolved before declaring done. Each comment verified, each change tested.
- **code-simplification** — "Simplified" is not "done". Verify the simplification didn't break anything.
- **ci-cd-automation** — CI passing is a completion criterion. Do not declare done until the pipeline is green.
- **performance-optimization** — "Optimized" is not done until measured improvement is confirmed.
- **shipping-and-launch** — Do not declare launch complete until the monitoring period passes and rollback plan is verified.
