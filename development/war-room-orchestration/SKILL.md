---
name: war-room-orchestration
last_updated: 2026-05-17
description: "How CEO and C-suite dispatch work through the Beamix war-room trust-spec system: Linear label routing, Cloudflare bridge, HMAC-signed specs, fan-out/fan-in via Inngest, and audit_log enforcement. Use when authoring or debugging any CEO/C-suite dispatch flow."
tags: [orchestration, beamix-specific, agents, war-room]
source: beamix-authored 2026-05-16
risk: low
---

# War Room Orchestration

## Quick reference

> Routines fire on cron → orchestrate via Linear comments → fan-out via Inngest → fan-in via mem0. Never wait inline.

## When to use

- Authoring or refining a CEO, CTO, CPO, CMO, CBO, or QA-Lead agent file
- Debugging why a Routine did not fire or a sub-ticket was not picked up
- Writing an Inngest fan-in-watcher or timeout-watcher function
- Building the Cloudflare bridge Worker
- Understanding how trust_mode specs flow from Linear comment to Routine execution

## When NOT to use

- For product feature work unrelated to the war-room control plane
- When only a single-agent worktree task is needed (no fan-out)

## Core concepts

### Three agent classes

| Class | Examples | Spawn capability |
|-------|----------|-----------------|
| Main-thread Routine | CEO, CTO, CPO, CMO, CBO, QA-Lead, 11 standing Routines | Spawns subagent workers via Task |
| Subagent worker | backend-engineer, frontend-engineer, code-reviewer | Spawns nothing |
| Board persona | Visionary, Strategist, Architect, Risk-Modeler, Customer-Voice, Aria, Broad-Adversary | Spawns nothing |

Workers NEVER spawn subagents. If a worker thinks it needs to delegate, it returns `PARTIAL` with `needs_followup`. The parent C-suite decides.

### Tier system

Tiers are assigned at the Cloudflare bridge by a 50-line Haiku classifier OR pre-set by Adam via Linear label:

| Label | Tier | CEO path |
|-------|------|----------|
| `tier:quick` | Quick | CEO spawns worker directly via Task in same session |
| `tier:lite` | Lite | CEO fires single C-suite via Linear sub-ticket + bridge |
| `tier:full` | Full | CEO fans out to N C-suites; Inngest manages fan-in |
| `tier:irreversible` | Irreversible | Full path + mandatory multi-judge + Adam sign-off |

Deterministic override: a YAML file `.claude/qa-tier-floor.yml` maps file paths to minimum tiers. The bridge reads it — no LLM involved.

## The dispatch flow (Full-tier example)

```
Adam (Linear ticket BMX-100, labels: tier:full, agent:cto, agent:cmo)
  ↓
Cloudflare bridge:
  1. HMAC-verify webhook
  2. Verify issued_by.linear_user_id ∈ ALLOWED_ISSUERS
  3. Parse spec only from sentinel-bracketed comment (never ticket body)
  4. Validate nonce uniqueness (KV, 24h TTL)
  5. Acquire Durable Object lock (routine_id, ticket_id)
  6. Write audit_log row: status=fired
  7. Bridge HMAC-signs spec, POSTs to /v1/claude_code/routines/{cto_id}/fire
     and to /v1/claude_code/routines/{cmo_id}/fire
  ↓
CTO Routine starts (fresh main thread)
  - Validates HMAC of inbound spec (rejects if invalid)
  - Writes audit_log: status=accepted
  - Writes session_id to BMX-101 first comment
  - Spawns workers via Task
  - On complete: writes audit_log: status=complete, sets BMX-101 Done
  ↓ (parallel)
CMO Routine starts (same flow, BMX-102)
  ↓
Inngest fan-in-watcher (listens for linear/issue.updated with fan_in_key):
  - Validates session_id matches KV-stored expected session
  - When all sub-tickets Done with valid session_ids → fires CEO synth
  ↓
CEO synth: writes consolidated comment to BMX-100, sets Done
```

## Trust spec format

Specs are injected into Linear comments as sentinel-bracketed JSON. Never in ticket body.

```
---BEAMIX-SPEC-V1-START---
{
  "spec_version": "1.0",
  "trust_mode": true,
  "nonce": "3f2a-uuid-v4",
  "issued_at": "2026-05-16T10:00:00Z",
  "expires_at": "2026-05-16T14:00:00Z",
  "issued_by": {
    "kind": "adam",
    "linear_user_id": "adam-linear-user-id",
    "agent_session_id": "ceo-1-1778941761",
    "session_file": "docs/08-agents_work/sessions/2026-05-16-ceo-bmx100.md"
  },
  "linear_ticket": "BMX-101",
  "parent_ticket": "BMX-100",
  "fan_in_key": "uuid-v4-fan-in-key",
  "scope": {
    "intent": "ship",
    "domain": "backend",
    "constraints": ["no breaking changes to public API"],
    "definition_of_done": "PR merged AND staging deployed",
    "out_of_scope": ["billing changes", "auth flow"]
  },
  "budget": {
    "max_cost_usd": 5.0,
    "max_runtime_minutes": 30,
    "max_tool_calls": 200
  },
  "_signature": "HMAC-SHA256-bridge-signed"
}
---BEAMIX-SPEC-V1-END---
```

## Fan-in-watcher (Inngest)

```typescript
// inngest/functions/fan-in-watcher.ts
export const fanInWatcher = inngest.createFunction(
  { id: 'fan-in-watcher' },
  { event: 'linear/issue.updated' },
  async ({ event, step }) => {
    const { fan_in_key, session_id, ticket_id } = event.data;
    if (!fan_in_key) return;

    const kvSession = await step.run('validate-session', async () => {
      return kv.get(`fan-in:${fan_in_key}:expected-session:${ticket_id}`);
    });

    if (kvSession !== session_id) {
      await supabase.from('audit_log').insert({
        status: 'anomaly',
        ticket_id,
        reason: 'session_id_mismatch',
      });
      // escalate to Adam via Linear comment
      return;
    }

    // When all sub-tickets done, fire CEO synth
    await step.run('fire-synth', async () => {
      await fetch(`${ANTHROPIC_API}/routines/${CEO_SYNTH_ROUTINE_ID}/fire`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${CEO_SYNTH_TOKEN}` },
        body: JSON.stringify({ trust_mode: true, ...synthSpec }),
      });
    });
  }
);
```

## Audit log schema

Three writers — bridge, agent, Inngest watcher — each write their own row. No single point of erasure.

```sql
-- audit_log table (key columns)
id              uuid primary key
routine_id      text        -- which Routine fired
ticket_id       text        -- Linear ticket
session_id      text        -- agent session identifier
status          text        -- fired | accepted | complete | blocked | timeout | over_budget | anomaly | rule_violation
cost_usd        numeric
created_at      timestamptz
```

## See also

- `linear-mvp-recipe` — [[linear-mvp-recipe]]
- `board-meeting-protocol` — [[board-meeting-protocol]]
- `anthropic-routines` — [[anthropic-routines]]
- `qa-gate-protocol` — [[qa-gate-protocol]]

## Anti-patterns

- Parsing trust specs from ticket bodies — exploit surface for prompt injection
- Skipping HMAC verification on the receiving agent side
- Inline await on Routine completion inside an Inngest step — causes Vercel 60s timeout
- Workers writing to Linear (only C-suite and CEO write)
- Multiple Linear comments per agent per ticket (one synthesis comment only)
- CEO spawning workers directly for Lite+ tasks (always go through C-suite)
