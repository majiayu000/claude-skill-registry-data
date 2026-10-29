---
name: cloudflare-costs
description: >
  Estimate Cloudflare spend per project (Worker) for the current month: Workers requests and CPU,
  Durable Objects requests and duration, KV, R2, D1 and Workers AI. Reads usage from the GraphQL
  Analytics API and applies list prices, so it works when account credits make the invoice $0.
  Use when asked what Cloudflare costs, which project spends the most, monthly spend reports,
  billed usage per project, or to check a cost fix (DO hibernation, KV writes) after deploy.
---

# cloudflare-costs

Account credits hide the real bill. This skill reads **usage** and multiplies it by **list prices**, per project.

```
cf auth whoami (refreshes OAuth token)
  ──▶ Workers API: bindings of every script ──▶ KV / R2 / D1 resource → project
  ──▶ GraphQL Analytics: usage per script, DO namespace, KV namespace, bucket, database
  ──▶ list prices × usage, scaled to a full month ──▶ markdown table per project
```

## Run the report

```bash
bun ~/.config/opencode/skills/cloudflare-costs/cost-report.ts                 # month to date
bun ~/.config/opencode/skills/cloudflare-costs/cost-report.ts --from 2026-10-01 --to 2026-10-20
bun ~/.config/opencode/skills/cloudflare-costs/cost-report.ts --json > /tmp/costs.json   # per-metric usage and cost
```

- **Project** = Worker script name without `-preview` / `-production` / `-staging`.
- A KV namespace, R2 bucket or D1 database bound to several projects is **split evenly**. Unbound resources show as `(unbound) ...`.
- Usage is **scaled** to the full calendar month. Storage (KV, R2, D1 GB-month) is not scaled.
- The account free tier is subtracted once from the total (`net`), not per project.
- Use full past days for `--to` when comparing before/after a fix; today is partial and data lags minutes.

If `cf auth whoami` fails, ask the user to run `cf auth login` (device flow; give them the code it prints).

## Try the real invoice first

`cf billing usage query` returns billable usage, but needs the `billing:read` scope (cf ≥ 1.0.0-beta.18 asks for it by default; older logins do not have it). If it returns 403/405, use the report above.

## Pricing rules the script encodes

| product | billed metric | gotcha |
|---|---|---|
| Workers | requests $0.30/M, CPU $0.02/M ms | subrequests and static assets are free; a WebSocket is 1 request at Upgrade |
| DO requests | $0.15/M | invocation `type: hibernation` = incoming WS messages, billed **20:1**; `http`/`rpc`/alarm count 1:1 |
| DO duration | `activeTime_µs / 1e6 × 0.128 GB × $12.50/M` | one DO awake 24/7 ≈ $3.40/month; protocol pings and `setWebSocketAutoResponse` are free |
| KV | reads $0.50/M, writes/deletes/lists **$5/M**, $0.50/GB-month | writes per request are the usual cost bug |
| R2 | $0.015/GB-month, class A $4.50/M, class B $0.36/M | deletes are free |
| D1, DO SQLite | rows read $0.001/M, rows written $1/M | DO `rowsWritten` is per namespace |
| Workers AI | $0.011 per 1k neurons, 10k/day free | account level only |

Not covered: Workers Logs ($0.60/M above 20M), Images, Stream, Browser Rendering, Containers, Queues. Mention them as unknown when reporting.

## Digging into one project

- **Durable Objects** (per object, hibernation check, per-day trend): read `~/.config/opencode/skills/cloudflare-workers/durable-object-usage.md`.
- **DO connect loops**: group `durableObjectsInvocationsAdaptiveGroups` by `objectId` with `type:"http"`. A steady connect every few seconds on one object means a client reconnect loop.
- **KV**: `kvOperationsAdaptiveGroups` by `namespaceId` + `actionType`; namespace titles come from `cf kv namespaces list`.

## Reporting rules

- Always say the numbers are **list-price estimates from analytics, not the invoice**.
- Show the top projects with their main cost driver, the gross, the free tier and the net month estimate.
- Compare with the previous report when one exists and call out projects that grew more than 25%.
