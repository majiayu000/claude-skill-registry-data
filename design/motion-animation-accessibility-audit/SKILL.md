---
name: motion-animation-accessibility-audit
description: Audits web-interface motion and time-based behavior for accessibility barriers, including prefers-reduced-motion, CSS and JavaScript animation, transitions, scrolling effects, autoplay, carousels, parallax, GSAP timelines, flashing, pause controls, and motion-triggered interaction. Use when a user asks to review animation accessibility, reduced-motion behavior, vestibular risk, scroll-jacking, autoplay, flashing, motion controls, or WCAG 2.2 motion and timing concerns without requesting implementation changes.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository or artifact access; a running interface is required to confirm runtime behavior.
metadata:
  category: frontend-a11y
  task_type: review
  audience: accessibility-auditors-frontend-developers-and-designers
  tags:
    - accessibility
    - wcag
    - motion
    - animation
    - reduced-motion
    - autoplay
    - flashing
    - carousels
    - scroll-behavior
  status: draft
  side_effects: none
---

# Motion and Animation Accessibility Audit

## Purpose

Audit motion, animation, and time-based interface behavior for barriers to operating, reading, orienting, and remaining comfortable in an interface. Produce evidence-bounded findings that keep WCAG failures distinct from broader comfort and usability recommendations.

This skill is independently usable. When an audit orchestrator provides scope, target IDs, evidence, severity rules, exclusions, or a finding contract, preserve those inputs and return compatible specialist findings rather than replanning the entire audit.

## When to use this skill

Use this skill when:

- The user wants a review of CSS animations, transitions, JavaScript animation, GSAP timelines, or motion-library behavior.
- A site or application contains autoplay, carousels, tickers, parallax, scroll-linked effects, smooth scrolling, scroll-jacking, flashing, or automatic updates.
- The user needs reduced-motion, vestibular-risk, pause-control, reading-disruption, or motion-triggered-interaction coverage.
- Source, prototypes, videos, screenshots, a running build, or existing audit evidence needs a focused motion and timing pass.

Do not use this skill when:

- The request is to design or implement an animation system; use a motion-planning or implementation workflow.
- The primary concern is captions, transcripts, audio description, or text alternatives for media; use a media-alternatives specialist.
- The request is for legal advice, certification, or a complete WCAG conformance determination.
- No interface, source, recording, or other behavior evidence is available to inspect.

## Operating rules

- Review only. Do not modify source, settings, timelines, or production controls.
- Do not claim complete WCAG conformance or infer a pass from absent evidence.
- Treat the requested WCAG version and conformance level as authoritative. If none is supplied, use WCAG 2.2 as a mapping reference and label Level AAA criteria as advisory unless they are in scope.
- Do not equate a preference query, motion-library option, or duration value with accessibility. Confirm observable behavior and fallback.
- Separate applicable WCAG findings from vestibular comfort, attention, readability, predictability, and product-quality recommendations that lack a supported success-criterion failure.
- Map a criterion only when its normative conditions, exceptions, scope, and evidence fit the observed behavior.
- Base severity on user impact, task criticality, breadth, persistence, and workaround quality; never on WCAG level.

## Inputs to inspect

Start with the smallest evidence set that represents important tasks and motion patterns:

- Audit brief; in-scope routes, components, flows, roles, devices, browsers, locales, motion preferences; and target WCAG version and level.
- Shared CSS, keyframes, transitions, custom properties, design tokens, utility classes, and component styles.
- JavaScript and TypeScript event handlers, requestAnimationFrame loops, timers, Web Animations API calls, GSAP timelines, motion-library configuration, IntersectionObserver use, and scroll handlers.
- Carousel, ticker, modal, disclosure, toast, loading, navigation, drag, gesture, parallax, canvas, SVG, video, and autoplay implementations.
- Existing tests, stories, feature flags, browser-support notes, and no-JavaScript or failure-state behavior.
- Running routes and representative states, plus recordings, prototypes, screenshots, user research, support themes, and prior audit findings when available.

