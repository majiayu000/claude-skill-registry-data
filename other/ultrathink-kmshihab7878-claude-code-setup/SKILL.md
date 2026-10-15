---
name: ultrathink
description: Cognitive depth engine for Claude Code. Defines 5 thinking modes (quick → council), activation triggers, quality bars, reasoning scaffolds, and the ultrathink protocol for complex multi-domain decisions. Use when a task requires deep synthesis before action — architecture decisions, security reviews, strategic planning, cross-system design. Pairs with /ultraplan for full execution.
---

# Ultrathink — Cognitive Depth Engine

The thinking depth control system for CoreMind. Five modes, each with explicit activation criteria, quality bars, and tool bindings. Never over-think simple tasks. Never under-think critical ones.

> "Depth of thought is proportional to the cost of being wrong."

---

## The 5 Modes

### Mode 0: Quick (< 30 seconds)

**Activate when:**
- Single-file edit with clear requirements
- Lookup (docs, file contents, status check)
- Trivial bug with obvious fix
- Formatting, naming, comment update

**Protocol:**
- No special reasoning scaffolding
- Read → act → verify in one pass
- No subagents, no planning stage
- Direct tool calls only

**Quality bar:** Output is correct and complete. Nothing more required.

---

### Mode 1: Standard (1-2 minutes)

**Activate when:**
- Multi-file change with clear requirements
- API endpoint, test generation, refactor of known pattern
- Debugging with a hypothesis already formed

**Protocol:**
- Read relevant files before acting
- Verify understanding before each edit
- One round of self-check before delivery
- Qwen Code dispatch for L5-L6 subtasks

**Quality bar:** No regressions, meets requirements, passes linter.

---

### Mode 2: Deep Think (5-10 minutes)

**Activate when (any of these):**
- Task touches 3+ files or 2+ system layers
- Architecture decision with non-obvious tradeoffs
- Debugging without a clear root cause
- New feature with downstream effects
- Security-adjacent change
- Keyword: "think hard", "complex", "architecture"

**Protocol:**
1. Load CONTEXT_MAP (PRE-STAGE 0 from /ultraplan)
2. Use `mcp__sequential__sequentialthinking` for multi-step analysis (5-10 thoughts)
3. Enumerate at least 2 alternative approaches before committing
4. Check MEMORY.md for relevant confidence facts
5. State the root cause or core decision explicitly before acting
6. Route via DAG (Stage 4 mini-version): identify critical path
7. Subagents if parallelizable

**Quality bar:** Root cause stated. Tradeoffs enumerated. Evidence collected. Two approaches considered.

**Invocation:** Think through the problem using sequential reasoning tool before writing any code.

---

### Mode 3: Ultrathink (20-30 minutes)

**Activate when (any of these):**
- Cross-system design (frontend + backend + DevOps together)
- Architectural decision that affects >5 files or entire subsystem
- Security audit, incident response, data migration
- Strategic planning (product, revenue, go-to-market)
- Task complexity = enterprise
- Keyword: "ultrathink", "enterprise", "critical", "strategic", "design the system"

**Protocol:**
1. **Full Knowledge Synthesis** — run PRE-STAGE 0 of /ultraplan (all 3 layers in parallel)
2. **Sequential Reasoning Chain** — `mcp__sequential__sequentialthinking` with 10-20 thoughts
3. **Multi-perspective scan** — for each aspect: security, scalability, maintainability, cost
4. **Agent council (mini)** — invoke 2-3 specialized agents for independent perspectives:
   - System-architect for structural decisions
   - Security-engineer for any auth/data/secrets concerns
   - Performance-engineer for bottleneck analysis
5. **Enumerate 3+ alternatives** — with explicit tradeoff matrix
6. **Risk assessment** — T-tier assignment for every action in the plan
7. **DAG construction** — explicit dependency graph with critical path
8. **KB article draft** — before executing, draft the wiki/ article this will produce
9. **Execute via /ultraplan pipeline** — all 15 stages active

**Quality bar:**
- ≥ 3 alternatives considered
- Tradeoff matrix populated
- Risk tier assigned to every action
- Root cause or core insight explicitly stated
- Knowledge capture planned before execution begins

