---
name: quick-eval
description: Execute a bounded Coval evaluation on explicit test cases, then audit conversation, recording and metric evidence. Use when the user requests a run; does not automatically rerun, tune an agent or schedule evaluations.
argument-hint: "[agent] [test-set]"
compatibility: Coval CLI with agent mode; Python 3.10+ for optional local planning and read-only evidence helpers.
---

# Run a bounded evaluation

Launch only the selected evaluation, then explain what its evidence supports.
For voice, success requires actual voice conversations and inspected recordings;
a saved resource or a completed run status is not sufficient.

## Preflight and budget

Confirm the intended org, workspace and API environment from the customer's
context; authentication alone does not identify the organization. Reuse their
agent/persona/test set. Read the exact cases and metric definitions before
launching. Use `coval --agent agent doctor`, resource `context` and `--help`.
Do not print secrets or change the machine's global account configuration.

Keep a local session ledger of launch IDs, cases, metric tests and budget used.
If no budget is given, propose one connection-check call, then at most three
conversations total for a starter evaluation, one iteration and concurrency one.
These are defaults to propose, not spending authority. Honor already authorized
counts; a plan/audit request does not authorize a paid call. A larger scope needs
an explicit budget, not a quiet increase after an inconclusive result.

Show the concrete plan: IDs, named cases, metrics, iteration and concurrency,
base/mutation variants, maximum calls, configured per-call duration, and wall-clock
stop. Cost includes Coval, connected providers and metric tests. Coval may add mandatory
or dependency metrics beyond the requested IDs; inspect actual outputs and treat
planned metric counts as requested work, not an exact billing total. Quote money only
with known current rates; otherwise report counts and a duration upper bound.

**Call count = selected cases × iterations × (1 + mutation count)** per persona
run, summed across all runs. A single mutation also runs the base agent. Concurrency
changes speed, not total calls. Re-scoring existing outputs costs metric work but
requires no new voice calls. Reserve rerun budget explicitly rather than treating
retries as free. Do not assume cancellation instantly prevents every queued call.

## Build and check the exact request

Use explicit `options.test_case_ids` from the chosen test set. Don't launch the
whole set by omission or substitute a random subset during a paired comparison.
Check the current [runs schema](https://api.coval.dev/v1/openapi/runs).

```json
{
  "agent_id":"<selected-agent-id>",
  "persona_id":"<selected-persona-id>",
  "test_set_id":"<selected-set-id>",
  "metric_ids":["<selected-metric-id>"],
  "options":{"test_case_ids":["<selected-case-id>"],"iteration_count":1,"concurrency":1},
  "metadata":{"display_name":"First evaluation - connection check"},
  "config_overrides":{"simulation_timeout_seconds":120}
}
```

Verify that the duration override is supported by the current API/agent type;
otherwise use a verified stored limit or stop to resolve the limit. Don't mutate
an existing agent to set it incidentally. Verify created/run metadata after
launch; a local plan is not a server-enforced spending cap.

Use the optional **local-only** planner from this installed skill's directory:

```bash
python3 scripts/plan.py --launch run.json --remaining-simulations 3 --max-concurrency 1
```

`--remaining-simulations` is the already authorized remaining session budget.
For multiple personas/runs, put all launch bodies in one JSON array and validate
the batch together; the helper decrements the same remaining budget for every
launch. It checks explicit subsets, positive bounds, base + mutations and a call
limit. It does not authenticate, validate resource ownership, reserve budget,
enforce server-side limits or launch anything. Read each resource to establish
ownership and case membership separately. Preserve an exact copy of the request.

## Launch once and follow that run

```bash
coval --agent runs launch --input-json @run.json
```

Check `ok` and the exit code; save the returned run ID immediately. On a timeout
or ambiguous response, inspect recent matching runs before considering another
launch. Don't retry a POST blindly. API errors are not empty results.

Poll `coval --agent runs get <run-id>` at a reasonable interval, for example 20–30
seconds, until terminal or the agreed wall-clock deadline. Status spellings can
include spaces; read the current response. Don't wait forever with `runs watch`.
At the deadline report the pending run and preserve its ID. Never start a second
run because the first is slow. Cancel only when requested or already covered by
the agreed stopping policy, and verify the resulting state.

## Audit the result, not just the run status

For a small run, inspect **every** conversation and selected metric:

```bash
coval --agent simulated-conversations list --run-id <run-id> --page-size 100
coval --agent simulated-conversations get <simulation-id>
coval --agent simulated-conversations metrics <simulation-id>
coval simulated-conversations audio <simulation-id> -o <local-recording.wav>
```

Some CLI versions omit pagination tokens. For complete evidence, the optional
read-only helper fetches the public API with pagination and strict run membership:

```bash
python3 scripts/fetch_run.py --run-id <run-id> --workspace-id <workspace-id> --out run-evidence.json
```

It reads `COVAL_API_KEY` from the environment, uses `https://api.coval.dev/v1`,
and writes a private local file including transcripts. Never paste/export the
key or read it into terminal output. `--max-conversations` bounds reads (default
100); exceeding it fails rather than silently claiming completeness. This helper
is for the public production API; for another explicitly chosen environment,
use its documented API with the same scoping/pagination checks. Do not silently
switch environments to make the helper work.

The snapshot retains superseded metric outputs so a later re-score cannot silently
replace historical evidence. Select the intended output IDs and versions; multiple
outputs for one metric are not extra conversations. Inspect full metric details
when criterion subvalues are missing or flagged as truncated. The snapshot excludes
raw runtime metadata; retrieve the exact output separately when model provenance matters.

Check:
- Expected vs observed calls, selected case IDs and base/mutation counts.
- Individual status/end reasons, both transcript speakers, and whether the caller
  actually exercised the case. Separate simulator/test-design faults from agent faults.
- Voice recording retrieval and relevant audio segments. `has_audio` is availability
  metadata, not listening proof. Avoid publishing signed recording links.
- Every selected metric's status and coverage. `FAILED`, `SKIPPED`, `CANCELLED`,
  missing and null values are unevaluated, not zero or pass.
- Value, units, polarity, explanation and per-criterion details. A correct answer
  quoted only by the caller is not evidence the assistant answered correctly.
- Captured metric version/model metadata and prompt/config snapshot. If historical
  version evidence is unavailable, say so instead of substituting today's definition.

If transcripts or metric results are delayed, use a bounded read-only poll of the
same IDs. Never resimulate automatically. Don't use legacy `/eval/*` fallbacks.

## Report and stop

Return actual run/resource IDs, requested/observed/scored counts, execution
failures, quality findings and unknowns separately. Use verified app URLs from
the user's org/workspace context. Explain what was listened to, read and measured.
A small successful run is a smoke test, not production prevalence or statistical
confidence. Preserve raw evidence locally; redact sensitive content for sharing.

Recommend one next step based on the result. No automatic hill-climbing, agent
prompt changes, new cases, metric-default changes, scheduling or cleanup.
