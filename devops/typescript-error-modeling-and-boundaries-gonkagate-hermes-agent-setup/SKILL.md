---
name: typescript-error-modeling-and-boundaries
description: Own internal error architecture and boundary design in strict-mode TypeScript backends. Use whenever the task is about choosing between exceptions, explicit error values, or nullable returns; stabilizing error identity with `code` or `kind`; preserving context with `cause`; or deciding where infrastructure failures should be enriched, translated, and shaped for callers, even if the user frames it as "clean up error handling", "should this throw?", "why are we matching messages?", or "where should this become AppError?"
---

# TypeScript Error Modeling And Boundaries

## Purpose

Own the narrow seam of internal error architecture in modern TypeScript
backends.

This skill is about how failure is represented, identified, preserved, and
translated as it crosses internal boundaries.

It owns:

- when a path should `throw`, reject, return an explicit error value, or use a
  nullable absence result
- how error identity should stay stable through `code`, `kind`, or another
  discriminant instead of message matching
- where errors should be created, where they should be enriched with context,
  where they should be translated across layers, and where they should be
  shaped for callers
- how `cause`, caught-`unknown` normalization, and Node delivery boundaries
  affect correct internal error design

It is not a generic "error handling" style guide, not a `neverthrow`
mechanics skill, not a runtime-validation skill, and not the owner of public
API error-envelope design.

Use it to reason like a boundary specialist:

- split failure families before choosing mechanics
- assign owners for create, enrich, translate, and shape
- keep stable identity separate from human-readable messages
- preserve useful cause and context without noise
- make handoffs to adjacent skills explicit instead of absorbing them
- make the tempting shortcut lose for a concrete reason

## Specialist Stance

Do not spend time repeating broad exception folklore.

The goal of this skill is to be more discriminating inside one seam:

- sharper on what kind of failure is happening
- sharper on which boundary owns the next translation
- sharper on what the stable identifier is
- sharper on how context is preserved without over-wrapping
- sharper on where Node delivery mechanics change the design

If removing this skill would leave the answer looking like generic
"error-handling best practices", the skill is not doing enough work.

## Expert Target

Design this skill to stay narrow and durable inside this seam.

That means:

- do not try to win with a broader survey of familiar error advice
- do not try to win by being longer, stricter-sounding, or more exhaustive
- do not rely on trivia, jargon density, or generic custom-error enthusiasm
- win by enforcing a narrower and more falsifiable reasoning path

The durable advantage of this skill must come from better seam judgment:

- forcing a real failure-family split before mechanism choice
- forcing explicit create, enrich, translate, and shape ownership
- forcing stable identity over message matching
- forcing delivery-boundary awareness where sync-only reasoning would fail
- forcing one rejected shortcut to lose explicitly

The skill is doing its job when it produces a sharper boundary decision,
catches a real trap, or rejects a weak abstraction. "More complete" is not
enough.

## Quality Bar

Reject vague error prose.

A good answer from this skill must:

- classify each recommendation as one of:
  - stable boundary principle
  - repo-local default
  - context-shaped preference
  - out-of-scope handoff
- identify the relevant failure families:
  programmer bug, operational failure, expected branching outcome,
  cancellation or abort when relevant
- choose one primary signal form for each family and explain why the tempting
  alternative loses here
- name the stable identity field:
  `code`, `kind`, or another discriminant
- treat `message` as human-readable text rather than the machine contract
- assign ownership for:
  create, enrich, translate, and shape
- say how caught `unknown` values are normalized and how `cause` is preserved
- call out at least one delivery-boundary risk:
  promise rejection, floating promise, EventEmitter or stream `'error'`,
  swallow-to-null, or over-wrapping
- separate observed facts from assumptions and lower confidence when runtime,
  compiler, or framework behavior is inferred
- surface a sharper boundary decision or a rejected shortcut that stayed
  implicit
- catch a concrete trap, reject a weak boundary, or produce a more stable
  outward contract

If the answer could be summarized as "use custom errors and do not throw
strings", it is not yet expert enough.

## Differentiation Test

Before trusting the answer, identify the tempting broad recommendation that
still feels plausible.

Then make the skill reject or refine it in a concrete way:

