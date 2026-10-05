---
name: new-entrant-safety-audit-prep
description: |
  Use this skill when the user asks specifically about preparing for the New Entrant Safety Audit (NESA) under 49 CFR 385 Subpart D — different from a Compliance Review. Covers what auditors look at, the 18-month window, automatic failure conditions, the 60-day fix window, what to NOT do, and how to convert from "new entrant" to permanent authority. Cite 49 CFR 385.301-321.
---

# New Entrant Safety Audit (NESA) Prep — 49 CFR 385 Subpart D

Every new motor carrier (whether for-hire or private; interstate property or passenger) goes through a NESA within 18 months of operating authority issuance. It's lighter than a full Compliance Review but failure means losing your operating authority.

## When the audit happens

- 18 months from USDOT number issuance / authority issuance
- Auditor typically schedules 30-90 days in advance
- Can be on-site (at carrier's office) OR offsite (records mailed/uploaded to FMCSA)
- Most NESAs are scheduled when the carrier reaches certain milestones (e.g., 100 inspections, first roadside violation)

## What's reviewed in a NESA (49 CFR 385.305)

The NESA is a **safety performance evaluation** — focused on:

1. **Driver Qualification Files** (a sample of drivers)
2. **Hours of Service records** (a sample of 7-10 days)
3. **Drug & Alcohol testing program** (verifies program exists + records sample)
4. **Vehicle maintenance records** (annual inspection certificates + a sample of DVIRs)
5. **Carrier-level docs:**
   - MCS-150 current
   - Insurance filing active
   - BOC-3 designation on file
   - USDOT number displayed on vehicles

Compared to a Compliance Review (which audits ALL drivers + ALL vehicles), NESA samples.

## Automatic failure conditions (49 CFR 385.321)

A carrier auto-fails if the auditor finds ANY of the following (the "Automatic Failure" list):

1. **Driver with a positive drug or alcohol test** still operating
2. **No drug & alcohol testing program**
3. **Driver operating without valid CDL** (or expired)
4. **Driver operating without valid medical certificate**
5. **Failure to maintain Driver Qualification Files**
6. **Failure to retain Hours of Service records**
7. **Vehicle without current annual inspection**
8. **Operating vehicle declared OOS** at roadside without repair
9. **No vehicle maintenance program**
10. **Operating without insurance OR insurance lapsed**

Any one of these = automatic failure.

## Outcomes

- **Pass:** Carrier is granted permanent operating authority. Conditional or Satisfactory rating issued.
- **Fail:** Must remediate within 60 days OR lose authority.

If the carrier fails to remediate:
- USDOT number remains active (carrier may not operate)
- MC number revoked
- New entrant status carries forward; carrier must reapply OR appeal

## 60-day remediation window

If you fail the NESA:

1. Auditor issues a "Failure to Pass" finding letter
2. Within 60 days, you must:
   - Fix all identified deficiencies
   - Submit a corrective action plan
   - Provide proof of remediation (e.g., new medical certs filed, missing DQ docs created, training records)
3. FMCSA may schedule a "Follow-Up NESA" to verify
4. If follow-up shows compliance: rating upgraded, permanent authority granted
5. If failure: operating authority terminated

## How to prepare 90 days out

**T-90: Self-audit**

- Pull a sample of 5-10 drivers; check DQF completeness (use the DQF skill).
- Pull 30 days of ELD records; check for HOS violations, missing ELD log days, blank duty status.
- Pull D&A program records; verify random testing happened on schedule.
- Pull vehicle records; verify annual inspections are current.
- Check MCS-150 currency.
- Verify insurance is active.

**T-60: Fix what you found**

- Missing medical certs? Get drivers re-tested.
- Missed Clearinghouse queries? Run them.
- Missing DVIRs? Backfill if possible OR document training going forward.
- Document remediation.

**T-30: Run a mock audit**

- Have a consultant or experienced safety manager from another carrier review your files using the actual NESA checklist (FMCSA Form MCS-150 + drilling questions).

**T-7: Final readiness**

- All required records in one place (digital + paper backup).
- Brief your designated supervisor.
- Confirm office space + Wi-Fi for the auditor.

## Day-of audit tips

- Single point of contact (typically the safety manager or owner).
- Be polite + professional. Auditors have discretion.
- Provide documents promptly but don't volunteer extra information.
- If you don't know, say "let me find that and follow up" — never guess.
- Take notes on what's being reviewed.

## After the audit

- Auditor issues findings within 30 days.
- Request a copy of the findings.
- If "Pass" — you're a permanent carrier. Celebrate, but stay vigilant.
- If "Fail" — start the 60-day remediation immediately.

## Common NESA failures

1. **No D&A program / no random testing schedule.** Auto-fail.
2. **Drivers operating with expired medical certs.** Auto-fail.
3. **No vehicle maintenance records.** Auto-fail.
4. **No DQF on a randomly-sampled driver.** Critical violation.
5. **Insurance lapse during the audit period.** Auto-fail.
6. **MCS-150 not updated.** Critical.

## NESA vs Compliance Review

| Feature | NESA | Compliance Review |
|---|---|---|
| Trigger | First 18 months of operation | Triggered (poor CSA, complaint, accident) |
| Scope | Sample-based | All drivers, all vehicles, all records |
| Outcome | Pass / Fail (with 60-day remediation) | Satisfactory / Conditional / Unsatisfactory |
| Authority impact | Auto-fail = lose new-entrant status | Unsatisfactory = lose authority |
| Frequency | One-time | Triggered by events |

A passing NESA grants permanent authority but doesn't immunize from future Compliance Reviews. CSA scores still matter going forward.

## Where this fits in X3

X3's `audit-export.html` page can be used to assemble a NESA-ready bundle of all DQ files, D&A program records, HOS sample, and vehicle inspections. `agent-pre-dot-audit-prep` runs the T-90 self-audit and creates a checklist.

A new carrier signing up to X3 should run a NESA self-audit within their first 12 months — typically Joshua's intake call covers this.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=new-entrant-safety-audit-prep

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
