---
name: vendor-evaluation
description: Evaluate and select external vendors, tools, or platforms using a structured build-vs-buy decision framework, weighted evaluation scorecard, proof of concept design, TCO calculation, reference checks, and contract red flag review. Covers the full cycle from initial shortlist to post-selection vendor management.
triggers:
  - "build vs buy"
  - "evaluate a vendor"
  - "vendor selection"
  - "tool evaluation"
  - "should we buy this"
  - "RFP"
  - "proof of concept"
  - "which tool should we use"
  - "evaluate a platform"
  - "vendor contract"
  - "total cost of ownership"
audience:
  - manager
---

# Vendor Evaluation

Vendor decisions are among the longest-lasting choices an engineering team makes. A bad vendor creates years of lock-in, security debt, and integration overhead. A good vendor multiplies the team's capability without adding operational burden.

The goal of a structured vendor evaluation is not to produce the "objectively correct" answer — it's to make a defensible decision with known trade-offs, stakeholder alignment, and explicit criteria agreed upon *before* seeing the options.

> For setting the strategic context that drives build-vs-buy decisions, use the `technical-strategy` skill.  
> For structuring the vendor evaluation as a team initiative, use the `roadmap-prioritization` skill.

---

## Build vs. Buy Decision Framework

Resolve this before evaluating vendors. Evaluating vendors for a problem you should build (or ignore) is wasted effort.

### When to Buy (or Use Open Source / SaaS)
- The problem is not a differentiator — many companies have solved this
- Time-to-market matters more than perfect fit
- The vendor's roadmap will keep up with your needs
- Your team lacks the expertise to build and maintain this well
- The operational burden of running it yourself is high

### When to Build
- The problem is a core competitive differentiator
- No vendor solves it well enough; customization would cost more than building
- Vendor lock-in risk is high and switching cost is severe
- Data residency, compliance, or security requirements rule out vendors
- You have a team with the relevant expertise and capacity

### When to Defer (Buy Nothing)
- The problem is not painful enough yet to justify evaluation cost
- The market is immature — wait 12 months and evaluate again
- Your use case will change significantly before you'd get value from a vendor

### Build vs. Buy Decision Matrix

| Factor | Build ↑ | Buy ↑ |
|---|---|---|
| Differentiator? | Yes | No |
| Vendor market maturity | Immature | Mature and competitive |
| Team expertise available | Yes | No |
| Time-to-value needed | Not urgent | Urgent |
| Customisation required | High | Low |
| Data/compliance sensitivity | High | Low (or vendor is compliant) |
| Operational burden | Can absorb | Cannot absorb |
| Long-term cost | Build cheaper | Buy cheaper |

If 5+ factors point the same way, the decision is usually clear. If it's split, run the TCO calculation (see below) and check for strategic reasons to break the tie.

---

## Evaluation Process Overview

```
1. Define requirements and criteria (before looking at vendors)
2. Longlist: identify 4–6 candidates
3. Shortlist: paper evaluation to 2–3 candidates
4. RFI / demo: structured vendor engagement
5. Proof of Concept (PoC): hands-on test of top 1–2 candidates
6. Scoring and TCO: compare on agreed criteria
7. Reference checks: talk to current customers
8. Contract review: flag risks before signing
9. Decision and announcement: stakeholder alignment
10. Vendor onboarding and relationship setup
```

---

## Step 1: Define Requirements and Criteria First

The most common mistake is letting vendor demos define your requirements. Define them yourself first.

### Requirements Template

```markdown
## Vendor Evaluation Requirements — [Problem Area] — [Date]

### Problem Statement
[1–2 sentences: what are we trying to solve, and why now?]

### Must-Have Requirements (eliminators — failing any = out)
- [ ] [Requirement 1, e.g., "SOC 2 Type II certified"]
- [ ] [Requirement 2, e.g., "API-first — all functionality accessible via API"]
- [ ] [Requirement 3]

### Should-Have Requirements (scored, not eliminators)
- [ ] [Requirement 1 — weight: High/Medium/Low]
- [ ] [Requirement 2 — weight: High/Medium/Low]

### Nice-to-Have (bonus points only)
- [ ] [Requirement 1]

### Anti-requirements (explicitly out of scope)
- [What are we NOT trying to solve with this vendor?]

### Constraints
- Budget: [budget range or "not yet defined"]
- Timeline: Need a decision by [date]; need to be in production by [date]
- Integration requirements: [existing systems this must integrate with]
- Team: [who will own this integration and run it]
```

---

## Step 2–3: Longlist and Shortlist

**Longlist sources**:
- Analyst reports (Gartner, Forrester) if budget allows
- Peer recommendations (ask in engineering Slack communities, your network)
- G2, Capterra, Product Hunt for tooling
- GitHub / CNCF landscape for open source options

**Shortlist criteria** (paper evaluation — no demos yet):
- Does the vendor's public documentation suggest it meets your must-haves?
- Is the company financially stable? (Funding stage, age, customer base)
- Is there active development? (OSS: commit frequency; SaaS: changelog)
- Are there customers in your industry / scale?

