---
name: financial-velocity-budgeting
description: Implement token cost estimation, sliding-window velocity caps, and hierarchical credit allocation for multi-agent LLM systems. Prevent runaway API spend with pre-request budget gates and dead-man switches.
origin: YAMTAM Engine rule 60, Anthropic usage API, tiktoken (MIT)
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Financial Velocity Budgeting

Enforce hard token budgets before LLM requests are made — not after the bill arrives.

## When to Use

- Multi-agent systems where any single runaway agent can exhaust daily API budget
- Autonomous loops that run unsupervised for extended periods
- Cost-sensitive deployments where token spend must be bounded per agent/session
- Detecting prompt injection attacks that inflate token usage deliberately

## Do NOT use for

- Single-request CLI tools where cost is predictable and low
- Internal model inference (no API cost)

## Pre-Request Budget Gate

```js
class TokenBudgetGate {
  constructor(opts = {}) {
    this.dailyCap   = opts.dailyCap   ?? parseInt(process.env.YAMTAM_DAILY_TOKEN_BUDGET ?? '100000');
    this.agentCap   = opts.agentCap   ?? parseInt(process.env.YAMTAM_AGENT_TOKEN_CAP ?? '5000');
    this.windowSec  = opts.windowSec  ?? 10;
    this.windowCap  = opts.windowCap  ?? 2000;
    this.used       = new Map();   // agentId → { session, window, windowStart }
    this.dailyTotal = 0;
  }

  // Estimate tokens before sending (rough: 1 token ≈ 4 chars)
  estimate(prompt) {
    return Math.ceil(prompt.length / 4) * 1.3;  // +30% output estimate
  }

  check(agentId, prompt) {
    const estimated = this.estimate(prompt);
    const state = this.used.get(agentId) ?? { session: 0, window: 0, windowStart: Date.now() };

    // Reset sliding window
    if (Date.now() - state.windowStart > this.windowSec * 1000) {
      state.window = 0;
      state.windowStart = Date.now();
    }

    if (state.session + estimated > this.agentCap)
      throw new BudgetExceededError('AGENT_SESSION_CAP', agentId, estimated, this.agentCap - state.session);
    if (state.window + estimated > this.windowCap)
      throw new BudgetExceededError('VELOCITY_CAP', agentId, estimated, this.windowCap - state.window);
    if (this.dailyTotal + estimated > this.dailyCap)
      throw new BudgetExceededError('DAILY_CAP', agentId, estimated, this.dailyCap - this.dailyTotal);

    return { ok: true, estimated };
  }

  record(agentId, actual) {
    const state = this.used.get(agentId) ?? { session: 0, window: 0, windowStart: Date.now() };
    state.session += actual;
    state.window  += actual;
    this.dailyTotal += actual;
    this.used.set(agentId, state);
  }
}
```

## Prompt Injection Cost Attack Detection

```js
function detectCostAttack(prompt) {
  // Repeated phrase bomb
  const words = prompt.split(/\s+/);
  const freq = new Map();
  for (const w of words) freq.set(w, (freq.get(w) ?? 0) + 1);
  const maxFreq = Math.max(...freq.values());
  if (maxFreq > 50) throw new Error('COST_ATTACK: repeated phrase detected');

  // Token stuffing via Unicode
  const unicodeDensity = (prompt.match(/[^\x00-\x7F]/g)?.length ?? 0) / prompt.length;
  if (unicodeDensity > 0.3) throw new Error('COST_ATTACK: Unicode stuffing detected');
}
```

## Hierarchical Budget Tree

```
Global (100k tokens/day)
  ├── Orchestrators (40k)  ← YAMTAM_ORCH_TOKEN_POOL
  ├── Executors     (50k)  ← YAMTAM_EXEC_TOKEN_POOL
  │   └── Per agent (5k)   ← YAMTAM_AGENT_TOKEN_CAP
  └── Reserve       (10k)  ← emergency rollback + auditor
```

## Dead-Man Integration

```js
// If daily budget > 80%, require human confirmation
if (gate.dailyTotal > gate.dailyCap * 0.8) {
  const approved = await requireHumanApproval('Budget at 80% — continue?');
  if (!approved) throw new Error('DEADMAN: human declined continuation');
}
```

## Anti-Fake-Pass Checklist

- [ ] `gate.check()` called BEFORE every LLM API call, not after
- [ ] `gate.record()` called with ACTUAL tokens from API response (not estimate)
- [ ] Velocity window resets correctly — test with `Date.now()` mock
- [ ] Cost attack detection tested with 100× repeated phrase
- [ ] Dead-man 80% threshold tested by simulating high daily usage
