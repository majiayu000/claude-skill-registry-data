---
name: using-langfuse
description: LLM observability with Langfuse — tracing (sessions/spans/generations/scores), prompt management, datasets, eval, cost/latency monitoring.
when_to_use: >
  Reach for this when adding observability, prompt versioning, evaluation, or cost/latency
  monitoring to any LLM application — preferred in this library over OpenLLMetry, Helicone,
  PromptLayer, and Weights & Biases for LLM tracing. Works across providers (Anthropic,
  OpenAI, Perplexity) and frameworks (LangChain, LangGraph, raw SDKs). For *provider-specific*
  capability decisions defer to the provider skill (using-anthropic-platform /
  using-openai-platform / using-perplexity-platform); for the *agent graph* itself use
  building-langgraph-agents; for *tool-call* design see building-tool-orchestration; for *RAG
  evaluation metrics* see building-rag-pipelines. **ALWAYS WebFetch
  https://langfuse.com/docs and https://langfuse.com/docs/changelog BEFORE recommending an SDK
  version, integration path, eval primitive, or pricing tier — Langfuse ships features
  (datasets v2, prompt experiments, dashboards) faster than any training snapshot.**
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Langfuse — LLM Observability Quick Reference

Langfuse is an open-source LLM engineering platform: tracing, prompt management, evaluation,
and dataset experiments. Use it as the cross-cutting observability layer over every other LLM
skill in this library.

---

## Stay current — DO NOT rely on training-data knowledge of Langfuse SDKs or features

Langfuse ships rapidly (decorators, v3 SDKs, prompt experiments, dataset run modes, native
integrations with LangChain/LangGraph/OpenAI/Anthropic, self-hosted vs cloud feature parity).
**Before** you (a) recommend an SDK version, (b) cite a feature, (c) wire a provider
integration, (d) describe pricing, or (e) compare self-host vs cloud, you **MUST** WebFetch
and cite:

- **Docs (canonical):** https://langfuse.com/docs
- **Changelog:** https://langfuse.com/docs/changelog
- **Pricing:** https://langfuse.com/pricing
- **Self-hosting:** https://langfuse.com/self-hosting
- **Python SDK reference:** https://langfuse.com/docs/sdk/python
- **JS/TS SDK reference:** https://langfuse.com/docs/sdk/typescript

Cite source URL + fetch date for every SDK call / feature / price you assert. **Trust the
fetch over the snapshot.** For provider-specific model selection / pricing claims, defer to
the provider skill's Stay-current — Langfuse's role is to *observe* what you run.

---

## When to Use

Load this skill when:
- `langfuse` Python or `langfuse` npm package is in dependencies
- `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` / `LANGFUSE_HOST` env vars present
- The project needs prompt versioning, A/B tests, or dataset evaluation
- You're debugging "why did the agent answer X" in production
- Cost / latency monitoring is a requirement

---

## Core Data Model

```
Trace                          (one user request / agent invocation)
├── Observation: SPAN          (a logical step — "retrieve", "rerank", "answer")
│   ├── Observation: GENERATION  (an LLM call — model, prompt, completion, usage)
│   ├── Observation: SPAN         (nested step)
│   └── Observation: EVENT        (a point-in-time marker)
├── Scores                     (numeric/categorical evaluations on the trace or observation)
└── Session                    (multi-trace grouping — full conversation)
```

- **Trace** = root of a user-facing operation.
- **Span** = duration-bounded step (you choose granularity).
- **Generation** = LLM call specifically (auto-captures tokens, cost, model).
- **Score** = eval result (`faithfulness=0.87`, `thumbs_up=1`, `relevance="good"`).
- **Session** = string id linking traces from one conversation/user thread.

---

## Quick Start

### Python (decorators)

```python
from langfuse.decorators import observe, langfuse_context
from langfuse.openai import openai          # drop-in instrumented client

@observe()
def answer(user_id: str, question: str) -> str:
    langfuse_context.update_current_trace(user_id=user_id, session_id=f"sess-{user_id}")
    context = retrieve(question)                    # also @observe()'d
    return generate(question, context)              # also @observe()'d

@observe(as_type="generation")
def generate(question: str, context: list[str]) -> str:
    resp = openai.chat.completions.create(          # auto-traced as a generation
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer from context."},
            {"role": "user", "content": f"Q: {question}\n\nContext:\n" + "\n".join(context)},
        ],
    )
    return resp.choices[0].message.content
```

### TypeScript

```typescript
import { Langfuse } from 'langfuse';

const lf = new Langfuse();   // reads LANGFUSE_* env vars

const trace = lf.trace({ name: 'chat', userId, sessionId });
const retrieveSpan = trace.span({ name: 'retrieve' });
const context = await retrieve(question);
retrieveSpan.end({ output: { count: context.length } });

const gen = trace.generation({
  name: 'answer',
  model: 'gpt-4o-mini',
  input: { question, context },
});
const answer = await llm(question, context);
gen.end({ output: answer, usage: { promptTokens: 1200, completionTokens: 80 } });

await lf.flushAsync();   // important in serverless / short-lived processes
```

---

## Provider & Framework Integrations

Verify each via WebFetch (versions and method names change):