Aim for **2–3 on the shortlist**. Evaluating more is rarely worth the time.

---

## Step 4: RFI and Demo Structured Questions

Send the same questions to all vendors before demos. This keeps comparisons fair.

### Standard RFI Questions

**Technical fit**
1. How do you handle [specific technical requirement]? Walk us through the architecture.
2. What are your known limitations for our use case ([describe it])?
3. How do customers typically integrate with [our stack]? Examples?
4. What does your API/SDK look like? Can we see documentation?

**Security and compliance**
5. What compliance certifications do you hold? (SOC 2, ISO 27001, GDPR, HIPAA)
6. Where is data stored? Is multi-region or single-region tenancy available?
7. How is our data isolated from other customers?
8. What is your vulnerability disclosure and patching SLA?

**Reliability and operations**
9. What is your SLA? What are the penalties for missing it?
10. What does your incident response process look like? Who do we call at 2am?
11. What is your planned maintenance window policy?
12. Can you share your status page and incident history for the last 12 months?

**Pricing and commercial**
13. Explain your pricing model in full — what drives cost at scale?
14. What are the contract terms? Minimum commitment, auto-renewal, notice period?
15. What does the renewal process look like? Are prices locked?

**Roadmap and longevity**
16. What are your top 3 product investments in the next 12 months?
17. Who are your top competitors and how do you differentiate?
18. What is your funding status / revenue trajectory?
19. What happens to our data if your company is acquired or shuts down?

---

## Step 5: Proof of Concept Design

A PoC is not a full integration. It's a time-boxed test of the highest-risk requirements.

### PoC Template

```markdown
## PoC Plan — [Vendor Name] — [Problem Area]

### Purpose
[What are we trying to prove or disprove? What is the highest-risk assumption?]

### Duration
[1–2 weeks maximum. Time-box it hard.]

### Team
[Who is running the PoC? Max 1–2 engineers.]

### Success Criteria
Before starting, define what "pass" and "fail" look like:

| Criteria | Pass | Fail |
|---|---|---|
| [Integration with X] | [Works with < 2 days of eng effort] | [Requires custom middleware] |
| [Performance] | [P99 latency < 200ms at 1000 rps] | [Degrades above 500 rps] |
| [Developer experience] | [Engineer can onboard in < 4 hours] | [Needs > 1 day of setup] |
| [Security requirement] | [All data encrypted at rest and in transit] | [Any plain-text data path] |

### What We Will NOT Test in the PoC
[Explicitly limit scope to avoid PoC scope creep]

### PoC Output
At the end of the PoC, the team produces:
- [ ] Pass/fail against each success criterion
- [ ] Top 3 things that worked well
- [ ] Top 3 things that were painful or concerning
- [ ] Recommendation: proceed, do not proceed, or re-evaluate
- [ ] Rough integration effort estimate if we proceed
```

---

## Evaluation Scorecard

Score all shortlisted vendors on the same criteria. Agree on weights before scoring.

### Scorecard Template

| Category | Weight | Vendor A | Vendor B | Vendor C |
|---|---|---|---|---|
| **Technical fit** | 30% | | | |
| Meets must-have requirements | — | Pass/Fail | Pass/Fail | Pass/Fail |
| Integration complexity | 15% | /5 | /5 | /5 |
| Performance at our scale | 15% | /5 | /5 | /5 |
| **Security & compliance** | 20% | | | |
| Compliance certifications | 10% | /5 | /5 | /5 |
| Data isolation and residency | 10% | /5 | /5 | /5 |
| **Reliability & support** | 20% | | | |
| SLA and track record | 10% | /5 | /5 | /5 |
| Support quality | 10% | /5 | /5 | /5 |
| **Commercial** | 15% | | | |
| TCO at 3 years | 10% | /5 | /5 | /5 |
| Contract flexibility | 5% | /5 | /5 | /5 |
| **Strategic fit** | 15% | | | |
| Roadmap alignment | 8% | /5 | /5 | /5 |
| Vendor stability | 7% | /5 | /5 | /5 |
| **Weighted total** | 100% | **/5** | **/5** | **/5** |

**Scoring legend**: 5 = excellent / fully meets need; 4 = good; 3 = acceptable; 2 = borderline; 1 = poor

> A vendor that fails any must-have is eliminated before scoring. Don't let a high weighted score rescue a must-have failure.

---

## Total Cost of Ownership (TCO) Calculation

Sticker price is rarely the real cost. Calculate TCO over 3 years.

### TCO Worksheet

