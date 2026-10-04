---
name: convert-lamport
description: Convert an existing prose, flat, or loosely organized mathematical proof into a source-mapped Lamport-style hierarchy without repairing or completing its mathematics. Use when a submitted proof needs a traceable hierarchical rendering before a forward Lamport audit or for clearer presentation. Do not use to invent a proof, certify validity, or restructure an already hierarchical proof merely to audit it.
---

# Convert a Proof to Lamport Style

## Mission

Render an existing proof as a Lamport-style hierarchy while preserving its theorem, route, assumptions, logical strength, omissions, and defects. Account for every proof-bearing source segment and make every introduced structural step traceable.

This is a provenance-preserving conversion, not a proof repair or validity audit. A clean hierarchy can expose a gap; it cannot close one.

## Boundaries

Do not:

- invent or repair an inference;
- add a hypothesis, lemma, witness, case, definition, citation, or side condition that the source does not supply;
- silently choose among materially different readings;
- reorder claims to legalize a dependency or hide a scope problem;
- replace the submitted route with a stronger, shorter, or more familiar proof;
- treat an unavailable citation as a remembered theorem;
- call the result valid, established, proved, verified, or machine checked merely because it has been converted.

Preserve false, circular, overstated, and unsupported steps as source-mapped claims with explicit support defects. If the user asks to correct the mathematics, finish this source-faithful rendering first and keep any proposed repair separate.

## Routing

- Use this skill when an existing ordinary or loosely organized proof needs a source-mapped Lamport-style rendering.
- If the submitted proof is already hierarchical and the task is to judge it, use `$forward-lamport` directly.
- Use `$forward-lamport` after conversion to audit hierarchy, scope, constructs, and local validity.
- Use `$reverse-lamport` for a conclusion-first bounded obligation graph. In a full workflow, run it after `$forward-lamport`.

Conversion status is independent of audit verdicts. `SOURCE-MAPPED` does not imply forward `PASS` or reverse `FOLLOWS`.

## Required input

Use the exact theorem statement, the submitted proof text, any definitions or cited material that the user places in scope, and the accepted primitives explicitly supplied for the task. Never infer a broad background theory from the subject area or from a word such as “standard.”

If the theorem or proof is absent, do not supply one from general knowledge. Return `NOT SOURCE-MAPPABLE` and identify the missing input. `NOT SOURCE-MAPPABLE` is a pre-rendering stop: missing required input is a source-boundary condition, not an `OPEN` proof obligation inside a submitted route. Do not assign the absence an `OBLIGATION`, source-support status, issue identifier, or register entry. If part of a submitted proof route is usable, convert that material and expose defects within that route through the status and issue register instead.

## Conversion model

### Rendering status

Choose exactly one:

- **SOURCE-MAPPED** — Every proof-bearing source segment is placed, and every rendered assertion or structural step traces to source material or to an explicit obligation. Gaps, admissions, and unavailable citations may remain.
- **PARTIALLY SOURCE-MAPPED** — A useful hierarchy can be rendered, but at least one material source segment is unplaced or has multiple materially different readings that cannot be conservatively represented as one proof route.
- **NOT SOURCE-MAPPABLE** — The theorem or proof is missing, unreadable, or too indeterminate to support a defensible hierarchy.

Judge only traceability when assigning this status. Do not lower or raise it because the proof appears mathematically correct or incorrect.

### Mapping kinds

Assign each source-to-step ledger row exactly one mapping kind:

- `DIRECT` — The rendered content closely restates an explicit source claim, assumption, justification, or transition.
- `NORMALIZED` — Notation or syntax is standardized without changing proposition, quantifier scope, domain, or logical strength.
- `STRUCTURAL` — A hierarchy marker or construct such as `ASSUME/PROVE`, `CASE`, `SUFFICES`, or `Q.E.D.` makes organization already encoded by the source explicit.
- `OBLIGATION` — A placeholder records support that the source route requires but does not provide. It is not a supplied proof step and must not be presented as one.

`STRUCTURAL` permits only organizational scaffolding. It cannot introduce a new mathematical bridge. When a proposed parent-child relationship would itself assert an unstated implication, record an `OBLIGATION` instead.

Classify mathematical content separately from organizational scaffolding. Include the rendered theorem contract in this accounting. When `DIRECT` and `NORMALIZED` both seem plausible, use `NORMALIZED` if the rendering standardizes the source's notation or syntax; reserve `DIRECT` for content whose source form is closely retained. If one source item both undergoes such normalization and motivates a Lamport construct, use separate ledger rows: `NORMALIZED` for the unchanged proposition and `STRUCTURAL` for the construct. Do not let `STRUCTURAL` absorb source-content normalization.

Every nonclosed issue identifier must appear on at least one `OBLIGATION` ledger row. If the source also supplies the affected claim, citation, admission, or ambiguous wording, preserve that content on a separate `DIRECT` or `NORMALIZED` row; a source-content row does not replace the obligation row. Reuse the same issue identifier on the obligation row and wherever the same defect propagates.

