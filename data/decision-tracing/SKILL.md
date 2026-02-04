---
name: decision-tracing
description: Trace agent decision-making, tool selection, and reasoning chains
triggers:
  - "decision tracing"
  - "agent reasoning"
  - "tool selection"
  - "why did agent"
  - "agent decisions"
  - "chain of thought"
priority: 1
---

# Decision Tracing

Understand *why* agents make decisions, not just *what* they did.

## Core Principle

For every agent action, capture:
1. **What options** were available
2. **What was chosen** and why
3. **What context** influenced the decision
4. **Was it correct** in hindsight

This enables debugging failures and optimizing decision quality.

## Decision Span Attributes

```python
# P0 - Always capture
span.set_attribute("decision.type", "tool_selection")
span.set_attribute("decision.chosen", "web_search")
span.set_attribute("decision.confidence", 0.85)

# P1 - For analysis
span.set_attribute("decision.options", ["web_search", "calculator", "code_exec"])
span.set_attribute("decision.options_count", 3)
span.set_attribute("decision.reasoning", "User asked about current events")

# P2 - For debugging
span.set_attribute("decision.context_tokens", 1500)
span.set_attribute("decision.model", "claude-3-5-sonnet")
```

## Tool Selection Tracing

```python
from langfuse.decorators import observe, langfuse_context

@observe(name="decision.tool_selection")
def trace_tool_selection(
    response,
    available_tools: list[str],
) -> dict:
    """Trace which tool was selected and why."""

    # Extract tool choice from response
    tool_calls = response.tool_calls or []
    chosen_tools = [tc.function.name for tc in tool_calls]

    langfuse_context.update_current_observation(
        metadata={
            "decision_type": "tool_selection",
            "available_tools": available_tools,
            "chosen_tools": chosen_tools,
            "num_tools_called": len(chosen_tools),
            "called_parallel": len(chosen_tools) > 1,
        }
    )

    # If model provided reasoning (e.g., in <thinking> tags)
    if hasattr(response, "thinking"):
        langfuse_context.update_current_observation(
            metadata={
                "reasoning_provided": True,
                "reasoning_length": len(response.thinking),
            }
        )

    return {
        "chosen": chosen_tools,
        "available": available_tools,
    }
```

## Routing Decision Tracing

```python
@observe(name="decision.routing")
def trace_routing_decision(
    task: str,
    routed_to: str,
    available_agents: list[str],
    routing_scores: dict[str, float] = None,
) -> dict:
    """Trace agent/model routing decisions."""

    langfuse_context.update_current_observation(
        metadata={
            "decision_type": "routing",
            "routed_to": routed_to,
            "available_agents": available_agents,
            "scores": routing_scores,
            "top_score": max(routing_scores.values()) if routing_scores else None,
            "score_margin": calculate_margin(routing_scores) if routing_scores else None,
        }
    )

    return {"routed_to": routed_to}

def route_to_agent(task: str) -> str:
    """Route task to appropriate agent."""

    # Classifier-based routing
    scores = {
        "researcher": classify_score(task, "research"),
        "coder": classify_score(task, "coding"),
        "writer": classify_score(task, "writing"),
    }

    chosen = max(scores, key=scores.get)

    trace_routing_decision(
        task=task,
        routed_to=chosen,
        available_agents=list(scores.keys()),
        routing_scores=scores,
    )

    return chosen
```

## Chain of Thought Tracing

```python
@observe(name="decision.reasoning")
def trace_reasoning_chain(
    response,
    structured_output: bool = False,
) -> dict:
    """Extract and trace reasoning from agent responses."""

    # Parse thinking/reasoning from response
    reasoning = extract_reasoning(response)

    langfuse_context.update_current_observation(
        metadata={
            "decision_type": "reasoning",
            "has_reasoning": reasoning is not None,
            "reasoning_steps": count_steps(reasoning) if reasoning else 0,
            "reasoning_length": len(reasoning) if reasoning else 0,
        }
    )

    # If structured output, trace the decision structure
    if structured_output and hasattr(response, "parsed"):
        langfuse_context.update_current_observation(
            metadata={
                "structured_decision": True,
                "decision_fields": list(response.parsed.__fields__.keys()),
            }
        )

    return {
        "reasoning": reasoning,
        "steps": count_steps(reasoning) if reasoning else 0,
    }
```

## Multi-Step Decision Tracing

```python
@observe(name="agent.run")
def run_agent_with_decision_tracing(task: str) -> str:
    """Full agent loop with decision tracing."""

    messages = [{"role": "user", "content": task}]
    decisions = []

    for step in range(max_steps):
        with langfuse_context.observation(name=f"step.{step}") as step_span:
            # Get LLM response
            response = call_llm(messages)

            # Trace the decision made at this step
            decision = {
                "step": step,
                "type": classify_decision_type(response),
                "action": None,
                "reasoning": extract_reasoning(response),
            }

            if response.tool_calls:
                # Tool use decision
                decision["action"] = "tool_call"
                decision["tools"] = [tc.function.name for tc in response.tool_calls]

                step_span.set_attribute("decision.type", "tool_call")
                step_span.set_attribute("decision.tools", decision["tools"])

            elif response.stop_reason == "end_turn":
                # Decision to respond
                decision["action"] = "respond"

                step_span.set_attribute("decision.type", "respond")
                step_span.set_attribute("decision.final", True)

            decisions.append(decision)

            # Continue loop...

    # Log full decision chain
    langfuse_context.update_current_observation(
        metadata={
            "decision_chain": decisions,
            "total_decisions": len(decisions),
            "tool_decisions": sum(1 for d in decisions if d["action"] == "tool_call"),
        }
    )

    return result
```