Do not read an entire repository when shared motion utilities, representative components, route entry points, and high-risk flows establish the relevant patterns.

## Evidence model

| Evidence | Can establish | Cannot establish alone |
|---|---|---|
| Source inspection | Declared animations, preference branches, control wiring, event paths, likely fallback logic, and test coverage | Actual rendering, timing, interruption, browser preference handling, user operability, or flash rate |
| Screenshot or recording | Visible motion concept, captured controls, apparent parallax, and a sampled sequence | Whether controls work, sequence repetition, exact flash thresholds, focus behavior, or reduced-motion behavior |
| Prototype | Intended triggers, sequencing, and design alternatives | Production timing, browser behavior, JavaScript failure behavior, and reliable keyboard or touch operation |
| Running interface | Reproducible start, stop, pause, resume, reduced-motion, focus, reading, scroll, and fallback behavior in the tested environment | Untested routes, settings, devices, data, roles, or browsers |
| Automated scan or static search | Candidate motion code and repeatable configuration checks | Vestibular impact, animation meaning, threshold compliance, user control, or complete WCAG coverage |
| Flash analysis | Measured luminance, area, and flash characteristics for sampled output | A complete product assessment or behavior outside the sampled asset and state |

Use direct evidence for confirmed findings. Use provisional for persuasive but incomplete evidence and needs-validation when a stronger method, state, device, or measurement is required.

## Source-inspection requirements

1. Inventory every source of motion: CSS animation and transition declarations; JavaScript, Web Animations API, GSAP, and motion-library timelines; media and canvas; browser-scroll calls; timers; and third-party embeds.
2. Trace each trigger: load, viewport entry, pointer, keyboard, touch, scroll, device motion, data update, timeout, navigation, or a chained animation completion.
3. Check whether reduced-motion handling reaches every high-risk path, including dynamically mounted content, inline styles, timeline configuration, and third-party integrations.
4. Find automatic loops, autoplay, interval-driven updates, repeat or yoyo settings, and code that restarts movement after a user pauses or hides it.
5. Inspect controls and their state: visible label, keyboard reachability, programmatic name, pause or resume state, persistence, and whether the control affects the actual moving content.
6. Check whether focus, announcements, reading order, actionable state, or task completion waits on an animation event or fixed timeout.
7. Inspect scroll interception, wheel or touch handlers, scroll snapping, smooth-scroll overrides, body locking, and route-transition code for scroll-jacking or loss of native expectations.
8. Review progressive enhancement: essential content, controls, and task outcomes must remain available if JavaScript, a library, a network resource, or an animation callback fails.

Static inspection can identify candidates and code-evident defects. It cannot substitute for the runtime tests below.

## Runtime-test requirements

Exercise representative critical and motion-heavy flows in a running interface. Record browser, operating system, preference state, viewport, input method, route, component state, and test data.

1. Test the default experience, then enable the platform reduced-motion preference before loading the page and while the interface is active.
2. Test automatic start, pause, stop, hide, resume, reset, dismissal, navigation, and repeated triggers with pointer, keyboard, and touch when applicable.
3. Test loading, error, empty, slow-network, partial-data, cancellation, background or tab-return, route-change, and repeated-interaction states that can restart or interrupt motion.
4. Verify focus movement, visible focus, reading position, selection, text entry, and screen-reader-relevant state are not delayed, concealed, moved, or reset by animation.
5. Test browser zoom and responsive layouts where scroll-linked effects, pinned sections, carousels, or animation containers can clip content, trap scroll, or hide controls.
6. Disable JavaScript where practical, block the motion dependency, or simulate its failure. Verify essential content, controls, navigation, and a non-motion state remain usable.
7. For suspected flashing, record or measure rendered output with an appropriate method; do not estimate compliance from code review or visual impression.

## Audit coverage

