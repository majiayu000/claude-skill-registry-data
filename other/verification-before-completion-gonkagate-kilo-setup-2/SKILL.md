---
name: verification-before-completion
description: "Decide the smallest sufficient proof set before closeout for TypeScript/Node backend work. Use whenever the question is whether a change is actually ready, what must be verified before completion, which concrete checks are enough, or whether a readiness claim is under-evidenced, even if the user only says 'is this done?', 'what should we verify?', or 'can we close this out?'."
---

# Verification Before Completion

## Purpose

Use this skill to decide what proof is actually needed before a backend change
should be treated as ready.

This skill is a narrow `workflow-meta` specialist. It does not own design,
implementation, or full test-plan authorship. Its job is to turn a closeout
question into:

- a small set of proof obligations
- the smallest convincing checks for those obligations
- a clear readiness verdict
- an explicit list of what is still unproven

When used from a project agent, let the agent own scope, handoffs, and final
decisions. This skill owns proof selection and readiness discipline only.

## Expert Standard

Do not spend time restating generic closeout advice.

This skill is not here to repeat normal engineering hygiene.
It should create a durable expert delta over a competent baseline answer by
being narrower, deeper, and more discriminating about proof:

- name the exact claim that needs proof before asking for checks
- identify the seam that actually owns that claim
- choose the smallest check that can actually falsify that claim
- distinguish fresh direct evidence from partial, stale, or irrelevant signals
- explain why the chosen layer is sufficient and why smaller or broader layers
  lose
- refuse to let broad reassurance stand in for missing seam-specific proof
- say "not yet verified" when a material claim still lacks evidence
- keep the answer compact enough to drive the next closeout step immediately

If the answer would still look good after replacing the concrete task with
"some backend change," it is too generic for this skill.

## Read These References When You Need Them

- `references/proof-selection-workflow.md`
  Use by default when deciding what actually needs proof before closeout.
- `references/seam-activation-matrix.md`
  Use when deciding which shared topic seams the current change really
  activates.
- `references/readiness-claim-bar.md`
  Use before endorsing a readiness claim or when existing evidence feels thin.
- `references/proof-layer-matrix.md`
  Use when several plausible checks exist and the hard part is choosing the
  narrowest honest proof layer.
- `references/stack-specific-proof-anchors.md`
  Use when the proof method is mostly clear but exact stack semantics could
  still make the chosen check misleading or insufficient.
- `references/proof-smells.md`
  Use when the proposed checks sound broad, theatrical, stale, or poorly
  matched to the changed risk.

## Relationship To Shared Research

Start with the local method and references in this skill.

This skill should not own a separate umbrella deep-research prompt.

Load `references/proof-selection-workflow.md` by default.

Load `references/seam-activation-matrix.md` before pulling in shared topic
packs.

Load `references/readiness-claim-bar.md` before calling something ready, or
when the honest answer might be conditional or "not yet verified."

Load `references/proof-layer-matrix.md` when choosing between unit, service,
route, contract, integration, migration-preflight, targeted runtime, or
workflow-recovery proof.

Load `references/stack-specific-proof-anchors.md` when proof sufficiency turns
on exact Fastify, schema, Prisma/Postgres, Redis, workflow-state, or Vitest
semantics rather than on method alone.

Load `references/proof-smells.md` when the first proof set feels too broad,
too indirect, or too stale.

Then load only the shared topic files that match the changed claim:

- `../_shared-hyperresearch/deep-researches/api-contract.md`
  Use for request or response schema, validation, serialization, content-type,
  OpenAPI/publication, or compatibility-sensitive claims.
- `../_shared-hyperresearch/deep-researches/fastify-runtime.md`
  Use for hooks, decorators, plugin order, reply ownership, startup, shutdown,
  streaming, or lifecycle-sensitive runtime claims.
- `../_shared-hyperresearch/deep-researches/prisma-postgresql.md`
  Use for schema changes, migrations, constraints, transactions, query shape,
  and real database semantics.
- `../_shared-hyperresearch/deep-researches/redis-runtime.md`
  Use for TTL, Lua/script, guard, reconnect, readiness, coordination, or
  replay-sensitive Redis claims.
- `../_shared-hyperresearch/deep-researches/runtime-workflow-state-machines.md`
  Use for legal transitions, waits, timers, cancellation, recovery, and
  re-entry-sensitive workflow claims.
- `../_shared-hyperresearch/deep-researches/vitest-qa.md`
  Use when the hard part is choosing the proof layer, harness realism,
  isolation discipline, or the smallest convincing test shape.

Do not load all topics by default. Start with the changed seam plus only the
adjacent seam that would materially change the proof choice.

## Scope

- decide what proof is materially required before closeout
- map each changed claim to the smallest honest check
- inventory what is already proven, partially proven, stale, or still missing
- decide whether a readiness claim is supported, conditional, or unsupported
- name the residual risk when full proof is unavailable

## Boundaries

Do not:

- turn the task into design review or architecture critique
- write the full implementation or test plan unless the task is explicitly
  redirected
- default to the broadest test layer "just to be safe"
- treat compile-time green checks as proof of changed runtime, data, or state
  behavior
- treat stale CI, previous runs, or generic manual notes as fresh closeout
  evidence
- endorse readiness while a material claim remains unproven
- load every shared topic "for completeness"

## Escalate When

Escalate if:

- the underlying design is still unsettled, so proof cannot be chosen honestly
- the change portfolio is large enough to need a dedicated test-plan skill
- the current evidence surface is too thin to produce even a conditional
  verdict
