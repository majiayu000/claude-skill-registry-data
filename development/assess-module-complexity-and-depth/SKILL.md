---
name: assess-module-complexity-and-depth
kind: skill
status: ready
provenance:
  principles:
  - P028
  - P027
  - P019
  - P030
  - P011
  claims:
  - C00116
  - C00280
  - C00303
  - C00304
  - C00305
  - C00306
  - C00307
  - C00308
  - C00327
  - C00328
  - C00329
  - C00346
  - C00347
  - C00350
  - C00351
  - C00381
  source_anchors:
  - 5e67c59e0e18-c0001
  - aca1f3444508-c0000
  - aca1f3444508-c0001
  authored_from_digest: 09027404bdd41f0a5f35cd85cf0260a1addc6bcbee77f3861f0cfedc4523b851
---

# Assess Module Complexity and Depth

## Purpose

Provide a structured, principle-grounded assessment of one or more modules, classes, or
subsystems for structural complexity and interface depth. The assessment produces a ranked
finding list — the costliest structural flaw named first — with each finding traced to a
specific complexity symptom and cause, and the smallest safe structural change recommended
for each (PRC-001; PRC-005).

Complexity is anything about a system's structure that makes it harder to understand or
modify; it is the primary thing this review manages (PRC-001; clm-001). Because complexity
accumulates from many small contributions rather than a single large failure, resistance must
be applied on every change, not deferred to a future clean-up pass (clm-004).

## When to use

- A module's interface feels disproportionately large or difficult relative to the
  functionality it provides.
- Two or more modules must change together whenever a single conceptual decision changes.
- A class or method has no behaviour of its own beyond forwarding arguments elsewhere.
- A design has proliferated many small classes, each contributing minimal functionality.
- Module boundaries appear to follow the order of execution rather than what each part owns
  or hides.
- A reviewer needs a prioritised finding list before recommending any refactoring work.

Do **not** apply this skill when the concern is purely runtime performance tuning, a specific
reproducible defect, or a business-requirements triage with no structural question attached
(see `profile.yaml when_not_to_use`).

## Procedure

### Step 1 — Gather the artefact and context

Collect:
- The artefact under review (source code, interface signatures, class diagram, or design
  description).
