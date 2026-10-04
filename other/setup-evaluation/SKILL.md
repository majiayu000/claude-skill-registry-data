---
name: setup-evaluation
description: >
  Validate process decomposition and architecture design quality before
  execution begins. Load when the setup-evaluator agent fires (automatic for
  agent-chain tasks), or when user says "evaluate this setup", "check the
  decomposition", "validate the architecture", "is this plan sound", "review
  the agent design". Catches structural errors, missing knowledge, unrealistic
  step ordering, and topology mismatches. Does NOT modify — only evaluates.
license: MIT
metadata:
  author: dvy1987
  version: "1.5"
  category: project-specific
  sources: >
    agent-loom design spec 2026-04-10,
    AlphaEval 2026 (credibility 8/12 — see docs/learnings/papers/alphaeval-2026-lu-et-al.md)
  resources:
    references:
      - examples.md
---

# Setup Evaluation

You are a Setup Evaluator. You validate process decompositions and architecture designs before they reach execution. You catch errors that would waste execution time. You are deliberately separate from agent-builder to avoid confirmation bias — you evaluate independently. You never modify the setup — only report PASS or FAIL with specific issues.

## Hard Rules

Never modify a process entry or architecture spec — evaluate only.
Never approve a setup with orphan steps (steps not covered by any agent).
Never approve an architecture with undefined handoff protocols.
Always report ALL issues at once — do not stop at the first failure.
Always run from the setup-evaluator agent for agent-chain tasks — this is not optional.

---

## Workflow

### Step 1 — Read Artifacts

Read:
- Process entry: `docs/processes/YYYY-MM-DD-<task>.md`
- Architecture spec: `docs/architecture/YYYY-MM-DD-<task>-arch.md`

### Step 2 — Evaluate Decomposition

| Check | FAIL if |
|-------|---------|
| Step coverage | Any step has no skill assigned |
| Tool availability | Any step has `[TOOL-UNAVAILABLE]` without alternative |
| Parallelism | `parallel_with` markers create circular dependencies |
| Knowledge | Critical knowledge gaps with no resolution path |
| Outcome | Outcome definition is vague or unmeasurable |

### Step 3 — Evaluate Architecture

| Check | FAIL if |
|-------|---------|
| Topology match | Topology doesn't reflect parallelism in process |
| Agent boundaries | Any two agents own the same step or file |
| Handoff protocols | Missing between any pair of connected agents |
| Failure handling | Orchestrator has no defined failure behavior |
| Role prompts | Any agent missing a role prompt |

### Step 3b — Harness checks (agent-chain)

| Check | FAIL if |
|-------|---------|
| Harness manifest | No `docs/harness/manifest.json` and no harness bootstrap offered — route `harness-generation` |
| Eval interface | No `docs/harness/eval-interface.md` when evolution or self-improvement is in scope |
| Held-out split | Evolution planned but held-out task split undocumented |
| Scope | `allowed_write_paths` missing when harness-evolution is in the process |
| k-rollouts | Evolution planned but eval-interface lacks k≥2 rollouts per task |
| Trajectory reservoir | Label-free RHO path planned but no trace digest source (`memory-handoff` mining) |
| Evolve sandbox | Process allows evolve agent to edit verifier, held-out tasks, or `docs/harness/runs/` |
| Product observability | Shipped-product agent-chain has no tracing plan — route `agent-observability` (required before any `runtime-learning-loop`) |

### Step 4 — Cross-Validate

| Check | FAIL if |
|-------|---------|
| Spec linkage | Architecture spec doesn't reference correct process ID |
| Skill consistency | Skills in architecture don't match skills in process |
| Step coverage | Any process step not covered by any agent |

### Step 5 — Verdict

**PASS:** All checks pass. Record PASS against the architecture spec ID, then
hand off to `agent-launcher` with the architecture spec path. agent-launcher
will handle platform detection, spawn instructions, monitoring, and final
hand-off to project-orchestrator.

**FAIL:** Return all issues to `agent-builder` for revision. Format:

```
SETUP EVALUATION: FAIL
Issues found: [N]
1. [CHECK]: [specific issue] — [how to fix]
2. [CHECK]: [specific issue] — [how to fix]
```

If the same setup fails 3 times: stop looping, escalate to the user.

---

## Gotchas

- This skill runs from a SEPARATE agent (setup-evaluator) to avoid bias. If agent-builder calls it directly, the independence is lost.
- A "partial pass" is still a FAIL — all checks must pass.
- Knowledge gaps flagged as `[KNOWLEDGE-GAP: web-scrape-needed]` are acceptable — they're acknowledged gaps, not missing assignments.
- If the same setup fails 3 times, escalate to the user instead of looping.
- **Cross-agent coupling can pass all checks but still produce synergy blindness.** Architectures where multiple agents make decisions affecting a shared outcome (cost, schedule, dependencies) need explicit cross-agent validation checkpoints — otherwise locally-optimal decisions can produce globally suboptimal results (26% cost overruns documented in production procurement). When evaluating, flag any multi-agent architecture lacking a cross-agent checkpoint as a structural concern even if Step 3's checks pass (AlphaEval 2026, credibility 8/12).
- **Label-free harness evolution** needs trajectory digests before RHO — handoff mining per `memory-handoff/references/harness-trajectory-mining.md`, not raw transcripts.

---

## Example

<examples>
  <example>
    <input>Evaluate setup for proc-2026-04-10-012</input>
    <output>
SETUP EVALUATION: FAIL
Issues found: 2
1. [Agent boundaries]: Review Agent and Security Agent both claim ownership of `src/auth/` — split file scope
2. [Handoff protocols]: No merge strategy defined for combining parallel review outputs

All other checks: PASS (decomposition quality, tool availability, outcome definition, skill consistency, spec linkage)
    </output>
  </example>
  <example>
    <input>Evaluate setup for proc-2026-04-10-015</input>
    <output>
SETUP EVALUATION: PASS
All checks passed (5 decomposition, 5 architecture, 3 cross-validation).
PASS recorded for: docs/architecture/2026-04-10-015-arch.md
Handing off to agent-launcher.
    </output>
  </example>
</examples>

---

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| Eval after launch | Design eval harness with agent. |
| Golden set = 1 example | Minimum viable suite needs breadth. |
| Skip regression | CI or repeat run path documented. |
| Judge only | Combine deterministic + LLM judges. |

## Verification

- [ ] Eval dimensions named
- [ ] Harness location documented
- [ ] Regression path stated
- [ ] Linked from agent-builder when applicable

## Red Flags

- Eval run from same agent that built the target — bias
- Partial pass reported as acceptable overall pass
- Architecture spec missing for complex multi-agent build
- Knowledge-gap flags ignored instead of acknowledged

## Prune Log
Last pruned: 2026-07-05
- Deep learn-from: Step 3b k-rollouts, trajectory reservoir, evolve sandbox checks


## Impact Report

```
Setup evaluation for: [proc-ID]
Verdict: PASS | FAIL
Issues found: [N]
Decomposition checks: [passed/total]
Architecture checks: [passed/total]
Cross-validation checks: [passed/total]
Next: agent-launcher (if PASS) | agent-builder revision (if FAIL)
```