| Area | Inspect for |
|---|---|
| Reduced motion | A complete and effective prefers-reduced-motion response; no large, unexpected, or repeated movement remains when a non-motion or lower-motion alternative can preserve purpose |
| Essential versus decorative motion | A documented purpose for motion that communicates orientation, state, causality, feedback, or progress; a non-motion cue when movement carries information; removal or suppression of purely decorative movement |
| Interaction-triggered motion | Hover, focus, press, drag, gesture, device-motion, and scroll-triggered animation that can be avoided, canceled, reversed, or completed without forcing movement or precise input |
| Autoplay and controls | Automatically moving, blinking, scrolling, or updating content has an effective pause, stop, or hide mechanism where WCAG requires it; audio autoplay is reviewed separately from visual motion |
| Carousels and tickers | Manual navigation, keyboard operation, current-item exposure, stable focus, non-restarting pause, no forced advance, and a readable static or user-controlled state |
| Parallax and scroll effects | Reduced-motion alternatives, no large forced spatial movement, no loss of orientation, no scroll interception that blocks expected navigation, and no essential information tied only to scroll position |
| GSAP and timelines | Preference-aware initialization, cancel or cleanup behavior, no timeline-gated meaning, no unbounded loops, and a safe final state after interruption or failed callbacks |
| Flashing | Flashes, red flashes, rapid luminance changes, large-area effects, video, canvas, SVG, and third-party embeds against the relevant threshold and safety guidance |
| Focus and reading disruption | Animation that shifts focus, resets scroll, overlays text, changes line position, removes a target before it can be used, advances content, or makes reading depend on timing |
| Time-sensitive transitions | Animations or exit delays that block a next action, discard input, hide a status, expire a control, or create an avoidable time limit; a stable final state and adequate completion path |
| Meaning and fallback | Motion is not the sole cue for state, progress, relationship, urgency, success, or error; non-motion feedback works with scripts disabled or failed |

## Workflow

1. **Confirm scope and evidence.**
   - Record the target, critical tasks, routes, components, patterns, supported environments, known motion preferences, and requested standards.
   - Preserve orchestrator-provided target IDs, exclusions, severity rules, and shared finding contract.
   - State unverified conditions rather than assuming a platform, browser, or user setting.

2. **Build a motion inventory.**
   - List every motion source, target, trigger, start and end condition, repetition rule, purpose, affected task, control, and fallback.
   - Group reused primitives separately from one-off motion. Expand the sample when the same library or utility is configured differently.

3. **Inspect source and configuration.**
   - Complete the source-inspection requirements and identify testable hypotheses.
   - Trace preference branches and third-party boundaries instead of accepting a global reduced-motion rule as sufficient evidence.

4. **Classify purpose and dependency.**
   - Mark each motion as essential to the task, functional but replaceable, decorative, or unknown.
   - For essential or functional movement, identify an equivalent non-motion cue and a stable completion state.
   - Do not accept motion as the only way to understand state, locate content, or operate the task.

5. **Test reduced-motion and interruption behavior.**
   - Run the same task with default and reduced-motion settings.
   - Test interruption by repeated input, reversal, route change, resize, focus change, backgrounding, slow loading, and cancellation.
   - Confirm preferences are honored for initial and dynamically created content, and controls do not silently restart movement.

6. **Test automatic motion, autoplay, and reading conditions.**
   - Let each automatic sequence run long enough to observe loops, restart rules, expiration, and adjacent-content disruption.
   - Verify pause, stop, or hide controls where applicable: keyboard access, state feedback, scope, persistence, and whether interaction accidentally resumes autoplay.
   - Test reading, selecting, entering text, navigating by keyboard, and returning after interruption.

7. **Test scrolling, carousels, and motion input.**
   - Verify native scrolling, browser navigation, keyboard scrolling, touch, zoom, and focus anchors are not overridden without an accessible alternative.
   - Test carousel controls, current-item feedback when relevant, and first or last-item behavior.
   - Test device-motion or gesture triggers for an alternative input method and a way to avoid accidental activation where required.

8. **Assess flashing and time limits.**
   - Identify sequences that may exceed flash thresholds, especially large, high-contrast, red, full-screen, or repeated effects.
   - Obtain a rendered measurement or classify as needs-validation. Account for supplied WCAG scope and relevant exceptions.
   - Distinguish a visual transition from an actual task time limit, then verify warnings, extensions, cancellation, and preserved progress where applicable.

