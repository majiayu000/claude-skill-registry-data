---
name: apply-single-responsibility
kind: skill
status: ready
provenance:
  principles:
  - P018
  - P005
  - P020
  - P015
  claims:
  - C00475
  - C00476
  - C00477
  - C00478
  - C00479
  - C00480
  - C00549
  - C00550
  - C00551
  - C00552
  - C00553
  - C00554
  - C00555
  - C00556
  - C00661
  - C00721
  source_anchors:
  - 0574f24ece08-c0000
  - 0574f24ece08-c0001
  - 5b1b9ca368a5-c0001
  - 5b1b9ca368a5-c0003
  authored_from_digest: c805857357f41a007178d79ff395e2a5ff63da62aadeb0f8cc8bb19a82f55233
---

# Apply Single Responsibility

## Purpose

Review a class, module, or function to determine whether it bears more than one reason to
change, and recommend the smallest structural reorganisation that restores a single,
cohesive responsibility to each unit — without creating information leakage, shallow
pass-through layers, or classitis in the process.

The Single Responsibility Principle holds that a class or module should have one, and only
one, reason to change (PRC-015; clm-053). The operative measure of class size is the count
of its responsibilities, not the count of its lines (clm-052). Pursuing high cohesion
consistently tends to yield many small classes, because separating concerns to keep each
class cohesive multiplies the number of classes; that outcome is a natural consequence of
applying the principle, not a shortcoming (clm-054). At the function level the same
discipline applies: each function should do one thing, do it well, and do it only
(PRC-014; clm-045), with all of its statements operating at the same level of abstraction
(clm-046).

**Faithfulness boundary.** SRP must not be applied so aggressively that tightly-coupled
information is fragmented across units, creating information leakage or shallow
pass-through classes that hide nothing and add indirection without value (PRC-005;
PRC-021). When a proposed split would force two modules to change in lockstep for every
future decision, or produce a class that merely delegates to another without adding any
meaningful abstraction, the split is counterproductive. The goal is structural clarity and
reduced maintenance cost, not mechanical class multiplication.

## When to use

- A class, module, or function is submitted for review and the team suspects it has grown
  to cover more than one purpose.
- The divergent-change smell is observed: the same module is modified in different ways
  for different types of reasons across successive change events (clm-067).
- A function is long, contains clearly distinct phases of work, or mixes high-level
  orchestration with low-level detail in the same body (PRC-014; clm-046).
- A reviewer struggles to write a concise, accurate name for a class or function — naming
  difficulty is a diagnostic signal that the unit has not yet resolved to a single concept.
- A team is planning a behaviour-preserving refactoring and needs to identify which class
  boundaries need redrawing before the work begins (PRC-012).

## Procedure

### Step 1 — Enumerate all reasons to change in the candidate unit

For each class or module under review, systematically list the reasons a future change
might require editing that unit. A "reason to change" corresponds to a distinct actor,
stakeholder, or system concern whose evolving requirements could independently drive a
modification.

1. Read the class or module in full and name every distinct concern it addresses — for
   example: persistence logic, domain validation, output formatting, orchestration of
   external calls.
2. For each pair of concerns, ask: if concern A changed independently of concern B — say a
   new storage format was required whilst domain rules stayed fixed — would both concerns
   still need to be in the same file? If yes, they may be genuinely coupled and the split
   could cause information leakage. If no, they are candidates for separation.
3. Record each concern as a named candidate responsibility. More than one candidate
   responsibility → the unit is a candidate for splitting (PRC-015; clm-053).
4. If the unit has only one identifiable reason to change, record that it satisfies SRP
   and proceed to Step 4 (function-level review).

### Step 2 — Confirm with the divergent-change smell

An enumeration of concerns is necessary but not sufficient confirmation of an SRP
violation. Cross-reference candidate responsibilities against the divergent-change smell
before proceeding:

- Examine the change history of the unit, or ask the engineer to describe how it has
  changed recently. Does it get edited for different reasons by different people, or in
  response to distinct categories of event? That pattern is divergent change
  (clm-067; martin-fowler-refact-0574f24e-h0140).
- One identifiable cluster of changes driven by one concern and a separate cluster driven
  by another concern confirms multi-responsibility
  (clean-code-a-handboo-5b1b9ca3-h0403; clean-code-a-handboo-5b1b9ca3-h0407).
