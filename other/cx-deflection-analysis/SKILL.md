---
name: cx-deflection-analysis
description: Use to measure whether a support bot, AI agent, or self-service channel actually reduces contact volume, and to audit a vendor's containment or deflection number. Trigger for "what's our real deflection rate", "is the bot working", "our containment rate is 70% but tickets haven't dropped", automation ROI, self-service savings, AI agent resolution rate, or designing a holdout test for a support bot.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Measuring real deflection

Almost every automation dashboard reports containment as:

```
containment = sessions with no human handoff / total bot sessions
```

That number is usually 60–80%, and it is usually wrong in a specific,
predictable direction: **it counts every way a customer can leave without being
helped as a success.**

The tell is a team with a 70% containment rate and flat human ticket volume. Both
numbers are real. The metric is measuring the wrong thing.

## The four ways the naive number misleads

**Silent abandonment.** The customer gives up mid-flow and closes the tab. No
handoff occurred, so the session is counted as contained. This is the single
largest contributor, and it is invisible without a resolution signal.

**Return contacts.** The bot "resolves", the customer comes back tomorrow with the
same problem and reaches a human. The bot session is still counted as contained,
and the human ticket is counted separately as normal volume. The same issue is now
in both the numerator of your success metric and your cost base.

**Channel switching.** The bot fails in chat, so the customer phones. Chat
containment is unaffected; voice volume rises. Deflection is reported while total
cost goes up. Any containment measured within a single channel is structurally
blind to this.

**Denominator inflation.** Putting a bot widget on a page that previously had no
contact route manufactures sessions that were never going to be tickets — someone
who would have searched Google now asks the bot. Every one of those is a
"contained" session and a pure denominator gift. This is why containment can rise
while ticket volume is unchanged.

## The four buckets

Classify every bot session into exactly one bucket. This is the analysis.

| Bucket | Definition |
| --- | --- |
| **handoff** | Escalated to a human inside the session |
| **leaked** | No handoff, but the customer reached a human within the window, on any channel |
| **abandoned** | No handoff, no return, and no resolution signal |
| **contained** | No handoff, no return, and a resolution signal |

```
naive containment = (leaked + abandoned + contained) / total
true  containment =                       contained  / total
overstatement     = (leaked + abandoned)  / total
```

The overstatement figure is the deliverable. It is usually between 15 and 40
percentage points, and it is the difference between "the bot handles 72% of
contacts" and "the bot resolves 41%".

Precise definitions, edge cases, and SQL if you are computing this in a
warehouse: [references/metric-definitions.md](references/metric-definitions.md).

## Data you need

One file with **both bot sessions and human contacts**, so returns on other
channels are visible. A bot-only export cannot measure leakage and will just
reproduce the vendor's number.

| Field | Required | Why |
| --- | --- | --- |
| `id` | yes | Unique contact id |
| `customer_id` | yes | Stable across channels — this is what makes leakage visible |
| `started_at` | yes | ISO 8601 |
| `ended_at` | no | Distinguishes the handoff from a later return |
| `handled_by` | yes | `bot` or `human` |
| `channel` | no | Shows where leaked customers went |
| `handed_off` | bot rows | In-session escalation |
| `intent` | no | Enables same-intent return matching |
| `resolved` | no | Splits contained from abandoned |
| `csat` | no | Compares satisfaction across buckets |

**`customer_id` must be stable across channels.** If chat identifies people by
session cookie and voice by phone number, cross-channel leakage is undetectable
and every result is an upper bound on containment. Fix the join before trusting
the output, or state the limitation prominently.

**`resolved` is the field most teams lack.** Without it, contained and abandoned
cannot be separated and the script reports those sessions as `unknown` rather than
guessing. Usable proxies, in rough order of quality: an explicit "did this solve
it?" prompt, the customer confirming in the final turn, a completed transactional
action (refund issued, address changed), or reaching a designated terminal node in
the flow. **Do not use "the session ended without a handoff"** — that is the naive
metric wearing a disguise.

