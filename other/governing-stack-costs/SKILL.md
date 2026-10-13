---
name: governing-stack-costs
version: "1.0.0"
description: >
  Tracks, alerts on, and optimizes cloud infrastructure costs across the
  production stack — Anthropic API token spend, Supabase compute and
  egress, Vercel function invocations, and n8n executions. Establishes
  per-service budget thresholds, monthly review workflow, and quick-win
  optimization patterns. Activates when reviewing cloud costs, setting
  budget alerts, an unexpected bill arrived, trying to reduce API spend,
  figuring out what's costing money, optimizing token usage, or setting
  up cost governance for a production system. Also triggers on: cost
  spike, cloud bill, Anthropic costs, API spend, reduce token usage,
  cost optimization, budget alert, Supabase bill, Vercel usage, what
  am I spending, cloud costs, LLM costs.
---

# Cloud Cost Governance

Covers the full production stack cost picture, not just LLM costs.
For LLM-specific optimization patterns (model routing, caching), see
`ecc:cost-aware-llm-pipeline`.

---

## Cost Centers by Service

### Anthropic API
- **Billing model:** tokens (input + output, priced per million)
- **Typical range:** $0–500/month depending on agent usage
- **Cost drivers:** long system prompts, high turn-count sessions, Sonnet
  on tasks that Haiku could handle
- **Dashboard:** console.anthropic.com → Usage

### Supabase
- **Billing model:** compute tier + egress + storage
- **Free tier limits:** 500MB DB, 1GB storage, 2GB egress/month
- **Cost drivers:** egress (data leaving Supabase), active database
  connections, storage growth
- **Dashboard:** supabase.com/dashboard → project → Settings → Billing

### Vercel
- **Billing model:** function invocations + bandwidth + build minutes
- **Pro plan includes:** 1M function invocations, 1TB bandwidth
- **Cost drivers:** high-traffic API routes, large bundle sizes, frequent
  deployments on feature branches
- **Dashboard:** vercel.com → team → Settings → Billing

### n8n
- **Billing model:** execution count (cloud) or self-hosted compute
- **Cost drivers:** polling workflows running too frequently, high-volume
  webhook processing, complex workflows with many nodes
- **Dashboard:** app.n8n.cloud → Settings → Usage

---

## Budget Thresholds (Starting Points)

Set these as alerts in each service's dashboard. Adjust once you know
your actual baseline.

| Service | Monthly budget | Alert at 75% | Hard alert at 100% |
|---|---|---|---|
| Anthropic API | $[set yours] | $[×0.75] | $[×1.0] |
| Supabase | $[set yours] | — | At plan limit |
| Vercel | $[set yours] | — | At plan limit |
| n8n Cloud | $[plan cost] | 75% of executions | 90% of executions |

**Set Anthropic usage alerts:**
console.anthropic.com → Settings → Billing → Usage alerts
Configure: monthly budget limit + email notification at 75% and 100%.

---

## Monthly Cost Review (20 minutes)

Run this on the 1st of each month:

1. **Pull actual spend:** Anthropic console, Supabase dashboard,
   Vercel billing, n8n usage
2. **Compare to previous month:** is any service trending up more than
   usage growth would explain?
3. **Find the top 3 cost drivers** in Anthropic (by context/feature tag
   if you have the wrapper from `instrumenting-production-stack`)
4. **Identify waste:** n8n polling workflows running more often than needed,
   unused Vercel deployments, large files in Supabase storage
5. **Record in Notion:** date, each service's cost, total, notable changes

---

## Quick-Win Optimizations

### Anthropic API

- **Use Haiku for simple tasks:** classification, summarization, routing
  decisions, extraction. Cost: 15-25x less than Sonnet.
  Rule of thumb: if the task fits in under 500 tokens and doesn't require
  complex reasoning, Haiku is sufficient.

- **Cache repeated system prompts:** use prompt caching (available on
  Claude 3.5+ models) for system prompts and static context over 1024
  tokens. Cached tokens cost ~10% of normal input price.

- **Reduce turn count:** long multi-turn conversations cost more per
  session. If the agent is averaging >8 turns per task, the system
  prompt or tool definitions may need clarification.

- **Log and review high-token sessions:** any session over 50K tokens
  is worth reviewing — it may indicate a context management issue or
  an agent stuck in a loop.

### Supabase

- **Reduce egress:** add indexes to avoid full table scans, which
  return more rows than needed. Use `select()` with explicit column
  lists instead of `select *`.

- **Connection pooling:** use Supabase's built-in connection pooler
  (Transaction mode for serverless, Session mode for persistent)
  to prevent connection limit overruns that force upgrade.

- **Storage cleanup:** delete unused storage objects and old backups.
  Storage costs accumulate silently.

### Vercel

- **Edge vs. Serverless routing:** move lightweight middleware and
  simple API routes to Edge Functions (faster, cheaper) and reserve
  Serverless Functions for DB-connected routes.

- **Bundle size optimization:** large bundles increase cold start time
  and bandwidth. Run `@next/bundle-analyzer` to identify large dependencies.

### n8n

- **Increase polling intervals:** if polling every 1 minute is
  unnecessary, change to every 5 or 15 minutes. Polling executions
  count against your quota even when no data is found.

- **Deactivate unused workflows:** inactive workflows still count as
  "active" in some n8n plans. Deactivate anything not running in
  the last 30 days.

---

## Self-Verification

- [ ] Budget thresholds set in Anthropic console with email alerts
- [ ] Monthly cost review on the calendar
- [ ] High-cost Anthropic context tags are labeled (see instrumenting-production-stack)
- [ ] n8n polling intervals reviewed and minimized
- [ ] Haiku vs. Sonnet routing policy defined for agent tasks

---

## CLAIMS
- Tagging Anthropic API calls by feature context (from
  `instrumenting-production-stack`) makes it possible to identify the
  top cost drivers within days of a cost spike rather than weeks
- Polling interval reduction in n8n is the single highest-ratio
  cost/effort optimization for workflow-heavy stacks

## COUNTEREXAMPLE
- Model routing to Haiku introduces the risk of quality regression on
  tasks that appear simple but require nuanced reasoning; validate with
  evals before routing production traffic

## CONTRADICTIONS
- Aggressive cost optimization conflicts with observability investment;
  both detailed telemetry and cost reduction are valid goals that
  require explicit tradeoffs rather than maximizing both simultaneously
