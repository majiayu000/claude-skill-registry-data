---
name: opentelemetry-semantic-telemetry
description: Instrument multi-agent swarms with OpenTelemetry spans, semantic drift monitoring, anomaly detection, distributed trace propagation across 87 agents, and SIEM bridge export for security events.
origin: OpenTelemetry spec (Apache-2.0), Grafana Loki, YAMTAM rule 55
license: Apache-2.0
version: 1.0.0
compatibility: claude-sonnet-4-6, claude-opus-4-7
---

# OpenTelemetry Semantic Telemetry

Every agent action emits a span. Every span has a Trace ID. No action is invisible.

## When to Use

- Debugging complex multi-agent workflows where an error propagates across many agents
- Building observability dashboards for 87-agent swarms (Grafana, Jaeger)
- Detecting anomalous CPU/RAM patterns that indicate a compromised agent
- Forwarding security alerts to a SIEM for centralized monitoring

## Do NOT use for

- Simple single-agent CLI tools where stdout is sufficient
- Environments where telemetry overhead > 1ms per span is unacceptable

## Span Structure

```js
import { trace, context, SpanStatusCode } from '@opentelemetry/api';

const tracer = trace.getTracer('yana-ai', '1.4.0');

async function instrumentedAgentCall(agentId, command, fn) {
  return tracer.startActiveSpan(`agent.${command}`, async (span) => {
    span.setAttributes({
      'agent.id':      agentId,
      'agent.command': command,
      'agent.role':    agentRegistry.get(agentId)?.role,
      'trust.score':   agentRegistry.get(agentId)?.trustScore,
    });

    try {
      const result = await fn();
      span.setStatus({ code: SpanStatusCode.OK });
      span.setAttribute('result.status', 'PASS');
      return result;
    } catch (e) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: e.message });
      span.setAttribute('result.status', 'BLOCK');
      span.recordException(e);
      throw e;
    } finally {
      span.end();
    }
  });
}
```

## Trace Propagation Across Agents

```js
import { propagation, context } from '@opentelemetry/api';

// Sender: inject trace context into Bus message
function routeWithTrace(router, msg) {
  const carrier = {};
  propagation.inject(context.active(), carrier);
  return router.route({ ...msg, traceContext: carrier });
}

// Receiver: extract and restore trace context
function processWithTrace(msg, handler) {
  const ctx = propagation.extract(context.active(), msg.traceContext ?? {});
  return context.with(ctx, () => handler(msg));
}
```

## Anomaly Detection (Lớp 81)

```js
class MetricAnomalyDetector {
  constructor() {
    this.baselines = new Map();  // agentId → { ram: [], cpu: [] }
  }

  record(agentId, ram, cpu) {
    const b = this.baselines.get(agentId) ?? { ram: [], cpu: [] };
    b.ram.push(ram); b.cpu.push(cpu);
    if (b.ram.length > 60) { b.ram.shift(); b.cpu.shift(); }
    this.baselines.set(agentId, b);
  }

  isSawtooth(agentId) {
    const { ram } = this.baselines.get(agentId) ?? { ram: [] };
    if (ram.length < 6) return false;
    const last6 = ram.slice(-6);
    // Sawtooth: alternating high-low pattern
    let alternations = 0;
    for (let i = 1; i < last6.length; i++) {
      if (Math.abs(last6[i] - last6[i-1]) > last6[i-1] * 0.5) alternations++;
    }
    return alternations >= 3;
  }
}
```

## Semantic Drift Monitoring (Lớp 82)

```js
// Detect gradual prompt injection via embedding distance
async function detectSemanticDrift(currentPrompt, baselineEmbedding) {
  const currentEmbedding = await embed(currentPrompt);
  const distance = cosineSimilarity(currentEmbedding, baselineEmbedding);

  // distance < 0.6 means topic has drifted significantly
  if (distance < 0.6) {
    return { drifted: true, distance, alert: 'SEMANTIC_DRIFT_DETECTED' };
  }
  return { drifted: false, distance };
}
```

## Loki Log Labels

```js
// Structure logs for Grafana Loki querying
function lokiEntry(event, agentId, fortress, severity) {
  return {
    stream: {
      env:       'yamtam',
      agent_id:  agentId,
      fortress:  fortress,   // 'I' through 'X'
      severity:  severity,   // 'INFO' | 'WARN' | 'BLOCK'
    },
    values: [[String(Date.now() * 1e6), JSON.stringify(event)]],
  };
}
```

## SIEM Bridge (Lớp 90)

```js
// Forward security events in CEF format
function exportToSIEM(event) {
  const cef = `CEF:0|YAMTAM|Engine|1.4.0|${event.code}|${event.name}|${event.severity}|` +
    `agentId=${event.agentId} cmd=${event.command} ts=${event.ts}`;

  fetch(process.env.YAMTAM_SIEM_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain', Authorization: `Bearer ${siemToken}` },
    body: cef,
  }).catch(() => {/* best-effort — do not block on SIEM failure */});
}
```

## Anti-Fake-Pass Checklist

- [ ] Every agent call wrapped in `startActiveSpan` — no uninstrumented paths
- [ ] Trace context propagated through Bus messages (check W3C traceparent header)
- [ ] Anomaly detector tested with synthetic sawtooth RAM data → `isSawtooth()` returns true
- [ ] Semantic drift tested with off-topic prompt → distance < 0.6
- [ ] SIEM export is fire-and-forget — a SIEM failure must NOT fail the agent task
