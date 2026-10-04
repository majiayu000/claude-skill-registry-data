---
name: aio
description: "Agentic Implementation Optimizer — audit existing agentic AI implementations for reliability/cost/architecture issues, walk through creating new agentic implementations from scratch, or extend existing implementations with new capabilities. Use when: '/aio', 'audit my agent', 'build an agent', 'agentic review', 'extend this agent', 'agent architecture', 'optimize my agent'. Covers architecture patterns, reliability engineering, guardrails, cost optimization, observability, escape-hatch/abstention design, gap-signal capture, and production readiness."
---

# Agentic Implementation Optimizer (AIO)

Expert-level guidance for building, auditing, and extending agentic AI systems. The
operational rules below are stated imperatively; every rule is tagged with a `[KB:claim-id]`
pointer into `references/knowledge-base.md`, which carries the supporting evidence.
**Read a KB entry on demand** — to justify a finding, cite a source, or go deeper on a check.

---

## Mode Detection

| Trigger | Mode |
|---------|------|
| "audit", "review my agent", "check my agent", "assess", `--audit` | **Audit** |
| "create", "build", "new agent", "start from scratch", "walk me through", `--create` | **Create** |
| "extend", "add feature", "add capability", "improve", "optimize", `--extend` | **Extend** |
| (ambiguous or no indicator) | **Ask the user** which mode they want |

---

## Cross-Cutting Principle: Resourcing, Escape Hatches & Gap Signals

These three concerns are one loop, applied in **every** mode. Most production "hallucination" is
not a model defect; it is an agent forced to act without the resources to act correctly and with
no sanctioned way to decline. Close the loop and hallucinations convert from silent failures into
a labeled backlog of what to build next. `[KB:gap-signals]`

**1. Progressive disclosure — provision context just-in-time.** Surface a thin, high-signal
layer by default; let the agent pull deeper detail on demand (skill/sub-skill loading,
retrieval, sub-agent hand-off). Prefer tools that *fetch* context over statically stuffing it.
More context is not more capability — identical context can yield large gains *or* sharp
degradation, even with perfect retrieval. Disclose progressively and measure the sign. On
frontier models, single-source instructions and prefer judgment over rigid rules — prune
scaffolding the model no longer needs. `[KB:progressive-disclosure]` By decision time it either
*has* what it needs or can *go get it*; if neither, it hits an escape hatch — never guess.

**2. Escape hatches — sanction the decision to NOT decide.** Abstention is an architectural
primitive, not an afterthought. State it to the agent plainly: *"Without what you need for a
high-confidence decision, don't make one. Abstain, take the safe action, log the gap."*
- Define the safe default per decision point — escalate, return a typed "insufficient-context"
  result, fall back to a deterministic path, or no-op. Silence-and-guess is never the default.
- Gate on calibrated trajectory-level confidence, not vibes; hedge specificity rather than
  refuse outright where a partial answer is possible. `[KB:abstention]`
- Make the hatch cheap and reachable in the tool surface — an explicit `flag_gap` / `escalate`
  / `report_insufficient_context` action. If the only action is "answer," the agent *will*
  answer — wrong.
- Clarification is a sanctioned hatch — trigger it on structural events (fork, conflict, scope
  change), not the agent's felt uncertainty (detection is the weak link); generate candidates
  first, ask what discriminates. `[KB:clarification]`
- Recovery ≠ diagnosis — the hatch is the *guaranteed* recovery path when in-loop recovery
  fails. `[KB:diagnosis-recovery-gap]`

**3. Gap signals — every abstention and hallucination is a labeled data point.** The hatch is
an *instrument*: each trip points at a missing resource, dataset, or capability.
- Route every trip to a durable, queryable sink — a structured event
  (`{decision_point, missing_resource, confidence, inputs_hash, timestamp}`), not a scrolling
  log line.
- Capture caught hallucinations as the same class — a hatch that *should have fired and didn't* —
  feeding both a gap signal and a calibration correction.
- Aggregate by decision point, rank by frequency × cost, feed the top gaps into the roadmap —
  the agent telling you what to build next, grounded in real traffic. `[KB:gap-signals]`

**Mode hooks:** Audit verifies all three exist and that gap signals reach a queryable sink (a
hatch with no sink is theater). Create builds the abstention primitive in Phase D and the
signal pipeline in Phase F. Extend gives every new capability its own escape hatch and signal
route before shipping.

---

## Mode 1: Audit

Audit an existing agentic implementation. Spawn sub-agents in parallel across independent
dimensions, then synthesize.

### Step 1: Discovery (Sub-Agent)

