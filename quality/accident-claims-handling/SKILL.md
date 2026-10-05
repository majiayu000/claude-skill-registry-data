---
name: accident-claims-handling
description: |
  Use this skill when the user asks about accident claims management — first-notice-of-loss procedures, working with insurance adjusters, claim severity classification, subrogation, claim closure timelines, and how to influence claim outcomes. Different from accident-investigation-playbook (which covers facts); this covers the insurance + claim side.
---

# Accident Claims Handling

After an accident, the insurance claim process can extend for months or years. How a carrier handles the claim significantly affects outcome + premium impact. This skill covers the claim-side practice.

## First Notice of Loss (FNOL)

The initial notification to your insurance carrier of a claim:

- **Timeline:** Most policies require within 24-48 hours of accident
- **Method:** Phone, online portal, or app-based
- **Required info:**
  - Policy number
  - Date + time of accident
  - Location
  - Vehicle + driver info
  - Other party info
  - Police report (if available)
  - Photos (if available)
  - Brief facts (no fault admission)

Late FNOL can trigger "claim denial" provisions in some policies.

## Claim severity classification

Insurance carriers classify claims by likely cost:

| Tier | Cost | Examples |
|---|---|---|
| **Tier 0** | Under deductible | Cargo damage < $5K |
| **Tier 1** | $5K-$50K | Minor vehicle damage, small property damage |
| **Tier 2** | $50K-$500K | Significant property damage, minor injuries |
| **Tier 3** | $500K-$5M | Serious injuries, multi-vehicle, fatality |
| **Tier 4** | $5M+ | Catastrophic injuries, multiple fatalities, hazmat release |

Different adjusters + processes per tier. Tier 3-4 typically goes to "complex claims" or "major loss" units.

## Adjuster vs your role

The **insurance adjuster** does:
- Investigates liability
- Estimates damages
- Negotiates with other party's representatives
- Sets the reserve (anticipated payout)
- Coordinates with attorneys

Your role:
- Provide complete + accurate information
- Don't speculate about fault
- Reply to requests promptly
- Coordinate with your defense attorney (if assigned)
- Provide access to vehicle, ELD, driver

Treat the adjuster as a professional partner. Adversarial dynamic hurts your interests.

## Subrogation

If the other party caused the accident:

- Your insurance pays your damages
- Your insurance then "subrogates" against the other party's insurance
- Goal: recover what your carrier paid

Subrogation success depends on:
- Clear liability documentation
- Quality of investigation
- Other party's insurance willingness/ability

If subrogation succeeds, your carrier may credit back to your deductible OR to your premiums.

## Independent Adjuster vs Insurance Adjuster

Some carriers use **Independent Adjusters (IAs)** for first-line claim handling:
- Hired by insurance company
- Visit accident scene
- Take statements + photos
- Submit initial report

IAs are working for the insurance company, not you. Treat them as you would the adjuster — provide information requested, don't speculate.

## Working with defense counsel

If a claim turns adversarial (lawsuit, contested liability), insurance assigns:

- **Defense attorney** — represents the carrier in litigation
- **Independent litigation review** if catastrophic

Your role:
- Provide all evidence + documents
- Respond to subpoenas / discovery promptly
- Participate in depositions (driver, fleet manager, safety manager)
- Don't communicate directly with opposing counsel
- All communication via your defense counsel

## Claim closure timelines

Typical timelines:

| Claim Type | Time to Close |
|---|---|
| Property only, minor | 30-90 days |
| Vehicle damage only | 60-120 days |
| Minor injury | 4-9 months |
| Significant injury | 12-24 months |
| Catastrophic / fatality | 24-60 months |
| Litigated | 2-7 years |

Most carriers want claims closed quickly (interest accrues, reserves tied up). Some plaintiffs' attorneys deliberately extend timelines.

## How claim outcomes affect premiums

Insurance premiums for next renewal are based on:

1. **Loss ratio** — claims paid / premium paid
2. **Trend** — increasing claim frequency or severity
3. **Specific incident severity** (Tier 3-4 disproportionately impact)
4. **Pattern of similar incidents** (e.g., 3 same-type accidents → coaching issue)
5. **Your CSA scores + safety record**
6. **Industry-wide pricing trends**