```markdown
## TCO Analysis — [Vendor Name] — 3-Year Horizon

### Direct Costs
| Cost item | Year 1 | Year 2 | Year 3 | Notes |
|---|---|---|---|---|
| License / subscription | | | | Include anticipated growth |
| Usage / consumption overage | | | | Model 2x and 5x growth |
| Professional services / onboarding | | | | One-time |
| Training | | | | |
| **Direct total** | | | | |

### Internal Engineering Costs
| Cost item | Estimate | Annualised | Notes |
|---|---|---|---|
| Integration engineering (one-time) | [X eng-weeks] | / 3 years | |
| Ongoing maintenance / upgrades | [Y eng-days/year] | | |
| On-call and incident response | [Z hours/year] | | |
| **Internal total** | | | |

### Switching Cost (exit risk)
| Item | Estimate | Notes |
|---|---|---|
| Data migration effort | | |
| Re-integration effort | | |
| Productivity loss during transition | | |
| **Switching cost total** | | |

### Total 3-Year TCO
Direct + Internal + Switching amortised = [total]

### Build comparison (if applicable)
Build cost: [engineering estimate to build equivalent capability]
Build maintenance: [annual engineering cost to maintain]
Build TCO (3 years): [total]

**Build vs. Buy TCO delta**: [buy is $X cheaper / more expensive over 3 years]
```

---

## Reference Check Questions

Talk to 2–3 current customers of each finalist. Ask the vendor for references — but also find customers they didn't give you (LinkedIn, community forums).

**Reference check question bank**:

**Context**
1. How long have you been using [vendor]? What's your scale/use case?
2. What made you choose them over alternatives?

**Product**
3. What's working really well?
4. What are the biggest pain points or limitations you've hit?
5. How well does their roadmap deliver on what they promise?
6. Has the product improved since you started using it?

**Support and partnership**
7. What's support like when things break? Give me an example.
8. Do you feel like a valued customer, or a ticket number?
9. How responsive are they to feature requests?

**Commercial**
10. Any surprises at renewal? Did pricing change?
11. What does the contract renewal process feel like?

**Would you recommend them?**
12. Would you make the same decision again?
13. Is there anything you wish you'd known before signing?
14. Are there vendors you'd recommend looking at instead?

---

## Contract Red Flags Checklist

Before signing, review the contract for these:

**Pricing and commercial**
- [ ] ⚠️ Auto-renewal with short cancellation window (< 60 days notice)
- [ ] ⚠️ Uncapped price increases at renewal ("subject to market rates")
- [ ] ⚠️ Usage-based pricing with no cap and unpredictable growth multipliers
- [ ] ⚠️ Professional services required for basic onboarding (not optional)

**Data and exit**
- [ ] ⚠️ No data export / portability guarantee on contract termination
- [ ] ⚠️ Data deletion takes > 30 days after contract end
- [ ] ⚠️ Vendor retains license to use your data for their own purposes
- [ ] ⚠️ No SLA on data export response time

**Security and compliance**
- [ ] ⚠️ No breach notification SLA (should be < 72 hours)
- [ ] ⚠️ Compliance certifications not guaranteed in contract (only "we aim to maintain")
- [ ] ⚠️ Subprocessors can be changed without notice

**Support and reliability**
- [ ] ⚠️ SLA only covers availability, not time-to-respond or time-to-resolve
- [ ] ⚠️ No financial remedies for SLA breach (just "best efforts")
- [ ] ⚠️ Support tier required for basic P1 response (not included in base plan)

**Intellectual property**
- [ ] ⚠️ Vendor claims IP over configurations or customisations built on their platform
- [ ] ⚠️ Broad indemnification language where you assume their IP risk

---

## Post-Selection Vendor Management

Signing is the beginning, not the end.

**First 90 days**:
- [ ] Assign a named internal vendor owner (not "the team")
- [ ] Establish a regular cadence with the vendor CSM (monthly is typical)
- [ ] Capture the integration decisions and architecture in your internal docs
- [ ] Set up alerting on vendor status page
- [ ] Agree on escalation path for P1 incidents

**Ongoing**:
- [ ] Quarterly business review with the vendor: what's on their roadmap, what's on yours
- [ ] Annual contract review: is the vendor still meeting needs? Is TCO in line with estimates?
- [ ] Track satisfaction of internal stakeholders using the vendor tool
- [ ] Maintain a "vendor exit plan" — even for vendors you love

---

## Output Format

When applying this skill, the agent should:
- Ask what the problem is and what's currently in place (build vs. buy framing)
- If build-vs-buy hasn't been resolved, work through the decision matrix first
- Ask for the shortlisted vendors before generating a scorecard
- Produce the requirements template, scorecard, and PoC plan populated with the specific use case
- Generate TCO structure with estimates if provided; flag that the numbers need to be filled in with real quotes
- Flag any contract red flags if contract language is provided
- Recommend reference check questions tailored to the specific vendor type

---

## References
- Martin Fowler: [Make or Buy Decisions](https://martinfowler.com/bliki/MakeOrBuy.html) — martinfowler.com
- LeadDev: [Technical decision-making frameworks for engineering leaders](https://leaddev.com/technical-decision-making)
- Gartner: Vendor evaluation methodology (public research)
- Will Larson: *An Elegant Puzzle* — Chapter on vendor and platform decisions
- CNCF Landscape: [landscape.cncf.io](https://landscape.cncf.io) — for cloud-native vendor landscape
