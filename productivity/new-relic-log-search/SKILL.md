---
name: new-relic-log-search
description: Search New Relic logs, discover matching services, count errors, and compile deduplicated production errors. Use when the user asks about New Relic logs, log counts, errors, production logs, or service/project-specific failures.
---

# New Relic Log Search

Use New Relic account_id `3393970` by default.

For project-specific log requests, first discover matching services instead of assuming the service name.

```sql
SELECT count(*)
FROM Log
WHERE service IS NOT NULL
SINCE 30 minutes ago
FACET service, app, entity.name, env
LIMIT MAX
```

Match the user's project name against discovered `service`, `app`, or `entity.name` values. If multiple obvious variants match, include all of them.

For production logs, inspect env values for the matched services first. Treat production as `env LIKE 'prod%'` unless discovery shows a different convention.

Search every replica and revision relevant to the window. Absence from one worker's log stream is not absence, and queue depth zero does not prove completion. Facet by task, container, host, or revision fields when they are available.

Before proposing a code or provider-endpoint change, extract the exact exception class, HTTP status, message, and provider response. Keep missing evidence explicit instead of inferring it from a wrapper exception.

Structured logs often keep their text in attributes rather than `message`, so match the attribute fields (for example `filter_keys IS NOT NULL`). Logs UI links drop filters: share the NRQL with the message ID. A log line from a fallback path does not by itself confirm a leak.

For CMC production shell access, use the established Copilot/ECS workflow. Do not suggest Kubernetes unless the user explicitly identifies Kubernetes.

For error logs, use this filter:

```sql
level IN ('error', 'ERROR', 'Error')
```

For deduplicated errors, group by message or log pattern, then normalize volatile values like timestamps, request IDs, UUIDs, memory addresses, parser object IDs, numeric offsets, and generated IDs.
