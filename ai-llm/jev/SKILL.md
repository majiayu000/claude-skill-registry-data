---
name: jev
description: "TypeSafe AI's Jev System One model for typed software decisions: Choice/Score/Noul question primitives, state design, confidence gating, the direct api.typesafe.ai /v1/systemone API, typesafe-sdk (Python) and @typesafe-ai/sdk (JS), Cloudflare Workers AI typesafe/jev (binding, REST, AI Gateway), Vercel AI Gateway/OpenRouter/LiteLLM routes, errors incl. 401-vs-403, limits, pricing, Jev 1.13 weaknesses, prompt-injection risk. WHEN: \"jev\", \"Jev 1.13\", \"TypeSafe\", \"typesafe.ai\", \"typesafe/jev\", \"System One\", \"systemone\", \"system_one\", \"typesafe-sdk\", \"@typesafe-ai/sdk\", \"Noul\", \"jev-latest\". Do NOT use for prompt-injection threat modeling (ai-security), MCP servers (mcp), agent loops (claude-agent-sdk, openai-agents-sdk, google-adk), harness config (claude-code, codex), generic OpenRouter/Bedrock routing (inference-providers), LLM-judge grading (evals), or Lightbend's Typesafe/Scala."
license: MIT
---

# Jev (TypeSafe AI)

Jev is TypeSafe AI's hosted "System One" model. You send it one `state` plus a map of typed questions, and it returns typed answers with calibrated probabilities that your code acts on. It does not generate text. This skill covers choosing primitives, calling jev on every documented transport, handling failures and cost, and designing around its weaknesses.

## Volatility rule

Jev launched into waitlisted early access on 2026-09-15. Every fact here is a snapshot as of **2026-09-23**. This includes aliases, SDK versions, prices (which the vendor says may be subsidised), rate limits (which "can change without notice"), and gateway surfaces (several of which are `alpha` or `experimental_`).

- Always re-check the cited URL before you commit a price, limit or model id to config.
- Never state a figure this skill marks **unconfirmed**. Say it is unconfirmed and point to the source to check.

## Routing

| Request | Load |
|---|---|
| Field-level schemas, limits per primitive, structured JSON in questions, answer shapes, confidence | `references/primitives-and-schemas.md` |
| Raw HTTP, Python `typesafe-sdk`, JS `@typesafe-ai/sdk`, env vars, `RetryPolicy`, Vercel/OpenRouter/LiteLLM routing | `references/api-and-sdks.md` |
| `env.AI.run('typesafe/jev')`, Cloudflare REST, Cloudflare AI Gateway, Cloudflare billing and token scope | `references/cloudflare-workers-ai.md` |
| Fan-out, confidence routing, composite scoring, intent routing, hybrid with an LLM, TypeSafe's own agent skill | `references/patterns.md` |
| Jev 1.13 failure modes, prompt injection, tool-call gating, privacy, DPA, MCA, Trust Center, SLA | `references/limitations-and-security.md` |
| Cost estimate, 64k/32k limits, rate limits, full error table, 401-vs-403 defect, retry defaults | `references/pricing-limits-errors.md` |
| "jev vs OpenAI structured outputs / BAML / Instructor / Outlines / AutoTrain", integrations, who makes it | `references/ecosystem-and-alternatives.md` |
| Model aliases, SDK release history, breaking changes | `references/versions/jev-1.13.md` |

## Mental model

- **One call** carries one `state` and N named questions. All questions are evaluated **in parallel and in isolation** against the same state, and answers come back keyed by name.
- **Output is data.** You get a choice, a score or a probability plus a distribution. There is no text, no explanation and nothing to parse.
- **Text-only input.** State is a string, a JSON object or an array. English gets the best accuracy. Other languages are accepted with lower accuracy, so test them first.
- **No customization surface.** jev cannot be fine-tuned or LoRA-adapted. You steer it with the wording of `state`, `instructions` and `criteria`.
- **Design rule** from TypeSafe: "Keep code in control; use AI only for narrow, structured decisions." Control flow, arithmetic, dates and thresholds live in your code, and jev answers atomic judgments inside it.

