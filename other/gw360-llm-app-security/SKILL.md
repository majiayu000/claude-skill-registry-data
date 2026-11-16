---
name: llm-app-security
description: Apply operational controls to applications built on the Anthropic API or similar LLM SDKs. Maps the OWASP LLM Top 10 to practical controls, plus rate limiting, cost caps, PII scrubbing, audit logging, model-version pinning, and an AI-incident response playbook. Invoke when shipping an LLM feature to production, when handling an abuse complaint, or after a model-provider advisory.
---

# LLM App Security

The prompt and the tools are one layer of the story. This skill covers the other layer: **the operational side** of running an LLM-powered feature in production. The threats are mostly mundane (abuse, cost, leak, compliance), the controls mostly familiar from API security, applied to a substrate that has new failure modes.

Companion to [`prompt-injection-defense`](../prompt-injection-defense/SKILL.md) (prompt layer) and [`ai-agent-guardrails`](../ai-agent-guardrails/SKILL.md) (tool layer).

## When to invoke

- Designing or reviewing an LLM feature before public launch
- Investigating unusual API spend or 429s
- Handling an abuse complaint ("your AI told a user to ...", "your AI leaked ...")
- After a model-provider security advisory
- Periodic re-review of an existing LLM product surface

## The OWASP LLM Top 10 — practical mapping

Walk these against your app. Most issues fall under one of these.

| ID | Issue | Practical control |
|---|---|---|
| LLM01 | Prompt injection | See [`prompt-injection-defense`](../prompt-injection-defense/SKILL.md) |
| LLM02 | Insecure output handling | Treat model output as untrusted: escape, sanitize, validate before acting |
| LLM03 | Training-data poisoning | Mostly upstream; pick reputable providers, version-pin |
| LLM04 | Model DoS | Per-user/IP rate limit; cost cap; max-tokens cap; timeout |
| LLM05 | Supply chain | Pin SDK versions, audit MCP/plugin packages, scan deps |
| LLM06 | Sensitive information disclosure | PII scrubbing pre-context; output review; allowlist what the model can fetch |
| LLM07 | Insecure plugin / tool design | See [`ai-agent-guardrails`](../ai-agent-guardrails/SKILL.md) |
| LLM08 | Excessive agency | Narrow tool scope; human-in-loop for high-tier actions |
| LLM09 | Overreliance | UI disclosures; show provenance for facts; gate medical/legal/financial advice |
| LLM10 | Model theft / prompt theft | Treat the system prompt as a secret (not strong, but reduces casual leakage) |

## Rate limiting and cost caps

LLM calls are uniquely expensive — a single user can burn 1000× a regular API user's spend before a normal rate-limiter fires.

Layer your limits:

```ts
// Pseudocode — apply all three, not just one
async function callLLM(userId: string, request: Request) {
  await assertWithinRpmLimit(userId);          // requests/minute per user
  await assertWithinDailyTokenBudget(userId);  // tokens/day per user
  await assertWithinGlobalCostBudget();        // $/day across all users — hard kill switch

  const response = await anthropic.messages.create({
    model: "claude-sonnet-4-6",
    max_tokens: 4096,              // hard cap on output
    ...request,
  });

  await recordTokenSpend(userId, response.usage);
  return response;
}
```

Specific recommendations:

- **`max_tokens` is your friend.** Always set it. The model can be talked into producing 100k tokens if it has the budget.
- **Cap requests per user per minute** at a number a real user could plausibly hit, not the theoretical maximum.
- **Daily token budget per user** with a configurable enterprise tier. Reset on UTC midnight.
- **Global $/day cap** that hard-kills LLM calls — fail closed. This is the cost equivalent of a kill switch.
- **Long-prompt detection** — flag and cap prompts that exceed a typical-user-prompt percentile. Most abuse is paired with very long prompts (context-stuffing).

## Cost-side abuse detection

Cost-monitoring is detection-in-disguise:

- Sudden spike in tokens per request → context-stuffing attack or accidental loop
- Sudden spike in requests-per-second from one user → automation/scraping
- Tokens billed but very short user-visible outputs → exfiltration probe (model produces hidden output to a tool)
- Repeated identical prompts → harvesting / consistency probing
- API-key usage outside business hours from a single key → key compromise

Hook these into your existing on-call.

