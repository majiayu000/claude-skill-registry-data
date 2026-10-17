---
name: run-adapter-diagnostic
description: Check adapter health, latency percentiles, and error rates in real time. Reports against SLA targets.
compatibility: |
  - Runtime: Node.js 18+
  - Dependencies: Adapter telemetry service access
---

# run-adapter-diagnostic

Reports adapter health: success rate, latency percentiles, and error rate against SLA targets.

## Trigger

```bash
run-adapter-diagnostic [adapter-name] [time-window]
```

## Input Schema

```typescript
interface DiagnosticInput {
  adapterName?: string;  // e.g., "BrowserNavigate", "ModelGenerate" (optional)
  timeWindow?: string;   // "5m" | "1h" | "24h" (default: "5m")
}
```

## Output Schema

```typescript
interface DiagnosticOutput {
  status: "success" | "error";
  adapter: string;
  successRate: number;
  latency: { p50: number; p95: number; p99: number };
  errorRate: number;
  recentErrors: string[];
  timestamp: string;
}
```

---

**Full reference:** See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md).


