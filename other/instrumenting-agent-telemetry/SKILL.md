---
name: instrumenting-agent-telemetry
version: "2.0.0"
description: >
  Instruments AI agents to produce observable telemetry — what to log at
  each agent step, which metrics signal health vs. degradation, how to wire
  PostHog (MCP connected) for agent-specific observability, and how to detect
  behavioral drift before it reaches users. Datadog is NOT connected — all
  Datadog steps including statsd custom metrics and monitor creation are
  static reference guides only, clearly labeled, and not executable via MCP.
  Activates when setting up monitoring for an AI agent, wiring an agent to
  PostHog, figuring out what to log in agent interactions, detecting when an
  agent is getting worse, building dashboards for agent health, or setting
  alert thresholds for agent failure rates. Also triggers on: agent monitoring,
  agent observability, agent drift, agent performance tracking, LLM cost
  monitoring, tool call logging, agent latency, agent dashboard, agent
  metrics, is my agent getting worse, PostHog agent events.
allowed-tools: Read Write Bash
---

# Agent Telemetry Instrumentation

Agents are black boxes by default. This skill makes them transparent.

**Live operational path: PostHog MCP ✅**
**Datadog: ❌ NOT connected — [STATIC REFERENCE] sections are manual setup guides only.**

The distinction from application monitoring: standard APM tells you about
infrastructure (CPU, memory, latency). Agent telemetry tells you about
*behavior* — whether the agent is making the right decisions, calling the
right tools, and producing quality outcomes over time.

---

## DEPENDENCY_DECLARATION

| Tool | Status | Operational Path | Notes |
|------|--------|-----------------|-------|
| PostHog | MCP ✅ CONNECTED | Live event queries, insight creation, alert config, session analysis | Primary agent observability path |
| Supabase | MCP ✅ CONNECTED | Structured agent event logging, durable backup store | Ask before write ops |
| n8n | MCP ✅ CONNECTED | Agent workflow execution status | |
| Datadog | ❌ NOT_CONNECTED | Static reference only — no MCP execution | `from datadog import statsd` requires Datadog agent running locally — not available here |

**Rule:** Any step in a [STATIC REFERENCE] section requires manual Datadog setup. Do not execute Datadog API calls, `statsd` emits, monitor creation, or dashboard operations in a Claude session — Datadog is not connected. Any claimed result would be fabricated.

---

## FAIL_IF

- **FAIL_IF** you attempt to create Datadog monitors, dashboards, log pipelines, or custom metrics via MCP — Datadog is not connected; results would be fabricated.
- **FAIL_IF** you run `from datadog import statsd` or `statsd.increment()` as a live operational step — this requires a Datadog agent running locally, which is not available.
- **FAIL_IF** you claim "four baseline Datadog monitors are created" without Datadog being connected and manually configured.
- **FAIL_IF** you log user message content, email addresses, names, or any PII in PostHog events — use anonymized session UUIDs only.
- **FAIL_IF** you embed PostHog server keys, Anthropic API keys, or any secret in a code block — all keys from environment variables only.
- **FAIL_IF** you set alert thresholds before collecting at least 1 week of baseline production data from the target agent.
- **FAIL_IF** you use `posthog-node` in client-side code or `posthog-js` in server-side code — the SDK choice is environment-specific.

**"Just do it" override:** if the user requests immediate setup, proceed with the PostHog-only live path, label Datadog steps as manual follow-ups, and continue without asking for clarification.

---

## Evals

**Should trigger:**
1. "Set up monitoring for my FlashFusion intake agent"
2. "Is my agent getting worse? I need to see behavioral trends"
3. "Wire agent telemetry to PostHog"
4. "Build a dashboard for agent health metrics"
5. "How do I detect agent drift?"

**Should NOT trigger:**
1. "Set up Vercel and Supabase infrastructure monitoring" → instrumenting-production-stack
2. "Why is my Anthropic bill so high" → governing-stack-costs
3. "Build an eval suite for my agent" → evaluating-ai-agents

---

## What to Log at Each Agent Step

### Minimum viable agent log event

Every agent interaction must emit at least one structured log entry. This is a ship gate — no agent goes to production without it.

