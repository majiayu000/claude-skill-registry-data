---
name: define-your-icp
description: Define your ICP the way a context repo needs it, so every downstream skill runs on real fit instead of a vague category. Named tiers with explicit criteria (not "Series B SaaS"), the technographic and organizational signals that indicate fit, an explicit anti-ICP, a qualification framework with must-haves separate from red flags, and an evolution log. Feeds context/icp-definition.md. Fire on "define our ICP", "who are we for", "ICP tiers", "write our ICP", "anti-ICP", "qualification criteria", or the start of building a GTM context repo.
---

# Define Your ICP: tiers, criteria, and the anti-ICP

## What this does
Turns a fuzzy "we sell to Series B SaaS" into a real ICP definition: named tiers with explicit criteria, the signals that indicate fit, the anti-ICP you exclude on purpose, and a qualification framework. This is the substance the rest of your context repo runs on. A category is not a definition, and bad context in is bad output out.

## What you'll need (reads)
What you know about your best and worst customers: who renews and expands, who churned, who you lost and why. No connectors required, do it from memory or a whiteboard. A customer list or CRM export sharpens it but is not required.

## The method
1. Separate category from definition. "Series B SaaS" is a category. A definition adds the employee range and why, the technographic signals, the organizational signals (does this function even exist there?), and the exclusions.
2. Name the tiers. Tier 1 buys fast, expands, and references. Tier 2 fits but is slower or smaller. Tier 3 works but is not the focus. Give each explicit, checkable criteria.
3. Write the anti-ICP. The segments you exclude on purpose, and why. This saves more rep time than the ICP itself.
4. Build the qualification framework. Must-haves (no deal without them) kept separate from red flags (proceed with caution). Not one blended list.
5. Start the evolution log. Date the definition. Every time a filter tightens or a segment gets cut, record what changed and why. Six months of that log is worth more than the current definition.

## Failure points
- Naming a category and calling it a definition.
- One blended qualification list instead of must-haves vs red flags.
- No anti-ICP, so reps chase everything.
- No evolution log, so you never learn why the ICP changed.

## The receipt (writes)
[your tier definitions with explicit criteria, the anti-ICP, the must-have vs red-flag framework, and the first evolution-log entry. This becomes context/icp-definition.md]

Example (illustrative):
- Tier 1: Series B to D B2B SaaS, 50 to 500 reps, a RevOps leader in seat, on Salesforce plus an outreach tool. Trigger: a new VP of Sales in the last 90 days.
- Anti-ICP: seed stage, no RevOps function, founder-led sales only.
- Must-have: a dedicated RevOps owner. Red flag: no CRM of record.
- Evolution log, 2026-07-26: tightened Tier 1 from over 25 reps to over 50 after three sub-50 deals stalled on no owner.

## Example chat
Here is the skill running on a real fuzzy ICP, start to finish.

**You:** Define our ICP for real. We keep saying "Series B SaaS" but reps chase everything.

**Claude:** Turned the category into a definition.
```
Tier 1: Series B to D B2B SaaS, 50-500 reps, a RevOps leader in seat,
on Salesforce plus an outreach tool. Trigger: new VP of Sales in last 90 days.
Anti-ICP: seed stage, no RevOps function, founder-led sales only.
Must-have: a dedicated RevOps owner. Red flag: no CRM of record.
```
The gap this closes: "Series B SaaS" alone does not tell a rep whether to chase a company with no RevOps owner. The anti-ICP does.

**You:** Log why we're tightening it. We used to take anything over 25 reps.

**Claude:** Added the evolution-log entry.
```
Evolution log, 2026-07-26: tightened Tier 1 from over 25 reps to over 50
after three sub-50 deals stalled on no owner.
```
One sharpener: connect a CRM export so the tier criteria get checked against your actual renewed and expanded accounts instead of memory.

## Go further
The read is step one. Here is where an operator takes it once the manual version proves out.

- **Score every account against it automatically.** Feed the tier definitions into a composite-scoring workflow that runs against Salesforce nightly, so fit is not a one-time judgment call.
- **Catch drift as the market shifts.** Schedule a Claude task quarterly to compare closed-won and churned accounts against the current tiers and flag when the anti-ICP needs updating.
- **Push it downstream automatically.** Wire the ICP definition into Clay or an enrichment tool so new leads get scored against your real tiers the moment they hit the CRM.

Hand the ICP to Positioning so your message speaks to exactly who you just defined. Built GTM. Receipts only.

## Next move
Hand the ICP to Positioning so your message speaks to exactly who you just defined. Built GTM. Receipts only.
