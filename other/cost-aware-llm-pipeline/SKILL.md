---
name: cost-aware-llm-pipeline
description: Cost optimization patterns for LLM API usage — model routing by task complexity, immutable budget tracking, narrow retry logic, and prompt caching. Use when building or reviewing code that calls LLM text APIs (Claude, GPT, etc.) and spend must be routed, capped, or tracked — batch pipelines, multi-model routing, budget guardrails. Do NOT use for paid image/video render approval (that is the STOP-AND-SHOW / cost-governance-gate human-consent flow) or for choosing which model a Claude Code agent session itself runs on.
origin: ECC
---

# Cost-Aware LLM Pipeline

Patterns for controlling LLM API costs while maintaining quality. Combines model routing, budget tracking, retry logic, and prompt caching into a composable pipeline.

## When to use

- Building applications that call LLM APIs (Claude, GPT, etc.)
- Batch processing pipelines where per-item cost adds up quickly
- Multi-model architectures that need intelligent routing by task complexity
- Production systems that need budget guardrails — fail early rather than overspend
- Optimizing cost without sacrificing quality on complex tasks

**When NOT to use:**

- Paid image/video render governance — that is a human-consent gate (STOP-AND-SHOW, one manifest → one `y` → one call), not a code pattern. This skill governs programmatic text-API spend inside a pipeline the owner already approved.
- Choosing which Claude model an interactive agent session runs on — that is session/model policy, not pipeline code.

## Inputs

Required before starting. **Absent input = stop** — never proceed on a guessed value:

1. **Current per-token pricing** for every candidate model, fetched this session from the vendor's pricing page or Context7 `[docs]`. The Pricing Reference table below is a dated snapshot — pricing changes; never trust it (or your memory) over the vendor page.
2. **An explicit budget limit in USD** from the pipeline owner. No limit stated → stop and ask. Defaulting to "unlimited" (or skipping the `over_budget` check when the tracker is absent) is the fail-open pattern — bug-230.
3. **A measurable complexity signal** available at call time — text length, item count, or equivalent. Routing without a measurable input degenerates to a hardcoded model choice.
4. **The installed SDK's exception hierarchy** for the retry allowlist (e.g. `anthropic.APIConnectionError`, `RateLimitError`, `InternalServerError`) verified against the installed version (`pip show anthropic`), not training data.

## Core Concepts

### 1. Model Routing by Task Complexity

Automatically select cheaper models for simple tasks, reserving expensive models for complex ones.

```python
MODEL_SONNET = "claude-sonnet-4-6"
MODEL_HAIKU = "claude-haiku-4-5-20251001"

_SONNET_TEXT_THRESHOLD = 10_000  # chars
_SONNET_ITEM_THRESHOLD = 30     # items

def select_model(
    text_length: int,
    item_count: int,
    force_model: str | None = None,
) -> str:
    """Select model based on task complexity."""
    if force_model is not None:
        return force_model
    if text_length >= _SONNET_TEXT_THRESHOLD or item_count >= _SONNET_ITEM_THRESHOLD:
        return MODEL_SONNET  # Complex task
    return MODEL_HAIKU  # Simple task (3-4x cheaper)
```

### 2. Immutable Cost Tracking

Track cumulative spend with frozen dataclasses. Each API call returns a new tracker — never mutates state.

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class CostRecord:
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float

@dataclass(frozen=True, slots=True)
class CostTracker:
    budget_limit: float = 1.00
    records: tuple[CostRecord, ...] = ()

    def add(self, record: CostRecord) -> "CostTracker":
        """Return new tracker with added record (never mutates self)."""
        return CostTracker(
            budget_limit=self.budget_limit,
            records=(*self.records, record),
        )

    @property
    def total_cost(self) -> float:
        return sum(r.cost_usd for r in self.records)

    @property
    def over_budget(self) -> bool:
        return self.total_cost > self.budget_limit
```

### 3. Narrow Retry Logic

Retry only on transient errors. Fail fast on authentication or bad request errors.

```python
from anthropic import (
    APIConnectionError,
    InternalServerError,
    RateLimitError,
)

_RETRYABLE_ERRORS = (APIConnectionError, RateLimitError, InternalServerError)
_MAX_RETRIES = 3

def call_with_retry(func, *, max_retries: int = _MAX_RETRIES):
    """Retry only on transient errors, fail fast on others."""
    for attempt in range(max_retries):
        try:
            return func()
        except _RETRYABLE_ERRORS:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
    # AuthenticationError, BadRequestError etc. → raise immediately
```

### 4. Prompt Caching

Cache long system prompts to avoid resending them on every request.

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},  # Cache this
            },
            {
                "type": "text",
                "text": user_input,  # Variable part
            },
        ],
    }
]
```

## Composition

Combine all four techniques in a single pipeline function:

```python
def process(text: str, config: Config, tracker: CostTracker) -> tuple[Result, CostTracker]:
    # 1. Route model
    model = select_model(len(text), estimated_items, config.force_model)

    # 2. Check budget
    if tracker.over_budget:
        raise BudgetExceededError(tracker.total_cost, tracker.budget_limit)

    # 3. Call with retry + caching
    response = call_with_retry(lambda: client.messages.create(
        model=model,
        messages=build_cached_messages(system_prompt, text),
    ))

    # 4. Track cost (immutable)
    record = CostRecord(model=model, input_tokens=..., output_tokens=..., cost_usd=...)
    tracker = tracker.add(record)

    return parse_result(response), tracker
```

## Procedure

