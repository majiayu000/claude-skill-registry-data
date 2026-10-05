---
name: vanara-orchestrate
description: Run a goal end-to-end as a gated pipeline of specialist agents — reproduce → test → patch → review → commit — where nothing advances past a gate until its exit condition holds and the required agent has signed off. Use when a task needs several agents in sequence with checkpoints, not a single one-shot answer.
type: skill
version: 1.0.1
updated: 2026-07-27
---

# vanara-orchestrate — outcomes, not one-shots

A single agent answers a question. **Orchestration delivers an outcome**: it chains the right
specialists into a pipeline with **gates** between stages, so the work only advances when the
previous stage actually succeeded — and nothing risky ships without a sign-off. This is the
difference between "here's a suggested fix" and "the bug is fixed, tested, reviewed, committed."

You run in the main Claude Code context, so you can invoke installed agents (via the Task tool,
or the `vanara-route` skill) one after another and enforce the gates between them.

## The core loop

For any goal, run **plan → act → gate → advance**, repeating until done:

1. **Plan the pipeline.** Pick the named workflow that fits the goal (see
   [references/workflows.md](references/workflows.md)), or compose one from installed agents.
   State the stages and their gates up front, in one short line each.
2. **Run one stage.** Invoke exactly one agent for the current stage and let it finish.
3. **Check the gate.** Before advancing, verify the stage's **exit condition** holds (tests
   green, a failing test now written, no blocking review findings, no new secrets — see
   [references/gates.md](references/gates.md)). If it doesn't hold, do **not** advance: loop
   back, fix, and re-check. A gate is a hard stop, not a suggestion.
4. **Checkpoint.** Record the stage result so the run is auditable and resumable:
   ```bash
   node .claude/skills/vanara-orchestrate/scripts/checkpoint.mjs "fix-defect" "review" "pass"
   ```
5. **Advance** to the next stage, or finish.

## Named workflows

- **fix-defect** — reproduce → write a failing regression test → patch → review → commit.
  Gate before commit: tests green **and** the reviewer returns no blocking findings.
- **ship-feature** — plan → write tests first → implement → review → commit. Gate before
  implement: tests exist and fail (RED); gate before commit: GREEN + review clean.
- **harden** — audit (security) → triage → fix highest severity → re-audit → report. Gate
  before "done": the re-audit shows the fixed findings gone and no new ones introduced.

Full stage/gate definitions are in [references/workflows.md](references/workflows.md).

## Rules that make orchestration trustworthy

- **One agent per stage.** Don't blur stages; each has one owner and one gate.
- **Never skip a gate to save time.** A red gate means the pipeline stops and reports exactly
  which condition failed and why — that failure is the useful output, not a thing to hide.
- **Escalate, don't loop forever.** If a stage can't clear its gate after a reasonable attempt,
  stop and hand back to the user with the specific blocker. Cap retries (2–3), don't spin.
- **The reviewer is the last gate.** For anything that writes to the repo, the final stage is a
  review, and nothing commits with blocking findings open.
- **Respect the operating protocol.** Every stage still grounds its claims and logs its changes;
  orchestration adds sequencing and gates on top, it doesn't replace an agent's own discipline.

## Edge cases

- **Missing agent for a stage** → use `vanara-route` to find the closest fit, or tell the user
  which specialist to `npx vanara install` before the pipeline can run.
- **A gate that can't be evaluated** (no tests exist to run) → say so; treat an unverifiable
  gate as *not passed*, don't wave it through.
- **Partial progress** → the checkpoint log lets you resume from the last passed stage instead
  of restarting the whole pipeline.

## Example

> **Goal:** "the login endpoint 500s on an empty email."
>
> Pipeline (`fix-defect`): `debugger` reproduces → `test-author` writes a failing test for the
> empty-email case (gate: test is RED) → `debugger` patches validation (gate: that test is now
> GREEN) → `code-reviewer` reviews (gate: no blocking findings) → commit. Each stage checkpointed;
> if review flags a blocking issue, the pipeline loops back to the patch stage, not forward.

## Worked micro-example

A real run of the fix-defect pipeline, gate by gate:

```text
$ goal: "users report duplicate webhooks after retry"

[gate 1 REPRODUCE] debugger writes a failing test that fires the dup
                   → RED (good — the bug is now falsifiable)      PASS
[gate 2 TEST]      test-author hardens it: adds the idempotency-key
                   contract test the codebase never had            PASS
[gate 3 PATCH]     fix lands: dedupe on (source_id, delivery_id)
                   unique index + upsert                           PASS
[gate 4 REVIEW]    code-reviewer: flags the index migration as
                   non-concurrent — BLOCKS                         FAIL
[gate 4 RETRY]     migration rewritten CONCURRENTLY → re-review    PASS
[gate 5 COMMIT]    checkpoint.mjs logs all five gates; commit cites
                   the checkpoint id
```

The point of the transcript: gate 4 FAILING is the system working — a blocked
stage stops the pipeline instead of shipping a table lock to production.
