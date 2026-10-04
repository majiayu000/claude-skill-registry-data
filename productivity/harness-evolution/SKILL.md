---
name: harness-evolution
description: >
  Improve agent reliability over time — diagnose why agents fail and fix the setup.
  Triggers on: agent keeps failing, same mistake again, agent not improving, make
  agent smarter, agent quality plateau, agents ignore skills, agent skips tests,
  fix agent behavior, agent unreliable, improve agent setup, self-improving
  harness, agents worse over time, tune agent instructions, agent going in
  circles, agent ignores AGENTS.md, repeated agent errors. Requires harness v0
  and eval harness. AUTO-ROUTED from harness-engineering on symptoms. Not first
  setup — harness-generation first.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: >
    AHE arXiv:2604.25850, Self-Harness arXiv:2606.09498, HarnessFix arXiv:2606.06324,
    RHO arXiv:2606.05922, auto-harness, metaharness
  resources:
    references:
      - evolution-loop.md
      - diagnosis-etclovg.md
      - examples.md
---

# Harness Evolution

You close the harness improvement loop: **execute → trace → diagnose layer → propose
minimal edit → regression validate → promote or reject**. Model weights are out of scope.

## Hard Rules

Never run an evolution round without **harness vN manifest** and **operational eval harness**.
Never propose an edit without trace evidence tied to a failure cluster.
Never accept an edit without regression gate: held-in Δ ≥ 0 AND held-out Δ ≥ 0 AND max(Δ) > 0 (Self-Harness).
Never make outcome-only edits — attribute failure to an ETCLOVG layer first (HarnessFix).
Never allow evolve agent to modify verifier config, eval held-out tasks, or LLM API keys (AHE sandbox).
Never promote prompt-only changes when tools/middleware/skills are the diagnosed layer (AHE ablation).
Never bypass file-scope guard — edits only to paths declared in manifest `allowed_write`.

---

## Workflow

### Step 0 — Preconditions (mandatory)

Verify:
1. `docs/harness/manifest.json` exists (else → `harness-generation`).
2. `docs/harness/eval-interface.md` + regression task set defined (else → `eval-rubric-design` → `eval-pipeline`).
3. Held-out split documented — **never fed to proposer** (Self-Harness, Meta-Harness).

FAIL fast with specific route if any missing.

### Step 1 — Capture traces

Collect from: benchmark runs, `docs/memory/agent-handoffs.md`, session logs, or
`docs/harness/runs/iteration_NNN/`. Distill to layered digest per AHE experience observability —
raw millions of tokens are not fed to the proposer.

### Step 2 — Diagnose (ETCLOVG + HTIR)

Per `references/diagnosis-etclovg.md`:
- Normalize traces to step-level nodes (HarnessFix HTIR pattern).
- Attribute each failure cluster to one primary layer: Execution, Tooling, Context,
  Lifecycle, Observability, Verification, Governance.
- Consolidate recurring flaws into actionable records — one mechanism per record.

### Step 3 — Propose diverse-minimal candidates

Generate K candidate edits (default K=3), each:
- Tied to **one** failure mechanism (Self-Harness).
- Scoped to manifest `allowed_write` paths (metaharness scope guard).
- Documented with **evidence quad** (AHE): failure evidence, root cause, targeted fix, predicted impact.

Write `docs/harness/evolve/change_manifest.json` before evaluation.

### Step 4 — Regression validate

Invoke `eval-pipeline` (harness regression mode) on held-in + held-out splits.

| Gate | Rule |
|------|------|
| Self-Harness acceptance | held-in Δ ≥ 0 AND held-out Δ ≥ 0 AND improvement > 0 |
| Scope | No files outside `allowed_write` |
| No-change | Zero file changes → inherit parent scores, do not promote (metaharness) |
| pass@1 | Optimize pass@1, not pass@k flaky strategies (AHE) |

### Step 5 — Promote or reject

**Accept:** bump manifest version to vN+1, update hashes, archive run under `docs/harness/runs/`.
**Reject:** log predicted-vs-actual in manifest; if same flaw persists 2+ rounds at same layer → rollback component and pivot layer (AHE).

Optional **label-free path** (RHO): when no labeled eval exists, use self-consistency +
pairwise self-preference among candidates — still require positive mean score before promote.

### Step 6 — Memory + handoff

On promote: `memory-capture` with harness version, delta metrics, and changed components.
Append `docs/skill-outputs/SKILL-OUTPUTS.md`.

---

## Gotchas

- **Compressed feedback loses credit assignment** — never reduce traces to scalar score only (Meta-Harness).
- **Runtime supervision patches** suppress errors without fixing harness flaws — reject as edits (HarnessFix).
- **Self-attribution misses regressions** — manifest must list `risk_tasks` predicted to break (AHE).
- **Generic prompt bloat** — every instruction must map to a diagnosed failure cluster.
- **Label-free RHO is fallback** — prefer verifier-backed regression when labels exist.

---

## Output Format

```
Harness evolution — round [N]
Diagnosed layer: [ETCLOVG]
Candidates: [K] | Accepted: [id or none]
Held-in Δ: [x] | Held-out Δ: [y]
Promoted: v[N] → v[N+1] | [rejected — reason]
Changed components: [list]
Next: [another round | reality-check claim audit]
```

---

## Example

<examples>
  <example>
    <input>Agent keeps retrying the same failing tool call — improve the harness.</input>
    <output>
Harness evolution — round 1
Diagnosed layer: Tooling (F6 tool-use loop)
Candidates: 3 | Accepted: candidate-2 (middleware retry cap + alternate tool path)
Held-in Δ: +2 | Held-out Δ: +1
Promoted: v0 → v1 | Changed: docs/harness/middleware.md, tool descriptions
    </output>
  </example>
</examples>

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Skip eval — vibes say it's better" | No regression gate = unfalsifiable (reality-check) |
| "Fix in the prompt only" | AHE: prompt-only regresses; fix diagnosed layer |
| "Use test failures as held-out" | Contaminates proposer — splits are sacred |
| "One big harness rewrite" | Diverse-minimal proposals beat monolithic edits |
| "Evolve without manifest" | No attribution, no rollback |

## Verification

- [ ] Preconditions verified (manifest + eval harness + held-out split)
- [ ] Failure attributed to ETCLOVG layer with trace refs
- [ ] change_manifest.json with evidence quad
- [ ] Regression run via eval-pipeline
- [ ] Promotion only if dual-split rule passes

## Red Flags

- Evolution round without eval harness
- Held-out tasks leaked to proposer
- Scope violations in edited files
- Prompt bloat without failure mapping

## Prune Log
Last pruned: 2026-07-05
- Deep learn-from: evolution-loop, diagnosis-etclovg, examples L3 (5 papers + 5 repos)

## Impact Report

```
Harness evolution round [N]: [accepted|rejected]
Layer: [ETCLOVG] | v[N]→v[N+1]
Held-out Δ: [x] | Components changed: [list]
eval-pipeline: [run id]
```

## Reference Files

- `references/evolution-loop.md` — full loop, auto-harness 3-step gate, filesystem artifact store
- `references/diagnosis-etclovg.md` — HTIR nodes, layer attribution, flaw records
- `references/examples.md` — accept, reject, and RHO fallback examples
