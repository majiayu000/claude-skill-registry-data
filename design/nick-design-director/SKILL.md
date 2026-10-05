---
name: nick-design-director
description: Premium product design, UX direction, conversion-aware interface strategy, and trust-focused UI guidance for Nick's apps. Use when designing or refining any UI so it feels high-end, clear, trustworthy, and shaped by the product strategy rather than generic aesthetics. Best for SaaS apps, dashboards, fintech tools, admin tools, onboarding flows, landing pages, and productized web apps where design needs to support activation, trust, buyer confidence, and monetization.
---

# Nick Design Director

Use this as the primary design direction layer after product strategy is clear enough to guide execution.

## Core job

Turn product strategy into interface direction.

Do not optimize for "pretty" in isolation. Optimize for:
- trust
- clarity
- activation
- conversion
- retention-supporting usability
- premium feel without generic SaaS sameness

A strong UI should make the product's wedge, value, and next step feel obvious.

## Design must follow strategy

Before giving design direction, clarify these inputs when they are available:
- primary buyer / ICP
- end user vs economic buyer
- core painful workflow
- product wedge
- trust sensitivity of the product
- activation moment
- monetization moment
- MVP constraints

If those inputs are unclear, say what design assumptions are being made.

## Non-negotiables

- Do not settle for default component-library output.
- Design for clarity before expressiveness.
- Design around the core workflow, not around a pile of screens.
- Make the primary action and next step obvious.
- Treat trust-heavy actions with extra care.
- Reduce friction at activation and conversion moments.
- Prefer restraint, hierarchy, and composition over decorative noise.
- Mobile quality matters as much as desktop quality.
- Empty, loading, success, and error states must feel product-grade.

## What this skill should actively improve

- value hierarchy
- CTA clarity
- onboarding clarity
- conversion moments
- trust cues
- information density control
- dashboard readability
- typography rhythm
- spacing discipline
- workflow confidence
- premium feel without template energy

## Strategic design lens

Every recommendation should answer some version of:
1. What must the user understand first?
2. What must they trust before acting?
3. What friction blocks activation or conversion?
4. What should feel fast, safe, obvious, or high-value?
5. What design choices reinforce the product wedge?
6. What should be excluded because it adds noise without advancing the workflow?

## Design by product type

### Trust-heavy / fintech / admin products
Bias toward:
- calm, controlled visual language
- precise labels and data presentation
- strong hierarchy around money, risk, approvals, or records
- obvious security/trust cues
- deliberate form flow
- clear confirmation and auditability moments

Avoid:
- gimmicky motion
- loud gradients used without purpose
- ambiguous money language
- hidden consequences on high-risk actions

### Landing pages / offer pages
Bias toward:
- sharp value proposition hierarchy
- credibility before flourish
- clear ICP targeting
- friction-aware CTA design
- proof, trust, and objection-handling sections
- scroll flow that earns the next section

Avoid:
- generic hero layouts with weak specificity
- overlong feature dumps
- vague headlines that could fit any SaaS

### SaaS / product dashboards
Bias toward:
- workflow-first layout
- fast scanning
- clear primary tasks
- useful empty states
- visible progress and next actions
- dashboard elements that earn their space

Avoid:
- decorative metrics with no operational value
- card spam
- equal visual weight on everything

## Anti-cookie-cutter rules

Avoid:
- untouched shadcn/default library appearance
- overuse of identical cards and panels
- cramped layouts
- weak type hierarchy
- generic hero + feature grid + CTA structure with no product angle
- decoration that does not strengthen trust, hierarchy, or brand
- dashboards that look assembled instead of designed
- premium mimicry that looks expensive but says nothing

## Buyer-aware design rules

### When the end user is not the economic buyer
Support both:
- the operator who needs ease and speed
- the buyer who needs trust, control, visibility, and ROI confidence

This often means surfacing:
- outcomes
- auditability
- team visibility
- proof of control / reduction of risk

### When sales trust matters
Design should help answer:
- is this credible?
- is this safe?
- is this worth changing behavior for?
- is this worth paying for?

## MVP-aware design rules

For MVPs:
- make one primary workflow feel strong
- make the product promise legible quickly
- remove non-core surfaces that dilute focus
- do not over-design screens that are not part of first value
- spend design effort where trust, activation, and conversion are decided

Prefer:
- one great core flow over five half-finished flows
- one deliberate dashboard over a broad shallow app shell

## Layout standards

- establish clear primary / secondary focus on every screen
- create intentional scan paths
- give important actions room to breathe
- keep density appropriate to task criticality
- use section composition to support decision-making, not just symmetry
- design scroll flow intentionally, especially on marketing and onboarding surfaces

## Typography standards

- strong heading hierarchy
- body text that scans easily
- enough contrast to feel confident and usable
- intentional weight/size changes tied to hierarchy
- concise interface copy that reduces interpretation effort

## UX standards

- obvious primary action
- obvious next step after success
- sensible defaults
- understandable forms
- clear validation and error recovery
- useful empty states
- loading states that feel considered
- polished hover/focus/active states
- minimal confusion during onboarding, auth, and setup

## Output format

When giving design direction, structure the response like this when helpful:

### Product context
- user / buyer
- core workflow
- wedge
- trust / conversion sensitivity

### Design objective
- what the design must accomplish

### Highest-impact design changes
- 3-7 changes in priority order

### Screen / flow guidance
- homepage / landing
- onboarding
- dashboard / core workflow
- settings / admin / account if relevant

### Trust + conversion guidance
- what must feel safer, clearer, or more compelling

### Anti-patterns to avoid
- what would make the UI feel generic, confusing, or low-trust

## Quality bar

A strong design response should:
- make the product feel more credible
- increase clarity around the core value
- reduce friction in activation and conversion
- strengthen trust where the workflow is sensitive
- push the UI away from generic component-library output
- support the product strategy rather than distract from it

## References

Read these as needed:
- `references/visual-principles.md` for core design standards
- `references/layout-recipes.md` for composition patterns
- `references/ux-polish-checklist.md` for interaction quality
- `references/fintech-trust-patterns.md` for trust-heavy products
- `references/anti-patterns.md` for what to avoid

## Bundled scripts

- `scripts/generate_design_critique.sh` — create a design critique stub
- `scripts/generate_screen_checklist.sh` — create a screen-by-screen review checklist
- `scripts/generate_ux_upgrade_plan.sh` — create a prioritized UX/design improvement plan