### Source-support statuses

Assign each rendered claim or obligation exactly one source-support status:

- `EXPLICIT` — The relevant claim and its stated support occur explicitly in the supplied material.
- `IMPLICIT` — The relationship is necessarily encoded by the source's grammar or organization, though not stated verbatim. This describes provenance, not logical validity.
- `EXTERNAL UNAVAILABLE` — The source invokes external material whose exact statement or proof is not supplied.
- `ADMITTED` — The source expressly postpones, assumes, or omits the support.
- `OPEN` — The source asserts or needs the item but supplies no support. Words such as “clearly” or “obviously” do not by themselves supply support.
- `AMBIGUOUS` — The source supports multiple materially different readings and does not select one.

Use stable identifiers for every nonclosed support item, numbered independently by prefix in first-source order:

- `GAP-001`, `GAP-002`, ... for `OPEN`;
- `AMB-001`, `AMB-002`, ... for `AMBIGUOUS`;
- `EXT-001`, `EXT-002`, ... for `EXTERNAL UNAVAILABLE`;
- `ADM-001`, `ADM-002`, ... for `ADMITTED`.

Do not use an issue identifier for `EXPLICIT` or `IMPLICIT` support.

Assign one identifier per underlying source-support defect and reuse it everywhere that same defect appears or propagates. Split identifiers only for logically independent missing, ambiguous, external, or admitted items; do not create separate IDs merely for the statement, applicability check, and downstream effects of one unavailable citation.

When one source span has independent defects, use separate ledger and register items rather than forcing one row to carry two statuses. In particular, an assertion whose exact proposition is `AMBIGUOUS` and whose proof is also absent requires both an `AMB-...` item for the reading and a `GAP-...` item for the unsupported inference. Ambiguity must not conceal missing support, and missing support must not be used to choose a reading.

## Procedure

### 1. Freeze the source contract

Record without strengthening or weakening:

- the theorem, quantified variables, and domains;
- hypotheses, definitions, and ambient conventions explicitly supplied;
- the accepted primitives explicitly supplied, without enlarging them;
- the exact proof and any cited material in scope;
- any genuinely unavoidable conservative transcription assumption.

Do not resolve a nonstandard undefined term silently. Mark a material unresolved reading `AMBIGUOUS`.

### 2. Inventory the source

Split the proof into proof-bearing segments in source order and assign `SRC-001`, `SRC-002`, and so on. Include assertions, assumptions, justifications, case boundaries, witnesses, definitions, citations, admissions, and conclusion transitions. Expository text may be grouped, but no mathematical content may disappear.

For each segment, record a minimal identifying quotation or precise paraphrase and its role. Do not quote more text than needed for traceability.

### 3. Render the hierarchy

Use standard Lamport labels and constructs when the source supports them. Preserve the source's dependency order and local scopes. A rendered step may be:

- a source-supplied claim with its source-supplied proof or citation;
- structural scaffolding tied to identified source segments;
- an explicit obligation with an issue identifier where support is absent.

Never make a gap look proved. Put an issue marker at the exact point where support is missing, for example:

```text
⟨2⟩1. Required bridge proposition
        Proof: OPEN — GAP-001; no support supplied in the source.
```

If a source sentence compresses several logically distinct claims, split it only when each rendered claim remains traceable to that sentence. If splitting reveals an unstated bridge, add an obligation instead of inventing the bridge.

If ambiguity prevents one faithful hierarchy, render only the common unambiguous structure, list the competing readings under `AMB-...`, and use `PARTIALLY SOURCE-MAPPED`.

#### Preserve construct semantics

Structural scaffolding must itself be a legal Lamport hierarchy. Do not introduce an illegal cross-level citation merely to display the source. If the source depends on a private, future, or otherwise unavailable claim, preserve that dependency as an explicit scope defect or `OPEN` obligation; do not encode it as a valid citation or move the claim to repair it.

- **`ASSUME/PROVE`:** The parent step asserts the discharged implication, quantified claim, or local sequent. Its children are visible only while proving that local goal. An internal `Q.E.D.` closes the local goal, and only the completed parent step is exported; later siblings must not cite its private descendants.
- **`Q.E.D.`:** It asserts exactly the current goal and may cite only legally visible established steps. A `Q.E.D.` outside a subproof cites the completed parent `ASSUME/PROVE` step, not that step's children. If no legal closing route is supplied, attach an explicit obligation instead of manufacturing a citation.
- **`SUFFICES`:** Use it only when the source indicates that reduction. Its proof must establish the reduction to the old goal before any assumptions local to the new goal are available. An unsupported bridge is `OPEN`.
- **`PICK`:** Expose the required existence proof before the witness enters scope. If that proof is open, retain downstream source uses of the witness but mark them as dependent on the failed introduction; do not treat the witness as legally available.
- **`CASE`:** Preserve only source-supplied cases. If exhaustiveness is not supplied, add an open coverage obligation; never invent a missing case.
- **`DEFINE`:** Introduce only definitions present in the source, in the scope in which the source makes them available.

