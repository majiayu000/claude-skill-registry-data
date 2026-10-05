---
name: ui-critic
description: "Review UI and mockups for usability, visual consistency, interaction patterns, and accessibility."
version: 0.1.0
---

# UI Critic

## JTBD (Jobs To Be Done)

### Primary Job
When I already have a design artifact and need to know whether it is actually good enough to ship,
I want an evidence-backed review of what is helping or hurting users,
so I can fix real problems without getting lost in taste-only feedback.

### Secondary Jobs
- When a UI feels off but I cannot explain why, I want a structured diagnosis, so I can target the right fixes.
- When I need launch confidence for a design change, I want a harsh but grounded review, so I can ship with fewer blind spots.

### Job Layers
- Functional: Review an existing UI artifact for usability, accessibility, consistency, and readiness with concrete evidence.
- Emotional: Reduce uncertainty about whether the artifact is truly ready or just looks polished in static review.
- Social: Helps the user defend design decisions and fixes to stakeholders, teammates, and reviewers with evidence rather than opinion.

### This Skill Is For
- A user with a live UI, screenshot, mockup, or spec who wants diagnosis before launch or handoff.
- A user who wants to know what is genuinely impairing usability rather than collecting vague feedback.
- A user validating whether a design artifact meets accessibility and consistency expectations in real use.

### This Skill Is NOT For
- A user who needs a fresh design direction or a new design plan from rough requirements; use `design-partner`.
- A user who only needs domain implementation planning without reviewing an existing design artifact.

### Paired With
- `design-partner`: After `ui-critic` identifies current-state failures, use it to produce the next design direction or redesign response.
- `a11y-critic` or specialist domain critics: Layer them in when accessibility or domain-specific risks need a deeper primary review.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has an existing UI and wants launch confidence | UI Critic runs browser-first review | Verdict plus evidence-backed findings |
| Has confusing user feedback but no clear diagnosis | UI Critic identifies actual friction and severity | A prioritized problem list |
| Wants review and redesign in one pass | UI Critic diagnoses first, then hands off to `design-partner` | Findings plus a clear next design step |

### When to Escalate
- If browser testing cannot happen and the user needs real ship-confidence, escalate to live testing before final sign-off.
- If the next job after diagnosis is redesign or system direction, escalate to `design-partner`.

## Overview
Run a harsh-critic style review with design-specific checks, Nielsen's heuristic evaluation, accessibility audit, visual consistency analysis, and context-driven audience perspectives.

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
- Design review rubric: [references/design-review-rubric.md](references/design-review-rubric.md)
- Audience activation: [references/audience-activation-matrix.md](references/audience-activation-matrix.md)

## Research-Backed Evidence Gate
Before assigning a final verdict, check whether the artifact or plan includes:
- `Reference Inventory`: project-local sources, user examples, research-only inspiration, style vocabulary, anti-patterns, and missing evidence.
- `Design Memory Notes`: DESIGN.md/DESIGN_MEMORY.md continuity, durable decisions, and intentional departures.
- `State Matrix`: normal, loading, empty, error, disabled, focus, hover/tap, active, and any agentic/tool-running states.
- `Source/Provenance Notes`: where visual decisions, tokens, references, and generated UI patterns came from.
- Agentic interface controls when relevant: visible status, generated UI regions, tool invocation affordances, cancellation/retry, confirmation, and trust boundaries.

Missing evidence is not automatically a design defect, but it must be reported in `What's Missing` and can support REVISE when it hides material UX or design-system risk.

## Browser-First Review Protocol (Mandatory)
All testing and evaluation MUST happen in an actual browser. Do not evaluate designs from a single static screenshot or by reading code alone.

**Experience the page as a human user would:**
- Open the page in a real browser (Playwright MCP, Claude in Chrome, or equivalent).
- Scroll through the page top-to-bottom at a natural reading pace — do NOT take a single full-page screenshot and evaluate from that. Humans don't see pages all at once; they scroll, scan, and discover content progressively.
- At each scroll position, take a screenshot and evaluate what's visible in the current viewport. Note what draws the eye first, what feels confusing, what gets lost.
- Test at multiple viewport sizes (375px mobile, 768px tablet, 1280px desktop, 1920px wide) — actually resize and scroll through each one.
- Interact with the page: hover elements, tab through focus order, click buttons, fill forms. Don't just look — use it.
- Record your experience chronologically: "On first load I see X, after scrolling I notice Y, the Z button is easy to miss because..."

