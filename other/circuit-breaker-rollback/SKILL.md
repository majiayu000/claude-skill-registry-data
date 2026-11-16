---
name: circuit-breaker-rollback
description: Implement circuit breaker patterns, canary deployment gates, hallucination telemetry checkers, and automated rollback for agent skill deployments. Stop cascading failures before they propagate across the swarm.
origin: Netflix Hystrix concept, Martin Fowler Circuit Breaker pattern, YAMTAM rules 56–57
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# Circuit Breaker & Automated Rollback

Isolate failing agents/tools automatically before errors cascade. Deploy new skills to 1% canary traffic, roll back if quality drops.

## When to Use

- Agent or tool returning repeated errors that are slowing the entire swarm
- Deploying a new skill and wanting automatic rollback if it degrades quality
- Protecting downstream agents from an upstream agent stuck in an error loop
- Implementing the YAMTAM circuit-breaker-law (rule 56) and canary-deployment-law (rule 57)

## Do NOT use for

- Single requests where retrying once is fine
- Tools that must always be called regardless of prior failures (e.g., audit logging)

## Circuit Breaker

```js
class CircuitBreaker {
  constructor(opts = {}) {
    this.threshold   = opts.threshold ?? 5;
    this.cooldown    = opts.cooldown  ?? 60000;  // 60s
    this.state       = 'CLOSED';
    this.failures    = 0;
    this.lastFailure = 0;
    this.openCount   = 0;
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      const elapsed = Date.now() - this.lastFailure;
      if (elapsed < this._cooldownMs()) throw new Error('CIRCUIT_OPEN');
      this.state = 'HALF_OPEN';
    }

    try {
      const result = await fn();
      this._onSuccess();
      return result;
    } catch (e) {
      this._onFailure(e);
      throw e;
    }
  }

  _onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  _onFailure(e) {
    this.failures++;
    this.lastFailure = Date.now();
    // Security blocks open immediately
    const immediate = e.exitCode === 3 || e.exitCode === 7;
    if (immediate || this.failures >= this.threshold) {
      this.state = 'OPEN';
      this.openCount++;
    }
  }

  _cooldownMs() {
    // Exponential backoff: 60s, 300s, 1800s
    return [60000, 300000, 1800000][Math.min(this.openCount - 1, 2)];
  }
}

// Usage
const breaker = new CircuitBreaker({ threshold: 5 });
await breaker.call(() => runAgentTool(agentId, command));
```

## Canary Deployment

```js
class CanaryGate {
  constructor(opts = {}) {
    this.rate      = opts.rate     ?? 0.01;  // 1%
    this.windowMs  = opts.windowMs ?? 30 * 60 * 1000;  // 30 min
    this.baseline  = opts.baseline ?? { errorRate: 0.02, latencyP95: 500 };
    this.canaryStats = { calls: 0, errors: 0, latencies: [] };
  }

  shouldUseCanary() {
    return Math.random() < this.rate;
  }

  record(isError, latencyMs) {
    this.canaryStats.calls++;
    if (isError) this.canaryStats.errors++;
    this.canaryStats.latencies.push(latencyMs);
  }

  shouldRollback() {
    const { calls, errors, latencies } = this.canaryStats;
    if (calls < 10) return false;  // not enough data

    const errorRate = errors / calls;
    const p95 = latencies.sort((a,b) => a-b)[Math.floor(latencies.length * 0.95)];

    return errorRate > this.baseline.errorRate + 0.02 ||
           p95 > this.baseline.latencyP95 * 1.2;
  }
}
```

## Hallucination Telemetry Checker

```js
async function checkHallucination(skillOutput, referenceOutput) {
  // Cosine similarity of embeddings (simplified)
  const similarity = cosineSimilarity(
    await embed(skillOutput),
    await embed(referenceOutput)
  );
  // < 0.85 similarity = potential hallucination
  return { score: similarity, hallucinated: similarity < 0.85 };
}

// In canary pipeline:
const { hallucinated, score } = await checkHallucination(canaryResult, baselineResult);
if (hallucinated) {
  canaryGate.rollback();
  secureLogger.logAction('canary', 'hallucination-detected', 'BLOCK', { score });
}
```

## Sovereign State Reconstruction (Lớp 96)

```js
// Restore swarm to last verified Merkle snapshot
async function emergencyRollback() {
  const lastGoodRoot = readFileSync('releases/logs/audit.jsonl.root', 'utf8').trim();
  const snapshotPath = `releases/snapshots/${lastGoodRoot.slice(0,16)}.tar.gz`;

  // Verify snapshot integrity before restoring
  const actual = sha256(readFileSync(snapshotPath));
  if (actual !== lastGoodRoot) throw new Error('SNAPSHOT_TAMPERED');

  execSync(`tar -xzf ${snapshotPath} -C /workspaces/yana-ai/`);
  secureLogger.logAction('system', 'emergency-rollback', 'PASS', { root: lastGoodRoot });
}
```

## Anti-Fake-Pass Checklist

- [ ] Circuit opens after exactly `threshold` failures — test with mock that always throws
- [ ] HALF_OPEN probe: single success closes circuit, single failure reopens
- [ ] Canary rate = 0.01 — verify `shouldUseCanary()` returns true ~1% of calls
- [ ] Rollback triggered before promoting canary to 100% if error rate rises
- [ ] Snapshot hash verified before restoring (tampered snapshot = abort)