- If the unit changes as a whole, consistently for a single coherent reason — even if it
  is large — the divergent-change smell is absent. Record this and reconsider whether
  splitting is warranted. Bulk alone is not a violation; responsibility count is the
  measure (clm-052).
- If change history is unavailable, note the limitation. Rely on the concern enumeration
  from Step 1 but flag confidence as lower.

### Step 3 — Propose a split; check for information leakage and shallow classes

For each unit confirmed as multi-responsibility in Step 2, draft a split proposal and
apply the following three checks before endorsing it:

1. **Name the resulting units.** Each proposed new class or module must have a name that
   reflects a single, coherent responsibility. If a precise name cannot be constructed,
   the proposed boundary is not clean — revise it or record a tension note.

2. **Check for information leakage.** If the split would force one new class to reach into
   the internals of the other on every operation — or if both must change together whenever
   a shared data structure is updated — the boundary leaks implementation detail. A
   leaking split worsens the design rather than improving it (PRC-006). Do not endorse it.

3. **Check for shallow pass-through classes.** If either resulting unit would hold nothing
   but delegation calls to the other without adding meaningful abstraction or hiding any
   implementation decision, the split has produced a classitis artefact (PRC-021). It adds
   interface and boilerplate complexity without reducing cognitive load. Do not endorse it.

4. **Confirm that cohesion rises.** Within each resulting unit, all remaining members
   should be closely related to its single stated responsibility. High cohesion within
   each unit after the split is the positive signal that the boundary is correct
   (clm-054; clean-code-a-handboo-5b1b9ca3-h0225; clean-code-a-handboo-5b1b9ca3-h0228).

If no candidate split passes all three checks, record the unit as exhibiting a tension
between SRP and information hiding, state the trade-off explicitly, and recommend no split.
This is the condition under which PRC-015 does not apply: splitting would scatter
tightly-shared information and create leakage instead of clarity.

### Step 4 — Review each function for single purpose and uniform abstraction level

For every function in the artefact — or, if the submission is a class or module, for every
function in the units identified in Steps 1–3:

1. **Single purpose.** Ask: what does this function do? If the accurate answer requires the
   word "and", the function likely does more than one thing and should be decomposed
   (clm-045; clean-code-a-handboo-5b1b9ca3-h0061). A useful test: can a meaningful
   sub-operation be extracted under a name that is not merely a restatement of the
   function's own name? If yes, extraction is warranted.

2. **Level of abstraction.** Read the function's body from top to bottom. Are all
   statements at roughly the same conceptual level — all high-level orchestration, or all
   low-level manipulation — or does the function mix the two? Mixing forces a reader to
   shift cognitive register mid-read and obscures intent (clm-046;
   clean-code-a-handboo-5b1b9ca3-h0065; clean-code-a-handboo-5b1b9ca3-h0066). Where
   levels are mixed, identify the boundary between them and propose an extraction.

3. **Smallness.** The governing discipline is that functions should be small, and smaller
   still (PRC-014; clm-044; clean-code-a-handboo-5b1b9ca3-h0057). This does not mean
   minimising line count mechanically; it means that a function's body should correspond to
   a single level of intent. Evaluate length in that frame, not against an arbitrary
   line limit.

4. **Pass-through caveat.** If decomposing a function would produce a call chain of thin
   wrappers — one function calling another that does nothing but forward to a third — the
   proposed extraction may not produce a meaningful new level of abstraction; it may only
   add indirection (PRC-005; PRC-021). In that case, do not recommend the extraction.

### Step 5 — Recommend the smallest bounded restructuring

Assemble findings from Steps 1–4 into a ranked set of recommendations, ordered by impact
on future maintenance cost (PRC-002):

1. **State the verdict.** Does the artefact satisfy SRP at both class/module level and
   function level, satisfy it partially, or violate it? Include a **comply / refactor /
   no-clean-split** disposition.

2. **For each violation, name:**
   - The unit (class, module, or function) and its identified responsibilities.
   - The proposed split or extraction — a one-sentence description of the new boundary.
   - Why the boundary is clean: it raises cohesion, does not leak information, and does
     not produce shallow pass-throughs.
   - If no clean split exists, state the tension explicitly and recommend no split.

