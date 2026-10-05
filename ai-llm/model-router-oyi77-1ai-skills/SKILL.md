---
name: model-router
description: Use when route AI model requests to the optimal provider based on task,
  cost, latency, and capability requirements. Manage multi-provider LLM deployments.
  Use when working with model router.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- ai
- llm
- routing
- multi-provider
- cost-optimization
- model-selection
version: 1.0.0
category: core
---


# Model Router

## When to Use

**Trigger phrases:**
- "model router"
- "When managing multiple LLM providers (OpenAI, Anthropic, Google, etc"
- "When optimizing for cost vs quality tradeoffs"
- "When implementing fallback chains for reliability"


- When managing multiple LLM providers (OpenAI, Anthropic, Google, etc.)
- When optimizing for cost vs quality tradeoffs
- When implementing fallback chains for reliability
- When routing by task type (code to Claude, vision to Gemini, etc.)

## When NOT to Use

- For single-provider setups (just use that provider SDK)
- For local-only inference (use Ollama skills)

## Overview

Model routing is the intelligence layer between your application and the diverse landscape of large language model providers. Rather than hardcoding a single provider, a model router evaluates each request against dynamic criteria — task type, required capability, latency budget, cost ceiling, and current provider health — to select the optimal model at runtime. This transforms LLM integration from brittle point-to-point connections into a resilient, cost-aware system.

The core problem routing solves is that no single model dominates every dimension. Claude excels at code generation and structured reasoning, GPT-4o handles creative writing and multimodal tasks, Gemini-2.5-flash delivers the lowest latency for high-throughput workloads, and open-source models offer cost advantages for batch processing. Without routing, teams either overspend on premium models for trivial tasks or degrade quality by using cheap models everywhere. A router captures these trade-offs as programmable rules.

Production-grade routers implement three layers: static routing (model-per-task mapping), dynamic routing (cost/latency-aware selection with real-time metrics), and fallback chains (primary → secondary → tertiary on failure). Each layer adds resilience. When OpenAI experiences an outage, traffic shifts to Anthropic. When latency spikes on Claude, the router demotes it in favor of Gemini without any developer intervention.

Beyond simple selection, routers track cumulative cost, enforce per-workspace budgets, collect latency percentiles, and surface provider reliability trends. These metrics enable continuous optimization — A/B testing between model versions, gradual rollouts of new providers, and automated downgrades when spending exceeds thresholds.

A well-designed router decouples the application from individual model SDKs. Teams change model assignments through configuration, not code deploys. New providers plug in via a common interface. This architectural boundary is what allows fast iteration as the model landscape evolves.
## Workflow

1. **Inventory available models** — Catalog every model accessible across your providers. Record each model's capabilities (code, vision, reasoning, multilingual), pricing tier (input/output per 1K tokens), context window size, rate limits, and known limitations. Maintain this inventory as a structured configuration file, not scattered environment variables.

2. **Define routing rules** — Create a routing table that maps task types and constraints to ordered model lists. Rules can be simple (code→Claude, vision→Gemini) or compound (reasoning tasks under 4K tokens → GPT-4o-mini for cost savings, over 4K → Claude Opus for quality). Express constraints as cost ceilings, latency SLOs, and required capability flags.

3. **Implement provider abstraction** — Wrap each provider's SDK behind a common interface with methods for chat completion, streaming, embedding, and token counting. Normalize error types (rate limit, authentication, server error, timeout) so the router handles them uniformly. Implement retry with exponential backoff at this layer.

4. **Build fallback chains** — For each route, define a primary, secondary, and tertiary model. The router tries the primary first. On non-recoverable errors (auth failure, 4xx), it skips to the next. On transient errors (5xx, timeout, rate limit), it retries with backoff before falling through. Log every fallback event for reliability monitoring.

5. **Instrument cost and latency tracking** — Record per-request metrics: model used, input/output tokens, latency, cost, and fallback depth. Aggregate into periodic summaries (daily cost by provider, p50/p95/p99 latency per model, success rate per provider). Store in a time-series database or structured log sink for trend analysis.

6. **Configure health checks and circuit breakers** — Implement a health probe that periodically tests each provider with a lightweight request. Track consecutive failures. When failures exceed a threshold, trip a circuit breaker that excludes that provider from routing until a cooldown period expires. Circuit breaker state changes should trigger alerts.

7. **Optimize continuously** — Run A/B experiments comparing model versions within the same route (e.g., 50% traffic to GPT-4o, 50% to GPT-4.1). Measure quality via downstream signals (user ratings, task completion rate). Adjust routing weights based on empirical data. Add new models to low-risk routes first, then promote as confidence grows.
## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "One model is enough" | Different models excel at different tasks — routing optimizes quality for each use case |
| "I will use the cheapest model" | Cheap models fail on complex tasks — cost of failure (retries, bad output) exceeds savings |
| "Routing is over-engineering" | A 3-line fallback chain prevents 90% of LLM outages across your stack |
| "Latency is the only metric that matters" | Optimizing for latency alone ignores cost explosion and quality degradation. Use latency SLOs as boundaries, not optimization targets |
| "Provider lock-in doesn't matter" | Relying on a single provider means their rate limits, outages, and pricing changes become your availability and cost ceiling |
| "Add every new model immediately" | Untested models can have unexpected behavior, higher latency, or different output formatting. Validate in shadow mode before routing production traffic
## Code Example (TypeScript)

