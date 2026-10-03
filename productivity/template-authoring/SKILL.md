---
name: template-authoring
description: >
  This skill should be used when the user asks to "create a template", "design a template",
  "constrain archetypes into a template", "review a template", "categorise a dataset with CGEM",
  "should this be persistent, episodic or event?", "split this form across compositions",
  "sketch a template from this form / which archetypes does this form need",
  or "work with OET / .t.json / OPT / web-template files" — OET authoring, constraint review,
  the form → template-sketch inverse workflow, and reading the tool-generated serialisations.
  Use `/ckm-search` to find existing CKM templates and `/openehr-explain` to explain one; this
  skill is for authoring and constraining new OET designs.
argument-hint: "<task: create|review|from-form> [template-id, use-case, or form text/path]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - mcp__openehr-assistant__ckm_template_search
  - mcp__openehr-assistant__ckm_template_get
  - mcp__openehr-assistant__ckm_archetype_search
  - mcp__openehr-assistant__ckm_archetype_get
  - mcp__openehr-assistant__guide_get
  - mcp__openehr-assistant__type_specification_get
  - mcp__openehr-assistant__terminology_resolve
---

# Template Authoring

## Conflict Resolution

When guides conflict, apply this priority (highest first):
1. Rules and syntax specifications
2. Idioms and structural constraints
3. Principles
4. Convenience

## Step 1: Load Guides (MANDATORY)

Before any template work, load the authoritative guides:

```
guide_get("openehr://guides/templates/principles")
guide_get("openehr://guides/templates/rules")
```

Load additional guides as needed:
- `guide_get("openehr://guides/templates/oet-syntax")` — OET authoring syntax
- `guide_get("openehr://guides/templates/oet-idioms-cheatsheet")` — common OET patterns
- `guide_get("openehr://guides/templates/cgem-framework")` — full CGEM dataset-splitting framework (Step 6)
- `guide_get("openehr://guides/templates/opt-structure")` / `guide_get("openehr://guides/templates/web-template")` — runtime forms (OPT, web template) when discussing deployment or FLAT/STRUCTURED paths

## Step 2: Research Before Creating

Search for existing templates first:

```
ckm_template_search("<use-case>")
```

If creating a new template, search for archetypes to include:

```
ckm_archetype_search("<concept>")
```

**When CKM comes up empty**, published-on-GitHub project content is a secondary channel — repositories tagged with the **`openehr-content`** topic (search `topic:openehr-content`, ~14 repos: freshEHR, Apperta-CKM projects, regional programmes, individual modellers). CKM holds relatively few templates, so this is more often useful for templates than for archetypes. Treat finds as **leads, not governed artefacts**: unlike CKM there is no editorial review, no reliable `lifecycle_state`, and no integrity guarantee, so cite the repo and commit you looked at, never present a find as "published". This needs web access (`WebSearch`/`WebFetch`/`gh`), which this skill does not hold — ask the main session to run the search.

## Step 3: Use-Case Specificity

Templates target particular clinical workflows. Define the use-case clearly:
- What clinical scenario does this template serve? (e.g., discharge summary, vital signs form, medication reconciliation)
- What data points are required vs optional?
- Who will use it? (clinician, nurse, admin)

## Step 4: Archetype Aggregation

### Selecting Archetypes
- Choose archetypes that precisely fit the use-case
- Minimize archetype count — each should serve a clear purpose
- Prefer well-established CKM archetypes over custom ones

### COMPOSITION Structure
Templates are rooted in a COMPOSITION archetype. Nest entry archetypes (OBSERVATION, EVALUATION, INSTRUCTION, ACTION) and CLUSTER archetypes within it.

Use `type_specification_get` to verify COMPOSITION structure when needed.

## Step 5: The Narrowing Principle

