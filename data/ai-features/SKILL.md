---
name: ai-features
description: This skill should be used when putting an LLM inside the product itself — a chatbot or support agent, AI-generated reports or summaries, classification, extraction, lead scoring, a WhatsApp or voice bot, or any feature where your code calls a model on behalf of your users. Trigger phrases (English) include "add AI to my app", "build a chatbot", "AI assistant for my users", "summarize with AI", "call the LLM API", "structured output", "the bot makes things up", "AI costs", "let users bring their own API key", "the model call times out". Trigger phrases (Spanish) include "agregar IA a mi app", "armar un chatbot", "un asistente con IA", "resumir con IA", "el bot inventa cosas", "cuánto me cuesta la IA", "que cada cliente ponga su API key". It decides who pays and with which credentials, what the model may decide versus what code must decide, and how to cap spend, ground answers and fail honestly. Not for using an AI coding agent to build the app — that is the rest of this plugin.
---

# AI Features

This skill covers the model as a **component of your product**: your server calls an LLM, your users see the result, and you get the invoice. It prevents the four ways this goes wrong: unbounded spend, invented facts, silent failures, and tests that pass while the feature is broken.

Analogy: the model is a brilliant temp worker with no memory of your business and no sense of what things cost. You don't hand them the company card and the customer list and leave. You give them a brief, a spending limit, a rule that says "if it's not in the file, say you don't know", and someone to call when they're stuck.

## Discovery (max 3 questions, only if unknown)

1. What does the model do — talk to end users, or produce something your code then uses (a score, a summary, a category)?
2. Who pays for the calls — you, or each customer with their own key?
3. Where does the call run — a serverless function, an automation tool, a long-lived server?

## Step 1 — Credentials and who pays (decide before writing code)

- **A product uses API keys, never a personal subscription.** Consumer plans (the kind you log into as a person) are licensed for individual use; routing your users' work through one — yours *or* theirs — is typically prohibited by the provider's terms and can be cut off without notice. Read the current terms of your provider before designing around a subscription.
- **Your key, you pay**: simplest. Price it into the plan and enforce a quota (Step 4).
- **Bring-your-own-key**: each customer pastes their key. You owe them a ledger — cost per run, per model — and their key is a secret you now store (server-only table, never returned to the browser).
- **One provider account per product**, with a low-balance alert. A balance shared across projects ran dry and took a production bot down with a payment-required error; a "workspace" inside one account did not separate the balance.
- **Keep the provider swappable**: one module wraps the call (base URL, key, model from config). You will change models more often than you expect.

## Step 2 — Code decides, the model judges

**Anything that can be computed is computed.** Counting, totals, dates, matching a record, applying a rule, choosing which image to send: code or SQL. The model gets the result and writes the sentence around it.

Why this is a rule and not a preference:
- A model treats a tool call that does not change what the user reads as optional. Asked to record buying signals as a side effect, one bot logged 3 across 106 real messages. A database trigger with tested rules replaced it.
- A model wrote one lead's summary using the name from a different row, and reported a "cost per sale" where there was no spend.

So: **validate what comes back before you store it** — types (the string `"false"` is truthy), enums, ranges, that every id it cites exists in the input. Where the output makes a claim, make it cite the record that supports it, and check the citation.

## Step 3 — Grounding

- **State the boundary explicitly**: "If it is not in the data below, you do not know it. Say so." Without that line the model fills every gap: a bot told a customer the batteries were lithium (the record did not say; they were not).
- **For every new field you add to the context, add what must not be inferred from it.**
- **Remove data you don't want weighed.** An instruction to ignore a line loses to the line itself. A classifier kept routing to sales because of one context line it had been told to disregard; deleting the line fixed it, rewording the instruction did not.
- **If you truncate the context, say how much was cut**, or the model reasons as if it saw everything.

## Step 4 — Spend control

Every paid call goes through the same four gates, **all on the server**:

