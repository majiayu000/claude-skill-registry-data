---
name: kaizen-audit
description: >-
  Audits a kensaiapp pipeline skill through an artifact it produced. Spawns the
  blind auditor fan-out (one kensaiapp-auditor per lens, none of them given the
  skill) over the artifact and its inputs, then the non-blind synthesis passes
  (version comparison, surfaced-set comparison) over both versions of the
  outputs, and gathers every finding into an audit.md
  beside the artifact. The caller supplies the evidence, the surfacing fact, and
  any prior round; this skill runs the auditors and collects what they find. Use to run
  the audit over a settled, snapshotted artifact — "audit this evidence", "fan
  out the auditors", "audit the <skill> output". Emits findings only. It does not
  produce the evidence it reads and does not act on the findings it emits.
license: MIT
metadata:
  author: Eyal Golan
  version: "2.2.3"
  created: "2026-07-17"
  category: audit
  tags: audit, auditor, fan-out, lenses, skill-hardening
  risk: safe
  depends-on: kensaiapp-auditor
---

# kaizen-audit — audit a skill through its output

You judge a **skill** through an artifact it produced, and hand back findings. The
looking is done by `kensaiapp-auditor` subagents, each carrying one lens; you
orchestrate. This skill owns *which auditors run, on what, in what order, and how
their findings are gathered* — the lens files own *how to look*. When this skill and
a lens seem to disagree, the lens wins.

The audit is one job with two halves: a **blind fan-out** — auditors that see the
artifact and never the instrument that made it — and a **non-blind synthesis** —
passes that compare across versions and locate a defect in the stack's text, which
a fresh read cannot do. You run the first, then the second, then collect.

## Scope — what the caller hands you, and what you hand back

You are given, by whoever calls you:

- **The artifact under audit and its inputs** — the produced document (a PRD, an
  SRS, …), the source inputs the skill consumed, and the answered companion
  file(s) if the skill surfaces work to the owner.
- **Whether the skill surfaces work to the owner** — a fact, stated by the caller.
  `compare_surfaced_set` is gated on it and must not infer it from the evidence (a
  dropped trail would hide behind the inference).
- **The prior version's artifact and its `audit.md`, if one exists** — the input to
  the comparison passes. Its absence just means those passes skip.
- **Round-shape flags** — anything that makes a cross-version comparison invalid: a
  delete-and-recreate rather than a re-run, a skill-version change between the draft
  and the settle, an owner override later withdrawn. These go into every auditor's
  brief so it judges on the right basis.

You hand back **findings**, gathered into an `audit.md` beside the artifact. You do
**not** produce the evidence you read — if the artifact and its inputs are not
already sitting together as a snapshot, stop and say so rather than auditing a live
file in place. And you do **not** act on the findings — fixing the skill, and
anything the caller does with the result, is the caller's, not yours.

## Read first

Before spawning anything, read — using the `<CORE>` path the session hook injects,
never a literal `core/`:

- `<CORE>/doctrine/kaizen/lenses/README.md` — the lens set and the blind/non-blind
  split. This is the authority for **which** lenses run at the fan-out and which at
  synthesis. If it has grown since this skill was written, follow it, not the list
  below.

Do **not** read the individual lens files yourself. Each auditor reads its own — and
only its own — so a lens can't learn which failures are another's job. Pulling the
whole set into one context here is the exact thing the fan-out is designed to
prevent.

## Step A — the blind fan-out

Spawn **one `kensaiapp-auditor` per blind lens** named in the lenses README (at this
writing: `content`, `surfacing`, `coverage`, `altitude`, `traceability` — follow the README if
it differs). They run **concurrently** — spawn them in one batch.

Each auditor's task prompt gives it:

- **The one lens it carries**, by name. One lens per auditor, never more. Naming the
  lens is enough — the agent loads its contract (`<CORE>/doctrine/kaizen/lenses/contract.md`)
  and its lens itself.