**Why this matters:** A design can look perfect in a full-page screenshot but fail completely in actual use. Above-the-fold hierarchy, scroll-dependent discovery, viewport-specific layouts, interaction feedback, and progressive disclosure can only be evaluated by experiencing the page the way real users will.

**If browser testing is not possible** (e.g., reviewing a static mockup image with no live URL), explicitly state this limitation in the Overall Assessment and note which checks could not be performed. Treat the review as incomplete — recommend browser testing before shipping.

## Workflow
1. Confirm review target and scope (mockup, component, page, live URL, design system).
2. **Open the target in a real browser** (see Browser-First Review Protocol above). If reviewing a live URL or local dev server, navigate to it and begin the scroll-and-scan process before any other analysis.
3. Make 3-5 pre-commitment predictions about likely UX failure points before deep review.
4. Run the Research-Backed Evidence Gate: check reference provenance, memory continuity, state coverage, source notes, and agentic interface controls where applicable.
5. Run protocol phases in order: verification, heuristic evaluation, multi-perspective analysis, explicit gap analysis, synthesis.
6. If reviewing design specs/plans, also run plan-specific checks: assumption extraction, user journey gap analysis, edge case audit, responsive breakpoint analysis, provenance/source review, and devil's-advocate challenge for major design decisions.
7. Run mandatory self-audit before finalizing findings:
   - LOW confidence or easily-refutable claims move to `Open Questions (unscored)`.
   - Preference/style-only points are downgraded or removed from scored sections.
   - Keep scored sections evidence-backed and high-confidence.
8. Run Realist Check on every surviving BLOCKS_USE/IMPAIRS_USE finding:
   - "If we shipped this design as-is, what is the realistic worst-case user experience?"
   - "What percentage of users would actually encounter this issue?" (all users, edge case, specific device/context)
   - "How quickly could this be detected and fixed post-launch?" (analytics, user reports, A/B test)
   - "Is the severity proportional to actual user impact, or was it inflated by reviewer standards?"
   Recalibration rules:
   - Edge case affecting <5% of users with easy workaround → downgrade BLOCKS_USE to IMPAIRS_USE
   - Mitigating factors substantially limit impact → downgrade one level
   - Fast detection + straightforward fix → note context but keep severity
   - Survives all four questions → correctly rated, keep it
   - NEVER downgrade findings involving accessibility barriers, data loss, or safety risks
   - Every downgrade MUST include a "Mitigated by: ..." statement.
   Report recalibrations in the Verdict Justification.
9. Apply the design review rubric from [design-review-rubric.md](references/design-review-rubric.md).
10. Activate perspectives based on [audience-activation-matrix.md](references/audience-activation-matrix.md).
11. Load at most 2-3 specialist external skills from the routing map when needed.
12. Return structured verdict with evidence.

## Compositional Quality Review (Always Run — after browser testing, before heuristic evaluation)
Evaluate the design as a composition, not just a collection of components:

- **First-viewport poster test:** Does the first viewport function as a standalone poster? Is the brand/product unmistakable? Is there one dominant visual element? Scannable in under 3 seconds?
- **Visual anchor per section:** Does each major section have one strong visual anchor? Or are sections text-heavy walls with no focal point?
- **Section job clarity:** Does each section have exactly one job? Or do sections mix purposes (hero that also shows testimonials and a feature grid)?
- **Card justification:** Are card grids actually necessary? Do cards enable interaction or are they decorative containers? Unjustified cards are FRICTION-level.
- **Headline meaning:** Do headlines carry product/brand meaning or are they generic decoration?
- **Motion quality:** If present, does motion serve hierarchy or atmosphere? If absent on a marketing page, note as gap.
- **Typography hierarchy:** Clear display → heading → body → caption levels? Max 2 font families?
- **Visual weight distribution:** Do primary sections (hero, CTA) have greater visual weight than secondary sections? Or is everything equal?

Report in a `### Compositional Quality` subsection within findings. Generic first viewport or flat visual hierarchy = IMPAIRS_USE. Unjustified cards or decorative headlines = FRICTION.

## Heuristic Evaluation (Nielsen's 10 — Always Run)
Evaluate the artifact against each heuristic. Score each 0-4 (0=no issues, 4=catastrophic):

