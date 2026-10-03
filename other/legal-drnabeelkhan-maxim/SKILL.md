---
name: L3.2 Legal Vertical
description: "Maxim L3 pack. Bundles: Attorney-client privilege + ethics walls + conflict-of-interest patterns. Primary framework: ABA Model Rules of Professional Conduct."
business_outcome: "See documents/ledgers/MOAT_TRACKER.md for the registered moat row; purchase to activate."
primary_framework: "ABA Model Rules of Professional Conduct"
product_id: L3.2
pack_tier: L3
ships_with: v1.0.0
license: proprietary
---

# L3.2 Legal Vertical

> Copyright (c) 2026 iSystematic Inc. Maxim product. Separately licensed via Stripe.

## What this pack delivers

Attorney-client privilege + ethics walls + conflict-of-interest patterns

## Primary framework

ABA Model Rules of Professional Conduct — applied across every output this pack produces. Framework mechanism named in the SKILL body below; anti-patterns registered in documents/ledgers/MOAT_TRACKER.md.

## Activation

This pack requires a valid license JWT. Purchase at https://maxim.isystematic.com/pricing. After checkout, Stripe webhook issues a JWT; the Cloudflare Worker validates locally on every tool call.

```
mxm-pack-engine activate --license <JWT-from-email>
```

Free tier (Starter) does not include this pack. See documents/guides/PACKS.md for full pricing and ADR-009 for pack architecture.

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. Separately licensed via Stripe (ADR-011)._