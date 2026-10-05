---
name: agent-design
description: Use when building an LLM agent that uses tools over multiple steps. Covers tool design, the agent loop, error recovery, termination, human checkpoints, and knowing when an agent is the wrong architecture.
metadata:
  category: ai
  version: 1.0.0
  tags: [agents, tools, llm, orchestration, autonomy]
---

# Agent Design

## Purpose

Build LLM agents that complete tasks reliably and fail safely. The two failure modes that define bad agents are looping forever without progress, and taking a destructive action confidently and wrongly.

## When to Use

- Building an agent that uses tools to accomplish multi-step tasks.
- An agent that loops, stalls, or takes wrong actions.
- Designing the tool surface an agent will use.
- Deciding whether an agent is warranted at all.

## Capabilities

- Tool design: granularity, naming, descriptions, and error returns.
- The agent loop: planning, acting, observing, and terminating.
- Error recovery and retry.
- Human-in-the-loop checkpoints for irreversible actions.
- Guardrails: budgets, timeouts, and permission boundaries.

## Inputs

- The task, and how it decomposes.
- The tools available, and which of them are destructive.
- The acceptable cost and latency per task.

## Outputs

- A tool surface designed for a model, not lifted from an API.
- An agent with a termination condition and a budget.
- Checkpoints before anything irreversible.

## Workflow

1. **Ask whether you need an agent** — If the steps are known in advance, write the workflow. A deterministic pipeline with one LLM call per step is cheaper, faster, more debuggable, and more reliable than an agent. Agents earn their cost only when the path genuinely cannot be known in advance.
2. **Design tools for the model** — Each tool does one thing, has a name that says what it does, and a description that says exactly when to use it and when not to. This description is the most important text in the system.
3. **Return useful errors** — A tool that fails should say what went wrong and what to try instead. `Error: 400` teaches the model nothing; `Error: 'status' must be one of [open, closed]. You passed 'active'.` lets it recover on the next step.
4. **Bound the loop** — A maximum step count, a token budget, and a wall-clock timeout. Every agent will eventually loop; the question is whether it stops.
5. **Checkpoint the irreversible** — Deleting data, sending a message, moving money, deploying. The agent proposes; a human confirms.
6. **Make it observable** — Log every step: the reasoning, the tool call, the result. An agent you cannot trace is an agent you cannot debug.

## Best Practices

- The tool description is the prompt. Most agent misbehavior is a tool whose description does not clearly say when it applies.
- Fewer, well-chosen tools beat many overlapping ones. An agent with thirty tools spends its reasoning deciding between them.
- An agent with no termination condition will loop. Detect "no progress" explicitly: the same tool call with the same arguments twice means it is stuck, not persevering.
- Do not give an agent a destructive tool without a confirmation step. Confidence is not competence, and the model has plenty of the former.
- Return structured, pruned tool results. A tool that dumps 50 KB of JSON burns the context budget the agent needs to think.
- Prefer a small, verifiable step to a large, plausible one. An agent that writes one function and runs the test is more reliable than one that writes the whole module and declares success.

## Examples

**A tool designed for a model rather than lifted from an API:**

```python
@tool
def search_orders(
    customer_email: str | None = None,
    status: Literal["open", "paid", "shipped", "cancelled"] | None = None,
    placed_after: date | None = None,
    limit: int = 20,
) -> str:
    """Search for orders. Use this to find an order when you do not know its ID.

    You must provide at least one filter. If you already have an order ID,
    use `get_order` instead — it is faster and returns full detail.

    Returns a compact list: order ID, status, total, and customer email.
    To see line items or the refund history, call `get_order` with an ID
    from these results.
    """
    if not any([customer_email, status, placed_after]):
        # An error the model can actually act on.
        return "Error: provide at least one of customer_email, status, or placed_after."

    orders = db.search(...)[:limit]
    if not orders:
        return "No orders matched. Try widening the date range or removing the status filter."

    # Compact: four fields, not the full object. The agent can fetch detail if it needs it.
    return "\n".join(
        f"{o.id} | {o.status} | {o.total_cents / 100:.2f} {o.currency} | {o.customer_email}"
        for o in orders
    )
```

**A loop that terminates, with a checkpoint before anything irreversible:**

```python
async def run(task: str, max_steps: int = 25, token_budget: int = 200_000) -> Result:
    history, tokens_used, recent_calls = [], 0, deque(maxlen=3)

    for step in range(max_steps):
        response = await model.complete(task, history, tools=TOOLS)
        tokens_used += response.usage.total

        if tokens_used > token_budget:
            return Result.halted("token budget exhausted", history)

        if response.is_final:
            return Result.done(response.text, history)

        call = response.tool_call

        # No-progress detection: the same call twice in a row means it is stuck.
        signature = (call.name, json.dumps(call.args, sort_keys=True))
        if recent_calls.count(signature) >= 2:
            return Result.halted(f"looping on {call.name} with identical arguments", history)
        recent_calls.append(signature)

        # Irreversible actions require a human. The agent proposes; it does not decide.
        if call.name in DESTRUCTIVE_TOOLS:
            approval = await request_approval(call, reason=response.reasoning)
            if not approval.granted:
                history.append(tool_result(call, f"Denied by operator: {approval.reason}"))
                continue

        result = await execute(call)
        history.append(tool_result(call, result))

    return Result.halted(f"step limit ({max_steps}) reached without completing", history)
```

## Notes

- The single most common agent failure is repeating an identical tool call because the result did not contain what it expected. Detecting a repeated call with identical arguments catches this in one extra line of code.
- An agent that can read but not write is dramatically safer and covers more use cases than most people assume. Start read-only and add write tools one at a time, each with a checkpoint.
- Cost per task is the metric that determines whether an agent is viable. Measure it early — a task that takes 40 tool calls at $0.30 each is not a product feature, it is a demo.