3. **Gate on tests.** Any recommendation that changes the internal structure of working
   code is a behaviour-preserving refactoring. Before endorsing it, confirm that a test
   suite capable of detecting behaviour change is in place (PRC-012). If tests are absent
   or insufficient, the first recommendation is to establish them; structural
   reorganisation follows only once that safety net exists.

4. **Keep the recommendation bounded.** Propose only the smallest restructuring needed to
   resolve the identified violation. Do not recommend wholesale rewrites, broader design
   changes, or generality not demanded by present known requirements (PRC-007).

## Inputs

| Field | Required | Description |
|---|---|---|
| `artefact` | Yes | The class, module, or function (or a design description thereof) under review |
| `requirements` | Yes | The present known requirements governing this artefact; used to distinguish genuinely distinct concerns |
| `change_history` | No | Recent modification log or engineer's account of how the unit has changed; enables the divergent-change check in Step 2 |
| `lifetime` | No | Anticipated system lifetime; calibrates how much restructuring investment is warranted |
| `team_conventions` | No | Project-specific conventions that legitimately override a general heuristic |

## Output

A structured SRP review containing, in order:

1. **Verdict line** — one sentence naming whether the artefact satisfies SRP at class/module
   level and at function level, with a **comply / refactor / no-clean-split** disposition.

2. **Class/module findings** — for each unit with more than one reason to change:
   - Named responsibilities (enumerated)
   - Divergent-change confirmation: present, absent, or unverifiable
   - Proposed split boundary (one sentence), or an explicit tension note if no clean split
     was found
   - Cohesion assessment of the proposed resulting units
   - Information leakage and shallow-class check result

3. **Function findings** — for each function that does more than one thing or mixes
   abstraction levels:
   - Named concern(s) and where the abstraction levels diverge
   - Proposed extraction (one sentence)
   - Pass-through check result

4. **Test-gate status** — confirmation that a test suite capable of catching behaviour
   change is in place, or a recommendation to establish one before restructuring proceeds
   (PRC-012).

5. **Bounded recommendations** — an ordered list of the smallest structural changes to
   resolve each finding, most-impactful first, with no replacement code.

The output does not include replacement code. Structural before/after sketches accompany a
bounded fix only when operating in `patch-suggest` mode; in `review` mode the output is a
critique only.

## References

- [`../../references/clean-code-heuristics-summary.md`](../../references/clean-code-heuristics-summary.md) —
  SRP, function smallness, single level of abstraction, and cohesion heuristics
- [`../../principles/principles.yaml`](../../principles/principles.yaml) —
  PRC-015 (Single Responsibility Principle: one reason to change, split on divergent
  change), PRC-014 (functions small, single purpose, single abstraction level), PRC-005
  (prefer deep modules; simple interface matters more than simple implementation), PRC-021
  (flag shallow pass-throughs and classitis), PRC-012 (behaviour-preserving refactoring
  requires a self-testing suite), PRC-007 (reject speculative generality and unneeded
  restructuring)

## Provenance

Authored from distillation-only sources; all content is paraphrased and no verbatim text
is reproduced from any source work.

- **Martin's Clean Code** (clean-code-a-handboo-5b1b9ca3), anchors h0215, h0218, h0225,
  h0228: class size is measured by number of responsibilities, not lines (clm-052); one
  reason to change (clm-053); high cohesion yields many small classes (clm-054). Anchors
  h0057, h0061, h0065, h0066: functions should be small (clm-044); a function does one
  thing (clm-045); statements within a function operate at one level of abstraction
  (clm-046). Anchors h0403, h0407: divergent change — the smell that reveals more than one
  responsibility and should drive a split (clm-067).
- **Fowler's Refactoring** (martin-fowler-refact-0574f24e), anchor h0140: divergent
  change — a module modified in different ways for different reasons — as the structural
  signal that a class or module carries more than one responsibility (clm-067).
- Governing principles: PRC-015 (SRP at class/module level), PRC-014 (SRP at function
  level), with the faithfulness boundary from PRC-005 and PRC-021 (no shallow
  pass-throughs or information leakage from over-zealous splitting).