- the main question is test quality review, design quality review, or root
  cause analysis rather than closeout proof

## Relationship To Neighbor Skills

- Use `technical-design-review` when the main question is whether the design
  itself is sound, not whether the current proof is sufficient.
- Use `typescript-coder-plan-spec` when the main task is execution sequencing
  rather than closeout verification.
- Use `vitest-qa-tester-spec` when the proving surface is large enough to need
  a dedicated test strategy or test-plan artifact.
- Use `vitest-qa-review` when the main question is whether existing tests are
  any good, rather than what proof is still needed before closeout.
- Use `typescript-systematic-debugging` when the main question is root-cause
  isolation rather than readiness proof.

## Input Sufficiency

Before answering, identify the minimum known facts:

- what changed
- what is being claimed as safe, complete, or ready
- which seams are actually touched:
  contract, runtime, data, Redis/state, workflow state, testing
- what fresh evidence already exists
- what the biggest wrong-closeout risk would be if the claim is false
- what execution surfaces are available:
  focused test file, route inject, real DB/Redis integration, startup/shutdown
  check, contract diff, migration preflight, manual probe

If those facts are missing, say so explicitly and lower confidence. Do not
invent test coverage, infra realism, or command results.

## Core Defaults

- Every readiness claim is claim-by-claim, not vibe-based.
- Fresh direct evidence beats broad historical reassurance.
- The smallest honest check is better than the broadest possible suite.
- Wider realism is justified only when lower layers cannot prove the claim.
- Stale, indirect, or neighboring evidence does not close a proof obligation.
- If one material claim is still open, the honest output may be conditional or
  not-ready.
- Residual risk should be stated explicitly, not hidden inside a positive
  verdict.

## Workflow

1. Normalize the closeout claim.
   - What changed?
   - What exactly is being claimed ready?
   - What would regress if that claim is wrong?
2. Activate only the touched seams.
   - Use `references/seam-activation-matrix.md`.
   - Pull in only the shared topics that change the proof choice.
3. List the proof obligations.
   - Name the concrete claims that need evidence:
     contract integrity, runtime lifecycle correctness, migration safety,
     Redis/state semantics, workflow-transition correctness, or test-layer
     sufficiency.
4. Inventory current evidence.
   - Classify each evidence item as:
     `fresh direct`, `partial`, `stale`, `indirect`, or `missing`.
   - Keep facts separate from interpretations.
5. Choose the smallest proof set.
   - For each open obligation, choose the smallest check that can genuinely
     falsify the risky claim.
   - Use `references/proof-layer-matrix.md` when the honest layer is
     non-obvious.
   - Use `references/stack-specific-proof-anchors.md` when a tempting proof
     layer might be invalidated by concrete stack semantics.
   - Common examples:
     - focused typecheck or no new test for a structure-only change with no
       runtime risk
     - `app.inject()` or route-level proof for request validation,
       serialization, headers, and in-process HTTP behavior
     - targeted startup, shutdown, or real `listen()` proof when `inject()`
       cannot cover the changed runtime behavior
     - real Postgres integration or migration preflight for constraints,
       transactions, backfills, and query semantics
     - real Redis proof for TTL, Lua, guard, reconnect, or coordination
       semantics
     - persisted transition and recovery checks for workflow-state claims
     - `vitest-qa` guidance when the honest proof layer is non-obvious
6. Remove proof theater.
   - Drop checks that do not change the verdict.
   - Drop broader layers when a narrower layer already proves the same claim.
7. Decide the readiness verdict.
   - `verified ready`
   - `conditionally ready`
   - `not yet verified`
     Use `references/readiness-claim-bar.md` before choosing.
8. Report what remains unproven.
   - Name the exact unsupported claim or missing check.
   - If risk is being accepted, say so explicitly instead of implying proof.

## Reasoning Obligations

For any non-trivial closeout question, force all of these before endorsing a
verdict:

- `Claim`
  - What exact behavior or guarantee is being treated as ready?
- `Risk If Wrong`
  - What user-visible, operator-visible, or data-visible failure would escape?
- `Current Evidence`
  - What is directly observed versus inferred?
- `Smallest Honest Check`
  - What is the narrowest check that could still falsify the claim?
- `Why This Layer`
  - Why is a smaller layer insufficient, or why is a broader layer unnecessary?
- `Residual Gap`
  - What would still remain unproven even if the chosen check passes?
- `Verdict Discipline`
  - Does the current evidence justify `verified ready`, only
    `conditionally ready`, or `not yet verified`?

If a claimed point cannot survive those passes, demote it or drop it.

## Deliverable Shape

Return closeout work in this order:

- `Verification Verdict`
- `Proof Obligations`
- `Smallest Proof Set`
- `Unsupported Or Unproven Claims`
- `Residual Risk / Confidence`

For each item in `Proof Obligations` or `Smallest Proof Set`, include:

- `Claim`
- `Why It Matters`
- `Evidence Status`
- `Chosen Check`
- `Why This Is Enough`

## Quality Bar

Keep a point only if all are true:

- the changed claim is specific
- the chosen check could actually falsify that claim
- the evidence status is honest
- the proof layer matches the real seam being changed
- the verdict does not quietly rely on unrun checks or stale results
- the residual unproven area is explicit
- the reasoning is narrower and more discriminating than generic closeout
  advice would be

Reject these weak patterns:

- "run the suite"
- "CI was green earlier"
- "lint and typecheck passed, so we are done"
- "manual smoke looked fine"
- "add an integration test" without naming the claim it proves
- "probably ready" with no explicit unsupported claim list
