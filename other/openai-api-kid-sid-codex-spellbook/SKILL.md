---
name: openai-api
description: Build against the OpenAI API with current model selection, Responses API patterns, Codex model guidance, streaming, structured outputs, retries, and key management. Use when integrating OpenAI or Codex models into an app, service, CLI, or agent workflow.
---

# OpenAI API

Use the OpenAI API through the Responses API by default, choose models intentionally, and keep integration code explicit about validation, retries, and cost boundaries.

## When to Activate

- Add OpenAI API calls to an application or service
- Choose a model for coding, agentic, or general reasoning work
- Build a Codex-like coding workflow against the API
- Implement streaming or tool-calling behavior
- Add structured outputs or schema validation
- Review API key handling, retries, or rate-limit behavior
- Refactor an older Chat Completions integration to a newer pattern

## Model Selection

As of April 18, 2026, current official docs indicate:

- `gpt-5.4` is the flagship general model for complex reasoning and coding.
- `gpt-5.4-mini` is the lower-latency lower-cost GPT-5.4 variant.
- `gpt-5.3-codex` is the current most capable agentic coding model for Codex-like environments.
- `codex-mini-latest` is optimized for the Codex CLI; the docs recommend starting with `gpt-4.1` for direct general API use of that class.

Sources:

- https://developers.openai.com/api/docs/models
- https://developers.openai.com/api/docs/models/gpt-5.3-codex
- https://developers.openai.com/api/docs/models/codex-mini-latest

| Need | Start With | Notes |
| --- | --- | --- |
| General app logic, strong reasoning, coding | `gpt-5.4` | Best default when quality matters most |
| Lower latency or cheaper general workloads | `gpt-5.4-mini` | Good cost/perf default |
| Agentic coding in Codex-like workflows | `gpt-5.3-codex` | Supports reasoning effort settings |
| Codex CLI tuning reference | `codex-mini-latest` | CLI-oriented, not the default general API pick |

## API Surface

| Situation | Preferred | Avoid |
| --- | --- | --- |
| New integrations | Responses API | Starting new work on legacy patterns by default |
| Need multimodal, tools, or stateful interaction | Responses API | Rebuilding these features manually |
| Existing stable legacy integration | Migrate deliberately | Blind rewrites with no regression plan |

## Basic Integration Pattern

Python

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5.4",
    input="Summarize the migration risks in this schema diff.",
)

print(response.output_text)
```

TypeScript

```ts
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const response = await client.responses.create({
  model: "gpt-5.4",
  input: "Summarize the migration risks in this schema diff.",
});

console.log(response.output_text);
```

## Structured Outputs and Validation

| Pattern | Preferred | Avoid |
| --- | --- | --- |
| Model output consumed by code | Validate against a schema | Trusting free-form text blindly |
| App workflow branching on model output | Use explicit enums or tagged objects | Parsing ad hoc phrases |
| External input to model | Normalize before sending | Passing raw unbounded payloads |

BAD

```ts
const result = await client.responses.create({ model: "gpt-5.4", input });
const action = result.output_text;
if (action.includes("approve")) {
  // ...
}
```

GOOD

```ts
const result = await client.responses.create({
  model: "gpt-5.4",
  input,
  text: {
    format: {
      type: "json_schema",
      name: "review_action",
      schema: {
        type: "object",
        additionalProperties: false,
        properties: {
          action: { type: "string", enum: ["approve", "reject"] },
          reason: { type: "string" }
        },
        required: ["action", "reason"]
      }
    }
  }
});
```

## Coding Workflows and Reasoning

| Use Case | Model | Reasoning |
| --- | --- | --- |
| Deep repo analysis or multi-step coding | `gpt-5.3-codex` | Start with `medium`; raise to `high` only when needed |
| Small coding helpers or edits | `gpt-5.4-mini` or `gpt-5.3-codex` | `low` or `medium` |
| Non-coding product logic | `gpt-5.4` | Match latency budget |

Rules:

- Increase reasoning only when correctness gains justify the latency.
- Keep prompts concrete: files, constraints, output shape, failure modes.
- For coding agents, provide repository context and clear acceptance criteria.

## Keys, Retries, and Limits

| Concern | Rule |
| --- | --- |
| API key | Load from environment or secret manager |
| Retries | Retry transient 429/5xx responses with backoff and jitter |
| Idempotency | Make caller-side operations safe before automatic retries |
| Logging | Log request IDs, latency, model, and token usage; do not log secrets |

BAD

```python
client = OpenAI(api_key="sk-live-real-key")
```

GOOD

```python
client = OpenAI()
```

## Checklist

- [ ] Model choice matches the workload, latency, and cost target
- [ ] New integrations use the Responses API by default
- [ ] Structured outputs are validated before application logic consumes them
- [ ] API keys come from environment or secret management
- [ ] Retries are limited to transient failures with backoff
- [ ] Logs capture request identifiers and usage without leaking secrets
- [ ] Coding workflows provide files, constraints, and acceptance criteria explicitly
