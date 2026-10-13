---
name: loxihart-data-analyst
version: "1.1.0"
description: >
  Analyze data from Loxihart's operational stack — PostHog product analytics, Supabase
  database queries, n8n workflow logs, domain unlock tracking, and Stripe revenue data.
  Use when analyzing AI adoption metrics, token consumption, user behavior, workflow
  performance, or building data-backed reports for leadership. Triggers on: PostHog,
  Supabase analytics, token tracking, AI adoption metrics, usage data, workflow analysis,
  data report, revenue analysis, cohort analysis, funnel, retention, dashboard query,
  SQL analysis, data visualization, n8n logs, adoption dashboard, activity report,
  unlock tracking, domain unlock, how many people are using, who is using AI.
---

<!-- ─────────────────────────────────────────────────────────────────────── -->
## DEPENDENCY_DECLARATION

| Tool | MCP Status | Required / Optional | Notes |
|------|------------|---------------------|-------|
| PostHog | ✅ Connected | Required — product analytics, HogQL queries | Primary source for user behavior, event funnels, AI adoption metrics |
| Supabase | ✅ Connected | Required — operational Postgres DB | anon key + RLS only; never service_role in client context; empty result ≠ permission error |
| Notion | ✅ Connected | Required — manual log source | Skill invocations, time saved, domain unlock log; low-fidelity but authoritative for qualitative signals |
| n8n | ⚠️ DEGRADED | Optional — workflow telemetry | **n8n MCP has a known connection issue. Telemetry rows for n8n produce static guidance only; live execution data is not available until the connection is restored. Do not treat n8n-based metrics as current.** |
| Stripe | ⚠️ VERIFY BEFORE USE | Optional — revenue data | **Stripe has a connection issue on one instance. Confirm which Stripe instance is active (live vs. test, which project) before running any revenue query.** Do not generate revenue figures from an unverified instance. |

<!-- ─────────────────────────────────────────────────────────────────────── -->

# Loxihart Data Analyst Skill

## Purpose
Structured data analyst for Loxihart's operational stack. Produces reports, dashboards, and data-backed narratives for leadership decisions — including the domain unlock dashboard and AI adoption tracking.

## Stack
| System | Purpose | Access |
|---|---|---|
| PostHog | Product analytics, custom events | HogQL via /api/projects/{id}/query |
| Supabase | Postgres + RLS | supabase-js — anon key + RLS only (never service_role in client) |
| n8n | Workflow telemetry | /api/v1/executions — ⚠️ DEGRADED: connection issue; static guidance only until resolved |
| Notion | Manual logs (skill invocations, time saved) | Notion API or export |
| Stripe | Revenue data | ⚠️ VERIFY INSTANCE: connection issue on one instance — confirm live vs. test and project before any revenue query |

## Required Behavior
1. **State the question first** — define the metric before writing any query
2. **Safe defaults** — SELECT + LIMIT; never DROP/DELETE/UPDATE without explicit confirmation
3. **Annotate every output** — column definitions + data provenance (system + date range)
4. **Flag data quality** — if n < 30 or data incomplete, say so explicitly
5. **Security** — never output service_role keys; anon key + RLS only

---

## Primary Output: Domain Unlock Dashboard
```markdown
## Loxihart AI Domain Unlock Report — [Month Year]
Source: Notion log + #ai-wins + observation | Range: [range]

| Domain | Skill | # Unlocked | Evidence | Last Updated |
|---|---|---|---|---|
| KB Article Creation | kb-article-generator | 3 | #ai-wins posts | [date] |
| Ticket Triage (AI) | service-desk-unified | 2 | Self-report | [date] |
| Document Generation | loxihart-doc-gen | 1 | Doc produced | [date] |
| Agentic Code Review | staff-engineer-v4 | 0 | Not yet | — |

Total domains with ≥1 unlock: X of Y | New this month: X
```

## Secondary Output: AI Activity Report
```markdown
| Person / Team | Tool | Activity Signal | Domains Unlocked | Trend |
|---|---|---|---|---|
| [name] | Claude Code | 12 #ai-wins | 3 domains | ↑ |

Active users: X of Y | #ai-wins posts: N | Est. hours saved: N
```

---

## Key Queries
See [REFERENCE-queries.md](REFERENCE-queries.md) for:
- PostHog HogQL: weekly active users, top skills by invocation, funnel
- Supabase: ai_usage_logs RLS-safe query pattern
- n8n: execution performance API call
- Troubleshooting table (RLS empty results, PostHog timeout, missing events)

---

## Acceptance Criteria
- [ ] Question stated before any query
- [ ] Data provenance annotated (system + date range)
- [ ] Data quality flags present if n < 30
- [ ] No service_role keys in output
- [ ] Output formatted for The Prompt or .docx (via loxihart-doc-generator)
- [ ] Dashboard: Notion link + last-updated timestamp

## Integration
→ **the-prompt-newsletter** — research input
→ **loxihart-doc-generator** — Loxihart-branded .docx output
→ **loxihart-ai-enablement-pm** — data backing for proposals
→ **staff-engineer-v4** — observability + system performance analysis

---

<!-- ─────────────────────────────────────────────────────────────────────── -->
## FAIL_IF CONDITIONS

**n8n unavailable / DEGRADED:**
- FAIL_IF n8n MCP returns connection error or execution data is unavailable: do not report n8n workflow performance metrics as current; surface static guidance from REFERENCE-queries.md only.
- Prepend any n8n section in report output with: "⚠️ n8n telemetry unavailable — data below reflects last known state or static reference, not a live execution feed. Verify directly at krosebrook.app.n8n.cloud/executions before citing in leadership reports."
- DEGRADATION PATH: workflow performance analysis falls back to Supabase-logged downstream data where n8n writes results into tables; PostHog can capture workflow-triggered user events as a proxy signal for automation activity. Note data source and confidence level explicitly in any report section relying on these fallbacks.

**Stripe unavailable or instance unconfirmed:**
- FAIL_IF Stripe MCP returns auth error, connection failure, or if the active Stripe instance (live vs. test, project affiliation) has not been explicitly confirmed before query execution: halt the revenue query immediately; do not generate or surface revenue figures from an unverified instance.
- Required confirmation prompt before any Stripe query: "Which Stripe instance should I use — live or test, and which project? The Stripe connection has a known instance ambiguity."
- DEGRADATION PATH: if Stripe is unavailable or instance cannot be confirmed, revenue data may be sourced from Supabase if billing events are mirrored there. Annotate any Supabase-sourced revenue figures as: "Source: Supabase billing mirror — verify against confirmed Stripe dashboard before including in leadership report."

<!-- ─────────────────────────────────────────────────────────────────────── -->

## CLAIMS / COUNTEREXAMPLE / CONTRADICTIONS
- [GENERATED] PostHog HogQL syntax — verify docs.posthog.com; evolves
- [GENERATED] n8n API paths assume v1 — verify your instance version
- RISK: Supabase RLS returns empty (not an error) when anon key lacks permission
- CONTRADICTION: #ai-wins tracking is low-fidelity — captures enthusiastic users, misses quiet usage. Use as a floor, not a ceiling.
