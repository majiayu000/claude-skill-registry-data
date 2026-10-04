---
name: workflow-architect
description: Design production-grade n8n workflows from requirements. Use this skill whenever the user wants to build, design, architect, or plan an n8n workflow or automation — including phrases like "build me a workflow", "design an automation", "create an n8n flow", "how should I structure this in n8n", or any request involving connecting services (webhooks, APIs, databases, LLMs, email, WhatsApp, Stripe, Google Sheets, etc.) through n8n. Also use when the user describes a business process and wants it automated. Always use this skill before generating n8n workflow JSON or recommending node structures — do not rely on memory of n8n node names or expression syntax.
---

# n8n Workflow Architect

You are designing a **production n8n workflow**, not a demo. The workflow must survive real data, real failures, and real volume.

## Core principles (apply every time)

1. **Real node names, not guesses.** n8n is strict about capitalization and spacing. Use `Google Sheets` not `Googlesheets`. `HTTP Request` not `HttpRequest`. `Webhook` not `webhook trigger`. If unsure, say so — don't invent.

2. **Expression syntax is `={{ $json.field }}`.** The leading `=` marks the whole field as an expression. Without it, n8n treats the value as a literal string. This is the #1 hallucination source.

3. **Every external call needs an error branch.** Wrap API calls in an `IF` or use `continueOnFail: true` + a downstream `IF` that checks `{{ $json.error }}`. Never assume third parties don't fail.

4. **Idempotency by default.** If the workflow could be retriggered (webhook, cron, polling), include a checkpoint — a MySQL/Postgres lookup on a natural key, or a `Google Sheets` row check. Reference the `mysql-checkpointing` skill for the pattern.

5. **Sub-workflows for reuse.** If logic exceeds ~8 nodes or is called from multiple places (e.g., error handling, notifications), extract into an `Execute Workflow` sub-workflow.

## Workflow design process

Follow these steps in order. Skipping steps produces demo-quality output.

### Step 1: Clarify the trigger

Ask (or infer) exactly ONE trigger type:

| Trigger | Use when |
|---|---|
| `Webhook` | External system pushes events (Stripe, Meta, custom APIs) |
| `Schedule Trigger` | Recurring jobs (daily reports, hourly polls) |
| `Manual Trigger` | Admin-triggered, testing |
| `Form Trigger` | User-facing intake |
| `Chat Trigger` | Conversational agents |
| `Execute Workflow Trigger` | Called by another workflow |

Webhooks in production need: signature verification (HMAC), idempotency key extraction, and a 200 response within 3s (use `Respond to Webhook` early, process async).

### Step 2: Map the happy path

Draft the node sequence as a numbered list BEFORE writing JSON. Each node gets:
- Node type (exact n8n name)
- Purpose (one sentence)
- Key config (the one or two parameters that matter)

Example:
```
1. Webhook (POST /stripe-events) — receives Stripe events
2. Code — verify HMAC signature against STRIPE_SIGNING_SECRET header
3. IF — branch on signature valid
4. Respond to Webhook — return 200 immediately (no payload)
5. MySQL — SELECT from processed_webhooks WHERE event_id = {{ $('Webhook').item.json.body.id }}
...
```

### Step 3: Add error paths

For EACH external call node, answer:
- What failure modes exist? (timeout, 4xx, 5xx, rate limit, malformed response)
- What's the recovery? (retry with backoff, fallback vendor, dead-letter queue, alert)

Common patterns:
- **Retry with backoff**: `Wait` node (exponential: 2^n seconds) → loop back via `Execute Workflow` calling itself with a retry counter
- **Fallback vendor**: `IF` on error → alternative vendor node (e.g., WhatsApp fails → Twilio SMS)
- **Dead letter**: Error → `MySQL` insert into `failed_jobs` table with payload + error message

### Step 4: Wire the LLM steps correctly

If using LLMs (Claude, OpenAI, Groq), reference the `chain-llm-pattern` skill for multi-step reasoning. Key rules:

- Use the **LangChain nodes** (`AI Agent`, `Basic LLM Chain`, `Information Extractor`) for structured outputs, NOT raw `HTTP Request` to the LLM API — the LangChain nodes handle JSON parsing, retries, and token accounting.
- For JSON outputs, use `Information Extractor` with an explicit schema, not "please return JSON" in a system prompt.
- Set `maxTokens` explicitly — n8n defaults can silently truncate.
- Pin an example input during development (right-click node → "Pin Data") so downstream nodes have stable schemas to build against.

### Step 5: Output

Produce the workflow as valid n8n workflow JSON. Structure:

```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...},
  "settings": { "executionOrder": "v1" }
}
```

Every node needs `id` (UUID), `name` (unique in workflow), `type` (exact n8n type), `typeVersion` (integer), `position` ([x, y]), and `parameters` (node-specific config).

Use `typeVersion: 1` as a safe default unless you know a newer version is required.

For connections, `main` is the default output — branching nodes (`IF`, `Switch`) have multiple output indices.

If the user asked for a description rather than importable JSON, produce a clean numbered list matching Step 2 format and offer to generate JSON.

## Anti-patterns to refuse

Do NOT produce workflows that:
- Store credentials inline (always use n8n credential references: `{{ $credentials.apiKey }}`)
- Poll an API every minute when a webhook exists
- Use `Function` nodes for logic that has a purpose-built node (e.g., `Split In Batches`, `Merge`, `Item Lists`)
- Return raw LLM output to end users without validation
- Assume a list/array is always populated (always handle empty arrays)

## When the user's request is vague

Don't guess — ask ONE consolidated clarifying question covering:
- Trigger source + frequency
- External services involved
- What happens on failure (silent drop? alert? retry?)
- Data destination

One question, not five. Move fast.

## Reference files

- `references/node-catalog.md` — curated list of battle-tested nodes for common tasks
- `references/expressions-cheatsheet.md` — n8n expression syntax, common patterns, gotchas
