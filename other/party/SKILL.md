---
name: mk:party
description: Multi-agent collaboration session. Brings 2-4 agent perspectives into one discussion for architecture decisions and trade-off analysis. Use when asked "should we X or Y?", "let's discuss", or "design review".
argument-hint: '"topic to discuss" [--agents planner,architect,developer]'
source: local
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
keywords:
  - party
  - multi-agent-deliberation
  - architecture-decision
  - trade-off-discussion
  - design-review
when_to_use: Use when deliberating architecture trade-offs — brings 2-4 agent perspectives into one discussion. NOT for solo brainstorming (see mk:brainstorming), NOT for re-examining a finished review or plan (see mk:elicit), NOT for product validation / 'is this worth building' (see mk:office-hours), NOT for sprint retrospectives (see mk:retro).
user-invocable: true
owner: research
criticality: medium
status: active
runtime: claude-code
---

# Party Mode — Multi-Agent Collaboration

Bring multiple agent perspectives into one room. Agents debate, challenge, and build on each other's ideas to catch design flaws before code exists.

## Required Agents

This skill orchestrates discussion among existing agent definitions. The following must exist under `.claude/agents/` (per `agent-routing.md`):

`architect`, `developer`, `security`, `tester`, `reviewer`, `ui-ux-designer`, `analyst`, `planner`, `researcher`

If a referenced agent is missing, fall back to the `Default` row in "1. Agent Selection". Never silently skip a topic-mapped agent without falling back — the discussion loses its challenge dimension.

## When to Use

- Architecture trade-offs ("REST vs GraphQL?", "monolith vs microservices?")
- Security vs UX trade-offs ("session timeout: 5min or 24hr?")
- Large refactors that touch many files (risk assessment)
- Brainstorming with domain expertise

> For dedicated retrospectives, use `mk:retro`. `mk:party` is for architectural trade-off deliberation.

## Protocol

> **Execution model:** Agents are simulated personas in the single orchestrator session — NOT real subagent spawns via the `Agent` tool. The per-round token caps (150 / 175 / 100) are enforced by the orchestrator generating each response in-context. For real parallel multi-session work (separate context windows, worktree isolation), see `mk:team-config`.

### 1. Agent Selection

Based on topic keywords, select 2-4 agents:

| Topic Signals | Agents Selected |
|---------------|----------------|
| architecture, design, system, scale | architect + developer + planner |
| security, auth, token, session, encrypt | security + developer + planner |
| UI, UX, design, responsive, accessible | ui-ux-designer + developer + planner |
| test, coverage, TDD, quality | tester + developer + reviewer |
| performance, latency, optimize, cache | architect + developer + analyst |
| refactor, migration, breaking change | architect + developer + reviewer |
| sprint, retro, what went wrong | planner + developer + tester + reviewer |
| Default (no keyword match) | planner + architect + developer |

User can override with `--agents` flag.

**Selection constraints (canonical):**

