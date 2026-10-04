---
name: plan-verify
description: >
  Harden a rough implementation plan into a verified one — expand each step and
  attach real proof, promoting confirmed steps to `🔗 verified`. Command-only,
  run once the product doc is settled and stable: it spends the real
  verification budget. Drafts a doc only.
disable-model-invocation: true
---

# Plan Verify

Verify the rough `impl.md` from `plan-impl` step by step against source code and
current external documentation, attaching proof to every claim. Last skill in the
chain: `plan-product` → `plan-impl` → **`plan-verify`**.

## Input and output

- Read `docs/plans/<slug>/impl.md`. If it is missing, stop and tell the user to
  run `plan-impl` first.
- The **only** write is back to that same `impl.md`. Read source files and
  external docs freely to check claims, but never change code, run git, or post
  to the network yourself. (External research goes through `dev-research`, below.)

## The verification mark

Every step ends at one of:

```
🔗 verified → src: path/to/file.ts:42          internal: the code exists / behaves as claimed
🔗 verified → doc: <url> §exact-section         external: the tool/approach is current and standard
❔ unverified (not checked)                      could not confirm this pass
❔ unverified (net-new)                          new code, so there is legitimately nothing to link
```

**No step is marked `🔗 verified` without proof you actually saw this session.**

- **Internal claims** — open the file and cite `file:line` you read. A step that
  says "add a handler in `FooService`" is verified only after you open the file
  and confirm `FooService` exists at that line. If it does not exist and the step
  is building it, that is `❔ unverified (net-new)` — expected, not a failure.
- **External claims** — a library API, a "standard" approach, a tool that may
  have changed since the model's training cutoff. Verify these by invoking the
  `dev-research` skill, which checks against current official docs before
  asserting. Cite the exact doc page and section it returns. Do not verify an
  external claim from memory — the cutoff makes that a real hallucination risk.

Leave a step `❔ unverified (not checked)` when you genuinely could not confirm
it this pass (docs unreachable, ambiguous, out of scope). Never downgrade an
honest unknown into a fake `🔗 verified`.

## Maturity is a separate axis

The maturity mark (`🌱`/`🤖`/`👤`/`✅`) is independent of verification. Advance a
step to `🤖 ai-audited(<model>)` on your own. Stamp `👤 human-ok` or `✅ settled`
only when the user explicitly instructs you to set that mark on a named step:
ask, wait for the instruction, then stamp — one step per instruction. Never stamp
either mark on your own initiative, and never reuse one step's instruction for
another. A step can be `🔗 verified` against source while still `🤖 ai-audited` on
maturity; that is a valid, expected combination.

## Workflow

1. Read `impl.md`. Work step by step, expanding each rough step into concrete
   detail as you go.
2. For each claim in a step, decide internal or external, then verify:
   - Internal → open the file, confirm, cite `src: file:line`.
   - External → invoke `dev-research`, cite `doc: <url> §section` it returns.
   - New code with nothing to check → `❔ unverified (net-new)`.
   - Couldn't confirm → `❔ unverified (not checked)`, and say why in the step.
3. Stack both marks on the step's mark line, e.g.
   `🤖 ai-audited(opus-4.8) · 🔗 verified → src: backend/export.ts:42`.
4. Update the `## Maturity` header in the same pass so it can't drift.

## human-writing

Follow the `human-writing` skill for any expanded prose.

## After writing

Do not render the doc in chat. Show the path and report a one-line tally: how
many steps are now `🔗 verified` (src vs doc), how many `net-new`, and how many
still `not checked` and why. Flag anything the verification pass proved wrong in
the product plan so the user can revisit it.
