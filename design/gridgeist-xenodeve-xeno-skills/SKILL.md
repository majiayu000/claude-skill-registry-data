---
name: gridgeist
description: Use when creating, redesigning, or reviewing web interfaces that need product-specific structure, clear hierarchy, responsive composition, accessible interaction, or relief from generic AI-generated SaaS aesthetics. Adapt grid, typography, imagery, motion, and product evidence to the established brand—including technical, editorial, image-led, warm, playful, and utilitarian directions—across React, Next.js, Tailwind CSS, HTML/CSS, landing pages, dashboards, documentation, portfolios, and interactive tools.
---

# Gridgeist

## Overview

Craft distinctive, product-native interfaces from audience, content, behavior, and brand intent. Use grid as structural logic; make it visible only when it serves the product.

## Select a mode

| Intent and authorization | Mode | Start with |
|---|---|---|
| Build an interface without an existing design | Create | Audience, primary task, content, and evidence |
| Change an existing interface with permission to edit | Redesign | Preserved behavior, brand signals, and state inventory |
| Diagnose without changing files | Review | Prioritized findings grounded in rendered evidence |

Let user authorization determine whether files change. Permission to redesign does not authorize choosing among materially different visual theses. Derive direction from explicit user intent or established brand evidence; audience, task, product category, and content may inform hierarchy but do not alone confirm a visual thesis. Use the alignment gate below whenever thesis-level ambiguity remains.

## Workflow

1. **Inspect** — Understand the audience, primary tasks, brand signals, content, product evidence, routes, components, tokens, and rendered desktop/mobile UI. Inspect existing design-system sources, including `DESIGN.md` when present, and reconcile them with the implementation and rendered evidence rather than assuming they agree. Inventory important interaction states and constraints. Do not invent customers, metrics, outcomes, research, or compliance.
   - **Align direction before editing** — Classify the direction as **user-confirmed**, **brand-derived**, or **provisional**. Treat a coherent user direction as confirmed even when it leaves implementation choices open; variations within the same thesis are not material ambiguity. Classify a direction as brand-derived only when existing visual implementation, assets, documented rules, or repeated brand conventions converge on one thesis; product subject matter or copy alone is not enough. When a broad Create or Redesign still supports materially different theses that would change core brand expression, hierarchy, imagery, color, or motion, offer two or three evidence-grounded directions with trade-offs and a recommendation, then ask the user to choose or authorize the recommendation. While the direction is provisional, do not define the replacement system or edit implementation files. Proceed without redundant questions when intent or coherent brand evidence is clear. Do not block Review or narrow repairs; label an unconfirmed Review replacement direction provisional.
   - **Hard stop for provisional broad work** — A provisional direction is not an implementable direction. End the turn after the options, trade-offs, recommendation, and alignment question. Do not set a thesis, read the system contract, create tokens, edit files, start implementation, or verify a redesign until the user selects a direction or explicitly authorizes the recommendation.
2. **Set a thesis** — Write one governing sentence combining audience, primary task, structural logic, brand expression, and a product-native motif. Read [design-language.md](references/design-language.md) before choosing the direction, especially for image-led, warm, playful, or otherwise nontechnical brands.
3. **Define the system** — Read [system-contract.md](references/system-contract.md) before making new or changed system decisions. Establish the relevant color, typography, layout, spacing, shape, surface, component, state, media, motion, and responsive rules as one compact contract. Decide whether the grid should be visible, quiet, or invisible. Reuse semantic tokens and existing primitives; keep narrow repairs proportional and do not create a persistent design artifact unless authorized.
4. **Compose** — Build hierarchy before detail. Make one area dominant, align related content, vary sections within shared logic, and let the most authentic material—product UI, data, prose, imagery, artwork, code, or the primary tool—carry visual weight.
5. **Implement** — Preserve required behavior and states. Follow repository conventions, semantic HTML, keyboard and touch behavior, and existing primitives. Recompose mobile layouts rather than shrinking desktop. Avoid dependencies for simple CSS effects.
6. **Verify** — Use [review-checklist.md](references/review-checklist.md). Render representative widths and exercise primary flows, states, focus behavior, reduced motion, overflow, and dynamic content. Fix clarity and hierarchy before polish. Report what was observed separately from what remains inferred or untested.

