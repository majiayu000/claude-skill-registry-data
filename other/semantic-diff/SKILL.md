---
name: semantic-diff
description: >
  This skill should be used when the user asks to "diff two archetypes", "compare two
  templates", "what changed between these two versions", "is this a patch, minor or major
  bump?", "how compatible are these two artefacts?", or invokes `/semantic-diff`.
  Auto-detects archetype vs template (any serialisation) and version vs sibling comparison,
  then reports a version-bump verdict (rule G1) or a compatibility report with a
  path-compatibility table. Not a textual/git diff; to review or fix a single artefact,
  use the `archetype-authoring` or `template-authoring` skill.
argument-hint: "<file-a> <file-b>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__ckm_template_get
---

# Semantic Diff

Compare two openEHR artefacts at the **semantic** level — not textual. Auto-detect whether the inputs are **archetypes** (ADL) or **templates** (OET, `.t.json`, OPT, web template), and whether the comparison is between two **versions** of the same concept or between **siblings / distinct concepts**, then produce the appropriate report.

## Instructions

1. Parse **$ARGUMENTS** into `<file-a>` and `<file-b>`. When invoked from conversation rather than `/semantic-diff` (no arguments), take the two artefact paths (or CKM ids) from the user's request. If only one artefact is identifiable, ask the user for the second and stop.
2. `Read` both files.
3. `Read` the rubric bundled with this skill — [`references/semantic-diff-rubric.md`](references/semantic-diff-rubric.md). Follow its classification rules exactly.
4. **Detect the artefact type** from the file content/extension:
   - **Archetype** — ADL source (`.adl`; `archetype (...)` header, `definition`, `term_definitions`). Load the archetype rules guide:
     ```
     guide_get("openehr://guides/archetypes/rules")
     ```
   - **Template** — one of four serialisations; load the template rules guide, plus the serialisation map when the pair is not OET:
     ```
     guide_get("openehr://guides/templates/rules")
     guide_get("openehr://guides/templates/serialization-formats")
     ```
     - **OET** (`.oet`) — authoring XML, `<template>`: diff archetype includes and `<Rule>` narrowing.
     - **`.t.json`** — Archetype Designer **source** template (AOM2 differential JSON: `@type: TEMPLATE`, `parentArchetypeId`, `differential: true`, `templateOverlays`): diff the root `definition` and the per-archetype overlays. It is *not* a web template.
     - **OPT** (`.opt`/`.optx`/`.optj`) — compiled operational template with archetype constraints inlined; also `guide_get("openehr://guides/templates/opt-structure")`. Differences here may come from a recompile rather than a design change, so say which; a raw-vs-profiled OPT pair differs in retained languages/bindings, not in design.
     - **Web template** (derived runtime JSON: `templateId`, `webTemplate`/`tree`, per-leaf `inputs`, `aqlPath`) — generated from an OPT; also `guide_get("openehr://guides/templates/web-template")`. Diff it only to assess **FLAT/STRUCTURED path-schema impact** on clients; never treat a web-template delta as the design delta, and point the user at the OET/`.t.json` pair for that.
   - Different serialisations of the same design are **not** comparable node-for-node (a `.t.json` keeps slots that its OPT has inlined). If the two files are different artefact types (e.g. an ADL vs an OPT, or an OET vs its own web template), report the mismatch, say which layer each sits at, and ask the user to confirm intent before proceeding.
5. **Detect the comparison mode** from the root identifiers:
   - **Version mode** — same root concept / archetype id / template id, differing version (or differing revision of the same concept). Use the version-bump workflow in §A.
   - **Sibling / cross-artefact mode** — **different** root concepts (e.g. `...health_summary` vs `...report`, or two distinct templates). Use the compatibility/divergence workflow in §B. Do **not** refuse, and do **not** emit a version-bump verdict — a bump is meaningless across distinct concepts.
6. Produce the report for the detected mode.

## A. Version mode (same concept, different version)

Compare the two artefacts and classify each change per the rubric (major / minor / patch). Then determine the overall bump: any major change → **major**; else any minor → **minor**; else **patch** (rubric rule **G1**).

