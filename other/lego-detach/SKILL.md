---
name: lego-detach
description: "Detaches a brick from a model and keeps it in the parts bin. Inputs that depended on it switch to their declared stubs so the model keeps running."
argument-hint: "[manifest path] [brick id]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion, Task
---

# /lego-detach — Lego Detach

**Category:** Lego (Modular Models) · **Primary agent:** `modeling-methodology-specialist`

Detaches a brick from a model and keeps it in the parts bin. Inputs that depended on it switch to their declared stubs so the model keeps running.

Arguments: `$ARGUMENTS`

## Purpose
Take a brick out of a model while keeping the model running: inputs that depended on it switch to their declared stubs, the brick stays in the parts bin with its files and validation history, and the difference between the attached and detached runs measures the contribution of the channel that was switched off. The output is an updated manifest and a clear statement of what economic feedback was removed.

**Use it when** simplifying a model, isolating the contribution of a channel, or removing a component that is unvalidated or not needed for the question.

**Do not use it when** the brick should be replaced by an alternative in the same slot (`/lego-swap`).

## Before you start
1. **Check required inputs.** For each input below record `FOUND` or `ABSENT` (never 'assumed'):
   - A model.lego.json manifest
   - The brick to detach
   If a required input is `ABSENT`, that part is **`NOT ASSESSED — NO DATA`**: do not estimate or invent it; name what is missing and which skill produces it. If all required inputs are absent, stop and say so.
2. **Check confidentiality.** Identify the data classification level of the inputs (`.claude/docs/confidentiality-and-ai-use.md`). Do not proceed with restricted or confidential data in a way the policy does not allow.
3. **Collaboration.** Follow `.claude/docs/collaboration-protocol.md`: ask questions first, present options, get approval before writing files, and update `production/session-state/active.md` after each approved section.

## Agents
- `modeling-methodology-specialist` — primary agent; coordinates the work and integrates results
- `economic-reasoning-specialist` — Frames the economic question and tests whether results make economic sense
- `model-validation-specialist` — Performs independent model validation

Run these agents as subagents (the `Task` tool), in parallel where the steps are independent. Subagents only write to the paths named in your instructions.

## Workflow
1. Dry-run: `python tools/lego.py detach <manifest> <brick>`. Present the plan: joints removed, stubs activated (with the fallback each uses), identities affected, and neighbours to re-validate
2. If the tool reports an OPEN stud (a consumer has no stub), the brick cannot be detached as is. Offer: add a stub to the consumer, swap the brick (`/lego-swap`), or force it only if the user insists
3. Explain the economic consequence of each activated stub: which feedback channel is switched off
4. Apply with `--apply --note '<why>'`. The brick stays in the manifest as detached; its code and files are not deleted
5. Run the model with the stubs and compare with the attached version. The difference is the contribution of the detached channel, which is useful in its own right
6. Mark neighbours for re-validation; keep the validation status of the detached brick

## Checkpoints with the user
- After the dry-run: approve the stub consequences
- After the comparison: confirm the interpretation of the channel's contribution

## Common pitfalls
- Detaching without explaining which feedback disappears
- Forcing a detach that leaves open studs
- Deleting the brick's files instead of keeping them in the parts bin

## Output
`Updated model.lego.json (+ history entry)`

The history entry records the reason; the comparison of attached and detached runs quantifies the channel's contribution.

## Gate / verdict
- Every consumer of the brick has a stub or a replacement
- Identities still verifiable
- The user was shown the stub consequences before applying
- The attached-versus-detached comparison is reported

## Suggested next steps
- `/lego-check`
- `/lego-add`
