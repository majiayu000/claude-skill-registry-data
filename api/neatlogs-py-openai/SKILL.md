---
name: neatlogs-py-openai
description: Use when adding neatlogs observability to a Python project that calls LLM provider SDKs directly (OpenAI, Anthropic, Google GenAI, Groq, etc.) and uses no agent framework.
metadata:
  author: neatlogs
  language: python
  framework: openai
---

# Neatlogs Python Setup — Direct LLM SDK (OpenAI / Anthropic / Google GenAI / …)

This project calls LLM APIs directly (e.g., `client.chat.completions.create()`). There is no agent framework managing tools or chains. Wrap supported clients once; decorate only the application's own orchestration and custom tools.

## Instrumentation — pick the path that matches the provider

There are two equivalent ways to capture LLM/embedding calls. **Prefer `neatlogs.wrap()`** — it is per-instance, explicit, and needs no global config.

### Path A (PREFERRED) — `neatlogs.wrap(client)` for OpenAI / Anthropic / Google GenAI

`neatlogs.wrap()` detects the client type and patches its LLM-relevant resources in place, returning the same instance:

```python
import neatlogs
from openai import OpenAI

client = neatlogs.wrap(OpenAI())        # chat, responses, embeddings, images, audio … all traced
client.chat.completions.create(...)     # → LLM span (model, tokens, latency)
client.embeddings.create(...)           # → EMBEDDING span
```

Supported by `wrap()`: `OpenAI` / `AsyncOpenAI`, `Anthropic` / `AsyncAnthropic`, `google.genai.Client`. Same call for all three — it auto-routes by type. When you use `wrap()`, do NOT pass `instrumentations=` for that provider.

### Path B (fallback) — `instrumentations=[...]` for providers `wrap()` doesn't cover

`wrap()` does NOT support Groq, Cohere, Bedrock, Mistral, Together, LiteLLM, etc. For those, pass the provider name to `init(instrumentations=[...])` (the global auto-instrumentor):

| Provider SDK | Path |
|---|---|
| OpenAI / Anthropic / Google GenAI | `neatlogs.wrap(client)` (Path A) |
| Groq | `init(instrumentations=["groq"])` |
| Cohere | `init(instrumentations=["cohere"])` |
| Bedrock | `init(instrumentations=["bedrock"])` |
| Mistral | `init(instrumentations=["mistralai"])` |
| Together | `init(instrumentations=["together"])` |
| LiteLLM | `init(instrumentations=["litellm"])` |

Mixing is fine: e.g. wrap an OpenAI client AND `init(instrumentations=["groq"])` if the app uses both. Never list a provider in `instrumentations=[]` AND `wrap()` the same client — that double-fires and produces duplicate spans.

## Combine with manual primitives

- `@neatlogs.span(kind="WORKFLOW"|"CHAIN"|"TOOL"|...)` — decorate orchestration / tool functions.
- `neatlogs.trace("name", kind="LLM", ...)` — create the canonical LLM span only for an unsupported/raw call that has no wrapper or instrumentor.
- `neatlogs.log("msg {x}", x=…)` — timestamped steps inside a span.

The captured LLM/EMBEDDING spans nest under your orchestration spans. Do not add a second manual LLM layer around them.

## Steps

1. **Install SDK** → `references/1-install-sdk.md`
2. **Add init()** → `references/2-add-init.md`
3. **Set environment variables** → `references/3-set-env.md`
4. **Wrap the LLM client(s)** → `references/4-wrap-client.md`
5. **Decorate orchestration functions** → `references/5-decorate-functions.md`
6. **Verify LLM calls have exactly one capture owner** → `references/6-wrap-llm-calls.md`
7. **Decorate tool functions** → `references/7-decorate-tools.md`
7.5. **Embeddings: wrapped/instrumented = automatic; custom = decorate** → `references/7.5-embeddings.md`
8. **Add flush/shutdown** → `references/8-flush-shutdown.md`

## Rules (apply to ALL steps)

- `neatlogs.init()` MUST execute BEFORE the LLM library is imported and BEFORE any client is constructed.
- If `load_dotenv()` exists, it MUST run BEFORE `neatlogs.init()`.
- Prefer `neatlogs.wrap(client)` for OpenAI/Anthropic/Google GenAI; use `init(instrumentations=[...])` only for providers `wrap()` doesn't support. Never both for the same client.
- Wrap EVERY supported LLM client whose calls you want traced: `client = neatlogs.wrap(client)`. Use the returned reference.
- Never hardcode API keys in source. Use `os.getenv()`.
- For EU projects, set `endpoint="https://eu.ingest.neatlogs.com"` in `neatlogs.init()`; for other managed projects, omit `endpoint` and `NEATLOGS_ENDPOINT`.
- Add imports ONLY for what a file actually uses:
  - File calls `neatlogs.wrap(...)` / `neatlogs.span(...)` / a manual raw-call `neatlogs.trace(...)` → add `import neatlogs`.
- When present, `import neatlogs` goes at module top level, never inside functions.
- `@neatlogs.span()` goes BELOW framework decorators (`@retry`, `@app.route`) — closest to `def`.
- Minimal edits only. Add wrap()/decorators + imports. Do not reformat, add comments, or refactor.

