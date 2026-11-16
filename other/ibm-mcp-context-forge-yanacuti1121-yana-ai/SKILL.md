---
name: ibm--mcp-context-forge
description: "IBM ContextForge — MCP Gateway + registry: federate MCP servers + A2A + REST/gRPC qua 1 endpoint. OTel tracing, JWT auth, RBAC, 7000+ tests. Production-ready."
allowed-tools: Bash, Read, Write
user-invocable: true
---

ContextForge (IBM): MCP gateway tập trung — federate nhiều MCP servers, REST APIs, gRPC services qua một managed endpoint với auth, rate limiting, tracing.

## Install

```bash
# PyPI
pip install mcp-contextforge-gateway

# Docker
docker run ghcr.io/ibm/mcp-context-forge:1.0.0-RC-3

# Kubernetes (Helm)
helm install contextforge ./charts/contextforge
```

## 3 Gateway Layers

```
Tools Gateway   — MCP servers + REST-to-MCP translation
Agent Gateway   — A2A protocol + OpenAI/Anthropic agent routing
API Gateway     — rate limiting + auth + retries + reverse proxy
```

## gRPC → MCP Auto-Translation

```python
# Service reflection auto-converts gRPC → MCP tools
# Không cần viết wrapper thủ công
```

## Unified Registries

```
Prompts   — Jinja2 templating + versioning
Resources — URI-based + caching + SSE updates
Tools     — native hoặc adapted, input validation
```

## Observability

```python
# OpenTelemetry tracing — any OTLP backend
# Phoenix, Jaeger, Zipkin compatible
# Distributed tracing qua federated gateways
# Automatic instrumentation: tools + resources + operations
```

## Security

```
JWT authentication
RBAC (role-based access control)
Cross-gateway routing via domain allowlist
Strong JWT secret + admin credentials required
```

## Admin UI

HTMX + Alpine.js — real-time management, config, log monitoring. Airgapped support.

## Khi nào dùng

- Nhiều MCP servers cần manage tập trung
- Cần auth/rate-limit trước khi expose MCP tools
- Enterprise: multi-cluster federation + auto-scaling
- Muốn OTel tracing xuyên suốt MCP tool calls

## Source

https://github.com/IBM/mcp-context-forge · Apache-2.0
