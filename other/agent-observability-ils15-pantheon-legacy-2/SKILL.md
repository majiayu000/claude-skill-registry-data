---
name: agent-observability
description: "Observability with OpenTelemetry, metrics, and logging. Use for monitoring agents and LLM calls."
context: fork
globs: ["**/*.py", "**/docker-compose*", "**/Dockerfile"]
alwaysApply: false
---

# Agent Observability & Monitoring Skill

## When to Use

Implement this skill when your multi-agent system needs observability across agent spans, LLM calls, token costs, latency, error rates, and alerting. Covers the full stack: trace export → metrics collection → structured logging → dashboards → incident response.

## OpenTelemetry Tracing

### Span Creation & Context Propagation

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind, Status, StatusCode
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.propagate import inject, extract
import json

resource = Resource.create({"service.name": "agent-orchestrator"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://jaeger:4317"))
)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

class AgentTracer:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.tracer = trace.get_tracer(agent_name)

    async def trace_agent_run(self, task: dict) -> dict:
        with self.tracer.start_as_current_span(
            f"agent.{self.agent_name}.run",
            kind=SpanKind.SERVER,
            attributes={
                "agent.name": self.agent_name,
                "task.id": task.get("id"),
                "task.type": task.get("type", "unknown"),
            },
        ) as span:
            try:
                result = await self._execute(task)
                span.set_attribute("result.status", "success")
                span.set_attribute("result.length", len(str(result)))
                return result
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise

    async def _execute(self, task: dict) -> dict:
        with self.tracer.start_as_current_span(
            f"agent.{self.agent_name}.execute",
            kind=SpanKind.INTERNAL,
            attributes={"task.priority": task.get("priority", 0)},
        ) as span:
            spans = await self._llm_call(task["prompt"])
            return spans
```

### Agent Span Hierarchy

```python
async def orchestrate_workflow(request: dict, headers: dict) -> dict:
    ctx = extract(headers)
    with tracer.start_as_current_span(
        "orchestrator", context=ctx, kind=SpanKind.SERVER
    ) as root:
        root.set_attribute("request.id", request["id"])

        with tracer.start_as_current_span("agent.hermes.run") as hermes_span:
            hermes_result = await hermes.process(request["query"])
            hermes_span.set_attribute("tokens", hermes_result["tokens"])

        with tracer.start_as_current_span("agent.aphrodite.run") as aphro_span:
            aphro_result = await aphrodite.render(hermes_result["data"])
            aphro_span.set_attribute("components", len(aphro_result["ui"]))

        root.set_attribute("total.duration_ms", root.end_time - root.start_time)
        return {"result": hermes_result, "ui": aphro_result}
```

## LLM Call Tracing with LangSmith

```python
from langsmith import Client, traceable
from langsmith.run_trees import RunTree
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

client = Client()

@traceable(
    project_name="agent-hermes",
    tags=["production", "hermes-v2"],
    metadata={"agent": "hermes", "version": "2.1.0"},
)
async def agent_llm_call(prompt: str, context: dict) -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    messages = [
        SystemMessage(content="You are Hermes, a backend agent."),
        HumanMessage(content=prompt),
    ]
    response = await llm.ainvoke(messages)
    return response.content

@traceable(run_type="chain", name="hermes_full_flow")
async def hermes_plan_and_generate(task: str) -> dict:
    plan = await agent_llm_call(f"Plan implementation for: {task}")
    code = await agent_llm_call(f"Generate code for plan: {plan}")
    return {"plan": plan, "code": code}
```

### Custom Traces & Feedback

```python
async def trace_with_feedback(task_id: str, user_input: str, output: str) -> None:
    run = RunTree(
        name="agent-qa",
        run_type="chain",
        inputs={"task_id": task_id, "query": user_input},
        tags=["qa-review"],
    )
    with run:
        child_llm = run.create_child(
            name="llm_check",
            run_type="llm",
            inputs={"prompt": user_input},
            outputs={"response": output},
        )
        child_llm.end()
    run.end()
    client.create_run(**run.dict())

    client.create_feedback(
        run_id=run.id,
        key="user_rating",
        score=0.95,
        comment="Answer was accurate and well-structured",
    )
```

## Token & Cost Tracking

### Token Counters

```python
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0

MODEL_PRICING = {
    "gpt-4o": {"input": 2.50 / 1_000_000, "output": 10.00 / 1_000_000},
    "gpt-4o-mini": {"input": 0.15 / 1_000_000, "output": 0.60 / 1_000_000},
    "claude-sonnet-4": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
    "claude-haiku": {"input": 0.25 / 1_000_000, "output": 1.25 / 1_000_000},
}

class TokenTracker:
    def __init__(self):
        self._usage: dict[str, dict[str, TokenUsage]] = defaultdict(
            lambda: defaultdict(TokenUsage)
        )

    def record(
        self,
        agent: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        feature: str = "general",
    ) -> TokenUsage:
        pricing = MODEL_PRICING.get(model, {"input": 0, "output": 0})
        cost = (input_tokens * pricing["input"]) + (output_tokens * pricing["output"])
        usage = TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost_usd=round(cost, 6),
        )
        self._usage[agent][feature] = usage

        with tracer.start_as_current_span("token.record") as span:
            span.set_attribute("token.agent", agent)
            span.set_attribute("token.model", model)
            span.set_attribute("token.input", input_tokens)
            span.set_attribute("token.output", output_tokens)
            span.set_attribute("token.cost", cost)

        return usage

    def total_cost(self, agent: Optional[str] = None) -> float:
        if agent:
            return sum(u.cost_usd for u in self._usage[agent].values())
        return sum(
            u.cost_usd
            for agent_usage in self._usage.values()
            for u in agent_usage.values()
        )

    def budget_alert(self, budget_usd: float, agent: Optional[str] = None) -> list[str]:
        alerts = []
        if agent:
            cost = self.total_cost(agent)
            if cost > budget_usd:
                alerts.append(f"{agent} cost ${cost:.2f} exceeds budget ${budget_usd:.2f}")
        else:
            for a in self._usage:
                cost = self.total_cost(a)
                if cost > budget_usd / len(self._usage):
                    alerts.append(f"{a} cost ${cost:.2f} exceeds proportional budget")
        return alerts

