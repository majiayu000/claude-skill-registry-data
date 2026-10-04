---
name: detect-code-smells
kind: skill
status: ready
provenance:
  principles:
  - P010
  - P015
  - P019
  - P029
  - P011
  - P007
  claims:
  - C00450
  - C00481
  - C00482
  - C00483
  - C00484
  - C00485
  - C00486
  - C00487
  - C00488
  - C00493
  - C00575
  - C00609
  - C00621
  - C00650
  - C00670
  - C00672
  source_anchors:
  - 0574f24ece08-c0000
  - 5b1b9ca368a5-c0000
  - 5b1b9ca368a5-c0001
  - 5b1b9ca368a5-c0004
  - 5b1b9ca368a5-c0006
  authored_from_digest: 11ed5779f94bb0f33bcd5658f74728ca7399504491fa6c92d0b3064546c2a218
---

# Detect Code Smells

## Purpose

Scan a code artefact systematically against two complementary recognition catalogues — the
Fowler smell set and the Ousterhout red-flag checklist — to produce a prioritised critique in
which the most costly structural symptom is named first, traced to its root cause and a
governing principle, and paired with the smallest bounded fix (PRC-013).

Code smells are heuristics, not rules. They signal *where* structural problems are likely;
they do not mandate action automatically (clm-063). The goal of this skill is to surface
where refactoring effort will yield the greatest reduction in future maintenance cost, not to
flag every cosmetic deviation (PRC-002).

## When to use

- A function, class, module, or component is submitted for design review and the team wants
  named structural symptoms rather than subjective commentary.
- Change amplification is suspected — small changes ripple widely or force edits across many
  files — and the structural root cause needs identifying.
- A module has grown over time and its readability or changeability has visibly degraded.
- Before planning a refactoring session, to determine which smells impose the highest cost
  and which can safely be deferred.
- A team wants to know whether apparent duplication in two or more places is a genuine DRY
  violation warranting unification, or merely coincidental resemblance that will evolve
  independently (PRC-009, clm-039).

## Procedure

### Step 1 — Gather context

1. Identify the artefact type: function, class, module, component, or cross-cutting slice.
2. Note any complexity symptoms the caller has already reported: change amplification, shotgun
   surgery, hard-to-name concepts, or high cognitive load.
3. Record the anticipated system lifetime and the present known requirements; these calibrate
   how urgent a smell is and whether a smell in stable code needs immediate action.
4. Note any team conventions that legitimately override a general heuristic (for example, a
   project rule that tolerates long parameter lists in generated protocol bindings).

### Step 2 — Scan against the Fowler smell set

Work through the catalogue systematically. For each smell found, record its canonical name,
the specific location (function, class, or code region), and a one-sentence description of
why it matches (clm-063). If a smell category is absent, record it as absent — do not skip
it silently.

| Smell | What to look for | Root-cause signal |
|---|---|---|
| **Duplicated code** | The same or nearly identical structure appearing in more than one location | A piece of knowledge with no single home; violates DRY (clm-064, PRC-009, clm-039) |
| **Long function** | A function whose length makes its intent harder to understand than its name suggests | Abstraction not yet extracted; single level of abstraction not maintained (clm-065) |
| **Long parameter list** | A function signature with so many parameters that its interface is hard to reason about | A missing concept that should group the parameters into a coherent object (clm-066) |
| **Divergent change** | One module modified in different ways for different reasons across different change events | More than one responsibility housed in the same module (clm-067) |
| **Shotgun surgery** | A single logical change that forces many small edits scattered across multiple modules | Responsibility that belongs in one place but has been spread across many (clm-068) |
| **Feature envy** | A function that spends more effort reaching into another module's data than working with its own | Behaviour and data are in the wrong modules; the function likely belongs closer to the data it uses (clm-069) |
| **Data clumps** | Groups of data items that always appear together as loose parameters or repeated fields | A missing concept that should become a dedicated type (clm-070) |
| **Primitive obsession** | Raw primitives used where a small, named value object would carry both the value and its constraints | Over-reliance on raw types where a richer type would eliminate implicit conventions (clm-070) |
| **Dead code** | Unreachable branches, unused variables, or functions never called | Code whose purpose has gone; adds noise without value (clm-056) |
| **Functions that do too much** | A function whose body contains multiple distinct operations or levels of abstraction | Single-responsibility violated at the function level (clm-056) |

