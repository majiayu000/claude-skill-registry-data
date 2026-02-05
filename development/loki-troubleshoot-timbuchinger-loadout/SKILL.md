---
name: loki-troubleshoot
description: "Help craft efficient Grafana Loki / LogQL queries for debugging logs — with label‑based filtering, narrow time windows, and best‑practice guidance to avoid expensive or overly broad scans."
---

# Loki Troubleshooting & Query‑Builder Skill

## What this Skill does

When a user asks you (Claude) for help inspecting logs via Loki — e.g. “find errors in service X”, “search for request_id=abc123”, “show me 500 responses between 2‑3 PM last night” — use this skill to:

- Ask clarifying questions if needed (e.g. which service / label context, approx time window, any known label names).  
- Build a recommended LogQL query that:  
  - uses **low‑cardinality labels** (service, env, host, etc.) whenever possible  
  - confines to a **narrow time window** (minutes — hours, not days) by default  
  - uses **fast filters** (`|=` or `|!=`) rather than regex or heavy parsing  
  - performs JSON/structured parsing only *after* filtering  
- Provide human-readable explanations and **warnings** for expensive queries  
- Suggest alternative strategies (metrics, recording rules, structured logs)

## Best Practices

- Prefer stable labels (`app`, `env`, `namespace`, `cluster`, etc.)  
- Avoid high-cardinality labels (`user_id`, `request_id`, UUIDs)  
- Always restrict the **time window**  
- Use `|=` before regex or parsing  
- Provide warnings for:  
  - No label selector  
  - Very wide time windows  
  - JSON parse without pre-filter  
  - Regex-heavy queries  

## Example Queries

| User Request                                                                                     | Resulting LogQL                                  |
|--------------------------------------------------------------------------------------------------|--------------------------------------------------|
| "Show me all 500 errors in the `orders` service in the last 2 hours."                            | `{app="orders", env="prod"}[2h] \|= "500"`        |
| "Find logs for request_id `abc123` in staging for `payments` service over past 30 minutes."      | `{app="payments", env="staging"}[30m] \|= "abc123"` |

## Limitations

- This skill does not execute queries
