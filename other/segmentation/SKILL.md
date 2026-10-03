---
name: segmentation
description: Build email audience segments from meaningful customer state, behavior, value, lifecycle, consent, and message relevance with stable definitions, exclusions, and measurable differences.
---
# Email Segmentation

Use when one email or journey should not treat the entire audience as interchangeable.

## Procedure
1. Start from the message decision and identify which audience differences could materially change relevance, timing, offer, or action.
2. Define segments using authoritative attributes or behavior with exact inclusion, exclusion, freshness, and fallback rules.
3. Prefer durable customer or lifecycle distinctions over dozens of tiny filters that cannot support different messaging.
4. Check sample size, overlap, mutual exclusivity where required, and how contacts move between segments over time.
5. Preserve consent, suppression, account permissions, and regional or contractual eligibility independently from marketing desirability.
6. Validate the segment against real records and inspect edge cases such as missing data, stale attributes, shared accounts, or recent state change.
7. Compare downstream outcomes by segment to confirm the distinction is useful rather than merely descriptive.
8. Version important segment definitions so campaign and experiment results remain interpretable after logic changes.

## Decision rules
- Segment because relevance or decision logic differs, not because the data field exists.
- More segments increase operational and measurement complexity.
- Consent and suppression rules are constraints, not marketing segments.
- Stale lifecycle data can make personalization worse than a generic message.

## Quality gate
The segmentation is ready when definitions are reproducible, message relevance genuinely differs, exclusions and eligibility are protected, overlaps and movement are understood, sample sizes support use, and performance can be interpreted against the exact segment revision.