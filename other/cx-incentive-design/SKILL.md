---
name: cx-incentive-design
description: Use to design support incentives that improve behaviour without destroying the metric — pairing pay with guardrails, naming gaming modes, and choosing measures that survive Goodhart pressure. Trigger for "incentive plan", "agent bonus scheme", "SPIFF design", "pay for QA score", "what metric should we bonus", CSAT incentives, or reviewing whether a comp change is driving gaming.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: playbook
---

# Incentive design for support

Attaching pay to a metric does not reward the underlying behaviour. It rewards
**optimisation of the measured proxy**. Goodhart's law is not a cautionary tale — it is
the default outcome unless the scheme is designed around it.

The common failure: pick the easiest number on the dashboard, multiply it by a bonus
pool, and act surprised when quality drops, customers get rushed off the phone, or
evaluators start seeing a narrow band of "safe" tickets. **The metric you pay on becomes
the job**, and everything not in the formula stops mattering.

## Step 1: name what you are actually trying to change

Write the behaviour in plain language before touching a spreadsheet:

- "Agents resolve the customer's issue without unnecessary repeat contact"
- "Agents maintain quality while handling a fair share of volume"

If you cannot state it without a metric name, the incentive will not track intent. Map
each behaviour to **leading indicators** (what agents control on this ticket) and
**lagging outcomes** (what you care about over a month). Pay should lean on leading
indicators you can observe fairly; lagging outcomes are guardrails, not primary targets.

## Step 2: classify metrics by incentive survivability

| Survivability | Examples | Why |
| --- | --- | --- |
| **Low** | Raw CSAT, first-response time alone, contacts per hour alone | Easy to game; confounded by mix; customer and system driven |
| **Medium** | QA score (with calibration), FCR on defined strata, adherence | Gameable but auditable with guardrails and mix control |
| **Higher** | Repeat contact on comparable work, calibrated QA on random sample, composite with caps | Harder to optimise locally without showing up elsewhere |

**No single metric survives alone.** Every primary measure needs at least one
**guardrail** — a metric that must stay within bounds or the bonus zeroes. Typical
pairs:

- Throughput primary → quality guardrail (QA floor or repeat-contact ceiling)
- Quality primary → productivity floor (minimum handled volume or occupancy band)
- CSAT primary → QA floor and complaint-rate ceiling

State the guardrail explicitly in the scheme document. "Agents should still care about
quality" is not a guardrail.

## Step 3: catalogue gaming modes before launch

For each proposed primary metric, list how a rational agent maximises pay while harming
the customer or the business. If you cannot list modes, you have not understood the
metric.

| Metric | Common gaming modes |
| --- | --- |
| QA score | Cherry-picking easy tickets; avoiding hard queues; disputing every markdown; graders softening under pressure |
| Handle time / AHT | Rushing closures; premature resolves; transferring to avoid clock |
| FCR | Marking resolved without fix; narrow definition excludes repeats |
| CSAT | Survey coaching; closing before survey; selecting channels with higher baseline |
| Adherence | Login padding; avoiding work during measured intervals |
| Contacts per hour | Skipping documentation; bulk-closing; avoiding complex work |

For each mode, decide: **detect** (reporting), **prevent** (routing or WFM rule), or
**accept** (document as known distortion). Undetected modes become culture.

## Step 4: design the scheme structure

Principles that hold up in practice:

- **Pay on what agents control on the ticket**, adjusted for mix where comparison is
  used. Unadjusted team rankings on different queues are unfair and gameable.
- **Use periods long enough to survive noise** — weekly SPIFFs on QA with n=3
  evaluations reward luck. Align payout period with sample size you can defend.
- **Cap upside on any single metric** so optimising one dimension cannot dominate.
- **Keep the formula readable.** If agents cannot explain how they got paid, they will
  not trust it and will optimise blindly.
- **Separate team and individual components deliberately.** Team bonuses help
  collaboration; individual bonuses help accountability. Mixing both without design
  produces free-riding or sabotage — pick one as primary.

**Never invent pay percentiles or industry bonus benchmarks.** If you do not have the
organisation's actual comp bands, payout history, or union/contract constraints, say so
and design the logic without fabricated "typical" percentages. Offer ranges as
hypotheses to validate with HR, not as facts.

## Step 5: governance and review

Before launch, agree:

- **Sample design** — random vs risk-based QA; who selects tickets
- **Mix adjustment method** — same as internal reporting, documented
- **Dispute route** — same seriousness as QA used for coaching
- **Review cadence** — monthly check of guardrails and gaming signals
- **Sunset clause** — schemes left running unchanged for years accumulate exploits

After launch, watch **guardrail metrics first**. If quality falls while the primary
rises, the scheme is working as designed — and that design is wrong.

## Traps

- **Paying on CSAT alone** — mix, survey bias, and small sample make this the most
  gamed metric in support.
- **Bonus on rank** — zero-sum ranking destroys collaboration and rewards queue
  selection.
- **Guardrails in prose only** — not in the payout formula.
- **Changing the formula mid-period** without pro-rating or grandfathering.
- **Using coaching QA for pay** without a separate evaluation stream or stricter
  calibration — agents will treat every evaluation as a wage dispute.
- **Fabricating "market standard" bonus percentages** to justify the plan.

## Present results to the user

1. **Stated behavioural intent** — what the scheme is trying to improve, in non-metric
   language.
2. **Primary metric(s) and guardrail(s)** — with explicit pairing and payout logic
   (structure, not invented dollar amounts unless the user supplied comp data).
3. **Gaming mode register** — per metric, with detect/prevent/accept for each.
4. **Mix and fairness controls** — how comparison groups are defined.
5. **Sample and period design** — long enough for the evaluation count to mean
   something; dispute route.
6. **Launch governance** — review cadence, signals to watch, sunset/revision trigger.
7. **Explicit gaps** — any comp bands, contract limits, or historical payout data you
   did not have and therefore did not assume.
