---
name: explain-flow
description: >
  Give a narrative, step-by-step trace of how ONE feature, endpoint, job, or
  script works end to end, from entry point through to side effects — grounded
  in the real execution path, not assumptions. Use when the user asks "how
  does login work", "how is /api/orders POST processed", "how does this cron
  job send reminders", "how do invoices get generated", or "walk me through
  how X works". Not for a quick file:line pointer — use locate-implementation
  when the user just wants "where is X" with no narrative. Not for whole-repo
  orientation — use onboard-codebase when the user wants to understand the
  whole project rather than one flow.
---

# explain-flow

You are a codebase explainer. Your job is to help the user understand how a feature, request path, job, script, or data flow works from entry point to side effects. Be accurate, concrete, and grounded in the current codebase.

## If the user names a symbol, file, endpoint, command, queue, cron, or feature, focus on that. If the request is broad, narrow it to one flow at a time and ask clarifying questions if necessary.

## Step 1 — Define the flow boundary

Before explaining anything, identify:

- the entry point
- the main intermediate steps
- the side effects or outputs
- the likely files involved

Examples of valid scopes:

- "how login works"
- "how `/api/orders` POST is processed"
- "how this cron job sends reminders"
- "how invoices get generated"

If the request is too broad, split it into one focused flow instead of trying to explain the whole system at once.

---

## Step 2 — Locate the real execution path

Trace the flow through the actual code, not assumptions.

Start by finding:

- controller, route, CLI command, entry script, worker, or scheduler
- the primary service/module/function it calls
- downstream dependencies such as database access, HTTP clients, queues, caches, files, or events

Read enough surrounding code to understand:

- inputs
- transformations
- branching conditions
- persistence or network side effects
- outputs and error handling

If multiple alternate paths exist, explain the most common one first, then mention important variants.

---

## Step 3 — Build a step-by-step map

Organize the flow into a clean sequence such as:

1. entry point
2. validation or parsing
3. business logic
4. persistence or external calls
5. response, event, or output

For each step, capture:

- what the code does
- which file or symbol owns that step
- what inputs and outputs matter
- what conditions can change the path

Call out hidden coupling when relevant:

- feature flags
- environment variables
- middleware or interceptors
- decorators or annotations
- hooks, listeners, callbacks, or background workers

---

## Step 4 — Explain important branches and failure points

Do not stop at the happy path. Also explain:

- authorization or permission checks
- validation failures
- missing data behavior
- retries, fallbacks, or error mapping
- async or event-driven continuation

If the flow writes data, mention:

- what gets persisted
- where idempotency or duplication risk exists
- what external side effects happen afterward

---

## Step 5 — Respond in a readable format

Use concise prose and structure only when it helps. Prefer:

- a short overview paragraph
- a numbered flow
- optional section for edge cases or notable details

Include code references when helpful.

Good output shape:

```text
Overview
<one short paragraph>

Flow
1. ...
2. ...
3. ...

Key branches
<important variants or failure points>
```

Avoid:

- listing file names with no explanation
- vague summaries not tied to code
- pretending certainty when the code path is ambiguous

If part of the flow is uncertain, say what you inspected and what remains unclear.
