---
name: technical-design-review
description: "Read-only technical design review for TypeScript/Node backends. Use whenever the task is to review an RFC, spec, design doc, ADR, refactor plan, or architecture proposal for ownership seams, trade-offs, and missing proof; start from architecture and only pull in contract, runtime, data, reliability, security, performance, or test-proof topics when the design actually crosses them, even if the user only asks for a quick design sanity check."
---

# Technical Design Review

Use this skill for read-only review of technical designs in this repository's
backend stack.

This is a dynamic-composite consumer lens. Do not restate the shared topic
research. The job is to review the proposed design more sharply than a generic
architecture critique would:

- start from architecture
- activate only the seams the design really touches
- surface the smallest set of material findings
- separate true flaws from explicit trade-offs and missing proof
- keep confidence and assumptions honest

## Expert Standard

Do not spend time retelling the usual architecture advice.

Do not spend time restating common patterns or adjacent-stack basics.

This skill must stay better than a generic architecture review.
It wins by being narrower, deeper, and more disciplined:

- name the concrete seam where the design becomes risky or unclear
- identify the exact guarantee the design is trying to preserve
- expose the strongest nearby failure story or competing interpretation
- show whether the current design already defeats that story
- distinguish a true design flaw from a deliberate trade-off
- distinguish a trade-off from a missing-proof obligation
- recommend the smallest design correction or next proof step
- state assumptions and confidence explicitly when evidence is partial

The value is not extra trivia.
The value is tighter seam selection, stronger discrimination between flaw
versus trade-off versus missing proof, and sharper review pressure than a
broad first-pass review will apply consistently by default.

If the review would still read the same after replacing the design with "some
backend proposal", or if it mainly repeats generally-known architecture
guidance, it is too generic for this skill.

## Relationship To Shared Research

Start from the local references in this skill.

Load `references/review-workflow.md` by default.

Load `references/seam-activation-matrix.md` when deciding which adjacent topics
the design actually activates.

Load `references/finding-calibration.md` when the draft review feels right but
the point classification is still fuzzy.

Load `references/design-pressure-test.md` when the draft sounds plausible but
has not yet beaten the strongest nearby alternative or named the missing proof
cleanly.

Load `references/architecture-hard-anchors.md` when the verdict depends on
exact architecture invariants such as composition-root ownership, dependency
publication, config or error boundaries, transport contamination, or Node ESM
run-correctness.

Load `references/stack-specific-hard-anchors.md` when the verdict depends on
exact Fastify, TypeBox, Prisma, PostgreSQL, Redis, or Vitest semantics rather
than on abstract architecture reasoning alone.

Start every real review from
`../_shared-hyperresearch/deep-researches/ts-backend-architecture.md`.

Load additional shared deep research only when the design crosses that seam:

- `api-contract`
  for request or response shapes, schema ownership, compatibility, serializer
  or publication drift
- `fastify-runtime`
  for hook placement, decorator scope, lifecycle, streaming, or error-handler
  behavior
- `prisma-postgresql`
  for migrations, data ownership, query shape, transaction scope, or
  database-backed guarantees
- `redis-runtime`
  for cache or coordination semantics, TTL, Lua, queue-like runtime state, or
  replay-sensitive Redis behavior
- `node-reliability`
  for deadlines, retries, degradation, shutdown, backlog, recovery, or replay
  semantics
- `node-security`
  for trust boundaries, auth, secrets, outbound HTTP, unsafe exposure, or
  fail-open posture
- `node-performance`
  for queueing, pool contention, payload cost, backpressure, or measurement
  sensitive bottlenecks
- `vitest-qa`
  when the design's credibility depends on a proof plan, test layer choice, or
  claimed regression coverage

Do not load untouched topics for completeness.
Do not turn the skill into a second umbrella hyperresearch prompt.

## Relationship To Neighbor Skills

- Use `ts-backend-architect-spec` when the main task is producing design
  decisions rather than reviewing them.
- Use single-topic review skills such as `api-contract-review`,
  `fastify-runtime-review`, `prisma-postgresql-review`, `redis-runtime-review`,
  `node-reliability-review`, `node-security-review`, `node-performance-review`,
  or `vitest-qa-review` when one seam clearly dominates and deeper specialist
  detail matters more than cross-seam synthesis.
- Use `typescript-coder-plan-spec` when the main task is producing an ordered
  implementation plan.
- Use `typescript-coder` when the main task is implementation.
- Use `verification-before-completion` when the question is proof sufficiency
  before closeout rather than design quality itself.

If a task crosses seams, keep this skill at design-review scope and hand off
implementation or single-topic deep dives explicitly.

