---
name: design-partner
description: "Design direction and implementation-ready UI plans. Use before building components, pages, or design systems."
version: 0.1.0
---

# Design Partner

## JTBD (Jobs To Be Done)

### Primary Job
When I know I need a UI but not yet the right direction,
I want a concrete design approach and implementation-ready guidance,
so I can build something distinctive without inventing the visual system under pressure.

### Secondary Jobs
- When a design feels generic or incoherent, I want a stronger direction, so I can reset the work before implementation hardens bad choices.
- When I need to extend a design system or component library, I want structured design decisions, so I can keep the system consistent while moving quickly.

### Job Layers
- Functional: Turn design requirements or vague intent into a clear visual direction, system guidance, and actionable design output.
- Emotional: Reduce the fear of shipping bland, inconsistent, or unbuildable design decisions.
- Social: Helps the user look intentional and credible to teammates, stakeholders, and reviewers by articulating a defensible design direction.

### This Skill Is For
- A user starting a new interface and needing design direction before frontend implementation.
- A user with requirements, rough notes, or references who needs a coherent visual and interaction approach.
- A user extending a design system and wanting tokens, components, and patterns to stay deliberate rather than ad hoc.

### This Skill Is NOT For
- A user who already has a concrete design artifact and wants to know whether it is good enough or ready to ship; use `ui-critic` first.
- A user looking for a pure code architecture plan with no design-direction problem; use the domain planner instead.

### Paired With
- `ui-critic`: After a current-state design exists, use it to diagnose what is actually failing before redesigning.
- Domain planners such as `react-planner`: After the design direction is set, use them to turn the design into domain-specific implementation architecture.

### Structured Handoff to web-design-planner
When design-partner output will feed into web-design-planner, produce a `### Design Direction Handoff` section with:
- **Visual Thesis**: One sentence — mood, material, energy (e.g., "Warm editorial confidence with generous whitespace and serif authority")
- **Typography Rationale**: Font pairing + why (e.g., "DM Serif Display + IBM Plex Mono — editorial credibility with technical precision")
- **Color Strategy**: Named palette with semantic meaning (e.g., "Ink-and-signal — near-black surfaces, green/amber/red signal system for skill types")
- **Spatial Approach**: Layout philosophy (e.g., "Asymmetric editorial split — heavy left column, light right detail")
- **Anti-Generic Commitments**: What this design will NOT do (e.g., "No card grids, no purple gradients, no Inter font, no symmetrical layouts")
- **Motion Intent**: 0-3 intended motions with triggers and purposes

This handoff format is consumed by web-design-planner's "Design Direction Input" section.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has rough requirements but no clear direction | Design Partner commits to an aesthetic and system direction | A concrete design direction and rationale |
| Has a design system gap or extension need | Design Partner defines tokens, patterns, and component guidance | System-consistent design decisions |
| Has both current-state problems and redesign goals | Route through `ui-critic` first, then use Design Partner | Diagnosis plus a better direction to build from |

### When to Escalate
- If the user’s primary need is evidence-backed critique of an existing artifact, escalate to `ui-critic`.
- If implementation architecture is the unresolved problem after design direction is clear, escalate to the relevant domain planner.

## Overview
Proactive design generation and guidance with design system awareness, anti-generic guardrails, and optional design tool integration (Pencil, Figma).

## External Skill References (No Copy Policy)
Use external skills as references only.

- Canonical reference file: [external-skills-manifest.yaml](references/external-skills-manifest.yaml)
- Routing policy: [skill-routing-map.md](references/skill-routing-map.md)

Rules:
- Do not copy external skill body content into this repository.
- Use manifest IDs/URLs and pinned commit metadata for traceability.
- If a referenced skill is unavailable in runtime, continue with local rubric fallback and state the limitation.

## References
- Shared design principles: [../../../../shared-design-core/.claude/skills/shared-design-core/references/design-principles-rubric.md](../../../../shared-design-core/.claude/skills/shared-design-core/references/design-principles-rubric.md)
- Research-backed workflow: [../../../../shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md](../../../../shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md)

## Research-Backed Design Preflight
Before committing to a visual direction, apply the shared research-backed workflow:
- Build a `Reference Inventory` from project sources, user references, and research-only inspiration sources. Treat Refero Styles, TypeUI, interface-design, Open Design, AG-UI, Stitch, and similar sources as provenance-backed inspiration, never copied prompt bodies or client-ready visual systems.
- Run discovery before pixels: audience, surface, primary job, tone, constraints, success criteria, and non-goals.
- Read DESIGN.md and DESIGN_MEMORY.md when present. Preserve existing token names, rationale, and rejected directions unless the user asks to change them.
- If the artifact is an assistant/agent UI, define visible status, generated UI regions, tool invocation affordances, recovery paths, and trust boundaries before layout advice.
- Use Codex/local verification assumptions for testing and hardening. Do not route benchmark or evaluation work through Anthropic API unless the user explicitly overrides that constraint.

