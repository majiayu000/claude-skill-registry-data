---
name: motion-guide
description: "Use when designing, adding, changing, suggesting, or reviewing UI motion. Motion Guide is a default-trigger motion decision advisor for AI coding agents: it decides whether motion should exist, selects an appropriate functional or expressive pattern, and constrains implementation with timing, easing, accessibility, reduced-motion, and performance safeguards."
---

# Motion Guide Advisor

Motion Guide is a default-trigger motion decision skill for AI coding agents. It helps the agent decide **whether motion should exist**, which Motion Guide pattern fits the product situation, and how to implement or review that motion without harming accessibility, performance, readability, or task completion.

It is not a component library or effect gallery. It may recommend `no motion`, a static layout change, clearer copy, or a lighter interaction state when motion would not improve the product.

## When to Use

Use this skill whenever an agent is designing, adding, changing, suggesting, or reviewing UI that may include motion, even if the user did not explicitly say "animation".

Common triggers:

- loading states, progress, skeletons, spinners, or async status
- form submission, button feedback, success/error confirmation, or toast behavior
- route, modal, drawer, tab, card, or view transitions
- hover, focus, press, drag, swipe, or input feedback
- onboarding cues, coach marks, guided tours, or feature discovery
- chart/data reveals, counters, timelines, or knowledge/system visualization
- scroll progress, sticky navigation, parallax, reveal-on-scroll, or reading aids
- brand-forward landing pages, product showcases, storytelling, 2D/3D/WebGL/shader/particle hero motion
- code review of an existing UI diff that adds, removes, or changes motion

When website content changes, keep this skill plus `references/motion-database.md` and `references/creative-motion-pack.md` synchronized with the public Motion Guide decision set.

## When Not to Use

Do not add or intensify motion when it lacks a clear product function. Prefer static hierarchy, spacing, contrast, clearer copy, or instant state changes for:

- checkout, payment, destructive, legal, security, medical, financial, trading, or operational-critical flows
- dense dashboards, admin tables, settings, logs, or frequent repetitive workflows
- precision tools where elasticity, bounce, delay, or theatrical motion implies imprecision
- fake or unmeasurable progress; never show a determinate percentage without real progress data
- long text pages where parallax, scroll hijacking, or repeated reveals reduce reading clarity
- large/filterable lists where staggered animations replay across many items
- any interaction where motion delays access to primary content or hides critical information

Creative/decorative motion is allowed only when it supports brand expression, storytelling, product understanding, focused attention, or system comprehension without damaging usability.

## Output Contract

Preserve these decisions internally for every motion task:

1. **Motion decision**: `use motion`, `reduce motion`, or `no motion`.
2. **Selected pattern**: Motion Guide slug, or why no pattern applies.
3. **Product reason**: the function served by the motion, not just the visual effect.
4. **Misuse boundary**: at least one concrete when-not-to-use condition.
5. **Implementation constraints**: duration, easing, accessibility, reduced-motion, focus/keyboard/screen-reader behavior, and performance notes.
6. **Verification**: what to test manually or with tooling.

For normal user-facing replies, keep the rationale concise. Report the selected pattern, key constraints, and verification. Do not dump the full checklist unless the user asks for detailed reasoning or an audit report.

## Decision Workflow

1. **Detect context** — identify page type, user task, interaction state, brand intent, device constraints, and risk level.
2. **Gate motion** — decide whether motion is functional, expressive, decorative-but-justified, reducible, or unnecessary.
3. **Select pattern** — match the context to a documented Motion Guide pattern and compare nearby alternatives.
4. **Implement minimally** — use the smallest useful motion layer. Do not add a motion library for simple opacity, scale, press, hover, or focus feedback when CSS or existing primitives are enough.
5. **Verify** — confirm the motion improves comprehension or product communication and does not block task completion.

## Practical Motion Mode

Practical Motion Mode is the default for ordinary product UI, dashboards, forms, checkout, admin tools, and routine workflows.

Use motion when it improves:

- feedback and confirmation
- navigation, spatial orientation, or hierarchy
- state-change comprehension
- loading/progress confidence
- input clarity and tactile response
- onboarding or guidance
- data understanding
- meaningful content reveal

High-confidence mappings:

| Situation | Primary pattern | Notes |
|---|---|---|
| Form submit | `button-loading-state` | Keep the user anchored to the submitted action. |
| Unknown wait | `spinner`, `indeterminate-progress-bar`, or honest status text | Do not fake determinate progress. |
| Measurable upload/import | `progress-bar` | Use only when progress is real. |
| List/feed loading | `skeleton-screen`, optionally `shimmer-loader` | Preserve layout context. |
| Search/filter flow | `expandable-search-bar`, instant results, result-count feedback | Avoid decorative animation on search-first pages. |
| Validation error | `form-validation-error` | Point to the exact fix; avoid playful destructive-error motion. |
| Onboarding explanation | `popover-coach-step` | Use semantics and copy, not just attention effects. |
| Lightweight attention | `focus-ring-highlight` | Only when the user already understands the control. |
| Trend reveal | `line-chart-draw` | Use selectively when motion clarifies the trend. |
| Long reading | `scroll-progress-bar` | Avoid parallax on mobile/text-heavy pages. |
| Non-blocking success | `toast-notification` | Use when the user can continue. |
| Journey-complete success | `success-screen-transition` | Use only after real completion. |

For all 114 patterns, use `references/motion-database.md`.

## Creative Motion Mode

Creative Motion Mode is opt-in by context. Activate it only when:

- the user explicitly asks for creative, expressive, cinematic, immersive, 3D, shader, particle, WebGL, React Three Fiber, kinetic, morphing, or generative motion; or
- the product context is a brand-forward landing page, portfolio, marketing hero, launch page, product showcase, storytelling experience, editorial feature, AI/system visualization, or data/system narrative.

Creative motion still needs product intent. Do not add creative motion as standalone decoration with no reusable product function.

Creative categories and examples:

- **3D Product Showcase**: `floating-product-object`, `interactive-3d-card-stack`, `orbital-feature-system`
- **Shader / Atmosphere**: `aurora-shader-background`, `morphing-gradient-blob`, `particle-network-field`
- **Data / System Visualization**: `data-stream-tunnel`, `animated-knowledge-graph`, `tool-call-timeline`
- **Kinetic Typography**: `svg-path-drawing`, `kinetic-headline-reveal`
- **AI / Tech Expression**: `ai-thinking-orb`

Use `references/creative-motion-pack.md` for detailed decision cues, constraints, and prompt guidance.

Creative constraints:

- target 60fps and provide a lower-end fallback
- include reduced-motion fallback: static keyframe, still image, simplified fade, or minimal state change
- do not convey critical information through motion alone
- avoid creative effects in dashboards, forms, checkout, admin, or dense operational interfaces unless there is an explicit product reason

## Evaluation-Backed Rules

This skill's strongest value is precise pattern mapping, accessibility coverage, implementation readiness, and restraint. Preserve these rules when advising, coding, or reviewing:

- Prefer honest progress states: `indeterminate-progress-bar`, staged status text, `button-loading-state`, or real `progress-bar` only when measurable.
- Confetti and celebratory motion only after real completion. Pending payment, authorization, upload, save, or async agent work should show loading/status, not celebration.
- For AI/tool activity, use `tool-call-timeline` as the primary accountable pattern. `ai-thinking-orb` is ambient only and must not replace observable step states.
- Coach marks need semantics. Use `popover-coach-step` when users need explanation; `focus-ring-highlight` is only enough for lightweight attention.
- Reject spatial or personality-heavy motion in enterprise, ops, and dense dashboards: avoid bounce, gooey nav, large 3D grids, and dramatic route transitions.
- Large lists should not item-stagger. For repeated search/filter workflows, use instant updates, group-level fades, skeletons, or direct feedback instead of many delayed items.
- Animate charts only when motion improves comprehension. Use `line-chart-draw`, `chart-bar-growth`, or `pie-chart-reveal` selectively.
- Avoid adding animation libraries for trivial effects. CSS or existing dependencies are enough for simple scale, opacity, hover, focus, and press feedback.
- Every recommendation should include reduced-motion behavior, screen-reader/focus notes where relevant, performance constraints, and no-go examples.

## Code Generation Rules

When modifying UI code:

- **Frequent route transitions**: prefer opacity-only fades by default. Avoid blur and spatial `x/y` travel unless continuity requires it. Reduced motion should bypass the transition, not merely shorten a risky transform.
- **Large or filterable grids**: do not use container-wide stagger that replays across all results. Use first-load-only reveal with a capped delay, then keep filtering immediate.
- **Bound delay by cap, not result count**: if reveal is useful, cap delay to the first few items rather than scaling across dozens or hundreds of cards.
- **Result updates**: preserve focus and scroll predictability. Consider polite result-count/grid announcements when filtering changes visible content.
- **Coach/tour components**: represent relationships semantically with labels/descriptions. Do not collapse meaningful coach UI into one `role="img"` unless it is purely decorative documentation.
- **Demo components**: keep compact demos focus-safe. If demo controls are not truly interactive, avoid unexpected tab stops; if they are interactive, provide real dismissal/next controls and focus return.
- **Dependency restraint**: use CSS/Tailwind/existing primitives first. Add Framer Motion, GSAP, Lottie, Three.js, or WebGL only when the product need justifies the dependency and a fallback exists.

Timing defaults:

```text
button press: 100-150ms
hover/focus/scale: 150-250ms
fade: 150-300ms
slide/drawer/modal: 200-400ms
shared element: 300-500ms
error shake: 400-600ms
spinner cycle: 700-1000ms
shimmer cycle: 1.5-2.5s
```

Reduced-motion examples:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
className="transition motion-reduce:transition-none motion-reduce:animate-none"
```

## Review Mode

When reviewing an existing UI diff, do not only praise the animation. Inspect whether motion should exist at all.

Review steps:

1. Identify all added, changed, or removed motion: CSS transitions/animations, JS animation code, motion libraries, route transitions, hover/focus effects, loading/status components, scroll effects, and creative effects.
2. Classify each motion as functional, expressive-but-justified, decorative-risky, misleading, inaccessible, performance-heavy, or unnecessary.
3. Check for missing reduced-motion, keyboard/focus handling, screen-reader announcements, and layout stability.
4. Flag fake progress, celebration before completion, repeated large-list stagger, slow modal/route transitions, scroll hijacking, and animation libraries added for trivial effects.
5. Suggest the smallest safe patch: remove, reduce, replace pattern, or add accessibility/performance constraints. Avoid wholesale rewrites unless the motion architecture is fundamentally wrong.
6. Verify with the relevant checks: build/typecheck, browser smoke, reduced-motion mode, keyboard navigation, and representative low-end/mobile behavior when feasible.

Review output should separate:

- **Keep**: motion that clearly helps product comprehension or feedback
- **Reduce**: motion that is useful but too intense, slow, or broad
- **Remove**: motion with no clear product function or high risk
- **Fix**: missing reduced-motion, semantics, focus behavior, or performance guardrails

## Anti-Patterns to Avoid

- **Endless spinner**: spinner running beyond a short wait without explanation. Use skeletons, progress, or status text.
- **Fake progress bar**: determinate bar without real progress data. Use indeterminate progress or honest copy.
- **Celebration before completion**: confetti/checkmarks while payment/upload/save/agent work is still pending.
- **Slow modal or route entrance**: theatrical movement when the user expects immediate focus or navigation.
- **Aggressive hover motion**: cards jumping, tilting, or glaring during grid scanning.
- **No reduced motion**: large, looping, scroll-linked, blur, parallax, or vestibular-sensitive motion without fallback.
- **Decorative dashboard motion**: personality-heavy effects in dense admin/ops/analytics views.
- **Library inflation**: adding a heavy dependency for a simple opacity/scale/press effect.

## References

- `references/motion-database.md` — full 114-pattern database with when-to-use, when-not-to-use, timing/easing, risks, alternatives, code notes, and real-world examples.
- `references/creative-motion-pack.md` — creative motion mode, 2D/3D/WebGL/shader/data/system visualization guidance.

## Verification Checklist

- [ ] Motion has a clear role: feedback, navigation, state comprehension, progress, input clarity, guidance, data understanding, content reveal, or explicit brand/expression.
- [ ] Selected pattern matches a Motion Guide situation, comparison, recipe, or documented pattern.
- [ ] Recommendation includes when-not-to-use guidance, especially for task-heavy interfaces.
- [ ] Decorative/expressive motion is constrained to contexts where brand, storytelling, delight, atmosphere, or product understanding is part of the goal.
- [ ] Creative motion has performance budget, low-end fallback, and reduced-motion fallback.
- [ ] No critical information is conveyed through motion alone.
- [ ] Timing and easing are specific and appropriate.
- [ ] Reduced-motion fallback is included for large, looping, scroll-linked, parallax, blur, or vestibular-sensitive motion.
- [ ] Implementation avoids fake progress, premature celebration, competing animations, layout instability, and unnecessary expensive paints.
- [ ] Result does not hide primary actions, trap focus, or delay access to critical information.