| Stack | Integration |
|-------|-------------|
| OpenAI Python SDK | `from langfuse.openai import openai` (drop-in) |
| OpenAI JS SDK | `observeOpenAI(client)` wrapper |
| Anthropic | Decorator + manual `generation()` or wrapper if available |
| LangChain (PY/TS) | `CallbackHandler` from `langfuse.callback` |
| LangGraph | Same callback handler; auto-traces nodes |
| Vercel AI SDK | Built-in telemetry → Langfuse exporter |
| LiteLLM | Built-in Langfuse callback |
| OpenTelemetry | OTel exporter (cross-framework) |

Always cite the specific integration page you used.

---

## Prompt Management

Promote prompts from code into Langfuse so changes don't require deploys.

```python
from langfuse import Langfuse
lf = Langfuse()

# Fetch by name + label (production / staging / specific version)
prompt = lf.get_prompt("rag/answer", label="production")
rendered = prompt.compile(question=q, context="\n".join(ctx))

# Link the LLM call to the prompt version so traces show which version answered
gen = trace.generation(
    name="answer",
    model="claude-sonnet-4-20250514",
    prompt=prompt,           # binds version
    input=rendered,
)
```

Benefits:
- Edit prompts in UI without redeploying.
- Each trace's UI links back to the exact prompt version used.
- A/B labels (`production` vs `candidate`) enable progressive rollout.

---

## Scoring & Evaluation

### Manual (user feedback)

```python
langfuse.score(trace_id=trace_id, name="user_thumbs", value=1)        # 1 = up, 0 = down
```

### Programmatic (LLM-as-judge / heuristic)

```python
# After an answer is produced
score = judge_faithfulness(answer, context)   # returns 0.0–1.0
langfuse.score(trace_id=trace_id, name="faithfulness", value=score, comment=judge.reason)
```

### Dataset experiments

```python
dataset = lf.get_dataset("rag-eval-v1")
for item in dataset.items:
    with item.observe(run_name="cohere-rerank-v3") as trace_id:
        answer = pipeline(item.input)
        score = judge(answer, item.expected_output)
        lf.score(trace_id=trace_id, name="faithfulness", value=score)
```

Runs are comparable side-by-side in the UI — wire this into CI to block regressions.

---

## Cost & Latency Monitoring

Generations auto-capture `(input_tokens, output_tokens, model)`. Langfuse computes cost using
its model price table; verify your model is recognized and pricing is current. For unknown
models, supply `usage_details` and a `cost_details` block manually.

Dashboards out of the box: cost per user/session/trace, p50/p95/p99 latency by model or
endpoint, error rate over time, score distributions.

For SLO alerts, export to your metrics stack via OTel or webhooks.

---

## Sessions & Users

Group related traces:

```python
@observe()
def turn(...):
    langfuse_context.update_current_trace(
        session_id="conv-abc123",     # all turns of one conversation
        user_id="user-42",
        tags=["beta", "rag"],
        metadata={"tenant_id": tid, "experiment": "rerank-v3"},
    )
```

Sessions enable "show me the whole conversation" view — essential for debugging multi-turn
agent issues.

---

## Self-Hosted vs Cloud

- **Cloud**: fastest start; verify region (US/EU) for data residency. Pricing per ingested
  event — check the live pricing page.
- **Self-hosted**: Docker / Helm chart; Postgres + ClickHouse + Redis backend. Required for
  strict compliance / VPC-only / on-prem. Verify minimum infra reqs in current self-hosting
  docs.

Same SDK, switch via `LANGFUSE_HOST` env var.

---

## Serverless / Short-Lived Processes

The SDK batches in the background. In Lambda, Cloud Functions, edge runtimes:

```python
langfuse.flush()        # blocking — call at the end of the request
```

```typescript
await lf.flushAsync();  // critical before the runtime freezes
```

Missing the flush = silently dropped traces.

---

## Security

- **Never log secrets**: redact API keys / PII from inputs/outputs before tracing. The SDK
  supports a `mask` function — use it.
- **Tag with tenant_id** so you can filter / delete per-tenant.
- **Public vs secret key**: the public key is safe in browser/client SDKs; secret key is
  server-only.
- **Right-to-be-forgotten**: Langfuse exposes deletion APIs — wire them into your DSAR flow.

---

## Common Patterns

- **One trace per user-facing request.** Spans / generations nest under it.
- **Bind the prompt version** on every generation so UI shows source of truth.
- **Score everything you can cheaply** (user feedback, heuristics) and sample expensive
  judges (LLM-as-judge).
- **Dataset-driven CI**: run a golden dataset on every PR; fail on score regression > threshold.
- **Tag experiments** with a stable name so you can pivot the UI by experiment.

---

## Anti-Patterns

- **Forgetting to flush** in serverless — silently lose all traces.
- **Logging raw PII** in prompts/completions — pipe through a mask.
- **Hard-coding prompts** in code when you already pay for prompt management — defeats the
  purpose.
- **Treating Langfuse as your only eval.** Pair production scores with a small golden set
  in CI.
- **No `session_id`** on multi-turn agents — you'll see disconnected traces and waste hours
  debugging.

---

## See Also

- `using-anthropic-platform`, `using-openai-platform`, `using-perplexity-platform` —
  provider-specific SDK details; Langfuse instruments them.
- `building-langgraph-agents` — `CallbackHandler` auto-traces graph nodes.
- `building-tool-orchestration` — trace every tool call as a span; score selection accuracy.
- `building-rag-pipelines` — trace retrieve/rerank/answer; run dataset evals here.
- `building-agent-memory` — trace memory save/recall as spans.
