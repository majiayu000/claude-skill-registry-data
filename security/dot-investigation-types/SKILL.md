---
name: dot-investigation-types
description: |
  Use this skill when the user asks about FMCSA investigation types — Focused Investigation vs Comprehensive Review vs Compliance Review (CR) vs Investigation, when each is triggered, scope differences, on-site vs off-site, and how to prepare for each. Cite 49 CFR 385 Subpart C + D.
---

# FMCSA Investigation Types

FMCSA has multiple levels of carrier oversight. Each has a different trigger, scope, and consequence. This skill distinguishes them.

## 1. New Entrant Safety Audit (NESA) — 49 CFR 385 Subpart D

**Trigger:** All new carriers within 18 months of authority.
**Scope:** Sample-based — basic D&A program, sample DQF, sample HOS, vehicle maintenance basics, carrier registration currency.
**Outcome:** Pass = permanent authority; Fail = 60-day remediation OR lose authority.

See the `new-entrant-safety-audit-prep` skill for details.

## 2. Compliance Review (CR) — 49 CFR 385 Subpart B

**Trigger:** Generally triggered by:
- Poor CSA scores (BASIC above intervention threshold)
- A serious crash
- A complaint
- Random selection
- A previous CR Conditional rating

**Scope:** Comprehensive — auditor reviews ALL drivers' DQFs, ALL vehicles' maintenance records, 6+ months of ELD/HOS records, D&A program, insurance + authority docs.

**Outcome:** Safety rating issued:
- **Satisfactory** — No significant deficiencies
- **Conditional** — Some deficiencies; can continue operating but should remediate
- **Unsatisfactory** — Major deficiencies; 45-60 days to fix or lose authority

**On-site or off-site:** Typically on-site. May be off-site for limited reviews.
**Duration:** 1-5 days at the carrier's office.
**Frequency:** Reactive (when triggered), not scheduled.

## 3. Focused Investigation

**Trigger:** Specific concern triggered by:
- A specific crash (DOT-recordable, fatality)
- A targeted complaint
- One specific BASIC scoring high
- A single regulatory area concern (e.g., HOS violations from ELD data)

**Scope:** Narrower than CR — focuses on the specific issue area:
- Focused on Hours of Service if HOS BASIC high
- Focused on Vehicle Maintenance if VM BASIC high
- Focused on D&A if Controlled Substances BASIC high

**Outcome:** Findings letter + corrective action plan; safety rating may be adjusted but typically not changed.

**On-site or off-site:** Often off-site (records submitted electronically); can be on-site.

## 4. Off-Site Investigation

**Trigger:** Lower-risk concern OR initial follow-up to a Focused Investigation.
**Scope:** Records-only review; auditor doesn't physically visit.
**Outcome:** Findings + correction.

## 5. Comprehensive Review

**Trigger:** Most serious — typically:
- A pattern of violations across multiple BASICs
- A previous Unsatisfactory rating
- Major safety incident (multi-fatality crash, hazmat release)
- Reportable issue surfacing in CSA data

**Scope:** Most comprehensive of any review type. May include:
- Multiple on-site days
- All drivers' DQFs
- All vehicles' maintenance records
- 12+ months of ELD/HOS records
- Insurance review
- Operating authority review
- D&A program full review

**Outcome:** Safety rating with broad implications. Possible:
- Order to Cease Operations
- Civil penalties
- Criminal referral (rare)

## 6. State-Level Audits (separate from FMCSA)

States can perform their own audits for intrastate carriers + state-specific concerns:

- **California BIT (Basic Inspection of Terminals)** — yearly state inspection
- **Texas Railroad Commission oversight** — oil/gas-specific
- **State PUC audits** — for intrastate authority holders
- **State Workers Comp audits** — for worker classification

State + federal audits can run simultaneously.

## How to know which is coming

When you receive an audit notification, check:

| Letter type | Investigation Level |
|---|---|
| "Notice of New Entrant Safety Audit" | NESA |
| "Notice of Compliance Review" | Full CR |
| "Notice of Focused Investigation" | Focused |
| "Notice of Off-Site Investigation" | Off-Site |
| "Notice of Comprehensive Review" | Comprehensive |
| "Notice of Compliance Investigation" | Investigation (typically Comprehensive scope) |

The notification will specify:
- Type of review
- Scope (specific BASICs or all)
- Records requested
- On-site dates OR submission deadline
- Auditor name + contact

## Preparation by investigation type

### For NESA:
- See `new-entrant-safety-audit-prep` skill
- ~90 days self-audit
- Document everything

### For Focused (HOS):
- Pull last 6-12 months of ELD records
- Identify any violations + remediation
- Compile supporting documentation (BOL, dispatch records)
- Driver training documentation

### For Focused (Vehicle Maintenance):
- DVIRs (last 12 months)
- Annual inspection certificates
- Repair orders + invoices
- PM schedule + completion records

### For Focused (D&A):
- D&A program written policy
- Random testing pool + selection log
- Test results (separate file)
- MRO + SAP records
- Clearinghouse query records
- Supervisor reasonable-suspicion training records

### For Comprehensive Review:
- Everything above + insurance + operating authority
- Driver list with hire dates
- Vehicle list with annual inspection dates
- Last 12-24 months of CSA scoring + interventions
- 100% DQF sample readiness

## On-site investigation logistics

When FMCSA visits:

- Provide a quiet workspace + Wi-Fi
- Designate a single point of contact (typically safety manager)
- Schedule available staff (safety mgr, ops mgr, driver mgr if available)
- Have documents accessible (paper + digital)
- Don't volunteer information; answer what's asked
- Take notes on what's being reviewed
- Disagree professionally but document

## After the investigation

Within ~30 days, FMCSA sends:

- **Findings letter** — what was found + classification
- **Notice of Claim** if civil penalties proposed
- **Conditional or Unsatisfactory rating** if applicable
- **Corrective Action Plan request** if applicable

Carrier has:
- 60 days to request a Safety Rating upgrade (if Conditional)
- 60 days to contest findings via formal appeal
- 30 days to submit corrective action plans
- 30 days to pay civil penalties OR contest

## Penalties by investigation outcome

| Outcome | Penalty Range |
|---|---|
| Focused with minor findings | Warning letter; no civil penalty |
| Focused with significant findings | $5K-$50K civil penalties |
| CR with Satisfactory rating | None |
| CR with Conditional rating | Reputation hit; possible insurance/customer impact |
| CR with Unsatisfactory | $25K-$300K civil penalties + authority threatened |
| Comprehensive with major findings | $50K-$500K+ civil penalties + criminal referral possible |
| Egregious / Repeat offender | Multi-million civil penalties + authority revoked |

## Common investigation mistakes

1. **Ignoring the notification.** Schedule on-site visits as soon as possible.
2. **Not preparing for the specific type.** Focused HOS = bring HOS records, not everything.
3. **Volunteering information.** Stick to the questions.
4. **Arguing instead of documenting.** Disagreements go in writing; civil tone preserved.
5. **Not consulting an attorney for major investigations.** Comprehensive review = engage counsel early.
6. **Failing to submit corrective action plan.** Loses ability to upgrade rating.

## Where this fits in X3

X3's `audit-export.html` page assembles audit-ready packages tailored to investigation type. The `agent-pre-dot-audit-prep` Edge Function runs self-audits in advance. Mike Perry (X3's senior safety advisor) consults on Compliance Review prep + Unsatisfactory rating remediation.

When asked about an upcoming audit, walk the user through:
1. What type of investigation (letter type)?
2. What's the specific scope?
3. What's the timeline?
4. What records need to be prepared?


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=dot-investigation-types

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
