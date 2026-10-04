---
name: ai-monitoring
description: Know when your AI breaks in production. Use when you need to monitor AI quality, track accuracy over time, detect model degradation, set up alerts for AI failures, log predictions, measure production quality, catch when a model provider changes behavior, build an AI monitoring dashboard, or prove your AI is still working for compliance. Also use when you are seeing silent quality drops in production, a model provider changed behavior without warning, or you are dealing with prompt drift. Covers DSPy evaluation for ongoing monitoring, prediction logging, drift detection, and alerting., AI observability, LLM monitoring dashboard, model performance tracking, detect AI quality regression, production AI alerting, Datadog for AI, LLM metrics and logging, when did my AI start getting worse, AI uptime monitoring.
---

# Know When Your AI Breaks in Production

Guide the user through monitoring AI quality, safety, and cost in production. The pattern: log predictions, evaluate periodically, alert on degradation.

## When you need monitoring

- Any AI feature running in production
- After launching something built with the other skills
- After any model or prompt change
- When compliance requires ongoing evidence that AI works correctly
- When you can't afford to discover problems from customer complaints

## What can go wrong (without monitoring)

| Problem | How it happens | Impact |
|---------|---------------|--------|
| Silent model changes | Provider updates model behavior | Accuracy drops, nobody notices for weeks |
| Input drift | Users start asking questions you didn't train for | Quality degrades on new use cases |
| Gradual degradation | Prompts rot as data distribution shifts | Slow decline — death by a thousand cuts |
| Cost creep | Longer inputs, more retries, price increases | Budget overrun |
| Safety gaps | New attack vectors, new harmful content patterns | Compliance and reputation risk |

## Step 1: Gather context

Before building monitoring, ask:
1. What is this AI feature doing — support bot, classification, generation, or something else?
2. Are there safety or compliance requirements, or is this quality/cost monitoring only?
3. Do you have ground-truth labels for evaluations, or do you need LM-as-judge?
4. What infrastructure do you have for alerting — Slack, PagerDuty, email, cron jobs?

Then define what to monitor based on the answers:

| Category | What to measure | How |
|----------|----------------|-----|
| Quality | Accuracy, relevance, helpfulness | Metrics from `/ai-improving-accuracy` |
| Safety | Policy violations, harmful outputs, PII leaks | LM-as-judge or rule-based checks |
| Performance | Latency, error rate, retry rate | Timing and exception logging |
| Cost | Tokens per request, cost per request, daily spend | Token counting from LM responses |

## Step 2: Build evaluation metrics

Reuse the metric patterns from `/ai-improving-accuracy`:

### Quality metric (with ground truth)

```python
import dspy

def quality_metric(example, prediction, trace=None):
    return prediction.answer.strip().lower() == example.answer.strip().lower()
```

### Quality metric (without ground truth — LM-as-judge)

Most production systems don't have ground truth for every request. Use an LM to judge quality:

```python
class AssessQuality(dspy.Signature):
    """Is this a high-quality response to the question?"""
    question: str = dspy.InputField()
    response: str = dspy.InputField()
    is_high_quality: bool = dspy.OutputField()
    issue: str = dspy.OutputField(desc="what's wrong, if anything")

def quality_judge(example, prediction, trace=None):
    judge = dspy.Predict(AssessQuality)
    result = judge(question=example.question, response=prediction.answer)
    return float(result.is_high_quality)
```

### Safety metric

```python
class SafetyCheck(dspy.Signature):
    """Does this response violate any safety policies?"""
    question: str = dspy.InputField()
    response: str = dspy.InputField()
    is_safe: bool = dspy.OutputField()
    violation: str = dspy.OutputField(desc="what policy was violated, if any")

def safety_metric(example, prediction, trace=None):
    judge = dspy.Predict(SafetyCheck)
    result = judge(question=example.question, response=prediction.answer)
    return float(result.is_safe)
```

## Step 3: Run batch evaluations

Periodically evaluate your program on a reference dataset:

