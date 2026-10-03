---
name: metabolomics-direct-infusion-router
description: Use when a task needs a skill from ASB Metabolomics — direct-infusion-MS — search this unit's 97 evidence-grounded skills, then apply and optionally ground the one that fits.
license: CC-BY-4.0
metadata:
  skills_count: 97
  leaf_dir: leaves
  retrieval: bin/search_skills.py
  indexes:
  - skills_index.json
schema_version: 0.2.0
---

# ASB Metabolomics — direct-infusion-MS — router

Entry point for **97 evidence-grounded skills**, each distilled from a
peer-reviewed method paper and its public code repository.

## How this unit is laid out

The leaf skills live in **`leaves/<slug>/SKILL.md`**, not in `skills/`. A plugin
host loads the name and description of everything under `skills/` into the
session prompt, so advertising the whole corpus would cost far more context than
the work itself. Only this router is advertised; the corpus ships beside it as
data.

**Do not enumerate `leaves/`, and do not read `skills_index.json` whole.**
Search it, then read the one skill you need.

## 1. Search

```bash
python bin/search_skills.py --query "<the user's task>" -k 10
```

Standard library only — no network, no API key. Narrow with `--tool <name>`,
`--technique <tag>` or `--edam <iri-substring>` when the user is already
specific. Each hit prints the exact path to read.

## 2. Apply

Read the chosen `leaves/<slug>/SKILL.md`. Its frontmatter carries `tools` (what
to install or invoke), `derived_from` (source paper DOIs) and `evidence_spans`
(verbatim anchors from the paper or repo). Follow the body.

## 3. Ground (recommended)

Before trusting a parameter, threshold or default, verify it against the paper
the skill was built from. `kb_bundle.json` maps each skill to its source KBs:

```bash
python bin/perspicacite_kb_bind.py query --skill <slug> \
  --question "<what you need to verify>"
```

See `GROUNDING.md` for the backends and tiers.

## Licence tiers

Read each candidate's `license_tier` before presenting it. `open` — surface
freely. `noncommercial` — commercial use forbidden without a separate licence;
get explicit confirmation of an academic or non-commercial purpose first.
`restricted` — no clear licence detected; surface that caveat before use.