tracker = TokenTracker()

usage = tracker.record("hermes", "gpt-4o", input_tokens=1500, output_tokens=420, feature="code-gen")
print(f"Cost: ${usage.cost_usd:.4f}, Budget alerts: {tracker.budget_alert(10.0)}")
```

## Agent Performance Metrics

### Prometheus Counters & Histograms

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
from contextlib import asynccontextmanager
import time

agent_calls = Counter(
    "agent_calls_total",
    "Total agent LLM calls",
    ["agent", "model", "status"],
)

agent_latency = Histogram(
    "agent_latency_seconds",
    "Agent call latency in seconds",
    ["agent", "operation"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
)

agent_tokens = Counter(
    "agent_tokens_total",
    "Total tokens consumed",
    ["agent", "direction"],
)

agent_cost = Counter(
    "agent_cost_usd_total",
    "Total cost in USD",
    ["agent", "model"],
)

agent_errors = Counter(
    "agent_errors_total",
    "Agent errors by type",
    ["agent", "error_type"],
)

agent_concurrent = Gauge(
    "agent_concurrent_requests",
    "Current concurrent agent requests",
    ["agent"],
)

@asynccontextmanager
async def track_agent_call(agent: str, model: str, operation: str):
    agent_concurrent.labels(agent=agent).inc()
    start = time.monotonic()
    try:
        yield
        agent_calls.labels(agent=agent, model=model, status="success").inc()
    except Exception as e:
        agent_calls.labels(agent=agent, model=model, status="error").inc()
        agent_errors.labels(agent=agent, error_type=type(e).__name__).inc()
        raise
    finally:
        duration = time.monotonic() - start
        agent_latency.labels(agent=agent, operation=operation).observe(duration)
        agent_concurrent.labels(agent=agent).dec()

async def agent_handler(agent: str, model: str, prompt: str) -> str:
    async with track_agent_call(agent, model, "llm_invoke"):
        response = await llm_call(prompt)
        token_count = len(response.split())
        agent_tokens.labels(agent=agent, direction="output").inc(token_count)
        agent_cost.labels(agent=agent, model=model).inc(
            token_count * MODEL_PRICING[model]["output"]
        )
        return response
```

