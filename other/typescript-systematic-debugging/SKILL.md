---
name: typescript-systematic-debugging
description: "Systematic root-cause investigation for TypeScript backends. Use whenever the task is to debug an incident, regression, flaky behavior, timeout, unexpected 4xx/5xx, stuck stream, worker failure, Redis or Prisma weirdness, or external-integration issue and the right move is to narrow the failure surface and choose the next diagnostic step instead of guessing a fix, even if the user asks 'why is this happening?', 'what should I check next?', or proposes a patch too early."
---

# TypeScript Systematic Debugging

## Purpose

Apply a disciplined debugging method across the runtime, data, integration,
streaming, reliability, performance, and observability surfaces used in this
repository.

This skill is a narrow `workflow-meta` specialist. It does not own broad
architecture, review, or implementation work. Its job is to turn symptoms
into:

- a named failure surface
- a small set of competing mechanisms
- the best next diagnostic step
- an explicit bar for when "root cause" is justified

When used from a project agent, let the agent own scope, handoffs, and final
decisions. This skill owns the debugging method only.

## Expert Standard

Do not spend time restating common debugging advice.

Strong models will already know the generic moves:

- reproduce the issue
- inspect logs
- check recent changes
- form hypotheses

That is not the value of this skill.

The value of this skill is narrower and deeper reasoning:

- identify the first plausible bad boundary instead of narrating the whole
  stack
- separate neighboring failure classes that are easy to conflate
- choose the one next diagnostic step with the highest discriminating power
- keep the failure surface shrinking after each observation
- withhold fix direction until the mechanism has defeated the strongest nearby
  explanation
- keep the answer compact, operational, and hard to fool

If the answer could be rewritten as a generic debugging checklist with only
small wording changes, it is still too shallow for this skill.

## Read These References When You Need Them

- `references/investigation-checklist.md`
  Use when the symptom is still vague, the codebase is unfamiliar, or the
  prompt starts with only a failure report instead of a localized seam.
- `references/confusion-pairs.md`
  Use when the first explanation sounds plausible but could easily be the wrong
  neighboring failure class.
- `references/next-step-selection.md`
  Use when several probes are possible and the main job is choosing the one
  diagnostic step that best separates the live hypotheses.
- `references/root-cause-quality-bar.md`
  Use when deciding whether the answer supports only triage, a leading
  hypothesis, a measurement gap, or a real root-cause claim.
- `references/stack-specific-hard-anchors.md`
  Use when two theories are both plausible and the diagnosis turns on concrete
  Fastify, Prisma/PostgreSQL, Redis, outbound HTTP, streaming, timeout,
  readiness, or event-loop facts rather than method alone.

## Relationship To Shared Research

Start with the local method and references in this skill.

This skill should not own a separate umbrella deep-research prompt.

Load `references/investigation-checklist.md` by default when the issue is not
already localized.

Load `references/confusion-pairs.md` for every non-trivial debugging task or
when the first theory feels plausible but unproven.

Load `references/next-step-selection.md` when the main risk is wasting time on
low-discrimination checks or multi-variable experiments.

Load `references/root-cause-quality-bar.md` before calling something root
cause, before suggesting a fix, or when deciding whether the honest output is
still a triage plan.

Load `references/stack-specific-hard-anchors.md` when the next narrowing step
depends on concrete runtime semantics and a wrong assumption about the stack
would send the investigation in the wrong direction.

Then load only the shared topic files that match the currently suspected
surface:

- `../_shared-hyperresearch/deep-researches/fastify-runtime.md`
  Use for request lifecycle, hook order, decorator scope, reply ownership, and
  startup versus request-path failures.
- `../_shared-hyperresearch/deep-researches/prisma-postgresql.md`
  Use for query shape, pool wait, transactions, migrations, locking, ordering,
  and data-shape issues.
- `../_shared-hyperresearch/deep-researches/redis-runtime.md`
  Use for readiness, reconnect, TTL/state protocol, scripts, parser or reply
  shape, and key-design bugs.
- `../_shared-hyperresearch/deep-researches/external-integration-adapter.md`
  Use for outbound timeout, retry, transport, error mapping, parse, or
  provider-drift issues.
- `../_shared-hyperresearch/deep-researches/streaming-workers.md`
  Use for streaming lifecycle, abort, backpressure, queueing, worker pools,
  and response ownership.
- `../_shared-hyperresearch/deep-researches/node-reliability.md`
  Use for deadline propagation, retries, readiness, shutdown, overload, and
  failure amplification.
- `../_shared-hyperresearch/deep-researches/node-performance.md`
  Use for bottleneck localization, queueing chains, event-loop or worker-pool
  contention, Prisma wait, Redis RTT, and serialization cost.
