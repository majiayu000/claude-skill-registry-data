---
name: builtin-llm-models
description: "Reference for Manus's built-in LLM catalog and how to call it correctly. Read this BEFORE writing any script that calls LLMs in bulk (summarization, translation, classification, extraction, deep analysis, judging/evaluation, map/parallel fan-out) on a Manus computer — the Sandbox, the user's local computer, or a Cloud Computer — AND before using the built-in LLM in a webdev project (invokeLLM / listLLMModels). Use it to discover which models exist, each model's price/capabilities, how to pick one, the exact request shapes (thinking/reasoning, JSON-schema structured output, vision, tools), and the per-model gotchas (max-token handling, reasoning syntax) verified against the live proxy."
compatibility: opencode
---

# Built-in LLM Models

For the commands below, replace `<skill-dir>` with the **absolute directory containing this loaded `SKILL.md`**, using its actual read path or the current runtime Skill catalog locator. Keep the quotes, including when the path contains spaces. Use a path accessible on the computer executing the command; do not derive it from the shell working directory or assume an installation root. Bundled documentation links resolve from the file containing the link.

Manus ships an OpenAI-compatible LLM proxy. These entry points share the **same model catalog**:

| Context | How to call | Credentials |
| --- | --- | --- |
| Scripts on any Manus computer (Sandbox, local computer, Cloud Computer) | `manus-node` with the bundled `lib/llm.mjs` and `scripts/*.mjs` | Automatic |
| Sandbox only: Python | `openai` Python SDK with `OpenAI()` | `OPENAI_API_KEY`, `OPENAI_API_BASE` (preconfigured) |
| Webdev project (server-side) | `invokeLLM` / `listLLMModels` from `server/_core/llm` | `BUILT_IN_FORGE_API_URL`, `BUILT_IN_FORGE_API_KEY` |

All speak the OpenAI Chat Completions schema. **Do NOT hardcode the model list
from memory** — it changes. Always pull the live catalog (Step 1) before relying
on any specific ID, price, or capability.

**Scripts on any Manus computer.** `manus-node` is supplied by Manus on the local computer, Cloud Computer and Sandbox. It requires no npm install or user Node setup. Authentication is automatic; never read, print, copy or manually pass tokens. If `manus-node` or the runtime is unavailable, report that the Manus runtime needs updating. Run scripts with a literal absolute script path (keep the quotes; not a shell variable) or an explicit execution directory, so Manus can inspect the script before it runs.

**On a local computer or Cloud Computer**, use only the `manus-node` path. Python, the `openai` package and `curl` may be missing there, and any `OPENAI_API_KEY` / `OPENAI_API_BASE` variables belong to the user's own provider account, not to Manus — do not use them. LLM calls require network access: when using `exec` on a local computer, set `network: true` so Manus can request the normal network permission.

## Step 1 — Always fetch the live catalog first

The catalog (IDs, `pricing`, `capabilities.thinking_param`, `capabilities.thinking_example`)
is the source of truth. Snapshots in this skill go stale; the API does not.
Use only model IDs listed by the live catalog. Unlisted IDs may still answer for
backward compatibility, but they are retired and must not be chosen.

Any Manus computer:
```bash
manus-node "<skill-dir>/scripts/models.mjs"
```

Sandbox alternative:
```bash
curl -s "$OPENAI_API_BASE/models" -H "Authorization: Bearer $OPENAI_API_KEY" | python3 -m json.tool
```

Webdev (project shell, or `listLLMModels()` at runtime):
```bash
curl "$BUILT_IN_FORGE_API_URL/v1/models" -H "Authorization: Bearer $BUILT_IN_FORGE_API_KEY"
```

### Model Catalog Snapshot (2026-10-12)

