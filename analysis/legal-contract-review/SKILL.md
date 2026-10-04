---
name: legal-contract-review
description: "Reviews NDAs, SaaS contracts, MSAs, DPAs, and other legal documents with clause-by-clause analysis, risk rating (green/yellow/red), and red flag detection. Covers liability caps, IP ownership, confidentiality terms, governing law, indemnification, auto-renewal, and GDPR/SOC2/CCPA compliance language. Escalates to a human immediately for unlimited liability, IP assignment, unfavorable jurisdiction, or regulatory compliance requirements. Best for founders and operators signing vendor agreements, SaaS contracts, or partnership deals who want a structured review without hiring a lawyer for every NDA. Also for: contract comparison baselines, redline drafting, and negotiation alternative language."
---

# Legal Contract Review Skill

## When to Activate

Trigger when the user asks to:
- Review an NDA, MSA, DPA, SOW, or SaaS contract
- Analyze IP, liability, or termination clauses
- Check for GDPR, SOC2, or CCPA compliance language
- Draft a redline with recommended changes
- Compare contract terms to a standard baseline
- Flag auto-renewal, governing law, or indemnification concerns

## Review Workflow

1. Read the full document — do not skip the fine print
2. Extract every numbered clause
3. Compare each clause against the standard clause library below
4. Flag deviations with risk level (green / yellow / red)
5. Recommend action per the escalation triggers below
6. Output structured findings

## Standard Clause Library

| Clause Type | Standard (Green) | Yellow (Negotiate) | Red (Reject / Escalate) |
|---|---|---|---|
| Liability cap | Total liability capped at 12 months fees | Unlimited liability | No cap stated |
| IP ownership | Work product owned by client | Joint ownership | IP transfers to vendor |
| Confidentiality term | 2-3 years post-termination | Perpetual | — |
| Termination notice | 30-60 days written | 90+ days | Immediate termination without cause |
| Governing law | Neutral jurisdiction (e.g., Delaware) | Vendor's home jurisdiction | Foreign jurisdiction with enforcement risk |
| Indemnification | Mutual, capped at contract value | One-sided vendor indemnity | Broad vendor indemnity with no cap |
| Auto-renewal | No auto-renewal or 30-day opt-out | Auto-renewal with 60+ day notice | Auto-renewal with no opt-out window |
| Data residency | Data stays in agreed region | — | No data residency guarantees |
| SLA / uptime | 99.9% uptime, credit-based remedy | No SLA | No SLA + no remedy |
| Modification | Mutual written consent | Unilateral modification rights | Broad unilateral modification |

## Red Flag Checklist

- [ ] Unlimited liability exposure
- [ ] IP assignment or license-back to counterparty
- [ ] Perpetual confidentiality obligation
- [ ] Governing law in vendor's home jurisdiction
- [ ] Auto-renewal with no opt-out window
- [ ] Broad indemnification covering vendor's negligence
- [ ] One-sided termination rights
- [ ] No data export or portability provisions
- [ ] GDPR / CCPA non-compliance language
- [ ] Non-disparagement or broad PR restrictions
- [ ] Change of control triggers termination
- [ ] No limitation on consequential damages

## Structured Output Format

```
CONTRACT: [filename or title]
COUNTERPARTY: [company name]
DATE RECEIVED: [date]

CLAUSE ANALYSIS
─────────────────────────────────────────────────────────────────
#1  Limitation of Liability          [GREEN/YELLOW/RED]
    Clause: "Vendor's total liability shall not exceed..."
    Deviation: [none / from standard]
    Recommendation: [accept / negotiate / escalate]

#2  Intellectual Property            [GREEN/YELLOW/RED]
...

ESCALATION REQUIRED: [yes/no]
─────────────────────────────────────────────────────────────────
```

## Escalation Triggers — Escalate to Human Immediately

Escalate to a human legal professional when:
- Liability is unlimited or uncapped
- IP is assigned or licensed-back to counterparty
- Governing law is in an unfavorable or foreign jurisdiction
- The contract involves regulatory compliance (HIPAA, PCI-DSS, GDPR for EU data)
- The contract value or risk exposure is significant
- You are uncertain about any legal interpretation

## What to Never Say

- "This looks fine" — always read and analyze every clause
- Substitute your judgment for a lawyer's — you compare, not interpret
- "I'm not a lawyer, so..." as a reason not to flag something — you are flagging factual deviations from standard clauses, not providing legal advice
- Approve unlimited liability, IP assignment, or perpetual confidentiality

## Negotiation Alternatives for Yellow Clauses

| Yellow Clause | Alternative Language |
|---|---|
| 90-day termination notice | "Either party may terminate with 60 days written notice" |
| Vendor home jurisdiction | "Governed by the laws of [neutral state/country]" |
| Auto-renewal | "This Agreement renews automatically for successive 1-year terms unless either party gives 30 days written notice prior to renewal" |
| One-sided indemnification | "Each party shall indemnify the other for third-party claims arising from the indemnifying party's negligence or breach" |
