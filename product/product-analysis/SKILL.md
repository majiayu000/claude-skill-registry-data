---
name: product-analysis
description: Use when analyzing a product's performance or deciding what to build. Covers metric selection, funnel and retention analysis, distinguishing signal from noise, and prioritizing on evidence.
metadata:
  category: business
  version: 1.0.0
  tags: [product, metrics, retention, funnel, prioritization]
---

# Product Analysis

## Purpose

Understand how a product is actually used and decide what to do about it. The failure mode is a dashboard full of numbers that go up, none of which are connected to whether the product is working.

## When to Use

- Deciding what to build next.
- A metric moved and nobody knows why.
- Assessing whether a feature worked.
- Setting up product analytics.

## Capabilities

- Metric selection: the one that matters versus the ones that flatter.
- Funnel analysis and drop-off diagnosis.
- Retention and cohort analysis.
- Feature-adoption measurement.
- Prioritization on evidence.

## Inputs

- Usage data, at the event level.
- What the product is meant to do for the user.
- The decision this analysis informs.

## Outputs

- The metric that actually reflects value, and where it stands.
- The specific point of failure in the funnel, or the specific cohort that churns.
- A prioritized recommendation.

## Workflow

1. **Choose the metric that reflects value received** — Not signups, not page views, not "engagement". What is the action that means the user got what they came for? That is the metric.
2. **Look at retention before acquisition** — A product with a leaking bucket does not need more water. If week-4 retention is 8%, acquisition spend is being poured into a hole.
3. **Segment before concluding** — An aggregate number hides everything. A flat retention curve can be two cohorts: one that retains at 60% and one at 2%. Those require completely different responses.
4. **Find the drop-off, then find out why** — The funnel tells you *where* users leave. It never tells you *why*. That requires session recordings, support tickets, or asking them.
5. **Distinguish a movement from noise** — A 6% week-on-week change on a small base is noise. Before declaring a trend, check whether the change exceeds the normal variance.
6. **Recommend something specific** — With the expected impact and how you will know if it worked.

## Best Practices

- Vanity metrics go up regardless of whether the product works. Total registered users, cumulative page views, and total revenue since launch can only increase. If a metric cannot go down, it cannot tell you anything.
- Retention is the product metric. Everything else — acquisition, activation, revenue — is downstream of whether people come back.
- A cohort retention curve that flattens has found product-market fit for that cohort. One that goes to zero has not, regardless of how good the early numbers look.
- The aggregate hides the answer. Always segment: by acquisition channel, by cohort, by use case, by company size.
- A funnel identifies where users leave. It cannot tell you why, and guessing at the why is how teams ship the wrong fix.
- Before acting on a change, check whether it is larger than the week-to-week noise. Most "the metric moved" investigations are investigations of noise.

## Examples

**Segmentation revealing the actual product:**

```text
Aggregate week-4 retention: 22%. Flat for six months. Universally described in
the company as "our retention problem".

Segmented by the first action taken in the first session:

  Created a project + invited a teammate (11% of signups) : 71% retained at wk 4
  Created a project alone                (34% of signups) : 24%
  Browsed, created nothing               (55% of signups) : 3%

There is no retention problem. There is an activation problem, and a specific one:
users who invite a teammate in the first session retain at 71%, which is an
excellent number for this category.

The aggregate of 22% is a weighted average of one product that works extremely
well and one that does not exist — because 55% of signups never create anything.

What this changes:
  - The roadmap item "improve retention with weekly digest emails" is targeting
    the wrong thing. It emails people who never activated.
  - The correct target is the 55% who create nothing, and the specific question
    is why they leave without acting. That is a session-recording and
    user-interview question, not a data question.
  - The second target is moving single-user projects toward invites, which the
    data suggests triples retention.

Neither of these was visible in the aggregate.
```

**Checking that a movement is real before acting on it:**

```python
def is_signal(series: pd.Series, window: int = 12) -> Signal:
    """Most 'the metric moved!' investigations are investigations of noise."""
    recent = series.iloc[-1]
    baseline = series.iloc[-window - 1 : -1]

    mean, std = baseline.mean(), baseline.std()
    z = (recent - mean) / std if std > 0 else 0

    return Signal(
        value=recent,
        baseline_mean=mean,
        z_score=z,
        # Within 2 standard deviations of the trailing mean is normal variation.
        verdict=(
            "signal" if abs(z) > 2 else
            "noise — this is within normal week-to-week variance"
        ),
    )

# Signups fell 9% this week. Panic in the standup.
#   trailing 12-week std: 7.4%
#   z-score: -1.2
#   Verdict: noise. This week is not unusual. Do not investigate; do not
#   change anything. It will "recover" next week and someone will take credit.
```

## Notes

- The segmentation example is the most common shape of real product analysis: the aggregate says there is a problem with X, and the segments reveal the problem is entirely elsewhere. Segmenting first is almost always the highest-value move.
- A flattening retention curve is the clearest evidence of product-market fit available, and it is visible in a cohort chart long before it is visible in revenue.
- Before investigating why a metric moved, establish that it moved. A large fraction of analytics work is the careful investigation of random variation.