**This is a snapshot. Always re-verify against the live `/models` endpoint** because IDs, prices, and capabilities change over time. All models below support **tools, vision, JSON-schema structured output, and thinking/reasoning**; none expose streaming on the proxy (`supports_streaming: false`). Pricing is USD per 1M tokens (input / output); the catalog also reports `input_credits_per_1m_tokens` / `output_credits_per_1m_tokens`.

| Model ID | Owner | In / Out ($/1M) | thinking_param | Best for |
| --- | --- | --- | --- | --- |
| `gpt-5-nano` | openai | 0.05 / 0.40 | `reasoning` | Cheapest/fastest; huge-volume lightweight tasks |
| `gpt-5-mini` | openai | 0.25 / 2.00 | `reasoning` | **Default** cheap+fast workhorse for most bulk jobs |
| `gpt-5` | openai | 1.25 / 10.00 | `reasoning` | Flagship reasoning + coding |
| `gpt-5.5` | openai | 5.00 / 30.00 | `reasoning` | Hardest reasoning/generation workloads |
| `gemini-3-flash-preview` | google | 0.50 / 3.00 | `thinking` | Fast long-context + multimodal at low cost |
| `gemini-3.1-pro-preview` | google | 2.00 / 12.00 | `thinking` | Flagship long-context + multimodal reasoning |

Claude models are retired from the live catalog at this snapshot; do not use them. The Claude request shapes below apply only if the live catalog lists Claude IDs again.

## Step 2 — Pick a model

Decision order for typical Manus tasks:

1. **Translation / summarization / classification / tagging / simple extraction at scale** → `gpt-5-mini`. Drop to `gpt-5-nano` only if volume is very large and per-item quality tolerance is loose. Skip thinking for these (adds cost and latency with little gain).
2. **Nuanced analysis, code generation, structured reasoning over each item** → `gpt-5`, optionally with a modest reasoning effort.
3. **LLM-as-judge / evaluation, multi-step agentic reasoning, hardest problems** → `gpt-5.5` or `gemini-3.1-pro-preview`. Use real reasoning here.
4. **Very long inputs or image/PDF/audio/video inputs at low cost** → `gemini-3-flash-preview` (large context, multimodal, cheap), upgrade to `gemini-3.1-pro-preview` when quality matters.

If the live catalog lists Claude models, `claude-sonnet-*` fits item 2 and `claude-opus-*` fits item 3.

### Cost-aware batching pattern

For large batches, run a cheap model first (e.g. `gpt-5-nano`/`gpt-5-mini`), apply a programmatic quality gate (schema validation, length checks, confidence field), then re-run only the failures on a stronger model. This typically cuts spend by an order of magnitude versus running everything on a premium model.

### Mapping models to the `map` tool (wide / parallel research)

When using Manus's `map` tool for homogeneous parallel subtasks, the subtasks themselves run as full agents; you generally do not pick a proxy model there. Use this skill's `scripts/llm_batch.mjs` (or direct client calls) when YOU are writing a script that fans out raw LLM calls and needs explicit model/cost control.

## Step 3 — Call it with the correct request shape

The proxy mirrors OpenAI Chat Completions, but provider-specific behaviors (like extended thinking, reasoning effort, and strict JSON schemas) differ by family.

### 🚨 The Max-Token Trap (Crucial — differs by family)

When a model reasons/thinks, it consumes tokens *before* generating the final answer.

- **GPT:** Use `max_completion_tokens` to cap visible output while leaving reasoning unconstrained.
- **Gemini:** Use `max_tokens` (e.g. `max_tokens: 16384`). Do **NOT** use `max_completion_tokens` — on the current proxy it causes `content: null` with `finish_reason: "length"` regardless of budget size. Omitting the parameter entirely also works (the model will use its default limit).
- **Claude (when listed):** Use `max_tokens`, and it *must* be strictly greater than `budget_tokens` (e.g. `budget_tokens: 2048` requires `max_tokens: 2049` or higher).

### A. JavaScript with `manus-node` (every Manus computer)