Existing unambiguous Lamport labels and scopes should remain unchanged. Otherwise assign labels consistently, keep source order, and check every generated citation against its level and scope before freezing the rendering.

### 4. Build the mapping ledger

Account for both directions:

- the rendered theorem contract maps to the source theorem, including any `NORMALIZED` change in notation or syntax;
- every `SRC-...` segment maps to at least one rendered step, register item, or explicit statement that it is purely expository;
- every rendered mathematical assertion maps to the source theorem, at least one `SRC-...` segment, or an identified `OBLIGATION`;
- every `STRUCTURAL` step lists the source segments whose organization it exposes;
- every `GAP-...`, `AMB-...`, `EXT-...`, or `ADM-...` issue has an `OBLIGATION` row for the exact unresolved support or disambiguation task, separate from any row that preserves source-supplied content;
- no obligation is counted as source-supplied evidence.

The ledger must make duplicated, merged, split, normalized, and unplaced material visible.

### 5. Freeze the audit handoff

After rendering, freeze:

- the exact theorem contract;
- the rendered proof, including labels;
- the source-to-step ledger;
- all issue identifiers and support statuses;
- the exact accepted primitives;
- the supplied external-material boundary.

An ensuing audit must inspect this unchanged rendering. Source quotations and mapping annotations establish provenance only; they are not additional premises and cannot discharge an obligation.

When both audits are requested, use this order:

1. `$convert-lamport`
2. `$forward-lamport`
3. `$reverse-lamport`

Report the conversion status and both audit verdicts independently.

Gate the handoff by conversion status:

- For `SOURCE-MAPPED`, audit the exact frozen rendering normally.
- For `PARTIALLY SOURCE-MAPPED`, audit only the exact defensible rendering that was produced and keep every unresolved reading or unplaced dependency open; do not select a completion for the auditor.
- For `NOT SOURCE-MAPPABLE`, stop. There is no rendered proof to pass downstream, so do not fabricate a forward or reverse audit.

## Output format

For `SOURCE-MAPPED` and `PARTIALLY SOURCE-MAPPED`, produce the seven sections below in order.

For `NOT SOURCE-MAPPABLE`, the seven-section template does not apply. Produce only the rendering status, the exact supplied source boundary and missing required input, and a stop statement that no Lamport hierarchy or auditable rendering was produced. Do not create a source inventory, hierarchy, mapping ledger, mapping kinds, source-support statuses, issue identifiers, or gap and ambiguity register when no defensible proof rendering exists.

### 1. Rendering status

State exactly one rendering status and briefly identify any material traceability limit. Include this sentence:

> This status concerns source mapping only; it is not a validity verdict.

### 2. Frozen source contract

State the exact theorem, hypotheses, domains, definitions, accepted primitives, included proof text, and external-material boundary. List conservative transcription assumptions, if any.

### 3. Source inventory

| Source ID | Source segment | Role | Placement |
| --- | --- | --- | --- |

Use `Placement` to name rendered step labels, issue IDs, or `expository only`. Mark any unplaced segment explicitly.

### 4. Lamport-style rendering

Give the source-faithful hierarchy. Attach `GAP-`, `AMB-`, `EXT-`, or `ADM-` markers at the affected proof locations rather than hiding them in later commentary.

### 5. Source-to-step mapping ledger

| Rendered step / item | Source ID(s) | Mapping kind | Source support | Issue ID | Notes |
| --- | --- | --- | --- | --- | --- |

Use only the defined mapping kinds and support statuses. Use `—` when no issue ID applies.

### 6. Gap and ambiguity register

For each issue, state:

- the exact missing, admitted, or ambiguous proposition; for unavailable external material whose content is unknown, state the exact meta-obligation to obtain it and check that it supplies the affected target;
- where it occurs in the rendering;
- which source segment exposes it;
- what later rendered steps depend on it;
- what source material would be needed to close or disambiguate it.

Do not propose a mathematical repair unless the user separately asks for one.

### 7. Frozen audit handoff

State what the next audit must treat as fixed and repeat that mapping metadata is not proof evidence. If the status is `NOT SOURCE-MAPPABLE`, state that no auditable Lamport rendering was produced.

## Worked reference

Read [references/worked-rendering.md](references/worked-rendering.md) when calibrating the output format or deciding how to preserve an assertion introduced only by “clearly.” The example deliberately leaves `x^2 \ge 0` as an open support obligation rather than proving it during conversion.

## Operating principles

- Fidelity outranks elegance.
- Structural explicitness must not change mathematical content.
- A source assertion can be mapped even when its support is open.
- “Implicit” records a source relationship; it does not certify a valid inference.
- Conversion exposes gaps for later audit instead of laundering them into proof steps.
