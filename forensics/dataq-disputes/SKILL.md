---
name: dataq-disputes
description: |
  Use this skill when the user asks about DataQ — FMCSA's data review system at dataqs.fmcsa.dot.gov — for disputing inspection violations, crash records, or other entries that appear in a carrier's CSA / SMS score. Covers Request for Data Review (RDR) process, success rates, common dispute grounds, what evidence to attach, timeline expectations, and how successful disputes reduce BSI (BASIC Severity Indicator) scores. Cite 49 CFR 392.7 and the FMCSA DataQs User Guide.
---

# DataQ Disputes — fmcsa.dot.gov/dataqs

DataQ is FMCSA's Request for Data Review (RDR) system. If a violation, crash, or inspection record is wrong, a carrier can challenge it. Successful disputes REMOVE the violation from the carrier's SMS BASIC scores (potentially dropping you below an intervention threshold). This is one of the highest-ROI compliance activities a carrier can do.

## What's disputable

- **Roadside inspection violations** — citations issued at a weigh station or roadside stop
- **DOT-recordable crashes** — entries in the crash file that shouldn't be there
- **Inspection assignments** — wrong carrier credited
- **Specific violation severity** — usually not (severity is set by FMCSA)
- **Inspection ratings** (Satisfactory / Conditional / Unsatisfactory) — appeal via formal post-audit process, not DataQ

## Common successful dispute grounds

| Ground | Example | Win rate |
|---|---|---|
| Vehicle wasn't yours | Sold/leased before incident | ~80% |
| Driver wasn't your employee | Independent contractor mis-identified | ~70% |
| Driver was off-duty (PC) | Inspector mis-classified personal conveyance | ~50% |
| Citation cited wrong CFR | Inspector wrote 393.45 but the actual problem was 393.75 | ~50% |
| Measurement was wrong | Brake stroke measured incorrectly | ~40% (need re-measurement evidence) |
| Carrier wasn't responsible party | Owner-operator under another DOT number | ~70% |
| Driver had been removed | Driver already terminated; should be on next carrier's record | ~60% |
| Conviction never happened | Citation issued but dismissed in court | ~85% (with court records) |

## Submission process

1. Go to `dataqs.fmcsa.dot.gov`.
2. Sign in with FMCSA Portal credentials.
3. Search for the inspection / violation / crash to dispute.
4. Click "File a Request for Data Review" (RDR).
5. Select the type of issue.
6. Write a clear, factual narrative.
7. Upload supporting documents (BOL, lease agreement, court disposition, ELD record, photographs, prior maintenance records).
8. Submit.

A confirmation email arrives. The RDR is routed to a **state Disposition Office** (usually the state where the inspection occurred).

## Timeline expectations

- 30 days: state begins review
- 30-60 days: state requests info from inspecting officer (if reachable)
- 60-90 days: outcome posted in DataQ
- 6+ months for complex disputes or stale records

## How successful disputes affect CSA scores

When a violation is **removed** via DataQ, it's removed from your SMS BASIC calculation effective the date of removal (not retroactively). Your peer percentile re-calculates within 30-60 days.

When a violation is **amended** (e.g., severity reduced), the new severity replaces the old.

When a crash is **removed** (e.g., wrong carrier), it drops out of Crash Indicator BASIC.

## What's NOT disputable

- The fact that an inspection occurred (just that the violations were wrong)
- The severity weight FMCSA assigns to a particular CFR violation (those are fixed in SMS Methodology)
- "I didn't agree with the inspector's interpretation" without evidence
- Cosmetic / formatting issues on the inspection report

## Writing a winning DataQ narrative

**Bad narrative:** "The inspector was wrong. We didn't have any defects."

**Good narrative:**
> On 04/15/2026, Inspection Report #IL2026-04123 cites Driver John Smith (CDL #M99887766) for 49 CFR 393.75(a) (worn tire tread depth). At the time of inspection, the vehicle was operated by ABC Trucking LLC (USDOT #1234567), not XYZ Carrier (USDOT #7654321). XYZ Carrier sold the vehicle to ABC Trucking on 03/01/2026 — see attached Bill of Sale (Exhibit A) and IRP plate transfer (Exhibit B). Both XYZ and ABC's USDOT numbers were displayed on the vehicle at time of sale, which may have caused inspector confusion. Request the violation be transferred from XYZ Carrier to ABC Trucking.

The good narrative:
- States the facts clearly with dates
- Identifies the specific inspection report number
- Names specific exhibits attached
- Explains how the error could have occurred
- Requests a specific outcome (transfer, not just remove)

## ROI math

A typical mid-sized carrier (50 power units) might have 10-30 disputable violations per year. Win rate is roughly 40-60% with well-documented disputes. Each successful dispute can:

- Drop the carrier's peer percentile by 1-5 points in the relevant BASIC
- Reduce roadside ISS score (fewer inspections triggered)
- Avoid an intervention letter ($5K-$50K downstream cost)

A safety manager spending 30-60 minutes per dispute, with a 50% win rate, ROI per hour is typically very high.

## Continuous improvement loop

Track every dispute outcome internally:

- Date inspection / dispute filed
- Specific violation
- Grounds for dispute
- Evidence attached
- Outcome
- Days to resolution

Patterns emerge — e.g., one state consistently mis-identifies your carrier, or one inspector has a habit of miscategorizing personal conveyance.

## Common DataQ mistakes

1. **Filing too late.** No formal deadline, but stale evidence (>1 year old) is harder to win.
2. **Insufficient evidence.** Narrative without exhibits = denial.
3. **Wrong dispute type.** Pick "Inspection Report Review" vs "Crash Reportability Review" carefully.
4. **Disputing severity** (you can't via DataQ).
5. **Filing on minor violations** instead of high-severity ones. A successful dispute on a severity-10 violation removes more from your BSI than three successful disputes on severity-1 violations.

## Where this fits in X3

X3's `csa-scores.html` page surfaces each violation with a "Dispute via DataQ" CTA. The X3 `agent-dataq-drafter` Edge Function takes a violation + carrier-supplied evidence and drafts a DataQ narrative for the safety manager to review and submit.

## When the user asks about a specific case

Walk them through:
1. What's the violation? (CFR citation + inspection report #)
2. What evidence do you have? (specific docs)
3. Which dispute ground applies? (use the table above)
4. Draft the narrative together
5. Note the timeline expectation

If the user is asking about a violation older than 24 months, it's already aged out of SMS — disputing is mostly symbolic at that point.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=dataq-disputes

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
