---
name: typescript-runtime-boundary-modeling
description: Own trust-boundary shaping in strict-mode TypeScript backends. Use whenever the task is about turning request, config, external API, database, cache, JSON, or caught-error data from `unknown` or weakly typed input into trusted internal types through parsing, validation, normalization, guards, schema-derived types, or boundary layering, even if the user only says "make this type-safe", "validate this payload", "clean up these casts", or "why is `unknown` leaking?"
---

# TypeScript Runtime Boundary Modeling

## Purpose

Own the narrow seam where runtime data stops being merely present and starts
being trustworthy.

This skill is about how untrusted or weakly typed values become trusted
internal representations through real runtime checks, normalization, and
explicit boundary placement.

It is not a general TypeScript style guide, not public API contract design,
not advanced type-level modeling after parsing, and not storage-engine
semantics.

Use it to reason like a boundary specialist:

- name the exact source of untrusted data
- name the exact point where trust changes
- define the smallest surface that must be runtime-checked before the next
  layer can rely on it
- choose a concrete parsing or validation shape instead of generic tooling
  slogans
- keep assumptions, confidence, and residual trust-leak risk explicit

## Specialist Stance

This skill should reason more narrowly and more rigorously about runtime
trust boundaries, not just repeat generic type-safety advice.

The durable advantage of this skill must come from forcing a better reasoning
path:

- smaller and more explicit trusted claims
- sharper separation between validated, normalized, and truly trusted shapes
- stricter rejection of accidental trust leakage
- explicit assumptions, confidence, and rejected shortcuts
- pressure-testing the boundary before accepting the first plausible parser

If a broad but competent TypeScript answer would still look interchangeable
with the result, this skill is not doing enough work.

## Expert Standard

Do not spend time restating that TypeScript types disappear at runtime or
that schema libraries exist.

The value of this skill is narrower and more defensible boundary judgment, not
broader TypeScript trivia.

Its job is to force deeper specialist thinking:

- do not say "use zod", "add types", or "validate it" without naming the
  exact boundary, trusted claim, unknown-key policy, and output shape
- do not say "treat it as `unknown`" unless you also say where it stops being
  `unknown`
- validate the exact surface the next layer relies on, not a smaller prefix
  and not an unjustifiably larger object
- keep "validated" separate from "normalized" and separate again from
  "trusted internal"
- say what is observed in the code or config versus what is inferred
- lower confidence when the real parser, `tsconfig`, lint rules, or data shape
  are not visible
- name the most tempting unsafe shortcut and explain why it leaks trust
- name the omission that matters most here:
  an over-trusted shape, an unspoken policy, or a boundary that is too wide

If the answer could be rewritten as a generic "TypeScript safety" blog post
with only small wording changes, it is still too shallow for this skill.

## Expert Target

Keep this skill durable over time.

That means:

- optimize for better boundary decisions, not for surprising factual trivia
- encode a disciplined reasoning sequence so important checks are harder to
  skip
- require the answer to expose the omitted trust claim, policy choice, or
  boundary edge
- make the result more falsifiable through exact trusted claims, policy
  choices, and rejected alternatives
- reject answers that are merely competent and broad when the skill can be
  narrow and exact

## Quality Bar

Reject vague or decorative guidance.

A good answer from this skill must:

- identify the primary boundary source:
  request, config, external API, persistence, cache, JSON parse, or `catch`
- state the trust transition in concrete terms:
  `untrusted -> validated -> normalized -> trusted internal`
- define the minimal checked surface that supports the trusted claim
- choose a concrete mechanism:
  manual guard, assertion function, schema-derived parser, or boundary mapper
- choose concrete policies when they matter:
  throw versus result, reject versus strip versus passthrough, sync versus
  async parse, transform location
- name the trusted output shape and which layer owns it
- call out at least one trust-leak risk, rejected shortcut, or hidden
  assumption
- compare the strongest tempting broader answer and explain why it still
  trusts too much, checks too little, or hides a key policy decision
- separate observed facts from assumptions and give an honest confidence level

If any of those are missing, the answer is probably merely topical, not
expert.

## Scope

- `unknown` versus `any` at runtime boundaries
- request, config, external API, persistence, cache, and `catch` as sources
  of untrusted values
- parser functions, guards, assertion functions, schema-derived validation,
  and normalization layers
- explicit separation of transport DTOs, records, cached shapes, and trusted
  internal representations
- unknown-key handling, transform placement, parse result shape, and boundary
  ownership
- strict compiler and lint guardrails only where they materially affect
  boundary honesty

## Read These References When You Need Them

- the required step-by-step design pass for this seam:
  `references/boundary-design-workflow.md`
- the compact trade-off guide for mechanism and policy choices:
  `references/policy-decision-guide.md`