- **The artifact and its inputs** — and the answered companion(s) if the skill
  surfaces.
- **Nothing about the skill, the stack, the other auditors, or any prior version.**
  This is the whole of "blind": the lens judges the instrument through its output
  and is not shown the instrument. An auditor handed the SKILL.md stops fresh-reading
  and starts grading the text — the failure the design exists to prevent.
- **The round-shape flags**, where they bear on the lens.

A blind auditor reports findings with their classification
(blocking/non-blocking, change-local/skill-general) but **does not name a layer** —
locating needs the stack's text, which it doesn't have.

## Step B — the non-blind synthesis passes

Run these **after** the fan-out returns — they need both versions of the artifact,
so they can't be fresh-read and must never be handed to a blind lens. Gate each on
the lenses README's "when" column:

- **`compare_versions`** — when a prior version exists. Given this artifact, the
  prior artifact and its `audit.md`, and this round's answered companion. Asks
  whether the version bump earned itself and walks every unauthorized delta. No
  prior version → skip in one line.
- **`compare_surfaced_set`** — when the skill surfaces work **and** a prior version
  exists. Asks whether the change moved what the skill asks the owner. No surfacing
  pattern → skip in one line.

The two comparisons can run as their own concurrent batch.

## Step C — gather into audit.md

Collect every auditor's findings into one `audit.md` beside the artifact. You
**gather**; you do not re-judge or overrule a verdict. It should carry:

- **A producing-stack manifest** — the exact version of every layer the artifact was
  made by, so a later reader knows what "this stack" meant.
- **The round shape** — re-run vs delete-and-recreate, any mid-round version change,
  any owner override, and what each does to the comparisons' validity.
- **Who ran** — the blind lenses spawned, the synthesis passes run or skipped (with
  a one-line reason per skip), and the model they ran on.
- **The findings** in the contract's ledger grammar, grouped by classification,
  skill-general first — no layer is named here; locating is the fix-author's, at
  the deciding.
- **Disagreements surfaced, not silently resolved** — name where two auditors
  differ; don't delete a verdict to make the file tidy.

If a prior `audit.md` sits beside the previous version, match its shape — the
comparison passes only work if the audits are legible against each other.

## Close

**Commit `audit.md` first.** It is the round's durable record — the baseline the next
round's comparison passes read, and the asset the escape hatch harvests — so it must
land in git, never sit uncommitted for the caller to notice and rescue. Stage only
`audit.md` and commit it through the commit builder (`<CORE>/tools/commit_builder.py`),
resolving every trailer per `<CORE>/doctrine/governance/commit_format.md`: a
`kaizen(<skill>):` subject naming the version and verdict, the directional trailer
against the instance's open station, and `Role: Product` — the judging record is the
owner's. Committing the record is **not** acting on the findings: it persists the
output you just wrote. The fix stays the caller's.

Then report where `audit.md` landed and a one-line count: how many findings, how many
skill-general (the ones that point at a stack edit), how many change-local
(recorded about the artifact, not the skill). State that the audit is done and the
findings are the caller's to act on. Do not fix the skill, and do not remove the
artifact — neither is yours.

## Critical rules

- **Blind means blind.** The fan-out auditors never see the skill or the stack. The
  moment one does, its read is no longer fresh, and the finding it would have made
  from the artifact alone is gone.
- **One lens per auditor.** A lens that reads its siblings learns which failures are
  someone else's job and stops looking there.
- **Synthesis is not blind, and never a fan-out lens.** The comparisons need both
  versions. Run them at synthesis, never hand one to a blind auditor.
- **Gather, don't re-judge.** You orchestrate and collect. A verdict is the
  auditor's; surface disagreement, don't overwrite it.
- **Findings are the whole job.** You take the evidence as given, write the findings
  into `audit.md`, commit that record, and stop there. Producing the evidence, and
  acting on the findings, are the caller's.