```typescript
const routes: Record<string, string[]> = {
  code: ['claude-sonnet-4-20250514', 'gpt-4o', 'gemini-2.5-pro'],
  vision: ['gemini-2.5-pro', 'gpt-4o', 'claude-sonnet-4-20250514'],
  fast: ['gemini-2.5-flash', 'gpt-4o-mini', 'claude-haiku'],
  creative: ['gpt-4o', 'claude-opus-4-20250514', 'gemini-2.5-pro'],
};

async function routeRequest(task: string, prompt: string) {
  const models = routes[task] || routes.fast;
  for (const model of models) {
    try {
      return await callModel(model, prompt);
    } catch (e) {
      console.warn(`${model} failed, trying next...`);
    }
  }
  throw new Error('All models failed');
}
```


## Code Example (Python)

```python
import time
import logging
from typing import Any

# Router configuration with cost tracking
ROUTES = {
    "code": ["claude-sonnet-4", "gpt-4o", "gemini-2.5-pro"],
    "vision": ["gemini-2.5-pro", "gpt-4o", "claude-sonnet-4"],
    "fast": ["gemini-2.5-flash", "gpt-4o-mini"],
    "creative": ["gpt-4o", "claude-opus-4", "gemini-2.5-pro"],
}

COST_PER_1K_TOKENS = {
    "gpt-4o": (0.01, 0.03),        # (input, output)
    "gpt-4o-mini": (0.0015, 0.006),
    "claude-sonnet-4": (0.003, 0.015),
    "claude-opus-4": (0.015, 0.075),
    "gemini-2.5-pro": (0.01, 0.04),
    "gemini-2.5-flash": (0.0005, 0.0015),
}

class CostAwareRouter:
    """Routes requests with cost tracking and latency budgets."""

    def __init__(self, latency_budget_s: float = 5.0):
        self.latency_budget_s = latency_budget_s
        self.stats: dict[str, list[dict[str, Any]]] = {}

    async def route(self, task: str, prompt: str) -> str:
        models = ROUTES.get(task, ROUTES["fast"])
        for model in models:
            start = time.monotonic()
            try:
                result = await self._call_model(model, prompt)
                elapsed = time.monotonic() - start
                self._record(model, elapsed, "success")
                if elapsed > self.latency_budget_s:
                    logging.warning("%s within budget but exceeded latency SLO", model)
                return result
            except Exception as exc:
                elapsed = time.monotonic() - start
                self._record(model, elapsed, f"fail:{type(exc).__name__}")
                logging.warning("Fallback from %s after %.1fs", model, elapsed)
        raise RuntimeError("All models exhausted")

    def _record(self, model: str, latency: float, status: str) -> None:
        self.stats.setdefault(model, []).append({
            "latency": round(latency, 3),
            "status": status,
            "timestamp": time.time(),
        })

    def report(self) -> dict[str, Any]:
        summary = {}
        for model, records in self.stats.items():
            success = [r for r in records if r["status"] == "success"]
            summary[model] = {
                "total": len(records),
                "success": len(success),
                "avg_latency": round(sum(r["latency"] for r in success) / len(success), 3) if success else None,
            }
        return summary
```


## Setup / Configuration

### Provider Credentials

Store provider API keys in environment variables or a secrets manager, never in code. Define a common interface that all providers implement:

```python
import os
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    async def chat(self, model: str, messages: list, **kwargs) -> dict:
        ...
```

### Model Inventory Config

Maintain a structured configuration file that maps model IDs to their capabilities, pricing, and rate limits:

```yaml
# models.yaml
models:
  claude-sonnet-4:
    provider: anthropic
    capabilities: [code, reasoning, structured-output]
    context_window: 200000
    input_price_per_1k: 0.003
    output_price_per_1k: 0.015
    rate_limit_rpm: 1000
  gpt-4o:
    provider: openai
    capabilities: [vision, creative-writing, multilingual]
    context_window: 128000
    input_price_per_1k: 0.01
    output_price_per_1k: 0.03
    rate_limit_rpm: 500
  gemini-2.5-flash:
    provider: google
    capabilities: [fast, multilingual, vision]
    context_window: 1048576
    input_price_per_1k: 0.0005
    output_price_per_1k: 0.0015
    rate_limit_rpm: 2000
```

### Routing Table

Define routing rules in a separate config section that maps task types to ordered model lists with constraint annotations:

```yaml
routes:
  code:
    models: [claude-sonnet-4, gpt-4o, gemini-2.5-pro]
    max_cost_per_request: 0.05
    required_capabilities: [code, reasoning]
  vision:
    models: [gemini-2.5-pro, gpt-4o, claude-sonnet-4]
    required_capabilities: [vision, multilingual]
  fast:
    models: [gemini-2.5-flash, gpt-4o-mini]
    max_latency_ms: 2000
    max_cost_per_request: 0.003
```

