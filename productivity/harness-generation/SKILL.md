---
name: harness-generation
description: >
  Seed minimal agent harness v0 — manifest, eval checks stub, governance. AUTO-INVOKED
  after project-setup or retroactive-project-setup when docs/harness/manifest.json
  is missing. Also triggers on: generate harness, scaffold agents, agent bootstrap,
  first time agents in this repo, new project agent setup, set up agent harness,
  agent onboarding files, missing agent configuration, agent instructions setup,
  make agents read project rules, agent reliability setup, agents not configured.
  Pairs with project-setup. Evolution is harness-evolution.
license: MIT
metadata:
  author: dvy1987
  version: "1.2"
  category: project-specific
  sources: >
    AHE arXiv:2604.25850, Meta-Harness arXiv:2603.28052, harnessforge patterns,
    metaharness scaffold, Self-Harness arXiv:2606.09498
  resources:
    references:
      - component-manifest.md
      - scaffold-patterns.md
      - examples.md
---

# Harness Generation

You seed a **minimal, auditable harness v0** — the scaffold around a model (prompts,
tools, skills, memory hooks, lifecycle, verification interface, governance). You do
not evolve harnesses; route ongoing improvement to `harness-evolution`.

## Trigger Discipline

**Auto-invoke** when chained from `project-setup` 6c, `retroactive-project-setup`, `harness-engineering` Step 0, or `setup-evaluation` harness FAIL. See `harness-engineering/references/harness-readiness-gate.md`.

## Hard Rules

Never generate a harness without a versioned **component manifest** (`docs/harness/manifest.json`).
Never ship a pre-tuned bloated harness — v0 is minimal; components earn their place via measured rollouts (AHE).
Never rely on prompt-only harness — tools, middleware, skills, and eval interface are required surfaces (AHE ablation).
Never overwrite user-edited harness files without manifest drift check — refuse or merge explicitly.
Never claim self-improving without eval interface stub + pointer to `harness-evolution`.
Never embed external repo URLs in generated artifacts — distill patterns locally.

---

## Workflow

### Step 1 — Classify delivery context

| Context | v0 focus |
|---------|----------|
| agent-loom skill library project | Skill routing, AGENTS.md orchestration map, eval stub for skill quality |
| Consumer app repo | AGENTS.md, `.agents/skills/`, forbidden paths, key commands |
| Legacy repo (no AGENTS.md) | Gap-fill only — pair with `retroactive-project-setup` first |
| Multi-agent chain planned | Manifest only — topology is `agent-builder`, not this skill |

### Step 2 — Inventory repo (silent)

Read: manifests, existing `AGENTS.md`, `.agents/skills/`, CI configs, `docs/memory/`,
`docs/evals/`, `docs/harness/`. Auto-extract commands per `project-setup` Step 1b.

### Step 3 — Emit component manifest

Write `docs/harness/manifest.json` per `references/component-manifest.md`:
seven orthogonal components (prompt, tools, middleware, skills, sub-agents, memory, governance),
each with path, version, sha256, and `generated|user-edited` status.

### Step 4 — Scaffold artifacts

Apply patterns from `references/scaffold-patterns.md`:

1. **Prompt / routing** — merge into `AGENTS.md` or create harness section; keep ≤150 lines total.
2. **Skills** — ensure Skill Invocation block present; list installed skills in Orchestration Map.
3. **Tools** — document MCP/tool surfaces in manifest; stub `docs/harness/tools.md` if needed.
4. **Governance** — forbidden paths, allowed-write scopes, verifier sandbox rules.
5. **Eval interface stub** — `docs/harness/eval-interface.md` + empty `docs/harness/tasks.json` shape
   (file_phrase + command checks per metaharness pattern).
6. **Environment bootstrap** — compact snapshot block (stack, key commands, git branch) for meta-agents.

If `project-setup` already ran: **merge**, never replace user interview content.

### Step 5 — Drift gate

Document `harness sync --check` equivalent: compare manifest hashes to disk; flag user-edited files
skipped on re-run. CI recommendation in manifest notes.

### Step 6 — Hand off

| Next need | Route |
|-----------|-------|
| Full AGENTS.md interview missing | `project-setup` |
| Eval rubric + regression suite | `eval-rubric-design` → `eval-pipeline` |
| Improve harness from failures | `harness-evolution` (requires eval harness) |
| Multi-agent design | `agent-builder` (orthogonal) |

Append to `docs/skill-outputs/SKILL-OUTPUTS.md`. Log harness version `v0` in `docs/memory/current-state.md` if memory suite installed.

---

## Gotchas

- **Minimal seed is mandatory.** Pre-tuned harnesses contaminate attribution — every component added later must justify itself with traces (Self-Harness, AHE).
- **AGENTS.md must stay lean.** RHO/Codex paths cap combined project docs ~32KB — routing belongs in skills, detail in L3 refs.
- **Harness ≠ agent topology.** `agent-builder` designs who talks to whom; this skill designs what files/tools/prompts wrap the model.
- **Deterministic scaffold beats one-shot LLM init.** Inspect → plan → staged writes → manifest (harnessforge pattern); LLM fill is optional fallback only.
- **Blueprint validators that shell out are a trust boundary** — document, never auto-run untrusted commands.

---

## Output Format

```
Harness generation complete
Version: v0
Context: [library | consumer | legacy-gap-fill]
Manifest: docs/harness/manifest.json
Artifacts: [list paths]
Eval stub: docs/harness/eval-interface.md
Drift check: [documented command]
Next: [eval-pipeline | harness-evolution | project-setup]
```

---

## Example

<examples>
  <example>
    <input>Generate a harness for this React monorepo — we have AGENTS.md from project-setup.</input>
    <output>
Harness generation complete
Version: v0 | Context: consumer
Manifest: docs/harness/manifest.json (7 components, all generated)
Merged: Skill Invocation + Orchestration Map preserved from interview
Created: docs/harness/eval-interface.md, docs/harness/tasks.json (stub), docs/harness/governance.md
Next: eval-rubric-design to define harness regression dimensions
    </output>
  </example>
</examples>

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "AGENTS.md is enough" | No manifest, eval stub, or governance = not a harness v0 |
| "Skip eval stub for now" | harness-evolution hard-fails without it |
| "Copy external harness README" | Distill patterns; secure-scan; no URL embed |
| "Let LLM write the whole harness" | Deterministic manifest + merge beats opaque generation |
| "Agent-builder already ran" | Topology ≠ harness files — run both |

## Verification

- [ ] `docs/harness/manifest.json` exists with 7 components and hashes
- [ ] Eval interface stub + tasks.json shape present
- [ ] AGENTS.md ≤150 lines; user content preserved on merge
- [ ] Governance forbidden paths documented
- [ ] SKILL-OUTPUTS.md appended

## Red Flags

- Harness v0 bloated with speculative prompts/tools
- User-edited files overwritten without merge
- No eval interface stub when evolution is planned
- External SKILL.md vendored wholesale

## Prune Log
Last pruned: 2026-07-05
- Deep learn-from: scaffold-patterns L3 — drift CI, interface validation, AHE sandbox

## Impact Report

```
Harness v0 generated: [context]
Manifest: docs/harness/manifest.json | Components: 7
Eval stub: [yes/no] | Merged AGENTS.md: [yes/no]
Files created: [count] | Next route: [skill]
```

## Reference Files

- `references/component-manifest.md` — seven components, JSON schema, ETCLOVG map
- `references/scaffold-patterns.md` — inspect→render, drift CI, bootstrap snapshot
- `references/examples.md` — library project + consumer repo worked examples