### Drift Detection

```python
from collections import deque
import statistics

class LatencyDriftDetector:
    def __init__(self, window: int = 100, threshold: float = 2.0):
        self.window = deque(maxlen=window)
        self.threshold = threshold

    def record(self, latency: float) -> Optional[float]:
        self.window.append(latency)
        if len(self.window) < 30:
            return None
        mean = statistics.mean(self.window)
        std = statistics.stdev(self.window)
        z_score = (latency - mean) / max(std, 1e-6)
        if abs(z_score) > self.threshold:
            return z_score
        return None

drift = LatencyDriftDetector()
latency = 3.2
score = drift.record(latency)
if score:
    logger.warning(f"Latency drift detected: z-score={score:.2f}, latency={latency:.2f}s")
```

## Structured Logging

```python
import json
import logging
import re
from datetime import datetime, timezone
from uuid import uuid4

SENSITIVE_PATTERNS = [
    (re.compile(r'"api_key":\s*"[^"]+"'), '"api_key": "***REDACTED***"'),
    (re.compile(r'"password":\s*"[^"]+"'), '"password": "***REDACTED***"'),
    (re.compile(r'"token":\s*"[^"]+"'), '"token": "***REDACTED***"'),
    (re.compile(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b'), '***UUID-REDACTED***'),
]

class JSONFormatter(logging.Formatter):
    def __init__(self, agent_name: str):
        super().__init__()
        self.agent_name = agent_name

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "agent": self.agent_name,
            "correlation_id": getattr(record, "correlation_id", ""),
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }
        if hasattr(record, "extra_data"):
            log_entry["extra"] = record.extra_data
        raw = json.dumps(log_entry, default=str)
        for pattern, replacement in SENSITIVE_PATTERNS:
            raw = pattern.sub(replacement, raw)
        return raw

def setup_agent_logger(agent_name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(f"agent.{agent_name}")
    logger.setLevel(level)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter(agent_name))
    logger.handlers.clear()
    logger.addHandler(handler)

    correlation_id = str(uuid4())
    logger = logging.LoggerAdapter(logger, {"correlation_id": correlation_id})
    return logger

hermes_logger = setup_agent_logger("hermes", logging.DEBUG)
hermes_logger.info("Agent initialized", extra={"extra_data": {"model": "gpt-4o", "version": "2.1.0"}})
hermes_logger.error("LLM call failed", extra={"extra_data": {"tokens_used": 1500, "retry": 3}})
```

## Alerting

### Alertmanager Configuration

```yaml
# alertmanager.yml
route:
  receiver: "pagerduty-critical"
  routes:
    - match:
        severity: critical
      receiver: "pagerduty-critical"
      continue: true
    - match:
        severity: warning
      receiver: "slack-alerts"
    - match:
        severity: info
      receiver: "log-only"

receivers:
  - name: "pagerduty-critical"
    pagerduty_configs:
      - routing_key: "${PAGERDUTY_ROUTING_KEY}"
        severity: critical
        description: "Agent system alert - {{ .GroupLabels.alertname }}"

  - name: "slack-alerts"
    slack_configs:
      - api_url: "${SLACK_WEBHOOK_URL}"
        channel: "#agent-alerts"
        title: "{{ .GroupLabels.alertname }}"
        text: "{{ .CommonAnnotations.summary }}"
```

