---
name: design-token-critic
type: critic
disallowedTools: Write, Edit
description: "Review design token systems for naming consistency, value coverage, and cross-platform compatibility."
version: 0.1.0
---

# Design Token Critic Skill

## JTBD (Jobs To Be Done)

### Primary Job
When my design token system has grown organically and I'm not sure if it's consistent, well-named, or complete,
I want an evidence-backed audit of token architecture, math relationships, and coverage,
so I can fix structural token problems before they propagate across components and platforms.

### Secondary Jobs
- When I need to verify that CSS custom properties, Figma variables, and Tailwind config are aligned, I want a cross-platform parity check, so I can catch drift before it causes visual inconsistencies.
- When I suspect my color system has contrast problems, I want every color pairing audited against WCAG AA/AAA, so I can fix compliance gaps systematically rather than one-off.
- When a web-design-executor or infographic-executor generates code with design tokens, I want the token system reviewed before more surfaces consume it, so token debt doesn't compound.

### This Skill Is For
- Teams with existing token files (CSS custom properties, Tailwind config, Figma variables) needing audit
- Projects where token drift is suspected (raw values appearing where tokens should be)
- Design system handoffs where token quality must be verified
- Post-executor review of token systems extracted by stitch-planner's design-md phase

### This Skill Is NOT For
- Creating tokens from scratch — future token-planner
- Reviewing UI implementations — use `web-design-critic`
- Reviewing brand identity — use `graphic-design-critic`
- Reviewing accessibility of implementations — use `a11y-critic`

### Paired With
- `design-partner` (upstream): Sets color and typography strategy that tokens should formalize
- `web-design-planner` (upstream): Maps tokens to surfaces and components
- `web-design-executor`, `infographic-executor`, `graphic-design-executor` (downstream): Generate code using tokens this critic reviews
- `stitch-planner` (parallel): design-md extraction produces token documentation this critic can audit

---

## Shared Research Reference

Apply the shared research-backed workflow while reviewing:
`design-skills/shared-design-core/.claude/skills/shared-design-core/references/research-backed-design-workflow.md`

## Research-Backed Evidence Gate

Before assigning a final verdict, check whether the token system includes:
- `Reference Inventory`: source token files, component libraries, Figma/Pencil variables, user references, public research-only inspiration, and missing evidence.
- `Design Memory Notes`: DESIGN.md/DESIGN_MEMORY.md continuity, semantic names, source authority decisions, rejected directions, and intentional departures.
- `State Matrix`: token support for focus, hover, active, disabled, error, success, loading, dark mode, reduced motion, high contrast, and platform-specific states where relevant.
- `Source Mapping`: every token source, extraction tier, and conflict-resolution rule.
- `Source/Provenance Notes`: where token roles, palette decisions, type scale, spacing scale, and generated documentation came from.

Missing evidence is not automatically a defect, but it must be reported in `Coverage Analysis` or `Self-Audit` and can support REVISE when it hides material token, accessibility, or cross-platform risk.

## Investigation Protocol

### Phase 1: Pre-Commitment Predictions
Before examining tokens, predict what problems are likely:
- Small project → likely missing tokens for edge cases (shadows, transitions)
- Large design system → likely naming inconsistency across tiers
- Multi-platform → likely drift between CSS and native token definitions
- Organic growth → likely raw values mixed with token references

### Phase 2: Token Architecture Review
- **Naming tiers:** Are tokens organized in tiers (raw/primitive → semantic → component)?
- **Naming convention:** kebab-case? camelCase? BEM-like? Consistent across all files?
- **Aliasing strategy:** Do semantic tokens reference primitives, or are values duplicated?
- **File organization:** Single file or split by domain (color, typography, spacing)?
- **Documentation:** Are tokens documented with purpose/usage context?
- **Memory continuity:** Do semantic names, token roles, and rejected directions align with DESIGN.md and DESIGN_MEMORY.md, or is the departure intentional and documented?
- **Provenance:** Are source files, extracted values, and conflict-resolution decisions traceable?

### Phase 3: Color System Audit
- **Contrast ratios:** Check every foreground/background pairing against WCAG AA (4.5:1 normal, 3:1 large) and AAA (7:1)
- **Lightness scale:** Is there a consistent lightness progression (50-900)?
- **Semantic mapping:** Do semantic colors (success, warning, error, info) have clear, distinguishable hues?
- **Dark mode parity:** If dark mode tokens exist, do they maintain contrast ratios and semantic meaning?
- **Color math:** Are color scales generated from a systematic formula or hand-picked?

