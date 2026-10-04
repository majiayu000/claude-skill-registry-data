---
name: agent-observability
description: >
  Instrument a shipped product's AI agents with tracing and observability so
  you can see what they did, why outputs happened, and what each run cost.
  Plain-language primer plus free-tier-first backend selection (Langfuse,
  Phoenix, LangSmith, Braintrust) and OpenTelemetry/OpenInference
  instrumentation. Load when the user asks to add observability, add tracing,
  instrument my agents, see what my agent is doing in production, set up
  Langfuse or Phoenix or LangSmith, debug why my agent gave a bad answer, or
  track LLM cost per request. Also fires when agent-system-architecture or
  setup-evaluation requires an observability plan for an agent-chain product.
  NOT for tracing the coding agent itself — that is run-trace. Precondition
  for runtime-learning-loop.
license: MIT
metadata:
  author: dvy1987
  version: "1.0"
  category: project-specific
  sources: >
    OpenTelemetry GenAI semantic conventions (gen_ai.*), OpenInference
    (Arize), Langfuse/Phoenix/LangSmith/Braintrust public docs and pricing
    (verified 2026-07), practitioner comparisons 2026
  resources:
    references:
      - backends.md
      - examples.md
---

# Agent Observability

You instrument the user's *product* agents — not the coding agent — so every run leaves a trace that can be inspected, scored, and learned from. You explain everything in plain language: the user is non-technical.

## Plain-Language Primer (teach this first, once)

- A **trace** is the full story of one request: every model call, tool call, and retrieval step, in order, with timing, tokens, and cost attached.
- A **span** is one step inside that story (one LLM call, one tool call).
- **Observability** means you can answer "why did this output happen?" and "what did this run cost?" *after the fact*, without guessing.
- The **backend** is a separate managed service. Your product sends trace data to it over HTTPS as a side effect of running. You do NOT host it yourself in the common case, and it never runs on your laptop.
- Why it matters: an agent can return a confident wrong answer with HTTP 200. Without traces you cannot debug it, cannot measure quality, and cannot run any learning loop (`runtime-learning-loop` hard-fails without this).

## Hard Rules

Never log secrets, API keys, or user PII into trace payloads — configure redaction/masking before production traffic, not after.
Never propose self-hosting on the user's machine. Managed free tier first; self-host-in-cloud is a clearly-labeled last resort.
Always instrument against OpenTelemetry GenAI conventions (`gen_ai.*`) or OpenInference — never a proprietary-only SDK — so the backend can be swapped later by config, not a rewrite.
Always verify the first trace end-to-end (run once, open the trace, see spans + token counts) before calling the setup done.
Always set a sampling/cost policy before production scale — keep failures at 100%, sample successes.

## Workflow

### Step 1 — Scope
Identify: which agent flows matter most (start with ONE), expected volume/month, whether data is sensitive (PII/health/finance), and which framework the product uses (Google ADK, LangGraph/LangChain, OpenAI/Anthropic SDK direct, custom).

### Step 2 — Choose a backend
Read `references/backends.md` (decision table, free tiers, tradeoffs — verify current pricing at decision time; tiers change). Defaults: Langfuse Cloud free tier for general use; Phoenix for agent-heavy/ADK products (deepest multi-step agent views); LangSmith only if the product is LangChain/LangGraph-first. Sensitive data → check the backend's redaction options FIRST; most redact nothing by default.

### Step 3 — Instrument
Prefer auto-instrumentation for the detected framework (one `register()`/`instrument()` call + env vars for keys/endpoint). Put API keys in environment variables — never in code. Wrap only the entry point; let the instrumentor capture nested spans. Tag spans with `user_id`/`session_id`/feature name so cost and quality can be sliced later.

### Step 4 — Verify first trace
Run one real request. Open the backend UI. Confirm: full span tree visible, prompts/completions captured, token counts + cost present, no secrets/PII in payloads. If any check fails, fix before proceeding.

### Step 5 — Cost and sampling policy
Async exporters add negligible latency; the real costs are storage and noise. Policy: 100% of failed runs, sampled successes (start 10–25% at scale), retention matched to the free tier's window. Set a monthly span budget aligned to the free-tier cap.

