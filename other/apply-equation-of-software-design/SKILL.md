---
name: apply-equation-of-software-design
kind: skill
status: ready
provenance:
  principles:
  - P027
  - P011
  - P030
  claims:
  - C00116
  - C00280
  - C00288
  - C00290
  - C00292
  - C00303
  - C00304
  - C00305
  - C00306
  - C00307
  - C00308
  - C00311
  - C00312
  - C00313
  - C00314
  - C00325
  source_anchors:
  - 5e67c59e0e18-c0001
  - aca1f3444508-c0000
  authored_from_digest: 10497c24f46532932a22d219f453c7e942956a4376e447f16d46d040aafaaefe
---

# Apply Equation of Software Design

## Purpose

This skill operationalises the Equation of Software Design (PRC-002, clm-027): the
desirability of any design decision is directly proportional to the value it creates for
users and inversely proportional to the effort it requires. Because maintenance effort
dominates the cost of a long-lived system, reducing future maintenance effort outranks
reducing present implementation effort in most real decisions (clm-028). The skill
provides a repeatable procedure for eliciting the terms of the equation, ranking competing
options, calibrating the right level of design investment to the system's expected lifetime
(clm-029), and stating a recommendation grounded entirely in present-time evidence — never
in speculative future demand.

## When to use

Apply this skill whenever:

- Two or more design alternatives must be ranked before a commitment is made.
- A proposed change feels costly and the team needs to understand whether the design or
  the change itself is the problem.
- The team asks how much design investment a system deserves at a given point in its life
  (clm-029).
- A reviewer requires a principled, traceable explanation for preferring one option over
  another in value-over-effort terms.

**When this skill is less applicable:** If the system is explicitly throwaway — the
expected useful lifetime is measured in days or a small number of weeks, with no intent to
maintain or extend it — present implementation effort may legitimately dominate the
decision. The future-maintenance term shrinks proportionally with expected lifetime
(PRC-002, clm-029), and only minimal structural investment is warranted. Even in this
case, confirm the throwaway intent explicitly before reducing that weight; do not assume it.

## Procedure

### Step 1 — Establish the system's expected lifetime and its present requirements

1. Ask the caller to state (or estimate in order of magnitude) how long the system is
   expected to remain in active use and under maintenance.
2. Record only the present, known requirements. Speculative future requirements must not
   enter the value calculation at this stage (PRC-003, clm-026).
3. Note any symptoms already observed — places where small changes ripple widely, or
   where rework recurs in the same areas — as early evidence of where maintenance effort
   is already accumulating (PRC-008, clm-031).
4. Treat the lifetime estimate as a calibration input, not as licence to invent future
   requirements. A system expected to be in use for five years does not automatically
   need every feature that could conceivably appear in five years; it needs a design that
   absorbs real requirements cheaply as they arrive (clm-029, clm-037).

### Step 2 — For each competing option, estimate value and effort separately

For each option (A, B, …) under consideration, record the following four quantities.

**2a. Value**
Assess how concretely the option increases the degree to which the software helps its
users, measured against the stated present requirements (PRC-003, clm-026). Express the
value rating relative to the alternatives: higher, comparable, or lower, with a brief
justification. Do not count speculative future benefits as value; a benefit with no
present requirement behind it does not belong in the numerator.

**2b. Present implementation effort**
Estimate the engineering work needed to produce this option now. Record it separately
from future maintenance effort; conflating the two obscures the term that dominates.

**2c. Future maintenance effort**
Estimate the ongoing effort this option will impose over the expected lifetime (clm-028).
Examine:

- How many places in the codebase typically require edits for a representative anticipated
  change? Fewer is better (clm-037).
- How much cognitive load does the structure place on a reader who must modify it later?
- How well does the option localise the impact of likely future changes, so that a shift
  in the environment requires the least corresponding change to the software (PRC-008,
  clm-037)?
- Note that defect probability rises with change size, so options that make typical future
  changes smaller are inherently safer (clm-036).

**2d. Keep the two effort terms distinct**
Always record present-implementation effort and future-maintenance effort as separate
quantities. For systems with a substantial expected lifetime, the future-maintenance term
weighs more heavily than the present-implementation term in the final ranking (clm-028).

### Step 3 — Calibrate the warranted design investment and rank the options

1. Form the ranking: **desirability ∝ value / (present effort + lifetime-weighted future
   maintenance effort)**. Higher desirability is preferred (PRC-002, clm-027).
2. Scale the weight placed on the future-maintenance term to the expected lifetime: the
   longer the system will be in active use, the greater the weight (clm-028, clm-029).
   A prototype lasting a few weeks warrants minimal structural investment; a system
   expected to evolve over several years warrants careful attention to simplicity and
   change-localisation.
