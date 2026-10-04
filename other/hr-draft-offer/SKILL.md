---
name: hr-draft-offer
version: 1.0.0
description: Draft a clear, complete, ready-to-send offer letter with compensation, terms, and contingencies — flagging every unconfirmed figure.
author: matrixx0070
tags: [offer-letter, compensation, hiring, onboarding, terms, contingencies]
capabilities: []
---

## When to use

Reach for this when a candidate has verbally accepted or a hiring manager has approved an offer and you need a written letter ready to send. Produce a professional, accurate document that mirrors the approved requisition exactly.

**Not for:** deciding the numbers or benchmarking pay (use hr-comp-analysis), planning the new hire's ramp (use hr-onboarding), or giving binding legal advice — route jurisdiction-specific clauses to counsel.

## Method

1. **Collect inputs** — candidate name, role title, level, manager, team, start date, employment type (full-time/part-time/contract), work location/remote status, reporting line.
2. **Assemble compensation** — base salary (and pay period), sign-on bonus (with clawback window if any), target annual bonus, equity grant (type, amount, vesting, cliff), benefits summary.
3. **State conditions** — at-will language (jurisdiction-appropriate), background check, work authorization/I-9 or local equivalent, offer expiration date.
4. **Add key terms** — relocation, confidentiality/IP assignment, PTO policy, probation period if applicable. Decision point: include only terms the requisition or policy supports; do not invent.
5. **Set tone** — warm, welcoming opener; precise on every number; clean acceptance instructions (signature + date + deadline).
6. **Verify before delivery** — cross-check every figure and date against the approved req. Decision point: any value you cannot confirm gets a visible `[CONFIRM]` marker, and any legal-sensitive clause routes to counsel before sending.

Never invent numbers, dates, or legal terms. When in doubt, mark it and escalate.

## Example

Candidate Priya Shah, Product Manager (L4), start 2026-08-04, full-time, hybrid (SF). Base $165,000/yr paid semi-monthly; sign-on $15,000 (12-month clawback); target bonus 12%; 12,000 RSUs vesting 4yr with 1-yr cliff. Contingent on background check and I-9. Offer expires 2026-07-25. Placeholder left: `[CONFIRM manager name]` because the req listed "TBD — Growth PM lead." That marker plus a reviewer note ("route clawback clause to legal — CA") ships with the draft.

## Pitfalls

- Copying comp numbers from an earlier draft or memory instead of the signed-off requisition.
- Omitting the offer expiration date, leaving the offer open-ended.
- Using generic at-will boilerplate in a jurisdiction where it is unenforceable (e.g., outside the US).
- Sending before legal/finance review on equity, clawback, or relocation clauses.

## Output format

```
--- OFFER LETTER (ready to send) ---
Greeting
Position: <title>, <level> — reporting to <manager>, <team>
Start date | Employment type | Location/remote
Compensation: base, pay period, sign-on (+clawback), target bonus
Equity: type, amount, vesting, cliff
Benefits: summary
Contingencies: background check, work authorization, offer expiration
At-will / terms: confidentiality/IP, PTO, probation
Acceptance block: signature ___ date ___ deadline ___
---
Placeholder list: [CONFIRM ...] items needing sign-off
Reviewer notes: clauses to route to legal/finance
```

## Reference

### Offer-letter anatomy — required components

A complete offer letter carries every element below. Missing any of the first group creates ambiguity; missing the contingencies group creates legal exposure.

**Core terms**
- Position title, level, and department/team
- Reporting manager (name and title)
- Employment type: full-time / part-time / contract / temporary
- Work location and remote/hybrid/on-site designation
- Start date
- FLSA classification (US): exempt vs. non-exempt (drives overtime eligibility)

**Compensation**
- Base salary with pay period stated (annual + per-paycheck; for non-exempt, hourly rate)
- Sign-on bonus, if any, with amount, payment timing, and clawback/repayment window
- Target annual/variable bonus: % of base, $ target, plan basis (individual/company), proration for partial year, and whether year-1 is guaranteed
- Equity grant: type (RSU/ISO/NSO/options), quantity or $ value, vesting schedule, cliff, and a note that grants are subject to board approval and the plan documents
- Benefits summary: health/dental/vision, retirement (e.g., 401k match), PTO/leave, other perks — usually by reference to plan docs

