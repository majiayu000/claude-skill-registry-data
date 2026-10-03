---
name: L3.3 Fintech Vertical
description: "Maxim L3 pack. Bundles: PCI-DSS + FINTRAC + SOX + FDX. Primary framework: PCI-DSS v4.0 (Payment Card Industry)."
business_outcome: "See documents/ledgers/MOAT_TRACKER.md for the registered moat row; purchase to activate."
primary_framework: "PCI-DSS v4.0 (Payment Card Industry)"
product_id: L3.3
pack_tier: L3
ships_with: v1.0.0
license: proprietary
---

# L3.3 Fintech Vertical

> Copyright (c) 2026 iSystematic Inc. Maxim product. Separately licensed via Stripe.

## What this pack delivers

PCI-DSS + FINTRAC + SOX + FDX

## Primary framework

PCI-DSS v4.0 (Payment Card Industry) — applied across every output this pack produces. Framework mechanism named in the SKILL body below; anti-patterns registered in documents/ledgers/MOAT_TRACKER.md.

## Activation

This pack requires a valid license JWT. Purchase at https://maxim.isystematic.com/pricing. After checkout, Stripe webhook issues a JWT; the Cloudflare Worker validates locally on every tool call.

```
mxm-pack-engine activate --license <JWT-from-email>
```

Free tier (Starter) does not include this pack. See documents/guides/PACKS.md for full pricing and ADR-009 for pack architecture.

---
_Copyright (c) 2026 iSystematic Inc. Maxim product. Separately licensed via Stripe (ADR-011)._