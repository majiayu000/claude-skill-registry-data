---
name: model-dos
description: Detects LLM endpoints missing token caps, rate limits, or prompt-length
  bounds, enabling cost and resource exhaustion. Use when writing LLM API call
  handlers, setting up inference endpoints, implementing chatbot backends, or
  configuring token limits for LLM services. Also invoke when accepting user-
  provided prompts without length constraints.
---

# Model Denial of Service Security Check (OWASP LLM04:2025)

## What this checks

Protects against resource exhaustion caused by unbounded prompts, missing token caps,
or absent rate limiting. Attackers can submit enormous or recursive inputs that inflate
inference costs, saturate GPU/CPU, and deny service to legitimate users.

## Vulnerable patterns

- LLM API calls with no `max_tokens` parameter — model generates until its internal limit
- No input length validation before sending to the inference endpoint
- Multi-turn chat that accumulates context indefinitely across turns
- No per-user or per-IP rate limiting on the prompt endpoint

## Fix immediately

Flag the vulnerable code and explain the risk. Then suggest a fix that establishes
these properties:

1. **Every LLM call sets an explicit output cap** — the provider's max-tokens
   parameter or its equivalent. Leaving it at the provider default lets a single
   request run for minutes and rack up dollars in tokens.
2. **Prompt input is length-capped at the handler boundary** before it reaches the
   inference client. Measured in chars, bytes, or tokens — the exact unit does not
   matter as long as the cap runs before the upstream call.
3. **Conversation context is bounded.** Either the handler is stateless
   single-turn, or accumulated history is trimmed to a fixed turn or token
   budget before every call. Unbounded history is an attacker's favorite
   amplifier.
4. **Per-identifier throttling** (per user, per API key, per IP) runs on every
   LLM endpoint. In-process token bucket, framework middleware, or reverse-proxy
   rule — anything that survives alias and batch tricks and prevents one caller
   from pinning the endpoint.
5. **Every inference call has a deadline.** SDK timeout, HTTP client timeout, or
   request-context cancellation — a hung upstream must not be able to
   indefinitely occupy a worker.

Translate each principle to the inference SDK, web framework, and rate-limiter of
the audited file. Use the SDK's documented cap and timeout parameters — do not rely
on global defaults.

## Verification

Confirm the following *properties* hold (language-agnostic):

- [ ] Every LLM API call sets an explicit output cap on generated tokens — never left to the provider default
- [ ] Caller-supplied prompt text is length-capped (chars, bytes, or tokens) and rejected at the handler boundary before reaching the inference client
- [ ] Conversation context fed to the model is bounded: either the handler is single-turn and stores no history at all, or any accumulated history is trimmed to a fixed turn/token budget before the call
- [ ] Every LLM endpoint enforces a per-identifier throttle (per user, per API key, or per IP) through any mechanism — in-process bucket, framework middleware, reverse-proxy rule — not just a global concurrency cap
- [ ] Every inference call runs under an explicit deadline expressed through any available mechanism — SDK timeout parameter, HTTP client read/write timeout, request context or cancellation deadline, or framework-level request timeout — so a hung upstream cannot pin a worker indefinitely

## References

- CWE-400 ([Uncontrolled Resource Consumption](https://cwe.mitre.org/data/definitions/400.html))
- CWE-770 ([Allocation of Resources Without Limits or Throttling](https://cwe.mitre.org/data/definitions/770.html))
- [OWASP LLM04:2025 Model Denial of Service](https://genai.owasp.org/llmrisk/llm04-model-denial-of-service/)
