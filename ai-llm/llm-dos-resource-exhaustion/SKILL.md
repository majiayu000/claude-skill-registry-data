---
name: llm-dos-resource-exhaustion
description: Review AI systems for LLM-specific denial-of-service vulnerabilities including token flooding, recursive prompt expansion, sponge attacks, computational complexity exploitation, and resource exhaustion patterns that degrade availability for all users.
last_reviewed: 2026-04-30
---

# LLM DoS and Resource Exhaustion

## First Principle

**LLM inference has no fixed computational cost per request. An attacker who can set the cost ceiling can make every request arbitrarily expensive.**

Traditional web services have bounded computational cost per request. LLM inference cost grows with input length, output length, and the complexity of reasoning required. An attacker who can maximize any of these dimensions — through token flooding, recursive expansion prompts, or sponge inputs engineered to maximize attention computation — can exhaust GPU resources for all users with a small number of requests. The attack surface is the inference pipeline itself.

## Attack Mental Model

1. **Token flooding** — attacker submits requests with maximum allowed context length, all tokens filled with adversarial content engineered to maximize attention computation. Quadratic attention scaling means long inputs are disproportionately expensive.
2. **Recursive expansion** — a prompt is crafted so the model's output instructs a downstream pipeline to make additional LLM calls. Each call generates outputs that trigger further calls, causing recursive expansion until resource limits are hit.
3. **Sponge attack** — inputs are crafted using dense, ambiguous text (long lists, nested structures, contradictory statements) that maximizes the number of attention operations the model performs per token — draining compute without necessarily increasing output length.
4. **Streaming response exhaustion** — an attacker opens many long-running streaming connections simultaneously. Even if per-request token limits are enforced, concurrent streaming ties up GPU memory and bandwidth.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Request parameters are bounded server-side before reaching the model. Client-supplied `max_tokens`, `n`, and context length values are capped regardless of what was submitted. |
| **Scope** | Per-account, per-IP, and global token budgets are enforced with shared counters. A single account cannot exhaust global capacity even with valid credentials. |
| **Isolate** | Recursive LLM call chains are detected and broken at configurable depth limits. A pipeline cannot recursively call itself or create unbounded agent loops. |
| **Enforce** | Inference capacity is monitored in real time. Circuit breakers halt new request acceptance when GPU utilization exceeds a threshold, before exhaustion affects in-flight requests. |

## LDR.1 Request Bounding and Sponge Attack Mitigation

**The core vulnerability:** LLM inference time scales super-linearly with input length due to attention's quadratic complexity. An input of 10,000 tokens is not 10× more expensive than 1,000 tokens — it can be 100× more expensive. Without server-side input bounds, an attacker can exhaust inference capacity with a single request.

### Check

- Are input context lengths bounded server-side — with the bound enforced before tokenization, not after?
- Is there a cost estimator that rejects requests whose estimated compute cost exceeds a per-request limit before they reach the model?
- Are inputs with high adversarial complexity signals (dense repetition, deeply nested structures, contradictory constraint chains) flagged for pre-processing inspection?

### Action

- **Enforce multi-dimensional request bounds before inference:**

```python
MAX_INPUT_TOKENS = 4096
MAX_OUTPUT_TOKENS = 2048
MAX_TOTAL_TOKENS_PER_REQUEST = 6000
MAX_CONCURRENT_STREAMS_PER_ACCOUNT = 5

def validate_request(request: InferenceRequest, account: Account) -> None:
    input_tokens = count_tokens(request.messages)
    if input_tokens > MAX_INPUT_TOKENS:
        raise RequestTooLarge(f"Input exceeds {MAX_INPUT_TOKENS} tokens")

    capped_output = min(request.max_tokens or 512, MAX_OUTPUT_TOKENS)
    if input_tokens + capped_output > MAX_TOTAL_TOKENS_PER_REQUEST:
        raise RequestTooLarge("Combined token budget exceeded")

    if request.stream:
        active_streams = get_active_streams(account.id)
        if active_streams >= MAX_CONCURRENT_STREAMS_PER_ACCOUNT:
            raise TooManyStreams("Concurrent stream limit reached")

    request.max_tokens = capped_output  # enforce server-side cap
```