9. **Test resilience and fallback.**
   - Test no-JavaScript or failed-dependency behavior where practical.
   - Verify content and functions animation reveals, advances, or completes remain available in a stable state without the motion code.
   - Record only failures demonstrated by the tested fallback; mark other environments for validation.

10. **Classify and normalize findings.**
    - Use Applicable WCAG findings only when evidence supports a criterion in the named scope.
    - Use Comfort and usability recommendations for vestibular risk, distraction, timing friction, or predictability concerns without a supported WCAG failure.
    - Use Needs validation for unmeasured flashes, untested preferences, third-party behavior, and source-only hypotheses.
    - Merge observations with the same target behavior, root cause, user impact, and verification method.

11. **Define remediation outcomes and retests.**
    - Recommend outcomes such as honoring the preference, providing a stable alternative, preserving a readable state, exposing an operable control, or avoiding animation-dependent meaning.
    - Do not prescribe a particular duration, library, or animation technique unless the evidence requires it.
    - Provide reproducible retests in the relevant environment and preference state.

## WCAG mapping boundary

Use the requested WCAG version as authoritative. These WCAG 2.2 criteria are common candidates, not automatic mappings:

| Concern | Candidate criteria | Mapping boundary |
|---|---|---|
| Automatically moving, blinking, scrolling, or auto-updating content | 2.2.2 Pause, Stop, Hide | Confirm duration, automatic start, parallel presentation, user control, scope, and exceptions; visual busyness alone is not a failure |
| Flashing content | 2.3.1 Three Flashes or Below Threshold | Measure rendered output and assess thresholds and exceptions; do not report a suspected flash from source or a still image as confirmed |
| Animation triggered by interaction | 2.3.3 Animation from Interactions, Level AAA | Reduced-motion support is good practice at all levels, but this criterion is an in-scope failure only when Level AAA applies and motion is non-essential |
| Time limits or forced waiting that impairs completion | 2.2.1 Timing Adjustable; 2.2.3 No Timing, Level AAA | A brief visual transition is not automatically a time limit; verify normative conditions, exceptions, and task consequence |
| Auto-playing audio | 1.4.2 Audio Control | Apply when audio plays automatically for more than three seconds and meets criterion conditions; coordinate with media review |
| Device-motion activation | 2.5.4 Motion Actuation | Apply only when motion-actuation functionality lacks an alternative or a way to disable accidental activation, subject to the criterion conditions |
| Scroll-jacking, gesture-only controls, or blocked keyboard operation | 2.1.1 Keyboard; 2.5.1 Pointer Gestures; 2.5.2 Pointer Cancellation; 2.4.3 Focus Order | Map the demonstrated operability, cancellation, or focus defect, not the use of a scroll library itself |
| Motion-only state or relationship meaning | 1.3.1 Info and Relationships; 1.3.3 Sensory Characteristics; 4.1.2 Name, Role, Value; other applicable criteria | Identify missing programmatic or non-sensory information; movement alone does not determine the criterion |
| Unexpected movement on focus or input | 3.2.1 On Focus; 3.2.2 On Input | Confirm an unexpected change of context under the criterion, not merely a visible transition |

Prefers-reduced-motion is not itself a WCAG success criterion. It is a critical implementation mechanism and a strong indicator for evaluating motion from interactions and broader comfort risks. Keep vestibular, migraine, attention, and reading-disruption concerns visible even when no WCAG mapping applies.

## Finding contract

Give every finding a stable ID and include:

