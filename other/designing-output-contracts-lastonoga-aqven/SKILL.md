---
name: designing-output-contracts
description: "Designs AQVEN types and llm output schemas models can produce: required fields, refusal and unknown as states, maxItems and maxLength, tool or prompted mode. Use before editing types/ or an inference output, for nested outputs, and on OUTPUT_SCHEMA_REJECTED or MODEL_SCHEMA_MISMATCH."
---

## MUST

- Every output field is decidable from the input the model receives. What only history or the subject can tell (payment status for an invoice PDF, intent beyond the words said in a call, events off-screen in a clip) becomes another input of the step or leaves the contract.
- Every field the prompt asks about is required in the output type; where the input may not show the answer, `cannot_tell` is one of its values.
- An enum that describes the input covers what real inputs contain, not the nominal scope: `other` (or `outside_scope`) for what falls outside it, `cannot_tell` for what the input does not show.
- "Cannot read it" is its own state of the output (a declined flag with a reason), never "no" on every field.
- Downstream, a missing field reads as "unknown", never as "no". An empty intersection is "unknown", not 0.
- Output is flat by default; nest only after `models shapes --live` passed for every model that serves it.
- Every list has `maxItems`, every string `maxLength`, and the prompt states those limits in words.
- A retry to the same model gets the same `OUTPUT_SCHEMA_REJECTED`; the options are a smaller schema, `output.mode: prompted` or another model (step 3).
- 429 is not a property of the schema: the model's rate-limit lane handles it; never lower parallelism by hand.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 1 | Start from the consumer's decision. A final output gets the fewest fields, flat records, enums sized to that decision (a router needs about 8 intents, not 60) holding only values the input can show, `maxItems` on every list, `maxLength` on every string. An intermediate output that feeds another step carries the fields that separate what the next step confuses: refund against billing error needs "money already charged"; total against subtotal needs the printed label next to the amount; a meeting summary needs speaker changes; a clip needs the order of events. "Fewest fields" applies to final outputs only. Draft every enumeration as a short list and get the owner's yes before writing files; while the owner's requirements are still arriving, offer two or three options in one question. Each value's definition in the prompt comes from the same table as the enum (`building-flows` step 6) | the owner agreed the value lists; no `E_OUTPUT_UNBOUNDED` |
| 2 | Answer states: present, absent, declined (with a reason) and "not asked" are distinguishable; the prompt asks about the content ("does this contract have a termination clause") rather than "can you read this". A retry check never rejects `cannot_tell` (`hardening-flows`) | every field has a stated meaning for its absence; a refusal shows in the flow output |
| 3 | Estimate the state space: arrays of objects × `maxItems` × enum sizes × `maxLength`. A large closed enum inside a list (60 values × `maxItems` 15) can exceed a provider's constrained decoding: `OUTPUT_SCHEMA_REJECTED` with "too many states". Options, each with its cost: `output.mode: prompted` (no grammar; repairs are paid calls); a smaller type (only the values the consumer's decision needs, a lower `maxItems`); the list split across fields or calls (more calls, each blind to the others). `output.strict: false` still sends the schema and does not help. Offer the options that fit to the owner; verify the chosen one with one call on the failing case (`run_start`, `mode: "live"`, `dataset_item_id`; a copy of the agent in `prompted` mode is tried without a flow edit through `agent_overrides: {<node_id>: <agent_id>}`), then compare `schema_valid_first_try`, completeness and cost in a series | a large space goes to step 4; a rejected schema passed one call on its failing case |
| 4 | A nested or large schema: `uv run aqven models shapes <agent> --project <package> --live` for the model and each of its `fallback_models`; record the boundary in one sentence of the agent's `description` | the schema is within the boundary of every model that serves it |
| 5 | The shape depends on the input (items × questions per item): pick one of the five dynamic-shape cases; measure answers with missing fields with an "answered every asked field" check | a case is chosen; the completeness check is in the experiment |
| 6 | The output limits are written in the prompt text | otherwise it is a specification gap, not a model limit |
| 7 | Output mode: `uv run aqven models check <agent> --project <package> --live` tries every mode with `output.strict: true`; pin `output.mode`. If the probe passes but the real request gives `MODEL_SCHEMA_MISMATCH`, the options are `prompted`, a smaller schema, or another model with the owner's yes; try one on the failing case with `agent_overrides`, then compare `schema_valid_first_try` in a series | no unresolved `W_OUTPUT_MODE_RESOLVED`; `schema_valid_first_try` known |
| 8 | Pilot a new or intermediate output on about 10 varied `dev` cases before a series: `series_start` with `look` over named cases, or a smoke with `--cases 10` (`running-series`); read the pilot in one call: `series_outputs` `{series_id, split: "dev", fields: [<pointers or node id>]}` (a pointer such as `/label` into the flow output, a node id for a top-level node's output). Count the values per field: a field with one value on more than 80% of the cases carries nothing. `MODEL_SCHEMA_MISMATCH` on one field, read next to the model's raw answer, shows a missing enum value | in the pilot each field varies across the classes the next step must tell apart; no field rejected on more than one case |
| 9 | Keep working limits the same across the project; change them file by file with Edit | no regex over several files |

The CLI probes read keys from the environment and `<package>/.env`. Keys saved in Studio settings are visible only
to the project server: if your shell has no key, ask the owner to run the probe and paste the output.

## Pitfalls

| What goes wrong | Do instead |
|---|---|
| A 60-value vocabulary of ticket intents generated before the consumer's decision was known; most values could not be told apart from the message | size the enum to the decision; a short list agreed with the owner first (step 1) |
| A field the input cannot show (a caller's satisfaction from a transcript that never states it) was required, and the model guessed | another input of the step, or out of the contract |
| An enum built from the nominal scope met receipts and credit notes in an "invoices" set; the schema rejections counted as model failures | `other` and `cannot_tell` in the enum; the 10-case pilot (step 8) |
| An intermediate record too coarse to carry what the next step needed (one value per field, the distinguishing detail folded into a generic word); accuracy fell and a general negative lesson was drawn | fields from the downstream confusion pairs; a pilot that shows spread; the lesson covers that schema only |
| `output.strict: false` tried against `OUTPUT_SCHEMA_REJECTED` | one of the options of step 3 |
| A nested output failed on a small model at the first smoke | flat by default; `models shapes --live` before nesting |
| The same model retried after `OUTPUT_SCHEMA_REJECTED`; the rejection came and went because the calls reached different backends (an aggregator's upstream routing, a gateway's pool) | smaller schema; on an aggregator, pin the upstream order (`choosing-models`) |
| `tool` mode passed the small probe, then the real schema failed with `MODEL_SCHEMA_MISMATCH` on required fields | the options of step 7; compare `schema_valid_first_try`, the share of complete answers and the cost in a series |
| Missing fields read downstream as "no": a model skipped part of the asked questions and the output looked clean | required fields, "unknown" downstream, an "answered every asked field" check |
| Two empty answers scored as agreement 0.0 | keep it unknown: a nullable field (`None`) in the `code` step; a check cannot return unknown (it must return a `Verdict`, and a scored check without `score` is an error), so measure agreement only on cases where it is defined, selected with `cases.tags` |
| A refusal looked like "no" on every question in the flow output | a separate declined field with a reason |
| The prompt asked "can you read this" and got "yes" on blank pages, silent audio and off-topic images | ask for the property itself |
| Optional inputs left out of cases | write an explicit `null` |
| Parallelism lowered by hand against 429 | the lane pauses the model; see `choosing-models` |

## Tools and commands

- `aqven` MCP `aqven_check`, `prompt_preview` (the output contract the model receives).
- `aqven` MCP `run_start` (one call on a failing case, `agent_overrides` for a copy of the agent), `series_start` with
  `look` and `series_outputs` (the pilot).
- `uv run aqven models shapes <agent> --project <package> --live`, `uv run aqven models check <agent> --project <package> --live`.

## References

- `references/concepts/schema-state-space.md`: how the state space grows, how providers fail on it, aggregators included,
  a large enum in a list, the options against a rejection and their costs, `tool` against `prompted`. Read at step 3.
- `references/concepts/answer-refusal-and-unknown.md`: only what the input shows, enums that cover real inputs,
  fields for an intermediate step, required fields, refusal as a state, unknown against no, the completeness
  check. Read at steps 1 and 2.
- `references/engine/field-constraints.md`, `references/reference/fields.md`, `references/reference/types.md`:
  every constraint and type. Read at step 1.
- `references/reference/inference.md`: `out`, `checks`, `allowed_sets`. Read before editing an inference.
- `references/engine/check-shapes.md`: `models shapes` axes and output. Read at step 4.
- `references/engine/check-providers.md`: `models check`, output modes and `strict`. Read at step 7.
- `references/engine/dynamic-shape.md`, `references/concepts/five-dynamic-shape-cases.md`: shapes that depend on
  the input. Read at step 5.