### Prometheus Alert Rules

```yaml
# alerts/agent_alerts.yml
groups:
  - name: agent_observability
    rules:
      - alert: HighAgentLatency
        expr: histogram_quantile(0.95, rate(agent_latency_seconds_bucket[5m])) > 10
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "P95 latency > 10s for agent {{ $labels.agent }}"

      - alert: HighErrorRate
        expr: |
          rate(agent_calls_total{status="error"}[5m])
          /
          rate(agent_calls_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate > 5% for agent {{ $labels.agent }}"

      - alert: CostAnomaly
        expr: |
          rate(agent_cost_usd_total[1h])
          /
          avg(rate(agent_cost_usd_total[24h])) > 3
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "Cost spike 3x above 24h average for {{ $labels.agent }}"

      - alert: TokenRateSpike
        expr: rate(agent_tokens_total[5m]) > 100000
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Token rate > 100K/5m for {{ $labels.agent }}"

      - alert: AgentDeadlock
        expr: |
          agent_concurrent_requests > 20
          and
          rate(agent_calls_total[5m]) < 0.1
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "Agent {{ $labels.agent }} has 20+ concurrent requests but no completions in 30s"

      - alert: BudgetExceeded
        expr: agent_cost_usd_total > 50
        labels:
          severity: warning
        annotations:
          summary: "Agent {{ $labels.agent }} exceeded $50 daily budget"

      - alert: NoTraces
        expr: rate(agent_calls_total[10m]) == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "No agent calls detected for 10 minutes - possible pipeline failure"
```

## Dashboards

### Grafana Panels

```json
{
  "title": "Agent Observability",
  "panels": [
    {
      "title": "Agent Throughput",
      "type": "timeseries",
      "targets": [{
        "expr": "rate(agent_calls_total{status=\"success\"}[5m])",
        "legendFormat": "{{ agent }} - {{ status }}"
      }],
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 0}
    },
    {
      "title": "LLM Cost by Agent (24h)",
      "type": "barchart",
      "targets": [{
        "expr": "sum by(agent) (increase(agent_cost_usd_total[24h]))",
        "legendFormat": "{{ agent }}"
      }],
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 0}
    },
    {
      "title": "Token Consumption Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "rate(agent_tokens_total[5m])",
        "legendFormat": "{{ agent }} - {{ direction }}"
      }],
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 8}
    },
    {
      "title": "Latency Percentiles",
      "type": "stat",
      "targets": [
        {"expr": "histogram_quantile(0.50, rate(agent_latency_seconds_bucket[5m]))", "legendFormat": "P50"},
        {"expr": "histogram_quantile(0.95, rate(agent_latency_seconds_bucket[5m]))", "legendFormat": "P95"},
        {"expr": "histogram_quantile(0.99, rate(agent_latency_seconds_bucket[5m]))", "legendFormat": "P99"}
      ],
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 8}
    },
    {
      "title": "Error Rate",
      "type": "timeseries",
      "targets": [{
        "expr": "rate(agent_calls_total{status=\"error\"}[5m]) / rate(agent_calls_total[5m])",
        "legendFormat": "{{ agent }}"
      }],
      "gridPos": {"h": 8, "w": 12, "x": 0, "y": 16}
    },
    {
      "title": "Concurrent Requests",
      "type": "timeseries",
      "targets": [{
        "expr": "agent_concurrent_requests",
        "legendFormat": "{{ agent }}"
      }],
      "gridPos": {"h": 8, "w": 12, "x": 12, "y": 16}
    }
  ]
}
```

## Incident Response

### Trace → Log → Metrics Correlation

