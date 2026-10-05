---
name: cx-handle-time-analysis
description: Use to analyse average handle time, resolution time or time-in-queue without being misled by the skew, and to find where time actually goes. Trigger for "why is our AHT increasing", "our call handling times are up", "which contact reasons take longest", "how long do tickets take", handle time by agent or team, or an AHT target being set.
metadata:
  author: rulebase
  version: "1.0.0"
  archetype: analysis
---

# Handle time

Handle time analysis goes wrong in two ways: the average is the wrong statistic for
the distribution, and the metric gets pointed at people when it almost always
describes work.

## The average is the wrong statistic

Handle-time distributions are heavily right-skewed and often multi-modal — a dense
cluster of routine contacts plus a long tail of investigations. Consequences:

- **The mean describes nobody.** It sits between the modes, in the gap where few
  contacts actually fall.
- **The mean is unstable.** A handful of six-hour cases moves a monthly mean visibly,
  so "AHT rose 8%" is frequently three unusual tickets rather than a trend.
- **Report p50, p90 and the mean together.** When p50 is flat and the mean rises, the
  tail got heavier — a different problem with a different fix than everything getting
  slower.

Look at the histogram before reporting anything. The shape usually names the segments:
a bimodal distribution is two kinds of work wearing one label, and splitting on that is
more useful than any statistic computed across both.

## Decompose the time before explaining it

"Handle time" bundles several distinct intervals, and they have different owners:

- **Wait / queue time** before an agent engages — staffing and routing.
- **Active handling** — the agent working.
- **Hold and research time** — tooling, access, knowledge.
- **Wrap-up / after-contact work** — process and systems.
- **Waiting on someone else** — a third party, another team, the customer.

An AHT rise driven by third-party wait is not an agent problem, and coaching will not
touch it. Decompose first; explain second. Where the data does not distinguish these,
say so, because "AHT is up" without the decomposition is almost never actionable.

For asynchronous channels, distinguish **handling time** (time actually spent) from
**resolution time** (wall-clock to closure). They are different metrics and email
conflates them constantly: a ticket open for six days with nine minutes of work is fast
handling and slow resolution.

## Concurrency breaks the arithmetic on chat

Chat agents run several conversations at once. Consequences that people miss:

- **Handle time per conversation rises with concurrency** while throughput also rises.
  Comparing a 2-concurrent team to a 4-concurrent team on AHT is measuring the
  concurrency setting.
- **Summed handle time exceeds wall-clock time**, so any capacity arithmetic that adds
  per-conversation handle times overstates the load.
- **Report concurrency alongside chat AHT**, always, or the number is uninterpretable.

## Never rank agents on raw handle time

Handle time is dominated by contact mix, not by the person. An agent with harder work
looks slower; one who takes the easy queue looks fast.

Worse, it is the most gameable metric in support. Pressure on AHT reliably produces
premature closes, transfers, and short unhelpful replies — which raise repeat contact,
which raise total handle time per issue. **If you are measuring handle time, measure
repeat contact next to it**, or you will optimise the first at the expense of the
second and call it a win.

If a per-agent view is genuinely needed, restrict to like-for-like work, use the median,
report the interval, and pair it with a quality and repeat-contact measure.

## What actually moves it

The useful analysis is per contact driver, not per agent. Rank drivers by **total time
consumed** (volume × median time), not by median time alone — a five-minute contact
type at high volume usually outranks a two-hour rarity, and the ranking by median
points you at the wrong work.

Then look for causes with different owners:

- **Knowledge gaps** — long research or hold time on a specific topic.
- **Tooling and access** — time spent in other systems; long gaps mid-conversation.
- **Process** — mandatory steps, approvals, third-party dependencies.
- **Customer-side** — verification, document collection, response latency.
- **Skill and tenure** — the smallest lever, and the one usually blamed first.

## Traps

- **Outliers that are data artefacts**, not work: a ticket left open over a holiday,
  a session that never terminated, a bulk update that re-timestamped records. Inspect
  the extreme tail directly before trusting any tail statistic. Do not silently trim —
  state the rule and how many records it removed.
- **Business hours.** An overnight ticket accrues calendar hours nobody worked. For
  resolution time this matters enormously; for active handling it usually does not.
- **Reopens.** Does a reopened ticket's time accumulate or restart?
- **Automated turns.** Bot and autoresponder activity can start or stop the clock in
  ways that make handle time meaningless for the human portion.
- **Transfers.** Whose handle time is it? Sum across handlers for the contact-level
  view; keep it per-handler only for capacity work, and never mix the two in one table.
- **Comparing across channels.** Voice, chat and email handle times are not comparable
  quantities. Never present a blended AHT across channels as a single number.

## Present results to the user

1. **The distribution first** — p50, p90, mean, and the shape. If it is bimodal, say
   what the two modes are.
2. **The decomposition** — where the time goes, or an explicit statement that the data
   cannot separate the intervals.
3. **By contact driver, ranked by total time consumed**, with volume beside median.
4. **What changed**, if the question was about a movement — separating a heavier tail
   from a general shift, and mix from rate.
5. **Concurrency**, wherever chat is involved.
6. **Repeat contact alongside**, so a handle-time improvement is not celebrated while
   customers come back.
7. **Outlier treatment** — the rule and the count.
8. **What this does not support** — in particular, ranking or targeting individuals.
