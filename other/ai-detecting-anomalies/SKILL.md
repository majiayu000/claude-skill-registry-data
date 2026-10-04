---
name: ai-detecting-anomalies
description: Detect fraud, unusual behavior, and anomalies in events or transactions using AI. Use when detecting fraud, flagging suspicious transactions, anomaly detection in logs, spotting unusual user behavior, abuse detection, identifying outliers in data, suspicious activity monitoring, fraud scoring, unusual pattern detection, flagging account takeover attempts, detecting bot traffic, abnormal usage patterns, security event triage, risk scoring with AI.
---

# Build an AI Anomaly Detector

Build an AI anomaly detector with DSPy - define what normal looks like, score events for severity, route by risk level, and explain findings to human reviewers.

## Step 1: Understand the detection task

Ask the user:
1. **What events are you analyzing?** (transactions, logins, API calls, server logs, user actions, etc.)
2. **What does "normal" look like?** (Do you have historical baselines? Average values? Known-good patterns?)
3. **What counts as suspicious?** (Frequency spikes, unusual amounts, geographic outliers, time-of-day mismatches, etc.)
4. **What action fires on detection, and how strict is your false-positive tolerance?** (Actions: alert, block, escalate, log for review. Tolerance: low = only flag high-confidence anomalies; high = cast a wide net and filter later.)

The answers determine severity thresholds, routing logic, and how much baseline context to include.

### When NOT to use AI anomaly detection

- **High-volume numeric time series** — millions of events/second with simple numeric signals (CPU, latency, request rate). Use statistical methods instead - z-score, EWMA, isolation forest, or Prometheus alerting rules.
- **Simple threshold rules** — "flag any transaction over $10,000" does not need an LM. Write a rule.
- **Real-time sub-10ms requirements** — LM calls add latency. Use rule-based pre-filters and only invoke the LM on candidates.
- **When you have millions of events per second** — LM calls cost money. Pre-filter with cheap heuristics, then use AI only on flagged candidates.

## Step 2: Build baseline construction

Summarize historical "normal" behavior into a compact string the LM can reason against. A good baseline summary describes typical patterns, ranges, and context.

```python
import dspy

lm = dspy.LM("openai/gpt-4o-mini")  # or "anthropic/claude-sonnet-4-5-20250929", etc.
dspy.configure(lm=lm)

class SummarizeBaseline(dspy.Signature):
    """Summarize the normal behavior pattern from historical event data.
    Produce a concise description of what typical events look like - include
    typical values, frequencies, time patterns, and common attributes."""
    historical_events: str = dspy.InputField(
        desc="Sample of recent normal events, formatted as JSON or CSV"
    )
    baseline_summary: str = dspy.OutputField(
        desc="Concise description of normal behavior - typical ranges, patterns, and context"
    )

baseline_summarizer = dspy.ChainOfThought(SummarizeBaseline)
```

For many use cases, the baseline summary can be constructed once per period (daily, hourly) and cached rather than recomputed per event.

## Step 3: Build the anomaly scorer

The core signature takes an event and the baseline summary, and outputs a severity level with a specific explanation.

```python
from typing import Literal

SEVERITY_LEVELS = ["normal", "low", "medium", "high", "critical"]

class ScoreAnomaly(dspy.Signature):
    """Analyze an event against the normal baseline and determine if it is anomalous.
    Consider all dimensions - amount, timing, location, frequency, sequence, and context.
    Severity reflects both how unusual the event is AND the potential impact if malicious."""
    event: str = dspy.InputField(
        desc="The event to analyze, as a JSON object or structured text"
    )
    baseline_summary: str = dspy.InputField(
        desc="Description of normal behavior for this type of event"
    )
    severity: Literal[tuple(SEVERITY_LEVELS)] = dspy.OutputField(
        desc="Anomaly severity - normal (expected), low (minor deviation), "
             "medium (notable deviation), high (strong anomaly signal), "
             "critical (likely fraud or attack, needs immediate action)"
    )
    explanation: str = dspy.OutputField(
        desc="Specific explanation citing concrete details - what exactly is unusual, "
             "how it deviates from the baseline, and what the risk is. "
             "Not vague ('looks suspicious') but specific ('transaction amount $4,800 "
             "is 12x the users 30-day average of $400, combined with a new device "
             "and 3am local time')."
    )
    anomaly_score: float = dspy.OutputField(
        desc="Confidence score from 0.0 (clearly normal) to 1.0 (clearly anomalous)"
    )

anomaly_scorer = dspy.ChainOfThought(ScoreAnomaly)
```

## Step 4: Full detection pipeline module

Combine baseline construction and anomaly scoring into a single reusable module.

