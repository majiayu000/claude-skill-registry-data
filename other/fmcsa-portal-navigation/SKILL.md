---
name: fmcsa-portal-navigation
description: |
  Use this skill when the user asks where to find specific information at fmcsa.dot.gov — the SAFER (Safety and Fitness Electronic Records System), Carrier Snapshot, Compliance Safety Accountability (CSA) data, PSP (Pre-Employment Screening Program), Clearinghouse, Unified Carrier Registration (UCR), MCS-150 update, complaints, DataQs, and the FMCSA Portal login. Reference fmcsa.dot.gov.
---

# FMCSA Portal Navigation

FMCSA's online resources are scattered across multiple sub-portals. This skill is a directory of where to find what.

## Main entry point: fmcsa.dot.gov

The hub for federal motor carrier safety regulations. From here, navigate to:

### Public pages (no login)

- **SAFER (Safety and Fitness Electronic Records)** — safer.fmcsa.dot.gov
  - Carrier Snapshot (look up any carrier's USDOT info)
  - Inspection history (last 24 months public)
  - Crash history (last 24 months)
  - Operating authority status
  - Insurance filings status
  - Power unit count + driver count

- **CSA Public** — ai.fmcsa.dot.gov/SMS
  - BASIC scores (only intervention-flagged carriers)
  - Inspection details
  - Crash details (for carriers with public exposure)

- **FMCSA Hotlines + Forms**
  - 1-800-832-5660 (general)
  - Various complaint hotlines

### Authenticated portal (FMCSA Portal)

Sign up at portal.fmcsa.dot.gov. Used for:
- MCS-150 biennial update
- New entrant safety audit response
- Insurance filing review (private; not public)
- Owner-operator account access
- Carrier-specific data downloads

## Specific FMCSA portals (each is a separate sub-system)

### 1. Unified Registration System (URS)

- New USDOT number applications
- New MC number applications
- BOC-3 process agent designation
- Operating authority changes
- Fees: USDOT free, MC $300

URL: fmcsa.dot.gov/registration

### 2. MCS-150 Biennial Update

- Updates carrier's operating information every 24 months
- Schedule based on USDOT number last digit
- Penalty: up to $1,150/day for failure to update

URL: portal.fmcsa.dot.gov

### 3. SAFER (Safety and Fitness Electronic Records System)

- Public carrier safety snapshot
- Searchable by USDOT, MC, name, address
- Shows last 24 months of inspections + crashes
- Free access

URL: safer.fmcsa.dot.gov

### 4. Pre-Employment Screening Program (PSP)

- Carrier subscribes to access driver history
- $10 per query for a 5-year crash + 3-year inspection report
- Used pre-hire to evaluate driver

URL: psp.fmcsa.dot.gov

### 5. Drug & Alcohol Clearinghouse

- Pre-employment Full + Annual Limited queries
- Verified positive test reporting
- SAP completion reporting
- $1.25 per query

URL: clearinghouse.fmcsa.dot.gov

### 6. DataQs

- Request for Data Review on inspection + crash records
- Dispute violations or wrong carrier assignment
- 30-90 day processing typical

URL: dataqs.fmcsa.dot.gov

### 7. Hazmat Safety Permit

- HMSP application + renewal
- Required for certain hazmat in placardable quantities

URL: fmcsa.dot.gov/hazmat

### 8. Compliance Safety Accountability (CSA)

- Public BASIC scores (intervention-threshold-flagged only)
- Carrier intervention history
- Safety rating + dispute history

URL: ai.fmcsa.dot.gov/SMS

### 9. Crash Preventability Determination Program (CPDP)

- Request preventability review on eligible crash types
- 16 categories of crashes eligible
- 60-120 day processing

URL: cpdp.fmcsa.dot.gov

### 10. FMCSA Customer Self-Service (CSS)

- Some services available without full FMCSA Portal login
- Renewals, applications

URL: cs-fmcsa.dot.gov

## Hotlines

- **General FMCSA:** 1-800-832-5660
- **Driver / Carrier complaints:** 1-888-DOT-SAFT (1-888-368-7238)
- **HHG Mover complaints:** 1-888-368-7238
- **Hazmat hotline:** 1-800-467-4922
- **PHMSA (Hazmat):** 1-800-467-4922

## Field offices

FMCSA has field offices in each state. Find your local at fmcsa.dot.gov/field-offices. Useful for:
- In-person audits + investigations
- Insurance filing questions
- Compliance assistance

## Common navigation mistakes

1. **Looking for CSA scores at SAFER.** SAFER shows snapshot; CSA scores are at ai.fmcsa.dot.gov/SMS.
2. **Trying to file PSP query without subscription.** $10 per query but need account first.
3. **Looking up driver Clearinghouse status at SAFER.** Clearinghouse has its own portal.
4. **Filing DataQ at FMCSA Portal.** DataQs has its own portal.
5. **MCS-150 update through SAFER.** Update happens at portal.fmcsa.dot.gov.

## Account setup tips

- Use a generic email (joshua@x3fleetsafety.com vs personal Gmail)
- 2FA recommended for FMCSA Portal
- Designate a primary + backup admin
- Update contact info when staff changes
- Audit annually who has access

## State equivalents

For state-specific compliance + permits:
- **State DOT** — state-level commercial vehicle regulations
- **State PUC** — non-consensual tows, intrastate freight
- **State Tax Authority** — IFTA, HUT, weight-distance, KIT, etc.
- **State Agriculture Department** — agricultural exemptions
- **State DMV** — CDL, vehicle registration

## Where this fits in X3

X3 cross-references these portals + can integrate with some via API. The X3 dashboard pulls carrier snapshot data from SAFER + CSA data from SMS automatically. Future: deeper Clearinghouse + PSP integration for streamlined hiring workflow.

When a customer asks "where do I find X?" — use this skill to point them to the right portal.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=fmcsa-portal-navigation

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