### Step 6 — Wire to quality loops
Point `eval-pipeline` at production traces (score samples with `eval-judge`); this trace+eval pair is the precondition `runtime-learning-loop` checks. Record backend choice + config in `docs/observability/OBSERVABILITY.md` and log it to `docs/skill-outputs/SKILL-OUTPUTS.md`.

## Output Format

```
=== Observability Plan: [product] ===
Flow instrumented: [flow] | Framework: [ADK|LangGraph|SDK|custom]
Backend: [name + tier] — why: [1 line] | Est. volume: [spans/mo] vs free cap: [cap]
Redaction: [what is masked] | Sampling: [failures 100%, successes N%]
First trace verified: [yes/no] | Saved: docs/observability/OBSERVABILITY.md
Next: eval-pipeline wiring → runtime-learning-loop precondition met
```

## Gotchas

- **Traces are for the shipped product; `run-trace` is for the coding agent.** Different data, different store — never mix them.
- **SaaS backends receive your prompts.** That is user data leaving your infrastructure — check redaction defaults (usually OFF) before pointing production at them.
- **Instrument to the standard, not the vendor.** All major backends ingest OTel GenAI `gen_ai.*` spans; the backend is a 2-year decision, the instrumentation is forever.
- **Free-tier caps are per month and small** (e.g. tens of thousands of spans). One agent request can emit 5–30 spans. Do the multiplication before promising "free".
- **A trace that omits tool calls is half a trace.** Multi-agent debugging lives in the tool/handoff spans, not the final completion.

## Example

<examples>
  <example>
    <input>My appeal-drafting app gives weird answers sometimes and I have no idea why. Add observability. It's Google ADK + FastAPI on Cloud Run.</input>
    <output>
Primer given (traces/spans/backend in plain language).
Scope: draft-appeal flow, ~3k requests/mo (~30k spans), synthetic PHI only — still mask document text.
Backend: Phoenix (deepest agent-trace views; OpenInference auto-instrumentation for ADK) — cloud free tier fits 30k spans/mo.
Instrumented via openinference-instrumentation for ADK + env-var keys. First trace verified: 14 spans, tokens + cost visible, document text masked.
Sampling: failures 100%, successes 25%. Saved docs/observability/OBSERVABILITY.md. Logged to SKILL-OUTPUTS.
Next: wire eval-pipeline to score 20 sampled traces/week.
    </output>
  </example>
</examples>

Read `references/examples.md` for full walkthroughs (Langfuse path, redaction setup, backend swap).

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Add observability later, ship first" | You cannot debug the past — traces only exist from instrumentation day forward. |
| "Logs are enough" | Logs show 200 OK; traces show the wrong retrieval that caused the bad answer. |
| "Self-host to save money" | Ops burden (DB + Redis + storage) exceeds free-tier value at this scale; laptop hosting is banned. |
| "Pick the backend by brand" | Pick by framework fit + free-tier math + redaction needs; instrumentation stays portable. |
| "Trace everything forever" | Cost and noise explode; sample successes, keep failures, match retention to need. |

## Verification

- [ ] First real trace opened in backend UI with full span tree + token counts
- [ ] No secrets or PII visible in any span payload (spot-check 3 traces)
- [ ] Sampling + retention policy written into OBSERVABILITY.md
- [ ] Instrumentation is OTel GenAI / OpenInference (backend swappable by config)
- [ ] docs/skill-outputs/SKILL-OUTPUTS.md appended

## Red Flags

- Backend chosen before checking framework auto-instrumentation support
- Production traffic flowing with default (empty) redaction config
- Proprietary SDK wrapped around every call site instead of one instrumentor
- "Observability done" claimed without opening a single real trace
- Coding-agent activity and product traces mixed in one store

## Impact Report

```
Observability set up for: [product/flow]
Backend: [name + tier] | Framework instrumented: [name]
First trace verified: [yes/no] | Redaction: [configured/not needed]
Sampling: [policy] | Files: docs/observability/OBSERVABILITY.md
Ready for: eval-pipeline wiring, runtime-learning-loop precondition
```