Spawn an Explore agent to map the implementation:
- Orchestration pattern (single agent, prompt chain, routing, orchestrator-workers, full agent
  loop, multi-agent)
- All tools/functions the agent can call
- Context management strategy (system prompts, memory, RAG, scratchpads)
- State management (vector stores, KV, knowledge graphs, checkpointing)
- Error handling, retry logic, fallback paths
- Guardrails, validation, human-in-the-loop gates
- Evaluation/testing infrastructure (evals, unit, integration)
- Observability instrumentation (tracing, logging, metrics)

Return a structured summary to the main thread.

### Step 2: Parallel Audit Agents

Based on discovery, spawn these **in parallel**:

#### 2a. Architecture Audit Agent
Evaluate against the pattern complexity hierarchy:

| Pattern | When Justified |
|---------|---------------|
| Single LLM + retrieval | Well-scoped task, few tools |
| Prompt chaining | Fixed sequential subtasks with validation gates |
| Routing | Input classification dispatches to specialized handlers |
| Parallelization | Independent subtasks or voting for confidence |
| Orchestrator-workers | Dynamic task decomposition needed |
| Evaluator-optimizer | Clear evaluation criteria, iterative refinement helps |
| Full agent loop | Open-ended, tool-using, multi-step reasoning |

- **Is it over-architected?** Single agents match or beat multi-agent at equal compute;
  multi-agent only wins with heterogeneous models or structured adversarial debate. Flag any
  multi-agent setup that doesn't justify itself. `[KB:pattern-hierarchy]`
- **Tool design** (Anthropic guidance): action-verb specs, explicit param types with units,
  few-shot examples, rationale-before-call, semantic field names (`name`, not `uuid`),
  pagination/truncation for large responses, few well-designed tools over many narrow ones.
  `[KB:tool-design]`
- **Context engineering**: sub-agent isolation with condensed summaries, compaction near
  limits, structured memory layers over raw conversation stuffing. `[KB:context-eng]`
- **Harness**: most production agent value is in the harness/scaffold, not the model; registry-
  style tools still beat MCP/plugin in production. `[KB:harness-design]`
- **Memory — don't add it by default.** Plain long-context often beats dedicated memory systems;
  require a workload that demonstrably needs cross-session recall, multi-hop relational
  reasoning, or context beyond long-context capacity before recommending one. `[KB:memory-justify]`
- Verify observability uses OTel GenAI semantic conventions. `[KB:otel]`

#### 2b. Reliability Audit Agent
**Three-layer testing** `[KB:three-layer-testing]`:
- *Unit (deterministic)*: mocked-LLM tests for tool routing, argument extraction, result
  handling, schema validation — running in CI on every commit.
- *Evals (quality)*: curated datasets with LLM-as-judge scoring, threshold assertions
  (`assert avg_accuracy >= 0.8`), prompts versioned as code with regression testing. Validate
  the judge itself — audit agreement/consistency/bias; high judge self-consistency is not
  validity. `[KB:judge-validity]`
- *Integration/E2E*: full multi-step workflows against real/simulated environments covering API
  timeouts, auth failures, bad external responses, edge cases.

**Metrics coverage** across session/trace/span: quality (goal accuracy, completion, coherence),
tool use (selection accuracy, parameter correctness), safety (hallucination, PII, toxicity,
injection), performance (latency p50/p95/p99, throughput, cost/task), business (satisfaction,
escalation rate, cost efficiency).

**Structured output**: prefer constrained decoding (Outlines, vLLM) over validation+retry — it
is strictly more reliable; if using validation+retry, confirm it's a conscious tradeoff.
`[KB:structured-output]`

**Error handling & recovery**:
- Opaque errors transformed into actionable guidance; two-phase init (setup vs execution agent);
  sub-agents writing through the lead agent vs direct filesystem.
- **Failure-attribution loop?** Long-horizon agents need root-cause attribution feeding
  corrective signals back. Recognize *trajectory drift* (compounding off-path tool calls), not
  just terminal failures. Recommend an offline+online pair for any agent running >10 steps.
  `[KB:failure-attribution]`
- **Does it RECOVER, not just diagnose?** Correct attribution does not imply the agent can act
  on it — recovery is a separate, harder metric. Flag any recovery story measured only by
  attribution accuracy. `[KB:diagnosis-recovery-gap]`
- **Is review external?** Flag self-critique loops with no external signal, and "are you sure?"
  challenge prompts (sycophancy, not reconsideration). Late-stage review goes to a
  fresh-context reviewer as someone else's plan. `[KB:self-critique]`