For interactive products, inventory at least default, loading, empty, error, success, disabled, and destructive states when applicable. Preserve privacy, safety, data, and platform constraints as product behavior, not optional polish.

## Coordinate companions

- Keep Gridgeist as the sole owner of product and visual direction. Do not automatically combine it with another broad frontend-design or art-direction skill. If the user explicitly requests both, establish one direction owner before editing instead of silently blending their defaults.
- **Explicit overlap gate** — When the user requests Gridgeist plus another broad visual-design skill, state the overlap and recommend one direction owner before selecting a thesis or editing; use Gridgeist by default for product-native, brand-adaptive work. Do not silently ignore the requested companion or run both visual theses. After ownership is clear, use only non-conflicting implementation or verification help from the other skill unless the user chooses it as owner.
- Use context capabilities during Inspect, asset generation after the thesis, technical audits after implementation, and browser automation during Verify.
- Treat companions as optional. Do not block work or add dependencies when they are unavailable.

## Anti-slop contract

- Use one thesis and one coherent system.
- Preserve or deliberately evolve the brand instead of importing a house aesthetic.
- Build hierarchy through scale, position, density, rhythm, and contrast.
- Give grid visibility, borders, radii, shadows, gradients, and motion defined roles.
- Prefer authentic product evidence; label sample or fictional material and never fabricate proof.
- Give sections or workflows distinct compositions within shared structural logic.

Repeated rounded cards, centered hero copy, gradient blobs, excessive pills, uniform sections, arbitrary icon boxes, generic claims, and technical chrome on nontechnical brands are diagnostic signals, not automatic violations. Replace weak structure with a stronger product-specific idea.

## Decision reference

| Dimension | Decide from |
|---|---|
| Structure | Information order, task flow, shared alignments, and the brand's degree of regularity |
| Type | Brand voice, reading needs, and role hierarchy; reserve mono for genuinely technical content |
| Visual lead | Product UI, data, prose, imagery, artwork, code, or a primary interactive surface |
| Shape and surface | Brand geometry, containment, adjacency, state, and interaction—not fashion |
| Color | Existing brand palette and semantic roles; do not assume neutral plus one accent |
| Components | Product tasks, shared anatomy, variants, density, state behavior, and repository conventions |
| Motion | Causality, feedback, spatial change, and tone, with reduced-motion support |
| Responsive | Priority, order, density, input method, and content behavior at each range |

## Output contract

For user-confirmed or brand-derived Create or Redesign, provide **Direction** with the thesis and preserved constraints, complete responsive **Implementation**, and **Verification** evidence naming observed viewports, flows, states, and remaining gaps. When system decisions materially change, identify the relevant contract or where its tokens and component rules are implemented. For provisional broad Create or Redesign, output only the alignment options, trade-offs, recommendation, and question; do not include **Implementation** or redesign **Verification** claims. For Review, make no edits and provide a one-line **Verdict**, prioritized findings with location, evidence, impact, and the smallest coherent correction, plus one replacement **Direction**. Never claim verification without observation.

## Common mistakes

| Mistake | Correction |
|---|---|
| Treating Gridgeist as a visible-grid preset | Use grid as underlying logic and expose it only when the brand benefits |
| Copying a reference literally | Extract principles and preserve the user's identity and content |
| Styling before understanding behavior | Inventory tasks, constraints, and states before composing |
| Making minimalism empty | Add useful evidence and controlled density |
| Styling components one at a time | Define shared anatomy, tokens, variants, and states before polishing instances |
| Improving the default state only | Design loading, empty, error, success, disabled, and destructive paths |
| Stacking desktop UI on mobile | Redesign order, density, navigation, media, and interaction |
| Reporting subjective taste alone | Tie findings to comprehension, usability, consistency, brand, or accessibility |
| Reporting automated checks as user evidence | Separate technical verification from usability, safety, and research claims |

## Contrasting examples

> Redesign dense API documentation with a visible information grid, precise code states, and verified mobile navigation.

> Redesign a warm image-led portfolio with an invisible alignment system, expressive type, artwork-led pacing, and accessible project narratives.