- the concrete TS, lint, Node, and validator anchors that reject
  plausible-but-wrong boundary advice:
  `references/stack-specific-hard-anchors.md`
- the source-by-source default boundary map:
  `references/source-surface-matrix.md`
- concrete parser, guard, assertion, and normalization shapes:
  `references/parser-shape-rules.md`
- red flags that indicate accidental trust leakage:
  `references/trust-leak-smells.md`
- how to audit an unfamiliar repository for real trust boundaries:
  `references/unfamiliar-codebase-checklist.md`
- the pressure-test that turns a plausible answer into a stronger specialist
  answer:
  `references/reasoning-pressure-test.md`

## Relationship To Shared Research

Start with the local references in this skill.

Load `references/boundary-design-workflow.md` by default.

Load `references/reasoning-pressure-test.md` for every non-trivial task or
when the first draft feels plausible but too generic.

Load `references/policy-decision-guide.md` when the hard part is choosing
between guards versus schemas, throw versus result, reject versus strip, or
how much of the raw shape should become trusted.

Load `references/stack-specific-hard-anchors.md` when the recommendation turns
on concrete TypeScript compiler flags, `typescript-eslint` `no-unsafe-*`
guardrails, Node `process.env` behavior, `catch` variable semantics, or
validator-specific caveats like unknown-key defaults and transform or async
parse behavior.

Load the focused reference that matches the current question. Do not load
everything unless the task genuinely crosses several runtime-boundary sources.

Load `../_shared-hyperresearch/deep-researches/typescript-runtime-boundary-modeling.md`
only when:

- the task depends on version-sensitive TypeScript or validator semantics
- the local references are not enough to resolve a boundary decision
- the codebase is unfamiliar and you need the deeper investigation map
- the choice between manual guards, schema-derived parsing, and layered
  normalization is still ambiguous

Version anchor: TypeScript 5.9 strict-mode Node.js/backend code. If the repo
or task depends on a different TS version or a materially different runtime
stack, say so explicitly.

## Relationship To Neighbor Skills

- Use `typescript-language-core` when the main issue is ordinary narrowing,
  optionality, or `unknown` semantics without a real runtime-boundary design
  decision.
- Use `typescript-public-api-design` or `api-contract-designer-spec` when the
  hard question is which public request or response shape should exist, rather
  than how to make an already-chosen input trustworthy.
- Use `typescript-advanced-type-modeling` when the difficult work starts after
  normalization inside the trusted internal model.
- Use `prisma-postgresql-data-spec` when relational semantics, migrations, or
  query behavior dominate beyond generic record-to-internal shaping.
- Use `redis-runtime-spec` when cache semantics, TTLs, or Redis data behavior
  dominate beyond generic cache-value distrust.
- Use `external-integration-adapter-spec` when the real problem is provider
  adapter ownership rather than local parsing and trust conversion.

If a task crosses seams, keep this skill focused on trust conversion and hand
off the rest explicitly.

## Input Sufficiency

Before answering, identify the minimum missing facts:

- is this greenfield boundary design, refactor, or audit of existing code
- what is the real source surface and raw shape
- do you see the actual parser or only the symptom
- do you know the effective `tsconfig` and type-aware lint guardrails
- is the goal to trust the whole object or only a smaller internal claim

If those facts are missing, say what you are assuming and reduce confidence.
Do not talk as if the real boundary has been observed when it has not.

## Trust Model

Treat each value at a runtime boundary as moving through four states:

1. `Untrusted`
   Raw runtime data. This should usually be modeled as `unknown` or a weak raw
   shape.
2. `Validated`
   Structural checks have proved the fields and forms the next step depends on.
3. `Normalized`
   The validated data has been coerced, trimmed, defaulted, or mapped into the
   canonical local form.
4. `Trusted Internal`
   Internal code may rely on the shape and invariants that the boundary really
   established.

Important rule:

- "trusted" means "this exact claim was runtime-checked or produced by code
  that only runs after runtime-checks"
- it does not mean "we wrote an interface" or "TypeScript accepted the cast"

### Minimal Checked Surface

Use the smallest fully checked surface that the next layer actually relies on.

That means:

- if the next layer needs only `id`, `status`, and `expiresAt`, validate and
  normalize exactly that surface and keep the rest opaque
- if the next layer receives the full object as trusted internal state, then
  the full object must be checked according to the chosen policy
- do not validate a top-level object and then trust unvalidated nested fields

### Healthy Boundary Ownership

A healthy runtime boundary usually has:

- one obvious parser, decoder, or mapper entrypoint
- one obvious place where unknown-key or extra-shape policy is chosen
- normalization in the same boundary layer or immediately after structural
  validation
- a trusted output type that the core can consume without importing request
  DTOs, DB records, or cache wire shapes

