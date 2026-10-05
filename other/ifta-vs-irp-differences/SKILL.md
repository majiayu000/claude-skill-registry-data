---
name: ifta-vs-irp-differences
description: |
  Use this skill to differentiate IFTA (fuel tax) and IRP (apportioned registration). Covers what each is for, deadlines, and how they interact.
---

# IFTA vs IRP — What's the Difference?

IFTA and IRP are commonly confused because both involve interstate operations and base-state filing. They're different systems with different purposes.

## IFTA (International Fuel Tax Agreement)
- **Purpose**: Fuel tax reciprocity across states
- **What it does**: Lets you buy fuel in any state and report taxes once
- **When you need it**: Any motor carrier qualifying vehicle (>26K lbs)
- **Frequency**: Quarterly returns + license decals (annual)
- **Cost**: Annual decal fee (~$25 per vehicle) + quarterly tax (varies)

## IRP (International Registration Plan)
- **Purpose**: Vehicle registration across states
- **What it does**: One license plate recognized in all IRP jurisdictions
- **When you need it**: Any commercial vehicle crossing state lines
- **Frequency**: Annual registration renewal + quarterly mileage report
- **Cost**: Annual registration fee (apportioned by mileage)

## Comparison table
| Aspect | IFTA | IRP |
|---|---|---|
| What you're paying | Fuel tax | Vehicle registration |
| Decal vs plate | Decals + license | License plate |
| Reporting frequency | Quarterly | Quarterly (mileage) + annual (registration) |
| Tax/fee basis | Fuel consumed × rate | Miles driven × rate |
| Base state | Where vehicle is based | Where vehicle is based |
| Renewal cycle | Annual decal | Annual registration |

## How they interact
- Both use mileage data (you can derive both from ELDs)
- Both require state-by-state allocation
- Both expect quarterly reporting
- Both have audit programs

## When you need ONE but not the OTHER
- **IFTA only**: typically not applicable (if you have IFTA you usually have IRP)
- **IRP only**: typically not applicable (if you have IRP you usually have IFTA)
- Some states have intra-state-only registration that's not IRP

## Common confusion
- "IFTA decals" vs "IRP plates" — different
- IFTA fuel tax owed vs IRP registration fees — different
- IFTA quarterly return vs IRP quarterly distance report — different forms, same data

## Compass approach
- IFTA module: focused on fuel + tax
- IRP integration shares mileage data
- Quarterly reports generated from same ELD + fleet data
- Single calculation engine; two output formats

## CFR citations
- **IFTA Articles of Agreement**
- **IRP Articles of Agreement**

## How Compass surfaces this
Searchable in Compass Ask. Runs against carrier fleet data when invoked from the relevant tracker. Read-only; no actions without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=ifta-vs-irp-differences

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