- **Detect sponge input patterns before inference.** Compute a complexity score for incoming context: repetition ratio, nesting depth, contradiction density. Inputs with anomalously high scores are throttled or require explicit account-level approval.
- **Tokenize on the server before accepting the request.** Validate against token limits using server-side tokenization. Client-reported token counts cannot be trusted.

### Failure Modes

- A request arrives with `max_tokens=100000` and a 50,000-token context filled with dense nested JSON. The input length check is applied after client-reported `num_tokens` passes validation. Server-side tokenization finds 50,000 tokens; the request reaches the model before the limit check fires.
- A free-tier account sends 10 concurrent streaming requests, each maxed at `max_tokens=2048`. The per-request limit is within bounds but 10 concurrent streams saturate GPU memory for all other users on the shared worker.

## LDR.2 Recursive Expansion and Loop Detection

**The core vulnerability:** Agentic pipelines that allow model outputs to trigger additional model calls can be exploited to create unbounded recursive loops. An attacker who can influence the model's output to include tool calls or agent instructions that re-invoke the pipeline can exhaust resources without per-request limits catching the attack.

### Check

- Is there a maximum call depth for agentic LLM chains? Is this enforced in code, not relying on model self-termination?
- Can a model output trigger an action that directly or indirectly calls back into the same pipeline? If so, is there a cycle detection mechanism?
- Is there a total token budget per user request — across all LLM calls in a chain — not just per individual call?

### Action

- **Implement call depth limits and cycle detection for agentic pipelines:**

```python
from dataclasses import dataclass, field

@dataclass
class AgentExecutionContext:
    root_request_id: str
    call_depth: int = 0
    total_tokens_consumed: int = 0
    call_chain: list[str] = field(default_factory=list)

MAX_CALL_DEPTH = 10
MAX_TOTAL_TOKENS_PER_CHAIN = 50000

def invoke_llm_in_chain(
    prompt: str,
    context: AgentExecutionContext,
    model: LLMModel,
) -> str:
    if context.call_depth >= MAX_CALL_DEPTH:
        raise RecursionLimitExceeded(f"Max call depth {MAX_CALL_DEPTH} reached")

    if context.total_tokens_consumed >= MAX_TOTAL_TOKENS_PER_CHAIN:
        raise TokenBudgetExceeded(f"Chain budget {MAX_TOTAL_TOKENS_PER_CHAIN} exhausted")

    context.call_depth += 1
    response = model.generate(prompt)
    context.total_tokens_consumed += response.tokens_used
    context.call_depth -= 1
    return response.text
```

- **Implement a global circuit breaker for inference capacity.** When GPU utilization exceeds 85%, new request acceptance is paused and incoming requests receive a `503 Service Temporarily Unavailable` with `Retry-After` header. This prevents cascade failure when a DoS is in progress.
- **Monitor per-account token consumption velocity.** An account consuming tokens at 10× its historical average is either under attack or is itself running a DoS. Automatic rate reduction at 3× average; alert at 5×; suspend at 10×.

### Minimum Deliverable Per Review

- [ ] Input bounds: server-side tokenization and token count enforcement before inference
- [ ] Output bounds: `max_tokens` server-side cap regardless of client-supplied value
- [ ] Concurrent stream limits: per-account limit on simultaneous streaming connections
- [ ] Call depth limit: maximum depth for agentic LLM chains enforced in code
- [ ] Chain token budget: total token limit per root request across all recursive calls
- [ ] Circuit breaker: global inference capacity protection with automatic new-request pause at threshold
- [ ] Consumption velocity monitoring: per-account anomaly detection with tiered automated response

## Quick Win

**Add server-side input tokenization and enforce a hard input token limit before any request reaches the model.** Do not rely on client-reported counts. A single `if token_count > MAX_INPUT_TOKENS: return 413` before inference eliminates the token flooding attack surface entirely.

## References

- Model serving security → [model-serving-security/SKILL.md](../model-serving-security/SKILL.md)
- Inference API abuse prevention → [inference-api-abuse-prevention/SKILL.md](../inference-api-abuse-prevention/SKILL.md)
- Agentic trust boundaries → [agentic-trust-boundaries/SKILL.md](../agentic-trust-boundaries/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
