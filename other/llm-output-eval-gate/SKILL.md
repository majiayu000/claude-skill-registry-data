---
name: llm-output-eval-gate
description: Add a two-layer quality gate around any LLM call so bad model output never reaches the user. Use when building agents or apps that call an LLM for structured output (plans, JSON, reviews, summaries) and need deterministic validation, model-based scoring, bounded auto-retry, best-of fallback, and an audit log. Not for prompt authoring, model selection, or replacing human review of high-stakes output.
version: 1.0.0
---

# LLM Output Eval Gate

Most "AI features" are a thin shell over an LLM API: whatever the model returns is shown to the user, wrong or not. This skill wraps every LLM call in a quality gate so unusable output is caught, retried, and logged.

## The Pattern

```
generate → L1 deterministic validation → L2 quality scoring → pass
                │                            │
                └─ fail ─→ retry (bounded) ─→ fall back to best attempt
                                   │
                                   └─ log every attempt (auditable)
```

1. **L1 — deterministic rules.** Cheap, instant, no model involved. Check JSON structure, required fields, enum values, numeric ranges, count bounds, duplicates, and any domain budget (e.g. total minutes ≤ available time). L1 failures skip L2 entirely.
2. **L2 — quality scoring.** LLM-as-Judge when an API is available; a heuristic scorer as offline fallback so behavior stays consistent without a key. Score 0-10 against a threshold (default 7).
3. **Bounded retry.** Retry at most 2 times. Track the best-scoring attempt and fall back to it if nothing passes — never return nothing.
4. **Audit log.** Persist every attempt: pass/fail, issues, score, retry count, mode (live/mock), timestamp. Surface the log inside the product, not just in dev tools.

## Implementation

Copy `scripts/eval-gate.js` into the project (vanilla JS, zero dependencies, works in browser and Node). It exposes one async function:

```js
var res = await EvalGate.gate({
  name: "plan",                    // label used in logs
  generate: async (attempt) => {...},  // call the LLM, return parsed result
  validate: (result) => ({ pass, issues }),  // L1 rules
  judge: async (result) => ({ score, comment }), // L2 scoring
  threshold: 7,
  maxRetries: 2
});
// res = { ok, result, report:{ attempts, retries, finalPass, finalScore, mode } }
```

Write `validate` and `judge` per domain; the gate mechanics never change.

## Setting The Threshold

Do not pick the threshold by intuition. Build a small set of deliberately-bad outputs (too many items, over budget, wrong enums, duplicate titles) and a few known-good ones, then choose the lowest threshold that blocks every bad sample without rejecting good ones. Keep the threshold in config so it can be tuned without a deploy. A demo mode that intentionally generates a bad first output is the fastest way to prove the gate works.

## Design Rules

- Put hard constraints in L1, taste in L2. Anything checkable without a model belongs in L1.
- Always define the fallback: best-of-attempts, a safe default, or a clear error — never an unvalidated render.
- Make the retry loop visible to the user (badge, toast, log entry). The gate is a product feature, not hidden plumbing.
- Mock mode must reproduce the same pass/fail behavior as live mode, including a deliberately-failing first attempt, so the pipeline is demoable without a key.

## Before / After

Before, a typical AI feature ships whatever the model returns:

```js
var plan = await callLLM(prompt);
render(plan);            // 字段缺失、超预算、格式错，用户直接看到
```

After, the same call is wrapped in the gate:

```js
var res = await EvalGate.gate({
  name: "plan",
  generate: callLLM,
  validate: (r) => ({ pass: r.items.length <= 5 && r.minutes <= 240, issues: [] }),
  judge: scorePlan,
  threshold: 7,
  maxRetries: 2
});
if (!res.ok) renderFallback(res.result);   // 永远有东西可渲染，且每次尝试都有日志
```

Bad output is caught, retried at most twice, and logged before it can reach the user.
