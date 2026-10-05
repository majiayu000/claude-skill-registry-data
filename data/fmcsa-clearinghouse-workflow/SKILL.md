---
name: fmcsa-clearinghouse-workflow
description: |
  Use this skill when the user asks about the FMCSA Drug & Alcohol Clearinghouse — full vs limited query, pre-employment vs annual query, query credit purchasing, who has access (employers, drivers, MROs, SAPs, state licensing agencies), reporting violations to the Clearinghouse, the "prohibited" status workflow, consent forms, or how to register/use the clearinghouse.fmcsa.dot.gov portal. Cite 49 CFR 382.701-727.
---

# FMCSA Drug & Alcohol Clearinghouse — 49 CFR 382.701-727

The Clearinghouse is FMCSA's federal database of CDL driver drug & alcohol violations. **Mandatory effective Jan 6, 2020.** All testing violations must be reported; all employers must query.

## Two query types

| Query | Required When | Consent | Cost |
|---|---|---|---|
| **Pre-Employment Full Query** | Before hiring/contracting any CDL driver | Driver-specific electronic consent | $1.25 |
| **Annual Limited Query** | At least once every 12 months for every active CDL driver | One-time blanket consent at hire | $1.25 |

**Limited query** returns "yes/no" — does this driver have any Clearinghouse records? If yes, you must then conduct a Full Query (with separate consent) within 24 hours to see details.

**Full query** returns: every violation, refusal, RTD status, follow-up status.

## Reportable violations (49 CFR 382.705)

Employers, MROs, SAPs, and state licensing agencies report:

- Verified positive drug test (employer + MRO each report)
- Verified positive alcohol test (≥ 0.04)
- Test refusal (any of the 9 refusal reasons under 49 CFR 40.191)
- Actual knowledge violation (saw the driver drinking on duty, etc.)
- RTD test results
- SAP "successful completion" reports
- Follow-up test results

Reporting deadline: **3 business days** for most violations.

## Driver "prohibited" status

A driver is "prohibited" from operating a CMV in safety-sensitive functions when they have:

- Any violation that hasn't been resolved through SAP + RTD test, OR
- A positive pre-employment test (until SAP completion)

A "prohibited" driver appears as such in Clearinghouse queries. They cannot be hired, retained in CDL function, or re-instated until they complete SAP + RTD.

## How to register & use the portal

For employers:

1. Go to `clearinghouse.fmcsa.dot.gov`
2. Create an account with FMCSA Portal credentials (or USDOT-tied login)
3. Establish your designated Consortium/Third-Party Administrator (C/TPA) if applicable
4. **Purchase query credits** (or buy a "Query Plan" annual subscription)
5. Use the portal to query individual drivers OR batch upload a CSV of drivers for annual limited queries

## Consent forms

The Clearinghouse-mandated consent forms are:

- **Full Query Consent** (electronic, driver-signed in the Clearinghouse portal) — required for each Full Query
- **Limited Query Consent** (paper, blanket, one-time) — required to perform Limited Queries on this driver for the duration of employment

**Critical:** The Limited Query Consent does NOT cover Full Queries. You must obtain separate Full Query consent for the pre-employment query.

## C/TPA (Consortium / Third-Party Administrator)

Smaller carriers often designate a C/TPA (e.g., DISA, US HealthWorks, or any DOT-compliant TPA) to handle:

- Random selection pool management
- Clearinghouse queries on the carrier's behalf
- Test result tracking
- MRO interface

The C/TPA is granted Clearinghouse access via the employer's designation. Cost is typically a per-driver-per-month subscription.

## Query credit math

Query credits are pre-purchased. As of 2026:

- Single query: $1.25
- Annual unlimited query plans: not currently offered (you pay per query)
- Bulk discounts: minor (~$1.00 each at 1000+ credits)

For a 25-driver carrier:
- 25 × $1.25 pre-employment full queries (if all new hires) = $31
- 25 × $1.25 annual limited queries = $31
- Plus any post-violation follow-up queries
- ~$60-75/year for a stable fleet

## The "prohibited driver" workflow

A driver shows up as prohibited in your query. Now what?

1. **Remove from safety-sensitive function immediately** (and document).
2. Provide the driver with a list of qualified SAPs.
3. The driver completes SAP evaluation + treatment + re-evaluation.
4. Driver passes a RTD test (drug and/or alcohol, observed).
5. SAP submits the "successful completion" to Clearinghouse.
6. Driver's status changes to "not prohibited" in Clearinghouse.
7. Driver can be returned to CMV duty.
8. **Follow-up tests** continue for 1-5 years per SAP schedule.

If a prohibited driver tries to operate, they violate 382.501; the carrier violates 382.215.

## Common Clearinghouse mistakes

1. **Pre-employment query was Limited instead of Full** — common when carriers default to "Limited because it's cheaper." Limited returns yes/no only and may not satisfy pre-employment requirements.
2. **Annual Limited query missed for an active driver** — must be performed at least once every 12 months from the prior query.
3. **Failed to obtain Limited Query Consent at hire** — a Limited query without consent is a violation.
4. **Carrier doesn't report a verified positive within 3 days** — separate from MRO reporting; both must report.
5. **Carrier hires a driver showing "prohibited" without remediation** — violation under 382.703 + 382.219.

## State licensing agency interface

As of 2024 amendments, state CDL licensing agencies (DMVs) also query the Clearinghouse and downgrade a CDL to a non-commercial license when the driver is prohibited. This is the "downgrade" provision and can happen without warning to a driver who hasn't resolved a Clearinghouse violation.

## Where this fits in X3

X3 includes Clearinghouse query workflow in `dq-files.html` and surfaces "Clearinghouse status" on the driver record. `vendor_orders` can carry `vendor='clearinghouse'` orders for either Limited or Full query types. Once the FMCSA opens an API for employer queries (currently web-only), X3 will automate this.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=fmcsa-clearinghouse-workflow

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
