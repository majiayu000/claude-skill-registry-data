---
name: carbon-cost-pair
description: Pair every cloud spend value with a kgCO2e estimate by region and service category for CSRD and SEC climate disclosure. Input is region, service category, and dollar value; output is paired kgCO2e with confidence label (vendor-published, third-party, or estimated) and source citation. Defaults to electricity-only Scope 2 market-based factors.
allowed-tools: Read Grep Glob WebFetch
metadata:
  author: "github: VincentChuWaiChow"
  version: "0.1.1"
  updated: "2026-05-13"
  category: finops
  lifecycle: experimental
---

# Carbon Cost Pair

## Purpose

For every cloud spend line item, produce a paired kgCO2e estimate suitable for CSRD and SEC climate disclosure. The skill pairs a dollar value (or resource quantity) with the best available carbon emissions factor for the given cloud region and service category, and returns the estimate with a mandatory confidence label and source citation.

No cloud credentials accepted. Carbon factors are fetched from provider sustainability pages or third-party sources.

## When to use

Use this skill when:

- The user needs to pair a cloud spend or usage figure with a carbon estimate for sustainability reporting (CSRD Article 29a, SEC climate rule, GHG Protocol Scope 2)
- The user wants to compare the carbon intensity of the same workload across cloud regions or providers
- The user wants to understand the confidence level of a carbon estimate before including it in a regulatory disclosure

## Operating rules

- **Default to electricity-only Scope 2, market-based.** Unless the caller specifies otherwise, compute Scope 2 emissions using market-based electricity factors (renewable energy certificate or PPA-adjusted). Location-based factors are available on request.
- **Fetch live data first.** Use WebFetch to retrieve the latest carbon factor data from the provider's sustainability API or dashboard before falling back to documentation-based estimates.
- **Confidence labels mandatory.** Every kgCO2e output must carry exactly one label:
  - `vendor-published` — factor sourced from the provider's own sustainability API, dashboard, or data export within this session (include source URL and ISO 8601 timestamp)
  - `third-party` — factor sourced from Electricity Maps, Cloud Carbon Footprint project, or equivalent third-party source (include source URL and timestamp)
  - `estimated` — factor derived from regional grid average or published industry emission factors where no provider or third-party data is available (state the factor, source, and assumptions)
- **No credentials accepted.** No cloud credentials, billing account IDs, tenant data, or sustainability API tokens are accepted or required.
- **Acknowledge data lag.** Provider carbon data typically lags 60-90 days or more. State the data period whenever citing vendor-published factors.
- **FOCUS column mapping.** There are no native FOCUS v1.2 carbon columns. Represent carbon estimates as FOCUS tags: `Tags/kgco2e`, `Tags/carbon_confidence`, `Tags/carbon_source`.
- **Load references only when needed.**

## Input

| Field | Required | Description |
|---|---|---|
| Cloud provider | Yes | AWS, Azure, Google Cloud, OCI, or multi-cloud |
| Region | Yes | Provider region name (e.g., `us-east-1`, `eastus`, `us-central1`, `ap-sydney-1`) |
| Service category | Yes | Compute, Storage, Networking, AI and Machine Learning, Databases, or Other |
| Dollar value ($) | Yes | The spend amount to pair with a carbon estimate |
| Resource quantity | Optional | If available, the underlying resource quantity (e.g., vCPU-hours, GiB-hours, GB transferred) for a more precise estimate |
| Scope preference | Optional | Default: Scope 2 market-based. Options: `scope2-market`, `scope2-location`, `scope1+2` |

## Output shape

Return, per line item:

```
Region:           <provider region>
Service category: <category>
Dollar value:     $<amount>
kgCO2e estimate:  <value> kgCO2e  [<confidence label>]
Scope:            Scope 2 (market-based)  |  Scope 2 (location-based)
Data period:      <e.g., Q3 2025 or "Current as of 2026-05-13">
Source:           <URL>  (fetched: <ISO 8601 timestamp>  |  documentation date: <date>)
Methodology note: <one sentence describing the emission factor used>

FOCUS tags:
  Tags/kgco2e:           <value>
  Tags/carbon_confidence: <vendor-published | third-party | estimated>
  Tags/carbon_source:     <URL>
```

If multiple regions or service categories are provided, return one block per line item followed by a summary table.

## Confidence label decision tree

1. Does the cloud provider publish a region-level carbon factor or API for this region and service?
   - Yes, and it was fetched this session → `vendor-published`
   - Yes, but the fetch failed or data is not current → proceed to step 2
2. Is Electricity Maps data available for the grid region, or is Cloud Carbon Footprint data available for this provider/region?
   - Yes → `third-party`
3. Fall back to IEA regional grid average emission factor or the provider's country-level average.
   - → `estimated`; state the factor used (e.g., `0.386 kgCO2e/kWh — IEA 2023 US average`)

## Regulatory context

- **CSRD (Corporate Sustainability Reporting Directive)**: requires disclosure of Scope 1, 2, and 3 emissions under ESRS E1. Cloud compute is typically Scope 2 (purchased electricity) and may contribute to Scope 3 Category 1 (purchased goods/services) for customers.
- **SEC Climate Rule**: requires material climate-related disclosures including Scope 1 and 2 emissions for large accelerated filers.
- **GHG Protocol**: defines market-based and location-based approaches for Scope 2. Both may be required; market-based is the default here.

## References

Load these only when needed:

- [Carbon data sources](references/sources.md) — provider sustainability API URLs, third-party data sources, and fallback options.
- [Methodology](references/methodology.md) — market-based vs location-based Scope 2, data lag, and uncertainty labeling.