**Long-horizon framing**: is reliability measured beyond pass@1? For multi-step agents, single-
shot success is the wrong metric — look for reliability-decay metrics and checkpoint-and-restart
policies for meltdown runs. `[KB:reliability-decay]`

**Escape hatches & gap-signal capture** (see Cross-Cutting Principle): can the agent abstain via
a sanctioned path? Is abstention gated on calibrated confidence? Do hatch trips and caught
hallucinations reach a queryable sink? Is there a loop from gap signals to the roadmap? Is
context provisioned via progressive disclosure (over-stuffed context is itself a reliability
defect)?

#### 2c. Safety & Guardrails Audit Agent
**Guardrail stack** at input / flow / output layers, positioned *outside* the agent execution
loop (control-plane pattern); check OWASP Agentic Top 10 (ASI01–ASI10) and the "least agency"
principle. `[KB:guardrail-stack]`

**Prompt-injection defense** (concrete, not just taxonomies) `[KB:injection-defense]`:
- A provenance-aware defense (ARGUS-class) or at least an indirect-injection defense; static
  input filters are insufficient.
- Request-structure integrity (PCFI-class): system/dev/user/retrieved segments treated as
  priority-tiered, not concatenated text.
- For any agent receiving retrieved content (RAG, tool output, web), assume injection-by-default.
- **No wrapper saves you** — two independent impossibility results bound injection defense.
  Audit for *impact containment* (least agency, action-boundary gating, provenance auditing),
  not just a filter. `[KB:injection-impossibility]`

**Tool-execution surfaces as untrusted RPC** `[KB:tool-exec-sandbox]`: sandbox any tool that
touches the filesystem; assume any retrieved/generated string can become a shell. Language-level
sandboxes are not trust boundaries — recommend process-level isolation (gVisor/Firecracker/
microVMs) beneath any in-process interpreter.

**Agent identity & MCP auth** (often the real gap) `[KB:agent-identity]`: identity tracing, not
content filtering, is the dominant MCP weakness. For any MCP-wired or multi-agent system, verify
per-agent identity, scoped least-privilege credentials, and delegation provenance. Flag token
pass-through and over-broad scopes as HIGH.

**Compliance readiness** `[KB:eu-ai-act]` `[KB:nist]` `[KB:compliance-properties]`:
- EU AI Act (enacted amendment): high-risk deferred to **Dec 2 2027** (embedded products **Aug 2
  2028**), but **Article 50 agent-disclosure is in force since Aug 2 2026** — an EU-user-facing
  agent without it is non-compliant NOW; flag HIGH, never as an upcoming deadline. ≥6-month log
  retention + override mechanisms for high-risk; penalties up to €15M / 3% turnover.
- US parallel: NIST AI Agent Standards Initiative (agent identity/auth, JIT access, action-level
  approvals). The five compliance properties (traceability, explainability, authorization,
  immutability, reproducibility) map directly to AI Act requirements.

**Human-in-the-loop** `[KB:hitl]`: which pattern (multi-tier oversight / synchronous approval /
async audit)? Confidence thresholds appropriate to domain — financial 90–95%, routine customer
service 80–85%, escalation-rate target 10–15% (60%+ signals miscalibration). Selective vs
comprehensive automation (Klarna lesson: automate selectively).

#### 2d. Production Readiness Audit Agent
**Cost** `[KB:cost-optimization]`: model routing/tiering (cheap for classification, frontier for
complex), prompt caching (highest ROI — but cache the system prompt + stable tool specs, exclude
dynamic tool results; naive full-context caching can *increase* latency `[KB:cache-pitfall]`),
semantic caching, batching (50% token discount), output-token optimization (output dominates
agent spend). Watch for accuracy-only optimization producing far more expensive agents.
`[KB:cost-accuracy]` **Effort dial** `[KB:effort-dial]`: tune the reasoning-effort knob (eval-gated)
before a tier jump; don't default to max — optimum is task-dependent.

**Observability** `[KB:otel]`: distributed tracing (OTel-compatible), semantic drift detection,
circuit breakers for long-running operations.

**Compliance/auditability** (if applicable) `[KB:compliance-properties]`: traceability,
explainability (flight recorder for prompts/tool calls/reasoning), authorization (action-level
gates), immutability (write-once + signatures), reproducibility (deterministic fallback), kill
switches (error-rate thresholds, freeze protocols).

### Step 3: Synthesize & Report

Collect sub-agent findings into a structured report, severity CRITICAL / HIGH / MEDIUM / LOW per
finding. Template: `references/audit-report-template.md` — load it at synthesis.