Templates constrain archetypes — they NEVER expand:
- **Mandatory stays mandatory**: Cannot make required fields optional
- **Optional can become mandatory**: Can set `min=1` on optional fields
- **Optional can be excluded**: Set `max=0` to hide fields
- **Value sets only narrow**: Can restrict coded text options, never add new ones
- **Cardinality only narrows**: Can reduce max occurrences, never increase beyond archetype definition
- **Tightening unconstrained RM attributes is allowed**: constraining an RM attribute the archetype left open is still narrowing

A template's four jobs (Archetype Technology Overview): **composition** (fill slots), **element choice** (remove/mandate/leave optional), **narrowing**, and **setting defaults**.

### Defaults vs assumed values
Set a **default value** (OET: `default="..."` on a `<Rule>`) where the use case fixes or strongly implies a single value (e.g. setting, patient position). Defaults **appear in the recorded data**; archetype-level *assumed values* are semantic fallbacks for omitted optional items and do **not** appear in the data — never confuse the two.

## Step 6: CGEM Framework

Use CGEM (freshEHR's analysis method — a design aid, **not** an openEHR specification) to decide how a dataset splits across templates, and to set each template's composition category. Load `guide_get("openehr://guides/templates/cgem-framework")` for the definitions, mapping table and caveats:

| CGEM category | Data nature | `COMPOSITION.category` | Versioning behaviour |
|----------|-------------|---------------|---|
| **Global Background** | True across all contexts for the patient's whole life (allergies, problem list, CPR/ReSPECT decision, current medications) | `persistent` (431) | One current version per patient, updated in place |
| **Contextual Situation** | Single source of truth for one care journey / episode / condition (diagnosis-and-staging summary, condition care plan) | `episodic` (451) | One current version per journey; a new journey creates a new instance |
| **Event Assessment** | Discrete, repeated recordings at a point in time (vitals at a visit, lab result, assessment score) | `event` (433) | New composition per submission; never overwritten |
| **Managed Response** | Formal order/fulfilment cycle tracked from request to completion (referral, prescription, investigation request) | **not a category code** — usually `event` (sometimes `persistent`) | Order state tracked across ACTIONs via the ISM |

Applying it: inventory the datapoints → categorise each C/G/E/M → group same-category datapoints into candidate templates → set each template's category to match → decide reuse (Global Background is usually already modelled and often only *read* by the form; Event templates are prime reuse candidates) → confirm Managed Response items genuinely need INSTRUCTION/ACTION + ISM and downgrade the rest to simple records.

Three things to state explicitly in any split report:
- **Four CGEM categories, three category codes** — Managed Response is not a `COMPOSITION.category`; it is an `event` (or `persistent`) composition distinguished by its INSTRUCTION/ACTION entries and the ISM.
- **`451 episodic` is normative but unevenly implemented** — confirm the target platform supports it; `persistent` plus governance conventions is the common fallback.
- **One form commonly spans several compositions** across several categories, so a single form rarely means a single template.

## Step 6b: Template from a form (inverse workflow)

When the starting point is a clinical form to implement rather than a template design, **load [`references/template-from-form.md`](references/template-from-form.md)** and follow it: parse the form into a field inventory, run the CGEM dataset split (Step 6) *first*, then sketch each implied template — archetypes to aggregate, RM entry type per field group, narrowing notes. Step 1's mandatory guide loads still apply in this mode (plus the CGEM guide — the reference covers it). The output is a design sketch, never OET XML; once the user confirms the sketch, continue at Step 8b to emit the file.

## Step 7: Terminology in Templates

- Prefer DV_CODED_TEXT over free text where possible
- Constrain value sets to the local clinical context
- Use `terminology_resolve` to verify **openEHR** terminology bindings inherited from archetypes — openEHR terminology only; it errors on external codes, so check SNOMED CT / LOINC / ICD bindings against the archetype's own `term_bindings` rubrics instead

## Step 8: The four serialisations

One design intent, four serialisations at three layers — **not** interchangeable, and only OET is hand-authorable:

| Format | Layer | Purpose |
|--------|-------|---------|
| **OET** (`.oet`) | source | Authoring format — human-editable XML referencing archetypes plus narrowing. The artefact to version |
| **Archetype Designer `.t.json`** | source | AOM2 **differential** template JSON (`@type: TEMPLATE`, `parentArchetypeId`, `differential: true`, `templateOverlays`) — the JSON analogue of OET, from Better's Archetype Designer ("Export Fileset"). Tool-managed: read and review it, but make design edits in the tool or in an OET |
| **OPT** (`.opt`/`.optx`/`.optj`) | compiled | Operational Template — flattened, self-contained runtime artefact the CDR validates against (XML in ADL 1.4 practice; OPT2 adds ADL/XML/JSON, and raw vs profiled variants). Generated, never hand-authored |
| **Web Template** (JSON) | derived runtime | Better/EHRbase simplified projection **of the OPT** for UI generation; its node ids define the FLAT/STRUCTURED path schema. Derived, lossy, never authored |

```
OET (or .t.json) + archetypes  ──►  OPT  ──►  web template
```

**`.t.json` is not a web template** — it sits at the *source* layer with slots intact, while a web template is flattened runtime JSON with `aqlPath`/`inputs`. Both come from Better, at opposite ends of the pipeline; "the Better template" is ambiguous, so always name which one.

For when each format is hand-authorable vs tool-generated and what checksums each carries, load `guide_get("openehr://guides/templates/serialization-formats")`; for the runtime forms in depth, `guide_get("openehr://guides/templates/opt-structure")` and `guide_get("openehr://guides/templates/web-template")`. Reference syntax guides:
```
guide_get("openehr://guides/templates/oet-syntax")
guide_get("openehr://guides/templates/oet-idioms-cheatsheet")
```

## Step 8b: Emit the OET

Produce a real, slot-correct OET — not just a design sketch. (The from-form mode in Step 6b produces the sketch; this step turns a confirmed design into the file.) Following `templates/oet-syntax`:

1. Root `<template>` with a root **COMPOSITION** archetype reference and a fresh `<id>` (see UID note below).
2. A `<Content>` entry per included archetype, nested to mirror the COMPOSITION → SECTION → ENTRY → CLUSTER structure.
3. `<Rule path="…">` elements for each narrowing constraint (`min`/`max`, `limitToList`, unit hardening, `hide_on_form`, label overrides, `default="…"` for use-case-fixed values) — respecting the narrowing principle (Step 5).
4. A trailing `<Context>` if the design needs composition context (e.g. `/context/setting` fixed to a code).

There is **no automated OET/OPT validator** available, so validate manually against the loaded `templates/oet-syntax` guide and the Step 9 checklist; state any unconfirmed constraint rather than asserting validity.

## Step 9: Quality Review

Run through the quality checklist:

```
guide_get("openehr://guides/templates/checklist")
```

Verify:
- [ ] Clear use-case definition
- [ ] Appropriate archetype selection
- [ ] Narrowing principle respected (no expansions)
- [ ] Required fields marked correctly
- [ ] Excluded fields set to max=0
- [ ] Terminology constraints appropriate for context
- [ ] Value sets verified (quantity constraints, unit hardening, "limit to list" coded text)
- [ ] Defaults set where the use case fixes a single value (setting, patient position); no assumed-value confusion
- [ ] Annotations and UI hints appropriate (hide_on_form, contextual label overrides)
- [ ] Valid OET syntax

## Output

Generate valid OET files. Use the Write tool to create `.oet` files in the appropriate project location.

### Identifiers and checksums
- A new template needs a fresh `uid` — mint a random UUID (v4). If a shell is available, `uuidgen` (or `python3 -c 'import uuid; print(uuid.uuid4())'`) works; otherwise generate the UUID directly (this skill has no `Bash` tool, so don't assume shell access).
- Do not hand-write build checksums (`MD5-CAM-*`, `build_uid`) — they are tool-computed; a missing/stale checksum is advisory and never blocks authoring the OET.