- The module's stated purpose and present known requirements.
- Any complexity symptoms already reported by the team (e.g. "a one-line change forced edits
  in eight files" or "nobody is sure what breaks when we touch this class").
- Optionally: the system's anticipated lifetime, used to calibrate how much structural
  investment is warranted.

If no symptoms are reported, note that the scan in Steps 2–3 will surface them.

---

### Step 2 — Measure module depth

For each module or class in scope, perform the following three sub-steps.

**2a. Enumerate the interface surface.**
List every public method, constructor, configuration parameter, caller-visible type, and
exception. Flag any element that requires a caller to understand internal ordering
constraints, internal state, or internal error-handling branches — these are interface
surface that adds cognitive burden on callers (clm-008).

**2b. Enumerate the hidden functionality.**
Describe what the module actually decides and does that callers are not required to do
themselves. Include: branching logic, format decisions, error normalisation, default
selection, and any volatile implementation detail the interface conceals.

**2c. Assign a depth rating.**
A deep module provides substantial hidden functionality behind a narrow, stable interface;
callers benefit from the abstraction (PRC-005; clm-007). A shallow module exposes an
interface that is roughly as complex as the implementation it wraps, giving callers little
reduction in what they must know or do (clm-008).

Rate each module: **deep**, **adequate**, or **shallow**.

Record: interface element count, hidden-functionality inventory, and a one-sentence
depth judgement citing the evidence.

---

### Step 3 — Scan for red flags

Examine the artefact for each red flag below. For every flag found, record the module(s)
affected and the specific evidence (method names, shared types, parameter lists, etc.).

| # | Red flag | Signal to look for | Grounding |
|---|---|---|---|
| RF-1 | **Shallow module** | Interface complexity is comparable to or greater than implementation complexity; callers absorb decisions the module could make for them | clm-008; PRC-005 |
| RF-2 | **Information leakage** | The same design decision (e.g. file format, wire protocol, internal data structure) is reflected in two or more modules, forcing them to change together | clm-011; PRC-006 |
| RF-3 | **Temporal decomposition** | Module boundaries mirror the execution sequence (read → parse → validate → write) rather than the information each phase owns or hides | clm-012; PRC-006 |
| RF-4 | **Pass-through method** | A method does nothing beyond forwarding its arguments to another method with the same or near-identical signature, adding no behaviour and hiding nothing | clm-014; PRC-021 |
| RF-5 | **Classitis** | Many small classes each provide minimal functionality, increasing the total interface and boilerplate surface a caller must navigate | clm-009; PRC-021 |
| RF-6 | **Exposed volatile decision** | A design decision likely to change — algorithm choice, storage format, external protocol detail — is visible in the public interface rather than hidden behind it | clm-010; PRC-006 |

---

### Step 4 — Diagnose the complexity symptom and cause

For each candidate finding from Step 3, identify the **symptom** and the **cause** it
belongs to.

**Symptoms** (PRC-001; clm-002):

- *Change amplification* — a single conceptual change requires edits in many modules or
  locations. Each additional edit site raises defect risk.
- *High cognitive load* — a developer must hold a large amount of context to make or
  understand a change; this raises onboarding costs and review difficulty.
- *Unknown unknowns* — it is not apparent which code must change when a requirement shifts.
  **This is the most dangerous symptom** because the affected developer cannot detect the
  gap (clm-002).

**Causes** (PRC-001; clm-003):

- *Dependency* — a module cannot be understood or changed in isolation because it is coupled
  to the internals of another.
- *Obscurity* — important information exists but is not visible from the interface or
  structure; it must be discovered by reading implementation detail.

Record the symptom–cause pair for each finding. Any finding whose primary symptom is
**unknown unknowns** is automatically elevated to the highest severity tier.

---

### Step 5 — Assess whether bounded generality would deepen the interface

For any shallow module (RF-1) or narrowly special-purpose interface, ask:

> Would a slightly more general-purpose interface — one shaped to the current *family* of
> known use cases rather than only the immediate case — produce a simpler, narrower surface
> for the same or greater hidden functionality?

If yes, note the candidate generalisation and the present known uses that justify it
(PRC-026; clm-013).

**Binding constraint:** any proposed widening must be justified by present known
requirements, not by imagined future ones. Speculative generality is itself a source of
complexity and is forbidden (PRC-007). If no present need supports the generalisation, do
not recommend it.

---

### Step 6 — Order findings by cost

Rank all findings from most to least costly using the following priority order:

1. **Unknown-unknowns symptom** — ranked first because the developer affected cannot see the
   risk; silent, accumulating damage to maintainability (clm-002).
2. **Change amplification** — ranked second; each additional edit site increases defect
   probability and integration effort.
3. **High cognitive load** — ranked third; raises cost of safe change but does not cause
   silent failures.

Within each tier, rank by scope: cross-module flags (RF-2 Information leakage, RF-3
Temporal decomposition) typically outrank within-module flags (RF-4, RF-5) because their
blast radius is larger.

---

### Step 7 — Prescribe the smallest safe fix for each finding

For each finding, propose the minimum structural change that removes the root cause rather
than patching its symptom. Match the fix to the flag type:

- **Shallow module (RF-1):** Pull complexity downward — move caller-side default selection,
  error interpretation, or format decisions into the module so callers supply only what
  genuinely varies. The implementer should absorb complexity rather than expose it
  (PRC-005; clm-015).

- **Information leakage (RF-2):** Consolidate the shared design decision into a single
  module. Give that module sole ownership; let the other(s) consume the result through a
  stable, narrow interface (PRC-006; clm-011).

- **Temporal decomposition (RF-3):** Redesign the module boundary around what each module
  *knows* rather than when it *runs*. Group elements by the information domain they own,
  not by their position in the execution sequence (PRC-006; clm-012).

- **Pass-through method (RF-4):** Either add real behaviour that justifies the method's
  existence and earns it a place in the interface, or remove it and let callers interact
  with the wrapped module directly — whichever choice more clearly expresses the
  responsibility division (PRC-021; clm-014).

- **Classitis (RF-5):** Merge shallow classes that share the same information domain into a
  single class with a deeper interface. Reducing the number of concepts a caller must hold
  is the goal; do not merge classes whose domains are genuinely distinct (PRC-021; clm-009).

- **Exposed volatile decision (RF-6):** Encapsulate the volatile decision behind a stable
  abstract interface. Callers receive the result, not the mechanism; the module owns the
  volatility (PRC-006; clm-010).

- **Overly narrow or special-purpose interface:** Widen to the smallest general-purpose
  interface that covers the present family of known needs and no wider. Verify that the
  wider interface is genuinely simpler for callers before recommending it (PRC-026; clm-013).

Each recommended change must be bounded. Do not recommend changes for which no present
known requirement exists, and do not propose more restructuring than the flag demands
(clm-004; PRC-007).

---

### Step 8 — Compose and deliver the output

Assemble the ranked finding report as described in `## Output`, then close with one of three
overall verdicts:

- **Proceed** — no significant red flags found; the module's depth is adequate and
  information is well hidden.
- **Refactor** — red flags are present but bounded fixes are available and sufficient;
  no wholesale redesign is needed.
- **Redesign** — structural problems are pervasive, or the dominant symptom is unknown
  unknowns across multiple modules, indicating the current decomposition is fundamentally
  misaligned with the information it should hide.

## Inputs

| Input | Required | Notes |
|---|---|---|
| Artefact under review | Yes | Source code, interface signatures, class diagram, or design description |
| Stated present known requirements | Yes | Used to bound any fix or generalisation recommendation |
| Observed complexity symptoms | No | Accelerates diagnosis; absence does not block the assessment |
| System's anticipated lifetime | No | Used to calibrate how much structural investment is appropriate |
| Team conventions or constraints | No | Legitimate local overrides to general principles; note these explicitly |

## Output

A structured finding report containing:

1. **Ranked finding list** — ordered most-costly first (unknown unknowns → change
   amplification → cognitive load), each finding containing:
   - Red flag name and the module(s) affected.
   - Concise evidence (specific methods, parameters, or shared types).
   - Complexity symptom (change amplification / cognitive load / unknown unknowns) and cause
     (dependency / obscurity).
   - Principle(s) violated, cited by ID.
   - The smallest bounded fix, describing a structural change rather than replacement code.

2. **Overall verdict** — one of: **proceed**, **refactor**, or **redesign**, with a
   one-sentence justification.

The minimum useful output is one sentence naming the single costliest red flag, the
principle it violates, a one-sentence bounded recommendation, and the verdict.

## References

- [`../../references/ousterhout-red-flags-catalogue.md`](../../references/ousterhout-red-flags-catalogue.md) —
  Full red-flag catalogue with definitions and examples for RF-1 through RF-6 and related
  flags.
- [`principles/principles.yaml`](principles/principles.yaml) — Canonical principle
  definitions for PRC-001 (complexity model), PRC-005 (deep modules), PRC-006 (information
  hiding), PRC-021 (shallow layering), and PRC-026 (bounded generality).

## Provenance

Derived from principles PRC-001, PRC-005, PRC-006, PRC-021, and PRC-026 and their
supporting claims (clm-001 through clm-004, clm-007 through clm-015) as recorded in
`principles/principles.yaml`, and grounded in source anchors
`a-philosophy-of-soft-5e67c59e-h0020` through `a-philosophy-of-soft-5e67c59e-h0088`.

**Rights notice:** the source text (`a-philosophy-of-soft-5e67c59e`) is distillation-only.
All content in this skill has been paraphrased into original language; no verbatim runs of
source wording appear anywhere in this file.