```json
{
  "event": "agent_interaction",
  "agent_id": "flashfusion-intake-agent",
  "session_id": "uuid-anonymized",
  "timestamp": "ISO-8601",
  "input_tokens": 1240,
  "output_tokens": 387,
  "total_cost_usd": 0.0048,
  "tools_called": ["search_kb", "create_ticket"],
  "tool_errors": [],
  "turns": 3,
  "latency_ms": 2840,
  "outcome": "completed | failed | escalated | timed_out",
  "outcome_detail": "string — sanitized summary, no PII"
}
```

### Per-tool-call log entry

```json
{
  "event": "tool_call",
  "session_id": "uuid-anonymized",
  "tool_name": "create_ticket",
  "input_hash": "sha256 of sanitized input — not raw input",
  "success": true,
  "error": null,
  "duration_ms": 340
}
```

**Do not log full tool inputs/outputs by default.** They frequently contain PII or sensitive context. Log hashes or sanitized summaries. Full inputs only in an explicit debug mode with data handling controls in place.

### What NOT to log (ever)

- User message content
- Full tool inputs or outputs containing personal data
- API keys, tokens, or secrets — ever, anywhere
- Full system prompt (IP risk)
- Email addresses, names, or any PII — use session UUID as the only identifier

---

## Metrics That Matter

### Health metrics (alert when these degrade)

| Metric | Healthy range | Alert threshold |
|--------|--------------|----------------|
| Task completion rate | >92% | <85% |
| Tool call success rate | >97% | <90% |
| P95 latency | <8s | >15s |
| Error rate (unhandled) | <2% | >5% |
| Escalation rate | <10% | >20% |

These are starting-point thresholds. Calibrate against your agent's actual 1-week baseline before finalizing.

### Cost metrics (alert when these spike)

| Metric | Alert condition |
|--------|----------------|
| Cost per session | >2× 7-day rolling average |
| Total daily cost | >$X (set per-agent budget ceiling) |
| Input token growth | >50% week-over-week |
| Sessions with >10 turns | >15% of total sessions |

High turn counts signal either a stuck agent loop or a user who is struggling — both are quality problems, not just cost ones.

---

## PostHog Setup for Agent Telemetry (LIVE ✅)

PostHog is the live operational path for agent behavioral observability. Use it for funnels, session patterns, outcome trends, and cost analysis.

### Emit agent events — server-side (LIVE ✅)

```typescript
// server-side ONLY — posthog-node package
// posthog-js is for browser clients; never use it server-side for agent events
import { PostHog } from 'posthog-node'

// Loaded from environment variable — never hardcoded
const ph = new PostHog(process.env.POSTHOG_SERVER_KEY!)

// Emit after each agent session completes
ph.capture({
  distinctId: sessionId,  // anonymized UUID — not user email, not user name
  event: 'agent_session_completed',
  properties: {
    agent_id:            'flashfusion-intake-agent',
    outcome:             'completed',  // completed | failed | escalated | timed_out
    turns:               3,
    tools_used:          ['search_kb', 'create_ticket'],
    tool_error_count:    0,
    cost_usd:            0.0048,
    input_tokens:        1240,
    output_tokens:       387,
    session_duration_ms: 2840,
    // NEVER include: message_content, user_email, user_name, auth_token
  }
})

// Emit per tool call for tool-level granularity
ph.capture({
  distinctId: sessionId,
  event: 'agent_tool_call',
  properties: {
    agent_id:    'flashfusion-intake-agent',
    tool_name:   'create_ticket',
    success:     true,
    duration_ms: 340,
    error:       null
  }
})
```

### PostHog insights to build (via MCP or PostHog UI)

- **Outcome breakdown:** `agent_session_completed` breakdown by `outcome` — percentage complete vs. escalate vs. fail vs. timed_out
- **Cost trend:** `agent_session_completed` sum `cost_usd` by day
- **Latency distribution:** `agent_session_completed` percentile on `session_duration_ms`
- **Tool success rate:** `agent_tool_call` where `success = false` as percentage of total
- **High-turn session flag:** `agent_session_completed` where `turns > 10` as percentage of total
- **Cost by agent:** `agent_session_completed` sum `cost_usd` breakdown by `agent_id`

**Use PostHog MCP to query insights in session:**
> "Pull agent_session_completed events from the last 7 days, breakdown by outcome, trend by day"

### PostHog alerts to configure (LIVE ✅ — set up in PostHog UI)

Create these four alerts in PostHog (Insights → Alerts):

