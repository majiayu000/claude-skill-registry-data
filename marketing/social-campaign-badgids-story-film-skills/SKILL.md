---
name: social-campaign
description: Plan a coordinated social-media release campaign with verified facts, audience segments, content pillars, platforms, placements, aspect ratios, deliverable matrix, spoiler rules, accessibility, and a relative or dated campaign calendar.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Social Campaign

## Workflow

1. Read `../../references/SOCIAL_CAMPAIGN.md`, film/trailer release facts, audience intent, canon, and approved marketing assets.
2. Write `06_release/social/campaign.json` with a `CAMP-###` ID.
3. Write `06_release/social/deliverables.jsonl` with stable `SOC-###` IDs.
4. Cover requested video, still, key-art, thumbnail, caption, and copy formats.
5. Create `06_release/social/calendar.csv`. Use relative launch phases when exact dates are unknown.
6. Record verified release facts separately from unresolved facts.
7. Never invent ratings, awards, quotes, availability, cast credits, links, or dates.
8. Validate the campaign with `scripts/promo_validate.py`.

## Done

The campaign has a traceable deliverable matrix and no marketing claim depends on an invented fact.

## Brand and repurposing state

For multi-asset campaigns, run `campaign-brand` before copy production and `content-repurpose` when one approved source is adapted into multiple destinations. `CONTENT-###` lineage records must preserve source IDs, transformation purpose, claim IDs, spoiler constraints, and destination. Use `design-system` for coordinated campaign visuals.