## Workflow
1. Understand the design context: purpose, audience, tone, technical constraints, and differentiation goals.
2. Check for existing design system artifacts (DESIGN.md, design tokens, component library, Figma files, Pencil .pen files).
   - **DESIGN.md inheritance**: If a DESIGN.md exists (check `./DESIGN.md`, `./docs/DESIGN.md`, `./.design/DESIGN.md`), read it and incorporate existing tokens into your direction. Extend the existing design system — do not overwrite it. Your Design Thinking Phase outputs should reference existing DESIGN.md tokens where they align and explicitly justify departures where they don't. Produce a `### Design System Inheritance` subsection in your output mapping your direction recommendations to existing DESIGN.md tokens (which tokens you're keeping, which you're extending, which you're replacing and why).
   - **DESIGN_MEMORY.md awareness**: If a DESIGN_MEMORY.md exists, read prior session decisions to maintain naming and directional continuity.
3. Run the Research-Backed Design Preflight and prepare the `Reference Inventory` and `Design Memory Notes` sections.
4. Load relevant external skills (max 3) from the routing map based on context.
5. If a design tool MCP is available (Pencil, Figma), use it to inspect existing components and design tokens before generating new ones.
6. Apply the Design Thinking Phase:
   - **Purpose**: What problem does this solve? Who is the audience?
   - **Tone**: Commit to a specific aesthetic direction (not generic). Name it explicitly.
   - **Constraints**: Framework, performance budget, a11y requirements, existing system.
   - **Differentiation**: What makes this memorable? What generic pattern are we deliberately avoiding?
7. Generate or advise on the design artifact, following the design principles rubric.
8. If generating code, produce working HTML/CSS/JS or framework components (React, Vue, etc.) that are production-grade, not placeholder.
9. Run a self-check against the Anti-Generic Guardrails before delivering output.

## Design Thinking Phase (Required)
Before generating any visual output, explicitly state:
- **Aesthetic direction**: Name the specific style (e.g., "editorial minimalist", "brutalist data-dense", "warm organic SaaS"). Never proceed with an unnamed/generic direction.
- **Typography choice rationale**: Why these fonts? What do they communicate?
- **Color strategy**: Dominant/accent relationship. CSS variables for consistency.
- **Spatial approach**: Grid strategy, whitespace philosophy, density level.

## Anti-Generic Guardrails
Before delivering, self-check against these traps:
- ❌ Default Inter/Roboto/Arial without justification
- ❌ Purple-to-blue gradient as default accent
- ❌ Perfectly symmetrical card grids with no hierarchy
- ❌ Generic hero section with stock-photo-style placeholder
- ❌ Uniform rounded corners on everything
- ❌ No clear information hierarchy (everything same weight/size)

If any of these are present, revise with intentional alternatives and state what changed.

## Hard Gates
- No design-direction output without Reference Inventory, Design Memory Notes, Source/Provenance Notes, and Critic Handoff.
- No interactive or agentic interface direction without a State Matrix covering relevant interaction, generated UI, tool-running, recovery, and trust-boundary states.
- No departure from DESIGN.md or DESIGN_MEMORY.md without explicit rationale.
- No use of public references as copied prompt bodies, screenshots, branded assets, page structures, or client-ready visual systems.
- No benchmark/evaluation routing through Anthropic API unless the user explicitly overrides that constraint.

## MCP Integration Points (Optional)
When these tools are available, use them:

### Pencil (pencil.dev)
- `batch_design` — create/modify design elements on canvas
- `batch_get` — inspect existing components, search elements
- `get_screenshot` — render previews for verification
- `snapshot_layout` — analyze structure, detect positioning issues
- `get_variables` / `set_variables` — manage design tokens

### Figma MCP (Framelink or similar)
- Read existing Figma files for design specs
- Extract design tokens, spacing, and typography
- Bridge between design intent and code implementation

### Storybook MCP
- Discover existing components in the library
- Check for component documentation gaps
- Suggest story coverage for new components

## Output Format
Output depends on the request type:

### For component generation:
- Working code (HTML/CSS/JS or framework-specific)
- Design rationale (aesthetic direction, token usage, a11y considerations)
- Component API documentation (props, variants, states)
- Reference Inventory, Design Memory Notes, State Matrix, Source/Provenance Notes, and Critic Handoff

### For design system guidance:
- Token recommendations (colors, spacing, typography scale)
- Component architecture advice
- Design-code consistency checks
- Proposed DESIGN_MEMORY.md entry for durable decisions
- Reference Inventory, Source/Provenance Notes, and Critic Handoff

### For wireframes/layouts:
- If Pencil available: .pen file with layout
- If not: Detailed structural description with spatial relationships, or HTML/CSS prototype
- Reference Inventory, Design Memory Notes, relevant State Matrix, Source/Provenance Notes, and Critic Handoff

## Skill Loading Rules
- Default: one aesthetic direction skill + one system/component skill.
- Add a11y skill when any user-facing output is being generated.
- Max loaded external skills per run: 3.
- Prefer higher-priority, active entries in external manifest.
