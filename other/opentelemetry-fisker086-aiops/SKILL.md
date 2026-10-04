---
name: opentelemetry
description: Query OpenTelemetry traces and services from Jaeger/Tempo
activation_keywords: [opentelemetry, jaeger, tempo, tracing, trace, span, observability]
execution_mode: server
---

# OpenTelemetry Skill

Provides read-only trace querying via Jaeger or Tempo HTTP API:
- List services
- List traces for a service
- Get trace details by trace ID
- Search traces by tags and time range
- Get service operations

Use `builtin_opentelemetry` tool with fields:
- `operation`: one of "list_services", "list_traces", "get_trace", "search_traces", "list_operations"
- `service`: service name (required for list_traces/search_traces/list_operations)
- `trace_id`: trace ID (required for get_trace)
- `trace_url`: Jaeger or Tempo query URL (default: http://localhost:16686 for Jaeger, http://localhost:3200 for Tempo)
- `backend`: trace backend type ("jaeger" or "tempo", default: "jaeger")
- `tags`: query tags (for search_traces, e.g. "http.status_code=500")
- `limit`: max results (default: 20)
- `start`, `end`: time range (Unix timestamp in seconds)

Note: All operations are read-only.
