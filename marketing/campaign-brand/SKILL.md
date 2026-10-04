---
name: campaign-brand
description: Define and enforce durable campaign voice, terminology, naming, CTA, spoiler, accessibility, and prohibited-claim rules so trailers, social copy, press materials, and promotional art stay recognizably consistent.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Campaign Brand

1. Read `../../references/CAMPAIGN_BRAND.md`, campaign state, canon, verified release facts, and approved writing samples when available.
2. Write `06_release/social/brand_voice.json`.
3. Define voice attributes, perspective, preferred and avoided vocabulary, CTA behavior, spoiler limits, accessibility tone, exact naming rules, and prohibited claims.
4. Keep campaign voice separate from character dialogue voice.
5. Use examples as calibration, not text to copy repeatedly.
6. Run `scripts/campaign_content.py PROJECT --validate` when campaign copy and lineage exist.

Done when downstream promotional writing can be checked against an explicit project voice rather than guessed from memory.
