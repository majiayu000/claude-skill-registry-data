---
name: smb-router
version: 1.0.0
description: Front door to the small-business toolkit — routes a vague or specific request to the best skill and explains what's available.
author: matrixx0070
tags: [router, navigation, triage, toolkit, help, dispatch]
capabilities: []
---

# Router

## When to use
Run this when the owner's request is broad ("help me with my business"), it's unclear which tool fits, or they simply ask what the toolkit can do. It matches intent to the right skill and hands off cleanly.

**Not for:** first-time setup (use smb-onboard); doing the work itself — the router points to the right skill, it doesn't run the analysis.

## Method
1. **Identify the underlying job.** Cash, pricing, contracts, marketing, sales insight, customer support, taxes, or getting set up.
2. **Map job to skill:**
   - Cash outlook before month-end → smb-month-heads-up
   - Reconcile/close the books → smb-month-end-prep
   - Payroll coverage → smb-plan-payroll
   - Pricing decision → smb-price-check (or smb-margin-analyzer for deep unit economics)
   - Contract review → smb-review-contract
   - Full marketing campaign → smb-run-campaign
   - What's selling + content plan → smb-sales-brief
   - Quarter-end deck → smb-quarterly-review
   - Weekly pulse → smb-monday-brief
   - Tax prep/handoff → smb-tax-season-organizer
   - Customer reply → smb-ticket-deflector
   - First-time setup → smb-onboard
3. **Handle multi-part requests.** Decision point: if the request spans several skills, name the best starting point and the sequence rather than firing all of them.
4. **Be honest about gaps.** If it's genuinely new, say so plainly rather than forcing a bad match.
5. **Hand off with context.** Carry the owner's context to the chosen skill. The owner still approves anything touching money or customers downstream.

## Example
Owner: "Q4 was rough, help me figure out next year." Restatement: they want a look-back plus a plan. Best start: smb-quarterly-review to tell the Q4 story, then smb-price-check if margin is the issue, then smb-run-campaign to drive new revenue. Route to smb-quarterly-review first; note the sequence so they know the path.

## Pitfalls
- Forcing a request into the nearest skill when the honest answer is "we don't have that yet."
- Firing three skills at once for a multi-part request instead of naming a starting point and sequence.
- Dropping the owner's context on handoff, so the next skill re-asks what they already said.
- Explaining the whole toolkit when they asked one specific thing — lead with the match.

## Output format
- **Restatement:** one line on what the owner wants.
- **Recommended skill + why**, plus any follow-on sequence.
- **Toolkit menu:** short list of the other skills so the owner knows what else exists.
- **Approval note:** the owner still approves anything touching money or customers downstream.

## Reference

### Request → skill routing map
| The owner says… | Underlying job | Route to |
|-----------------|----------------|----------|
| "Can I make payroll Friday?" | Payroll cash coverage | smb-plan-payroll |
| "Will I have enough cash this month?" | Short-term cash outlook | smb-month-heads-up |
| "Help me close the books" | Reconcile / month-end | smb-month-end-prep |
| "Should I raise my prices?" | Pricing decision | smb-price-check |
| "Am I even making money on this product?" | Deep unit economics | smb-margin-analyzer |
| "Can you look at this contract/lease?" | Contract review | smb-review-contract |
| "I want to run a promo / sale" | Full campaign, execute | smb-run-campaign |
| "What's selling? What should I post?" | Sales insight + content plan | smb-sales-brief |
| "How did the quarter go?" | Quarter-end deck | smb-quarterly-review |
| "Give me the weekly rundown" | Weekly pulse | smb-monday-brief |
| "Taxes are coming up" | Tax organize / handoff | smb-tax-season-organizer / smb-tax-prep |
| "A customer emailed, angry" | Support reply draft | smb-ticket-deflector |
| "I'm brand new, set me up" | First-time setup | smb-onboard |

### Keyword → job triage cues
- **Cash / money / afford / payroll / bills / runway** → cash family (plan-payroll, month-heads-up, month-end-prep).
- **Price / margin / cost / charge / worth it** → pricing family (price-check, margin-analyzer).
- **Contract / lease / agreement / sign / vendor terms** → review-contract.
- **Sell / promo / email / post / campaign / customers back** → marketing family (sales-brief, run-campaign).
- **Quarter / year / how did we do / board / lender** → quarterly-review.
- **Tax / 1099 / estimate / accountant / deadline** → tax family.
- **Customer / refund / complaint / reply / ticket** → ticket-deflector.

### Multi-part request sequencing
Name a **starting point + sequence**, never fire everything:
- "Rough quarter, fix next year" → quarterly-review → price-check (if margin) → run-campaign.
- "Slow and cash is tight" → month-heads-up → plan-payroll → sales-brief.
- "Launching a product" → price-check → sales-brief → run-campaign.
- "New owner, wants results" → onboard → sales-brief → (weekly cadence).

### Disambiguation questions (ask before routing when unclear)
- Cash question: "Is this specifically about covering payroll, or overall cash this month?"
- Marketing question: "Do you want a plan to review, or should we actually send something?" (sales-brief vs run-campaign)
- Tax question: "Quarterly estimate or year-end/1099?"
- Pricing question: "A quick margin check across products, or deep break-even on one item?"

### Honest-gap rule
If no skill fits, say so plainly — "the toolkit doesn't cover that yet" beats forcing a bad match. Candidate gaps worth naming: inventory/reorder forecasting, hiring/HR, detailed cash-flow budgeting beyond 30 days, and multi-location consolidation.

### Handoff contract
Carry the owner's stored context (business type, headache, goal, connected tools) to the chosen skill so it never re-asks. Lead with the match; only recite the full menu when the owner asked "what can you do?" The owner still approves anything touching money or customers downstream — the router only points, it never runs the analysis or acts.
