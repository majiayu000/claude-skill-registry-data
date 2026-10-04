---
name: apply-plan
description: >-
    Execute an existing plan folder under tmp/ from its first unfinished step onward — read the
    plan's README for order and dependencies, then apply each remaining step in turn (via the
    apply-step workflow), validating after each. Resumable and idempotent. Use when asked to apply,
    execute, continue, or resume a plainworks plan.
---

# Applying a plan from its remaining steps

`apply-plan` takes a plan folder (produced by `create-plan`) and drives it to completion, **starting from the first step that is not yet done** so it can be run repeatedly to resume interrupted work.

## Input

A plan folder under `tmp/` — e.g. `tmp/channel-sse-reconnect/`. If the caller does not name one, list candidates and ask which to apply:

```bash
ls -d tmp/*/
```

## 1. Read the plan and compute the remaining steps

- Read `tmp/<plan>/README.md` first: the goal, the ordered step index, the **dependency order**, and the cross-cutting baseline rules that bind every step.
- List the step files and find each one's progress signal — the `**Status:**` field and the `- [ ]` / `- [x]` acceptance boxes.

```bash
ls tmp/<plan>/NN-*.md 2>/dev/null || ls tmp/<plan>/*.md
grep -n '\*\*Status:\*\*' tmp/<plan>/*.md
```

- **Remaining = every step not marked `done`.** The first remaining step in dependency order is the resume point. A step is eligible only when the steps it *Depends on* are already `done`; never start a step ahead of an unfinished dependency.

## 2. Apply each remaining step in order

For each remaining step, in dependency order, run the **`apply-step` workflow** on that step file (read the README + all prior steps for context, apply the current step test-first, validate, mark it done). Do not skip ahead; do not batch several steps into one undifferentiated change — each stays a standalone, reviewable unit.

Between steps:

- **Validate the affected package(s)** with the [`validate`](../validate/SKILL.md) skill (scoped `turbo`/`bun run`) — do not proceed on a red one.
- If a step's acceptance criteria cannot be met as written, **stop** and report the divergence rather than forcing a green; the plan may need a `create-plan` revision. The baseline in [`../../copilot-instructions.md`](../../copilot-instructions.md) wins over the plan text. That includes a step written as "additive" or "keep the old path working". In alpha, apply it for the end state, or revise the plan first.

## 3. Baseline and review

Every step is executed against plainworks' baseline, not a looser plan-local standard. After a step (or a coherent group of steps) lands, run the [`review`](../review/SKILL.md) passes over the diff in a fresh, clean-context agent. Treat a green `validate` run as necessary but not sufficient.

## Repo workflow

Do the work on a branch — cut it with [`create-branch`](../create-branch/SKILL.md) (off an up-to-date `main`, named by the change, not the plan or a step number). Apply steps and leave the edits **uncommitted**: the maintainer commits and pushes, and a PR is opened (in **draft**) only when explicitly asked. Applying a plan never commits, pushes, or opens a PR on its own.
