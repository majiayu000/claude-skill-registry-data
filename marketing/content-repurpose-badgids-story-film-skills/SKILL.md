---
name: content-repurpose
description: Adapt approved film, trailer, transcript, press, and campaign material into destination-specific content while preserving source lineage, verified claims, spoiler policy, brand voice, and the central promise.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Content Repurpose

1. Read `../../references/CAMPAIGN_BRAND.md`, social campaign, brand voice, source material, and claim ledger.
2. Plan each derivative as `CONTENT-###` in `06_release/social/content_lineage.jsonl`.
3. Record source IDs, destination, format, transformation, `COPY-###`, `CLAIM-###`, and status.
4. Adapt hook, length, pacing, crop, CTA, and context for the destination without changing verified facts.
5. Avoid posting identical text everywhere merely for convenience.
6. Public factual claims must resolve through the claim ledger or verified release facts.
7. Validate with `scripts/campaign_content.py PROJECT --validate`.

Done when every derived campaign item can be traced back to approved source material and verified claims.
