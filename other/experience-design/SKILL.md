---
name: experience-design
description: "Own product experience decisions for client surfaces: user jobs, information architecture, routes and navigation intent, screen inventory, content priority, workflows, visible states, recovery, and microcopy. Use directly for read-only UX audits or focused experience deltas; product-craft routes new or materially changed surfaces here before interface design."
argument-hint: "[audit | delta | experience request]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
disable-model-invocation: false
---

# Experience Design

Define the experience before deciding its visual expression. Own only the experience sections of the canonical `design-contract.md`; do not choose art direction, visual tokens, component appearance, or durable product code.

Task: $ARGUMENTS (if empty, infer the experience outcome from the request)

## Routing Precedence

1. PR, diff, or review feedback → `code-review`; stop this skill.
2. Confirmation of a completed feature → `verify`; stop this skill.
3. Read-only IA, navigation, workflow, state, recovery, or microcopy critique → run `audit` here.
4. New or materially changed product surface → `product-craft` owns orchestration and selects the contract depth before this stage.
5. A change limited to experience-owned sections of an approved contract → run `delta` here.
6. Whenever `design` independently triggers, finish the required experience/interface gates before technical planning; no durable write occurs here.

Parallel sub-agents may assist only below the selected owner. They never own an experience decision.

## Modes

Default behavior is verb-free: infer the smallest applicable path.

- `audit` — inspect an existing experience and report evidence-backed findings. Read-only; findings do not authorize a delta or source edits.
- `delta` — propose changes only to named experience-owned contract sections. Preserve every unaffected section.
- Default — produce the Seed or Full experience baseline requested by product-craft.

## Owned Contract Sections

- Product Context
- UX Model
- Data & State Model
- Interaction Model
- Microcopy

User-facing route intent belongs to UX Model. Framework routing topology, data architecture, global state ownership, persistence, dependencies, and infrastructure belong to the general `design` workflow.

## Required Context

Read only what the selected depth needs:

1. Nearest applicable `design-contract.md` and its Scope & Inheritance.
2. User request, stated audience, product evidence, affected screens/components, and representative states.
3. `../product-craft/references/contract-schema.md`, `../product-craft/references/quality-floor.md`, and `../product-craft/references/output-formats.md`.
4. `references/experience-method.md`.

Mark repository or render evidence `[captured]`, new decisions `[proposed]`, and compact Seed assumptions `[inferred]` while proposing. Disclose inference; never present it as user-confirmed fact.

## Workflow

### 1. Frame the Job

Name primary users, roles, trigger, requested action, observable success, failure/retry, and non-goals. For additions or refinements, emit the exact User-job closure record from the shared output formats.

### 2. Build the Experience Model

Use the method reference to define only what the depth requires:

- IA, navigation intent, routes, and screen inventory.
- Content priority per screen.
- Primary and recovery flows.
- Empty, loading, error, partial, overflow, validation, destructive, conflict, and success states when applicable. These are semantic states and they are owned here; which of them the medium can express is the medium's business, and one it cannot express raises `CONTRACT GAP` rather than disappearing.
- Keyboard intent, feedback, recovery semantics, and task-specific microcopy.

**Do not settle on the first plausible structure.** At Full depth, work out more than one way
to organize this surface and put them side by side before choosing. Alternatives that differ
only in section naming are one alternative wearing two labels — they must differ in how
content is grouped, where the entry points are, or what the user does first.

Make the alternatives reactable. Use the shared shell —
`../product-craft/references/decision-dashboard.html` — with tier 1 only and no axes: each
structure shown with real content length, labeled regions, actual navigation, actual ordering.
That tells the user more in ten seconds than a paragraph does, and lets them recognize a
preference they could not have stated in advance. Keep it visually neutral: no palette,
typography, radius, decoration, or art direction. Structure is the subject, and the regions
carry `data-region` / `data-parent` / `data-entry` so two alternatives can be compared as
skeletons rather than by impression.

### 3. Blind-Spot Pass

Before asking for approval, look for what the request did not mention and the obvious reading
would not surface. This is a deliberate pass, not a form to fill in.

The usual hiding places: real content length and distribution, how often each path is actually
used, whether the reader arrives cold from search or a shared link, what failure and recovery
look like, what shows with no data or partial data, the narrowest device in real use, Korean
typography and line breaking, and anything off-screen the surface still owes — sharing, SEO,
print.

Report what you found as material questions or disclosed assumptions. Say what you looked for
and did not find; silence is not coverage.

### 4. Challenge Material Ambiguity

Gate only questions that would materially change jobs, IA, flow, state, recovery, or scope. For Seed, disclose non-blocking compact inferences and auto-chain when the user's explicit build request authorizes it. Full requires explicit Experience approval. Focused Delta requires approval for every changed section.

If an interface or implementation constraint implies an experience change, evaluate it as a proposal rather than silently adapting the contract.

### 5. Hand Off

Emit `Surface Obligations` rows for this stage using
`../product-craft/references/output-formats.md`: `Stage: experience`, one `OBL-NNN` per
material obligation, `Derives from: —` for obligations originating here, concrete evidence or
`missing`, and `GAP` where intent stays unresolved. At Full depth a missing material job,
route, state, or recovery is itself a `GAP`.

This stage's approval token is `experience_approved`, recorded only from explicit user
evidence.

Full covers every material job, route, state/recovery outcome, and navigation intent. Seed and
Focused Delta cover touched obligations only and name the unaffected authority they preserve.
Inference stays disclosed; never present it as user-confirmed fact.

Emit the exact Experience gate record. `READY FOR INTERFACE` requires resolved jobs and
success, sufficient IA/flow, applicable states and recovery, microcopy intent, no open
material question for the affected scope, every applicable experience obligation at `PASS`,
and `experience_approved` recorded from explicit user evidence. Rows that pass while approval
is still unrecorded keep their `PASS` status, but the gate stays `BLOCKED` and those ids are
what blocks it. The gate never self-approves. A ready gate hands ownership to
`interface-design`.

Do not edit the canonical contract unless the user authorized the file change and the applicable Experience gate is approved. Product-craft coordinates the canonical update and Decision Log.

## Audit

An audit is read-only.

1. Establish the lens: user job → approved contract or captured product evidence → accessibility floor.
2. Inspect the rendered surface and key states when available; identify the uninspected scope.
3. Report prioritized findings with severity (`blocks the job`, `slows the job`, `polish`), concrete observation, evidence location, user-job impact, and one actionable correction.
4. Separate strengths from friction. Do not treat aesthetic preference as UX evidence.
5. If the user requests changes later, convert only accepted findings into a Focused Delta.

## Routed Stops

When required experience intent is missing or contradictory, mark the affected EXP row
GAP, emit `CONTRACT GAP`, and stop the affected path. Missing intent routes to the
established experience section owner; contradictory intent reopens the affected
Experience gate even when prior approval exists. When another stage requests an
experience-owned change, answer through a Focused Delta and return fresh Experience
Coverage plus a fresh gate; never let the requester mutate the section itself.