## What's auto-captured (DO NOT also manually trace)

Once a client is `wrap()`'d (or its provider is in `instrumentations=[]`), these are auto-captured — do not add a TOOL/EMBEDDING span around them:
- `client.chat.completions.create()` / `client.responses.create()` → LLM span (model, tokens, latency, finish reason)
- `client.messages.create()` (Anthropic) → LLM span
- `client.models.generate_content()` (Google GenAI) → LLM span
- `client.embeddings.create()` → EMBEDDING span
- Streaming variants

You may add WORKFLOW/CHAIN/AGENT spans around genuine multi-step orchestration. Do NOT add `neatlogs.trace(kind="LLM")` around any wrapped or instrumented provider call; the automatic span is canonical.

## Safety gate

Before any edit, confirm this service is Python. Identify the active interpreter
and package manager from its manifests and lockfiles, then read the declared and
installed SDK version. Do not install or change dependencies during this
inspection. Run Doctor through the active interpreter so it can use only the
installed SDK:

```bash
python -m neatlogs doctor --local --json
```

Do not substitute `npx`, `uvx`, `pipx run`, a Wizard command, or another
downloaded Doctor. Local mode must be read-only and network-free. It requires no
credential and must not change source or configuration. Require
`format_version: "neatlogs.doctor/v2"`, `runtime.language: "python"`, and
`runtime.schema_version: "2"`. Treat `runtime.sdk_version` as evidence of the
installed package, not as an exact-version allowlist.

If the command is missing or its result has the wrong format, language, or
schema, fail closed. Check the canonical package registry for the latest
published stable release. If the project uses an older release, show the exact
upgrade command for the detected package manager and obtain explicit user
approval before running it. Accept newer compatible releases and never
downgrade one. If the installed release is already current but lacks Doctor v2,
stop and give safe manual/support remediation. Rerun local Doctor after any
approved upgrade. Do not edit while this gate is unresolved.

A local `pass` proves only that the installed SDK produced and validated its
controlled in-process envelope. It does not prove that the application is
instrumented, that anything was exported, or that a hosted trace is visible.
Preserve every `reason_code` and `remediation_code` exactly. Treat a warning,
failure, or unknown future code as manual/support remediation unless the code is
explicitly safe/fixable here. The only source fixes allowed by this gate are:

- `INSTRUMENTOR_INACTIVE`: apply only this skill's documented initialization or
  wrapper step.
- `ROOT_MISSING`: add only the already-requested, documented WORKFLOW boundary
  at a confirmed entry point.
- `ROOT_NOT_ENDED`: add only this skill's documented lifecycle hook.

Do not edit for credential, authentication, transport, backend, ambiguous
ownership, or unknown codes. Never reproduce backend PII, routing, mapping, or
finalization implementation. Before any build, test, or user-workflow command,
show the exact command and obtain explicit user approval. Make reruns idempotent:
reread the target first and never duplicate initialization, wrappers, roots, or
shutdown hooks. Keep a pre-edit diff. If an approved check fails, use the
rollback plan to revert only the edits from this run when they can be isolated
safely. Otherwise, stop and give manual recovery instructions that preserve
unrelated user work.

After instrumentation, obtain approval for the project checks and one
representative real workflow. Obtain separate approval for the authenticated
probe. Use only a credential already supplied through the process environment.
Never print it, place it in command arguments or files, copy it into output, or
put it in agent context.

```bash
python -m neatlogs doctor --probe --json
```

Probe mode sends one controlled four-span trace through `POST /v1/traces` with
`x-neatlogs-doctor: v1`, then reads that exact trace through
`GET /api/traces/v3/{trace_id}` with the same project credential. Accept a
probe `pass` only when capture and readback trace IDs match, the trace is
finalized, exactly four spans contain one meaningful WORKFLOW root with
AGENT→LLM and root→TOOL relationships, there are no duplicates, required
semantics and I/O are present, and token values remain numeric. Never infer
success from installation, local logs, exporter flush, HTTP 2xx, or any
uncorrelated trace. Probe success proves the controlled path only. Verify the
real user workflow separately through the completion gate below.

## Completion gate

After local Doctor passes and the requested instrumentation is in place:

1. Show the exact project build, test, and real-workflow commands and obtain
   explicit user approval before running them.
2. Run only the approved checks. Restart a long-running process so it loads the
   new initialization and wrappers; keep reruns idempotent.
3. Exercise one representative real user workflow. End every opened span and
   use the documented flush/shutdown lifecycle for that process type.
4. Through the target project's normal product trace view or supported public
   read path, verify that exact run is finalized, has one meaningful root and
   the expected semantic hierarchy, and contains no duplicate operation spans.

Keep project credentials in the process environment or client secret storage;
never put them in commands, output, files, or agent context. Do not use a
legacy marker-discovery protocol. Installation, local logs, exporter flush,
HTTP 2xx, a local Doctor pass, and a separate probe pass are not proof that the
application's real workflow is correct. If the exact user trace cannot be
inspected, report the missing access or observation as a blocker and provide
rollback/manual recovery instructions without claiming completion.

## Reference

- Span kinds → `references/span-kinds.md`
- LLM call patterns → `references/llm-call-patterns.md`
- Sessions & end-users → `references/sessions-and-end-users.md`
