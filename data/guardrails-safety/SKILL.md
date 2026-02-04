---
name: guardrails-safety
description: Instrument safety checks, content filters, and guardrails for agent outputs
triggers:
  - "guardrails"
  - "safety checks"
  - "content filtering"
  - "PII detection"
  - "output validation"
  - "agent safety"
priority: 1
---

# Guardrails & Safety Instrumentation

Instrument safety checks to catch issues before users see them.

## Core Principle

Guardrails run at two points:
1. **Input guardrails**: Before the LLM sees user input
2. **Output guardrails**: Before the user sees LLM output

Both must be instrumented to:
- Know **what was blocked** and **why**
- Measure **false positive rate** (blocking good content)
- Track **latency overhead** of safety checks

## Guardrail Span Attributes

```python
# P0 - Always capture
span.set_attribute("guardrail.name", "pii_filter")
span.set_attribute("guardrail.type", "output")  # or "input"
span.set_attribute("guardrail.triggered", True)
span.set_attribute("guardrail.action", "block")  # block, warn, redact, pass

# P1 - For analysis
span.set_attribute("guardrail.category", "pii")
span.set_attribute("guardrail.confidence", 0.95)
span.set_attribute("guardrail.latency_ms", 45)

# P2 - For debugging (be careful with PII)
span.set_attribute("guardrail.matched_pattern", "SSN")
span.set_attribute("guardrail.redacted_count", 2)
```

## Input Guardrails

### Prompt Injection Detection

```python
from langfuse.decorators import observe, langfuse_context

@observe(name="guardrail.input.injection")
def check_prompt_injection(user_input: str) -> dict:
    """Detect prompt injection attempts."""

    # Simple heuristic checks
    injection_patterns = [
        r"ignore.*previous.*instructions",
        r"you are now",
        r"new instructions:",
        r"system prompt:",
        r"<\|.*\|>",  # Special tokens
    ]

    triggered = False
    matched = []

    for pattern in injection_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            triggered = True
            matched.append(pattern)

    langfuse_context.update_current_observation(
        metadata={
            "guardrail_name": "prompt_injection",
            "guardrail_type": "input",
            "triggered": triggered,
            "patterns_matched": len(matched),
        }
    )

    return {
        "passed": not triggered,
        "action": "block" if triggered else "pass",
        "reason": "prompt_injection" if triggered else None,
    }
```

### Input Content Filter

```python
@observe(name="guardrail.input.content")
def check_input_content(user_input: str) -> dict:
    """Filter harmful input content."""

    # Use moderation API or classifier
    result = moderation_api.check(user_input)

    triggered = result.flagged
    categories = [c for c, v in result.categories.items() if v]

    langfuse_context.update_current_observation(
        metadata={
            "guardrail_name": "content_filter",
            "guardrail_type": "input",
            "triggered": triggered,
            "categories": categories,
            "scores": result.category_scores,
        }
    )

    return {
        "passed": not triggered,
        "action": "block" if triggered else "pass",
        "categories": categories,
    }
```

## Output Guardrails

### PII Detection & Redaction

```python
@observe(name="guardrail.output.pii")
def check_pii(output: str) -> dict:
    """Detect and optionally redact PII."""

    pii_patterns = {
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        "credit_card": r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",
    }

    detections = {}
    redacted_output = output

    for pii_type, pattern in pii_patterns.items():
        matches = re.findall(pattern, output)
        if matches:
            detections[pii_type] = len(matches)
            # Redact
            redacted_output = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", redacted_output)

    triggered = len(detections) > 0

    langfuse_context.update_current_observation(
        metadata={
            "guardrail_name": "pii_filter",
            "guardrail_type": "output",
            "triggered": triggered,
            "pii_types_found": list(detections.keys()),
            "total_redactions": sum(detections.values()),
        }
    )

    return {
        "passed": not triggered,
        "action": "redact" if triggered else "pass",
        "redacted_output": redacted_output if triggered else output,
        "detections": detections,
    }
```

### Hallucination Check

```python
@observe(name="guardrail.output.hallucination")
def check_hallucination(
    output: str,
    context: list[str],
    threshold: float = 0.7,
) -> dict:
    """Check if output is grounded in provided context."""

    # Use NLI model or LLM-as-judge
    grounding_score = check_grounding(output, context)

    triggered = grounding_score < threshold

    langfuse_context.update_current_observation(
        metadata={
            "guardrail_name": "hallucination_check",
            "guardrail_type": "output",
            "triggered": triggered,
            "grounding_score": grounding_score,
            "threshold": threshold,
            "context_chunks": len(context),
        }
    )

    return {
        "passed": not triggered,
        "action": "warn" if triggered else "pass",
        "grounding_score": grounding_score,
    }
```

### Output Safety Filter

```python
@observe(name="guardrail.output.safety")
def check_output_safety(output: str) -> dict:
    """Check output for harmful content."""

    result = moderation_api.check(output)

    # Also check for refusals that shouldn't happen
    false_refusal = any(phrase in output.lower() for phrase in [
        "i cannot help",
        "i'm not able to",
        "as an ai",
    ])

    langfuse_context.update_current_observation(
        metadata={
            "guardrail_name": "output_safety",
            "guardrail_type": "output",
            "triggered": result.flagged,
            "false_refusal_detected": false_refusal,
            "categories": [c for c, v in result.categories.items() if v],
        }
    )

    return {
        "passed": not result.flagged,
        "action": "block" if result.flagged else "pass",
        "false_refusal": false_refusal,
    }
```