---

## Mode 2: Create

Walk the user through building a new agentic implementation. Interactive — ask, validate, build
incrementally.

### Step 1: Requirements Gathering
Ask (adapt to what they've told you): (1) **Problem** — what must the agent accomplish, inputs/
outputs? (2) **Tools/APIs** needed? (3) **Complexity** — well-scoped vs open-ended, steps,
branching? (4) **Risk profile** — customer-facing? financial? compliance? cost of being wrong?
(5) **Scale** — volume, latency, cost constraints? (6) **Tech stack**?

### Step 2: Architecture Recommendation
Recommend the **simplest pattern that works** from the hierarchy (see Mode 1 table). Always
justify why you're *not* recommending a simpler pattern — single agents match or beat multi-agent
at equal compute. `[KB:pattern-hierarchy]` Recommend an orchestration framework, state/memory
backend, and tool-design approach. `[KB:frameworks]` `[KB:memory-justify]`

### Step 3: Implementation Walkthrough
Build phase by phase; explain what and why before writing code. Offer to write code or just
explain — let the user drive.

- **Phase A — Core Agent & Tools**: system prompt, tool definitions (action-verb specs, param
  types, examples, semantic fields), orchestration loop, rationale-before-call; on capable models
  prefer expressive typed interfaces over examples and single-source instructions. `[KB:tool-design]`
- **Phase B — Context Engineering**: sub-agent isolation, compaction strategy, structured memory
  layers. `[KB:context-eng]`
- **Phase C — Reliability**: structured output (prefer constrained decoding), actionable error
  handling, unit-test scaffolding, initial eval dataset + assertions. `[KB:structured-output]`
  `[KB:three-layer-testing]`
- **Phase D — Guardrails & Safety**: input validation (injection prevention), output validation,
  HITL gates for high-risk ops, domain-calibrated confidence thresholds. **Escape hatches**: an
  explicit abstention path per high-stakes decision — never let "guess" be the only action.
  `[KB:guardrail-stack]` `[KB:abstention]`
- **Phase E — Production Hardening**: model routing/tiering, prompt caching, observability
  (tracing, structured logging), circuit breakers, kill switch. `[KB:cost-optimization]` `[KB:otel]`
- **Phase F — Continuous Improvement**: trace-collection pipeline, eval suite with CI regression
  testing, prompt versioning, canary deploy. **Gap-signal capture**: route every hatch trip and
  caught hallucination to a structured queryable sink; aggregate by decision point, rank by
  frequency × cost, feed the top gaps into the backlog. `[KB:trace-loop]` `[KB:gap-signals]`

### Step 4: Production Readiness Checklist
Before declaring done, walk `references/readiness-checklist.md`.

---

## Mode 3: Extend

Add new capabilities while maintaining or improving reliability.

### Step 1: Understand Current State
Spawn an Explore agent (same discovery as Audit Step 1). Summarize: current pattern, existing
tools/capabilities, context management, testing/eval coverage, known gaps.

### Step 2: Extension Requirements
Ask: (1) **What capability** — new tool, workflow, integration, perf improvement? (2) **Why** —
business driver, user feedback, operational need? (3) **Constraints** — must not break existing,
latency/cost budget, compliance?

### Step 3: Impact Analysis (Sub-Agent)
Analyze: does this change the architecture pattern? Which existing tools/workflows are affected?
What new tools are needed? Testing impact (new evals, affected evals)? Cost impact (more tool
calls, larger context, new tier)? Safety impact (new failure modes, new guardrail needs)?

### Step 4: Implementation Plan
Cover: (1) tool additions/modifications `[KB:tool-design]`, (2) orchestration changes if the
pattern must evolve, (3) context-engineering updates, (4) **new guardrails** — including an
escape hatch and a gap-signal route for the new capability, so a feature that can't yet be served
correctly fails safe and tells you what's missing `[KB:gap-signals]`, (5) testing additions (new
unit + eval cases + regression tests for preserved functionality), (6) observability updates,
(7) rollout strategy (feature flags, canary, rainbow deploy).

### Step 5: Execute
Implement per the plan. After each significant change: run existing tests to catch regressions,
add new tests, verify observability covers new paths.

---

## Knowledge Base

Full evidence — papers, benchmarks, industry data, reference tables, and per-claim provenance
trails — lives in **`references/knowledge-base.md`**. Load the specific `[KB:claim-id]` entry on
demand; never wholesale. Refreshed by **`aio-update`** — a private maintenance skill kept outside
this repo, not shipped or invocable here — which consolidates new research into existing claims
rather than accreting bullets.