3. Where the desirability ratios of two options are close, flag the uncertainty explicitly
   rather than overstating precision.
4. Check the leading option against the four simplicity tests, applied in priority order
   (PRC-019, clm-055):
   1. Does the design allow the test suite to pass — or, if no tests exist, does it
      avoid impeding testability?
   2. Does the design contain unnecessary duplication?
   3. Does the design express its intent clearly?
   4. Does the design use the fewest classes and methods the job requires?

   If the leading option scores poorly on any test, revisit the maintenance-effort
   estimate from Step 2c — it is likely understated.

### Step 4 — Prefer the option that localises future change and keeps pieces simple

1. All else being equal, prefer the design that absorbs the largest plausible shift in
   requirements for the smallest required change to the code (PRC-008, clm-037). Check
   which option better confines the impact of the changes most likely to occur given the
   current requirements.
2. Simpler individual pieces directly reduce future maintenance effort, because ease of
   maintenance is proportional to the simplicity of the parts (PRC-019, clm-040). Prefer
   the option whose components are easier to understand and modify in isolation.
3. Prefer options that make typical future changes smaller in scope, since change size is
   proportional to defect risk (clm-036).
4. Do not introduce structural elaboration — additional layers, configuration points, or
   abstractions — unless a present requirement demands it. Complexity added speculatively
   raises future effort rather than reducing it.

### Step 5 — State the recommendation on present-time evidence only

1. Name the preferred option and express its advantage in value-and-effort terms derived
   from Steps 2–4.
2. Cite the principle IDs that govern the choice.
3. State the verdict: **proceed** (the current design or the named alternative is
   acceptable as-is), **refactor first** (a bounded structural improvement is needed
   before the change is safe to make), or **redesign** (the fundamental structure must
   change before further development).
4. Confine every claim to present-time information. If the lifetime estimate is uncertain,
   state that as a caveat rather than using the uncertainty to justify speculative
   structure or inflated value (PRC-003, clm-026).
5. If the evidence gathered is insufficient to distinguish the options confidently, say so.
   Insufficient grounding is not a reason to invent supporting detail.

## Inputs

| Input | Required? | Notes |
|---|---|---|
| The artefact or competing design options under review | Required | Code, interface signatures, design document, or equivalent — at least one concrete option must be supplied |
| Present known requirements | Required | Only requirements in scope now; speculative futures are excluded from value calculations |
| Expected remaining system lifetime | Recommended | Used in Step 3 to weight the future-maintenance term; treated as non-throwaway if absent |
| Observed symptoms (change amplification, rework hotspots, repeated defects) | Optional | Provides direct evidence for the maintenance-effort estimate in Step 2c |

## Output

A structured recommendation containing:

1. **Lifetime and requirement summary** — the calibration inputs established in Step 1,
   including any caveats about estimate quality.
2. **Desirability table** — one row per option, showing value rating, present-implementation
   effort, future-maintenance effort, and overall desirability ranking (Steps 2–3).
3. **Simplicity test results** — the four-point check applied to the leading option, with
   notes on any failures (Step 3).
4. **Change-localisation assessment** — which option better absorbs likely future changes
   and keeps individual pieces simpler (Step 4).
5. **Verdict** — the preferred option named, its advantage expressed in value-over-maintenance
   terms, the governing principle IDs, and any material caveats (Step 5).

Minimum useful output: one sentence naming the preferred option and the governing
principle, plus a proceed / refactor / redesign verdict.

## References

- [`../../references/equation-of-software-design-summary.md`](../../references/equation-of-software-design-summary.md) —
  summary table of the Equation of Software Design, its terms, and lifetime-calibration
  guidance.
- [`../../principles/principles.yaml`](../../principles/principles.yaml) — canonical
  principle definitions; see PRC-002 (the Equation), PRC-003 (software's purpose is
  helping people), PRC-008 (design for change), PRC-019 (simplicity as the lever for
  maintainability).

## Provenance

Derived exclusively by paraphrase from two distillation-only sources:
`code-simplicity-the-aca1f344` (Kanat-Alexander, *Code Simplicity: The Fundamentals of
Software*) and `clean-code-a-handboo-5b1b9ca3` (Martin, *Clean Code: A Handbook of Agile
Software Craftsmanship*), together with package principles PRC-002, PRC-003, PRC-008,
PRC-019 and the associated claims listed in the frontmatter. All content is paraphrased;
no source text has been reproduced verbatim. No claim has been strengthened beyond the
evidence supplied in the grounding.
