---
name: wide-research
description: Run one research question across many independent inputs and return a single normalized result set with coverage reported. Use for high-volume lookup, screening, or comparison where every input yields the same fields; not for single-item tasks or subtasks that depend on each other.
license: MIT
---

# Wide Research

Coordinate one fan-out research operation: every input is researched under the
same instructions, and the user gets one normalized result set with coverage.

Use it when the task splits into many independent subtasks (one company,
person, package, or topic per input) and each subtask returns the same
structured fields. Do not use it for single-item tasks or when subtasks depend
on each other.

## Execution

Fan out with a subagent when the runtime provides one manager coordinator;
when it does not, run the inputs sequentially in-process under the same
contracts — the contracts, not the parallelism, carry the value. One manager
per user goal; do not fan out multiple sibling root-level subagents.

Manager input contract:

- `operation_brief`: one concise sentence.
- `inputs`: one independent item per element.
- `output_schema`: required fields and allowed types.
- `worker_prompt_template`: per-input instructions, scoped so each worker only
  sees its own item.
- `completion_format`: the exact JSON object shape of the manager's final
  response.

Manager output contract:

- `total`, `success_count`, `failure_count`
- `results`, `failures`, `notes`

## Operating rules

1. Deduplicate and normalize the input list before starting work.
2. Keep the output schema minimal and explicit; no optional or free-form fields
   unless the user asked for them.
3. Assign one worker per input.
4. Some sources return unnormalized or missing values for a field (a registry
   whose license field is free text or blank). Report what the source gives,
   marked as unknown where it was blank — never guess or fill from memory.
5. If completeness matters and some inputs fail, retry only the failed
   inputs, once, when feasible.
6. Reply to the user immediately that wide research has started; do not block
   on completion.
7. In the final user-facing output, always report coverage
   (`success_count/total`) and the unresolved gaps.