Write a `.mjs` script, import the bundled client by absolute path with `pathToFileURL` (portable, including Windows drive paths), and run it with `manus-node "/absolute/path/script.mjs"`. The client sends the request body as-is: provider-specific keys (`reasoning`, `thinking`, `reasoning_effort`) go at the **top level** of the body.

#### A1. Basic chat

```js
import { pathToFileURL } from 'node:url'
const { LlmClient, messageText } = await import(pathToFileURL('<skill-dir>/lib/llm.mjs').href)

const llm = new LlmClient()
const resp = await llm.chat({
  model: 'gpt-5-mini',
  messages: [
    { role: 'system', content: 'You are a precise translator.' },
    { role: 'user', content: 'Translate to French: Good morning.' },
  ],
})
console.log(messageText(resp))
console.log(resp.usage.prompt_tokens, resp.usage.completion_tokens)
```

`new LlmClient({ timeoutMs, maxRetries })` defaults to a 300 s timeout and 3 retries. The client retries only transient failures (network errors, HTTP 408/409/429/5xx, proxy rate limits). Proxy errors can arrive as HTTP 200 with an `error` field; the client throws them as `LlmError`. `error.fatal` (runtime not ready, invalid session, insufficient credits, unsupported model, blocked user) means stop the whole batch and report it — retrying will not help.

#### A2. Thinking / reasoning (family-specific)

The catalog field `capabilities.thinking_param` tells you which key to send; the field `capabilities.thinking_example` gives the exact shape.

**1. OpenAI GPT-5 Series** (`gpt-5-nano`, `gpt-5-mini`, `gpt-5`, `gpt-5.5`)
Controls reasoning via the `reasoning.effort` parameter. If you pass Anthropic/Google `thinking` syntax, it is silently ignored.
```js
await llm.chat({
  model: 'gpt-5',
  messages: [{ role: 'user', content: 'Prove sqrt(2) is irrational.' }],
  max_completion_tokens: 2000, // Prevents reasoning from eating the output budget
  reasoning: { effort: 'high' }, // "minimal" | "low" | "medium" | "high"
})
```

**2. Google Gemini Series** (`gemini-3.1-pro-preview`, `gemini-3-flash-preview`)
Gemini always reasons by default (no explicit param needed). Optionally use `reasoning_effort: "low"|"medium"|"high"` to adjust reasoning intensity.
```js
await llm.chat({
  model: 'gemini-3.1-pro-preview',
  messages: [{ role: 'user', content: 'Prove sqrt(2) is irrational.' }],
  max_tokens: 16384, // MUST use max_tokens for Gemini (NOT max_completion_tokens)
})
```

**3. Anthropic Claude Series (only when listed in the live catalog)**
Sonnet/Opus 4.6-generation models require an explicit thinking budget; Opus 4.7 uses adaptive thinking and does not require thinking parameters.
```js
await llm.chat({
  model: '<claude model id from the live catalog>',
  messages: [{ role: 'user', content: 'Prove sqrt(2) is irrational.' }],
  max_tokens: 4000, // MUST be strictly > budget_tokens
  thinking: { type: 'enabled', budget_tokens: 2048 },
})
```

#### A3. Structured output (JSON schema) — preferred for extraction/analysis

All proxy models fully support OpenAI's `response_format` JSON Schema specification. **Required:** `strict: true` and `additionalProperties: false`.

```js
const resp = await llm.chat({
  model: 'gpt-5-mini',
  messages: [
    { role: 'system', content: 'Output JSON only.' },
    { role: 'user', content: 'My name is Alice and I am 30.' },
  ],
  response_format: {
    type: 'json_schema',
    json_schema: {
      name: 'person',
      strict: true,
      schema: {
        type: 'object',
        properties: { name: { type: 'string' }, age: { type: 'integer' } },
        required: ['name', 'age'],
        additionalProperties: false,
      },
    },
  },
})
const data = JSON.parse(messageText(resp))
```

