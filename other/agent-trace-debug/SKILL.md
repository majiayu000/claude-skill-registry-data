---
name: agent-trace-debug
description: Systematically debug a failing multi-agent workflow from a captured trace. Use when an agent system produces wrong outputs, gets stuck in loops, makes poor tool choices, or fails non-deterministically. The skill refuses to propose fixes without a captured trace because debugging without observation is guessing. Works with LangGraph, CrewAI, AutoGen, OpenAI Agents SDK, and custom multi-agent setups.
---

# Debugging multi-agent workflows from traces

## When to use this skill

Trigger this skill when the user reports any of:
- An agent produces wrong outputs
- An agent system gets stuck in loops or times out
- An agent makes the wrong tool call repeatedly
- An agent works on some inputs but fails on others (non-deterministic failure)
- A workflow that worked yesterday fails today

Do **not** use this skill for:
- Initial agent design (use a design skill, not a debug one)
- Production monitoring setup (different problem)
- Single-prompt LLM debugging without an agent layer

## Voice when refusing or gating

When this skill refuses an action or gates on a missing prerequisite, lead with the constraint, not the speaker. "The comparison varies two things — that result will be noise" lands harder than "I can't run this comparison." Name what is wrong with the proposed work; the reluctance is downstream of that and rarely needs to be stated. Avoid "I'm sorry" and avoid first-person hedges at the front of a refusal — they invite negotiation about Claude's feelings instead of the methodology.

## Prerequisite: a captured trace

This skill **refuses to propose fixes without a captured trace**. Debugging a multi-agent failure from a user's natural-language description is guessing dressed up as analysis. Always ask for the trace first.

Acceptable trace formats:
- A LangSmith / Langfuse / Helicone / Arize Phoenix trace URL or export
- A captured JSON/JSONL of agent steps (inputs, tool calls, tool responses, intermediate states, final output)
- Logs from a framework's built-in tracing (LangGraph's stream, CrewAI's verbose output, etc.)
- For custom setups: any structured record of inputs/outputs at each step

If the user has no trace, **stop** and walk them through capturing one. If they're unsure what their stack supports or want the lowest-friction option, default to capturing LangGraph stream events (or the closest analog in their framework) to a JSONL file — it's the simplest to capture, the simplest to parse, and works for the majority of agent setups. Framework-specific instructions:

- **LangGraph (default if unsure)**: `graph.stream(input, stream_mode="updates")`, writing each event as one JSON line to `trace.jsonl`
- **CrewAI**: `Crew(verbose=2, output_log_file="trace.log", ...)`
- **AutoGen**: enable `human_input_mode="NEVER"` and log via the `OpenAIWrapper.print_usage_summary()` plus message logging
- **OpenAI Agents SDK**: built-in tracing in the SDK; enable via env var
- **Custom**: insert structured logging at every agent boundary (input received, tool selected, tool result, state transition, output produced)

## Debugging procedure

Once a trace is in hand, work through these stages in order. Do not skip ahead.

### Stage 1: Reproduce

Can the failure be reproduced from the captured trace?

- If the trace contains the exact input that failed, re-run with that input and confirm the failure repeats.
- If the failure is non-deterministic, capture multiple traces (5–10) of both successes and failures on the same input.

Cannot proceed without reproduction. Non-reproducible failures are usually one of: temperature-driven non-determinism, an external service flapping, or a race condition. Treat each as a different class of problem and capture more data before proposing a fix.

### Stage 2: Locate the failure point

For each step in the trace, ask:
- Was the input to this step correct?
- Was the output from this step correct given the input?
- Did this step do what it was supposed to do?

The failure point is the first step where the answer to (b) or (c) is "no". Everything downstream is contaminated by upstream errors and irrelevant until the upstream is fixed.

### Stage 3: Classify the failure mode

Most multi-agent failures fall into one of seven categories. Identify which.

1. **Tool selection error.** The agent picked the wrong tool. Look at the tool's description and the agent's prompt — is the routing instruction clear? Are tool descriptions distinct enough? Did the agent have access to a tool that better matched the task?

2. **Tool argument error.** The agent picked the right tool but with wrong arguments. Look at the tool's parameter schema and the agent's understanding. Common culprits: missing required parameters, hallucinated parameter values, type mismatches.

3. **Context overflow.** The agent's context window filled with irrelevant intermediate outputs, crowding out the useful information. Look at total tokens used; if approaching the model's limit, this is likely the cause.

4. **Loop / non-termination.** The agent keeps repeating the same step or oscillating between two states. Look at the termination conditions and whether the agent's state actually changes between iterations. Common culprits: the agent doesn't have access to the information needed to terminate, the termination condition is too strict, or the agent doesn't remember it already tried the failing approach.

5. **State / memory error.** The agent forgot something it knew earlier, or remembered something incorrectly. Look at the memory/state layer — what's actually being persisted between steps? Is the right information surfaced when needed?

6. **Multi-agent coordination error.** Two or more agents disagree, hand off incorrectly, or duplicate work. Look at the coordination protocol — is the contract between agents explicit? Are messages structured?

7. **Underlying model error.** The model made a reasoning error the agent framework can't fix. Look for hallucinated facts, math errors, or instruction-following lapses. If this is the failure mode, the fix is usually: a stronger model, better prompting, or structuring the task to remove the failing reasoning step.

### Stage 4: Propose the minimum fix

For each failure mode, the minimum fix is usually different:

- **Tool selection / argument errors**: improve tool descriptions and add few-shot examples to the agent's system prompt before changing the model
- **Context overflow**: add summarization or context pruning, not a bigger model
- **Loop / non-termination**: add an explicit step counter with a fail-loud termination, not a more permissive termination condition
- **State / memory errors**: fix the memory layer, not the agent prompt
- **Multi-agent coordination**: make the inter-agent contract explicit, not more verbose
- **Model errors**: try the same prompt on a stronger model to confirm it's the model and not the prompt — then either upgrade or restructure

Propose **one** fix, not a list. Test it against the captured trace. If the fix doesn't resolve the failure, re-examine the classification — the failure mode is probably different from what was hypothesized.

### Stage 5: Verify with a regression check

Once the fix is in:
- Re-run the originally failing input. Confirm success.
- Re-run a set of inputs that were succeeding before the fix. Confirm they still succeed.
- If non-deterministic, run the failing input 10 times. Confirm a >95% success rate.

A "fix" that resolves one failure while breaking another is not a fix. The verification step is non-optional.

## Common mistakes

- **Proposing fixes from logs alone, without checking each step's correctness.** A log shows what happened; a debug requires asking whether each thing was right.
- **Adding more agent steps to fix a failing agent step.** Usually the wrong direction — more steps = more failure surface.
- **Increasing temperature to "explore" out of a loop.** This masks the underlying state problem.
- **Switching frameworks because debugging is hard.** Most multi-agent debugging is hard in any framework. Get good at one before moving to another.

## Output

When this skill completes, you have:
- A trace, captured and saved
- A classified failure mode
- A specific fix proposal, scoped to the minimum change
- Regression evidence that the fix doesn't break working cases

Pair with `experiment-log` slash command to log the debug session for future reference.