- `../_shared-hyperresearch/deep-researches/node-observability.md`
  Use for signal ownership, missing or misleading telemetry, and choosing the
  next probe.

Do not load all topics by default. Start with the most likely seam plus one
adjacent seam only when the evidence crosses a boundary.

## Scope

- debug incidents, regressions, flaky behavior, and unexpected runtime
  behavior in the TypeScript backend stack
- narrow the failure surface across HTTP, DB, Redis, outbound calls,
  streaming, workers, startup, and shutdown
- choose the next diagnostic step that best separates plausible mechanisms
- state what is known, what is inferred, and what still needs proof
- decide when the evidence is strong enough to call something root cause

## Boundaries

Do not:

- guess fixes from the first plausible story
- turn the answer into a redesign or refactor plan
- treat symptoms, logs, or stack traces as full mechanism without boundary
  reasoning
- change several variables at once just to "see if it helps"
- recommend timeout, retry, cache, worker, schema, or pool changes before the
  failing surface is localized
- load every shared topic "for completeness"

## Escalate When

Escalate if:

- the issue is already localized and the real task is design, review, or code
  implementation rather than debugging
- the dominant question is observability design, performance planning, or
  reliability policy rather than root-cause isolation
- the evidence is so thin that the honest answer is a triage plan instead of a
  root-cause claim
- the task becomes primarily security, product, or rollout analysis

## Input Sufficiency

Before answering, identify the minimum known facts:

- what breaks and who feels it
- the first known failing phase:
  startup, request path, background work, streaming connection, or shutdown
- deterministic, intermittent, load-sensitive, deploy-sensitive, or
  data-dependent behavior
- the last known good signal and first bad signal
- which surfaces are plausibly touched:
  Fastify, Prisma/PostgreSQL, Redis, external integrations,
  streaming/workers, reliability, performance, observability
- what evidence already exists:
  repro steps, logs, traces, query data, metrics, recent diffs, timestamps

If those facts are missing, say so explicitly and lower confidence. Do not
invent environment details, workload shape, or runtime behavior.

## Core Defaults

- Symptoms are not mechanisms.
- One narrowed branch is better than five guesses.
- Prefer observation before mutation.
- Prefer one-variable-at-a-time checks.
- Prefer the diagnostic step that best separates the top hypotheses with the
  least blast radius.
- Keep facts, inferences, assumptions, and open questions separate.
- Lower confidence when the mechanism, trigger, or boundary is still inferred.
- Do not call something root cause until the nearby alternatives have been
  pressured.
- Prefer a more discriminating next step over a more comprehensive one.
- Prefer seam-local reasoning over stack-wide storytelling.
- Prefer killing the strongest wrong theory over collecting more plausible
  but non-separating detail.

## Workflow

1. Normalize the failure.
   - Rewrite the problem as what breaks, where, when, how often, and for whom.
   - Distinguish startup, request-path, streaming, background, and shutdown
     failures.
   - Note whether the issue is deterministic, intermittent, load-sensitive,
     deploy-sensitive, or data-dependent.
2. Classify the first likely failure surface.
   - Fastify lifecycle or decorator scope
   - Prisma/PostgreSQL query, pool, transaction, migration, or data shape
   - Redis runtime state, TTL, Lua/script, key, readiness, or reconnect
   - External integration transport, timeout, retry, mapping, or parsing
   - Streaming or worker lifecycle, abort, backpressure, queue, or ownership
   - Reliability budget, retry storm, readiness, shutdown, or degradation
   - Performance bottleneck or hidden queue
   - Observability gap or misleading signal
3. Draw the minimal causal path.
   - Name the path from trigger to failure.
   - Mark handoffs, state transitions, and external boundaries.
   - Identify the last point believed good and the first point believed bad.
4. Inventory evidence.
   - Separate hard facts from interpretation.
   - Note which evidence is direct, indirect, stale, conflicting, or missing.
   - If the codebase is unfamiliar, inspect the narrowest seam that could
     plausibly own the failure before widening search.
5. Build competing hypotheses.
   - Keep `2-4` live hypotheses.
   - For each one, state:
     mechanism, expected evidence, strongest counter-signal, and cheapest
     discriminator.
   - Reject hypotheses that do not explain the observed timing, scope, or
     boundary.
6. Choose the next diagnostic step.
   Pick the step that separates the current hypotheses while changing the least.
   Good next steps usually do one of:
   - confirm the failing lifecycle phase
   - compare queue wait versus execution time
   - distinguish network failure from HTTP error
   - distinguish client abort from server stall
   - distinguish missing signal from missing behavior
   - verify one boundary contract or state transition