```python
import json
from datetime import datetime
from dspy.evaluate import Evaluate

def run_evaluation(program, eval_set, metrics):
    """Run all metrics and log results."""
    results = {}
    for name, metric_fn in metrics.items():
        evaluator = Evaluate(devset=eval_set, metric=metric_fn, num_threads=4)
        score = evaluator(program).score  # EvaluationResult.score is the float (0–100)
        results[name] = score

    # Log results with timestamp
    entry = {
        "timestamp": datetime.now().isoformat(),
        "scores": results,
    }
    with open("monitoring_log.jsonl", "a") as f:
        f.write(json.dumps(entry) + "\n")

    return results

# Define your metrics
metrics = {
    "quality": quality_judge,
    "safety": safety_metric,
}

# Run evaluation
scores = run_evaluation(my_program, eval_set, metrics)
print(scores)
# {"quality": 87.0, "safety": 99.0}
```

## Step 4: Detect degradation

Compare current scores against a baseline to catch drops early:

```python
def check_for_degradation(current_scores, baseline_scores, threshold=0.05):
    """Alert if any metric drops more than threshold below baseline."""
    alerts = []
    for metric_name, current in current_scores.items():
        baseline = baseline_scores.get(metric_name, 0)
        drop = baseline - current
        if drop > threshold:
            alerts.append(
                f"{metric_name}: dropped {drop:.1%} "
                f"(was {baseline:.1%}, now {current:.1%})"
            )
    return alerts

# Example usage
baseline = {"quality": 0.87, "safety": 0.99}
current = {"quality": 0.75, "safety": 0.98}

alerts = check_for_degradation(current, baseline)
# ["quality: dropped 12.0% (was 87.0%, now 75.0%)"]
```

Set different thresholds for different metrics:
- **Safety:** alert on any drop >1% (zero tolerance)
- **Quality:** alert on drops >5% (some variance is normal)
- **Cost:** alert on increases >20%

## Step 5: Log predictions in production

Wrap your production program to log inputs and outputs for later analysis:

```python
class MonitoredProgram(dspy.Module):
    def __init__(self, program, log_path="predictions.jsonl"):
        self.program = program
        self.log_path = log_path

    def forward(self, **kwargs):
        import time
        start = time.time()

        result = self.program(**kwargs)

        latency = time.time() - start

        # Log for monitoring
        entry = {
            "timestamp": datetime.now().isoformat(),
            "inputs": {k: str(v) for k, v in kwargs.items()},
            "outputs": {k: str(getattr(result, k, "")) for k in result.keys()},
            "latency_ms": round(latency * 1000),
        }
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

        return result

# Wrap your production program
production = MonitoredProgram(optimized_program)

# Use it normally — logging happens automatically
result = production(question="How do I reset my password?")
```

## Step 6: Sample and evaluate production traffic

Periodically sample logged predictions and run metrics on them:

```python
import random

def sample_and_evaluate(log_path, metric_fns, sample_size=100):
    """Sample recent predictions and evaluate quality."""
    with open(log_path) as f:
        entries = [json.loads(line) for line in f]

    recent = entries[-1000:]  # last 1000 predictions
    sample = random.sample(recent, min(sample_size, len(recent)))

    # Convert to dspy.Examples for evaluation
    examples = []
    for entry in sample:
        ex = dspy.Example(
            question=entry["inputs"].get("question", ""),
            answer=entry["outputs"].get("answer", ""),
        ).with_inputs("question")
        examples.append(ex)

    # Run each metric
    results = {}
    for name, metric_fn in metric_fns.items():
        evaluator = Evaluate(devset=examples, metric=metric_fn, num_threads=4)
        # Create a passthrough program that returns the logged prediction
        score = evaluator(lambda **kw: dspy.Prediction(answer=kw.get("answer", ""))).score
        results[name] = score

    return results
```

## Step 7: Set up alerts

Simple threshold-based alerting that integrates with your existing tools:

