---
name: viz-lab
description: "Build best-in-class, real-data-grounded visualizations of YURI's own systems — energy/ΔU surfaces, quantum Q-spheres, circuitry graphs (2D edge-bundling + 3D die), telemetry cockpits, embedding atlases. Use when the task is to visualize, depict, render, or make interactive any YURI math / quantum / graph / telemetry data, build a 3D / WebGL / three.js / react-three-fiber or D3 visualization, turn a flat view into 3D, or prototype a viz before wiring it into the app. Triggers: visualize, viz, visualization, 3D, WebGL, three.js, D3, surface, graph, chart, dashboard, Q-sphere, edge bundling, make this 3D."
scope: harness
invocation: ability
---

# YURI Viz-Lab

Best-tool-per-depiction visualization of YURI's own math, quantum, graph, and telemetry layers. **Quality over friction**: pick the genuinely strongest tool for each depiction (Python / Rust / JS — whatever wins), and ground every visual in YURI's **real** code/data, never a lookalike.

## Method (the loop that produced the `demos/`)

1. **Ground in real data** — never synthesize a stand-in. Write a generator under `demos/build/*.mjs` that imports the real YURI module (e.g. `computeU` from `_SYSTEM/Scripts/math/yuri-energy.mjs`, the exports of `_SYSTEM/Scripts/quantum-hypothesis-tracker.mjs`) or reads the real artifact (e.g. `02_RESOURCES/RESEARCH/yuri-die-graph.json`), and emit `demos/data/<x>.js` as a `window.<GLOBAL> = …` script. The visual then provably reflects the live system.
2. **Best tool per depiction** — map the depiction to its strongest tool (table below); do not default to the readiest one. Stack-agnostic.
3. **Standalone-first, `file://`-safe** — one self-contained `.html` that opens by double-click. CDN module imports (CORS-enabled) + local data loaded as a `<script src>` global. NEVER a relative ES-module import or `fetch()` — both are blocked on `file://`.
4. **Adversarially verify** — `node --check` the extracted script; confirm every `getElementById` id resolves; prove **fidelity** (recompute a data cell against the real function; confirm a real invariant, e.g. the quantum order-effect P(A→B) ≠ P(B→A) with qq ≈ 0); then an independent render-review before claiming it works. First-run success is a hypothesis.
5. **Port, don't rewrite** — the standalone renderer ports into the Vite + react-three-fiber app (`_SYSTEM/src/scenes/`); the generator re-points from snapshot to live stream.

## Depiction → best tool

| YURI object | Depiction | Best tool |
|---|---|---|
| energy gate ΔU / U | 3D surface · isosurface · ridgeline · particle field | three.js (+ bloom) / VTK.js |
| quantum hypothesis sim | Q-sphere · Wigner · Hinton (coupling) | three.js (embed the real tracker) / Qiskit ref |
| circuitry / code graph | hierarchical edge bundling · 3D layered die · GPU force | D3 (HEB) · three.js (strata) · cosmos.gl (scale) |
| alpha factors | correlation clustermap · embedding atlas | seaborn / ECharts · regl-scatterplot + UMAP |
| prediction ledger / decision-sim | calibration diagram · quantile dotplot · fan cone | D3 / Vega · ArviZ |
| lane telemetry / tokens | uPlot + LTTB · horizon · streaming pivot | uPlot · FINOS Perspective |

Default JS stack (drops into the existing three.js@0.173 + R3F + Vite): **three.js / R3F** for 3D, **D3** for graphs/bundling, **uPlot** for time-series, **ECharts-GL / regl / Sigma** at scale.

## Reference assets (read first)

- Landscape survey — 12 families, every technique mapped to a YURI domain, with sources: `02_RESOURCES/RESEARCH/visualization-landscape-2026-06-16.md` (`ai search "visualization"`).
- Proven demos: `demos/vol-surface.html`, `demos/energy-surface.html`, `demos/qsphere.html`, `demos/circuitry-heb.html`, `demos/circuitry-die-3d.html`; generators `demos/build/gen-*.mjs`.

## Rules (failure-anchored)

- **`file://`-safe loading only**: CDN module imports + local-data globals; no relative module imports / `fetch()`. <!-- @anchor: v1 | failure: file:// CORS blocks relative ES-module imports + fetch (demos session 2026-06-16) | regression: the node --check + open-in-browser step of this skill -->
- **Real data, not lookalikes; quality over friction**: pick the BEST tool and the MOST COMPLETE real source, not the readiest. <!-- @anchor: v1 | failure: grabbed the 126-node projected graph (least-friction) when the owner wanted the 242-node die/merge — "best results, not least friction" (Marcel 2026-06-16) | regression: the ground-in-real-data + completeness check in this skill -->
- **Verify fidelity, not just syntax**: recompute a real value, confirm a real invariant, independent render-review before "it works".
- **No HUD/Kagami design tokens** — style with self-contained purpose-built CSS (standing owner preference).

## Session Notes

### 2026-06-16
- session: 155m | peak ctx: 0% | compacts: 0
- tools: Bash×338, Read×113, Edit×60, Write×21, Agent×14, TodoWrite×5, AskUserQuestion×3, ToolSearch×2, WebSearch×2
- corrections: none
- errors: none
