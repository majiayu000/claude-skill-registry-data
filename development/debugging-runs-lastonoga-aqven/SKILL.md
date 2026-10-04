---
name: debugging-runs
description: "Finds why an AQVEN run, node or series attempt failed or hangs: run_get_node, paged run_events, the first failing node, infra versus counted errors, the fix per code. Use when anything fails, or a series has infra errors or a stuck variant, before any fix; never restart the server."
---

## MUST

- Never start, stop, kill or restart the project server: project modules reload on the next run.
- A second engine server on the same project root breaks every series: report both processes (PID and project root) to the owner and kill nothing; never touch processes of another project.
- An `INTERNAL` from any aqven tool is an engine bug: report the tool, the time and the arguments; never investigate the machine instead.
- Prove the cause with an event from the run, not with a guess.
- Read in small pieces: `run_get_node` and `run_events` with a small `limit`, not a whole `run_get` of a long run.
- Outputs and error codes of many attempts come from `series_outputs` (or `aqven series export`) in one paged
  read, never one `run_get` per attempt, never from `.aqven/`.
- Never repeat a paid run only to see the output in another format.
- Replacing a model of the owner's set needs the owner's yes.

## Procedure

| # | Step | Exit criterion |
|---|---|---|
| 0 | No `run_id` and no error code (a vague report such as "looks cached" or "something is off"): ask once what the owner did, expected and saw; then map it to a run or a series | a run, a series or a concrete observation named |
| 1 | Get the `run_id`. A series: `series_outputs` `{series_id, outcome: "error"}` (or `"failed"`); each row carries `run_id`, `error_code`, `case` and `variant`. Or `run_list` `{series_id, view: "compact"}`. A single run: `run_list` `{flow_id, status: "failed"}`; it leaves series attempts out and counts them in `hidden_experiment_runs` | a `run_id` |
| 2 | Read in bounds: `run_get_node` of suspect nodes (`include_payloads: "truncated"` by default, `"full"` only for one node); `run_events` with `after_seq` and a small `limit` (up to 200; without `after_seq` it returns the tail) | every tool answer under about 10,000 characters |
| 3 | The first failing node upstream; for a `map`, the item (`item_index`); for a `parallel`, the branch (`branch_key`) | node and item named |
| 4 | Class: infrastructure (`provider_error` including a 429 that outlasted its retries, `timeout`, `MODEL_STREAM_STALLED`, `provider_key_missing`, `MODEL_FEATURE_UNSUPPORTED`, `INTERNAL`, broken code) or a counted failure (`MODEL_SCHEMA_MISMATCH`, `MODEL_RETRIES_EXHAUSTED`, `OUTPUT_SCHEMA_REJECTED`, a failed check, `truncated`, `refusal`). Above 5% infrastructure errors make a series `invalid` | the class named |
| 5 | Group the attempts by error code and by variant: `series_get` `{series_id, view: "summary"}` gives the top 3 failure groups per variant with one example; `series_outputs` `outcome: "error"` (then `"failed"`), counted by `error_code` × `variant`, gives all of them | counts per code and variant |
| 6 | Code → cause → fix from the table below and `references/reference/error-codes.md` | the cause proven by an event |
| 7 | Reproduce cheaply, on the failing case and variant only. After a fix in a project file: `run_start` `{flow_id, mode: "live", dataset_item_id: "<dataset_id>/<case_name>"}` on the failing case, or `series_start` with `look` over the failing `dev` cases. A failure only one agent shows: the same `run_start` with `agent_overrides: {<node_id>: <agent_id>}`, a run option for this run only, not a variant; nodes of a flow reached through `call` are not covered. A failure only a `prompt`, `use` or `flow` variant shows: a one-case smoke of that experiment (`running-series`). `run_fork` replays the original run from a node address and cannot change files, agents or input (`NOT_RUNNABLE`); `run_resume` answers a wait. Never rerun every variant to re-check one fix | one run on the failing case confirms the fix |
| 8 | What stays unexplained is reported as an anomaly, with its events | the anomaly written down |