| Field | Requirement |
|---|---|
| id | Stable unique identifier such as MAA-001 |
| classification | applicable-wcag, comfort-usability-recommendation, or needs-validation |
| target | Route, component, flow, state, preference setting, input method, browser, and environment as applicable |
| affected_task | The task and exact point where motion blocks, disorients, delays, distracts, or creates risk |
| evidence | Evidence type, method, reference, environment, and reproducible observation |
| user_impact | Affected functional needs, consequence, breadth, persistence, and available workaround |
| status | confirmed, provisional, needs-validation, not-reproduced, resolved, or accepted-risk |
| severity | critical, high, medium, low, or advisory, based on user and task impact |
| confidence | high, medium, or low, with the reason and missing evidence |
| framework_mappings | Supported WCAG criteria with version, level, and rationale; empty when no supported mapping exists |
| recommendation | Outcome-focused remediation guidance, constraints, and responsible surface |
| verification | Retest steps, expected result, method, environment, preference state, and evidence needed to close |

Optional fields are source_skill, related_ids, and root_cause. Set source_skill to motion-animation-accessibility-audit when the surrounding contract permits it.

## Output format

Return:

~~~md
## Audit summary

- Target and in-scope tasks:
- Evidence reviewed:
- Environments and preference states tested:
- WCAG version and level:
- Coverage limitations:
- Conformance disclaimer:

## Applicable WCAG findings

### MAA-001 — Finding title

- Classification:
- Target:
- Affected task:
- Evidence:
- User impact:
- Status:
- Severity:
- Confidence:
- Framework mappings:
- Recommendation:
- Verification:

## Comfort and usability recommendations

[Repeat the complete finding structure. Keep framework mappings empty unless noting an explicitly out-of-scope advisory.]

## Needs validation

[Repeat the complete finding structure and state the missing runtime, preference, device, or measurement evidence.]

## Coverage and verified strengths

- Motion inventory:
- Verified strengths:
- Untested routes, states, inputs, environments, and preference conditions:
- Recommended next evidence:
~~~

Omit empty finding sections, but never omit coverage limitations. Report strengths only when directly verified; do not treat them as a conformance statement.

## Quality bar

The task is complete only when:

- Every requested motion type was tested, ruled out as not applicable, or listed as not verifiable.
- Source inspection identifies actual animation and control paths rather than relying only on visual observation.
- Runtime tests cover default and reduced-motion settings, interruption, automatic start and restart, controls, focus and reading, scrolling, and a relevant fallback path.
- Flashing is measured or explicitly marked as needing measurement.
- Every finding has evidence, task impact, outcome-focused recommendation, and reproducible verification.
- WCAG failures remain separate from comfort and usability recommendations.
- WCAG mappings are criterion-specific, evidence-supported, scoped to the requested version and level, and never imply whole-product conformance.
- Severity, confidence, status, and WCAG level remain distinct.
- Shared root causes are deduplicated, and coverage gaps are explicit.
- No source or configuration was modified during the review.

## Edge cases

- **Screenshot or recording only:** Review visible motion concepts and apparent controls, but mark reduced-motion behavior, control operation, focus, restart rules, scrolling, fallback, and thresholds as not verifiable.
- **Source only:** Report static evidence and required runtime checks. Do not claim a media query, library option, or test name proves the rendered experience.
- **Third-party embed or iframe:** Separate owned controls and integration configuration from vendor behavior. Test with the actual embed when possible and state the remediation boundary.
- **Animations used for loading:** Distinguish optional progress feedback from an actual time limit. Preserve a stable status and a usable error or retry path.
- **Essential safety or spatial motion:** Do not remove essential meaning; provide an equivalent non-motion cue and a stable final state.
- **Reduced motion still uses fades:** Evaluate opacity, flashing, repeated change, and reading interference independently. Less movement is not automatically a safe or sufficient alternative.
- **Virtualized, infinite, or scroll-driven content:** Test whether position, focus, reading, loading, and back navigation remain predictable as content enters or leaves the viewport.
- **No-JavaScript fallback unavailable:** State the environment limit and inspect progressive-enhancement evidence; do not invent a fallback result.

## Related skills

- accessibility-validation-planner
- inclusive-interface-audit-orchestrator
- keyboard-focus-accessibility-audit
- media-alternatives-accessibility-audit
- dynamic-interface-accessibility-audit
- visual-responsive-accessibility-audit
- motion-behavior-planner
