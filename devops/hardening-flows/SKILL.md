---
name: hardening-flows
description: "Makes an AQVEN flow fail loudly and recover on purpose: run-time checks, join semantics, map on_item_error with a coverage guard, requires, limits, on_error. Use when a flow must hold in production, a step has no failure answer, or a run completed while an item failed."
---

## MUST

- The flow output says how many items were planned and how many were read. `degraded: true` on a node is
  invisible to the owner; a dropped item must show in the flow output.
- Input-contract errors and infrastructure errors never turn into default values or "no" answers.
- A guard reports a violation; it never repairs data silently.
- A construct that calls a model more than once for one decision (parallel readings, repeated `loop` passes, a
  second model checking the first) stays only when an experiment shows it beats a variant of equal budget, or
  when the owner asked for it.
- Compliance work such as PII masking is added only when the owner asks for it (see "Owner's rules" in
  `AGENTS.md`).

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | A table per node: possible failures (provider error, 429, refusal, truncation, invalid schema, empty or wrong input, some `map` items failing, a slow `parallel` branch; for tools an external API down or slow, a tool `wait` past its `timeout_seconds`, an approval nobody answers, an agent's tool-call loop stopped by `limits.tool_calls`; for long or split inputs a part of a document silently dropped, an empty list of pages, chunks, segments or rows), how to detect each, what to do, how a person sees it | every node has all four columns |
| 2 | Detection: `checks` in the inference with `on_fail: "retry"` (or `"fail"`, `"flag"`); built-ins `not_empty`, `unique_items`, `ids_in_allowed_set` (with `allowed_sets`); flow `requires` predicates (`families_distinct`, `family_disjoint_from_input`, `field_before`) where they fit. A retry check never rejects a declared `cannot_tell` value: the input may not show the answer | every failure in the step-1 table has a detection: a run-time check, a later guard or a flow-output field; no check rejects `cannot_tell` |
| 3 | Reaction to a call outcome in the agent: `output.on_error` (default `retry`), `output.on_refusal` and `output.on_truncated` (default `fail`), each `retry`, `fail` or `fallback`; `fallback` only with `fallback_models`. To see how a fallback model reads the real node, a project agent of that model through `run_start` `agent_overrides: {<node_id>: <agent_id>}` on a real case | no `E_OUTCOME_FALLBACK` |
| 4 | `parallel`: pick `join` from the table below; if every branch's answer is needed, `all`; with `quorum` the output carries how many branches answered (`$ok[*]`) | the output shows how many branches answered |
| 5 | `map`: `on_item_error` with `use: "skip"` or `use: "default"` only together with a coverage guard after the map (the required items) and an output field for the items not read (for example `unread`) | a missing required item fails the run; a missing optional item is visible in the flow output |
| 6 | Bad inputs: when blank pages, silent recordings or empty text occur in the inputs you opened, one option is a gate before the paid call (`code` for text length or row count, `tool` for media bytes, since only a tool reads them) with a `switch` on its verdict, weighed against the calls it saves; another is a declined state in the llm node's output (`designing-output-contracts`) | every bad-input kind seen has a detection, before the llm node or in its output |
| 7 | `limits` on the flow and the agent (`requests`, `tokens`, `usd_micros`, `seconds`, `tool_calls`); an agent's `limits.seconds` cuts a hanging call long before the 600 s of stream silence the engine allows; an agent with `tools` or `mcp_servers` gets `limits.tool_calls` (past it the call fails with `budget_exceeded`); its `approval` names the tools that write, with `assignee`, `timeout_seconds` and `on_timeout` (`fail` or `escalate`; `default` is refused with `E_HUMAN_DEFAULT_INVALID`); a tool with `wait` has a `timeout_seconds` the job can meet | limits are set; every tool that writes has an approval or a stated reason |
| 8 | A construct that calls a model more than once is measured against a variant of equal budget: a `use` factor on the container node, or a `flow` factor on a `call` slot (`designing-experiments`) | every such construct has an experiment or the owner's request behind it |
| 9 | Prove the failure path: a run where one item fails (a planted bad input, or `run_start` over a node range with `start_node`, `end_node` and `node_outputs` that plant a bad upstream output). After a series, count the not-read field across attempts in one call: `series_outputs` `{series_id, split: "dev", fields: ["/unread"]}` | the run view shows the item replaced or skipped, and the flow output has the "not read" field instead of a silent `completed` |

## `join` of a `parallel` node

| `join` | When the node closes | Danger |
|---|---|---|
| `all` | every branch succeeded; fails on the first error | one model's 429 fails the node; give its agent `fallback_models`, or on an aggregator its upstream fallbacks |
| `any` | the first finished branch, success or error | only the fastest model counts |
| `first_success` | the first success; fails when all fail | only one branch's answer counts |
| `quorum` with `min_ok` and `on_error` (`skip` or `fail`) | as soon as `min_ok` branches succeeded | a race, not a wait: with `min_ok: 2` of three, the slowest branch never takes part |

```yaml
join:
  use: "quorum"
  with:
    min_ok: 2
    on_error: "skip"
```

## Pitfalls

| What goes wrong | Do instead |
|---|---|
| `on_item_error` with `use: "skip"` drops a required item and the run still ends `completed` (a contract reader skips the page with the signatures) | a coverage guard after the map and an `unread` output field |
| An input-contract or infrastructure error turns into an answer (a timed-out invoice read comes back as "nothing due") | let contract and infrastructure errors fail; answer states belong to `designing-output-contracts` |
| A lost item shows only as `degraded: true` on a node (one ticket of a batch was never classified, the summary looks whole) | the flow output names what was not processed |
| `quorum` taken for "wait for two of three": it closes on the first answers, so the slowest branch never counts | `all` with fallbacks, or report how many answered |
| `join: all` over several providers: one provider's 429 fails the node on every case | fallbacks on each agent (`choosing-models`) |
| Compliance or safety work the owner did not ask for (PII masking added to an internal code-review flow) | follow "Owner's rules" |
| A yes/no question per item of a long checklist (40 contract clauses, 30 sound events in a recording) raised recall and false positives together, at several times the cost | measure precision and cost next to recall; evidence with each yes checked by a rule, one open question, or several readers merged are variants to compare, not the fix |
| A retry check rejected honest "cannot tell" answers (a required field the input did not show), so they counted as model failures | checks accept `cannot_tell`; a required field the input may not show is a contract bug (`designing-output-contracts`) |
| A speech-to-text tool caught its provider's timeout on a long call and returned an empty transcript, which the next step read as "the customer asked for nothing" | the tool raises and the step fails; an empty transcript, chunk or segment list is a guard violation, not an answer |
| An agent with a search tool and no `limits.tool_calls` kept calling it on a table of 5,000 rows until the run's budget ran out | `limits.tool_calls` on every agent with tools; send the model only the rows the question needs |

## Tools and commands

- `aqven` MCP `aqven_check`, `run_start` (`mode: "live"`, `agent_overrides`), `run_get_node`, `series_outputs`.
- `pytest_run` for failure scenarios when the project has `tests/`.

## References

- `references/concepts/designing-reliable-workflows.md`: what more nodes, `parallel`, a `loop` with a critic and a
  second model as judge each assume, when they fit and how to measure them. Read before step 8 and before
  offering any construct that calls a model more than once.
- `references/reference/built-in-policies.md`, `references/reference/policies.md`: every built-in `join`,
  `on_item_error`, `stop`, `select` and evaluator with its `with` parameters. Read at steps 2, 4 and 5.
- `references/concepts/what-happens-when-a-model-is-called.md`: outcomes `ok`, `error`, `refusal`,
  `truncated`, retries and their policies. Read at step 3.
- `references/engine/parallel-node.md`, `references/engine/map-node.md`: container semantics and `$ok`. Read at
  steps 4 and 5.
- `references/engine/field-constraints.md`: `maxItems`, `maxLength`, `pattern` and their run-time effect. Read
  with step 2.
- `references/reference/flows.md`, `references/reference/agents.md`: `limits`, `requires`, `output`,
  `fallback_models`, `approval`. Read at steps 3 and 7.
- `references/engine/tool-node.md`: a tool's `wait`, `timeout_seconds` and `idempotency_key`, and a tool node
  against an agent's own `tools`. Read at steps 1 and 7 for a step that calls a tool.
- `references/studio/investigate-a-run.md`: how a replaced or skipped item looks in the run view. Read at step 9.
