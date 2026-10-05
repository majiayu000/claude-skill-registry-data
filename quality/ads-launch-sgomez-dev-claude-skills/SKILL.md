---
name: ads-launch
description: "Draft or explicitly apply a paid-ad campaign launch through Claude Ads capability-gated adapters. Use for campaign creation, launch plans, publishing ads, activating campaigns, uploading creative, or requests to push a campaign live."
---

# Campaign Launch

Default to `--draft`.

1. Load the validated setup profile, account snapshot, campaign plan, creative
   manifest, platform capability manifest, policy findings, and tracking checks.
2. Refuse a draft that lacks account/object scope, objective, conversion, budget,
   dates, targeting, assets, destinations, measurement, or policy eligibility.
3. Produce a deterministic mutation plan with exact proposed objects, before/after
   state, blast radius, learning impact, owner, success measure, verification
   window, idempotency key, audit destination, and rollback.
4. For `--apply`, require the exact operation to be enabled and independently
   tested, then obtain explicit approval for that exact plan.
5. Apply the smallest reversible change, verify remote state, and preserve the
   immutable audit and rollback record.

Missing ceilings, stale account state, changed remote state, incomplete tracking,
failed policy review, or an unavailable adapter blocks apply. Permanent deletion is
not supported.