**Contingencies (offer is conditional on)**
- Satisfactory background check / references
- Proof of work authorization + I-9 (US) or local right-to-work verification
- Any role-specific screening (drug test, credit, security clearance) where lawful
- Offer expiration date/time

**Legal terms**
- At-will statement (US, where enforceable) — this is not an employment contract for a fixed term
- Confidentiality / IP-assignment / invention-assignment agreement (usually a referenced attachment)
- Restrictive covenants (non-compete/non-solicit) — jurisdiction-sensitive; many US states restrict or ban non-competes; route to counsel
- Contingency and probation language, if applicable

**Acceptance block**
- Signature line, printed name, date
- Explicit acceptance deadline

### At-will vs. contract — jurisdiction cautions

At-will employment is a US default (except Montana) meaning either party may end the relationship any time for any lawful reason. It is **not** a global concept: most of Europe, the UK, Canada, and much of the world requires notice periods, statutory grounds, and often a formal employment contract — copying US at-will boilerplate there is unenforceable and can invalidate other terms. Always match the governing-law state/country to the employee's work location and route non-US and multi-state offers to counsel.

### Equity clause essentials

State enough that the candidate understands what they're getting, without overstating certainty:

- **Type** — RSUs (taxed at vest, no strike) vs. options (ISO/NSO, carry a strike price, taxed differently).
- **Quantity vs. value** — number of units or a target $ value; note private-company shares are illiquid and current PPS is an estimate.
- **Vesting** — standard is 4 years with a 1-year cliff, then monthly or quarterly. State it explicitly.
- **Conditions** — "subject to board approval and the terms of the equity incentive plan and your grant agreement." Never promise a grant the board hasn't approved.
- **Strike/409A** (options) — strike is set at grant per the latest 409A/FMV; do not quote a strike you can't confirm → `[CONFIRM]`.

### Sign-on and clawback

Sign-on bonuses commonly carry a repayment clause if the employee leaves within a window (typically 12 months, sometimes prorated). State the amount, when it's paid (first paycheck vs. after 30/90 days), and the exact clawback terms. Route clawback and relocation-repayment language to legal.

### The [CONFIRM] discipline

Any figure, date, name, or term you cannot verify against the **signed-off requisition or approval** gets a visible `[CONFIRM …]` marker in the draft — never a guessed value, never a number pulled from an earlier draft or memory. Maintain a placeholder list at the bottom so the approver sees exactly what still needs sign-off. Comp numbers, in particular, come only from the approved req, not from a prior candidate's letter.

### Pre-send verification checklist

- [ ] Every comp figure matches the approved requisition exactly (base, bonus %, equity, sign-on)
- [ ] Start date, manager name, level, and location match the req
- [ ] Offer expiration date present and reasonable (commonly 3–7 business days)
- [ ] Governing law matches the employee's work location; at-will language appropriate for that jurisdiction
- [ ] Equity clause has type, amount, vesting, cliff, and board-approval caveat
- [ ] Contingencies listed (background, work auth/I-9)
- [ ] IP/confidentiality attachment referenced
- [ ] All `[CONFIRM]` markers resolved or explicitly flagged to the approver
- [ ] Legal/finance review completed on equity, clawback, relocation, and any non-standard clause
- [ ] Tone: warm opener, precise numbers, clear acceptance instructions

### Common state/jurisdiction traps (US)

- **Salary-history bans** (many states/cities) — don't reference prior pay.
- **Pay-transparency laws** (e.g., CA, CO, NY, WA) — job postings and sometimes offers must include ranges.
- **Non-compete restrictions** — CA, ND, OK broadly void them; other states limit scope; route to counsel.
- **Final-pay and PTO-payout rules** vary by state — relevant to any clawback or accrual language.
- **Multi-state / remote** — the employee's physical work location usually governs, not the company HQ.

Route anything jurisdiction-specific or non-standard to counsel before sending; this skill drafts, it does not give legal advice.
