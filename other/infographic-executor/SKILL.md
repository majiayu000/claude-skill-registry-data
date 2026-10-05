---
name: infographic-executor
type: executor
description: "Execute infographic implementations — data visualization, layout, and production."
version: 0.1.0
---

# Infographic Executor Skill

## When to Use

**Primary triggers:**
- "create an infographic", "generate a fact sheet", "build a visual summary"
- "make a one-pager", "create a process diagram", "generate a comparison infographic"
- "execute this graphic design plan as an infographic"
- User has a graphic-design-planner spec and wants an SVG infographic generated
- User has data/content and wants a visual one-pager

---

## Do Not Use When

- You need to **design** visual direction — use `graphic-design-planner` first
- You need to **review** a graphic — use `graphic-design-critic`
- You need an **interactive chart** — use `dataviz-executor`
- You need a **dashboard** — use `dashboard-executor`
- You need a **slide deck** — use `marp-executor`
- You need a **web page layout** — use `web-design-executor`
- You need **raster/photographic** output — this produces vector SVG only

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have a graphic-design-planner spec, need infographic | This skill |
| Need to design visual direction first | Use `graphic-design-planner`, then come back |
| Have an infographic, need design review | Use `graphic-design-critic` |
| Need an interactive data chart | Use `dataviz-executor` |
| Need a multi-chart dashboard | Use `dashboard-executor` |

---

## Supported Infographic Types

| Type | Use Case |
|------|----------|
| Statistical | Data comparison, survey results, KPI summary |
| Process/Timeline | Workflows, project phases, history |
| Comparison | Product vs product, before/after, options |
| Hierarchical | Org charts, taxonomy, decision trees |
| Geographic | Regional data, location-based stats |
| List/Checklist | Tips, best practices, key takeaways |
| Fact Sheet/One-Pager | Executive summary, quick reference |

---

## What You Get

- **Self-contained HTML+SVG file** — everything is inline vector graphics
- **Brand-aware**: colors from spec palette applied throughout
- **Visual hierarchy**: most important data gets largest visual treatment
- **Accessible**: all text as SVG `<text>` (screen reader compatible), `aria-label` on SVG
- **Print-ready**: `@media print` stylesheet included
- **Correct data scaling**: proportional shapes scale by area, not radius
- **Source citations**: every data claim has provenance
- **Deviation log** and **critic handoff command**

---

## Shared Research Reference

Apply the shared research-backed workflow while executing:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Research-Backed Execution Preflight

Before generating an infographic:
- Read the graphic-design-planner spec when present, including `Reference Inventory`, `Design Memory Notes`, hierarchy plan, asset specs, and `Source/Provenance Notes`.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Preserve token names, semantic roles, visual rationale, and rejected directions unless the user requests a change.
- If the input came directly from the user, create a compact reference inventory, source/citation inventory, data hierarchy, and production State Matrix before generating SVG.
- Translate public references into local design principles only. Do not copy public reference screenshots, branded assets, prompt bodies, layouts, or illustration styles.
- Use local verification by default: dimensions, safe zones, contrast, legibility, text overflow, print rendering, and area-correct scaling checks. Do not use Anthropic API for benchmark execution unless explicitly overridden by the user.

## Execution Protocol

1. Parameter Extraction
- Identify infographic type, audience, content inventory, data/source citations, format, visual direction, token source, and missing evidence.
2. System Continuity
- Map DESIGN.md tokens and DESIGN_MEMORY.md decisions into SVG/CSS variables and composition choices.
3. Data And Content Integrity
- Validate proportional encodings, source citations, hierarchy, and text length before layout.
4. Asset Generation
- Generate self-contained HTML+SVG with accessible labels, tokenized styles, print styles, and responsive framing when embedded on web.
5. Verification And Handoff
- Check contrast, overflow, safe zones, area scaling, and print preview; provide deviation log, proposed DESIGN_MEMORY.md entry, and `/graphic-design-critic` handoff.

## Hard Gates

- No infographic without source/citation inventory for every data claim
- No infographic without Reference Inventory, production State Matrix, Source/Provenance Notes, and Design Memory Notes
- No proportional shape encoding that scales radius instead of area
- No text below WCAG AA contrast minimum
- No text overflow or clipping in fixed containers
- No delivery without local verification results or an explicit limitation statement
- No public reference copying

## Required Output Contract

Use these top-level headings exactly:
- `## Parameter Extraction`
- `## Reference Inventory`
- `## Generated Files`
- `## Implementation Preview`
- `## Verification Notes`
- `## Design Memory Notes`
- `## Deviation Log`
- `## Execution Summary`

---

## Companion Skills

- **graphic-design-planner** (upstream): Designs visual direction, hierarchy, asset specs
- **graphic-design-critic** (downstream): Reviews for hierarchy, legibility, brand consistency, production readiness

---

## meta-router Registry Note

Listed under the **Executors** table.
Trigger signals: `create infographic, generate fact sheet, build visual summary, make one-pager, create process diagram, generate comparison infographic, visual explainer, data summary graphic`