```python
class AnomalyDetector(dspy.Module):
    def __init__(self):
        self.baseline_summarizer = dspy.ChainOfThought(SummarizeBaseline)
        self.scorer = dspy.ChainOfThought(ScoreAnomaly)
        self._cached_baseline = None

    def set_baseline(self, historical_events: str):
        """Pre-compute the baseline summary from historical data."""
        result = self.baseline_summarizer(historical_events=historical_events)
        self._cached_baseline = result.baseline_summary
        return self._cached_baseline

    def forward(self, event: str, baseline_summary: str = None):
        baseline = baseline_summary or self._cached_baseline
        if not baseline:
            raise ValueError("No baseline set. Call set_baseline() first or pass baseline_summary.")
        return self.scorer(event=event, baseline_summary=baseline)

detector = AnomalyDetector()

# Set baseline once from recent history
detector.set_baseline("""
Recent 30-day transactions:
- Average amount: $412, std dev: $180, max: $1,200
- Typical locations: New York, Chicago, LA
- Typical hours: 9am-9pm local time
- Devices: 1-2 known devices per user
- Frequency: 3-8 transactions/week per user
""")

result = detector(event='{"amount": 4800, "location": "Lagos", "hour": 3, "device": "unknown"}')
print(f"Severity: {result.severity}")
print(f"Score: {result.anomaly_score:.2f}")
print(f"Explanation: {result.explanation}")
```

## Step 5: Severity scoring with confidence-based routing

Route events automatically based on severity, and escalate only when confidence is high enough.

```python
def route_anomaly(result) -> dict:
    """Route a scored anomaly to the appropriate action."""
    routing = {
        "normal":   {"action": "dismiss",  "notify": False, "block": False},
        "low":      {"action": "log",      "notify": False, "block": False},
        "medium":   {"action": "queue",    "notify": True,  "block": False},
        "high":     {"action": "alert",    "notify": True,  "block": False},
        "critical": {"action": "escalate", "notify": True,  "block": True},
    }
    route = routing[result.severity]

    # Downgrade routing if confidence is low
    if result.anomaly_score < 0.6 and result.severity in ("high", "critical"):
        route = routing["medium"]  # reduce to queue for human review
        route["confidence_downgraded"] = True

    return {**route, "severity": result.severity, "score": result.anomaly_score}
```

### Severity to action mapping

| Severity | Score range | Default action | Blocks transaction |
|----------|-------------|----------------|--------------------|
| normal   | 0.0 - 0.2   | Dismiss silently | No |
| low      | 0.2 - 0.4   | Log for review | No |
| medium   | 0.4 - 0.6   | Queue for analyst | No |
| high     | 0.6 - 0.8   | Alert on-call | No |
| critical | 0.8 - 1.0   | Escalate + block | Yes |

Adjust these thresholds based on your false-positive tolerance.

## Step 6: Explanation generation for human reviewers

Explanations are only useful if they are specific. Force the LM to cite concrete numbers and deviations by adding a dedicated explanation signature for high-severity events.

```python
class ExplainAnomaly(dspy.Signature):
    """Generate a reviewer-ready explanation of why this event is anomalous.
    Write for a human analyst who needs to decide quickly. Cite specific numbers,
    list each anomalous dimension separately, and state the risk clearly."""
    event: str = dspy.InputField(desc="The flagged event")
    baseline_summary: str = dspy.InputField(desc="Normal behavior baseline")
    severity: str = dspy.InputField(desc="Assigned severity level")
    reviewer_explanation: str = dspy.OutputField(
        desc="Bullet-point explanation for human reviewer: what deviates, by how much, "
             "and what action is recommended. Must cite specific values from the event."
    )

explainer = dspy.ChainOfThought(ExplainAnomaly)

# Only invoke for high/critical — saves cost
if result.severity in ("high", "critical"):
    detail = explainer(
        event=event,
        baseline_summary=baseline,
        severity=result.severity,
    )
    print(detail.reviewer_explanation)
```

## Step 7: Alert routing by confidence

Batch multiple events together (same user, same time window) before scoring to give the LM session-level context.

```python
import json

class ScoreSession(dspy.Signature):
    """Analyze a sequence of events from the same user session for anomalies.
    Consider the pattern across events, not just individual events in isolation.
    Rapid-fire actions, escalating amounts, or device switches mid-session
    are signals invisible when events are scored individually."""
    session_events: str = dspy.InputField(
        desc="JSON array of events from the same user/session, in chronological order"
    )
    baseline_summary: str = dspy.InputField(desc="Normal behavior baseline for this user")
    severity: Literal[tuple(SEVERITY_LEVELS)] = dspy.OutputField()
    explanation: str = dspy.OutputField(
        desc="What pattern across the session is anomalous, not just individual events"
    )
    anomaly_score: float = dspy.OutputField()

session_scorer = dspy.ChainOfThought(ScoreSession)

def score_user_window(events: list[dict], baseline: str, window_minutes: int = 15):
    """Group events into time windows and score as sessions."""
    # Sort by timestamp, group into windows
    events_json = json.dumps(events, indent=2)
    return session_scorer(session_events=events_json, baseline_summary=baseline)
```