## Usage

```bash
node scripts/deflection-report.mjs contacts.jsonl --window-days 7
```

**Arguments**

- `--window-days <n>` — return window. Default 7. See below.
- `--strict-intent` — count a return as leakage only when intent labels match.
- `--min-sessions <n>` — suppress per-intent rows below n sessions. Default 30.
- `--json` — JSON only on stdout.

The report goes to stderr as text and stdout as JSON, so both work:

```bash
node scripts/deflection-report.mjs contacts.jsonl > report.json
```

**Report both bounds.** Intent matching is imperfect, so run it twice:

```bash
node scripts/deflection-report.mjs contacts.jsonl --strict-intent   # lower bound on leakage
node scripts/deflection-report.mjs contacts.jsonl                   # upper bound on leakage
```

Without `--strict-intent`, any human contact in the window counts as a return,
which over-counts leakage by catching unrelated new issues. With it, only matching
intents count, which under-counts because labels are noisy. True leakage is
between them. A single point estimate here is false precision.

**Choosing the window.** 7 days is a reasonable default. Justify it from your own
data rather than convention: plot the distribution of gaps between a bot session
and the customer's next human contact. There is normally a clear elbow — most
genuine returns cluster within 48 hours. A window past that elbow starts absorbing
unrelated contacts; a shorter one misses returns on slow-moving issues like
billing disputes.

## What containment still cannot tell you

Even a correct containment rate does not establish that automation reduced
volume. Contained sessions include ones that would never have been tickets, and
that fraction is unobservable in historical data.

**Only a holdout answers the volume question.** Randomly route a small share of
eligible traffic straight to humans, then compare *total human contacts per unique
customer per period* between arms. That comparison prices the bot; containment
only describes it. Design, sizing, and the weaker
pre/post alternative: [references/holdout-design.md](references/holdout-design.md).

## Cost, honestly

The standard savings claim is `deflected contacts × fully loaded cost per
contact`. It overstates, usually by a lot, because fully loaded cost includes
fixed overhead that does not leave when volume falls.

- Use **marginal** cost per contact — the cost that actually disappears with one
  fewer contact. For in-house teams that is close to zero until a headcount or
  shift change; for BPO contracts it is the per-contact rate, but only outside
  any minimum volume commitment.
- **Savings are realised when capacity changes**, not when the metric moves. Until
  someone reduces headcount, cuts overtime, or renegotiates a commitment, the
  saving is capacity freed, not money saved. Say which one you are reporting.
- Count the costs the bot adds: platform fees, per-resolution pricing, LLM usage,
  content maintenance, and the engineering time to keep flows current.
- Leaked contacts cost **more** than a direct contact — the customer has already
  spent effort, arrives more frustrated, and the human starts cold.

## Present results to the user

1. **Lead with both numbers and the gap.** "Naive containment 72%, true
   containment 41%, overstatement 31 points." Do not bury this.
2. **Break down where the 31 points went** — leaked vs abandoned. They have
   different fixes. Leakage is a resolution-quality problem; abandonment is
   usually a flow or escalation-access problem.
3. **Show leak destination channels.** Chat-to-voice leakage is the finding most
   likely to change a decision, because it means cost moved rather than fell.
4. **Report both intent-matching bounds**, and never a single point estimate.
5. **Break down by intent.** Containment is never uniform. The useful output is
   which intents genuinely automate and which are being pushed through a flow
   that does not work — that is the roadmap.
6. **Compare CSAT across buckets.** Contained sessions scoring well below
   handed-off ones means containment is being bought with customer experience.
7. **State the caveats the script emits.** They name exactly which conclusions the
   data does not support. Do not drop them from the summary.
8. **Separate description from causation.** If there is no holdout, say the
   analysis cannot show the bot reduced volume, and propose one.

Never report a containment rate without stating whether abandonment was
separable. If `resolved` was missing, the headline is a floor and must be labelled
as one.
