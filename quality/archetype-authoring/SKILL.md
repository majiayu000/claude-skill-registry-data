---
name: archetype-authoring
description: >
  This skill should be used when the user asks to "create", "edit", "specialize",
  "review / remediate", "write the rationale for", "translate / localise", or "fix the ADL
  syntax of" an openEHR archetype (including "this archetype won't parse / won't validate"),
  or to import a CKM archetype into the workspace for reuse. It covers the full
  author → review (lint → fix → re-lint) → rationale → translate lifecycle. To merely explain
  an existing archetype with no edits, use `/openehr-explain` instead.
argument-hint: "<task: create|edit|specialize|review|rationale|translate|import|fix-syntax> [archetype-id or concept]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - WebSearch
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__guide_adl_idiom_lookup
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__examples_search
  - mcp__openehr-assistant__examples_get
---

# Archetype Authoring

## Conflict Resolution

When guides conflict, apply this priority (highest first):
1. Rules and structural constraints
2. Syntax specifications
3. Anti-patterns
4. Principles and examples
5. Convenience

## Step 1: Load Guides (MANDATORY)

Before any archetype work, load the authoritative guides:

```
guide_get("openehr://guides/archetypes/principles")
guide_get("openehr://guides/archetypes/rules")
guide_get("openehr://guides/archetypes/adl-syntax")
```

Load additional guides as needed:
- `guide_get("openehr://guides/archetypes/structural-constraints")` — for cardinality, occurrences, existence rules
- `guide_get("openehr://guides/archetypes/terminology")` — for terminology binding patterns
- `guide_get("openehr://guides/archetypes/anti-patterns")` — to avoid common mistakes
- `guide_get("openehr://guides/archetypes/reference-formatting")` — for ADL formatting conventions

## Step 2: Research Before Creating

Before creating a new archetype, ALWAYS search CKM first:

```
ckm_archetype_search("<concept>")
```

**Reuse-first principle**: If a suitable archetype exists, use it. Only create new archetypes when no existing archetype covers the concept. If a close match exists, consider specialization instead.

**If CKM has nothing**, check the secondary channel before concluding "new": GitHub repositories tagged with the **`openehr-content`** topic (`topic:openehr-content`) publish project-level archetypes and templates outside CKM. These are **un-governed leads** — no editorial review, no dependable `lifecycle_state` — so use them as prior art and style reference, cite the repo and commit, and never call such a find "published". Requires web access, so run it in the main session (`WebSearch`, or `gh` where a shell is available — this skill holds no `Bash`), not in `ckm-scout`.

**For deep reuse surveys** (unfamiliar domain, or the first few hits look marginal), dispatch the `ckm-scout` agent instead of running searches inline. It runs 3 parallel phrasings, ranks candidates, and returns a reuse/specialize/new recommendation — keeping CKM search noise out of this skill's context.

### Consult gold-standard reference archetypes (when applicable)

For a small set of well-curated CKM archetypes — blood pressure, medication order, problem/diagnosis, encounter, procedure, anatomical location (CLUSTER), translation requirements (ADMIN_ENTRY) — try `examples_search(kind="archetypes")` when authoring or reviewing an archetype of the same type. These are native `.adl` files exposed as `openehr://examples/archetypes/{name}` and serve as concrete prior-art references for RM-type intent, terminology binding patterns, and structural idioms. Skip this step when the concept is outside the curated set.

### Import a CKM archetype for reuse

When reuse means pulling a published archetype into the workspace (not just citing it), make it land as a wired-in file rather than a copy-paste note:

1. Fetch the native ADL with `ckm_archetype_get("<id>")`.
2. Write it into the project (e.g. a `local/` directory) under its canonical `openEHR-EHR-<TYPE>.<concept>.v<N>.adl` filename.
3. If it fills a slot in a target archetype/template, add the constrained slot reference (`allow_archetype … include`) so the reuse is actually wired in.

A reused file keeps its published `uid`/checksums; do not alter them.

## Step 3: Concept Design

### One Concept Per Archetype
Each archetype represents exactly one clinical concept. When multiple independent ideas appear, split into separate archetypes connected via slots.

### RM Entry Type Selection
Choose the correct Reference Model entry type:

| RM Type | Purpose | Examples |
|---------|---------|---------|
| OBSERVATION | Measured/observed data | Blood pressure, body weight, lab result |
| EVALUATION | Assessed/interpreted data | Diagnosis, risk assessment, problem |
| INSTRUCTION | Orders/requests | Medication order, procedure request |
| ACTION | Activities performed | Medication administration, procedure |
| ADMIN_ENTRY | Administrative data | Admission, discharge, transfer |
| CLUSTER | Reusable data groups | Address, anatomical location, device |

Use `type_specification_get` to verify RM type structure when uncertain.

