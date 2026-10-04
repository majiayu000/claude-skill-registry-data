---
name: dependency-map
description: Extract a thesis's dependency fingerprint — the external variables its bull case actually rests on (key customers, suppliers/inputs, technology transitions, macro drivers, single points of failure). Use when user says "dependency map", "what does [TICKER] depend on", "dependency fingerprint", or "map exposures for [TICKER]".
---

**Codex execution:** Read `.agents/skills/_shared/codex-compat.md` first. Treat `SKILL_ARGS` as the arguments supplied with `$dependency-map`, or infer them from the user's request when this skill is invoked implicitly.

**Follow AGENTS.md Writing Standards strictly.** Lead with the dependency and its magnitude, no hedge words, tables over prose.

Extract the **dependency fingerprint** of one thesis: the specific external variables the bull case is actually a bet on. The output is the atom the `portfolio-correlation` workflow fans out to find names that secretly co-depend on the same variable.

## Arguments
`SKILL_ARGS` = a ticker or thesis name. If empty, ask which thesis.

## Read-only
This skill REPORTS analysis; it does not modify vault files (no lock, snapshot, or manifest). To persist a finding, the user asks explicitly ("add this to the [[thesis]]").

## Mental Models gate (MANDATORY — AGENTS.md)
Before analysis, read `[[Mental Models/Generalist - Overview]]` plus any `[[Mental Models/Industry - X]]` / `[[Mental Models/Lens - X]]` the thesis touches (Semiconductors, Automation & AI Readiness, Value Layer Monopoly). Apply the READING PROTOCOL — models are lenses, hunt the single falsifying datapoint. The **Value Layer Monopoly** lens is primary here: a dependency the company *owns* (a layer everything above must traverse) is the inverse of a dependency it is *exposed to*.

## Method  (single source of truth — the `portfolio-correlation` workflow reads this section)
1. **Read the thesis** (`Theses/TICKER - Name.md`) in full; skim its `## Related Research` for supporting evidence. Read `_graph.md` once for cluster peers (graph-primer Mode A — orient, do not skip reads).
2. **Enumerate dependencies in five buckets**, each as a concrete named variable (not a category):
   - **Demand-side**: key customers / end-markets whose spend the revenue rides (name them; note revenue concentration if known).
   - **Supply-side**: critical inputs / suppliers / capacity the COGS or roadmap depends on (e.g. a specific foundry node, a single-source component, HBM allocation).
   - **Technology transition**: the shift the thesis is levered to (e.g. accelerated compute, hybrid bonding, GAA, on-device inference) — and what stalls it.
   - **Macro driver**: the macro variable the bull case needs (AI capex, rates, FX, China access, memory cycle) — kept light here; `macro-exposure` goes deep.
   - **Single points of failure**: the one input/customer/approval whose loss breaks the thesis.
3. **Rate each dependency**: direction (needs it up / down), magnitude (load-bearing / contributory / minor), and **stated vs unstated** (is it named in the thesis, or a hidden assumption?).
4. **Name the 2–3 load-bearing dependencies** — the variables that, if they move against the company, break the thesis regardless of execution. These are the correlation atoms.

## Output (solo run)
A dependency table — columns: **Dependency | Bucket | Direction | Magnitude | Stated? | Note** — followed by a 2–3 sentence **load-bearing summary** naming the variables the thesis truly rests on, and any dependency the company *owns* rather than is exposed to (Value-Layer angle). No filler.

## Workflow reuse
`portfolio-correlation` (`.claude/workflows/portfolio-correlation.js`) fans this `## Method` out across every thesis, read-only, then finds names whose load-bearing dependencies coincide — correlated bets the market prices independently. Keep `## Method` the single source of truth; edits here flow to the workflow automatically.