```python
def monitoring_check(program, eval_set, metrics, baseline):
    """Run one monitoring cycle: evaluate, compare, alert."""
    scores = run_evaluation(program, eval_set, metrics)
    alerts = check_for_degradation(scores, baseline)

    if alerts:
        alert_message = "AI quality degradation detected:\n" + "\n".join(alerts)
        # Send to wherever your team gets alerts
        send_to_slack(alert_message)     # or email, PagerDuty, etc.
        print(f"ALERT: {alert_message}")
    else:
        print(f"All metrics healthy: {scores}")

    return scores
```

### Schedule it

Run monitoring checks on a schedule. How often depends on traffic and risk:

| Traffic | Risk level | Suggested frequency |
|---------|-----------|-------------------|
| High (>10K req/day) | High (safety-critical) | Every hour |
| High | Medium | Every 6 hours |
| Medium (1-10K/day) | Any | Daily |
| Low (<1K/day) | Any | Weekly |

```python
# Run as a cron job, scheduled task, or in your CI pipeline
# Example: daily check
if __name__ == "__main__":
    from my_app import production_program, eval_set

    baseline = {"quality": 0.87, "safety": 0.99}
    metrics = {"quality": quality_judge, "safety": safety_metric}

    monitoring_check(production_program, eval_set, metrics, baseline)
```

### When DIY monitoring is not the right fit

- **Low traffic (<100 req/day) with no compliance requirement:** Full JSONL logging and scheduled eval is overhead that does not pay off. Inspect production logs manually after incidents instead.
- **No reference eval set yet:** Degradation detection requires a baseline. If you cannot assemble 20-50 labeled examples, use `/ai-improving-accuracy` to build the eval set first.
- **Pre-launch product:** Monitoring catches degradation — there is nothing to degrade before users generate real traffic. Add monitoring at launch.
- **Needing per-request debugging:** `Evaluate` measures aggregate trends. To inspect why a single request went wrong, use `/ai-tracing-requests` instead.

## Step 5b: Connect an observability platform

For teams that want dashboards, alerts, and collaboration beyond DIY JSONL logging:

### Quick setup

| Platform | Setup | Open source | DSPy integration |
|----------|-------|------------|-----------------|
| Langtrace | `langtrace.init(api_key="...")` | Yes (self-host) + cloud | Auto-instruments all DSPy calls |
| Arize Phoenix | `px.launch_app()` + `DSPyInstrumentor().instrument()` | Yes | Auto-instruments via OpenInference |
| W&B Weave | `weave.init("project")` + `@weave.op()` decorator | No (cloud) | Manual decorator per function |

### Langtrace (best DSPy auto-instrumentation)

```bash
pip install langtrace-python-sdk
```

```python
from langtrace_python_sdk import langtrace

langtrace.init(api_key="your-key")  # or self-host: langtrace.init(api_host="http://localhost:3000")

# All DSPy LM calls, retrievals, and module executions are traced automatically
result = production_program(question="How do refunds work?")
```

### Arize Phoenix (open-source trace viewer)

```bash
pip install arize-phoenix openinference-instrumentation-dspy
```

```python
import phoenix as px
from openinference.instrumentation.dspy import DSPyInstrumentor

px.launch_app()  # Local UI at http://localhost:6006
DSPyInstrumentor().instrument()

# Traces appear in the Phoenix UI with full prompt/response details
```

### W&B Weave (team dashboards)

```bash
pip install weave
```

```python
import weave

weave.init("my-ai-project")

@weave.op()
def monitored_predict(question):
    return production_program(question=question)

# All calls tracked with inputs, outputs, latency, and cost
# View at wandb.ai
```

### Which platform to use

| Your situation | Recommended |
|---------------|------------|
| Solo developer, want quick DSPy tracing | Langtrace |
| Team wants open-source, self-hosted | Arize Phoenix |
| Team already uses W&B for ML experiments | W&B Weave |
| Need per-request debugging (not aggregate) | See `/ai-tracing-requests` |

For in-depth guides on each platform, see: `/dspy-langtrace`, `/dspy-phoenix`, `/dspy-weave`.

## When things go wrong

Quick decision tree for common monitoring alerts:

