---
name: eld-mandate-compliance
description: |
  Use this skill when the user asks about Electronic Logging Device (ELD) compliance under 49 CFR 395.20-38 — ELD mandate, AOBRD vs ELD transition, ELD exemptions, ELD malfunctions, 8-day paper backup, ELD certification on FMCSA registered list, data file integrity, edits + annotations, driver portability, and how to handle ELD failures at roadside. Cite 49 CFR 395.20-395.38.
---

# ELD Mandate Compliance — 49 CFR 395.20-38

The ELD Final Rule became effective Dec 18, 2017 for new ELDs and Dec 16, 2019 for AOBRD-using fleets to fully transition. As of 2026, virtually all interstate CMV drivers must use a registered ELD.

## Who must use an ELD

Drivers must use a registered ELD if all of:

- Required to maintain a record of duty status (RODS) under 49 CFR 395, AND
- Operating an interstate CMV requiring a CDL.

## Exemptions from the ELD rule

A driver does NOT have to use an ELD if:

- **Short-haul** (49 CFR 395.1(e)(1) or (e)(2)) — operates within 150 air-mile radius, returns to work-reporting location within 14 hours, etc.
- **8-day exception** — uses paper logs for 8 or fewer days in any 30-day period.
- **Driveaway-towaway** — vehicle is the commodity being delivered.
- **Pre-2000 engine** — operating a CMV manufactured before model year 2000 (engine model year governs).

## ELD registration

ELDs must be on the FMCSA's **Registered ELDs list** at `eld.fmcsa.dot.gov`. Manufacturers self-certify; FMCSA accepts the self-certification but reserves right to revoke. Some ELDs have been revoked — always verify your ELD is currently listed.

## Malfunction handling (49 CFR 395.34)

If an ELD malfunctions, the driver must:

1. Note the malfunction on the log
2. Reconstruct previous 7 days on paper if not already recorded
3. Continue manual paper logs until the ELD is repaired
4. Carrier has **8 days** from notification to repair/replace OR
5. Submit a malfunction notice to FMCSA requesting an extension

If a driver experiences a malfunction during a roadside inspection, they should display the device + show paper logs covering the relevant period.

## ELD data file (eRODS)

When inspected at roadside, the driver transfers the ELD data to the inspector via:

- **Web service** — driver enters inspector's email
- **USB drive** — physical handoff
- **Bluetooth** — wireless transmission

The ELD must support at least one method. Some ELDs support both; FMCSA's eRODS app reads either format.

## Edits + annotations (49 CFR 395.32)

A driver can edit duty status records (e.g., to correct mis-classified PC, missing yard moves, etc.) but:

- All edits are recorded with a timestamp
- The original data is preserved (cannot be deleted)
- The driver must annotate the reason for the edit
- Carrier cannot edit driver duty status without driver acknowledgment

## Personal Conveyance (PC) and Yard Moves (YM)

The ELD must allow drivers to log:

- **PC time** — off-duty driving (e.g., driving home in a company truck)
- **YM time** — on-duty driving within a yard/terminal at speeds < 20mph

Carrier must authorize PC + YM in writing. Drivers cannot unilaterally claim them.

## ELD vs AOBRD (legacy)

AOBRDs (Automatic On-Board Recording Devices) were the predecessor under 49 CFR 395.15. Major differences:

| Feature | AOBRD | ELD |
|---|---|---|
| Mandatory edits w/ annotation | No | Yes |
| Data file format | Carrier-specific | FMCSA standardized |
| Tamper resistance | Basic | Hardened |
| 8-day data display | Yes | Yes |
| Personal conveyance separation | Optional | Required |
| Mandatory roadside transfer | Carrier-specific | FMCSA standardized |

All AOBRD-only fleets had to transition by Dec 16, 2019.

## Common ELD violations + how to prevent

1. **Unidentified driver records** — when the truck is moving and no driver is logged in, the ELD creates "unidentified driving" records. Carrier MUST review + assign these within reasonable time. Auditors flag this.
2. **Falsified logs / log book violations** — even with ELDs, drivers can falsify by logging "off duty" while actually working. ELD GPS data exposes this.
3. **ELD not on registered list** — buying a cheap unregistered "ELD" violates 49 CFR 395.20.
4. **No paper backup for an 8-day malfunction.** ELD goes down and driver doesn't reconstruct on paper = violation.
5. **Carrier edits without driver acknowledgment.** Driver must confirm edits.
6. **Personal conveyance abuse.** "Driving home" 200 miles = not personal conveyance. FMCSA has issued guidance on what's reasonable.

## Where this fits in X3

X3's `hos-eld.html` page integrates with major ELD providers (Samsara, Geotab, Motive, etc.) and ingests duty status data. Unidentified driving records are flagged to the safety manager. ELD malfunctions are tracked + 8-day repair deadlines surface to the dashboard.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=eld-mandate-compliance

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