#### A4. Vision (image input)

```js
import { readFile } from 'node:fs/promises'
const image = (await readFile('/absolute/path/photo.jpg')).toString('base64')
await llm.chat({
  model: 'gemini-3-flash-preview',
  messages: [{
    role: 'user',
    content: [
      { type: 'text', text: 'Describe this image.' },
      { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${image}`, detail: 'auto' } },
    ],
  }],
})
```
For remote images, pass the `https://` URL directly.

#### A5. Tool / function calling

```js
const resp = await llm.chat({
  model: 'gpt-5-mini',
  messages: [{ role: 'user', content: 'Weather in Tokyo?' }],
  tools: [{
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get weather for a city',
      parameters: { type: 'object', properties: { city: { type: 'string' } }, required: ['city'] },
    },
  }],
  tool_choice: 'auto',
})
// resp.choices[0].message.tool_calls -> execute -> append role:"tool" result -> call again
```

#### A6. Concurrent batch (the common case for bulk summarize/translate/analyze)

A ready-to-run batch driver is bundled. It reads lines or a JSON array, keeps output in input order, writes JSONL (`index`, `input`, `output`, `error`, `usage`), applies the family rules above, and stops early on fatal errors:
```bash
manus-node "<skill-dir>/scripts/llm_batch.mjs" --help
manus-node "<skill-dir>/scripts/llm_batch.mjs" --input items.txt --out out.jsonl \
  --model gpt-5-mini --workers 8 --template "Summarize in one sentence: {input}"
```
Options: `--system`, `--schema schema.json` (strict structured output), `--reasoning-effort minimal|low|medium|high`, `--thinking-budget N`, `--max-retries N`, `--timeout-seconds N`.

Minimal inline version:
```js
import { pathToFileURL } from 'node:url'
const { LlmClient, mapLimit, messageText } = await import(pathToFileURL('<skill-dir>/lib/llm.mjs').href)

const llm = new LlmClient()
const items = [/* inputs */]
let fatal
const results = await mapLimit(items, 8, async text => {
  if (fatal) return { text, output: null, error: 'skipped' }
  try {
    const resp = await llm.chat({
      model: 'gpt-5-mini',
      messages: [{ role: 'user', content: `Summarize in one sentence:\n${text}` }],
    })
    return { text, output: messageText(resp), error: null }
  } catch (error) {
    if (error.fatal) fatal = error
    return { text, output: null, error: error.message }
  }
})
if (fatal) throw fatal
```
Keep concurrency modest (4–10); the proxy rate-limits each user and the client already retries transient failures. Save large results to files in the working directory instead of printing them.

### B. Sandbox Python (optional, Sandbox only)

The SDK auto-reads `OPENAI_API_KEY` and `OPENAI_API_BASE`; just call `OpenAI()`. Request bodies are the same as section A, except that non-OpenAI keys (`reasoning`, `thinking`) go in `extra_body`; `reasoning_effort`, `max_tokens`, `max_completion_tokens`, `response_format` and `tools` are regular keyword arguments.

```python
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Prove sqrt(2) is irrational."}],
    max_completion_tokens=2000,
    extra_body={"reasoning": {"effort": "high"}},
)
print(resp.choices[0].message.content)
print(resp.usage.prompt_tokens, resp.usage.completion_tokens)
```

The Python batch driver accepts the same options as `llm_batch.mjs` except `--timeout-seconds`:
```bash
python3 "<skill-dir>/scripts/llm_batch.py" --help
```
With a thread pool, keep `max_workers` modest (4–10); the proxy rate-limits and the SDK already retries.

### C. Webdev project (TypeScript, server-side only)

Import from the scaffold's core helper. Credentials are injected by the platform (`BUILT_IN_FORGE_API_URL` / `BUILT_IN_FORGE_API_KEY`); never call from the client. Calls deduct project credits.