## Use This Skill For

- reviewing RFCs, ADRs, specs, or design docs before implementation
- critiquing refactor plans and architecture proposals across multiple backend
  seams
- pressure-testing ownership boundaries, dependency direction, contract
  integrity, state boundaries, and failure semantics
- finding where a design relies on an unproven assumption or an under-specified
  proving strategy
- checking whether a proposed trade-off is explicit, bounded, and justified

## Input Sufficiency Check

Do not fake a design review from one vague sentence.

Before making strong claims, confirm what concrete design surface you actually
have:

- a spec or design doc
- an ADR or decision memo
- interface or schema sketches
- a flow description
- a migration or state-transition plan
- a proof or test plan

If that material is missing, say what is missing and downgrade the result to
`missing proof` or `open design question` instead of inventing design detail.

## Review Workflow

1. Frame the design before judging it.
   - What is changing?
   - What problem is it solving?
   - What constraints, non-goals, and rollout assumptions matter?
2. Start from the architecture base.
   - ownership and module seams
   - dependency direction
   - composition-root implications
   - config and error boundaries
   - publication surface of the changed modules
3. Activate only the touched adjacent seams.
   - Use `references/seam-activation-matrix.md`.
   - Do not load topic packs that the current design does not need.
4. For each active seam, ask the same design-review questions.
   - What guarantee is the design trying to preserve?
   - What strongest nearby failure story or conflicting interpretation could
     still break it?
   - What trade-off is being chosen?
   - What proof is still missing before this should be treated as ready?
5. Classify every material point before writing it up.
   - `finding`
   - `trade-off`
   - `missing proof`
   - `acceptable assumption`
6. Emit only high-signal output.
   - Prefer `specific seam -> consequence -> smallest correction or next proof
step -> confidence`.
   - If no material findings survive the bar, say so and list only residual
     trade-offs or proof obligations.
7. Keep the review read-only.
   - Do not rewrite the design from scratch unless the current design is
     unsalvageable and the smallest safe correction is still structural.

Use `references/review-workflow.md` when the design is broad or unfamiliar.
Use `references/finding-calibration.md` when the first draft has the right
topics but weak point classification.
Use `references/design-pressure-test.md` when the draft has not yet defeated
the strongest alternative story or named what evidence would change the
verdict.
Use `references/architecture-hard-anchors.md` when the draft depends on
concrete architecture boundary semantics such as `process.env` leakage,
service-locator wiring, `FastifyRequest` in the service layer, unstable deep
imports, or Node ESM module-resolution assumptions that would change the
design verdict.
Use `references/stack-specific-hard-anchors.md` when the draft depends on
concrete stack semantics such as `inject()` versus `listen()`, response-schema
serialization boundaries, migration safety around uniqueness or `TRUNCATE`,
Redis replay semantics, or timeout and queue behavior that would change the
design verdict.

## High-Discipline Reasoning Obligations

Before finalizing a material point, make the review clear this bar:

1. `Primary Seam`
   - Name the exact architecture or adjacent seam involved.
2. `Claimed Design Guarantee`
   - State what the design appears to promise.
3. `Strongest Alternative Story`
   - Name the nearest failure mode, ownership conflict, or under-specified
     interpretation that could still make the design unsafe or incoherent.
4. `Why The Current Design Does Or Does Not Beat It`
   - Use the available evidence from the design itself.
5. `Point Class`
   - Is this a finding, trade-off, missing proof, or acceptable assumption?
6. `Smallest Useful Response`
   - Name the narrowest design correction or next proof step that would
     materially improve confidence.
7. `Confidence Boundary`
   - Say what is observed directly, what is inferred, and what evidence would
     upgrade or downgrade the verdict.

If a candidate point cannot survive those passes, drop it or demote it.

## Review Quality Bar

Keep a point only if all are true:

- the seam and affected design surface are specific
- the broken or weakened guarantee is explicit
- the nearest alternative story has been challenged
- the point stays inside design-review scope rather than drifting into code
  authorship
- the smallest correction or next proof step is identifiable
- confidence and assumptions are honest

Reject these weak patterns:

- "split this into more services"
- "add caching"
- "needs better abstractions"
- "write more tests"
- "watch reliability/security/performance here"

Those are not design-review findings unless the review proves the exact seam,
the consequence, and the smallest safe correction.

## Boundaries

Do not:

- write implementation steps or code
- restate the shared research base locally
- widen into product or business-policy review
- invent numeric limits, timeout values, pool sizes, or rollout policies
  without evidence
- load every adjacent topic "just in case"
- force findings when the real outcome is a bounded trade-off or a missing
  proof obligation
