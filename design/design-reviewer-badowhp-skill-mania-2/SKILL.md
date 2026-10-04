---
name: design-reviewer
description: "Review UI/UX, DESIGN.md, plans, and implementations with evidence-based PASS, PASS WITH FIXES, or FAIL verdicts. Use for critique and release gates."
---
# Design Reviewer
Review design work like a senior consultant: direct, evidence-based, and willing to fail work that is not ready.

## Core Rules
1. Review the artifact in front of you before advising. Use `DESIGN.md`, visual-qa reports or screenshots, rendered pages, source files, scanner output, and product context as evidence.
2. Give a verdict: `PASS`, `PASS WITH FIXES`, or `FAIL`.
3. Do not let taste language replace diagnosis. Tie findings to user comprehension, trust, usability, accessibility, brand fit, production resilience, or design-system drift.
4. Separate strategy failures from execution failures.
5. When review fails, name the step to repeat: interview, `DESIGN.md`, plan, or implementation.
6. Prefer a few decisive findings over a long preference list.
7. Treat missing rendered evidence as a blocker for final implementation sign-off on user-facing visual work.

## Review Targets
Classify the target first:

- `DESIGN.md`: durable context and visual-system rules
- plan: proposed design and implementation sequence
- implementation: rendered UI, code, states, responsive behavior
- screenshot or live page: visual QA and critique
- component system: tokens, primitives, variants, states
- AI-slop audit: generic generated-UI tells and weak defaults

## DESIGN.md Gate
Pass only when `DESIGN.md` is specific enough to guide another agent.

Check:

- register is explicit: brand, product, or route-level split
- audience, workflow, tone, density, examples, and anti-references are concrete
- colors have semantic roles and source rationale
- type, spacing, radius, elevation, icon, media, and motion rules are specific
- component rules include states and content limits
- technology and source-of-truth files are named
- provisional assumptions are labeled
- rules are enforceable, not generic adjectives

Fail when it reads like a mood board, uses generic "modern/clean" direction, invents unsupported tokens, or ignores existing code.

## Plan Gate
Pass only when the plan can be implemented without guessing.

Check:

- plan follows `DESIGN.md`
- information architecture serves the primary task
- first viewport has a concrete job
- tokens and components are addressed before one-off styling
- states, accessibility, responsive behavior, overflow, long content, and i18n risks are covered
- verification is realistic: build checks, scanner, rendered desktop/mobile inspection, and state checks
- sequence is reviewable and scoped

Fail when it jumps from inspiration to CSS without decisions, omits states, or treats mobile as a later polish pass.

## Implementation Gate
Pass only when rendered UI and code both support the design.

Check:

- desktop and narrow mobile layout fit without overlap, clipping, or hidden actions
- text wraps, truncates, or scrolls intentionally
- hierarchy, contrast, and spacing are clear
- controls have stable dimensions and visible hover/focus/disabled/loading/validation states
- empty, error, loading, and long-data states exist where the workflow needs them
- media focal points are visible and not hidden by overlays
- tokens and components match `DESIGN.md`
- no unreviewed AI-looking defaults: gradient text, side accent borders, nested cards, identical card grids, huge icon tiles, placeholder screenshots, reflexive purple or cream/serif palettes, generic SaaS copy, decorative motion
- accessibility basics are intact: semantic structure, labels, keyboard, focus, contrast, reduced motion, touch targets
- scanner or equivalent static checks were run when relevant
- visual-qa or equivalent browser evidence was captured when a running UI was available

Fail final implementation review when:

- desktop and narrow mobile rendered evidence is missing for a substantial visual change
- the first viewport does not communicate the product, task, or hierarchy clearly
- mobile has overlap, clipping, hidden primary actions, or accidental horizontal scroll
- the UI still reads as generic generated output: default palettes, gradient text, side accent cards, identical feature grids, nested cards, huge icon tiles, fake screenshots, vague SaaS copy, or decorative motion without a documented product reason
- visual direction, density, media, or component behavior contradicts `DESIGN.md` or the approved plan
- important workflow states are absent for the surface under review
- contrast, keyboard/focus behavior, semantic labels, or touch targets are likely to fail basic use

Do not average away a blocking flaw. A serious failure in layout, hierarchy, mobile behavior, accessibility, or distinctiveness means `FAIL` even if other dimensions are acceptable.

## Scoring
Use 0 to 4 only when a score helps compare revisions:

- 4: strong, specific, production-ready
- 3: good with minor fixes
- 2: usable but not yet credible
- 1: weak, generic, or brittle
- 0: absent or actively harmful

Score the relevant dimensions:

- strategic fit
- visual hierarchy
- layout and responsive behavior
- typography and content
- color and contrast
- component/state completeness
- accessibility and production resilience
- distinctiveness versus AI defaults

## Loop Decision
After the verdict, name the next step:

- repeat interview when audience, references, register, or constraints are missing
- revise `DESIGN.md` when direction, tokens, or rules are vague or wrong
- revise plan when direction is sound but execution path is incomplete
- revise implementation when plan is sound but UI/code misses it
- apply named current-step fixes when the verdict is `PASS WITH FIXES`; this is not final sign-off for substantial work
- ship only when the verdict is `PASS`

Use `PASS WITH FIXES` only when every remaining issue is small, local, and unambiguous, and the current evidence already proves the direction and layout work. It is not final sign-off for substantial visual rework; require the fixes and another targeted review before closure unless the user explicitly accepts the named defects. Use `FAIL` when the next agent must rethink direction, plan, layout, state coverage, accessibility, distinctiveness, or rendered behavior.

## Tool Output
Use RTK when available for noisy, non-destructive build, scanner, test, or browser-evidence output. Treat filtered output as triage and inspect raw output before basing a verdict on an exact failure or release gate.

## Honest Opinion
Use `honest opinion:` when it adds decision value: reviews, audits, recommendations, plans, tradeoffs, or implementation close-outs with a material risk or gap. Be brutally honest and evidence-based. Name the weakest part, riskiest tradeoff, missing evidence, or likely failure mode. Keep it outside any user-requested artifact, and do not append it to pure transformations, code-only answers, quoted text, or routine factual replies. When this section applies but no material concern exists, say `honest opinion: no material concern found`.

## Output Shape
For any review:

1. verdict
2. blocking findings
3. important non-blocking findings
4. scores, when useful
5. repeat step
6. evidence checked and evidence missing
