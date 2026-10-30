---
name: langfuse-instrumentation
description: Add or change Langfuse tracing for a pipeline step and prove a real trace arrives. Use whenever the ingest, ask or evaluate pipeline changes.
---

# langfuse-instrumentation

## Inputs
Changed pipeline step, `docs/architecture.md` §3.2 span list, Langfuse Python SDK v5 docs.

## Steps
1. Env: `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_BASE_URL`. Check presence with
   `uv run flutter-rag env-check` — never print values.
2. One trace per ask/ingest/eval item; spans per stage; LLM calls as generations with model,
   usage and prompt version; trace metadata: config_id, corpus SHA, git SHA.
3. Do not put secrets or full raw private logs into trace input/output.
4. Call `flush()` before a short-lived CLI exits.
5. Verify: run a real command, then fetch the trace by ID through the Langfuse API or UI.
   Tests with a mocked client are labelled as mock and do not count as delivery proof.

## Outputs
Real trace ID (and URL), prompt version, what spans it contains.

## Boundaries
If keys are missing, state BLOCKED for trace delivery; do not claim it works.
