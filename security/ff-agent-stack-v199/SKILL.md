---
name: ff-agent-stack-v199
description: >
  FlashFusion Agent Stack v1.9.9 phased build pipeline. Activates for:
  agent stack, v1.9.9, phase 0, phase 1, phase 2, phase 3, phase 4,
  gaps audit, baton pass, langgraph, orchestration build, agent pipeline,
  flashfusion, flash-n-frame, supabase schema, rls policies, agent catalog,
  graph spec, memory spec, tool contracts, billing guardrails, observability
  runbook, rollback recovery, api contracts, typescript interfaces, smoke tests,
  tenant isolation, idempotency, checkpoint recovery, wsjf backlog, sprint backlog.
  Use this skill to run any phase of the v1.9.9 build pipeline, check WSJF
  priority, or get scaffolding stubs.
version: 1.0.0
---

# FlashFusion Agent Stack v1.9.9 — Build Pipeline Skill

## Purpose

Provides the complete 5-phase build pipeline for FlashFusion Agent Stack v1.9.9.
Each phase is a bounded, self-contained prompt that feeds the next via a BATON block.
Phase 0 is mandatory first. Phases 1–3 are parallel-safe after Phase 0 clears.
Phase 4 is the release gate.

---

## Quick Navigation

| Phase | Focus | Deliverables | Ref |
|-------|-------|-------------|-----|
| 0 | Gaps + Assumptions Audit | GAPS_AUDIT.md | [phases/PHASE_0.md](phases/PHASE_0_GAPS_AUDIT.md) |
| 1 | Foundation | ARCHITECTURE.md, SECURITY_MODEL.md, SQL migration | [phases/PHASE_1.md](phases/PHASE_1_FOUNDATION.md) |
| 2 | Orchestration | AGENT_CATALOG.md, GRAPH_SPEC.md, MEMORY_SPEC.md, TOOL_CONTRACTS.md | [phases/PHASE_2.md](phases/PHASE_2_ORCHESTRATION.md) |
| 3 | Operations | BILLING_GUARDRAILS.md, OBSERVABILITY_RUNBOOK.md, ROLLBACK_RECOVERY.md | [phases/PHASE_3.md](phases/PHASE_3_OPERATIONS.md) |
| 4 | Verification | API_CONTRACTS.md, TypeScript types, smoke tests, acceptance criteria | [phases/PHASE_4.md](phases/PHASE_4_VERIFICATION.md) |

WSJF sprint backlog: [WSJF_BACKLOG.md](WSJF_BACKLOG.md)

---

## How to Run This Pipeline

### In Claude.ai Projects (recommended for doc generation)

1. Upload this zip to your Project via **Settings → Skills → Upload Skill**
2. Start a new conversation in that Project
3. Type: `run phase 0` — the skill activates automatically
4. Paste the phase prompt from `phases/PHASE_0_GAPS_AUDIT.md` into the chat
5. Read the BATON block at the end before starting Phase 1
6. Repeat for each phase in order

### In Claude Code CLI / Antigravity (recommended for implementation)

```bash
# Copy scaffolding stubs into your repo first
cp scaffolding/supabase/001_v199_foundation.sql ./supabase/migrations/
cp scaffolding/typescript/v199.ts ./src/types/
# Then paste phase prompts directly into Claude Code chat
```

### Baton Pass Protocol

Every phase ends with a BATON block like this:

```
PHASE_N_STATUS: [COMPLETE / INCOMPLETE]
LOCKED_OUTPUTS: [what the next phase must reference]
OPEN_ITEMS: [gaps not yet resolved]
CONFIDENCE: [0-100%] — if below 80%, resolve before proceeding
```

**Do not start the next phase if CONFIDENCE < 80% or STATUS = INCOMPLETE.**
Paste the full BATON block at the top of the next phase prompt.

---

## Marking Conventions (used in all phases)

| Marker | Meaning |
|--------|---------|
| `[UNVERIFIED]` | Claim made, source not confirmed |
| `[SHALLOW]` | Correct direction, needs expansion |
| `[ASSUMED]` | Constraint assumed — call it out |
| `⚠` | Adversarial finding — must resolve |
| `!` | Internal contradiction flagged |

**Rule:** Shallow + honest beats deep + hallucinated. Use these markers.

---

## Stack Reference (locked for v1.9.9)

```
Frontend:       Next.js (App Router)
Backend:        Node.js / TypeScript
Orchestration:  LangGraph (primary spine)
                CrewAI (content lanes)
                AutoGen (premium reasoning, optional)
Auth + DB:      Supabase (Auth, Postgres, RLS, Storage)
Hot State:      Redis (run locks, queues, session state)
Vector Memory:  pgvector via Supabase
Tools:          MCP-compatible adapters
Model Routing:  OpenAI / Anthropic / Gemini (abstracted)
Background:     Worker pool
Operator UI:    Agent Studio (read-only trace viewer scope)
Automation:     Make / n8n (external ops only)
```

---

## Agent Cast (mandatory first wave)

| Agent | Role |
|-------|------|
| Router | Classify, gate, route requests |
| Planner | Decompose goal into bounded execution plan |
| Tool Executor | MCP calls, permission-scoped, idempotent |
| Memory | Decide what to retain / expire / redact |
| Validator | Schema, policy, plan, format checks |
| Publisher | External platform publish + post-actions |
| Recovery | Failure classification, rollback, resume |

Second-wave agents (feature-flagged only, not in v1.9.9 golden path):
Research, UI Critic, Brand Consistency, Commerce Optimizer

---

## Non-Negotiable Build Rules

**Security**
- All tenant data RLS-protected — no exceptions
- Service-role key never in frontend or client bundle
- Tool inputs/outputs redacted before log/trace storage
- Secrets via env vars only — never hardcoded

**Reliability**
- Every side-effecting action requires idempotency key
- Every run produces a replayable trace
- All long-running jobs support checkpoint + resume
- Compensating action defined for every irreversible side effect

**Cost Control**
- Per-run token budget enforced in graph
- Max hops, retries, wall-clock duration set per route
- Premium model path blocked unless plan gate passes

**Versioning**
- Graph version + prompt version + schema version + model route stored per run
- Prompts treated as code: versioned, rollback-safe

---

## Scaffolding Stubs

Pre-built stubs ready to drop into your repo:

- `scaffolding/monorepo/FOLDER_TREE.md` — full annotated monorepo structure
- `scaffolding/supabase/001_v199_foundation.sql` — migration stub with RLS
- `scaffolding/typescript/v199.ts` — typed interfaces stub

These are stubs, not finished code. Phase 1 and Phase 4 generate the real implementations.

---

## References

- [references/STACK_DECISIONS.md](references/STACK_DECISIONS.md) — why LangGraph over CrewAI / AutoGen / Make
- [references/AGENT_ROLES.md](references/AGENT_ROLES.md) — agent boundaries and interaction rules
- [references/BATON_TEMPLATE.md](references/BATON_TEMPLATE.md) — copy-paste baton block format
- [references/MARKING_CONVENTIONS.md](references/MARKING_CONVENTIONS.md) — full marker guide

---

## Version Notes

v1.9.9 is a **stability + hardening release**, not a feature release.

Ships when:
- All 8 smoke tests pass
- All tenant data is RLS-protected
- All agent runs produce replayable traces
- All premium paths are plan-gated
- All long jobs are resumable or safely rollback-able
- No service-role key in any client bundle
- No sensitive field in any log or trace

**Do not add experimental agents, new product features, or cosmetic improvements
unless they directly serve stability, isolation, idempotency, or observability.**