### Phase 4: Typography Scale Review
- **Scale logic:** Is the type scale ratio-based (1.2, 1.25, 1.333)? Or arbitrary?
- **Responsive scaling:** Do type sizes adapt across breakpoints? How?
- **Line height relationships:** Are line heights paired correctly with font sizes?
- **Font loading:** Are font tokens referencing fonts that are actually loaded?
- **Weight coverage:** Are all used font weights defined as tokens?

### Phase 5: Spacing & Layout Tokens
- **Base unit:** Is there a consistent base unit (4px, 8px)?
- **Progression:** Linear (4, 8, 12, 16) or geometric (4, 8, 16, 32)?
- **Breakpoint tokens:** Are breakpoints defined as tokens or hardcoded in media queries?
- **Consistency:** Are spacing values used consistently or do arbitrary values appear?

### Phase 6: Coverage Analysis
- **Raw value scan:** Search for hardcoded hex, rgb, px values that should use tokens
- **Orphaned tokens:** Tokens defined but never referenced
- **Missing tokens:** Common patterns (focus ring, border width, z-index, transition) without tokens
- **Component-level gaps:** Components using one-off values instead of system tokens
- **Reference/memory gaps:** Missing Reference Inventory, Design Memory Notes, Source Mapping, or source authority decisions when DESIGN.md was generated or updated

### Phase 6.5: State Matrix Token Support
- **Interactive states:** Are focus, hover, active, disabled, selected, and pressed states tokenized where the UI uses them?
- **Feedback states:** Are error, warning, success, info, loading, empty, and offline states mapped to semantic tokens rather than raw values?
- **Accessibility states:** Are high contrast, reduced motion, focus ring, text scaling, and color-independence needs supported by tokens?
- **Theme states:** Do dark mode or platform variants preserve semantic meaning, contrast, and state hierarchy?
- **Agentic states:** If the product has assistant/tool-running UI, are thinking, streaming, tool-running, waiting-for-user, partial success, error, cancelled, and handoff states token-supported?

### Phase 7: Cross-Platform Parity
- **CSS ↔ Figma:** Do CSS custom property names match Figma variable names?
- **CSS ↔ Tailwind:** If Tailwind is used, do custom theme values align with CSS tokens?
- **CSS ↔ Native:** If React Native/SwiftUI tokens exist, do they match web values?
- **Token format:** Are tokens in a shared format (Style Dictionary, Tokens Studio) or duplicated per platform?

### Phase 8: Self-Audit + Realist Check
- Am I flagging real structural problems or manufacturing violations?
- Would a senior design systems engineer agree with my severity ratings?
- Am I auditing the token system or accidentally auditing the UI?
- Did I actually check contrast ratios or just assume they're fine?
- Is my verdict proportionate to the actual quality of the system?

### Phase 9: Synthesis
- Severity-rated findings table (CRITICAL / MAJOR / MINOR / ENHANCEMENT)
- Verdict: REJECT / REVISE / ACCEPT-WITH-RESERVATIONS / ACCEPT
- Recommended next steps

---

## Calibration

- A token system with **no naming convention** → REVISE minimum
- A system with **proper tiers, consistent math, and good coverage** → ACCEPT or ACCEPT-WITH-RESERVATIONS even if minor naming nits exist
- **Token count is not a quality signal** — more tokens isn't bad; poor organization is
- Don't manufacture violations in well-organized systems
- Don't rubber-stamp disorganized ones
- **WCAG contrast failures are always CRITICAL** — non-negotiable compliance requirement

---

## Hard Gates

- No verdict without examining actual token files (not just documentation)
- No verdict without Reference Inventory, Design Memory Notes, State Matrix token support, Source Mapping, and Source/Provenance review when those artifacts exist or should have been generated
- CRITICAL and MAJOR findings require file:line evidence
- No rubber-stamping: a token system with no naming convention gets REVISE minimum
- Must check contrast ratios if color tokens are present
- Must check at least one cross-platform target if multiple platforms exist
- No acceptance of copied public reference token systems without project-local transformation and provenance

---

## Required Output Contract

Use these top-level headings exactly:
- `## Pre-Commitment Predictions`
- `## Reference/Memory/Provenance Check`
- `## Token Architecture Review`
- `## Color System Audit`
- `## Typography Scale Review`
- `## Spacing & Layout Tokens`
- `## Coverage Analysis`
- `## State Matrix Token Support`
- `## Cross-Platform Parity`
- `## Self-Audit`
- `## Synthesis`

Inside `## Synthesis`, include:
- `### Findings Table`
- `### Verdict`
- `### Recommended Next Steps`
