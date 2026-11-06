---
name: literature-review-map
description: Route literature tasks to PDF abstract extraction, Zotero screening, full-text reading, table export, WoS citation analysis, or static scientific figures.
---

# Literature Research Assistant

Use existing paths, scope, and authorization. Read the [shared contract](references/shared-contract.md) and only the required modules. Do not execute every workflow in sequence.

| Task | Module |
|---|---|
| PDF first pages and abstracts | [literature-pdf-abstract](skills/literature-pdf-abstract/SKILL.md) |
| Economical Zotero screening | [literature-zotero-screen](skills/literature-zotero-screen/SKILL.md) |
| Export existing records | [literature-export](skills/literature-export/SKILL.md) |
| Read a full paper | [literature-deep-read](skills/literature-deep-read/SKILL.md) |
| WoS cited references, co-citation, and bursts | [literature-wos-analysis](skills/literature-wos-analysis/SKILL.md) |
| Plot or restyle existing analysis | [literature-figures](skills/literature-figures/SKILL.md) |

For export requests, extract records first only if structured input is missing. For figure-only changes, reuse data. Combined tasks follow dependencies, such as analysis → export → figures, preserving each stage's evidence scope.

Screening is not deep reading; co-occurrence is not co-citation; final-year bursts are not confirmed frontiers. Default to English static images and separate output folders. Keep source libraries read-only. Scripts are in scripts/; see [record schema](references/records.md).