### Step 3 — Scan against the Ousterhout red-flag checklist

The Ousterhout red flags form a complementary set focused on module interfaces and
information hiding rather than internal structure (clm-025). Check each of the following:

| Red flag | What to look for |
|---|---|
| **Shallow module** | An interface nearly as complex as the implementation it wraps; the module hides little |
| **Information leakage** | Implementation details visible across a module boundary — in parameter types, file formats, or ordering assumptions |
| **Temporal decomposition** | Decomposition driven by execution order rather than by what information each piece needs to know |
| **Overexposure** | An interface that forces callers to be aware of details they should not need to understand |
| **Pass-through method** | A method that does nothing but forward a call to another method with the same or nearly the same signature |
| **Repetition** | The same snippet of logic at multiple call-sites without a shared extraction |
| **Special-general mixture** | General-purpose and special-purpose logic interleaved in the same module |
| **Conjoined methods** | Two methods that can only be understood by reading them together |
| **Vague name / hard-to-pick name** | A name so broad or awkward that no precise alternative can be found — often a signal that the underlying concept is not yet well-defined |
| **Hard-to-describe module** | A module whose behaviour cannot be summarised concisely without listing exceptions |
| **Nonobvious code** | Code whose side effects, assumptions, or behaviour cannot be understood from reading it locally |

Several Ousterhout red flags overlap with Fowler smells (for example, repetition ↔
duplicated code; shallow module ↔ pass-through method). When overlap occurs, cite both
catalogues — the convergence strengthens the finding.

### Step 4 — Rank findings by cost

Reorder all collected findings on two axes:

1. **Complexity impact** (primary): Does this smell cause change amplification (one logical
   change requires many physical edits), raise cognitive load (the reader cannot understand
   a unit locally), or create unknown unknowns (behaviour cannot be predicted from the
   interface)? These directly damage structural quality and represent the highest-cost smells
   (PRC-001).
2. **Future maintenance effort** (secondary): Does this smell make the codebase harder to
   change over time? Smells that obstruct future change rank above smells that affect only
   present readability (PRC-002).

Do not rank by cosmetic preference. A poorly named variable that does not impede
changeability ranks below shotgun surgery that amplifies every future modification.

**Approximate ranking guidance (most costly first):**

- **Shotgun surgery** and **divergent change** sit at the top when confirmed; they directly
  cause change amplification across the codebase (clm-067, clm-068).
- **Duplicated code** and **feature envy** follow; they create a covert dependency between
  sites that will eventually diverge incorrectly and silently (clm-064, clm-069, PRC-009).
- **Information leakage** and **temporal decomposition** are high-cost module-level smells
  that make future interface changes painful (clm-025).
- **Long function**, **long parameter list**, **data clumps**, and **primitive obsession**
  are significant but typically local in impact (clm-065, clm-066, clm-070).
- **Nonobvious code**, **vague names**, and **dead code** are lower-cost unless they
  directly obscure behaviour with wider consequences (clm-025, clm-056).

### Step 5 — Map each finding to its structural root cause and refactoring family

For every finding in ranked order, record:

- **Smell name**: the canonical label from Step 2 or Step 3.
- **Location**: specific function, class, or region in the artefact.
- **Structural root cause**: the underlying design choice that produced the smell (missing
  abstraction, responsibility mismatch, DRY violation, interface overexposure, etc.).
- **Principle(s) violated**: cite the relevant principle ID(s) and claim ID(s).
- **Refactoring family**: the family of behaviour-preserving transformations that addresses
  the smell. Name the family only — defer specific mechanics to the
  `plan-behaviour-preserving-refactoring` skill.
  - Duplicated code → *Extract Function / Extract Class / Pull Up Method* family
  - Long function → *Extract Function* family
  - Long parameter list → *Introduce Parameter Object / Preserve Whole Object* family
  - Divergent change → *Extract Class / Split Module* family
  - Shotgun surgery → *Move Function / Move Field / Inline Class* family
  - Feature envy → *Move Function* family
  - Data clumps / primitive obsession → *Introduce Value Object / Extract Class* family
  - Shallow module / pass-through / overexposure → *Inline Method / Merge Module / Reduce
    Interface* family
  - Information leakage / temporal decomposition → *Extract Module / Merge Module* family