1. Gather the four Inputs above. Missing any → stop.
2. Fetch current pricing for every candidate model (Context7 or vendor pricing page) and record it as named constants — one pricing table, not scattered literals. `[docs]`
3. Implement `select_model()` with explicit, named thresholds tied to your complexity signal. Start with the cheapest model as the default branch.
4. Implement `CostRecord` + `CostTracker` as `frozen=True` dataclasses; `add()` returns a new tracker. Compute `cost_usd` from the pricing constants, never inline arithmetic at call sites.
5. Implement `call_with_retry()` with an explicit allowlist of transient exception types and exponential backoff. Everything not on the allowlist raises immediately.
6. Add `cache_control: {"type": "ephemeral"}` to any system prompt over ~1024 tokens.
7. Compose the four pieces in one `process()` function in this order: route → budget gate → call → record. The budget gate runs **before** the call, so an over-budget batch stops without spending.
8. Log every model-selection decision (chosen model + the signal values that drove it) so thresholds can be tuned from real data.
9. Run the Verification checks below before calling the pipeline done.

## Verification

1. **Prove the pipeline invariants execute and can fail.** Run this self-contained check against the routing + tracker code (adapt names to your implementation — the assertions are the contract):

   ```bash
   python3 - <<'PY'
   from your_pipeline import select_model, CostRecord, CostTracker, MODEL_HAIKU, MODEL_SONNET
   assert select_model(500, 3) == MODEL_HAIKU          # simple → cheap
   assert select_model(10_000, 3) == MODEL_SONNET      # text threshold routes up
   assert select_model(500, 30) == MODEL_SONNET        # item threshold routes up
   assert select_model(50_000, 99, force_model="x") == "x"
   t0 = CostTracker(budget_limit=0.10)
   t1 = t0.add(CostRecord("m", 1000, 500, 0.06))
   t2 = t1.add(CostRecord("m", 1000, 500, 0.06))
   assert t0.records == () and t0.total_cost == 0.0    # original never mutated
   assert not t1.over_budget and t2.over_budget        # gate flips at the cap
   try:
       t1.budget_limit = 999
       raise SystemExit("FAIL: frozen dataclass allowed mutation")
   except AttributeError:
       pass
   print("OK: routing thresholds, immutability, budget gate all hold")
   PY
   ```

   **PASS:** prints the `OK:` line and exits 0. Any assertion failure or a successful mutation of the frozen tracker is a FAIL. `[repro]`

2. **In this repo:** `core/token_tracker.py` is the live production implementation of this pattern (`PROVIDER_COSTS` table, `TokenUsage.calculate_cost()`, `TokenTracker.get_total_cost()`). Its test suite must stay green after any change touching cost tracking:

   ```bash
   rtk proxy pytest tests/core/test_token_tracker_gate.py tests/core/test_token_tracker_embed.py -q
   ```

   **PASS:** all tests pass (all-dots line, `[100%]`), exit 0. `[test]` (Use `rtk proxy pytest`, not bare pytest — bare pytest can falsely report "no tests collected" in this repo.)

3. **Pricing freshness** — falsifiable manual check: diff every $/1M figure in your pricing constants (and the snapshot table below) against the vendor's pricing page retrieved **this session**. **PASS:** every figure matches the vendor page. Any mismatch → update the constant before shipping; a stale price silently corrupts every budget decision downstream. `[docs]`

## Worked example

Observed 2026-07-29 in this repo (worktree `glimmering-crafting-shannon`):

- Verification check 1, run with the skill's own reference implementation inlined in place of `your_pipeline`, printed exactly:

  ```
  OK: routing thresholds, immutability, budget gate all hold
  ```

  and exited 0. Deliberately breaking it (`t1.budget_limit = 999` succeeding) would exit non-zero — the check can fail. `[repro]`

- Verification check 2 output: 8 green dots, `[100%]`, `exit=0`. `[test]`

- The in-production instance of this pattern: `core/token_tracker.py` — pricing table `PROVIDER_COSTS` (dated "as of 2026-01-08" at `core/token_tracker.py:43`), per-call cost in `TokenUsage.calculate_cost()` (`core/token_tracker.py:93`, with an explicit `unknown_model_cost` warning path for unpriced models), cumulative spend in `TokenTracker.get_total_cost()` (`core/token_tracker.py:167`). `[repo]`

## Pricing Reference (snapshot 2025-2026 — re-verify per Inputs #1 before use)

| Model | Input ($/1M tokens) | Output ($/1M tokens) | Relative Cost |
|-------|---------------------|----------------------|---------------|
| Haiku 4.5 | $0.80 | $4.00 | 1x |
| Sonnet 4.6 | $3.00 | $15.00 | ~4x |
| Opus 4.5 | $15.00 | $75.00 | ~19x |

## Best Practices

- **Start with the cheapest model** and only route to expensive models when complexity thresholds are met
- **Set explicit budget limits** before processing batches — fail early rather than overspend
- **Log model selection decisions** so you can tune thresholds based on real data
- **Use prompt caching** for system prompts over 1024 tokens — saves both cost and latency
- **Never retry on authentication or validation errors** — only transient failures (network, rate limit, server error)

## Failure modes & anti-patterns

- **Missing budget limit treated as "no limit"** — the budget gate must fail CLOSED: absent limit = stop, not unlimited spend. This is the fail-open guard pattern (bug-230, ×6 in this repo).
- Using the most expensive model for all requests regardless of complexity.
- Retrying on all errors — wastes budget re-sending permanently-failing requests (auth, validation).
- Mutating cost tracking state — makes spend auditing unreliable; a mutated tracker cannot prove what a batch actually cost.
- Hardcoding model names and prices throughout the codebase — one stale literal corrupts routing and budget math; use named constants sourced per Inputs #1.
- Skipping prompt caching for repetitive system prompts — pays full input price on every call.
- Trusting a pricing table from memory or an old doc — pricing drifts; the snapshot above is dated for exactly this reason.
