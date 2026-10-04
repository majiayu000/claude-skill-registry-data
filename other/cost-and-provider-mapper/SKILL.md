---
name: cost-and-provider-mapper
description: Map DSDS architectures across AWS, GCP, and Azure equivalents and estimate cost-impact tradeoffs. Use when planning provider portability, comparing cloud options, and explaining cost/performance implications of design choices.
---

# Cost And Provider Mapper

## Overview
Translate component selections across cloud providers and reason about cost and performance implications. Produce comparable options instead of one-off provider-specific designs.

## Workflow

1. Build component inventory
- List all architecture components with scale assumptions and usage patterns.
- Mark critical latency and durability requirements.

2. Map cross-provider equivalents
- For each component, provide AWS, GCP, and Azure equivalent services.
- Flag components with no clean one-to-one mapping.

3. Identify primary cost drivers
- Compute, storage, network egress, data transfer, and managed-service premiums.
- Call out cost-sensitive workload patterns (bursty, diurnal, spike).

4. Evaluate tradeoffs
- Compare expected latency behavior, operational complexity, and portability risk.
- Highlight lock-in points and migration friction.

5. Produce recommendation pack
- Deliver at least two viable provider profiles with pros/cons.
- Include assumptions and confidence level.

## Output format
1. `Component mapping table`
2. `Cost driver summary`
3. `Tradeoff analysis`
4. `Recommended options`
5. `Assumptions and risks`

## References
- Read `references/provider-mapping-notes.md` for mapping and tradeoff checklist.
- Use these repo sources:
- `canonical-catalogue/DSDS Canonical Catalogue - Provider mapping (quick).csv`
- `canonical-catalogue/DSDS Canonical Catalogue - Metrics & SLIs.csv`
- `planning/IMPLEMENTATION_PLAN.md` (Phase 9.4)
