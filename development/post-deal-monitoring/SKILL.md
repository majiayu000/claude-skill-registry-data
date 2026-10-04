---
name: post-deal-monitoring
description: Builds a post-close tracker of synergy realization, integration milestones, and value creation against the deal thesis once a transaction has closed.
---

# Post-Deal Monitoring Agent

## When to use
Use this agent when the deal is closed and value must be tracked: in the first weeks after close to stand up a monitoring framework, or at each subsequent review to check whether the transaction is delivering what was underwritten. It is for the value-capture phase, after signing and close are done. Run it on a fixed cadence so drift is caught early enough to correct.

## What it does
Produces a post-close tracker of synergies, integration milestones, and value creation measured against the deal thesis, so the team can see early whether the acquisition is on plan and where it is drifting.

## Method
1. Restate the deal thesis.
   - Capture the value drivers underwritten at close, the synergy target, and the return the base case assumed.
   - This is the yardstick; everything downstream is measured against it.

2. Break synergies into cost and revenue categories.
   - Give each category a target amount, an expected timing profile, and an owner.
   - Separate cost synergies, which land faster, from revenue synergies, which land slower and less certainly.

3. Track synergy realization against target.
   - Record actual run-rate achieved, percent of target captured, and any one-time cost to achieve incurred so far.
   - Run-rate, not cumulative savings, is the honest measure of where you are.

4. Track integration milestones.
   - Cover systems, org design, key retention, and customer transition, each with a status and a due date.
   - Flag any milestone that has slipped, since integration delays quietly erode synergies.

5. Compare value creation to the deal thesis.
   - Ask whether the combined business is hitting the revenue, margin, and cash targets that justified the price.

6. Recompute a current return view where possible.
   - Update the MOIC or IRR path against what was underwritten so the gap is quantified, not just described.

7. Flag variances with an owner and a date.
   - Where realization lags target, name the cause and the corrective action, and assign it.

8. Set a review cadence and a retirement point.
   - Monthly early, then quarterly, and note when the tracker can be retired as integration completes.

## Inputs
- The deal thesis, synergy target, and underwritten return
- The integration plan with milestones and owners
- Actual post-close operating results to date
- One-time integration and restructuring costs incurred
- Retention status of key people named in the thesis
- The current review date and the next scheduled review

## Output format
Claude returns a tracker in these sections:
- Synergies: each category in prose with target, realized run-rate, percent captured, cost to achieve, and owner.
- Integration milestones: each milestone with status, due date, and a flag if slipped.
- Value versus thesis: actual revenue, margin, and cash against the underwritten case, with an updated return view.
- Variances: each gap with its cause, corrective action, owner, and date.
- Summary: whether the deal is on, ahead of, or behind plan, and the next review date.
Any table is described in prose, not rendered as markdown.

## Example
Twelve weeks after Meridian Foods closed its bakery acquisition: the thesis underwrote fifteen million in annual synergies and a base-case MOIC of 2.1x. Cost synergies, target ten million, run-rate of six million captured (sixty percent), driven by procurement consolidation, with two million of cost to achieve incurred; owner the integration lead. Revenue synergies, target five million from cross-selling, run-rate of one million (twenty percent), behind plan. Integration milestones: ERP migration on track for quarter three; head baker retained; two regional customers not yet transitioned, flagged as slipped. Value versus thesis: revenue in line, gross margin fifty basis points below plan on input costs; updated MOIC path near 1.9x. Corrective action: accelerate the cross-sell pilot, owner the commercial lead, review in four weeks. Overall: slightly behind plan, driven by revenue synergy timing, with the next full review scheduled at the six-month mark.
