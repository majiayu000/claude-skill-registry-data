---
name: architecture-treemap
description: "Render a self-contained HTML treemap of a codebase's architectural model: components sized by LOC, classified core/seam/removable, with static and audit-asserted coupling edges. Use to VISUALISE an architecture audit — it displays a model, it does not produce one. For Mermaid diagrams use /diagram; for the methodology use architecture-first-dev."
license: MIT
---

# Architecture Treemap

**Status: experimental.** Review for pruning by 2026-11-20.

## Overview

The architecture-treemap stack turns a codebase into a single self-contained HTML treemap: logical components sized by lines of code, coloured by classification (core / seam / removable), annotated with deterministic metric badges (LOC, fan-in/out, cyclomatic complexity, 90-day churn, test ratio), and wired with coupling edges that render solid when statically detected and dashed when asserted by architectural judgment. The artifact opens as a `file://` with no server — biologists and architects email it around.

The headline differentiator: this is a **semi-deterministic sandwich**. The bookends (extraction, rendering) are pure deterministic functions; the middle (audit, synthesis) is judgment. The metric badges are the trust scaffold — they let the reader see the deterministic substrate behind every judgment call.

**When to use this skill:**
- Visualising a retrospective architecture audit after a smoke/demo/in-vivo pass surfaced cross-cutting findings.
- Defending an OSS-core boundary before a pivot (open-source release, plugin extraction).
- A portfolio has accumulated 5+ features and the cross-feature coupling is no longer trackable by reading synthesis docs.

**When NOT to use this skill:**
- Scoping a new feature → use `/map` (the treemap is retrospective, not prospective).
- Rendering one feature's design diagrams → use `/diagram` (Mermaid from design artifacts).
- Producing the architectural model itself → this skill only renders; run `/components-extract` + `/synthesize-audit` first.

---

## Decision Tree

```
Want to see the shape of a codebase's architecture?
│
├─ I want to RENDER a model I already have (components.json)
│     → /architecture-treemap <path>  (this skill)
│
├─ I have code but NO model yet
│     ├─ Need the deterministic substrate (files, static edges, metrics)?
│     │     → /components-extract <repo>        (then synthesize)
│     ├─ Have an empirical anchor (smoke findings, regression, pre-pivot)?
│     │     → /audit-slice <concerns>  →  /synthesize-audit  →  /architecture-treemap
│     └─ No anchor, just scoping a feature?
│           → /map <slug>   (NOT this stack — far cheaper)
│
└─ I want one feature's design diagrams, not a whole-repo audit
      → /diagram <slug>     (Mermaid collector)
```

---

## The four-stage pipeline

Deterministic bookends, judgment middle:

| Stage | Command | Kind | Produces |
|---|---|---|---|
| 1 | `/components-extract <repo>` | **deterministic** | substrate components.json: `physical_components`, static direct-call `edges` (`evidence_class:"static"`), per-component `metrics`, `git_sha`, `extractor` block. Emits `logical_components: []` (empty) — it cannot author judgment. |
| 2 | `/audit-slice <concerns>` | **judgment** | N concern slices: findings (E-NN), connascence tags, decoupling proposals (R-NN). User-authored trigger only; off the autopilot. |
| 3 | `/synthesize-audit` | **judgment** | the FULL components.json: groups files into `logical_components`, assigns `classification`, adds audit-asserted edges, writes `prune_candidates` + `core_boundary`. Carries the substrate's static facts through unchanged. Validates against the schema. |
| 4 | `/architecture-treemap <path>` | **deterministic** | self-contained `treemap.html` (D3 inlined, no CDN). A pure function of the manifest; validates first and refuses to render on schema failure. |

Stages 1 and 4 are reproducible: same input → same output (modulo the force-graph seed, which is pinned in the URL hash). Stages 2 and 3 are where humans and the slice/synth agents do the irreducible architectural assessment.

---

## Quick Start

Render the golden fixture — the fastest path to a visible result:

```bash
# from the toolkit root
python skills/architecture-treemap/scripts/render_treemap.py \
    skills/architecture-treemap/references/example/components.json \
    --output /tmp/treemap.html

# open it (no server needed — self-contained file://)
xdg-open /tmp/treemap.html   # or: open /tmp/treemap.html on macOS
```

The fixture is a 4-component toy (api-router, store, plugin-loader, legacy-export) that exercises every feature: a core path, a seam, a removable component, static + audit-asserted edges, metric badges, a prune candidate, and a core boundary.

