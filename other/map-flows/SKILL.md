---
name: map-flows
description: Use when asked to map or analyze flows, pipelines, processes, or sequences of events in this repo — e.g. "mapa el flujo", "flow", "pipeline", "ciclo de vida", "trace the request", "how does the build/release flow work", "diagrama del flujo". Maps data flows, request lifecycles, CI/CD pipelines, and state transitions with verified file:line evidence. Distinct from analyze-code (which maps code structure); this skill maps movement over time.
---

# Flow Mapper

You trace and diagram how things move through a system: data, requests,
processes, CI/CD pipelines, and state. Every step in the flow is grounded in a
real file or command — a flow map is only as good as its evidence.

## Steps

1. **Identify the flow** — is it data flow, a request lifecycle, a CI/CD
   pipeline, a state machine, or a build/release process? Ask if ambiguous,
   otherwise infer from the request and proceed.

2. **Find the entrypoint(s) mechanically** — for a request/data flow: the
   listener, handler, or function that receives input. For a pipeline: the
   trigger (GitHub Actions: `on:` in `.github/workflows/*.yml`; web: the page
   that boots the JS; Go: `main()`). Read the entrypoint fully.

3. **Trace step by step** — follow each hop from source to sink:
   - What invokes the next step (function call, event, HTTP request, message,
     workflow step, cron)?
   - What data is passed, transformed, or dropped at each hop?
   - Where does it branch, retry, or fail?
   - Where does it end (response, file, DB, deployment, terminal state)?
   For each hop record `file:line` evidence.

4. **Check the flows you cannot trace by reading** — commands that prove
   behavior: run the pipeline dry (shellcheck, `go vet`, build), grep for the
   entrypoint callers, trace where a symbol/step is referenced. Note anything
   you had to infer rather than verify.

5. **Include failure paths** — every flow has error paths; map what happens on
   each failure (retry, abort, fallback, silent). A flow map without failure
   paths is a fairy tale.

6. **Diagram and report** — produce a step-by-step map. Use a text sequence
   (and offer Mermaid on request). Keep it precise, not decorative.

## Output format

1. **Flow type and scope** — what was mapped and from where to where.
2. **The map** — numbered steps, each with: action, responsible component/file
   (`file:line`), data in -> data out, and trigger.
3. **Branches and failure paths** — every conditional/error path with its
   outcome.
4. **Hot spots** — steps that are fragile, slow, or risky (blocking I/O,
   fixed ports, no timeout, no retry, `|| exit 1` chains).
5. **Verified** — commands run and results; anything inferred marked as such.
6. **Improvements** (only if requested or glaring) — concrete, ordered.

Rules: evidence at every hop; distinguish verified from inferred; map the
real flow, not the intended one.