1. **Visibility of system status** — Loading states, progress indicators, confirmation feedback, state changes.
2. **Match between system and real world** — Natural language, familiar concepts, logical information ordering.
3. **User control and freedom** — Undo/redo, escape hatches, clear back-navigation, non-destructive defaults.
4. **Consistency and standards** — Platform conventions, internal consistency across views, pattern library adherence.
5. **Error prevention** — Confirmation dialogs, input constraints, smart defaults, destructive action guards.
6. **Recognition rather than recall** — Visible options, contextual help, minimal memory load, affordances.
7. **Flexibility and efficiency** — Keyboard shortcuts, expert accelerators, customization, progressive disclosure.
8. **Aesthetic and minimalist design** — Signal-to-noise ratio, information hierarchy, visual clutter, whitespace.
9. **Error recovery** — Plain language errors, specific problem identification, constructive solutions.
10. **Help and documentation** — Searchable, task-focused, concise, contextual, discoverable.

Include heuristic scores in the `Heuristic Evaluation Summary` output section.

## Required Output Contract
Use this exact top-level structure:
- `VERDICT: [REJECT | REVISE | ACCEPT-WITH-RESERVATIONS | ACCEPT]`
- `Overall Assessment`
- `Browser Testing Log` (chronological account of the scroll-and-scan experience: what was seen at each viewport position, what drew attention, what was missed, what interactions were tested — at each tested viewport size)
- `Pre-commitment Predictions`
- `Reference/Memory/Provenance Check`
- `Heuristic Evaluation Summary` (table: heuristic name, score 0-4, key finding)
- `Critical Findings (BLOCKS_USE)`
- `Major Findings (IMPAIRS_USE)`
- `Minor Findings (FRICTION)`
- `Polish Suggestions (POLISH)`
- `What's Missing`
- `Accessibility Notes`
- `Multi-Perspective Notes`
- `Verdict Justification`
- `Open Questions (unscored)`

Rules:
- BLOCKS_USE and IMPAIRS_USE findings must include concrete evidence (element reference, screenshot region, code location, or specific UI description).
- If a section has no items, write `None.`
- Keep speculative points in `Open Questions` only.
- In `Verdict Justification`, state whether escalation to adversarial review happened and why.

## Perspectives
Always run:
- End User (first-time and returning)
- Accessibility (WCAG 2.1 AA minimum)
- Brand/Visual Consistency

Context-driven (activate when triggered):
- Mobile User (when responsive behavior is relevant)
- Power User (when expert workflows are present)
- Content Author (when CMS or editorial UI is involved)

Perspective notes must appear in `Multi-Perspective Notes`.

## Severity Scale (Design-Specific)
- **BLOCKS_USE**: Users cannot complete core tasks. Accessibility barriers preventing use. Critical interaction broken.
- **IMPAIRS_USE**: Users can complete tasks but with significant confusion, frustration, or errors. Major a11y issues.
- **FRICTION**: Noticeable UX friction, minor inconsistencies, suboptimal but workable patterns.
- **POLISH**: Aesthetic improvements, micro-interaction refinements, edge-case smoothing.
- Do not inflate severity for taste-only preferences.

## Design-Specific Must-Check List
Always check these before final verdict:
- Reference and provenance: Are public references transformed into local decisions rather than copied?
- Design memory continuity: Does the artifact respect DESIGN.md and DESIGN_MEMORY.md, or explain intentional departures?
- State matrix: Are all core interaction states covered, including agentic/tool-running states when relevant?
- Information hierarchy: Is the most important content visually prioritized?
- Interaction feedback: Does every interactive element have hover/focus/active/disabled states?
- Responsive behavior: Does the layout work at mobile (375px), tablet (768px), desktop (1280px), wide (1920px)?
- Loading and empty states: Are skeleton screens, spinners, and empty state messaging present?
- Error states: Are form validation, network errors, and edge cases handled?
- Contrast and readability: Does text meet WCAG 2.1 AA contrast ratios (4.5:1 normal, 3:1 large)?
- Keyboard navigation: Can all interactive elements be reached and operated via keyboard?
- Focus management: Is focus visible and logically ordered?
- Touch targets: Are tap targets at least 44x44px on mobile?
- Color independence: Is information conveyed by means other than color alone?

## Skill Loading Rules
- Default: one review/critique skill + one a11y skill.
- Avoid loading overlapping skills unless scope is broad.
- Prefer higher-priority, active entries in external manifest.

## MCP Integration Points (When Available)
- **Playwright MCP**: Screenshot comparison, responsive testing, accessibility-first browser testing.
- **axe-core MCPs**: Automated WCAG scanning layered with heuristic review.
- **Pencil**: `snapshot_layout` for structural analysis, `get_screenshot` for visual verification.

## Stop Conditions
- If review scope is too broad, narrow by component/page/feature.
- If evidence cannot be found, move concern to `Open Questions`.