**On a real repo, run the full pipeline:**

```bash
# 1. deterministic substrate
python skills/architecture-treemap/scripts/extract_components.py <repo-root> \
    --out audit/components.json --since-days 90 --lang python

# 2-3. judgment layer (slash commands — user-authored concerns)
#   /audit-slice <concern...>
#   /synthesize-audit        → fills logical_components, classifications, judgment edges

# 4. deterministic render
python skills/architecture-treemap/scripts/render_treemap.py audit/components.json
#   → writes audit/treemap.html (default: alongside the input)
```

**Verify it worked:**

```bash
# the renderer validates first and refuses to render invalid input;
# a standalone validation check:
python skills/architecture-treemap/scripts/validate_components.py \
    skills/architecture-treemap/references/example/components.json --strict
# expect: exit 0, "valid"
test -s /tmp/treemap.html && echo "non-empty HTML written"
```

---

## The treemap visualises a model; it does not produce one (memo Q-2.5)

This is the central trade-off, and the most common misunderstanding. **The deterministic ground truth is the substrate, not the architecture.** Extraction gives you physical files, static call edges, and complexity metrics — facts an AST and `git log` can prove. Everything that makes the treemap *useful* as an architecture view — the logical grouping, the core/seam/removable classification, the smells, the background-knowledge edges, the prune verdicts, the core boundary — is NOT statically detectable. It is architectural judgment, authored by humans and the slice/synth agents.

Consequences to internalise:
- A treemap is only as good as its `/synthesize-audit` run. Garbage judgment in, confident-looking treemap out. The metric badges exist precisely so the reader can sanity-check the judgment against the substrate.
- A component with no slice and no finding renders a **"judgement only"** pill, not a fabricated confidence score. Do not read more certainty into a tile than its provenance supports.
- **Structural proposes; you dispose.** Core/seam are rendered as PROVISIONAL, metric-anchored hypotheses that show the metrics driving them; seam is always a *candidate* ("confirm intent"), never an asserted detection. **Removable is never auto-classified** — a structural/LLM pass cannot see the product intent that makes code "unused", so a removable verdict with no grounding slice renders "requires your judgment — run /audit-slice". Every classification and edge carries an `epistemic_source` chip (measured / metric-anchored / requires-your-intent) so you can see how much each claim depends on information not in the code.
- **An unowned physical file renders NEUTRAL grey, never core.** A file with no `logical_owners` has not been grounded by any synthesis judgment; it is `unclassified`, not load-bearing. (The non-source inventory filter removes most scaffolding so legitimate unowned files stay visible and honest.)
- Re-running extraction produces a NEW snapshot (git-SHA-stamped, datestamped); it never mutates an old one. The treemap of last quarter's SHA stays valid as a historical record.
- The treemap is a *communication* artifact, not a *decision* artifact. The decision lives in the `synthesis-vN.md` decision menu; the treemap makes that decision legible to someone who was not in the room.

---

## Verification Checklist

After rendering, confirm:

- [ ] **Renders the golden fixture:** `bash skills/architecture-treemap/checks/golden_render.sh` exits 0.
- [ ] **Validation gate fires:** feeding an invalid manifest to `render_treemap.py` prints schema errors and refuses to render (no half-rendered HTML).
- [ ] **Self-contained:** the output `.html` opens as `file://` with no network — no external CDN fetch at view time.
- [ ] **Substrate visible:** metric badges appear on tiles that carry a `metrics` block; tiles without findings show the "judgement only" pill.
- [ ] **Edge evidence honoured:** static edges render solid, audit-asserted edges render dashed.

For automated verification: `bash skills/architecture-treemap/checks/golden_render.sh`

---

## Common Pitfalls

### Pitfall: treating the treemap as the source of truth

- **Symptom:** a stakeholder cites a "removable" tile as fact and deletes code; it breaks.
- **Cause:** classification is judgment from `/synthesize-audit`, not a static fact. The treemap renders the judgment faithfully — including its mistakes.
- **Fix:** read the `core_boundary.rationale` and the slice findings (E-NN) behind the classification before acting. The decision menu in `synthesis-vN.md` is the artifact to grill.

### Pitfall: running the stack to scope a new feature

- **Symptom:** ~1M tokens spent and the slices read like a `/map` with extra steps.
- **Cause:** no empirical anchor. With no smoke findings or regression to chase, concern-traversal degenerates into "enumerate everything" — which `/map` already does, ~20× cheaper.
- **Fix:** use `/map` for prospective feature work. Reserve this stack for retrospective audits with an anchor.