1. **Completion rate drop:** `agent_session_completed` where `outcome = completed` falls below 85% of hourly sessions → alert
2. **Cost spike:** `sum(cost_usd)` per hour exceeds 2× same-hour average from the prior 7 days → alert
3. **Error rate surge:** `agent_session_completed` where `outcome = failed` exceeds 5% over 15 minutes → alert
4. **Latency degradation:** `avg(session_duration_ms)` exceeds 15,000ms over a 10-minute window → alert

---

### [STATIC REFERENCE] Datadog Setup for Agent Telemetry

> ⚠️ Datadog is NOT connected via MCP. The steps below require manual Datadog configuration and a Datadog agent running in your infrastructure. Do not execute these in a Claude session — they cannot be verified and any claimed result would be fabricated.

#### Log pipeline (manual)

1. In your agent code, emit structured JSON logs to stdout
2. Datadog agent picks these up when JSON logging is enabled (`DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true` or equivalent)
3. In Datadog → Logs → Pipelines → create an agent-specific pipeline:
   - Filter: `service:flashfusion-agent`
   - Processor: JSON parser on log message
   - Facets: add `outcome`, `agent_id`, `tool_name` as indexed facets

#### Custom metrics (manual — requires Datadog agent running locally)

```python
# Requires: pip install datadog
# Requires: Datadog agent running at DD_AGENT_HOST
# DD_AGENT_HOST loaded from environment variable — never hardcoded
from datadog import statsd

# Emit after each agent interaction
statsd.increment('agent.interactions.total', tags=[f'agent:{agent_id}', f'outcome:{outcome}'])
statsd.gauge('agent.latency_ms', latency_ms, tags=[f'agent:{agent_id}'])
statsd.gauge('agent.cost_usd', cost_usd, tags=[f'agent:{agent_id}'])
statsd.increment('agent.tool_calls.total', tags=[f'tool:{tool_name}', f'success:{success}'])
```

#### Recommended Datadog monitors (create manually in Datadog UI)

1. **Completion rate drop:** 5-minute rolling `outcome:completed` rate < 85% → alert
2. **Cost spike:** hourly `agent.cost_usd` sum > 2× same-hour yesterday → alert
3. **Error rate surge:** 15-minute `outcome:failed` rate > 5% → alert
4. **Latency degradation:** 10-minute P95 `agent.latency_ms` > 15,000ms → alert

**When Datadog connects via MCP:** promote these steps to the live operational section, remove this [STATIC REFERENCE] block, and update DEPENDENCY_DECLARATION.

---

## Detecting Behavioral Drift

### Weekly drift review — 15 minutes (LIVE ✅ via PostHog MCP)

Pull these two reports weekly:

1. **Tool call distribution:** `agent_tool_call` breakdown by `tool_name` — compare this week vs. last week
2. **Outcome distribution:** `agent_session_completed` breakdown by `outcome` — this week vs. 30-day baseline

**PostHog MCP queries to run:**
> "Show me agent_tool_call events from the last 14 days, breakdown by tool_name, compare week-over-week"
> "Show me agent_session_completed events from the last 30 days, breakdown by outcome, trend by week"

If either report shows >10% relative change without a corresponding code or prompt change, investigate before assuming it is noise.

### Drift causes (in order of likelihood)

1. **Prompt change:** a recent edit to the system prompt is producing different tool selection behavior
2. **Tool schema change:** a tool's description or parameters changed, altering how the model interprets when to call it
3. **Model update:** the underlying model was updated and behaves differently on edge cases or ambiguous inputs
4. **Input distribution shift:** the types of requests coming in have changed — new user cohort, seasonal pattern, or marketing campaign effect
5. **Genuine degradation:** rare without one of the causes above — check all four before concluding this

### Response to confirmed drift

1. Identify the change that correlates with drift onset — check git log for prompt, tool schema, or model version changes
2. Run your regression eval suite against the current agent state (use `evaluating-ai-agents` skill)
3. If evals fail: revert the identified change and investigate root cause
4. If evals pass: drift may reflect improved behavior — verify by sampling a set of new interactions manually

---

## Supabase Backup Event Log (Optional — LIVE ✅)

If PostHog is unavailable or you need a durable structured store for agent events, write to Supabase:

