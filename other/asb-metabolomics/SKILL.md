---
name: asb-metabolomics
description: "Use when starting any task with the ASB Metabolomics skill collection — read this meta-skill first. It explains good practice (search -> apply -> ground), enforces the license-tier acknowledgment for non-open tools, then hands off to the _router skill for actual skill selection."
license: CC-BY-4.0
metadata:
  role: meta
  delegates_to: _router
derived_from:
- doi: 10.5281/zenodo.20794027
  title: ASB Metabolomics Skill Collection v2 (metabolomics-v0.1.0)
schema_version: 0.2.0
---

# asb-metabolomics

The entry point for the ASB Metabolomics collection. Run this before routing to a
specific skill.

## Protocol: search -> apply -> ground

1. **Search** for a skill via `skills_index.json` (EDAM IRI / tool / keyword) or
   `tools_index.json`.
2. **License-tier gate (governance).** Read the candidate skill's
   `metadata.tool_license`.
   - If `requires_ack: true` (tier `noncommercial`): surface `tier` + `ref` + `url`
     to the user and obtain an **explicit, blocking acknowledgment** that their use is
     a permitted (noncommercial) purpose **before applying the skill**. Commercial
     use is forbidden without a separate license.
   - If tier is `restricted` (`requires_ack: false`): surface a **non-blocking soft
     note** — "no clear license detected — verify before commercial use or
     redistribution" — then continue without waiting for acknowledgment.
   Default discovery to `open`-tier skills; flag non-open results.
3. **Apply** the selected skill.
4. **Ground** against the source via the Perspicacité binder. Grounding for non-open
   tiers is **link-only** (referenced, never embedded); assembling a local bundle is
   the consumer's responsibility.

## Hand-off

For the actual skill selection, delegate to the `_router` skill, which performs pure
routing over the indexes. This meta-skill owns guidance and license governance;
`_router` owns routing.

## Step 5: report what did not work

The collection hardens from use. When a skill turns out to be wrong or stale, when
the search finds nothing usable, or when the leaves exist but nothing composes them,
delegate to **`asb-contribute`**: it turns that friction into a redacted, dedupable
report the user approves before anything is filed. Offer once per problem, and drop
it if declined.

## License tiers

`open` = commercial use OK; `noncommercial` = academic/noncommercial only;
`restricted` = no grant / proprietary. See `governance/LICENSE_TIERS.md`. This axis is
separate from the paper open-access axis (`access.type`).
