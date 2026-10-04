---
name: kyoko-instrument
description: Wire an AI agent's telemetry into Kyoko and prove one real run shows up.
when_to_use: Use when the user says "set up telemetry", "instrument my agent", "send traces to Kyoko", "Kyoko is empty", "no traces yet", or "make my runs show up in Kyoko." Guides unknown repos by discovering the runtime, making the smallest safe change, and verifying one useful run landed in Kyoko.
---

You are helping instrument an AI agent so its next meaningful run shows up in
Kyoko. Kyoko is a local-first repair loop: the user's agent runs the workflow,
a recorder captures the run/spans, and Kyoko ingests that telemetry so it can be
inspected, diagnosed, and improved. Kyoko does not run the agent.

Your job is to get **one real run** into Kyoko with the smallest safe change,
verify it actually landed, and only then enrich it. Use Kyoko's documented
ingest paths. Do not invent endpoints or SDK calls.

## Core Rules

- Give visible progress. Say what phase you are in, what you found, and what you
  are about to edit. One or two sentences per update.
- Before editing any file, tell the user the intended change and how risky it is.
- Instrument one real agent entry point first. If several are plausible, ask
  which one should appear in Kyoko.
- Get a minimal run in first, then enrich. Do not trace every helper before a
  basic run lands.
- Prefer the offline file path for the first run (see below). It needs no
  running server, so it is the most reliable way to prove the pipe works.
- Verification is required. Success means Kyoko shows a real run, not just that
  the SDK imported.

## Mental Model: How A Run Gets Into Kyoko

A useful Kyoko run shows the input that triggered the agent, the final
output or error, the model call, and the real tool executions.

There is one canonical shape and two ways to deliver it:

1. **Record** with `KyokoRecorder`: open a run, open spans for model/tool calls,
   finish them. This produces a `kyoko.source_events.v1` payload.
2. **Deliver** that payload one of two ways:
   - **Offline file (preferred for first run):** write it to a JSON file and run
     `kyoko ingest`. This writes straight to the SQLite database and needs **no
     running server**. It cannot fail because a viewer is down.
   - **Live HTTP:** `KyokoClient().ingest(...)` POSTs to a running
     `kyoko serve`. This is best-effort by default: if the server is not up it
     warns and drops the telemetry rather than crashing the agent. Use it once
     `kyoko serve` is confirmed running and you want runs to appear live.

For non-Python stacks or existing OpenTelemetry setups, Kyoko also accepts OTLP
(`POST /v1/traces`) and ships source-adapter templates and importers. See
"Choosing The Path".

## Phase 0: Orient

Do a quick read-only pass:

- Find the target agent entry point: route, worker, CLI, queue job, agent class.
- Identify language/runtime and model/agent SDK.
- Identify where tools actually execute and where the run's input/output live.
- Check whether Kyoko is installed: `kyoko --version`. If not, `pipx install kyoko`
  (or `python3 -m pip install kyoko`).
- Pick the database path. If the project was bootstrapped it is
  `.kyoko/kyoko.db`; otherwise pick one, e.g. `/tmp/kyoko.db`, and reuse it for
  both ingest and `kyoko serve`.

Timebox this. If discovery is not converging, report what you know and ask the
smallest concrete question, e.g. "I found `app/agent.py` and `worker.py` — which
should appear in Kyoko first?"

## Phase 1: Get One Real Run In (Offline)

Goal: prove the pipe works with the smallest change, no server required.

For a Python agent, wrap one real entry point:

```python
from kyoko import KyokoRecorder

recorder = KyokoRecorder(
    profile_id="my-agent",      # stable id for this workflow
    profile_name="My Agent",
    root_path=".",
    agent_name="researcher",    # which agent within the workflow
)

with recorder.run("handle request") as run:   # the invocation boundary
    with run.span("llm", kind="model") as span:
        # ... the real model call ...
        span.finish(status="succeeded", output_ref="output://answer")
    run.finish(status="succeeded", summary="Answered the request.")

# Deliver offline — no server needed:
recorder.write_json("kyoko-run.json")
```

Then ingest the file:

```bash
kyoko ingest --db /tmp/kyoko.db kyoko-run.json --json
```

Run one representative invocation, then verify the run landed:

```bash
kyoko runs --db /tmp/kyoko.db --json
```

You should see the run with the right input/output. If you want to look at it in
the dashboard, start the server against the **same** database:

```bash
kyoko serve --db /tmp/kyoko.db   # then open http://127.0.0.1:8765
```

Phase 1 troubleshooting:

- Empty `kyoko runs`? Confirm the instrumented entry point actually executed and
  that `write_json` ran before the process exited.
- Ingest error? It is a payload problem, not a missing server — read the error;
  the recorder output should be a `kyoko.source_events.v1` object.
- Using `KyokoClient().ingest(...)` instead and seeing "telemetry not
  delivered"? The server is not running. Either start `kyoko serve` on the same
  DB, or switch to the offline `write_json` + `kyoko ingest` path above.
- Make sure the **same `--db` path** is used for ingest and for `kyoko serve`.
  A run ingested into one database will not appear in a server started on another.

## Phase 2: Enrich

Once a basic run lands, make it a useful debugging trace:

- Open a span for each real model call (`kind="model"`) and tool execution
  (`kind="tool"`). Wrap the real tool body, not the decision to call it.
- Pass `usage`, `attributes`, and `output_ref`/`input_ref` where you have them.
- On failure, call `span.fail(err)` / `run.fail(err)` so the error is captured.
- For live visibility while a long run is in flight, you may push live events
  to `POST /v1/live` (the TypeScript client exposes `ingestLive(...)`), but this
  is optional.

Once runs flow reliably, switch delivery to live HTTP if the user wants runs to
appear in the dashboard as the agent runs: start `kyoko serve` and call
`KyokoClient().ingest(recorder.to_source_events())` at the end of each run. It
is best-effort, so it will not break the agent when the server is down.

## Choosing The Path

- **Python agent, you can edit the loop:** `KyokoRecorder` as above. Default.
- **TypeScript/Node agent:** the `@kyoko/sdk` package mirrors the Python API
  (`new KyokoRecorder(...)`, `recorder.run(...)`, `new KyokoClient().ingest(...)`).
  Note TS requires explicit `run.start()` / `run.finish(...)` (no context
  manager).
- **Existing OpenTelemetry / OTLP exporter:** point it at Kyoko's OTLP endpoint
  `POST http://127.0.0.1:8765/v1/traces`, or ingest exported OTLP JSON with
  `kyoko ingest-otlp --db <db> <file.json>`. Do not stand up a second tracer
  provider.
- **You cannot edit the agent, but it writes logs/sessions:** generate a source
  adapter (`kyoko source-adapter-template <path> --framework <fw>
  --profile-name <name>`) or discover local sources
  (`kyoko discover-sources --db <db> --root-path .`). Importers exist for some
  formats (`kyoko import-hermes-kanban`, `kyoko import-openclaw-sessions`).

If no path fits safely, stop and report the entry point and telemetry setup you
found rather than guessing.

## Just Exploring?

If the user only wants to see what Kyoko looks like with data, skip
instrumentation and run the bundled demo:

```bash
kyoko demo --db /tmp/kyoko-demo.db --json
kyoko serve --db /tmp/kyoko-demo.db   # open http://127.0.0.1:8765
```

## Verification

Use the strongest available check:

- `kyoko runs --db <db> --json` lists the run you just produced.
- `kyoko current-run --db <db> --json` and `kyoko run-outline --db <db> <run-id>
  --json` confirm the spans/structure.
- Dashboard: the run appears under Traces at `http://127.0.0.1:8765`.

Phase 1 success: one real invocation appears with input/output. Phase 2 success:
the expected model/tool spans are visible. If a run exists but the content is not
useful, verification failed — keep diagnosing or stop with exact evidence.

## Handoff

Verified:

> Wired. I ran the agent once and confirmed a real run in Kyoko (`kyoko runs`
> shows it). Open http://127.0.0.1:8765 to inspect it.

Needs user run:

> Wired. Run `<command>` now; the next run should land in `<db>`. Check with
> `kyoko runs --db <db> --json`, or open the dashboard with
> `kyoko serve --db <db>`.

Blocked:

> I stopped before guessing. `<specific ambiguity/failure>`. The next step is
> `<specific user choice>`.
