---
name: web-design-executor
type: executor
description: "Execute web design implementations from web-design-planner specs."
version: 0.1.0
---

# Web Design Executor Skill

## When to Use

**Primary triggers:**
- "generate this page", "build this layout", "implement this design"
- "execute this web design plan", "generate HTML from this spec"
- "create a landing page", "build a responsive page"
- User has a web-design-planner spec and wants HTML/CSS generated
- User describes a page layout and wants production-ready code

---

## Do Not Use When

- You need to **design** a web interface — use `web-design-planner` first
- You need to **review** an implementation — use `web-design-critic`
- You need a **React/Vue/Svelte component** — this produces vanilla HTML/CSS
- You need a **dashboard** — use `dashboard-executor`
- You need a **data visualization** — use `dataviz-executor`
- You need an **infographic** — use `infographic-executor`

---

## Resolution Paths

| Situation | Route |
|-----------|-------|
| Have a web-design-planner spec, need HTML | This skill |
| Need to design the interface first | Use `web-design-planner`, then come back |
| Have an implementation, need review | Use `web-design-critic` |
| Need a React component | Use `react-planner` → implement manually |
| Need a dashboard | Use `dashboard-executor` |

---

## What You Get

- **Production-ready HTML/CSS** with semantic elements and modern CSS (Grid, Flexbox, custom properties)
- **Design tokens as CSS custom properties** for colors, typography, spacing, shadows, radii
- **Mobile-first responsive** with `min-width` media queries at all specified breakpoints
- **All interaction states** implemented: hover, focus-visible, active, disabled, loading, error, empty
- **Accessibility**: skip link, ARIA attributes, visible focus styles, semantic landmarks
- **Deviation log** and **critic handoff command**

---

## Shared Research Reference

Apply the shared research-backed workflow while executing:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## External Evidence References

- `web-design-guidelines` (vercel-labs/agent-skills): current web interface guideline reference. Use as design provenance, not as a replacement for Zivtech or client design constraints.
- `ui-screenshots`, `image-annotations`, `pr-screenshots`, `screen-recording` (github/awesome-copilot): evidence patterns for before/after screenshots, cropped annotations, and short interaction recordings.

## Research-Backed Execution Preflight

Before writing HTML/CSS:
- Read the web-design-planner spec when present, including `Reference Inventory`, `Design Memory Notes`, `State Matrix`, and `Source/Provenance Notes`.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Use existing tokens and semantic names as the default; log any intentional departures.
- If the input came directly from the user, create a compact reference inventory and state matrix before generating code.
- If the interface includes assistant or agent workflows, implement visible status, generated UI regions, tool invocation affordances, user confirmation points, cancellation/retry, error recovery, and trust boundaries.
- Translate public references into local design principles only. Do not copy public reference screenshots, branded assets, prompt bodies, or page structures.
- Use local verification by default: browser rendering, viewport checks, focus order, contrast, overflow, and interaction states. Do not use Anthropic API for benchmark execution unless explicitly overridden by the user.

---

## Key Implementation Guarantees

| Guarantee | Enforcement |
|-----------|-------------|
| No hardcoded colors | All colors via CSS custom properties |
| Mobile-first responsive | `min-width` media queries only |
| Visible focus styles | `:focus-visible` on all interactive elements |
| Font sizes in rem | Never px for text |
| Semantic HTML | `nav`, `main`, `section`, `article`, `aside`, `header`, `footer` |
| Skip link | Always included |
| No `outline: none` | Without replacement focus style |
| Memory continuity | DESIGN.md/DESIGN_MEMORY.md tokens and decisions preserved or deviations logged |
| Evidence handoff | Reference inventory, state matrix, provenance notes, and critic handoff included |

---

## Execution Protocol

1. Parameter Extraction
- Identify page type, audience, target breakpoints, content inventory, visual direction, state matrix, design tokens, and provenance requirements.
2. System Continuity
- Map DESIGN.md tokens and DESIGN_MEMORY.md decisions into CSS custom properties, component choices, and layout rationale.
3. Implementation
- Generate semantic HTML, tokenized CSS, responsive layouts, interaction states, and accessibility affordances.
4. Verification
- Run or specify local browser checks for 375px, 768px, 1280px, and 1920px; keyboard navigation; focus visibility; overflow; contrast; and empty/error/loading states.
- Capture or request a compact visual evidence packet: viewport screenshots, before/after screenshots when revising an existing surface, annotated crops for material defects fixed, and a short recording only when motion/interaction behavior matters.
- **Accessibility fix loop (when browser tooling is available):** Run axe-core at 1280px. If critical or serious violations are found, fix them and re-run until zero critical/serious remain. Log each violation found and fix applied. If browser tooling is unavailable, note the limitation explicitly in Verification Notes.
5. Handoff
- Produce deviation log, proposed DESIGN_MEMORY.md entry for new durable decisions, and `/web-design-critic` handoff.

---

## Companion Skills

- **web-design-planner** (upstream): Designs the interface architecture
- **web-design-critic** (downstream): Reviews the implementation for responsive, interaction, accessibility fidelity

---

## Hard Gates

- No generation without design-token mapping or an explicit deviation explaining why tokens are unavailable
- No generation without Reference Inventory, State Matrix, Source/Provenance Notes, and Deviation Log
- No agentic interface without visible status, generated UI region, user control/recovery, and trust boundary affordances
- No delivery without local browser verification results or an explicit limitation statement
- No public reference copying
- No copied public screenshots, third-party brand systems, or platform-specific PR image hosting workarounds in generated deliverables

---

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

## meta-router Registry Note

Listed under the **Executors** table.
Trigger signals: `generate page, build layout, implement design, create landing page, generate HTML CSS, execute web design, build responsive page`