### Dependencies

Install the provider SDKs your router supports:

```bash
pip install openai anthropic google-generativeai
# Or for Node.js:
npm install openai @anthropic-ai/sdk @google/generative-ai
```

## Common Issues / Troubleshooting

| Issue | Root Cause | Solution |
|---|---|---|
| All models in chain fail | Provider credentials misconfigured or expired | Verify each provider API key independently before integrating into router |
| High latency on fallback | Secondary/tertiary models are slower than primary | Reorder fallback chains so the fastest model is primary; use latency SLOs to disqualify models mid-flight |
| Cost overruns despite routing rules | Hardcoded model selection bypasses the router | Audit all code paths that call provider SDKs directly; redirect through the router |
| Circuit breaker never trips | Health probe is too lenient or interval too long | Set conservative thresholds (3 consecutive failures, 30s probe interval) and test with a known-bad endpoint |
| Router returns different results for same input | Load balancing across models with different output styles | Pin session or user to a specific model variant, or normalize outputs through a post-processing step |
| Rate limit errors cascade through fallback | All models in the chain share the same underlying infrastructure | Spread fallback models across independent providers (not just different models from the same provider) |
## Process

### Preparation

- **Inventory audit**: Run a provider discovery scan to confirm all expected models are accessible. Test each provider credential with a minimal request before wiring into the router.
- **Define SLOs**: Establish latency budgets (e.g., p95 < 5s), cost ceilings (e.g., $0.01 per request max), and reliability targets (e.g., 99.9% provider uptime before fallback).
- **Select routing strategy**: Choose between static routing (fixed model per task), dynamic routing (real-time cost/latency optimization), or hybrid (static defaults with dynamic fallback).
- **Set up monitoring**: Configure structured logging for every routing decision, provider latency percentile tracking, and cost accumulation sinks.

### Execution

- Deploy the router behind your application's LLM abstraction layer. Start with a single route and one fallback model.
- Route all LLM traffic through the router. Verify routing decisions match your configuration by inspecting decision logs.
- Monitor fallback rates — if fallback exceeds 5% of traffic, investigate the primary provider's health before the circuit breaker trips.
- Stream responses through the router so fallback transitions are invisible to end users. The router should buffer intermediate state so a retry on a new model resumes from the last user message.

### Stewardship

- Review cost and latency reports weekly. Rebalance routes when a cheaper model achieves comparable quality on a task.
- Update the model inventory as new provider versions release. Run shadow comparisons (route 5% traffic to the new model, measure quality) before promoting.
- Rotate API keys on a schedule. Coordinate key rotation with the router's credential store to avoid 401 errors during active traffic.
- Maintain a runbook for each provider outage scenario: expected behavior, alert thresholds, manual override procedures.

## Verification

- [ ] Routes correctly by task type — all configured task-to-model mappings dispatch to the expected provider
- [ ] Fallback triggers on primary failure — inject a fake 5xx or timeout, confirm secondary model handles the request within the SLO
- [ ] Cost tracking accurate per request — compare router-reported cost against provider billing API for a sample of requests
- [ ] Latency within acceptable bounds — p50 and p95 latency per model stay under configured SLOs
- [ ] No single point of failure — all providers can be removed from routing without blocking traffic
- [ ] Circuit breaker trips and recovers — after N consecutive failures, provider is excluded; after cooldown, it resumes
- [ ] Auth failure skips immediately — 401/403 errors do not trigger retry, fall through to next model directly
- [ ] Cross-provider fallback works — simulate total outage of one provider, verify traffic redirects to a different provider entirely
- [ ] Streaming fallback preserves state — if primary fails mid-stream, the new model receives the full conversation context

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Model Router as a Service | 2-3 months | Offer a managed routing API that handles provider failover, cost optimization, and latency management for teams that don't want to build their own. Charge per-request or monthly flat fee based on request volume. |
| Open-core with enterprise tier | 3-6 months | Release the basic router as open source (MIT/Apache-2.0), sell enterprise features: advanced circuit breakers, shadow-mode testing dashboards, multi-workspace cost reporting, and custom routing logic plugins. |
| Consulting: Router deployment & tuning | Ongoing | Help mid-size engineering teams design, deploy, and tune their model routing infrastructure. Deliverable: working router with monitoring dashboards, plus a routing rules playbook. Typical engagement 4-6 weeks. |
| Router observability add-on | 4-8 months | Build a dedicated analytics product that ingests router telemetry and provides cost anomaly detection, provider SLA dashboards, and automated routing optimization recommendations. Sell as a SaaS add-on to router deployments. |
| Embedded routing SDK | 6-12 months | License the router as a drop-in SDK for product platforms (chatbot builders, AI coding tools, workflow automation). Charge per-seat or per-active-model per month with usage tiers based on monthly API call volume. |
| Training & workshops | Ongoing | Deliver half-day and full-day workshops on LLM routing architecture, provider selection strategy, and production monitoring. Target: engineering teams adopting multi-provider AI stacks. |