| Code or sign | Cause | Fix |
|---|---|---|
| `truncated`, `finish_reason: length` | the output did not fit `max_tokens`; on a reasoning model the hidden reasoning used the budget (the attempt's `tokens_out` near `max_tokens` while the visible answer is short) | a reasoning model: a larger `settings.max_tokens`, or reasoning capped or switched off with the key its provider reads in `settings.provider_options` (`choosing-models`), each measured for quality; otherwise the agent's `settings.max_tokens` and output limits in the prompt |
| `OUTPUT_SCHEMA_REJECTED` | the schema is too big for the model; "too many states" is often a large enum times `maxItems` | `output.mode: prompted` or a smaller type, not `output.strict: false` (`designing-output-contracts`) |
| `MODEL_SCHEMA_MISMATCH` although the probe passed | `tool` mode does not hold the real schema | options: `prompted` (a copy of the agent tried on the failing case with `agent_overrides`), a smaller schema, or another model with the owner's yes; compare `schema_valid_first_try` in a series |
| `MODEL_NO_STRUCTURED_OUTPUT` | the output mode does not work live | `models check --live`, pin `output.mode` |
| `MODEL_FEATURE_UNSUPPORTED` | the provider refused a feature: an attachment kind (images, audio, video, documents; the message names it), tools, structured output | `choosing-models`; the owner's model changes only with a yes |
| `provider_error` with HTTP 429 | the provider, or an aggregator's upstream, limited the model; its lane paused (console line `<provider:model> rate-limited — pausing Ns, parallel 8→4` from logger `aqven.models.lanes`); a series attempt runs once more at the end | `fallback_models`, an aggregator's upstream fallbacks, `on_rate_limit`; never `rpm` |
| another call error | `output.on_error` retries by default | read the retries in the node's events |
| `CODE_NOT_FOUND` after a code edit | a reference or a generated name | `uv run aqven refs`, `uv run aqven tree`; no restart needed |
| `NOT_RUNNABLE` at a series start | a case or variant cannot run | `problems[]` names the case and the variant |
| `NOT_RUNNABLE` from `run_fork` | a fork with `overrides` or not `at: "original"` | step 7: `run_start` on the case, with `agent_overrides` or after the file fix |
| `INPUT_INVALID` with `problems[]` at `agent_overrides.<node_id>` (`AGENT_OVERRIDE_NODE_UNKNOWN`, `AGENT_OVERRIDE_NODE_AMBIGUOUS`, `AGENT_OVERRIDE_NOT_LLM`, `AGENT_UNKNOWN`) | the key is not an `llm` node of this flow, names several nodes, or the agent does not exist | the node id `run_get` shows (`<parent>__<node>`), or its file name when only one node has it; the message lists the flow's `llm` nodes and the agents |
| `aqven series` exit 5 | the CLI lost the project server after 300 s of retries | `series_get` on the series id: the series keeps running on the server |
| `INTERNAL` from an aqven MCP tool ("internal server error") | an engine bug | report the tool, the time and the arguments to the owner; use the CLI equivalent if one exists (`uv run aqven check <package>`, `uv run aqven series`) |
| `INTERNAL` on every run or series tool, or a series failed with "the series workflow was not started" | two engine servers on one project root share its state | report both to the owner with PIDs and roots; kill nothing |
| an attempt `running` without events for ten times its neighbours' median, later `MODEL_STREAM_STALLED` | the provider hangs; a silent stream is cut after 600 s, a call longer than `limits.seconds` ends in `timeout` | the agent's `limits.seconds` to cut sooner; `fallback_models` at another provider, with the owner's yes |
| `STALE_FILE` from `flow_patch` | the file changed since you hashed it | read it again and replay the intent |

## Pitfalls

| What goes wrong | Do instead |
|---|---|
| "Looks stale" sent the agent to list processes and environments while the setup was fine | ask for the concrete observation first (step 0) |
| A flag that does not exist, and a paid rerun just to get another output format | read the stored run with `run_get_node` |
| A whole `run_get` and an unpaged `run_events` of a long run flooded the context | bounded reads, step 2 |
| A node that failed in every run was explained by a guess; `run_get_node` was never called | open the node and quote its event |
| Truncation found only after the owner pointed at it | check `finish_reason` first |
| `run_list` by `flow_id` showed none of a series' runs | `series_id` or `mode: "experiment"`; `hidden_experiment_runs` counts what was left out (step 1) |
| A fix re-checked by rerunning every variant, or by a fork with another agent that returned `NOT_RUNNABLE` | `run_start` with `agent_overrides` on the failing case (step 7) |
| Studio's `Expected vs actual` panel showed `absent` because the output shape differs from the case's `expected_output`, and a passing answer was called wrong | the verdict is the attempt's `passed` and `failed_checks` in the `series_get` case row; the check's code says what it compares |
| Outputs of hundreds of runs collected by subagents making one read each, then from the engine's database | `series_outputs` (pages of up to 200 rows, `fields` to narrow) or `aqven series export`; never `.aqven/` |
| `CODE_NOT_FOUND` on every variant turned a whole series into failed runs | a one-case smoke run before a series |
| A hanging variant blamed on a slow `rpm` | the table row for an attempt `running` without events |
| A server of another project was stopped during clean-up | never kill a process; report it |
| Infrastructure errors of some attempts were left out of the report | report them as an anomaly with the events you have |
| A value read back different from what was just written (a key that came back empty) | report it as an anomaly with the file and the read; do not work around it |

## Tools and commands

- `aqven` MCP `run_list` (`series_id`, `view: "compact"`), `run_get_node`, `run_events`, `run_get`, `run_fork`,
  `run_resume`, `run_start` (`agent_overrides`), `series_start` (a `look` over named cases), `series_get`
  (`view: "summary"`), `series_outputs` (`outcome`, `variant`, `case`, `split`, `fields`, `cursor`).
- `uv run aqven series export <series_id> --path <package> --format jsonl --outcome error [--out FILE]`.
- `uv run aqven run <flow_id> --input <file.json> --agent <node>=<agent>` goes through the project server when one
  runs on this root, and starts an engine of its own only when none does; it takes a JSON input, not a dataset case.
- `uv run aqven refs <kind>:<id> <package>`, `uv run aqven tree <package>`.

## References

- `references/mcp-cli/runs.md`: every run tool and its fields, `agent_overrides`, what a fork can and cannot do.
  Read before the first run tool call.
- `references/mcp-cli/experiments-and-series.md`: `series_get` views, the rows and filters of `series_outputs`,
  `series_list`, `aqven series export`. Read at steps 1 and 5 when the failures come from a series.
- `references/concepts/finding-the-node-that-went-wrong.md`: the first failing node and cascades. Read at step 3.
- `references/studio/investigate-a-run.md`, `references/studio/read-the-dev-console.md`: what the owner sees and
  the console lines, and what the `Expected vs actual` panel is not. Read when you point the owner to a run.
- `references/concepts/what-happens-when-a-model-is-called.md`: outcomes, retries and policies. Read at step 4.
- `references/reference/error-codes.md`: every run-time error code with its class and fix, generated from the
  engine. Read at step 6 for a code this skill does not name.
- `references/reference/diagnostics.md`: every `aqven check` code. Read when a run fails on something `check`
  should have caught.