**Order vs record**: reserve INSTRUCTION/ACTION for genuine order/fulfilment lifecycles (CGEM "Managed Response"); model one-off assessments and simple records as OBSERVATION/EVALUATION ("Event Assessment"). Do not combine orders and observations in one archetype — see `guide_get("openehr://guides/templates/cgem-framework")`.

### Identifier Scheme
Follow the pattern: `openEHR-EHR-<RM_TYPE>.<concept>.v<VERSION>`

Examples:
- `openEHR-EHR-OBSERVATION.blood_pressure.v2`
- `openEHR-EHR-CLUSTER.anatomical_location.v1`

ADL 1.4 source ids carry the **major version only** (`.v1`, `.v2`); the full 3-part semver form (`.v1.0.0`) is the *physical* HRID from the AM Identification spec, used in ADL 2 and CKM revision metadata — do not put it in an ADL 1.4 `archetype` header.

## Step 4: ADL Authoring

### Constraint Patterns
Use `guide_adl_idiom_lookup` for specific ADL constraint patterns:
- Coded text constraints
- Quantity ranges with units
- Ordinal / rating scales — `DV_ORDINAL` for integer-only steps; **`DV_SCALE`** (RM ≥ 1.1.0) for non-integer steps (e.g. Borg CR10 0.5). See the `DV_SCALE` vs `DV_ORDINAL` idiom.
- Date/time constraints
- Slot definitions

### Terminology Section
- Define all at-codes with clear, descriptive text
- Bind to standard terminologies (SNOMED CT, LOINC, ICD-10) where appropriate
- Use `terminology_resolve` to verify **openEHR** terminology codes only — it does not cover SNOMED CT / LOINC / ICD and errors on an unresolvable input; read external rubrics from the artefact's `term_bindings` instead
- Ensure semantic equivalence, not approximation, in bindings

### Design for Reuse
- Keep archetypes terminology-neutral (avoid hardcoding specific value sets)
- Use explicit slot constraints (avoid open wildcards like `include all`)
- Design for international use — avoid locale-specific assumptions

### Identifiers and checksums
- A new archetype needs a fresh `uid` — mint a random UUID (v4). If a shell is available, `uuidgen` (or `python3 -c 'import uuid; print(uuid.uuid4())'`) works; otherwise generate the UUID directly (this skill has no `Bash` tool, so don't assume shell access).
- **Do not hand-write build checksums** (`MD5-CAM-*`, `build_uid`) — they are tool-computed by CKM/ADL tooling. If editing a published archetype, its checksum simply becomes stale: note that for upstream recomputation rather than inventing a value. This is advisory, not a blocker — a missing/stale checksum never stops local authoring.

## Step 5: Editing Existing Archetypes

When modifying existing archetypes:
- **Path stability**: Never rename or remove existing paths in minor versions
- **Backwards compatibility**: Additions are safe; removals require major version bump
- **Deprecation over removal**: Mark elements as deprecated before removing in next major version

## Step 5b: Fix ADL syntax (syntax-only remediation)

When the ask is to repair an archetype that won't parse or validate structurally — rather than to change what it models — **load [`references/fix-syntax.md`](references/fix-syntax.md)** and follow it exactly. It fixes syntax while preserving clinical semantics (five prohibited actions), and reports semantic findings instead of fixing them. Skip Steps 2–4 in this mode; the guides in Step 1 still apply.

## Step 6: Specialization

When extending via specialization:
- Only specialize for genuine semantic subtypes (e.g., blood_pressure -> invasive_blood_pressure)
- Single inheritance only — one parent archetype
- Preserve parent meaning — specialization narrows, never contradicts
- Maintain transparent lineage in the archetype identifier

## Step 7: Review, remediate & write rationale

When reviewing an archetype for quality, publication, or CKM submission, run the full pipeline. Stages at a glance: **intent & provenance → lint → remediate → review packet**, then optional **rationale prose**. (Provenance is advisory and detailed in the pipeline reference — editing a published CKM mirror diverges from canonical; never a blocker.) For a quick lint with no remediation, use the `archetype-lint` skill (`/archetype-lint`).

- Full pipeline (lint → fix-plan → patch → re-lint → review packet + checklist): **load [`references/review-remediate.md`](references/review-remediate.md)**.
- Drafting description / purpose / misuse / use prose: **load [`references/rationale-prose.md`](references/rationale-prose.md)**.

## Step 8: Translate / add a locale

To add or translate per-language text (`ontology.term_definitions`) for a target language, **load [`references/translation.md`](references/translation.md)** — it covers the three tab-sensitive insertion points and the at-code-parity verification gate. (Translations live in the ontology block in ADL 1.4, not a top-level `terminology` section.)

## Output

Generate valid ADL 1.4 files. Use the Write tool to create `.adl` files in the appropriate project location.