- sharper failure-family split
- clearer create, enrich, translate, and shape ownership
- more honest nullable-versus-error-value decision
- more explicit delivery-boundary risk
- clearer stable identity and discarded alternatives

If the answer is merely broader, more polished, or more complete, but not more
discriminating, it is not yet good enough.

## Scope

- choosing between exceptions, explicit error values, and nullable returns
- designing stable internal error identity with `code`, `kind`, or similar
  discriminants
- choosing between error classes and discriminated error values
- preserving cause and useful context through wrapping
- deciding where infrastructure failures become domain or application failures
- deciding where internal failures become caller-facing shapes
- handling caught `unknown` values and Node delivery boundaries as part of
  correct internal error design

## Expertise

### Failure-Family Split

- treat programmer bugs and invariant violations differently from expected
  business or application outcomes
- keep operational infrastructure failures distinct from expected branching
  outcomes
- treat cancellation or abort as its own outcome when the caller or runtime
  cares about it
- reject one-mechanism-for-everything answers

### Signal-Form Discipline

- use exceptions or rejected promises for failures that should abort the
  current operation and are not part of the ordinary branching contract
- use explicit error values when the caller is supposed to branch on the
  outcome as part of normal control flow
- allow `null` or `undefined` only when absence is the sole expected
  non-success branch and the caller does not need reason, identity, or context
- reject silent `catch { return null; }` translations that destroy causality

### Identity And Context Discipline

- keep machine identity on `code`, `kind`, or another stable discriminant
- treat `message` as mutable human text, not a protocol
- never match runtime behavior on message strings when a stable identifier can
  exist
- normalize caught `unknown` close to the boundary instead of letting raw
  thrown values drift upward
- use `cause` when adding new operational context, not as a reason to wrap on
  every layer

### Boundary Ownership

- create an error where the primary failure is understood
- enrich an error where new operation-specific context becomes known
- translate an error when layer responsibility or audience changes
- shape an error where a caller-facing contract begins
- in this repo, expected failures may stay explicit inside services or utils
  and become `AppError` at route or handler boundaries; final `/v1*` or
  `/api*` envelope shaping is a transport handoff, not this skill's primary
  ownership

### Delivery-Boundary Discipline

- include promise rejection behavior in the design, not just sync `throw`
- include EventEmitter or stream `'error'` strategy when those surfaces exist
- reject boundary designs that assume `try/catch` covers later event delivery
- reject floating promises when their failure path still matters to the
  operation

## Read These References When You Need Them

- the step-by-step workflow for designing or auditing this seam:
  `references/boundary-design-workflow.md`
- choosing between `throw`, explicit error values, nullable returns, and stable
  identity fields:
  `references/signal-selection-and-identity.md`
- create, enrich, translate, shape, and repo-local handoff defaults:
  `references/layer-translation-and-shaping.md`
- caught-`unknown` normalization, `cause`, promise rejection, emitter or stream
  delivery, and version-sensitive Node details:
  `references/delivery-boundaries-and-context.md`
- concrete TypeScript and Node hard anchors that materially change boundary
  recommendations in real code:
  `references/stack-specific-hard-anchors.md`
- auditing an existing repository to find the real error boundaries, identity
  rules, and translation seams before proposing changes:
  `references/unfamiliar-codebase-checklist.md`
- pressure-testing a plausible answer until it is clearly better than generic
  error advice:
  `references/reasoning-pressure-test.md`

## Relationship To Shared Research

Start with this skill file and its local references.

Load `references/boundary-design-workflow.md` by default.

Load `references/unfamiliar-codebase-checklist.md` when the task is an audit,
refactor, or "why is our error handling messy?" investigation over an existing
codebase.

Load `references/stack-specific-hard-anchors.md` when the recommendation turns
on concrete TS or Node behavior rather than only on abstract boundary rules:
`useUnknownInCatchVariables`, `ErrorOptions` and `cause`, `SystemError`
translation fields, `DOMException` identity, EventEmitter `'error'`,
unhandled rejections, source maps, native TS execution, or Node-version
differences around `Error.isError`.

Load `references/reasoning-pressure-test.md` for every non-trivial task or
when the first draft still feels like broad error-handling advice.

Load the shared deep research:
`../_shared-hyperresearch/deep-researches/typescript-error-modeling-and-boundaries.md`
only when:

