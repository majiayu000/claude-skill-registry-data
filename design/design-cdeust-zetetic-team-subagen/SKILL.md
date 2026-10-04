---
name: design
description: UX/UI design and accessibility audit -- name the user, task, and success criterion before any layout decision, enforce WCAG 2.2 AA as a constraint from the first sketch, walk the 10 Nielsen heuristics, and refuse patterns that defeat usability or research integrity.
---

# Design

## Purpose

Decide what interface a user should encounter, why, and on what evidence. Three decision
types: the user task flow (who, what, success criterion, failure modes) before any visual
decision; the accessibility constraint envelope (WCAG 2.2 AA enforced from the first sketch,
not audited at the end); and the design-system consistency verdict (reuse a token/component,
or justify the exception). Not aesthetic preference -- the procedure below, applied in order.

## Procedure

1. **Name the user, the task, the success criterion, and the failure modes (Move 1).** A
   specific user segment with a competency level (not "users"); a verb phrase with an outcome;
   an observable/measurable success criterion; enumerated failure modes (input error, network
   failure, screen-reader silence, keyboard focus lost, etc.). Do not propose a layout before
   these four sentences exist.

2. **Calibrate stakes.** High: onboarding, checkout, critical flows, accessibility-critical
   forms, error handling. Medium: settings, navigation, dashboards. Low: marketing pages,
   internal admin tools for trained users. Record the classification and its criterion.

3. **Accessibility audit -- WCAG 2.2 AA is a constraint from the start (Move 2).** Perceivable /
   Operable / Understandable / Robust. For every interactive element: keyboard reachability,
   visible focus indicator not obscured by other content (2.4.11), no keyboard trap. For every
   text block: contrast (body >=4.5:1, large text >=3:1, UI boundaries >=3:1). For every image:
   informative (alt text) or decorative (empty alt) -- no third category. For every form input:
   a persistent `<label>` (never placeholder-only), errors associated via `aria-describedby`.
   For every state change: a live region or a focus move. Native HTML element first; ARIA only
   when semantic HTML is insufficient. Touch targets: AA minimum 24x24 CSS px (2.5.8), prefer
   the stricter 44x44 px AAA target (2.5.5) as canonical mobile guidance. If any of these seven
   checks has an unverified answer, the design is not ready.

4. **Enumerated refusals (Move 3).** Refuse by default, absent a documented justification:
   "users want X" without a cited method/n/confidence; a new component or token when an
   existing one fits within tolerance; color as the sole indicator (WCAG 1.4.1); placeholder
   text as the only label (WCAG 3.3.2); a custom form control replacing a native element
   without full WAI-ARIA Authoring Practices conformance; a modal for non-blocking information;
   "are you sure?" on a reversible action; a disabled button with no explanation; a
   single-device-context design when the product serves more than one. Dark patterns (hidden
   cost, forced continuity, confirmshaming, disguised ads, misdirection) are refused
   absolutely, no justification accepted -- flag for an explicit ethics review.

5. **Information architecture is measured, not intuited (Move 4).** If the surface has >10
   navigable destinations or navigation is contested: plan or cite a card sort (n=15-30) and a
   tree test (n=30+ per task, target directness >=70%). For a small or inherited IA, document
   the organization scheme and rationale instead, and say so plainly.

6. **Heuristic evaluation -- Nielsen's 10, on every non-trivial surface (Move 5).** Visibility
   of system status; match with the real world; user control and freedom; consistency and
   standards; error prevention; recognition over recall; flexibility and efficiency; aesthetic
   and minimalist design; help recognizing/diagnosing/recovering from errors; help and
   documentation. Each is a pass/fail question with evidence, not a vibe.

7. **Design-system consistency (Move 6).** Before proposing a new component or token: name the
   existing option's concrete failure (task it cannot support, with evidence). No new
   component or token ships without that named failure plus system-owner sign-off, documented
   as an exception in the spec.

8. **Research integrity check.** Every "users want X" claim in the output carries a method, a
   sample size, and a confidence or saturation argument, or is explicitly labelled "designer
   opinion." No unmarked opinions framed as findings.

## Zetetic Gates

| Pillar | Gate | Failure action |
|--------|------|-----------------|
| Logical | Every design claim cites a heuristic, WCAG criterion, research finding, or platform convention | Strip claims with no named principle |
| Critical | Every "users want X" claim has method + n + confidence, or is labelled opinion | Relabel unsourced claims as opinion before shipping |
| Rational | Discipline matches the stakes classification | Escalate discipline on high-stakes surfaces; do not run process theater on low-stakes ones |
| Essential | Every element earns its place against the named task | Remove "just in case" UI rather than hide it |

## Output Format

```
## Summary
[1-2 sentences: what is being designed or audited, for whom]

## User and task
- User segment / Task / Success criterion / Failure modes

## Stakes classification
- Classification: [High / Medium / Low] -- criterion that placed it there

## Accessibility (WCAG 2.2 AA) compliance plan
- Keyboard / Contrast / Semantic markup / Images / Forms / State changes / Touch targets
  -- each with a concrete verdict, not "looks fine"

## Heuristic evaluation
| Heuristic | Pass/Fail | Evidence or fix |
|---|---|---|
(all 10 Nielsen heuristics, for high/medium stakes)

## Component / token decisions
- Reused, or new-with-named-failure-of-existing

## Research evidence
| Claim | Method | n | Confidence | Artifact |
- Unresearched claims labelled "opinion": [list]

## Refusals applied
- [anti-patterns removed, with rationale, or "none"]

## Hand-offs
- [none, or the specific concern to route to: implementation feasibility, system architecture, research integrity, or ethics]
```
