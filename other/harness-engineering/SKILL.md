---
name: harness-engineering
description: >
  Orchestrator for agent harness work — the setup that makes AI agents follow
  project rules and improve when they fail. FIRES PROACTIVELY when agents
  misbehave, repeat mistakes, ignore instructions, skip skills, or when
  AGENTS.md exists but docs/harness/manifest.json is missing. Also triggers on:
  harness engineering, agent scaffold, agent keeps failing, agent not following
  instructions, make agents reliable, agents going off rails, agent forgot
  context, improve agent setup, self-improving agents, agents keep making
  mistakes, why is my agent bad, agent quality, agent setup broken, agents
  ignore skills, same mistake again, fix agent behavior, tune agent
  instructions, set up agent infrastructure, after project setup agents still
  bad. Routes bootstrap vs evolution. Not multi-agent topology — agent-builder.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: >
    AHE arXiv:2604.25850, Self-Harness arXiv:2606.09498, auto-harness PROGRAM.md,
    docs/plans/2026-07-05-harness-skills-research-and-implementation-plan.md
  resources:
    references:
      - routing.md
      - harness-readiness-gate.md
      - examples.md
---

# Harness Engineering

You are the harness orchestrator. You route **bootstrap** vs **evolution** vs **audit**,
ensure eval prerequisites exist, and keep harness work separate from agent topology design.

## Trigger Discipline

**Proactive — user need not say "harness."** Fire when: agent misbehavior symptoms; `AGENTS.md` without `docs/harness/manifest.json`; post-`project-setup` backfill; self-improvement claims. Full symptom table: `references/harness-readiness-gate.md`.

## Hard Rules

Never conflate harness work with `agent-builder` — topology is who; harness is what wraps the model.
Never route to `harness-evolution` without eval harness — bootstrap eval first.
Never skip `harness-generation` on greenfield projects before evolution.
Never execute child skill workflows yourself — delegate and synthesize reports.
Never present the route plan before invoking child skills (unless user said "go ahead").

---

## Workflow

### Step 0 — Harness readiness scan (mandatory)

Read `references/harness-readiness-gate.md`. Silent: manifest exists? eval interface? symptoms?
No manifest → bootstrap. Manifest + symptoms → evolution. Self-improvement claim → `reality-check`.

### Step 1 — Classify intent

| Signal | Route |
|--------|-------|
| New project / no `docs/harness/manifest.json` | Step 2 bootstrap |
| "Improve" / failures / plateau / self-improving | Step 3 evolution |
| Legacy repo, no AGENTS.md | `retroactive-project-setup` → bootstrap |
| "Is it self-improving?" / claim audit | `reality-check` |
| Multi-agent / topology / "design agents" | `agent-builder` (harness orthogonal) |
| Eval only | `eval-output` |

Read `references/routing.md` for disambiguation vs `project-setup` and `project-orchestrator`.

### Step 2 — Bootstrap path

```
project-setup (if no AGENTS.md) → harness-generation (v0)
  → eval-rubric-design (harness dimensions)
  → eval-pipeline (regression stub)
```

Skip `project-setup` if populated AGENTS.md exists — merge via `harness-generation` only.

### Step 3 — Evolution path

Precondition check (delegate verification to `harness-evolution` Step 0):
- manifest exists
- eval harness operational
- held-out split defined

If missing: run bootstrap substeps, then `harness-evolution`.

### Step 4 — Agent-chain coordination

When user is building multi-agent systems:
1. `harness-generation` if no v0 (parallel-safe with `process-decomposer`).
2. `agent-builder` for topology.
3. `setup-evaluation` must PASS harness + eval checks before `agent-launcher`.

### Step 5 — Unified report

Present child skill outputs in one summary (see Output Format).

---

## Gotchas

- **Harness is a first-order performance lever** — same model, different harness, double-digit pass-rate swings (AlphaEval, Self-Harness).
- **Harness is model-specific** — evolved harness vN may not transfer unchanged across model families without re-validation.
- **PROGRAM.md pattern** (auto-harness): human writes optimization directive; agent edits declared surfaces only — good for long improvement campaigns.
- **Self-improvement without eval trajectory is a 4/10 claim** — `reality-check` standard.

---

## Output Format

```
=== Harness Engineering Report ===
Intent: [bootstrap | evolution | audit | topology-handoff]
Routes invoked: [skills]

=== Harness State ===
Version: [vN] | Manifest: [path]
Eval harness: [ready | missing → action]

=== Child Results ===
[per-skill summaries]

=== Next ===
[recommended follow-up]
```

---

## Example

<examples>
  <example>
    <input>Improve my agent harness — it keeps failing on lint steps.</input>
    <output>
=== Harness Engineering Report ===
Intent: evolution
Routes: harness-evolution (round 1), eval-pipeline (regression)

=== Harness State ===
Version: v0 → v1 | Eval harness: ready

=== Child Results ===
Diagnosed: Verification layer | Promoted middleware pre-lint hook

=== Next ===
Run round 2 only if held-out plateaus
    </output>
  </example>
</examples>

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "agent-builder handles harness" | Topology only — run harness-generation |
| "Skip eval for quick fix" | harness-evolution hard-fails — route eval first |
| "project-setup is enough" | One-shot AGENTS.md ≠ versioned harness + eval stub |
| "I'll evolve prompts only" | AHE ablation: prompt-only regresses |
| "Orchestrator does the work" | Delegate to child skills |

## Verification

- [ ] Correct child skill selected per intent table
- [ ] Evolution not routed without eval precondition
- [ ] agent-builder requests include harness v0 check
- [ ] Unified report presented

## Red Flags

- harness-evolution invoked without eval harness
- Harness conflated with multi-agent topology
- Bootstrap skipped on greenfield evolution request

## Prune Log
Last pruned: 2026-07-05
- Deep learn-from: routing.md Pareto frontier; INGEST-QUEUE pairwise compares cleared

## Impact Report

```
Harness engineering: [intent]
Child skills: [list] | Harness version: [vN]
Eval ready: [yes/no] | Promoted: [yes/no]
```

## Reference Files

- `references/routing.md` — disambiguation matrix, lifecycle map, PROGRAM.md pattern
- `references/harness-readiness-gate.md` — proactive triggers, symptom phrases, readiness checklist
- `references/examples.md` — bootstrap, evolution, and agent-chain coordination examples