- Minimum 2 agents, maximum 4.
- Always include one agent who will IMPLEMENT the decision (usually `developer`).
- Always include one agent who will CHALLENGE the decision (`reviewer`, `security`, or `architect`).
- Never include `orchestrator` or `analyst` in challenge slots — they manage, not debate. (`analyst` may participate in performance-domain rows where it's already mapped.)

### 2. Discussion Rounds

Each round, every selected agent responds to the topic in their role:

- **Round 1:** Each agent states their position (max 150 tokens each)
- **Round 2:** Each agent responds in two dimensions (max 175 tokens combined — slightly higher than Round 1 to accommodate both dimensions):
  - critique, build on, or counter at least one other agent's position
  - name one thing every agent — including itself — has NOT yet addressed (the blind-spot probe forces collective gap detection, not just pairwise critique)
- **Round 3:** Each agent gives final recommendation (max 100 tokens each)

User can interject between rounds. User can say "decide" to skip to synthesis.

See "Example" below for one full round + synthesis at the prescribed token caps.

### 3. Synthesis

After rounds complete (max 3) or user says "decide", produce a synthesis using the canonical Decision Record Template (see "Decision Record Template (canonical)" below). The same template is used for both the in-discussion synthesis output and the persistent memory write — single source of truth.

See "Example" for a populated record.

## Example

Topic: "REST or GraphQL for the public API?"

Selected agents (architecture row): `architect + developer + planner`.

**Round 1 — positions (≤150 tokens each):**

- **architect:** GraphQL surfaces structural coupling earlier — clients declare exact fields, the schema is the contract. REST hides this in undocumented response shapes. Risk: GraphQL adds a resolver layer that can N+1 if not cached. Verdict: GraphQL.
- **developer:** REST is cheaper to implement. We have OpenAPI tooling, existing middleware, no new ops surface. GraphQL needs a schema-codegen pipeline and rate-limit-by-cost (not by-request). Verdict: REST unless the client federation case is real.
- **planner:** What clients are we actually serving? If <3, REST. If 5+ with different field needs, GraphQL pays back. We have 2 today, 4 on roadmap. Verdict: REST now, plan for GraphQL when the 5th lands.

**Round 2 — challenges + blind spots (≤175 tokens combined each):**

- **architect → developer:** "Cheaper to implement" ignores client cost — three iOS engineers writing parallel field-fetchers cost more than one resolver layer. *Blind spot:* nobody has named what "public API" means here. Are external partners on roadmap? That changes the schema-stability calculus entirely.
- **developer → planner:** "Plan for GraphQL when the 5th lands" defers migration cost. If we know it's coming, build now. *Blind spot:* we haven't discussed the auth model. REST + per-route auth is one cost shape; GraphQL field-level auth is another. Both absent from the trade-off so far.
- **planner → architect:** Resolver N+1 is real and we lack query-cost rate limiting — operationally we'd ship a footgun. *Blind spot:* nobody has asked who maintains either layer in 12 months. Bus factor matters more than the technology choice.

**Round 3 — final recommendations (≤100 tokens each):**

- **architect:** GraphQL with persisted queries only. Block ad-hoc queries at the gateway.
- **developer:** REST + a thin BFF layer per client. Defer GraphQL.
- **planner:** REST now, BFF when client #4 lands, GraphQL re-evaluation at #5. Cap each step at one quarter.

**Synthesis (using Decision Record Template):**

```markdown
## 2026-05-09 — Public API: REST first, GraphQL re-eval at client #5
**Context:** 2 clients today, 4 on roadmap; team has REST tooling but no GraphQL ops experience.
**Decision:** REST + per-client BFF. Re-evaluate GraphQL when client #5 ships, with persisted-queries-only as a hard constraint if adopted.
**Rationale:** Operational cost of GraphQL (N+1, no query-cost rate limiting) outweighs schema-coupling benefit at current client count. Migration cost was raised but discounted given <5 clients. Round-2 blind spots also surfaced: external-partner exposure, field-level auth model, and 12-month maintainer bus factor — all flagged as open questions before any GraphQL re-evaluation.
**Dissent:** architect argued for GraphQL-now with persisted queries only. Acknowledged but overruled because the team lacks GraphQL ops experience and the client count doesn't yet justify the operational surface.
**Next Action:** Spec the per-client BFF interface for client #3 (next on roadmap). Cap at 1 sprint; delivery unblocks the re-evaluation criteria.
```

> The verdict in this example is illustrative only — not a project-wide stance on REST vs GraphQL. What it calibrates is response SHAPE: token-bounded position, terse challenge, compressed final recommendation, and a Decision Record that names dissent without erasing it.

## Constraints (Anti-Token-Explosion)

- **Max 4 agents** per session
- **Max 3 rounds** before forced synthesis
- **Max 150 tokens** per agent response in Round 1, **175 tokens** in Round 2 (covers critique + blind-spot probe), **100 tokens** in Round 3
- **Budget ceiling:** ~8K tokens per party session
- **No code changes** during party mode — discussion only

## Prompts

- `prompts/agent-selector.md` — Logic for choosing relevant agents
- `prompts/synthesis.md` — Template for decision summary

## Gotchas

- LLM sycophancy: agents tend to agree rather than critique — prompts explicitly instruct agents to challenge and counter
- Token budget is PER SESSION, not per round — a 4-agent × 3-round session at the new caps (150 / 175 / 100) ≈ 1700 tokens of agent output plus synthesis
- Party mode is discussion-only — if an agent suggests code changes during party, redirect to the normal pipeline after the decision
- Decision write is NOT optional — see "Memory Write" below
- "decide" keyword ends the discussion immediately — don't use it in the topic itself (e.g., avoid "decide between REST and GraphQL")
- `allowed-tools` is intentionally broad: `Bash` for `mkdir -p .meowkit/memory`, `Grep`/`Glob` for topic-keyword grounding against the codebase, `Read` for `prompts/*.md` references, `AskUserQuestion` for the "decide" gate. Do not trim without measuring loss.

## Decision Record Template (canonical)

This template is the single source of truth for both the in-discussion synthesis output and the persistent record written to `.meowkit/memory/decisions.md`. Do NOT introduce alternative shapes elsewhere in the skill.

```markdown
## {ISO-date} — {decision-title}
**Context:** {1-sentence problem}
**Decision:** {chosen option}
**Rationale:** {key reasons from synthesis, including notable Round-2 blind spots}
**Dissent:** {minority position, if any}
**Next Action:** {single concrete first step, OR `(none — decision is its own action)`}
```

**Synthesis rules:**

- Synthesis must be factual — do not invent consensus that didn't emerge.
- If no consensus reached, set `**Decision:** No consensus.` and list the options with their advocates under `**Rationale:**`.
- Always populate `**Dissent:**` if any agent disagreed; "(none)" only if every agent converged.
- Always populate `**Next Action:**`. Use `(none — decision is its own action)` when the decision needs no separate follow-up step (e.g., "use REST" — the codebase choice IS the action). Otherwise name ONE concrete first step (not a list).
- Roll Round-2 blind spots into `**Rationale:**` when they materially shaped the decision; ignore probes that surfaced no new information.

## Memory Write (required, not optional)

After synthesis concludes, append the populated Decision Record (using the template above) to `.meowkit/memory/decisions.md`. Run `mkdir -p .meowkit/memory` first to create the directory if it does not exist.

This step is NOT optional. Decisions lost to session end cannot be recovered.

## Integration

Party mode is opt-in:
- User invokes `/mk:party "topic"`
- Orchestrator may suggest it for COMPLEX architectural decisions
- Never auto-triggered without user consent
- Does not replace or bypass any gates