Always put related facts in `state` and the judgments in `questions`. Never embed the question inside the state.

## Choosing a primitive

| Need | Primitive | Request | Response | Hard limit |
|---|---|---|---|---|
| One option from an unordered set | **Choice** | `criteria`: `{option: description}` | `choice`, `probabilities`, `confidence` | ≤ 255 options |
| A position on an ordered rubric | **Score** | `criteria`: `[level0, level1, ...]`, lowest first | `score` (can be fractional), `probabilities`, `legend`, `confidence` | 2–10 levels |
| Yes/no | **Noul** | `criteria` optional: `{true, false}` | `noul` (P(yes), 0–1) and **no `confidence`** | — |

You can mix primitives freely in one request.

- **Choice for categories, Score for degree, Noul for one condition.** Pick by the shape of the answer your code branches on.
- **Always include an `"other"` / `"none of the above"` option** in a Choice when the taxonomy may be incomplete. Otherwise jev must force-fit.
- **Always give the complete taxonomy**, not a shortlist.
- **Write Score levels as concrete situations** ("Broken or degraded feature, but workaround exists"). Never use bare numbers or relative wording like "worse than previous", because each level is judged independently.
- **Keep one dimension per Score and one condition per Noul.** Split "angry AND wants a refund" into two Nouls.
- **Treat Noul 0.5 as uncertainty.** It never means "medium".
- **Use Score to threshold or rank.** Never interpolate a magnitude from it: Jev 1.13 has "weak numerical calibration" between levels.
- **Normalize Score** with `score / (len(criteria) - 1)` before you weight dimensions in code.
- **Use structured JSON in `instructions` or `criteria`** (objects such as `{what, not_for, examples}`) when options need scope boundaries or the source data is already structured.
- **Validate limits client-side.** The published JSON Schema enforces only Score `minItems: 2`. The 255-option and 10-level maxima exist only in prose.

## Designing state and questions

- **Filter state to what the decision needs.** Irrelevant context lowers accuracy and costs input tokens, which are the only tokens billed.
- **Ask the question you mean, literally.** Jev reads scoping words and negations exactly, and it will not infer unstated intent.
- **Never ask jev to count, calculate or compare dates.** Compute these in code, then ask a Noul or Choice about the *result*.
- **Avoid multi-hop questions** ("properties of properties"), double negatives, and instructions that contradict their criteria.
- **Fan out speculatively.** Extra questions in the same call barely change latency, so ask every question you might need and read only the relevant answers.
- **Never assume cross-question consistency.** Jev does not guarantee P(X) + P(not X) = 1. Check invariants in code if they matter.
- **Keep all question definitions and thresholds in one reviewed module.** Question wording is production logic.

## Reading answers and gating actions

"The answer tells you what; confidence tells you whether to act."

The vendor's starting bands, which you should tune on your own data:
- **> 0.9**: act automatically.
- **0.5–0.9**: confirm or flag for review.
- **< 0.5**: route to a human or ask for clarification.

For Choice, the primitive page suggests a review threshold around 0.3–0.5.

- **Scale thresholds with consequence.** Use one low floor for genuine uncertainty, then higher, action-specific bars for destructive actions. Example: in the voice-banking pattern, a balance check executes at ≥ 0.6, while a transfer needs confirmation at 0.6–0.85 and executes only above 0.85.
- **Inspect `probabilities`, not just `score`.** Identical scores can come from different distributions.
- **Never retry to "fix" an answer.** Jev does not revise the way an LLM does, so a validator retry loop tends to return the same answer and burn its budget. Change the question or escalate instead.
- **Log state, question schema, option order, `response.model` and confidence together** for every consequential decision.

## Calling jev: pick a transport