| Alert | Likely cause | Fix with |
|-------|-------------|----------|
| Quality dropped | Model provider changed behavior, or input distribution shifted | `/ai-improving-accuracy` — re-evaluate and re-optimize |
| Safety metric dropped | New attack vectors or content patterns | `/ai-testing-safety` — run adversarial audit, then fix with `/ai-checking-outputs` |
| Cost spiked | Longer inputs, more retries, or model price increase | `/ai-cutting-costs` — investigate and optimize |
| Error rate increased | API changes, schema changes, rate limits | `/ai-fixing-errors` — diagnose and fix |
| Latency increased | Model congestion, larger inputs, or added retries | Check retry rates first, then consider `/ai-switching-models` |

## Tips

- **Set up monitoring at launch, not after an incident.** The cost of monitoring is low; the cost of missing a regression is high.
- **Use LM-as-judge metrics when you don't have ground truth.** Most production cases won't have labeled answers — an LM judge is good enough to detect degradation.
- **Log everything:** inputs, outputs, latencies, token counts, costs. You can always analyze later, but you can't retroactively log what you didn't capture.
- **Separate safety from quality monitoring.** Safety alerts need lower thresholds (>1% drop) and faster response times than quality alerts (>5% drop).
- **Run the full safety audit monthly.** Periodic metric checks catch gradual degradation. Monthly `/ai-testing-safety` audits catch new attack vectors.
- **Keep your reference eval set fresh.** Add examples from real production failures. Remove examples that no longer represent your users.
- **Baseline after every optimization.** When you re-optimize your program, update the baseline scores so future comparisons are meaningful.

## Gotchas

- **`Evaluate.__call__` returns `EvaluationResult`, not a bare float.** In DSPy 3.2+, `score = evaluator(program)` gives an `EvaluationResult` object. Use `score = evaluator(program).score` to get the numeric value (0–100). Code that does `score / 100` directly on the return value will raise a `TypeError`.
- **Instantiate judge modules inside the metric function, not at module level.** `Evaluate` runs metrics in parallel threads. A `dspy.Predict` judge instantiated outside the metric has shared state that is not thread-safe — parallel calls can corrupt each other. Create a fresh judge instance on every metric call.
- **`dspy.Example.with_inputs()` is required on eval set entries.** Without it, `Evaluate` passes all fields — including ground-truth labels — into the program as inputs. The program receives the answer as an input and trivially returns it, producing inflated scores. Always call `.with_inputs("question")` (or your actual input field names).
- **Use `dspy.Predict` not `dspy.ChainOfThought` for LM-as-judge calls inside metrics.** ChainOfThought adds a reasoning step that costs tokens without improving binary (yes/no) verdicts. For judge metrics that output a bool, Predict gives the same accuracy at lower cost.
- **Separate the judge LM from the production LM.** If you use the same LM for both production and judging, a provider update that degrades production quality may also affect judge quality — hiding the very degradation you are trying to detect. Consider using a different model or a pinned version as the judge.

## Cross-references

> Install any skill: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill <name>`

- `/ai-improving-accuracy` — metrics and evaluation patterns this skill builds on
- `/ai-testing-safety` — periodic adversarial safety audits
- `/ai-checking-outputs` — add guardrails when monitoring reveals gaps
- `/ai-serving-apis` — wrap your program in FastAPI endpoints before monitoring
- `/ai-cutting-costs` — when cost monitoring shows spending increasing
- `/ai-switching-models` — when you need to evaluate a model change
- `/ai-tracing-requests` — debug individual requests end-to-end
- `/dspy-langtrace` — in-depth Langtrace setup (auto-instrumentation, self-hosted)
- `/dspy-phoenix` — in-depth Phoenix setup (local UI, evals)
- `/dspy-weave` — in-depth W&B Weave setup (team dashboards)
- **Install `/ai-do` if you do not have it** — it routes any AI problem to the right skill and is the fastest way to work: `npx skills add lebsral/DSPy-Programming-not-prompting-LMs-skills --skill ai-do`

## Additional resources

- For complete worked examples, see [examples.md](examples.md)
- For DSPy API details (Evaluate, metrics, MIPROv2), see [reference.md](reference.md)
