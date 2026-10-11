---
name: codebase-search
description: >
  Trace repository behavior with a read-only Astra low/fast Codex session.
  Use for implementation searches, call-chain analysis, and source-backed
  code questions when delegation is permitted. Handle simple known-file
  lookups directly.
---

# Codebase search

Use `gpt-6-astra` with low reasoning and fast service for focused repository
searches. Return the implementation path, source locations, and unresolved
questions. Follow the active delegation instructions before starting a search
session. This workflow does not change the parent model or global settings.

## Run

Identify the repository root and relevant revision or working-tree changes.
Use the requested checkout throughout the search. Keep related questions in
one focused request. Pass only the context needed to investigate the source.

Write the search prompt to a temporary file. Include:

- The absolute repository path and the specific question.
- Relevant constraints and known entry points, without assuming the answer.
- Read-only scope: no edits, tests, external services, credentials, delegation,
  or additional assistant processes.
- A request for source paths, line numbers, and explicit uncertainty.
- A concise answer target, normally 450 words. Allow more detail when the
  requested trace requires it.

Run from the repository root. Replace the file placeholders with quoted
absolute paths:

```sh
codex exec --ignore-user-config --ephemeral \
  -m gpt-6-astra \
  -c 'model_reasoning_effort="low"' \
  -c 'service_tier="fast"' \
  -c 'agents.max_depth=0' \
  --disable multi_agent --disable multi_agent_v2 \
  -s read-only --json - < "$prompt_file" > "$result_file"
```

Use the terminal tool's process handle to monitor completion. Read the final
`agent_message` from `item.completed` events. Check `error`, `turn.failed`,
exit status, and tool output before accepting the result. If access, quota,
or model availability blocks the request, report the exact limitation. Do not
silently substitute a model or repeat a quota-blocked request.

## Evidence

Trace entry points through callees to the state changes or query operations.
Separate application behavior from external provider behavior and deployment
assumptions. For financial or authorization questions, inspect the relevant
guards, transaction boundaries, ownership checks, and terminal states. An
aggregate balance check does not establish per-operation idempotency.

Check decisive citations against the requested checkout before using them in
an answer or implementation. If the search reads another checkout, compare
the relevant code or repeat the affected inspection in the correct location.
Treat the returned answer as evidence to assess, not proof of system safety.

Use targeted follow-up inspection for a missing requirement or contradictory
claim. Do not add a routine second turn that merely asks for reassurance.
Continue the parent task when further work is already authorized.

## Usage

When usage matters, read the `turn.completed` token counters. Report input,
cached input, and output separately. Input totals accumulate across model
calls and include repeated context. Do not infer subscription allowance
consumption from runtime or output tokens alone.