```sql
CREATE TABLE agent_events (
  id             uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  agent_id       text NOT NULL,
  session_id     text NOT NULL,
  event_type     text NOT NULL,  -- 'session_completed' | 'tool_call'
  outcome        text,
  turns          int,
  cost_usd       numeric(10,6),
  latency_ms     int,
  tools_used     text[],
  tool_name      text,
  tool_success   boolean,
  created_at     timestamptz DEFAULT now()
);

-- Restrict reads to service role; no user-facing query of raw agent events
ALTER TABLE agent_events ENABLE ROW LEVEL SECURITY;
CREATE POLICY "service_role_only" ON agent_events FOR ALL USING (false);
```

Query this table via Supabase MCP for ad-hoc analysis when PostHog is unavailable.

---

## Self-Verification Checklist

- [ ] `agent_session_completed` events flowing to PostHog — **FAIL** if no events appear in PostHog Live Events after a test agent run
- [ ] `agent_tool_call` events emitted per tool call — **FAIL** if tool call granularity is absent
- [ ] PII excluded from all events (no email, name, message content) — **FAIL** if any PII field appears in any event
- [ ] All keys loaded from environment variables only — **FAIL** if any key appears in source code
- [ ] Four PostHog alerts configured in PostHog UI — **FAIL** if no alert thresholds exist
- [ ] PostHog outcome breakdown insight created and saved to dashboard — **FAIL** if no agent health dashboard exists
- [ ] Baseline metrics recorded for completion rate, cost, and latency — **FAIL** if thresholds were set before collecting ≥1 week of baseline data
- [ ] Weekly drift review scheduled (calendar or Todoist recurring task) — **FAIL** if no recurring reminder exists
- [ ] [STATIC — when ready] Datadog agent and custom metrics setup documented in Notion for future reference

---

## CLAIMS / COUNTEREXAMPLES / CONTRADICTIONS

**CLAIMS**
- [GENERATED] Logging outcomes rather than content is sufficient for operational monitoring and avoids the PII handling burden of logging message content.
- [GENERATED] Behavioral drift without a corresponding code or model change almost always traces to input distribution shift — verify this before concluding the agent has degraded.

**COUNTEREXAMPLE**
- For debugging specific complex failures, outcome-only logging is insufficient. A debug mode with full interaction logging — behind explicit consent and data handling controls, not enabled by default in production — is necessary for root-cause analysis on edge-case agent failures.

**CONTRADICTIONS**
- Comprehensive per-interaction logging conflicts with user privacy. Resolution: structured logging with explicit field-level decisions, a deny-list of PII fields, and debug mode gated behind an explicit feature flag — never enabled by default.
- ! CONTRADICTION: the previous version of this skill (v1.0.0) listed `from datadog import statsd` and four Datadog monitor creation steps as live operational steps. Datadog is NOT connected — those steps cannot execute via MCP and would require the Datadog agent running locally. The live path is PostHog. All Datadog content is now clearly labeled [STATIC REFERENCE].

---

## GAPS / BLINDSPOTS / UNKNOWN-UNKNOWNS

- **Datadog not connected.** When Datadog connects via MCP, [STATIC REFERENCE] sections should be promoted to live operational steps and DEPENDENCY_DECLARATION updated. Create a Linear issue to track this.
- **`POSTHOG_SERVER_KEY` rotation.** Must be rotated per `managing-credential-lifecycle` schedule. No auto-rotation mechanism is in place.
- **Sampling strategy undefined.** At high agent volume, logging every interaction at full detail becomes expensive. Define a sampling rate (10–25% for detailed per-interaction logging) before volume scales significantly.
- **Eval harness not wired to telemetry.** Drift detection currently requires manual PostHog queries. An automated eval run triggered when a drift threshold breach is detected would close this gap.
- **Supabase backup table is optional.** If PostHog goes down, agent events are lost unless the Supabase backup pattern is implemented. Assess whether the backup is worth the maintenance before adding it.
- **SELF-REVIEW:** Verified that `from datadog import statsd` appears only inside a [STATIC REFERENCE] block, clearly marked as requiring manual setup and not executable via MCP. All four Datadog monitor creation steps likewise moved to [STATIC REFERENCE]. PostHog is the sole live operational path. All keys use environment variables. DEPENDENCY_DECLARATION and FAIL_IF blocks added. Version bumped to 2.0.0 (major — Datadog removed from live path, gate logic changed).