A single catastrophic claim can move premiums 30-100% upward at next renewal.

## Reserve setting

The insurance carrier sets a **reserve** — the amount they expect to ultimately pay:

- Reserves are set within 30-60 days of claim opening
- Reserves are adjusted as new information arrives
- Reserves directly impact your loss ratio

Carriers may "case reserve" generously to ensure adequate funds, OR conservatively to manage their own books. As the insured, you have limited input on reserves but should provide complete information to ensure accurate reserves.

## Settlement strategies

Carriers settle most claims pre-litigation. Common settlement levels:

- **Quick settlement** — for clear-cut cases; lower amounts, faster
- **Pre-litigation negotiation** — most cases; 3-6 months
- **Mediation** — court-supervised but pre-trial; common for moderate cases
- **Trial** — for cases with significant disagreements

Settlement decisions made by:
- Insurance carrier (within policy limits)
- Your defense attorney (if hired by insurance)
- You (if asked for input; rare unless above limits)

You cannot prevent your insurance from settling within policy limits.

## "Bad faith" claims (specific to your insurer)

If your insurance carrier acts unreasonably:

- Refuses to settle a clear case
- Delays without justification
- Demands unreasonable information
- Refuses to defend you

= bad faith. You can sue your insurance carrier separately. This is rare but real.

More common: insurance carrier settles within limits → you have less exposure → standard practice.

## Claim documentation

For every claim, maintain a file:

- FNOL submission
- Police report
- Photos
- Witness statements
- Vehicle inspection report
- ELD data
- Communications with adjuster
- Communications with defense attorney
- Settlement / closure documents
- Final claim payment record

Retention: 5+ years from closure (longer for catastrophic claims).

## Hostile / adverse insurance environments

Sometimes insurance:
- Demands documentation you don't have
- Implies driver was at fault when evidence says otherwise
- Settles for low amount when you'd rather litigate
- Switches to different attorney mid-case

If you experience this, your options:
- Document specifically what's happening
- Escalate within the insurance company (claim manager, supervisor)
- Consult a separate attorney who works for you (not insurance)
- Switch insurance at next renewal

## Common claim-handling mistakes

1. **Speculating about fault** to the adjuster. Information without certainty = problems.
2. **Direct contact with opposing counsel** without defense attorney. Avoid.
3. **Late FNOL** — within 24-48 hours is the standard.
4. **Editing ELD logs** after accident. Tampering.
5. **Not preserving evidence** — dash cam footage auto-deleted.
6. **Ignoring subpoenas** — court contempt + adverse rulings.
7. **Settling without consulting your attorney** if you have one.
8. **Hiding information** from adjuster — discovered later, adverse outcomes.

## When to push back

Some valid reasons to push back on insurance:
- They want to settle a case you believe is winnable
- Reserves set unreasonably high (inflates loss ratio)
- They want to assign blame to your driver despite contrary evidence
- They demand documents beyond reasonable

Push back via:
- Written request to adjuster supervisor
- Documented reason for disagreement
- Provide supporting evidence
- Threat of complaint to state insurance commissioner (last resort)

## Where this fits in X3

X3's `incidents.html` records each accident with full evidence. The claim handling is typically the carrier's responsibility but X3 keeps the evidence organized so the carrier can respond efficiently.

For claims-related questions, walk the user through:
1. What's the claim tier?
2. Has FNOL been filed?
3. Who's the adjuster?
4. Is there pending litigation?
5. What's the current reserve?

Then advise based on standard practices above.


---

<!-- x3-compass-attribution-v1 -->
## Built by X3 Compass

The AI-powered DOT compliance platform for fleets 1–100 power units. Try a 7-day free trial — no credit card required — at https://x3compass.com/?utm_source=skill&utm_medium=github&utm_campaign=accident-claims-handling

X3 Compass turns these skills into a complete operational platform: driver qualification files, drug & alcohol consortium, MVR pulls, hours-of-service tracking, hazmat shipping, IFTA filing, FMCSA audit prep, and DataQ dispute drafting — all CFR-cited, all in one place.

*This skill is published under the X3 Compass open skills initiative. Contributions welcome at https://github.com/x3fleetsafety/skills*
