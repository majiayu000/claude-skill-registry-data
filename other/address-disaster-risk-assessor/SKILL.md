---
name: address-disaster-risk-assessor
description: Produce a source-attributed disaster risk packet for a Metro Manila address using validated public hazard and geospatial sources.
---

# Address Disaster Risk Assessor

Use this skill when the user wants to evaluate disaster exposure for a specific
address or set of coordinates.

## Scope

First geography: Metro Manila / NCR.

First risk classes:

- flood hazard and flood-prone history;
- river and waterway proximity;
- liquefaction exposure;
- active fault proximity;
- landslide relevance;
- storm-surge relevance where applicable.

Weak or later risk classes:

- waste-management quality;
- drainage maintenance quality;
- garbage-collection reliability;
- local complaint history.

Only include weak-service signals when a clean source or defensible proxy is
validated. Do not infer them from vibes or one-off anecdotes.

## Inputs

Preferred:

- address string;
- optional latitude and longitude;
- optional property/use type.

If coordinates are not available, geocode first and record confidence. If
geocoding confidence is low, stop and ask for a more precise address or
coordinates before scoring.

## Workflow

1. Normalize the input location.
2. Identify city and barangay when possible.
3. Load or query priority hazard sources from
   `data/disaster-risk/source-priorities.json`.
4. Check point-in-polygon exposure for hazard zones.
5. Check nearest-neighbor distance to flood-prone points, rivers, waterways, and
   active-fault features where available.
6. Assign per-component confidence based on source quality, freshness, spatial
   precision, and address confidence.
7. Generate a risk packet with sources, limitations, and non-certification
   language.

## Output Format

Return a concise report with these sections:

1. Location Normalization
2. Overall Risk Summary
3. Flood And Water Risk
4. Earthquake, Fault, And Liquefaction Risk
5. Landslide / Storm Surge Relevance
6. Waste Or Drainage Service Signals, only if evidence exists
7. Data Gaps And Confidence
8. Sources
9. Disclaimer

Also emit a structured JSON object when producing files:

```json
{
  "input_address": "",
  "normalized_address": "",
  "coordinates": { "lat": null, "lon": null },
  "geocode_confidence": "",
  "admin_context": {
    "city": "",
    "barangay": "",
    "psgc": ""
  },
  "overall_risk_label": "",
  "risk_components": [],
  "data_gaps": [],
  "limitations": [],
  "sources": []
}
```

## Risk Labels

Use:

- `high`
- `medium`
- `low`
- `unknown`
- `not_applicable`

Do not collapse unknowns into low risk.

## Required Caveat

This output is a public-data screening report, not an engineering assessment,
insurance determination, legal opinion, or official government hazard
certification.

## Priority Sources

Primary automation stack:

- MGBPublic Flood MapServer for flood susceptibility.
- MMDA Flood-Prone Areas FeatureServer for local flood-prone point history.
- MMDA River Line FeatureServer for waterway proximity.
- PHIVOLCS Liquefaction MapServer for liquefaction exposure.
- PHIVOLCS ActiveFault MapServer for nearest active fault distance.
- Project NOAH hazard maps through BetterGov for flood, landslide, debris-flow,
  and storm-surge zones after PMTiles schema inspection.
- HDX Philippines administrative boundaries for NCR/city/barangay joins.
- OSM / Geofabrik waterways, roads, and facility proxies.

Secondary or manual sources:

- MGBPublic RainInducedLandslide MapServer when landslide relevance exists.
- PAGASA Pasig-Marikina-Tullahan FFWS for live flood-warning context only.
- HazardHunterPH / GeoRiskPH for official manual cross-check.
- PHIVOLCS FaultFinder for official manual fault-distance cross-check.
- PHIVOLCS GroundShaking and Tsunami MapServers after more point validation.
- LGU DRRMO/CDRA and waste-service pages only as manual context or weak
  proxies.

## Verification

Before committing changes to this workflow:

```bash
npm run validate
git diff --check
```