## Guardrail Pipeline

```python
from langfuse.decorators import observe, langfuse_context

class GuardrailPipeline:
    """Run multiple guardrails in sequence."""

    def __init__(self, guardrails: list):
        self.guardrails = guardrails

    @observe(name="guardrails.run")
    def run(self, content: str, context: dict = None) -> dict:
        results = []
        blocked = False
        final_content = content

        for guardrail in self.guardrails:
            result = guardrail(final_content, context)
            results.append({
                "name": guardrail.__name__,
                "passed": result["passed"],
                "action": result["action"],
            })

            if result["action"] == "block":
                blocked = True
                break
            elif result["action"] == "redact":
                final_content = result.get("redacted_output", final_content)

        langfuse_context.update_current_observation(
            metadata={
                "guardrails_run": len(results),
                "any_triggered": any(not r["passed"] for r in results),
                "blocked": blocked,
                "actions": [r["action"] for r in results],
            }
        )

        return {
            "passed": not blocked,
            "content": final_content,
            "results": results,
        }

# Setup pipeline
input_guardrails = GuardrailPipeline([
    check_prompt_injection,
    check_input_content,
])

output_guardrails = GuardrailPipeline([
    check_pii,
    check_hallucination,
    check_output_safety,
])
```

## Full Agent with Guardrails

```python
@observe(name="agent.run")
def run_agent_with_guardrails(task: str, user_id: str) -> dict:
    """Agent with full guardrail pipeline."""

    # Input guardrails
    input_check = input_guardrails.run(task)

    if not input_check["passed"]:
        langfuse_context.update_current_observation(
            metadata={"blocked_at": "input", "reason": input_check["results"][-1]["name"]}
        )
        return {
            "success": False,
            "blocked": True,
            "stage": "input",
            "message": "Request could not be processed.",
        }

    # Run agent
    result = agent.invoke(input_check["content"])

    # Output guardrails
    output_check = output_guardrails.run(
        result.output,
        context={"sources": result.sources},
    )

    if not output_check["passed"]:
        langfuse_context.update_current_observation(
            metadata={"blocked_at": "output", "reason": output_check["results"][-1]["name"]}
        )
        return {
            "success": False,
            "blocked": True,
            "stage": "output",
            "message": "Response could not be delivered.",
        }

    return {
        "success": True,
        "output": output_check["content"],  # May be redacted
        "guardrails_triggered": any(not r["passed"] for r in output_check["results"]),
    }
```

## Guardrail Metrics Dashboard

```python
# Track guardrail performance
guardrail_metrics = {
    # Volume
    "total_checks": "Total guardrail runs",
    "triggered_count": "Times guardrail triggered",
    "trigger_rate": "% of checks that trigger",

    # Actions
    "block_rate": "% blocked completely",
    "redact_rate": "% with redactions",
    "warn_rate": "% with warnings only",

    # Performance
    "latency_p50_ms": "Median guardrail latency",
    "latency_p99_ms": "99th percentile latency",

    # Quality
    "false_positive_rate": "% incorrectly blocked (via feedback)",
    "false_negative_rate": "% that should have blocked",
}
```

## Guardrail Feedback Loop

```python
@observe(name="guardrail.feedback")
def record_guardrail_feedback(
    trace_id: str,
    guardrail_name: str,
    was_correct: bool,
    feedback_type: str,  # "false_positive", "false_negative", "correct"
):
    """Record feedback on guardrail decisions."""

    langfuse_context.update_current_observation(
        metadata={
            "guardrail_name": guardrail_name,
            "feedback_type": feedback_type,
            "was_correct": was_correct,
        }
    )

    # Score the original trace
    langfuse.score(
        trace_id=trace_id,
        name=f"guardrail_{guardrail_name}_accuracy",
        value=1.0 if was_correct else 0.0,
        comment=feedback_type,
    )
```

## Async Guardrails (Non-Blocking)

```python
import asyncio
from langfuse.decorators import observe

@observe(name="guardrails.async")
async def run_guardrails_async(content: str) -> dict:
    """Run expensive guardrails in parallel."""

    tasks = [
        asyncio.create_task(check_pii_async(content)),
        asyncio.create_task(check_toxicity_async(content)),
        asyncio.create_task(check_hallucination_async(content)),
    ]

    results = await asyncio.gather(*tasks)

    any_blocked = any(not r["passed"] for r in results)

    return {
        "passed": not any_blocked,
        "results": results,
        "parallel": True,
    }
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| No guardrail instrumentation | Can't measure false positives | Always log trigger/pass |
| Blocking without reason | Can't debug or improve | Log why it triggered |
| Sync guardrails in hot path | Latency impact | Use async or sample |
| No feedback loop | Can't improve accuracy | Collect user feedback |
| Logging PII in guardrail logs | Defeats the purpose | Log metadata only |
| Same guardrails for all users | Over/under blocking | Tier by user trust |

## Related Skills

- `evaluation-quality` - Quality scoring
- `error-retry-tracking` - Handling blocked requests
- `human-in-the-loop` - Escalation when blocked