- **Bounded fix**: the smallest structural change that removes this specific instance of the
  smell without introducing new scope or unrelated concerns (clm-016).

### Step 6 — Apply the stability caveat

If a smell is present in code that is not currently being modified and has not been linked
to reported symptoms (no change amplification, no defects traced to it), record it as a
**watch item** rather than a required action (clm-063, PRC-013). Note it in the output
with its rank so that future maintainers have a complete picture, but do not mandate a
refactoring pass on stable code solely because a smell is detectable. The decision to act
rests with the engineer or tech lead who owns the code.

### Step 7 — Compose the critique

Assemble the ranked findings into the output format described in `## Output`. Place the
most costly finding at the top. Open with a verdict line: one sentence naming the single
most costly smell, the principle it violates, and a **proceed / refactor / redesign**
recommendation.

If no smells are found after completing Steps 2 and 3, state that the scan was completed
against both catalogues and no instances were detected. Do not invent smells to fill the
output.

## Inputs

| Field | Required | Description |
|---|---|---|
| `artefact` | Yes | The code, interface signatures, module description, or design document to be reviewed |
| `requirements` | Yes | The present known requirements governing this artefact |
| `lifetime` | No | Anticipated system lifetime; calibrates how much structural investment is warranted |
| `observed_symptoms` | No | Complexity symptoms already reported (change amplification, hotspot files, hard-to-name concepts) |
| `team_conventions` | No | Project-specific conventions that legitimately override a general heuristic |

## Output

A structured critique with the following elements, in order:

1. **Verdict line** — one sentence: the single most costly smell or red flag found, the
   principle it violates, and a proceed / refactor / redesign recommendation.
2. **Ranked findings** — one entry per smell or red flag detected, ordered most-costly
   first. Each entry contains:
   - Smell name (canonical label from the Fowler set or Ousterhout checklist)
   - Location in the artefact
   - Structural root cause
   - Principle(s) violated (cited by principle ID and claim ID)
   - Refactoring family
   - Bounded fix (smallest structural change; no replacement code)
   - Stability note: **required action** or **watch item**
3. **Clean-scan confirmation** — explicit statement that both catalogues were checked, with
   a note of any smell categories where no instance was found, so absence is recorded
   rather than assumed.

The output does not include replacement code. Structural sketches accompany a bounded fix
only in `patch-suggest` mode; in `review` mode the output is a critique only.

## References

- [`../../references/fowler-code-smell-catalogue.md`](../../references/fowler-code-smell-catalogue.md) —
  canonical smell names and descriptions; used in Step 2
- [`../../references/ousterhout-red-flags-catalogue.md`](../../references/ousterhout-red-flags-catalogue.md) —
  red-flag checklist; used in Step 3
- [`../../principles/principles.yaml`](../../principles/principles.yaml) —
  PRC-013 (smells as heuristics for where to refactor, not strict rules),
  PRC-009 (Don't Repeat Yourself),
  PRC-001 (complexity model: change amplification, cognitive load, unknown unknowns),
  PRC-002 (future maintenance effort as the primary cost axis)

## Provenance

Authored from distillation-only sources; all content is paraphrased and no verbatim text
is reproduced from any source work.

- **Fowler's Refactoring** (martin-fowler-refact-0574f24e), anchors h0133, h0135–h0137,
  h0140–h0144: smell recognition as heuristics (clm-063); duplicated code (clm-064); long
  function (clm-065); long parameter list (clm-066); divergent change (clm-067); shotgun
  surgery (clm-068); feature envy (clm-069); data clumps and primitive obsession (clm-070).
- **Ousterhout's A Philosophy of Software Design** (a-philosophy-of-soft-5e67c59e), anchors
  h0623, h0163: the red-flag checklist as a complementary recognition set (clm-025).
- **Martin's Clean Code** (clean-code-a-handboo-5b1b9ca3), anchor h0358: duplication, dead
  code, and functions that do too much as further warning signs (clm-056).
- **Kanat-Alexander's Code Simplicity** (code-simplicity-the-aca1f344), anchors h0078,
  h0079: each piece of knowledge should exist in one place (clm-039); criteria for when to
  combine or separate code (clm-016).
- Governing principles: PRC-013 (smells are heuristics), PRC-009 (Don't Repeat Yourself).
