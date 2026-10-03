---
name: extract-verifiable-properties
description: Extract verifiable correctness properties from ONE component artifact — a spec, the source code, or a verification harness/verif — at a fixed, comparable granularity, with coverage by construction.
argument-hint: "<artifact files> <output file>"
---

## Purpose
From **one** artifact (a spec, OR the code, OR a harness/verif) produce the list of **verifiable
properties** it implies, at a **fixed granularity** so lists from different artifacts compare
row-by-row. Read only the named artifact; ground everything in it.

## What a verifiable property is (the unit)
> A **single, falsifiable, machine-checkable assertion about the component's observable behavior or
> state**, bound to **one subject**, expressed as **one specification-level obligation** — one
> precondition, one postcondition, or one invariant (NOT the solver VCs it expands into) — and
> **anchored to its source**.

All five: (1) **atomic** — one obligation, not a bundle, not a code fragment; (2) **subject-bound** —
one public operation OR one named global invariant; (3) **observable & falsifiable** — a counterexample
must be *possible*; reject tautologies, type facts, and any precondition so strong it admits no inputs
(vacuous); (4) **decidable** by a verifier; (5) **source-anchored** — spec: FR/US/AS/SC; code: `fn`+line;
harness: the assertion.

## Granularity — fixed
**One property = one obligation per (subject × kind).** Subjects = {each public operation} ∪ {each named
global invariant}. Bundle clauses of the same obligation; split distinct ones. (Count is not the goal;
coverage is.)

## Completeness — coverage by construction (do this; don't rely on noticing)
1. **Coverage ledger.** Walk **every unit of the source artifact**; each maps to ≥1 property OR is listed
   under *Not verifiable* with a reason — **nothing unaccounted**. Units by artifact:
   - **spec** → each FR, user story, acceptance scenario, edge case, clarification
   - **code** → each public fn, each branch/error-return, each field, each state transition
   - **harness** → each assertion / `#[ensures]` / `#[requires]` / goal
2. **Per-operation rubric.** For each operation ask the fixed five: (a) precondition to call it;
   (b) success postcondition; (c) **each** error case + its trigger; (d) **frame** — what must NOT change;
   (e) invariants it must preserve.
3. **Invariant sweep.** Walk **every data field** (its legal range/relation) and **every state +
   transition** (which are legal) to derive global invariants.

## Output — one YAML file (no `.md`)
Write **exactly one** file: the machine-readable, shareable YAML at the `<output file>` path the caller
passed (e.g. `spec_properties.yaml` or `code_properties.yaml`). This is what `build-property-inventory`
reconciles into `unified_properties.yaml`. Do **not** also emit a `.md` — the YAML is the artifact and the
HTML (rendered downstream) is the human-readable form.

One record per verifiable obligation and one per not-verifiable unit — record count must equal
`counts.total`, and the `verifiable: true` count must equal `counts.verifiable` (integrity rule).
```yaml
# header comment block — avoid the literal tokens id:/verifiable: true/verifiable: false in prose here
# so a plain editor Cmd+F over the file counts only real records
component:  <name>
source:     spec | code | harness        # which single artifact this extraction saw
artifact:   <path read>
pin:        <commit/date of the artifact read>
method:     blind-extraction             # this file is ONE blind pass; no cross-artifact reconciliation
generated:  <ISO date>
counts: {total: <n>, methods: <n>, verifiable: <n>, not_verifiable: <n>}
properties:
  - id:         <COMPONENT-SUBJECT-KIND>   # stable, semantic; never renumbered on reorder
    subject:    <public op OR named global invariant>
    kind:       precondition | postcondition | error-case | frame | invariant
    verifiable: true
    statement:  >
      <the obligation in FULL, self-contained plain English — see the rule below>
    traces:     [<FR-nnn / US-n / AS-n / SC-n>  (spec)  |  <fn+line>  (code)  |  <assertion>  (harness)]
  - id:         NV-1                        # not-verifiable ledger entry
    scope:      <the unit this covers>
    kind:       not-verifiable
    verifiable: false
    reason:     >
      <why it is not machine-checkable — reuse the Not-verifiable list below>
    traces:     [<source unit>]
```
The YAML is a faithful reformat of the obligations you extracted — do **not** re-extract differently to
produce it.

### YAML safety — quote any scalar that contains a colon-space (mandatory)
The values you write for `statement`, `reason`, `scope`, `subject`, and `note` are prose, and prose often
contains `": "` — *"Edge case: high contention"*, *"Assumption: caller performs the I/O"*, *"post: get(k)=v"*.
An **unquoted** scalar containing `": "` is parsed by YAML as a nested mapping and the whole file fails to
load (`mapping values are not allowed here`). Rules, applied to every scalar value you emit:
- If the value contains `": "` (colon followed by space) or a leading `? `, `- `, `[`, `{`, `#`, `&`, `*`,
  `!`, `|`, `>`, `@`, `` ` ``, quote it. The safe default is the **block scalar** already shown for
  `statement`/`reason` (`>`-folded on the next line, indented) — a block scalar needs no inner quoting and
  is the preferred form for any full sentence.
- For a **one-line** value that must stay inline (e.g. `scope:`, `subject:`), wrap it in **double quotes**
  and escape any embedded `"` as `\"`: `scope: "Edge case: high-contention eviction"`.
- Never leave a colon-bearing sentence bare after `scope:`/`subject:`/`note:`. This is the single most
  common way these files come out malformed.
Before finishing, mentally (or by a quick parse) confirm the file loads — a file that does not parse is not
a deliverable.

### The `statement` must be readable by a non-specialist (mandatory)
Every `statement` (and every `reason`) is a **full, self-contained sentence a non-specialist can
understand without the spec, the code, or any FV/tooling knowledge in front of them.**
- Write what the operation guarantees, in plain words: name the operation, the condition, and the
  outcome. *"After `insert(key, value)` succeeds, looking up `key` returns exactly that `value`, and no
  other entry in the map changes."* — not *"post: get(k)=v ∧ frame(m\k)"*.
- **No bare symbols, no jargon shorthand** as the whole statement (`∀`, `frame`, `WF`, `post:`, VC
  names). If a term is unavoidable, gloss it in the same sentence.
- **Self-contained:** do not require the reader to open FR-012 or `map.rs:88` to know what is being
  promised — the traces are provenance, not the explanation.
- One obligation per statement (granularity rule below still holds); just say it in English.

## Not verifiable (list here; don't force into rows)
Unbounded liveness / deadlock-freedom; wall-clock **timing** (a timeout's *occurrence* is verifiable, its
*duration* is not); caller/environment **assumptions** (I/O, allocation, pointer validity); pure
layout/size facts unless they gate behavior; logging (except a negative "does not log on error path");
non-deterministic / relaxed-ordering quantities.

## Method
1. **Discover** — read the artifact; note every candidate property *and* anything surprising
   (extra/undocumented behavior, missing guard, contradiction).
2. **Cover** — build the ledger, apply the rubric per operation, run the invariant sweep.
3. **Normalize** — one obligation per cell; drop non-falsifiable ones to *Not verifiable*; keep surprises
   as their own rows/notes.
4. **Write** the one YAML file at the requested output path, with a source on every record and a
   full plain-English `statement`. Read no files other than the named artifact.

## Harness note
A property = *what an assertion / `#[ensures]` actually checks*. A harness property with no counterpart in
spec or code = the harness verifies something unintended (a refinement gap) — flag it.
