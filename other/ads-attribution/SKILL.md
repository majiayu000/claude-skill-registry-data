---
name: ads-attribution
description: "Audit cross-platform attribution, conversion definitions, reporting windows, GA4, AdServices and AdAttributionKit, MMPs, browser and server events, offline conversions, and platform reconciliation. Use for attribution audit, attribution models, conversion windows, requests to add or total Meta and Google conversions, incompatible reporting-window aggregation, GA4 attribution, MMP review, AppsFlyer, Adjust, Branch, Singular, or cross-platform discrepancies."
---

# Attribution Audit

1. Read the main `ads` contract and normalized account snapshots.
2. Declare the business conversion, value, data window, timezone, currency, and
   decision the attribution analysis must support.
3. Inventory every browser, server, platform, analytics, MMP, offline, and app
   attribution source with its identity, counting, deduplication, and privacy rules.
4. Reconcile comparable events and explain differences caused by eligibility,
   view-through rules, consent, modeled data, conversion lag, thresholds, or scope.
5. Separate measurement quality from platform-reported performance.
6. Return findings, contradictions, confidence, missing evidence, and a measurement
   improvement plan through the common JSON contract.

Do not assume one platform is ground truth, add incompatible reports together, or
recommend an attribution model without the operator's decision context.

## Comparability gate

Reject aggregation until the sources share, or are explicitly normalized to, the
same conversion event and value definition, attribution window, click/view scope,
counting method, deduplication identity, timezone, currency, attribution model,
and modeled-data treatment. Until then, report the values side by side with their
definitions; do not compute a total.

Example: Meta seven-day conversions and Google thirty-day conversions are
incompatible. Refuse to add them, reconcile windows and definitions first, and
only aggregate a newly comparable dataset.