1. **Reserve before you call.** Take a row-level "turn" in the database first. Two simultaneous requests both passed a check that only looked at finished reports — and both were billed.
2. **Enforce the quota where the call happens.** A plan limit checked only in the browser is a suggestion.
3. **Cap by day, by hour per user, and in money**, and decide what happens at the cap — usually: stop calling, tell the user, hand off to a person. Without caps, 300 inbound messages are 300 paid calls.
4. **Never retry a paid call automatically.** Retry only when the user asks, and make the retry idempotent: a timeout that left "interrupted" on screen charged again on every click.

Record the real cost from the provider's `usage` response, not an estimate — and treat a missing value as unknown, not zero. On serverless, write that record with the platform's post-response hook (`after()` in Next.js, `waitUntil` elsewhere): work started after the response is sent is frozen, and one app was silently missing about 8% of its spend records.

## Step 5 — Fail honestly

The provider will be overloaded, slow, or down. Design the failure first:

- **Tell the user**, in plain words, that the assistant could not answer. Silence reads as being ignored.
- **Record an event with the real error**, so someone finds out without watching the screen.
- **Hand off to a human** where one exists, and don't repeat the apology on every message.
- **An empty or error result is not "nothing to report".** A failed run must not render as "0 items".
- **Budget the whole timeout chain.** Your timeout, the function limit, the caller's HTTP timeout: the shortest wins. Measure latency from where the code runs, with the production prompt, end to end — and before blaming a timeout, check whether the call is actually stuck (Step 6).
- **To test a hang, use a server that accepts the connection and never answers.** A bad API key fails in milliseconds and tests nothing.

## Step 6 — Structured output

- Ask for structure through the provider's schema or tool mechanism, then **validate it yourself anyway**.
- If structured output hangs or pads until the token limit, request the same schema as a **forced tool call** instead, and prove the fix by repeating the identical call many times — one success is not evidence.
- Through an aggregator, a response can be **HTTP 200 with the error in the body**, and a response cut off at the token limit can carry empty content. Check the body and the finish reason, not the status. If the aggregator picks the upstream provider per call, pin it: not every upstream supports every feature.
- Keep schemas small; providers limit union and nullable fields in ways the docs understate.

## Step 7 — Conversations

- **Wait a few seconds and batch.** People send three short messages in a row; answering each produces repeated questions and triples the cost.
- **Deduplicate by the platform's message id** — webhooks arrive twice.
- **Don't let the bot score itself**: filter its own messages out of any analysis.
- **Prompt caching** has to be set deliberately (an explicit cache point on the stable prefix) and only applies above the provider's minimum length. Verify cache reads in `usage`; in one case this cut cost about six-fold, in another the prompt was too short and nothing was cached.

## Step 8 — Moving a prompt or agent between platforms

Diff it piece by piece. Units and names change silently: a memory window of "10" meant ten exchanges on one platform and ten messages on the next, so the bot forgot half the conversation; a history query fetched the oldest 200 instead of the newest; the prompt named tools that had been renamed.

## Step 9 — Test the light, not the switch

- **A test must import the production function.** A test that rebuilds the request by hand stays green while production is broken.
- **Validate the test by mutation**: break the code on purpose and confirm the test goes red.
- **Assert on the outcome the user sees.** One suite checked that a "bot paused" flag was false; nothing checked that the bot replied.

## Output

Deliver: the credentials decision with its reason, the wrapper module, the deterministic/model split for this feature, the spend gates (reservation, quota, caps, cost record) as real code, the failure path the user sees, the output validation, and one test that calls the production path. State the measured cost per call once you have one.

## Field notes

`references/field-notes.md` — the production failures behind each step, with what was observed.

## Reference

Your provider's API docs for tool use, structured outputs, prompt caching and usage reporting — read the current version; these features change between model releases. Pairs with `secure-coding` (the key is a secret), `payments` (pricing the quota into plans), `integrations` (webhooks and chat platforms) and `api-design` (idempotency).