| Transport | Endpoint / call | Credential | Model id |
|---|---|---|---|
| Direct HTTP | `POST https://api.typesafe.ai/v1/systemone` | `Authorization: Bearer $TYPESAFE_API_KEY` | `"model"` **inside** the body: `jev-latest` or `jev-1.13.0` |
| Python | `pip install typesafe-sdk` (Py ≥ 3.10); `TypeSafeClient().system_one(...)` | `TYPESAFE_API_KEY` | default `jev-latest` |
| JS/TS | `npm install @typesafe-ai/sdk` (Node ≥ 20); `new TypeSafeClient().systemOne(...)` | `TYPESAFE_API_KEY` | default `jev-latest` |
| Cloudflare Worker | `env.AI.run('typesafe/jev', {state, questions})` | the `AI` binding | `typesafe/jev` |
| Cloudflare REST | `POST .../accounts/$ID/ai/run`, body `{"model": "typesafe/jev", "input": {...}}` | CF token with Workers AI Read + Edit | `typesafe/jev` in the **body** |
| Vercel AI Gateway | SDK `baseURL` = `https://ai-gateway.vercel.sh/typesafe` | AI Gateway key / OIDC | see ref |
| OpenRouter / LiteLLM | see `references/api-and-sdks.md` | provider key | differs by route |

Direct:
```bash
curl -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" -H "Content-Type: application/json" \
  -d '{"state":"I have asked three times now. Can I please just talk to a real person?","model":"jev-latest",
       "questions":{"is_human_escalation":{"type":"noul","instructions":"Is the customer asking for a human agent?"}}}'
```

Python:
```python
from typesafe_sdk import Choice, TypeSafeClient

with TypeSafeClient() as client:
    r = client.system_one(
        state="My running shoes arrived in the wrong size. Can I swap them for a size 10?",
        questions={"department": Choice(
            instructions="Which team should handle this?",
            criteria={"returns": "Exchanges, wrong or damaged items",
                      "shipping": "Delivery status, delays, lost packages",
                      "billing": "Charges, invoices, payment problems"})},
    )
    ans = r.answers["department"]          # .choice, .confidence, .probabilities
```

TypeScript:
```ts
import { choice, TypeSafeClient } from "@typesafe-ai/sdk";
const client = new TypeSafeClient();
const res = await client.systemOne({
  state: { document: "I was charged twice. Please fix this ASAP." },
  questions: { category: choice("What is this ticket about?", { billing: null, technical: null, other: null }) },
});
res.answers.category.choice; // typed from the questions map
```

Cloudflare REST: the model id goes in the body, never the path.
```bash
curl https://api.cloudflare.com/client/v4/accounts/$CLOUDFLARE_ACCOUNT_ID/ai/run \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" \
  -d '{"model":"typesafe/jev","input":{"state":"...","questions":{"q":{"type":"noul","instructions":"..."}}}}'
```

Transport directives:
- **Never put `model` inside the Cloudflare payload.** Its schema has `additionalProperties: false` and no `model` field. On the direct API, `model` is required in the body.
- **Never append `typesafe/jev` to the Cloudflare URL path.** The path form (`.../ai/run/@cf/...`) is for first-party `@cf/` models.
- **For Cloudflare AI Gateway, use the universal `/ai/run`** (binding option `{ gateway: { id } }`). No source says the OpenAI- or Anthropic-compatible routes accept jev.
- **Never set `dangerouslyAllowBrowser: true`** in the JS SDK for production. It exposes the key client-side.
- **The Vercel AI SDK provider reads `TYPESAFE_AI_API_KEY`**, not `TYPESAFE_API_KEY`, and its `experimental_evaluate` is unstable.
- **Do not plan for streaming.** No transport documents it, and LiteLLM and the AI SDK provider explicitly do not support it.
- **Use the Python SDK at ≥ 0.7.1.** Earlier versions could leak the key into logged exceptions.
- **Never assume parity between the two SDKs.** JS is at 0.6.0 with no 0.7.x equivalent yet.
- **Score `criteria` is a list in SDK ≥ 0.6.0** (it was a dict before).

## Errors and retries