## PII scrubbing — both directions

**Pre-context**: redact before the model sees it. The model cannot leak what it never had.

- Names, emails, phone numbers in transcripts going to summarization
- Stored secrets — never let the API key, DB password, etc. enter context. Use tools that *use* the secret on the LLM's behalf instead.
- Customer data fields beyond what the feature needs. If you only need the order ID, do not send the whole order row.

**Post-output**: scan model output for accidentally-emitted PII before persisting or rendering. Models occasionally regurgitate memorized strings under odd prompts.

## Audit logging — what to keep

Log enough to investigate an abuse complaint six months later. Avoid logging anything that turns the log into a new compliance liability.

| Keep | Maybe | Don't |
|---|---|---|
| Request ID, user ID, timestamp | Model name + version | Full unhashed prompts that may contain user PII |
| Token counts (input/output) | Tool calls + arguments (with secrets redacted) | API keys, auth tokens, cookies in any form |
| Latency, status, cost | High-level prompt category | Full responses that may contain regurgitated training data — unless legally required |
| Safety/moderation decisions | Hash of the prompt (for dedup) | |

Retention: align with your privacy policy. Hot tier 30 days, archive 12 months is a common compromise; defer to your DPO for jurisdictions with stricter rules.

## Response moderation hooks

For user-facing LLM outputs, run output through a moderation step before showing it. Options:

- Anthropic's built-in safety behavior is the first line; do not turn it off
- A small classifier for category-specific risk (medical advice, legal claims, financial recommendations)
- A simple regex layer for known-bad outputs (e.g. should never emit an SSN-shaped pattern in your context)

Show users what was filtered when it makes sense; do not just silently swallow content.

## Model version pinning

- **Pin to a specific model ID**, not an alias like "latest". Behavior changes between versions; pin to a known-tested version.
- **Define a migration policy** — when you upgrade model versions, re-run your regression suite (you have one, right?) and your jailbreak/injection corpus.
- **Watch deprecation notices** — providers retire models. Have a plan that does not involve "just switch to latest and hope".

## Disclosure and overreliance

LLM features get used as authoritative sources by users who shouldn't trust them that way. Defensive UI is part of security in 2026:

- Clear "AI-generated" labeling on output
- Show source citations where the feature is retrieval-based
- For high-stakes domains (medical, legal, financial, immigration, identity), explicit disclaimers and routing to human review
- Never let the LLM make irreversible decisions on the user's behalf without an explicit, structured confirmation step

This is partly UX, partly legal — but it is also security in the sense that overreliance creates incidents.

## Incident response for an AI feature

When an AI feature does something it shouldn't, the playbook is similar to [`incident-response`](../incident-response/SKILL.md) but with specifics:

1. **Capture the conversation** — full request, full response, full tool-call sequence. Hash the prompt; preserve the response.
2. **Disable the specific path** — feature flag the offending feature off (or fall back to non-LLM behavior) while investigating.
3. **Triage** — was this a prompt-injection, a model-output issue, a tool-design issue, or a user actually using the feature as intended?
4. **Contain** — for injection or output issues, narrow the system prompt or add a moderation layer. For tool-design issues, add a confirmation or remove the tool.
5. **Communicate** — affected user(s) get a direct response. If broader, a status post explaining what happened and what changed. Be concrete; do not blame "the AI" as a deflection.
6. **Add a regression test** — the specific prompt that produced the issue goes into your eval suite. Never let the same failure re-ship.

## Quick design checklist

Before an LLM feature ships:

- [ ] `max_tokens` is set on every call
- [ ] Per-user RPM and token-per-day limits
- [ ] Global cost cap with hard fail-closed kill
- [ ] PII redaction before context
- [ ] Output moderation hook for user-facing emissions
- [ ] Audit log: who, when, model, tokens, cost — without storing PII unnecessarily
- [ ] Model version is pinned, not alias
- [ ] UI labels output as AI-generated where applicable
- [ ] There is a feature-flag kill for the LLM path
- [ ] You have a regression eval suite, even a small one, and it runs in CI

## What this skill will not do

- Help build LLM features that bypass safety controls of the underlying model
- Recommend disabling rate limits, cost caps, or moderation in production
- Endorse using an LLM as the sole decision-maker for irreversible user-impacting actions