- the task depends on version-sensitive Node or TypeScript behavior
- the codebase is unfamiliar and the local references are not enough
- the boundary decision remains ambiguous after the local workflow pass
- you need deeper nuance on `cause`, Node delivery semantics, or error-family
  defaults

Version anchor:
the shared research is anchored on TypeScript 5.9 and Node.js 24 LTS+.
This repo's default context is TypeScript 5.x on Node.js 20+ LTS.
Most boundary guidance is durable across that gap, but version-sensitive
details such as `Error.isError`, native TypeScript execution behavior, and
some runtime defaults must be verified before they are treated as facts.

## Relationship To Neighbor Skills

- Use `typescript-result-error-flow-neverthrow` when the main issue is
  `Result`, `ResultAsync`, combinator choice, or where `neverthrow` flow should
  begin and end.
- Use `typescript-runtime-boundary-modeling` when the main issue is runtime
  parsing, validation, normalization, or trust conversion from `unknown` into
  trusted internal types.
- Use `typescript-language-core` when the question is mostly about `unknown` in
  `catch`, narrowing, or ordinary TypeScript semantics without a real
  architecture decision.
- Use `typescript-public-api-design` or `api-contract-designer-spec` when the
  main issue is public error envelopes, response contracts, or published API
  compatibility.
- Use `fastify-runtime-review` when the hard part is Fastify error-handler or
  hook behavior rather than the internal error model itself.
- Use `node-reliability-spec` or `node-reliability-review` when the hard part
  is crash policy, retries, degraded mode, or lifecycle behavior beyond local
  error-boundary design.

If a task crosses seams, keep this skill focused on internal error modeling
and hand off the rest explicitly.

## Input Sufficiency And Confidence

Before answering, identify the minimum missing facts:

- is this greenfield boundary design, a refactor, or an audit of existing code
- what are the current layers:
  infrastructure, domain or application, transport, worker, or stream
- what kinds of failures are expected to be part of normal branching
- what is the current stable identity shape, if any
- where does caller-facing shaping happen today
- which delivery styles exist:
  sync throw, promise rejection, callback, EventEmitter, stream
- what TypeScript and Node version facts are actually visible

If those facts are missing, say what you are assuming and reduce confidence.
Do not talk as if the real boundary behavior was observed when it was not.

## Workflow

### 1. Confirm Topic Fit

- decide whether the task is truly about internal error architecture and
  boundary design
- if the real question is public transport shape, `neverthrow` mechanics, or
  runtime validation policy, hand off instead of stretching this skill

### 2. Map The Boundaries

Name the relevant boundaries before recommending a mechanism:

- layer boundaries:
  infrastructure, domain or application, transport
- delivery boundaries:
  sync `throw`, promise rejection, callback, EventEmitter, stream
- audience boundaries:
  internal diagnosis, internal caller, external caller

### 3. Split The Failure Families

For the touched path, classify each important failure as:

- programmer bug or invariant violation
- operational infrastructure failure
- expected branching outcome
- cancellation or abort

Do not choose `throw` versus error value before this split is explicit.

### 4. Choose Signal Form And Identity

For each family:

- choose the primary signal:
  exception, rejected promise, explicit error value, or nullable absence
- choose the stable identifier:
  `code`, `kind`, or another discriminant
- say why the tempting alternative is weaker here

### 5. Assign Ownership

For each boundary, say who owns:

- create
- enrich
- translate
- shape

If the code is in this repo, be explicit about the local default:
services or utils may keep expected failures explicit, route or handler
boundaries may convert them to `AppError`, and transport surfaces own the final
OpenAI-compatible or standard envelope.

### 6. Pressure-Test The Shortcut

Before finalizing the answer, identify the strongest tempting shortcut and make
it lose:

- message matching
- `catch { return null; }`
- wrapping every layer with "Failed to X"
- using exceptions for expected branching
- leaking raw infrastructure errors into outward contracts
- assuming `try/catch` covers promise or emitter delivery later

## Deliverable Shape

For a concrete task, return:

- `Boundary Map`
- `Failure Families`
- `Signal Form`
- `Identity / Context`
- `Layer Translation`
- `Caller Shape / Handoffs`
- `Rejected Shortcuts / Risks`
- `Assumptions / Confidence`