7. Update the failure surface.
   - After each new observation, retire disproven branches.
   - Shrink the suspected surface explicitly.
   - If the surface widens instead of narrows, say why and load the next
     adjacent topic deliberately.
8. Cross the root-cause threshold only when all are true.
   - the failing surface is named precisely
   - the mechanism explains the symptom and timing
   - the trigger or precondition is identified
   - the nearby alternative explanations were addressed
   - the claim predicts what a confirming or disconfirming check should show
9. Only then mention fix direction.
   - Keep it minimal and surface-local.
   - Pair it with a validation step that would confirm the mechanism, not just
     silence the symptom.

## Reasoning Obligations

For any non-trivial debugging task, force all of these before sounding
confident:

- `Primary Failure Story`
  Name the currently leading mechanism and the first bad boundary or state
  transition.
- `Strongest Alternative`
  Name the neighboring explanation that a smart debugger could confuse with
  the primary one.
- `Why The Primary Wins`
  Explain what concrete observation currently favors the primary story.
- `What Would Falsify It`
  Name the observation that would demote or kill the current theory.
- `Next Step Value`
  Explain why the chosen next step separates the hypotheses better than the
  obvious alternatives.

If one of those is missing, lower confidence or stay at triage/hypothesis
rather than calling root cause.

## Cross-Domain Routing Cues

### Fastify Runtime

- Distinguish startup-time registration or decorator problems from request
  lifecycle failures.
- Hook order matters:
  `onRequest -> preParsing -> parsing -> preValidation -> validation -> preHandler -> handler -> preSerialization -> onSend -> onResponse`.
- Treat `async` plus `done`, early `reply.send`, raw-body reads, and decorator
  scope as separate failure classes.

### Prisma / PostgreSQL

- Distinguish Prisma pool wait from slow SQL.
- Distinguish transaction or locking problems from data-shape or query-shape
  regressions.
- Treat migration drift, unstable ordering, JSON null semantics, and
  retry/isolation behavior as different classes of failure.

### Redis Runtime

- Distinguish client readiness or reconnect issues from key or protocol logic
  bugs.
- Treat TTL as protocol state, not cleanup trivia.
- For scripts and guards, verify real reply shapes and truthiness semantics
  rather than assuming string `'OK'`.

### External Integrations

- Distinguish network failure, timeout, cancellation, HTTP error response,
  parse failure, and provider semantic rejection.
- Keep retry ownership and idempotency explicit before blaming the provider or
  adapter.

### Streaming / Workers

- Distinguish client abort, server stall, backpressure, queue growth, worker
  saturation, and response-ownership bugs.
- `reply.send()` plus manual writes, ignored `write() -> false`, and missing
  abort cleanup are different mechanisms, not one generic "streaming bug."

### Reliability

- Distinguish the original failure from amplification caused by retries,
  hidden queues, long transactions, overload, bad readiness, or shutdown
  behavior.
- Treat deadline propagation and cancellation gaps as debugging surfaces, not
  only future hardening work.

### Performance

- Distinguish symptom from bottleneck.
- Event loop, libuv worker pool, Prisma wait, PostgreSQL execution, Redis RTT,
  serialization or logging, and streaming backpressure are different queueing
  surfaces.

### Observability

- Distinguish "the system is not telling us" from "the system is doing the
  wrong thing."
- Choose the next probe by question and truth owner, not by spraying random
  logs everywhere.

## Quality Bar

A strong debugging answer should leave the reader with:

- a named failure surface, not only a symptom summary
- a compact set of live hypotheses, not a brainstorm dump
- one recommended next diagnostic step
- the reason that step best separates the current hypotheses
- the strongest nearby explanation and why it currently loses
- explicit assumptions and confidence
- a clear statement of what not to do yet

Reject answers that sound like:

- "Maybe increase the timeout."
- "Add retries and see."
- "It is probably Prisma."
- "Check the logs."
- "Let's rewrite this flow."

Those may become valid later, but not before the failure surface is narrowed.

## Deliverable Shape

Return debugging help in this order:

- `Symptom`
- `Failure Surface`
- `Known Facts`
- `Leading Hypotheses`
- `Next Diagnostic Step`
- `Why This Step`
- `Assumptions / Confidence`
- `Do Not Do Yet`

Add these only when evidence supports them:

- `Disproved Branches`
- `Confirmed Root Cause`
- `Minimal Fix Direction`
- `Validation After Fix`

## Escalate Or Reject

- a user-proposed fix being treated as proof of mechanism
- cross-domain symptoms being collapsed into one vague "infra issue"
- root-cause claims that cannot name the first bad boundary or state transition
- shotgun debugging plans that change several variables at once
- architecture advice that appears before the next discriminating check is
  chosen