## Workflow

### 1. Confirm Topic Fit

- decide whether the request is really about runtime trust conversion
- if the main problem is contract design, domain typing, or store semantics,
  hand off instead of stretching this skill

### 2. Locate The Real Boundary

Name:

- the source surface
- the raw form that enters
- the module or function where trust should change
- the layer that will consume the trusted output

Do not speak abstractly about "validation somewhere near the edge."

### 3. Define The Trusted Claim

Before choosing a tool, say exactly what the next layer is allowed to believe.

Examples:

- "service may rely on `port` as a normalized integer in range X"
- "domain code may rely on `email` and `role`, but raw provider metadata
  stays opaque"
- "cache reader may trust only the decoded envelope header, not the embedded
  payload"

### 4. Choose The Mechanism

Pick the smallest mechanism that can fully prove the trusted claim:

- manual guards for tiny, local, stable shapes
- assertion functions when failure should throw and the runtime proof is local
- schema-derived parsing when nesting, unknown-key policy, reuse, or clear
  trusted output matters
- explicit mappers when transport or record shapes must be separated from the
  trusted internal representation

Do not choose a library by brand recognition alone.

### 5. Choose The Boundary Policies

State the policy choices that affect real trust:

- `throw` versus structured result
- `reject`, `strip`, or `passthrough` for unknown keys
- sync versus async parsing when transforms or external checks exist
- where normalization happens and whether it is pure and centralized

If the answer does not name these choices where relevant, it is still too
hand-wavy.

### 6. Shape The Trusted Output

Define:

- the trusted output type or object shape
- whether it is DTO-like, record-like, or true internal representation
- which raw shapes remain outside the trusted zone
- whether core code can stay isolated from transport and persistence types

Prefer output signatures like:

- `parseX(input: unknown): TrustedX`
- `parseX(input: unknown): Result<TrustedX, Issues>`
- `assertX(input: unknown): asserts input is TrustedX`

Use `asserts` only when a real runtime proof happens inside that function.

### 7. Pressure-Test Trust Leakage

Before finalizing, ask:

- what fields are still untrusted?
- where could `any`, `!`, or `as unknown as` smuggle trust across the seam?
- are extra keys or nested values silently surviving without policy?
- is truthiness-based narrowing hiding valid empty values?
- is normalization happening ad hoc in several places instead of once?
- what observed facts support the answer, and what is still assumed?

### 8. Omission Check

State which boundary omission is still unresolved here, then state what it
would still miss:

- a trusted claim that is too wide for the proof
- a policy choice that stayed implicit
- a raw shape that leaked into core code
- a shortcut that looks clean but bypasses runtime evidence

If you cannot name that omission, the answer may still be too generic.

## Preferred Defaults

- treat every external value as `unknown` until a boundary parser proves
  otherwise
- keep one obvious parse or normalize entrypoint per boundary source
- prefer schema-derived parsing when the shape is nested, reused, or policy
  sensitive
- prefer manual guards only for small shapes where the full proof stays easy
  to review
- make unknown-key policy explicit
- keep transforms and defaults centralized in the boundary layer
- treat `process.env` as string input that must be parsed once at startup
- treat `catch (err)` as a boundary and narrow from `unknown`
- use strict compiler and `no-unsafe-*` lint rules as containment aids, not as
  substitutes for runtime checks

## Failure Smells

- `as any`, `as unknown as T`, or postfix `!` near external input
- a parser that checks the top-level object but trusts nested fields
- "we validate it in middleware" without naming the trusted output that leaves
  the middleware
- silent passthrough of extra keys without an intentional policy
- transforms that throw unexpectedly or run before structural assumptions are
  established
- domain or core modules importing transport DTOs or DB record types as if
  they were already trusted internal models
- config parsing spread across the codebase instead of one startup boundary
- `any` leaking from SDKs, JSON, cache reads, or third-party helpers into
  typed code

## Deliverable Shape

Design or audit answers should normally use this structure:

- `Boundary Source`
- `Observed Facts / Missing Facts`
- `Trust Transition`
- `Mechanism And Policies`
- `Trusted Internal Shape`
- `Trust-Leak Risks / Rejected Shortcut`
- `Confidence`

Inside `Mechanism And Policies`, explicitly cover:

- the parser or guard shape
- the checked surface
- unknown-key handling if relevant
- normalization location
- throw versus result behavior if relevant

## Escalate When

Escalate if:

- the real question is which public API contract should exist
- the trusted internal model needs advanced type-level design beyond the
  boundary
- persistence or cache semantics dominate the decision
- the recommended parser depends on library-specific performance or ecosystem
  trade-offs that are central to the answer
- the codebase hides the real parser, `tsconfig`, or lint boundary so heavily
  that confidence is low
