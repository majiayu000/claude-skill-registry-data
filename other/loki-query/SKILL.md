---
name: loki-query
description: Query Grafana Loki logs and metadata via HTTP API (LogQL)
activation_keywords: [loki, logql, logs, grafana loki, label, series]
execution_mode: server
---

# Loki Query Skill

Calls Loki’s HTTP API (read-only):

- `query` — instant LogQL query
- `query_range` — range query (use `start` / `end`, optional `limit`, `step`)
- `labels` — label names
- `label_values` — values for a `label`
- `series` — series matching `match` selector

Parameters: `loki_url` (default `http://localhost:3100`), optional `bearer_token`.

Tool name: `builtin_loki_query`.
