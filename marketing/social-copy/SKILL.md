---
name: social-copy
description: Write coordinated campaign captions, hooks, calls to action, accessibility text, hashtags, keywords, and platform variants using verified release facts and an explicit no-invented-claims rule.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Social Copy

## Workflow

1. Read the campaign brief, one or more `SOC-###` deliverables, verified release facts, tone rules, spoiler policy, and the actual media being promoted.
2. Write `06_release/social/copy.jsonl` using stable `COPY-###` IDs.
3. Separate hook, body, CTA, accessibility description, hashtags, and keywords.
4. Cite or list the verified project facts used by each copy record.
5. Omit unresolved release dates, URLs, ratings, awards, review quotes, and availability claims.
6. Avoid repeating identical copy across every platform when placement context differs.

## Done

Each deliverable that needs text has destination-appropriate copy grounded only in verified project information.

## Brand and evidence controls

When present, read `06_release/social/brand_voice.json` before drafting. Record factual public claims with `CLAIM-###` references and validate them through `campaign_content.py`. Record each transformed public content item in `content_lineage.jsonl` so repurposing does not silently change facts, spoilers, or campaign promises.