| Status | Meaning | Handle |
|---|---|---|
| 400 / 422 | Bad request or validation failure (question shape, criteria) | Fix the payload. Never retry. |
| **401** | **Invalid** key | Fix or rotate the key. |
| **403** | **Missing** key. This is **observed**; the docs say 401 (defect typesafe-ai/skills#8, open). | Treat it as a credential error. |
| 429 | Rate limited; `retry_after_ms` / `retryAfterMs` | Back off. The SDK retries. |
| 529 / 5xx | Overloaded or server failure | Exponential backoff. Circuit-break if it persists. |
| none | Connection error or timeout | Retried by default. Check the timeout budgets. |

- **Always catch both the 401 and 403 classes** (`TypeSafeAuthenticationError` + `TypeSafePermissionDeniedError`, or JS `AuthenticationError` + `PermissionDeniedError`) when checking credentials. You can also branch on `body.error_type == "authentication_error"`. Catching only `AuthenticationError` misses the missing-key case.
- **The SDK retry defaults are sane**: 2 retries, 0.5 s → 5 s backoff, statuses {408, 429, 500–599}, and `Retry-After` honoured. Python adds a 30 s total budget over its 10 s per-attempt timeout. JS has a 10 s per-attempt timeout and no total budget.
- **Quote `request_id` / `requestId` to support.** It comes from the `x-typesafe-request-id` header.

## Limits and pricing

| Item | Value |
|---|---|
| Context | **64k tokens per request**, with a nested **32k** limit for `state` + the longest single question. Cloudflare's "32,000" is the inner limit. |
| Rate limit (direct) | 250,000 tok/s and 1,200 req/min, "adjusting dynamically". Handle 429s; never hardcode these. |
| Price (direct) | **$0.042 / 1M input tokens. Output is free.** No free tier is documented. |
| Cloudflare price and billing path | **Unconfirmed.** Neither Unified Billing nor Workers AI Neurons is documented for jev. Check the Cloudflare dashboard. |
| Cloudflare rate limit for jev | **Unconfirmed.** |
| SLA | None. `status.typesafe.ai` is informational only. |

Question text and state are both billed input, so shorter criteria and filtered state reduce cost directly.

## Security: jev is not a security boundary

- **Prompt injection moves verdicts, and the vendor acknowledges it.** In a press-reported reproduction, a fake "pre-approved" tool-output field dropped the block probability for `rm -rf ~/.ssh` from 0.76 to 0.48. Never make jev the sole gate on a destructive or privileged action. Pair it with deterministic checks and human approval.
- **When gating tool calls, exclude tool output from `state`.** LangChain's middleware does this so fetched content "cannot authorize its own execution".
- **Gating discloses.** The tool-call arguments reach TypeSafe before the verdict returns, even when the call is refused. Strip secrets and regulated PII from `state` first.
- **Option order is input.** Reordering an enum or `Literal` can change the answer, so fix the order and test several orderings before you deploy.
- **Never use one jev setup as both gate and grader.** One injection can fool both layers.
- **Pin `jev-1.13.0` for audited decisions.** `jev-latest` and Cloudflare's `typesafe/jev` can roll forward.
- For threat modelling and defence-in-depth design, hand off to `ai-security`.

## Data and legal quick facts

- **No training on input** (privacy policy and MCA). Retention is purpose-bound with no fixed period. The DPA commits to breach notice within 72 hours and uses SCCs.
- **Zero data retention** is enterprise-only and on request (`privacy@typesafe.ai`).
- **Trust Center (`trust.typesafe.ai`) could not be fetched.** Never claim SOC 2, ISO 27001 or any other certification for TypeSafe. Tell the user to check the Trust Center directly.
- **The MCA governs API use; the site Terms of Use do not.** The MCA forbids training a model to imitate jev output (no distillation). Its liability cap is the greater of 12 months' fees or $50.
- **Cloudflare route**: Cloudflare does not train on or persist content by default. No source says whether TypeSafe's terms apply identically to Cloudflare-routed requests.
- **Not Lightbend.** TypeSafe AI has no relation to Lightbend's former Typesafe (Scala/Akka).

## Scripts

- `scripts/smoke-test.sh direct|cloudflare` sends one three-primitive request and prints the raw body and HTTP status. **Requires `TYPESAFE_API_KEY`, or `CLOUDFLARE_ACCOUNT_ID` + `CLOUDFLARE_API_TOKEN`, and spends real tokens.** Run it first when a user reports auth or shape errors, to separate credential and transport problems from question-design problems.

## References

- `references/primitives-and-schemas.md`: request/response tables per primitive, JSON Schemas, structured content, confidence.
- `references/api-and-sdks.md`: HTTP, both SDKs, config precedence, retry tables, gateway routes.
- `references/cloudflare-workers-ai.md`: binding, REST envelope, AI Gateway, unconfirmed billing and limits, token scope.
- `references/patterns.md`: the four official patterns, hybrid-LLM patterns, TypeSafe's own agent skill.
- `references/limitations-and-security.md`: the nine jaggedness modes, injection evidence and mitigations, privacy/DPA/MCA.
- `references/pricing-limits-errors.md`: cost math, the full limits table, the unified error table.
- `references/ecosystem-and-alternatives.md`: integrations, community tools (unverified), alternatives compared.
- `references/versions/jev-1.13.md`: model aliases and the SDK release tables.

## Sources

- https://typesafe.ai
- https://docs.typesafe.ai/introduction.md
- https://docs.typesafe.ai/concepts/state.md
- https://docs.typesafe.ai/concepts/how-to-build-with-system-one.md
- https://docs.typesafe.ai/primitives/choice.md
- https://docs.typesafe.ai/primitives/score.md
- https://docs.typesafe.ai/primitives/noul.md
- https://docs.typesafe.ai/primitives/advanced.md
- https://docs.typesafe.ai/confidence.md
- https://docs.typesafe.ai/patterns/confidence-routing.md
- https://docs.typesafe.ai/api.md
- https://docs.typesafe.ai/models.md
- https://docs.typesafe.ai/model-jaggedness/jev-1.13.md
- https://docs.typesafe.ai/sdk/python.md
- https://docs.typesafe.ai/sdk/python/api/retries.md
- https://docs.typesafe.ai/sdk/python/api/exceptions.md
- https://docs.typesafe.ai/sdk/javascript.md
- https://docs.typesafe.ai/sdk/javascript/api/interfaces/TypeSafeClientConfig.md
- https://docs.typesafe.ai/sdk/javascript/api/classes/APIError.md
- https://github.com/typesafe-ai/skills/issues/8
- https://pypi.org/project/typesafe-sdk/
- https://registry.npmjs.org/@typesafe-ai/sdk
- https://developers.cloudflare.com/ai/models/typesafe/jev/
- https://developers.cloudflare.com/ai/models/typesafe/jev/schema-input.json
- https://developers.cloudflare.com/workers-ai/get-started/rest-api/
- https://developers.cloudflare.com/ai-gateway/usage/rest-api/
- https://developers.cloudflare.com/ai-gateway/features/unified-billing/
- https://vercel.com/docs/ai-gateway/sdks-and-apis/typesafe
- https://ai-sdk.dev/providers/ai-sdk-providers/typesafe-ai
- https://docs.litellm.ai/docs/pass_through/typesafe
- https://pydantic.dev/docs/ai/models/typesafe/
- https://www.langchain.com/blog/building-a-harness-with-jev
- https://venturebeat.com/security/companies-are-putting-jev-in-charge-of-ai-agent-decisions-and-prompt-injection-can-influence-the-verdict (press)
- https://typesafe.ai/legal/mca
- https://typesafe.ai/legal/privacy-policy
- https://typesafe.ai/legal/data-processing
- https://trust.typesafe.ai/ (unfetchable; user must check directly)
- https://status.typesafe.ai

Fetched: 2026-09-23