**Archetype axes:**
- Root concept id and RM entry type.
- At-codes (ids, terms, definitions): added / removed / repurposed / renamed.
- Cardinality, occurrences, existence at each node.
- Value constraints (data types, ranges, units).
- Terminology bindings — when a binding differs, call `terminology_resolve` on both old and new codes and compare concept definitions to decide equivalence. It resolves **openEHR** terminology only and errors on anything else, so for SNOMED CT / LOINC / ICD bindings compare the `term_bindings` entries and their `term_definitions` rubrics instead, and flag the pair for human review when equivalence is not evident.
- Slot constraints.
- Language-specific terms (track translations separately from semantic changes).

**Template axes:**
- Included archetypes (by id) — added / removed / version-bumped.
- Slot fillers — added / removed / reassigned.
- Narrowing per archetype — compare cardinality, occurrences, existence, value sets, terminology bindings. **Stricter** narrowing = major (breaks composition consumers); **looser** = minor (previously-valid instances stay valid); new optional content = minor.
- RM-level composition category (event / persistent / episodic) — a change here is always major.

Use `type_specification_get` when authoritative RM/AM type detail (attributes, allowed structure) is needed to judge a change. Produce the output per the rubric's **Output layout**, adapted for templates with archetype-level grouping where useful.

### Version-mode constraints
- If the two files turn out to have **different** root concepts, do not refuse: emit a one-line note that input concepts differ and the comparison has auto-switched to **sibling mode** (§B), then produce the §B report instead.
- If a **template narrows an archetype beyond what that archetype allows**, flag it as a **validation error** rather than classifying — the template itself is broken.
- OET vs OPT of the *same* template is meaningful but mixes authoring and runtime forms; warn the user that the comparison spans format types.

## B. Sibling / cross-artefact mode (distinct concepts)

The two artefacts are different concepts, so a version bump does not apply. Emit a **compatibility / divergence** report instead (new-feature C1):

1. **Relationship line** — one line classifying the relationship: *same artefact* / *siblings (independent concepts in the same family)* / *one specialises the other* (detect from `specialize`/parent reference in ADL, or shared archetype includes in templates).
2. **Compatibility / divergence report:**
   - **Shared skeleton** — structure/paths (or shared archetype includes) common to both.
   - **Repurposed at-codes** — same at-code id used for a different concept across the two artefacts (a portability hazard).
   - **Additive fields** — paths/at-codes/includes present in one but not the other.
   - **Translation-coverage delta** — per-language `term_definitions` (archetypes) or language metadata (templates) present in one but missing in the other.
3. **Path-compatibility table** — list paths present in **both**, with a per-path verdict:

   | Path | A | B | Verdict |
   |------|---|---|---------|
   | `/data[...]/items[at0004]/value` | DV_QUANTITY {0..1} | DV_QUANTITY {0..1} | compatible |
   | `/...[at0010]/value` | DV_CODED_TEXT | DV_TEXT | type-changed |
   | `/...[at0021]` | present | — | removed |

   Verdicts: **compatible** (same path, type, and compatible constraints) / **type-changed** (path exists in both but RM type or value constraint differs) / **removed** (present in A, absent in B). Use `type_specification_get` to confirm RM-type compatibility where it is not obvious.

### Sibling-mode constraints
- Do **not** emit a patch/minor/major verdict and do **not** reference rule G1 — it is out of scope for distinct concepts.
- If the two later turn out to be the same concept (e.g. one is a renamed copy), note that and switch to version mode (§A).

## Shared constraints

- This is a **semantic** tool: do **not** perform a git-style line-by-line diff. Line numbers are irrelevant.
- When uncertain whether a terminology binding is non-equivalent, resolve both codes via `terminology_resolve` and compare concept definitions before classifying — **openEHR** terminology only (it errors on anything else); for SNOMED CT / LOINC / ICD bindings compare the `term_bindings` entries and their `term_definitions` rubrics instead, and flag the pair for human review when equivalence is not evident.
- When uncertain whether a text change alters clinical meaning, quote both versions and flag for human review — do not auto-classify as patch.
- When a version-mode classification is genuinely ambiguous, report the finding under a **Review needed** group with a targeted question instead of guessing.
- To compare against a published revision the user does not have locally, fetch it with `ckm_archetype_get` (archetypes) or `ckm_template_get` (templates), then diff as above.