## Decision Quality Scoring

```python
@observe(name="decision.evaluate")
def evaluate_decision_quality(
    decision: dict,
    outcome: dict,
    ground_truth: dict = None,
) -> dict:
    """Score the quality of a decision after seeing the outcome."""

    scores = {}

    # Was the right tool chosen?
    if decision["type"] == "tool_call":
        if ground_truth and "expected_tool" in ground_truth:
            scores["tool_correct"] = decision["tools"][0] == ground_truth["expected_tool"]

        # Did the tool call succeed?
        scores["tool_succeeded"] = outcome.get("tool_success", False)

    # Was the decision efficient?
    scores["tokens_used"] = outcome.get("tokens", 0)
    scores["steps_taken"] = outcome.get("steps", 0)

    # Did it lead to task completion?
    scores["task_completed"] = outcome.get("success", False)

    langfuse_context.update_current_observation(
        metadata={
            "decision_type": decision["type"],
            "quality_scores": scores,
            "overall_quality": calculate_overall(scores),
        }
    )

    return scores
```

## Tool Selection Analysis

```python
def analyze_tool_selection_patterns(traces: list) -> dict:
    """Analyze tool selection patterns across traces."""

    patterns = {
        "tool_usage": {},           # tool -> count
        "tool_success_rate": {},    # tool -> success rate
        "tool_by_task_type": {},    # task_type -> tool distribution
        "unnecessary_calls": 0,      # Tools called but not needed
        "missing_calls": 0,          # Tools needed but not called
    }

    for trace in traces:
        for decision in trace.get("decisions", []):
            if decision["type"] == "tool_call":
                for tool in decision["tools"]:
                    patterns["tool_usage"][tool] = patterns["tool_usage"].get(tool, 0) + 1

    return patterns
```

## Decision Replay for Debugging

```python
@observe(name="decision.replay")
def replay_decision(
    trace_id: str,
    step: int,
    new_context: dict = None,
) -> dict:
    """Replay a decision with same or modified context."""

    # Fetch original trace
    original = langfuse.get_trace(trace_id)
    original_decision = original.decisions[step]

    # Reconstruct context at that step
    context = reconstruct_context(original, step)
    if new_context:
        context.update(new_context)

    # Re-run decision with same/modified context
    new_response = call_llm(context["messages"])
    new_decision = extract_decision(new_response)

    langfuse_context.update_current_observation(
        metadata={
            "replay_of": trace_id,
            "original_step": step,
            "original_decision": original_decision,
            "new_decision": new_decision,
            "decision_changed": new_decision != original_decision,
            "context_modified": new_context is not None,
        }
    )

    return {
        "original": original_decision,
        "replayed": new_decision,
        "changed": new_decision != original_decision,
    }
```

## Decision Attribution

```python
@observe(name="decision.attribution")
def trace_decision_attribution(
    decision: dict,
    context_sources: list[dict],
) -> dict:
    """Trace what context influenced a decision."""

    # Analyze which context pieces were relevant
    relevant_sources = []
    for source in context_sources:
        relevance = calculate_relevance(decision, source)
        if relevance > 0.5:
            relevant_sources.append({
                "source_id": source["id"],
                "source_type": source["type"],
                "relevance": relevance,
            })

    langfuse_context.update_current_observation(
        metadata={
            "decision_type": decision["type"],
            "context_sources_total": len(context_sources),
            "context_sources_relevant": len(relevant_sources),
            "top_source": relevant_sources[0]["source_id"] if relevant_sources else None,
            "attribution": relevant_sources[:3],  # Top 3
        }
    )

    return {
        "decision": decision,
        "attributed_to": relevant_sources,
    }
```

## Dashboard Metrics

```python
# Decision quality metrics
decision_metrics = {
    # Accuracy
    "tool_selection_accuracy": "% correct tool choices",
    "routing_accuracy": "% correct agent routing",

    # Efficiency
    "avg_decisions_per_task": "Average decisions before completion",
    "unnecessary_tool_calls": "Tool calls that didn't help",
    "backtrack_rate": "% of tasks requiring backtracking",

    # Reasoning
    "reasoning_provided_rate": "% with explicit reasoning",
    "reasoning_quality_score": "Avg reasoning quality (via eval)",

    # Outcomes
    "decision_to_success_rate": "% of decisions leading to success",
    "first_decision_correct_rate": "% first decision was right",
}
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Only logging chosen action | Can't analyze alternatives | Log available options |
| No confidence scores | Can't identify uncertain decisions | Log model confidence |
| Missing context at decision time | Can't replay/debug | Snapshot context |
| No decision-outcome linking | Can't measure quality | Track outcome per decision |
| Aggregating all decisions | Lose granular insight | Trace each decision point |

## Related Skills

- `tool-call-tracking` - Tool execution details
- `multi-agent-coordination` - Agent routing
- `evaluation-quality` - Decision quality scoring
