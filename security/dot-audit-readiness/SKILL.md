---
name: dot-audit-readiness
description: |
  Use this skill when the user asks about DOT audits, FMCSA compliance reviews, new entrant safety audits (NESA), focused investigations, what auditors actually ask for, audit document checklists, common audit failures, the audit ratings (Satisfactory / Conditional / Unsatisfactory), or how to prepare for an upcoming audit. Cite 49 CFR 385.
---

# DOT Audit Readiness — 49 CFR 385

There are three intervention levels in FMCSA's safety oversight ecosystem. Each has different scope.

## Audit types

### 1. New Entrant Safety Audit (NESA) — 49 CFR 385 Subpart D

Every new carrier gets one within 18 months of obtaining their USDOT number. Light-touch.

**What auditors look at:**
- Driver Qualification Files (a sample of drivers)
- Hours of Service logs / ELD records (a sample week)
- Drug & Alcohol testing program
- Vehicle maintenance records (a sample)
- MCS-150 currency

**Outcome:** Pass (carrier is granted permanent operating authority) or Fail (carrier must remediate within 60 days or lose authority).

### 2. Compliance Review (CR) / Compliance Investigation — 49 CFR 385 Subpart B

Triggered by: poor CSA scores, an accident, a complaint, or random selection.

**Scope:** Broad. Auditors review:
- DQ files for ALL drivers (not a sample)
- HOS records for at least 6 months back
- Maintenance records, DVIRs, inspection reports
- D&A testing program records
- Hazmat program (if applicable)
- Accident register
- Driver training records (ELDT compliance)
- MCS-150 + insurance filings
- All policies and procedures

**Outcome:** Safety rating issued: **Satisfactory / Conditional / Unsatisfactory**.

### 3. Focused Investigation / Off-Site Review

Targeted audit for a specific issue (e.g., a single fatal crash, a complaint about HOS violations). Narrower scope.

## What auditors physically ask for

Have these ready in advance:

**Driver files (DQF for each):**
- [ ] Application for employment (49 CFR 391.21)
- [ ] Inquiry to previous employers (3-year lookback) (391.23)
- [ ] MVR + signed note (annual) (391.25)
- [ ] List of violations (annual) (391.27)
- [ ] Medical examiner's certificate + NRCME verification (391.43)
- [ ] Road test certificate OR CDL equivalent (391.31)
- [ ] Entry-Level Driver Training certification (if applicable; 380.609)
- [ ] CDL copy

**Driver D&A records (separate file, secured):**
- [ ] Pre-employment test
- [ ] Random test schedule + results
- [ ] Any post-accident, reasonable suspicion, RTD, follow-up tests
- [ ] Clearinghouse query records (Pre-employment Full + Annual Limited)
- [ ] Supervisor reasonable-suspicion training records

**HOS / ELD records:**
- [ ] At least 6 months of ELD records (digital file or print)
- [ ] Supporting documents (fuel receipts, BOL, tolls, dispatch records) for sampled days
- [ ] Driver training on ELD use
- [ ] ELD malfunction logs (if any)

**Vehicle records:**
- [ ] Annual inspection (49 CFR 396.17) for each vehicle
- [ ] Periodic inspection records (per 49 CFR 396.21)
- [ ] DVIRs for at least 1 year
- [ ] Roadside inspection reports (driver-side + carrier-side)
- [ ] Repair invoices / work orders showing defects were addressed

**Carrier-level:**
- [ ] Accident register (49 CFR 390.15) for last 3 years
- [ ] Insurance filings (MCS-90 or BMC-91/91X)
- [ ] MCS-150 — current within 24 months
- [ ] BOC-3 designation
- [ ] Operating authority (MC number) — current
- [ ] State permits (UCR, IFTA, IRP)
- [ ] D&A program policy + designated supervisor + C/TPA contract
- [ ] Hazmat permit / security plan (if applicable)

**Hazmat-specific (if applicable):**
- [ ] Hazmat training records (49 CFR 172 Subpart H)
- [ ] Hazmat Safety Permit
- [ ] Emergency response phone number documented
- [ ] Driver hazmat endorsements

## Safety ratings (49 CFR 385.5)

| Rating | What it means | Authority impact |
|---|---|---|
| **Satisfactory** | Carrier has effective safety management controls | Continues to operate |
| **Conditional** | Some non-compliance found; may continue operating but should remediate | Continues; some shippers/insurers may decline |
| **Unsatisfactory** | Significant non-compliance; safety management controls inadequate | Operations halted after 45-60 days unless corrected |

If you get a **Conditional** rating, you can request an upgrade after corrective action — typically requires another audit or self-attestation.

If you get **Unsatisfactory**, you have a short window to fix things or shut down. Take this very seriously and consult a DOT attorney immediately.

## Acute & critical violations (49 CFR 385 Appendix B)

Certain violations are "acute" or "critical" — they auto-fail the audit:

**Acute violations** (single instance is enough):
- Using a driver who has been declared OOS
- Using a driver without a valid CDL
- Permitting a driver to operate with a positive D&A test
- Operating with an expired MCS-90 / no insurance filing
- HM violation involving improper packaging / placarding

**Critical violations** (pattern of violation matters):
- Failure to maintain DQF for each driver
- Failure to perform required testing (random, post-accident, etc.)
- Failure to maintain ELD/HOS records
- Failure to repair OOS vehicles
- Failure to maintain accident register

## How to prepare (90-day pre-audit checklist)

T-90: Self-audit
- Pull a random 10% of driver files and check the DQF list. Note gaps.
- Pull 90 days of ELD records and spot-check for violations / lockouts / missing duty status.
- Review last 12 months of D&A test pulls (random rate ≥ 50%? all results in MRO custody?).
- Verify Clearinghouse: Annual Limited query performed on every active driver within last 12 months?
- Check MCS-150 currency; insurance filings active.

T-60: Fix what you found
- File missing documents. If a medical cert is expired, get a new one.
- Catch up on any missed Clearinghouse queries.
- Document remediation actions.

T-30: Run a mock audit
- Have someone outside daily ops (or a consultant) audit your files using the actual FMCSA audit forms.

T-7: Final readiness
- Print/digital copies of all required records in one place.
- Brief your designated supervisor on what to expect.
- Confirm office space + Wi-Fi for the auditor.

## Day-of-audit etiquette

- Have a single point-of-contact (usually the safety manager).
- Provide documents promptly but don't volunteer unrequested information.
- Take notes on what's being reviewed and what questions are asked.
- If you don't know an answer, say "let me find that and get back to you" rather than guessing.
- Disagreements should be polite and documented; you can challenge findings via formal appeal post-audit.

## After the audit

If you receive a finding:

1. Request a copy of the audit findings in writing.
2. Have 60 days to appeal (49 CFR 385.15).
3. If you can't dispute, file a Safety Management Plan within the deadline.
4. Implement corrections; document each one.
5. Track remediation progress for the upgrade audit (if applicable).

## Where this fits in X3

X3's `audit-export.html` page generates an audit-ready PDF bundle of all DQ files, D&A test results, HOS sampling, and vehicle maintenance records. `agent-pre-dot-audit-prep` runs the T-90 self-audit and creates a checklist for the safety manager. Mike Perry (X3's senior advisor; 20-year NY State Police CMV inspector) reviews audit prep packages.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=dot-audit-readiness

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
