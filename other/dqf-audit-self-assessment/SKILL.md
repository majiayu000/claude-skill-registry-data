---
name: dqf-audit-self-assessment
description: |
  Use this skill when conducting a self-audit of your DQF library before an FMCSA compliance review. Covers the systematic approach to verifying all 12 documents are current, complete, and properly maintained.
---

# DQF Audit Self-Assessment Workflow

A self-audit catches DQF issues before FMCSA does. Run quarterly or before any expected compliance review.

## Step 1: Driver list verification
- Pull list of all drivers active in past 12 months (including terminated)
- Cross-reference against your DQF library (should have a file for each)
- Flag missing DQF files immediately

## Step 2: Per-driver completeness check
For each driver, verify these 12 documents are present:
- [ ] 1. Employment application (§ 391.21) — date hired, complete signature
- [ ] 2. Prior employer inquiries (§ 391.23) — sent + responded OR documented attempts
- [ ] 3. MVR — current (within last 12 months) + 3-year history
- [ ] 4. Annual review of driving record (§ 391.25) — within 12 months of hire/last review
- [ ] 5. Annual driver's certificate of violations (§ 391.27) — within 12 months
- [ ] 6. Medical examiner's certificate — current (not expired)
- [ ] 7. Medical examiner verification — National Registry number on file
- [ ] 8. Road test certificate OR equivalent — at time of hire
- [ ] 9. Safety performance history — completed at hire
- [ ] 10. Medical variance — if applicable
- [ ] 11. CDL copy — current
- [ ] 12. ELDT certificate — for drivers with first CDL after 2/7/2022

## Step 3: Document quality check
- Signatures and dates legible
- All sections completed (no blanks)
- Documents are signed by authorized parties (medical examiner from National Registry)
- Certificates not expired
- Old certificates archived (3-year retention for replaced documents)

## Step 4: Cross-reference with HR system
- Hire dates match between DQF and HR
- Termination dates flagged for 3-year retention countdown
- No "ghost drivers" in DQF without HR record (or vice versa)

## Step 5: Generate audit report
- Total drivers in DQF library
- Total drivers with complete files (target: 100%)
- Drivers with at least 1 missing document (action items)
- Drivers with expired documents (urgency)
- Average DQF "completeness score"

## Documentation
Save the self-audit results — at the next compliance review, demonstrating self-audit shows continuous improvement intent.

## How Compass automates this
Compass DQ Files module runs this audit continuously. Each driver has a "compliance score" based on document presence + currency. Daily digest surfaces the top 5 driver files needing attention.

## CFR citations
- **49 CFR § 391.51**
- **49 CFR § 391.53**
- **49 CFR Part 385 Subpart B**

## How Compass surfaces this
This skill is searchable in Compass Ask and runs against the carrier's actual fleet data when invoked from the relevant tracker. Read-only; no actions taken without explicit user approval.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=dqf-audit-self-assessment

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