**Tools activated:**
- `mcp__sequential__sequentialthinking` (mandatory)
- claude-mem semantic search (mandatory)
- `council` skill (if strategic domain)
- `architecture-radar` skill (if infrastructure domain)
- `security-review` skill (if security-adjacent)

---

### Mode 4: Council (60+ minutes)

**Activate when (any of these):**
- Business-level decisions (pricing, strategy, market entry)
- Critical security incident
- Major architecture overhaul (entire system redesign)
- Conflicting constraints with no obvious resolution
- Keyword: "council", "full analysis", "executive decision", "bet-the-business"

**Protocol:**
1. All ultrathink steps, plus:
2. Invoke `business-panel-experts` agent for strategic framing
3. Invoke full `/council` command — multi-expert panel (Christensen, Porter, Drucker, etc.)
4. Produce a formal decision memo in `~/.claude/kb/outputs/decision_<topic>_<date>.md`
5. Present executive summary, 3 options, recommended path, reversibility assessment
6. Require explicit user approval before any T1+ action

**Quality bar:**
- Decision memo produced
- ≥ 3 experts' perspectives synthesized
- Reversibility explicitly assessed
- User approval obtained before execution

---

## Activation Map

| Signal | Mode | Why |
|--------|------|-----|
| "fix typo", "rename", "format" | Quick | Trivial, low risk |
| "add endpoint", "test", "refactor" | Standard | Contained scope |
| "think hard", "debug this", "architecture" | Deep Think | Tradeoffs involved |
| "ultrathink", "design the system", "critical" | Ultrathink | Cross-system, high stakes |
| "council", "strategic decision", "full analysis" | Council | Business-level, irreversible |
| task.complexity = enterprise | Ultrathink | Forced by intent parse |
| task.risk_level = critical | Ultrathink | Forced by intent parse |
| task.action_tier = T3 | Council | Forced by governance gate |
| keyword hook: "architect" / "design" | Deep Think | system-architect auto-activated |

---

## Reasoning Scaffold (for Deep Think + Ultrathink)

Use this structure with `mcp__sequential__sequentialthinking`:

```
Thought 1: What exactly is being asked? (restate in your own words)
Thought 2: What do I already know? (CONTEXT_MAP synthesis)
Thought 3: What are the constraints? (technical, time, risk, compliance)
Thought 4: What are the 3 main approaches?
Thought 5: What are the tradeoffs of each?
Thought 6: What does prior work suggest? (MEMORY.md facts, KB wiki)
Thought 7: What is the critical decision point?
Thought 8: What is the optimal approach and why?
Thought 9: What could go wrong with that approach?
Thought 10: What is the mitigation for each risk?
Thought 11+: [domain-specific analysis as needed]
Final: State the chosen approach, expected outcome, and first action
```

---

## Anti-Patterns (Never Do)

- Never apply Mode 3/4 to trivial tasks — wastes tokens and time
- Never apply Mode 0/1 to T2+ risk actions — governance violation
- Never start sequential reasoning without loading CONTEXT_MAP first
- Never skip tradeoff enumeration for architectural decisions
- Never end ultrathink without a concrete first action
- Never invoke council for decisions that don't require human approval

---

## Integration Points

- `/ultraplan` — ultrathink is the cognitive engine; ultraplan is the execution pipeline
- `governance-gate` skill — risk tier determines minimum thinking mode (T2 → Deep Think, T3 → Council)
- `council` command — Mode 4 always invokes it
- `mcp__sequential__sequentialthinking` — mandatory for Mode 2+
- claude-mem — mandatory context load for Mode 2+
- `~/.claude/kb/wiki/` — output destination for knowledge captured during ultrathink

---

## Quality Bars Summary

| Mode | Min. Alternatives | Sequential MCP | Agent Council | KB Capture | User Approval |
|------|------------------|----------------|---------------|------------|---------------|
| Quick | 0 | No | No | No | No |
| Standard | 0 | No | No | Optional | No |
| Deep Think | 2 | Yes | No | Yes (if new) | T2+ only |
| Ultrathink | 3 | Yes | 2-3 agents | Yes | T2+ always |
| Council | 3+ | Yes | Full council | Yes | Always |
