---
name: langfuse-tracing
description: "Wires Langfuse tracing into LLM apps for production observability, monitoring, telemetry, and offline eval - instruments via `@observe` (Python) / `startActiveObservation` (TS) decorators that auto-capture inputs / outputs / timings / errors per generation; exposes `langfuse.update_current_span()` for metadata + cost / latency annotation; supports trace-bound scoring for eval datasets and prompt-as-code management. Use when the user needs to monitor, log, trace, or debug LLM API calls in production beyond pre-deploy eval, wants to add LLM observability tooling to an existing app, or wants to ship traces from production to an eval dataset for offline regression testing."
---

# langfuse-tracing

## Overview

[lf-gh]: https://github.com/langfuse/langfuse-python

Langfuse is a production LLM observability platform (per [lf-gh][lf-gh]).

## Step 1 - Install

Per [lf-gh][lf-gh]:

```bash
pip install langfuse
```

For TypeScript:

```bash
npm install @langfuse/tracing
```

Set up project credentials per Langfuse self-hosted or cloud
project (`LANGFUSE_PUBLIC_KEY` + `LANGFUSE_SECRET_KEY` +
`LANGFUSE_HOST`).

## Step 2 - Instrument with `@observe`

Per [langfuse.com/docs/sdk/python/decorators][lf-py-deco]:

[lf-py-deco]: https://langfuse.com/docs/sdk/python/decorators

Python:

```python
from langfuse import observe

@observe(name="llm-call", as_type="generation")  # auto-captures inputs, outputs, timings, errors
async def my_async_llm_call(prompt_text):
    return "LLM response"
```

TypeScript - create an observation, do work inside it, then end it:

```typescript
import { startActiveObservation } from "@langfuse/tracing";

const { observation, end } = startActiveObservation({
  name: "llm-call",
  type: "generation",
  input: { prompt: promptText },
});

try {
  const result = await callMyLLM(promptText);
  observation.update({ output: result });
  return result;
} finally {
  end();
}
```

**Validation:** After your first instrumented call, open the Langfuse
UI → Traces. You should see a new trace with nested observations,
inputs, outputs, and timings. If no trace appears within ~30 s:
- Confirm `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, and
  `LANGFUSE_HOST` are set in the process environment.
- Call `await langfuse.flushAsync()` (TS) / `langfuse.flush()` (Python)
  before process exit to force-drain the queue.
- Check `langfuse.debug()` output for connection errors.

## Step 3 - Update current observation with metadata

Per [lf-py-deco][lf-py-deco]:

```python
from langfuse import get_client

langfuse = get_client()

with langfuse.start_as_current_observation(as_type="span", name="data-processing"):
    langfuse.update_current_span(metadata={"step1_complete": True})
```

Common metadata fields used in production:

- `model` - the model name (e.g., `claude-haiku-4-5`)
- `model_parameters` - temperature / top_p / max_tokens
- `usage` - input/output tokens, cost
- `tags` - environment (`prod` / `staging`), feature flag, customer ID
- `level` - `DEBUG` / `DEFAULT` / `WARNING` / `ERROR`

## Step 4 - Score traces

Per [langfuse.com/docs/scores][lf-scores]:

[lf-scores]: https://langfuse.com/docs/scores

```python
langfuse.score(
    trace_id="...",
    name="answer_relevance",
    value=0.87,           # numeric (0-1); also supports categorical (string) and boolean
    comment="Judged by GPT-4 rubric"
)
```

Scores can come from:

- **Manual review** (human raters via the Langfuse UI)
- **Automated eval** (run a metric in batch, score by `trace_id`)
- **User feedback** (thumbs-up / thumbs-down from the app)

**Validation:** After scoring, open the Langfuse UI → Traces →
select the trace. The score should appear in the Scores panel.
If missing, confirm the `trace_id` matches an existing trace and
that the score call did not raise an exception.

## Step 5 - Datasets for offline eval

Datasets are collections of `(input, expected_output)` items built from
production traces, CSV / JSONL imports, or the UI. Run one against your
app to diff vs a baseline:

```python
items = langfuse.get_dataset_items(dataset_id="...")
for item in items:
    actual = my_llm_app(item.input)
    item.run(actual)  # links the run back to the dataset for diff vs baseline
```

See [references/datasets.md](references/datasets.md) for building
datasets from production traces, the [lf-ds][lf-ds] API signature, and
the run-validation checkpoint.

[lf-ds]: https://langfuse.com/docs/datasets

## Step 6 - Prompt management

Fetch the current production prompt at runtime and pin its version
so prompt drift is traceable:

```python
from langfuse import get_client

langfuse = get_client()

# Fetch the production-labelled prompt; falls back to cache if offline
prompt = langfuse.get_prompt("my-prompt-name", label="production")
compiled = prompt.compile(user_input=user_query)

# Pass compiled text to your LLM call
response = my_llm_call(compiled)
```

Iterate prompt text in the Langfuse UI and roll out new versions
per environment (`production` / `staging` labels) without code
deploys. Version history and A/B comparison are available in the UI.

**Validation:** After an instrumented call using a managed prompt,
open the Langfuse UI → Traces → select the trace. The prompt name
and version should appear in the trace metadata, confirming prompt
version is pinned and attributable.

## Step 7 - CI integration

Langfuse is observability-side, not pre-deploy CI-side. Post-deploy CI
patterns query the Langfuse API for recent traces and assert on
aggregate metrics (a score-query gate, eval-on-trace, cost-regression,
score-based alerting). Runnable gate script and the full pattern list:
[references/ci-integration.md](references/ci-integration.md).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Trace everything in production with no sampling | Cost explodes at scale | Use `level=DEBUG` + UI-side sampling (Step 3) |
| Score traces only via UI (no automated path) | Can't catch silent regressions | Automated `langfuse.score()` per trace (Step 4) |
| Pull production trace inputs without privacy review | PII leakage into eval datasets | Cross-ref `synthetic-pii-generator` for fixture sanitization before promotion |
| Skip prompt versioning | Prompt drift breaks attribution | `langfuse.get_prompt()` with version pin (Step 6) |
| Conflate Langfuse with pre-deploy eval | Tries to be both; wins neither | Pair Langfuse (post-deploy) with Promptfoo/DeepEval/Ragas (pre-deploy) |

## Version notes

Per [lf-gh][lf-gh], the SDK was rewritten in v4 and released in March
2026; this skill targets the v4 API. v3 patterns are no longer
supported - pin the SDK version in requirements, and for v3 codebases
see the upstream migration guide.

## Limitations

- Langfuse cloud is hosted; for data-residency-strict teams,
  self-host (well-supported but operational overhead).
- SDK and score-API signatures may drift between versions; always
  consult [langfuse.com/docs][lf-docs] and [lf-scores][lf-scores]
  when authoring wiring against any rapidly-evolving endpoint.
- Integration with eval frameworks evolves rapidly; consult
  [langfuse.com/docs][lf-docs] for current Promptfoo / DeepEval /
  Ragas integration patterns.

[lf-docs]: https://langfuse.com/docs

## References

- [lf-gh][lf-gh] - Python SDK repo, install, version note
- [lf-py-deco][lf-py-deco] - `@observe` decorator + observation
  patterns
- [lf-scores][lf-scores] - score API
- [lf-ds][lf-ds] - datasets
- [lf-docs][lf-docs] - full documentation
- `promptfoo-evaluation`,
  `deepeval-evaluation`,
  `ragas-evaluation`,
  `giskard-llm` - pre-deploy eval sister
  tools