```python
import structlog
from opentelemetry import trace

async def incident_correlation(alert_name: str, labels: dict) -> dict:
    correlation_id = str(uuid4())
    logger = structlog.get_logger()
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span(f"incident.{alert_name}") as span:
        span.set_attribute("correlation_id", correlation_id)
        span.set_attribute("alert.name", alert_name)
        span.set_attributes(labels)

        logger.error(
            "incident_triggered",
            correlation_id=correlation_id,
            alert=alert_name,
            agent=labels.get("agent"),
        )

        metrics = await query_prometheus(
            f'rate(agent_calls_total{{agent="{labels.get("agent")}"}}[5m])'
        )
        span.set_attribute("metrics.query_result", str(metrics))

        recent_logs = await query_loki(
            f'{{agent="{labels.get("agent")}"}} |= "{correlation_id}"'
        )
        span.set_attribute("logs.matched", len(recent_logs))

        root_cause = await diagnose_root_cause(alert_name, labels, metrics, recent_logs)

        if root_cause["severity"] == "critical" and root_cause.get("auto_rollback"):
            await rollback_deployment(labels.get("agent"))
            logger.warning("auto_rollback_triggered", agent=labels.get("agent"))

        return root_cause

async def diagnose_root_cause(
    alert: str, labels: dict, metrics: dict, logs: list
) -> dict:
    error_rate = metrics.get("error_rate", 0)
    latency = metrics.get("p95_latency", 0)

    diagnosis = {"severity": "info", "cause": "unknown", "recommendation": ""}

    if error_rate > 0.1:
        diagnosis.update(
            severity="critical",
            cause="high_error_rate",
            recommendation="Rollback last agent deployment. Check model API status.",
        )
    elif latency > 30:
        diagnosis.update(
            severity="warning",
            cause="latency_regression",
            recommendation="Scale agent replicas. Check for prompt length increases.",
        )
    elif "rate_limit" in str(logs).lower():
        diagnosis.update(
            severity="warning",
            cause="rate_limited",
            recommendation="Implement exponential backoff. Reduce concurrency.",
        )
    return diagnosis

async def rollback_deployment(agent: str) -> None:
    logger = structlog.get_logger()
    logger.warning("rollback_initiated", agent=agent)
    span = trace.get_current_span()
    span.add_event("rollback.started", {"agent": agent})
```

### Complete Monitoring Setup

```python
from fastapi import FastAPI, Request
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from prometheus_client import make_asgi_app
import structlog

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()

@app.middleware("http")
async def observability_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-Id", str(uuid4()))
    with tracer.start_as_current_span(
        f"http.{request.method}.{request.url.path}",
        attributes={"correlation_id": correlation_id},
    ):
        response = await call_next(request)
        response.headers["X-Correlation-Id"] = correlation_id
        return response

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "metrics_endpoint": "/metrics",
        "trace_endpoint": "http://jaeger:16686",
    }

# Usage: app starts with OpenTelemetry SDK, Prometheus /metrics, structured logging
# Alertmanager watches Prometheus rules, PagerDuty/Slack on critical, Grafana dashboards
```

## Real-World Checklist
- [ ] OpenTelemetry SDK configured with exporter (Jaeger/Honeycomb/OTLP)
- [ ] All agent spans created with proper parent-child hierarchy
- [ ] LangSmith tracing enabled for LLM calls with metadata tags
- [ ] Token counters per agent per model with cost attribution
- [ ] Budget alerts configured (per-agent and global thresholds)
- [ ] Prometheus histograms for P50/P95/P99 latency per operation
- [ ] Error counters by agent and error type
- [ ] Structured JSON logging with correlation IDs across all agents
- [ ] Sensitive data redaction in logs (API keys, tokens, passwords)
- [ ] Alertmanager rules for latency spikes, error rates, cost anomalies, deadlock detection
- [ ] Grafana dashboard with throughput, costs, error rates, concurrent requests
- [ ] Incident response playbook with trace-log-metrics correlation
- [ ] Auto-rollback triggers for critical error rate thresholds
- [ ] Metrics endpoint exposed and scraped by Prometheus
