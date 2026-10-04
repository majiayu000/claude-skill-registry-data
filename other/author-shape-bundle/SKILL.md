---
name: author-shape-bundle
description: Author /shape's selection-and-composition bundle for one domain — confirm or prune each capability against the firmed profile + KB, SELECT which of the functionalities /understand already created to build now, place every functionality into a slice or the _deferred bucket, create the persona and USER journey records, the decisions, AND compose the domain's vertical slices. Every persona record carries structured grounding — goals (outcomes in the person's own words), cares_about (their trust criteria), failure_means (what a miss looks like for them) — read off the capability's ICE and the firmed profile, with description kept to the one-line who-they-are summary. Every slice is a user-facing vertical — it names at least one surface (a screen/view a named persona opens and checks) scaffolded incrementally, and journeys run on those surfaces; a backend-only slice is invalid. Surfaces are NAMED, not designed. Slices reference functionalities by spine id, carry no order/effort/dependencies (that is /roadmap). It does NOT create functionalities or author ICE — /understand did. Under direct-model-write (ADR 026) it writes the per-node RECORDS (each slice, persona, journey, decision, and the _deferred bucket) straight to the live model, with stable ids so re-runs don't duplicate, and emits the spine-delta (capability status flips, the slices index, the refs) as structured data in the manifest — it NEVER writes `_spine.yaml` or the profile. Generative artifact production for the /shape play.
version: 0.4.0
user-invocable: false
model: opus
allowed-tools: Read, Write, Bash, Glob
---

# author-shape-bundle

Turns a firmed domain — capabilities detailed by /understand (each with its functionalities
already created), profile `set` — into a **selection-and-composition bundle**: which
capabilities stay, which are pruned, which existing functionalities to build now, the
personas served, the journeys travelled, the decisions, and the domain's vertical slices.
It reads the profile to judge fit and the KB shelves to ground the selection.

## Altitude — the product owner

/vision was the CXO, /understand the product manager. /shape is the **product owner**: it
decides what gets built and in what shippable shape. It does not detail (that was
/understand) and does not plan order (that is /roadmap). Its output is **deliverable
verticals** — each a thin slice a user can open and check.

## Write discipline — direct-model-write containment split (ADR 026)

Under direct-model-write (`standards/rules/direct-model-write.md`) there is no `draft/` tree.
The split is mandatory:

- You write ONLY the per-node **record files** — each slice record, each persona record, each
  journey record, each decision (ADR) record, and the slice `_deferred.yaml` bucket —
  **straight to the live model** under the domain's home at
  `{product_base}product-os/{domain}/…`. Each is its own file with a stable id, so a re-run
  overwrites its own record and never duplicates.
- You **NEVER** write any shared model file: not `_spine.yaml`, not `profile.yaml`. The spine
  mutation — the capability `status` flips, the persona/journey/decision refs attached onto
  those capabilities, and the `slices` index entries — is the job of /shape's deterministic
  keyed persist script (`persist_shape.py`), which merges it into the live spine in place,
  keyed to the domain. Node-level containment inside the spine (only the named capabilities
  flip, only their status field moves) is the persist's, not yours.
- The spine entries you used to write into a draft `_spine.yaml` are now emitted as
  **structured data in `shape-manifest.yaml`** (a non-model STM artifact) under a
  `spine_delta` block. The keyed persist reads that block and applies it to the live spine.

## What it does NOT do

It does **not create functionalities** and does **not author ICE** — /understand already
created and detailed every functionality (a spine `functionalities` entry + a
`functionality.md`). /shape SELECTS among those and composes them; it never re-makes them.
It also never writes the profile (the box is /understand's; /shape selects against it) and
never cuts epics (/grill) or plans order (/roadmap).

## The always-scaffold-the-UI principle

A slice is a vertical only if a user can OPEN a surface and CHECK its outcome. So every
slice names at least one user-facing surface, and that surface is a **thin scaffold** — the
slice's own piece of the screen, not the whole dashboard. The UI is built up slice by
slice; the full product surface accretes as the slices land. Never cut a backend-only slice
(a pure ingestion or rollup layer with no surface), and never try to deliver "the whole
dashboard" in one slice.

## Inputs

| Field | Required | Description |
|-------|----------|-------------|
| `domain` | yes | The target domain: its id, slug, and the path to its folder under `{product_base}product-os/`. |
| `kb_shelf` | yes | The KB shelf this domain maps to, resolved by the play via `search-kb` (the product domain name is NOT the shelf name). |
| `product_base` | yes | From config. Read the live spine (capabilities + their functionalities, all detailed) and the profile; WRITE each record file (slices, personas, journeys, decisions, `_deferred`) in place under `{product_base}product-os/{domain}/…`. Never write `_spine.yaml` or the profile. |
| `manifest_path` | yes | Output path under STM for `shape-manifest.yaml` — the provenance + the `spine_delta` the keyed persist consumes. |
| `stm_base` | yes | From config. |

## Procedure

Reasoning (keep/prune judgment, which functionalities to build now, naming personas,
sketching journeys, cutting slices toward surfaces) is yours. Schema conformance and stable
ids are non-negotiable.

1. **Read the domain + the profile.** From the live `_spine.yaml`, load the domain's
   capabilities (all `detail: detailed`) and their functionalities, plus the profile box.
   Read the KB shelf via the router (`python3 $KB shelf <kb_shelf>`) for selection grounding.

2. **Confirm or prune each capability.** Against profile fit and the capability's grounding,
   decide `active` (keep) or `deprecated` (prune). Each prune becomes a decision. (Status
   flip only — never edit the capability otherwise; the flip is applied by the keyed persist,
   not by you.)

3. **Select the functionalities to build now.** From the functionalities /understand already
   created under each kept capability, choose which to build in this round. Selecting is a
   prioritization call, not creation — you never make a new functionality here. Every
   selected functionality must land in a slice or the `_deferred` bucket (step 7).

4. **Create personas + user journeys (records, in place).** Write each persona record (who
   the functionalities serve) and each journey record straight to the live model. A journey
   is a **user journey through a surface** — the ordered steps a persona takes ON a named
   surface to reach an outcome, never a backend pipeline. Each journey lists its
   `surface_refs` (the slice surface ids it runs on) and its steps. Stable ids from name/slug.

   **Every persona you write carries structured grounding. This is not optional for you.**
   A persona is WHO the work is for; an intent says what should be true, the persona says for
   whom. Downstream plays read these fields instead of re-deriving the person's goals from
   prose differently every run. Read them OFF the capability's `ice.yaml` (its intent,
   constraints, failure conditions) and the firmed product profile — never invent them. Write
   four things, and keep them separate:

   - `description` — **one line, who they are.** Their role and their relationship to this
     capability. Nothing else. Do NOT cram their needs or their trust criteria in here: those
     have their own fields now, and a description that carries everything is the exact drift
     this replaces. Bad: *"A pilot-team engineer whose machine the collector runs on. They need
     to inspect exactly what leaves that machine, confirm nightly reporting is working, and read
     consistent read-only usage answers with matching CSV."* Good: *"A pilot-team engineer whose
     machine the collector runs on."*
   - `goals` — **3–5 outcomes in THEIR words.** What this person is trying to achieve, stated
     as the end state they want, never as a feature, a screen, or a solution. Say "I know
     exactly what left my machine", not "an egress inspection view". Each goal must trace to
     something the capability's ICE says should be true; if you cannot point at it, it is not
     a goal of this persona.
   - `cares_about` — **the checks they would run before trusting the thing.** What they judge
     it by: accuracy, freshness, reversibility, privacy, cost, speed to an answer, whether two
     views agree. Pull these from the capability's constraints and the profile's non-functional
     stance. These are criteria, not wishes — each should be something a person could actually
     check.
   - `failure_means` — **one sharp sentence: what a miss looks like for THEM.** This is the
     sharpest field and the easiest to write limply. Name the concrete bad outcome they would
     experience, not the absence of a feature. Bad: *"the feature does not work well."* Good:
     *"They ship a report they cannot defend, because the CSV and the on-screen number
     disagree and they had no way to tell which one left their machine."* Ground it in the
     capability's failure conditions.

   `validate_shape.py` warns — it does not error — on a persona missing these three fields,
   because records written before #550 must keep validating. A warning against a persona YOU
   wrote this run is a defect to fix, not noise to carry.

5. **Record decisions (records, in place).** Write one decision (ADR) record per prune and per
   material selection choice, at the right level (capability or functionality), straight to
   the live model.

6. **Compose vertical slices — each with a scaffolded surface (records, in place).** Write
   each slice record straight to the live model, bundling the selected functionalities into
   the domain's slices — **vertical** increments cut TOWARD a user-facing surface, that may
   cross capabilities of THIS domain. For each slice: a stable id, a name, an outcome (the
   usable thing it delivers), the **`surface`** list (≥1 surface, each with a stable `id`, a
   `name`, the `persona_ref` who opens it, and the `user_action`), an `acceptance_intent`, and
   a `functionalities` list where each entry carries the `functionality_ref` (the spine
   functionality id — the reference IS the id; the grounding is its `functionality.md`) and a
   `delivery` flag (`full` | `partial`). NAME the surface, never DESIGN it (no
   wireframes/components — that is /realize's UX lens). The surface is a thin scaffold (this
   slice's piece of screen), not the whole product UI. Wire each surface to a journey. Do NOT
   set `order`, `effort`, or resolved `depends_on` (that is /roadmap). Every selected
   functionality must land in at least one slice OR the `_deferred` bucket.

7. **Write the manifest with the spine-delta.** Write `shape-manifest.yaml` to `manifest_path`
   (STM) carrying the keep/prune list, the grounding per kept capability + selected
   functionality, the slices + deferred bucket, the persona/journey/decision ids, AND a
   `spine_delta` block — the structured spine mutation the keyed persist applies: the capability
   `status` flips, the persona/journey/decision refs to attach onto those capabilities, and the
   `slices` index entries. You write the RECORDS to the live model and the DELTA to the
   manifest; the keyed persist merges the delta into the live spine.

## Output — records on the live model + a manifest

```
{product_base}product-os/
  {domain}/{capability}/
    personas/{persona-id}.yaml                  # persona record (in place on the live model)
    journeys/{journey-id}.yaml                  # journey record (surface_refs + steps)
    decisions/{decision-id}.yaml                # ADR per prune + material selection
  {domain}/slices/{slice-id}.yaml               # slice record (references functionalities by spine id)
  {domain}/slices/_deferred.yaml                # selected-but-not-placed functionalities (if any)

{manifest_path}                                 # shape-manifest.yaml (STM, non-model)
```

You do NOT write `{product_base}product-os/_spine.yaml` or the profile — the keyed persist
writes the spine from the manifest's `spine_delta`.

A persona record separates who-they-are from what they want and what they judge it by:

```yaml
persona:
  id: persona-pilot-engineer
  name: "Pilot-team engineer"
  description: "A pilot-team engineer whose machine the collector runs on."   # ONE LINE — who, nothing else
  node_ref: cap-local-usage-collection
  goals:                                            # outcomes in THEIR words, never features
    - "I know exactly what leaves my machine, before it leaves"
    - "I can tell at a glance that last night's reporting actually ran"
    - "I can answer a usage question for my team without waiting on anyone"
  cares_about:                                      # their trust criteria — checkable, not wishes
    - "the CSV and the on-screen number always agree"
    - "nothing is collected that I have not seen the full list of"
    - "reading an answer can never change anything"
    - "a stale answer is visibly stale, not silently old"
  failure_means: >                                  # ONE sharp sentence — what a miss looks like for THEM
    They ship a usage number they cannot defend, because the CSV and the screen
    disagree and there was no way to tell what actually left their machine.
  metadata:
    created_by: author-shape-bundle
    version: 1
```

A slice record references functionalities by their spine id; the surface is named, not designed:

```yaml
slice:
  id: slice-trusted-coverage
  domain_ref: dom-token-dash
  name: "Trusted source coverage"
  outcome: "A CTO opens the coverage view and sees every source's trust state from fixtures"
  surface:                                        # REQUIRED — ≥1; a thin scaffold, named not designed
    - id: surface-coverage-view
      name: "Source coverage view"
      persona_ref: persona-cto
      user_action: "open the coverage view and read each source's resolved trust state"
  functionalities:                                # references by SPINE ID — no ice_ref paths
    - { functionality_ref: func-source-usage-ingest,   delivery: full }
    - { functionality_ref: func-privacy-trust-labeling, delivery: full }
    - { functionality_ref: func-source-coverage-freshness, delivery: full }
    - { functionality_ref: func-dashboard-presentation, delivery: partial }   # this slice's screen scaffold
  acceptance_intent: "the CTO can open the coverage view and every source shows a resolved trust state"
  status: proposed
  # order / effort / depends_on intentionally absent — /roadmap fills these
```

The `shape-manifest.yaml` carries the provenance AND the structured `spine_delta`:

```yaml
shape:
  domain_ref: dom-token-dash
  capabilities:                                   # provenance: keep/prune + grounding
    - { id: cap-coverage, decision: active,     grounding: <kb shelf or proposal> }
    - { id: cap-legacy,   decision: deprecated, grounding: <kb shelf or proposal> }
  decisions: [dec-prune-legacy, dec-select-coverage]
  spine_delta:                                    # what the keyed persist applies to the live spine
    capabilities:
      - id: cap-coverage
        status: active                            # status field only
        personas:  [persona-cto]                  # refs to attach (additive)
        journeys:  [journey-check-coverage]
        decisions: [dec-select-coverage]
      - { id: cap-legacy, status: deprecated, decisions: [dec-prune-legacy] }
    slices:                                       # spine slices index entries
      - id: slice-trusted-coverage
        slug: trusted-coverage
        domain_ref: dom-token-dash
        status: proposed
        functionality_refs: [func-source-usage-ingest, func-privacy-trust-labeling]
        doc: token-dash/slices/slice-trusted-coverage.yaml
```

Return the enriched contract with the record paths on the live model and the
`shape-manifest.yaml` path — paths, never inline content.

## Rules

- **Select + compose, never create.** Choose among the functionalities /understand created;
  never make a functionality or author ICE here.
- **Selector, never box-mover.** Read the profile; never write it.
- **Records to live, the spine to the manifest.** Write the slice/persona/journey/decision
  records straight to the live model; NEVER write `_spine.yaml` or the profile — emit the spine
  mutation as the manifest's `spine_delta` for the keyed persist.
- **Grounded.** Every kept capability and selected functionality traces to a KB shelf or a
  proposal, recorded in the manifest.
- **Stable ids.** Personas, journeys, decisions, slices use ids from name/slug so re-runs
  never duplicate.
- **Soft prune.** A pruned capability is `deprecated`, never deleted; status flip only (applied
  by the keyed persist), never edit a capability otherwise.
- **Every slice is a user-facing vertical with a scaffolded surface.** Each slice names ≥1
  surface a persona opens and checks; a backend-only or one-per-capability horizontal slice
  is invalid. NAME the surface, never DESIGN it; the surface is a thin scaffold, not the
  whole UI.
- **Personas are grounding, not decoration.** Every persona record you write carries `goals`
  (outcomes in their words), `cares_about` (their trust criteria) and `failure_means` (one
  sharp sentence on what a miss looks like for them), each read off the capability's `ice.yaml`
  and the firmed profile — never invented. `description` stays ONE LINE of who they are;
  splitting those three out of it is the point.
- **Journeys are user journeys.** Each journey traverses a named surface via `surface_refs`;
  every surface a slice names is reached by at least one journey.
- **Slices reference by spine id.** A slice points at each functionality by its spine
  `functionality_ref` id; the functionality's grounding stays the single source of truth.
- **Cover every functionality.** Every selected functionality lands in a slice or the
  `_deferred` bucket — nothing unplaced. A functionality may appear in more than one slice.
- **Compose, don't plan.** Slices carry no `order`, `effort`, or resolved `depends_on` —
  that is /roadmap's. Free-text `dependency_notes` are fine.
- **Schema-true.** Slice records conform to the slice schema; the manifest `spine_delta`
  conforms to the spine schema; persona/journey/decision records conform to their schemas.
```