#### C1. Basic + list models

```ts
import { invokeLLM, listLLMModels } from "./server/_core/llm";

const { data } = await listLLMModels();         // discover IDs at runtime
const model = data.find(m => m.id.startsWith("gemini-"))?.id;

const res = await invokeLLM({
  model,                                          // optional; omit for default
  messages: [
    { role: "system", content: "You are helpful." },
    { role: "user", content: "Hello" },
  ],
});
const text = res.choices[0].message.content;
```

#### C2. Thinking / reasoning (forwarded unchanged)

```ts
await invokeLLM({
  model: "gpt-5",
  messages: [...],
  reasoning: { effort: "low" },
});
await invokeLLM({
  model: "<claude model id from the live catalog>",
  messages: [...],
  thinking: { type: "enabled", budget_tokens: 2048 },
});
```

#### C3. Structured output

```ts
const r = await invokeLLM({
  messages: [
    { role: "system", content: "Output JSON." },
    { role: "user", content: "name=Alice age=30" },
  ],
  response_format: {
    type: "json_schema",
    json_schema: {
      name: "person",
      strict: true,
      schema: {
        type: "object",
        properties: { name: { type: "string" }, age: { type: "integer" } },
        required: ["name", "age"],
        additionalProperties: false,
      },
    },
  },
});
// JSON.parse(r.choices[0].message.content)
```
The helper also accepts `outputSchema`/`output_schema` as a shorthand, plus `tools`, `toolChoice`, `maxTokens`. It retries non-2xx/network errors with exponential backoff internally.

#### C4. Streaming (not exposed by default)

`invokeLLM()` does not expose `stream`. If you truly need it, modify the helper to send `stream: true` and parse the SSE response. When proxying SSE, listen on the response object's close event (not the request) and guard with a `finished` flag, or the upstream gets aborted after the first event. Render markdown with `<Streamdown>{content}</Streamdown>` from `streamdown`.

### D. Raw HTTP (Sandbox only)

```bash
curl -s "$OPENAI_API_BASE/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-5-mini","messages":[{"role":"user","content":"ping"}]}'
```
Webdev path is `"$BUILT_IN_FORGE_API_URL/v1/chat/completions"` with `BUILT_IN_FORGE_API_KEY`. On a local computer or Cloud Computer, use the JavaScript client instead of raw HTTP.

## Troubleshooting

| Symptom | Likely Cause | Fix |
| --- | --- | --- |
| `Built-in LLM runtime is not ready` | Script not run with `manus-node`, or the Manus connection/runtime is outdated | Run with `manus-node` and an absolute script path; if it persists, report that the Manus runtime needs updating. Never supply credentials manually |
| `LLM proxy: Insufficient credits` | Account balance too low | Stop the batch and tell the user; do not retry |
| `LLM proxy: Unsupported model ...` | Model ID not in the live catalog | Re-run Step 1 and pick a listed ID |
| `LLM proxy: Rate limit exceeded` after retries | Too many concurrent requests | Lower concurrency (`--workers`) and re-run failed items |
| Gemini returns `content: null` + `finish_reason: "length"` | Used `max_completion_tokens` | Switch to `max_tokens` or omit the parameter |
| Claude returns 400 Bad Request | `max_tokens` <= `budget_tokens` | Set `max_tokens` strictly greater than `budget_tokens` |
| GPT output truncated with reasoning on | Used `max_tokens` with reasoning | Switch to `max_completion_tokens` for GPT |

## Files in this skill

- `lib/llm.mjs` — `LlmClient` (`models()`, `chat()`), `messageText()`, `mapLimit()`; runtime resolution, retries and credential redaction for every Manus computer.
- `scripts/models.mjs` — prints the live catalog.
- `scripts/llm_batch.mjs` — concurrent, retrying batch driver for every Manus computer.
- `scripts/llm_batch.py` — the same batch driver for Sandbox Python.
