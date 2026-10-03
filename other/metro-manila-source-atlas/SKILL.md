---
name: metro-manila-source-atlas
description: Refresh or extend the foundation Metro Manila/NCR source atlas that supports the address disaster risk assessor.
---

# Metro Manila Source Atlas

Use this skill when refreshing the foundation source atlas, adding new public
data sources, or rerunning a source validation pass for the address disaster
risk assessor.

## Boundaries

- Read-only network access only.
- No signups, credentials, paid actions, scraping behind auth, or terms bypass.
- Prefer machine-readable APIs, ArcGIS services, CKAN APIs, GeoJSON, CSV, ZIP,
  PBF, or documented downloads.
- Keep PDF-only and scrape-only sources separate from clean machine-readable
  sources.
- Preserve raw findings separately from integrated outputs.

## Research Lanes

Run independent lanes before integration:

1. Official statistics: PSA OpenSTAT, PSGC, census, income, prices,
   establishments, regional accounts.
2. Geography and boundaries: PSA PSGC, HDX COD-AB, MMDA boundaries, PSGC/HDX
   crosswalks.
3. Metro Manila and LGU data: MMDA GIS Hub, city dashboards, open data pages.
4. Transport and mobility: GTFS, OSM roads/transit tags, MMDA mobility sources.
5. Risk and service proxies: waste, drainage, access, facilities, waterways,
   roads, and local operational signals.
6. Portal and API infrastructure: BetterGov, HDX CKAN, ArcGIS search, Open Data
   Philippines, Overpass, Geofabrik.

## Source Row Schema

Every inventory row should include:

`name`, `owner`, `coverage`, `data_type`, `access_method`,
`endpoint_or_download_url`, `formats`, `auth_required`, `rate_limits`,
`last_updated_signal`, `freshness_grade`, `Metro Manila filter method`,
`sample_query`, `market_research_use_cases`, `license_or_terms`, `risks`,
`source_url`.

## Validation Checklist

For high-priority sources:

- GET metadata or a lightweight endpoint before deeper calls.
- Confirm Metro Manila coverage through PSGC codes, NCR labels, city names,
  bounding boxes, or spatial joins.
- Record freshness from API metadata, modified timestamps, release dates, or
  response titles.
- Record gating accurately: public, auth-gated, manual-only, commercial, or
  dead.
- Capture at least one sample API/download command when allowed by terms.
- Do not rely on snippets alone for endpoint claims; live-check when feasible.

## Integration And Ranking

Deduplicate by stable source identity first: owner, endpoint, item id, dataset
id, or download URL. Rank by:

- accessibility;
- freshness;
- Metro Manila specificity;
- automation value;
- license clarity;
- risk-assessment signal quality.

## Current Build Decision

The active product is the address disaster risk assessor. The source atlas is a
supporting inventory, not the product itself.

Use city-level sources for coarse context and feature-level hazard layers for
address-level screening. Move to barangay-specific outputs only after the
PSGC/HDX/MMDA/OpenSTAT crosswalk is validated.

Recommended source order:

`address/coordinates -> PSGC/boundary context -> hazard layers -> MMDA/OSM proximity overlays -> weak-service proxies`

## Required Outputs

Use these paths unless the user requests a different target:

- Raw lane findings: `data/agent-findings/`
- Integrated source inventory: `data/metro-manila-source-atlas.json`
- Validation record: `data/verification-log.md`
- Deep-dive structured evidence: `data/deep-dive/`
- Human-readable synthesis: `reports/`
- Durable decisions: `docs/decisions/`

## Verification Commands

```bash
npm run validate
git diff --check
```