### Pitfall: synthesising without the extractor substrate

- **Symptom:** every tile shows "judgement only"; no metric badges; no trust scaffold.
- **Cause:** `/synthesize-audit` ran on slices alone, with no `/components-extract` output to merge.
- **Fix:** run `/components-extract` first; pass its `components.json` to `/synthesize-audit` so static edges and metrics carry through.

### Pitfall: hand-editing a rendered treemap.html

- **Symptom:** edits vanish on the next render.
- **Cause:** the renderer is a pure function of `components.json`; the HTML is disposable output.
- **Fix:** edit the `components.json` (or re-run `/synthesize-audit`) and re-render.

---

## Robust authoring checklist (for the judgment layer)

`/synthesize-audit` (and the slicer feeding it) must satisfy these before a
manifest is done. Most fail silently — the manifest still validates and renders
— so they are guarded by discipline, not by the tooling (item 1 is the exception:
it is enforced by the validator's orphan gate under `--strict`):

1. **No orphan logical nodes.** Structural import edges between logical
   components are derived deterministically by `rollup_logical_edges.py` (run in
   `/synthesize-audit` Phase 2.6), not hand-authored. The author's job is to add
   judgment edges (shared-state, background-knowledge, forward contracts) where
   slices found coupling invisible to static imports, and to justify any node the
   rollup cannot connect as a leaf (`classification: removable` or `leaf: true`).
   The validator's non-leaf-orphan check under `--strict` is the enforcing gate.
2. **Ground every edge in a real citation** (file:line + the exact import/call,
   aliases included). `evidence_class: static` only for a real detectable
   import/call; `audit-asserted` for runtime contracts / background knowledge.
3. **Cross-cutting nodes get represented** — author the fan-in edges into config
   / shared kernels (the renderer dims high-fan-in sinks automatically); never
   leave a shared dependency floating.
4. **The tool must not audit its own output** — generated snapshots under
   `architecture-audit/` are excluded by the extractor by default.
5. **Metrics bias attention, never deliver verdicts** — read `refactor_pressure`
   / churn / fan-in to decide where to look first; never fabricate or override
   a metric.

The full version is the [robust authoring checklist](../architecture-first-dev/references/architecture-treemap-audit.md#robust-authoring-checklist).

## Resources

- **Schema (the binding data contract):** `skills/architecture-treemap/components.schema.json`
- **Metric model (single source of truth):** `skills/architecture-treemap/scripts/metric_registry.py` — the descriptor registry the extractor, schema, and renderer all derive from. Add a metric by registering one descriptor here. Ships `loc`, `fan_in/out`, `cyclomatic`, `churn_90d`, `test_ratio`, derived `instability` (`fan_out/(fan_in+fan_out)`) and `refactor_pressure` (+ a degraded `refactor_pressure_loc_proxy` when radon is absent).
- **Pedagogy model (single source of truth):** `skills/architecture-treemap/scripts/pedagogy_registry.py` — the sibling registry for classification / edge-type / evidence-class explainers, the `epistemic_source` legend (measured / metric-anchored / requires-your-intent), the direction encoding, per-metric explainers, and the concept glossary. Serialised into the manifest `pedagogy` block; the renderer draws every `(?)` affordance and the glossary from it. There is NO hardcoded help in the JS or HTML.
- **Metrics-architecture decision note (ADR):** `skills/architecture-treemap/references/metrics-architecture.md`
- **Golden fixture:** `skills/architecture-treemap/references/example/components.json`
- **Edge-type reference:** `skills/architecture-treemap/references/edge-types.md`
- **Classification rationale:** `skills/architecture-treemap/references/classification-rationale.md`
- **D3:** https://d3js.org/
- **Connascence (Page-Jones taxonomy):** Meilir Page-Jones, *What Every Programmer Should Know About Object-Oriented Design*.

---

## When not to use

- Do not use to PRODUCE an architectural model. It only renders an existing components.json — run /components-extract then /synthesize-audit first.
- Do not use for per-feature design diagrams. Use /diagram (collects Mermaid from design artifacts) instead.
- Do not use as a routine per-feature tool. A full audit costs roughly 1M tokens; it is a quarterly retrospective instrument, not a per-commit one.

---

## See also

- `architecture-first-dev` — Sibling; the design-before-code methodology and per-feature pipeline (this stack is the retrospective audit arm of the same harness)
