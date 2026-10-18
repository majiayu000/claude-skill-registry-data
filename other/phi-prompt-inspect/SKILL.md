---
name: phi-prompt-inspect
description: Inspect what a past run actually received—its instructions, task, tools, and tool results—using query_traces. Use to explain behavior or investigate stale, missing, or repetitive context.
---

Use `query_traces(sql, start, end)` with a narrow ISO 8601 time window and a
LIMIT. The tool caps output at 6,000 characters. Inspect one field in slices;
requesting an entire conversation or all attributes will truncate it.

Find the trace behind the behavior using `self-traces` if its identity is
unknown. Polling does not imply an agent run occurred. A trace may contain
Phi and several supporting agents; identify the model request you intend to
inspect rather than assuming the first span belongs to Phi.

For a known trace, list model requests:

```sql
SELECT start_timestamp, span_id, span_name,
       attributes->>'gen_ai.usage.input_tokens' AS input_tokens
FROM records
WHERE trace_id = '<trace_id>' AND span_name LIKE 'chat %'
ORDER BY start_timestamp LIMIT 30
```

For the chosen span, measure the logged fields before reading them:

```sql
SELECT length(attributes->>'gen_ai.system_instructions') AS instruction_chars,
       length(attributes->>'gen_ai.input.messages') AS input_chars,
       length(attributes->>'gen_ai.tool.definitions') AS tool_chars
FROM records WHERE span_id = '<span_id>' LIMIT 1
```

Read a bounded slice of one field; advance the offset only if needed:

```sql
SELECT substring(attributes->>'gen_ai.system_instructions', 1, 3500) AS excerpt
FROM records WHERE span_id = '<span_id>' LIMIT 1
```

Use the same pattern for `gen_ai.input.messages` (task and preceding turns)
and `gen_ai.tool.definitions` (exposed names, descriptions, schemas). Offsets
start at 1. The text is serialized JSON; a slice can split a JSON value.
Compare the first request with a later request when investigating tool-result
growth. A listed tool was available; only a tool-call span proves it was called.

These fields were verified against September 2026 model-request spans. Older
agent spans may use `pydantic_ai.all_messages`; inspect the actual shape rather
than assuming fixed system/user array positions. Null fields mean absent
telemetry, not absent instructions. Scrubbed values and truncated output limit
what you can conclude. A trace summary is not proof a claimed write succeeded.

Report the trace/span, relevant text, and the inference separately. Provider
input totals include cached subsets; do not add cache reads/writes again.

`/diagnostic` is a fresh scheduled-context preview. It omits the entry-point
task, notification-specific material, and exposed tool schemas; it is useful
for comparison but cannot reconstruct a past run. `docs/system-prompt.md`
maps blocks to their producers. Inspect a suspicious producer or tool contract
through `own-source` rather than turning a trace inference into a new rule.