## Step 8: Evaluate and optimize

```python
from dspy.evaluate import Evaluate

# Build a labeled dataset - events with known ground truth
# label: 0 = normal, 1 = anomalous
labeled_events = [
    dspy.Example(
        event='{"amount": 4800, "location": "Lagos", "hour": 3, "device": "unknown"}',
        baseline_summary="Avg $400, NY/Chicago, 9am-9pm, known devices",
        severity="critical",
    ).with_inputs("event", "baseline_summary"),
    dspy.Example(
        event='{"amount": 380, "location": "New York", "hour": 14, "device": "iPhone-known"}',
        baseline_summary="Avg $400, NY/Chicago, 9am-9pm, known devices",
        severity="normal",
    ).with_inputs("event", "baseline_summary"),
    # ... more examples
]

trainset = labeled_events[:int(len(labeled_events) * 0.8)]
devset = labeled_events[int(len(labeled_events) * 0.8):]

def anomaly_metric(example, prediction, trace=None):
    """Measure exact severity match, or partial credit for adjacent severities."""
    if prediction.severity == example.severity:
        return 1.0
    # Adjacent severity is a partial match (e.g., predicted high vs actual critical)
    order = {s: i for i, s in enumerate(SEVERITY_LEVELS)}
    distance = abs(order[prediction.severity] - order[example.severity])
    return max(0.0, 1.0 - distance * 0.3)

evaluator = Evaluate(
    devset=devset,
    metric=anomaly_metric,
    num_threads=4,
    display_progress=True,
    display_table=5,
)
score = evaluator(anomaly_scorer)
print(f"Baseline accuracy: {score:.1f}%")
```

### Optimize with BootstrapFewShot

```python
optimizer = dspy.BootstrapFewShot(
    metric=anomaly_metric,
    max_bootstrapped_demos=4,
)
optimized_detector = optimizer.compile(anomaly_scorer, trainset=trainset)

# Re-evaluate
score = evaluator(optimized_detector)
print(f"Optimized accuracy: {score:.1f}%")
# Typical result: ~65% exact severity match baseline → ~82% after BootstrapFewShot with 4 demos

# Save
optimized_detector.save("anomaly_scorer.json")
```

### False positive rate metric

```python
def false_positive_rate(examples, predictions):
    """Compute FPR - normal events flagged as anomalous."""
    normals = [(e, p) for e, p in zip(examples, predictions) if e.severity == "normal"]
    if not normals:
        return 0.0
    flagged = sum(1 for _, p in normals if p.severity != "normal")
    return flagged / len(normals)
```

## Key patterns

| Pattern | When to use |
|---------|-------------|
| Single event + baseline | Simple fraud scoring, log triage |
| Session window scoring | Account takeover, multi-step attacks |
| Two-stage (pre-filter + LM) | High-volume streams - rule-based pre-filter, LM on candidates |
| Cached baseline | Baselines are stable - build once per period, reuse |
| Explanation-on-demand | Cost savings - only generate detailed explanations for high/critical |

## Gotchas

- **Claude flags every unusual event as anomalous without baseline context** — always provide a `baseline_summary` in the signature. Without it, the model has no reference point and defaults to flagging anything non-trivial.
- **Claude outputs binary anomaly/not-anomaly instead of severity levels** — use `Literal` with five graduated severity levels (`normal`, `low`, `medium`, `high`, `critical`) so downstream routing can take proportional action.
- **Claude uses `dspy.Assert`/`dspy.Suggest` for severity validation** — use `dspy.Refine` with a reward function that checks severity is one of the valid values and the explanation cites specific numbers.
- **Claude generates vague explanations** such as "this looks suspicious" or "unusual activity detected" — add an explicit `desc` on the `explanation` field requiring concrete deviations, specific values, and a risk statement.
- **Claude processes events independently and misses session-level patterns** — batch related events (same user, same time window) into a session before scoring. Account takeover and credential stuffing are only visible at the session level.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- Need fraud scores instead of severity categories? See `/ai-scoring`
- Measure and improve detection accuracy - see `/ai-improving-accuracy`
- Generate labeled training data for anomalies - see `/ai-generating-data`
- Add reasoning before severity classification - see `/dspy-chain-of-thought`
- Iterative refinement with feedback to fix wrong severity outputs - see `/dspy-refine`
- Sample N severity predictions and pick the best one - see `/dspy-best-of-n`
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For worked examples (transaction fraud, user behavior, log anomalies), see [examples.md](examples.md)
- For DSPy API reference (constructor signatures, parameter tables, BestOfN/Refine/Evaluate), see [reference.md](reference.md)
