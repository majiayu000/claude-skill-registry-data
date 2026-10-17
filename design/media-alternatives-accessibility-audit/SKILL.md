---
name: media-alternatives-accessibility-audit
description: Audits web interfaces and media assets for accessible alternatives and operable controls across images, icons, SVG, canvas, audio, video, animation, and other time-based media. Use when the user asks to review alt text, decorative treatment, complex-image descriptions, icon names, captions, transcripts, audio description, media players, autoplay, pause, stop, hide, flashing, or canvas and custom-graphic fallbacks against WCAG 2.2.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository, rendered-interface, or supplied-media access. Definitive runtime findings may require media playback, browser accessibility inspection, assistive technology, or flash-analysis tooling.
metadata:
  category: frontend-a11y
  task_type: review
  audience: frontend-developers-content-authors-and-accessibility-reviewers
  tags:
    - accessibility
    - wcag
    - text-alternatives
    - images
    - icons
    - svg
    - canvas
    - captions
    - transcripts
    - audio-description
    - media-controls
    - flashing
  status: draft
  side_effects: none
---

# Media Alternatives Accessibility Audit

## Purpose

Audit whether non-text and time-based media communicates an equivalent purpose and remains controllable for disabled users. Evaluate alternatives from the media's purpose and surrounding context, distinguish what the available evidence can prove, map supported findings to WCAG 2.2, and identify checks that require manual review, media playback, assistive technology, or specialist analysis.

This is a review-only skill. It reports evidence-backed findings and verification work; it does not modify content, certify conformance, or provide legal advice.

## When to use this skill

Use this skill when:

- A site, application, component library, prototype, or content set contains images, icons, SVG, canvas, charts, maps, diagrams, custom graphics, audio, video, animation, or live media.
- The user asks whether alternative text is meaningful, an image is decorative, or a complex visual has an adequate extended description.
- Icon-only controls, custom media players, caption controls, transcripts, audio description, autoplay, or pause, stop, and hide behavior need review.
- Animated, blinking, flashing, scrolling, or auto-updating media may create distraction, vestibular, or seizure risks.
- Source inspection must be combined with a list of playback and manual tests before conclusions are made.
- A broader audit requires media findings in the shared finding contract.

Do not use this skill when:

- The request is a complete cross-domain accessibility audit; use an audit orchestrator and select this skill for its media work package.
- The user only wants new alternative text or captions written without an audit of purpose, context, and implementation.
- The task is to remediate code or media files. This skill may recommend outcomes but does not authorize changes.
- The user requests a legal opinion, certification, or an unqualified WCAG conformance claim.

## Operating rules

- Judge every alternative from the content purpose, nearby text, interaction, destination, task, and repeated use. Never infer quality or decorative status from a filename, asset folder, generated caption, empty `alt`, or element type alone.
- Treat the same asset as potentially informative in one context and decorative in another.
- Distinguish an absent alternative, an exposed-but-empty alternative, an inaccurate alternative, unnecessary duplication, and a technically present but unusable alternative.
- Do not treat a transcript as a substitute for synchronized captions or, at Level AA, for required audio description.
- Do not treat an automated rule, source attribute, caption-track presence, or player-library feature list as proof that the experienced result is correct.
- Map a WCAG criterion only when it applies to the target behavior and the evidence supports the mapping. Keep advisory good-practice findings unmapped when no criterion applies.
- Do not use a WCAG conformance level as severity. Base severity on user impact and task risk.
- Do not expose a tester to suspected flashing content merely to observe it. Prefer metadata review, frame extraction, or an appropriate flash-analysis tool before controlled playback.
- Preserve review-only behavior. Do not edit source, upload tracks, rewrite assets, or change remote systems.

## Inputs to inspect

Start with the smallest set that establishes purpose, implementation, and runtime behavior:

- User goals, target WCAG 2.2 level, in-scope routes or components, supported environments, and critical user tasks.
- Page copy, surrounding labels, captions, links, headings, instructions, figure legends, data tables, and content-authoring guidance.
- HTML, templates, component code, rendered DOM, computed accessibility tree, CSS backgrounds and pseudo-elements, SVG markup, canvas fallback DOM, and custom-graphic implementations.
- Audio, video, animation, poster, thumbnail, subtitle, caption, transcript, described-audio, and alternate-media assets or metadata.
- Player configuration and scripts governing autoplay, mute, volume, playback, seeking, caption selection, audio-description selection, focus, keyboard input, reduced motion, and pause, stop, or hide behavior.
- Representative states including before playback, playing, paused, ended, loading, error, full-screen, picture-in-picture, captions on and off, description on and off, and reduced-motion mode.
- Existing automated results, manual audit notes, media-production specifications, tests, browser support statements, and known third-party limitations.

Do not read or play every asset when a documented representative sample can cover shared templates or player implementations. Always include unique, critical, live, third-party, and high-risk flashing or autoplay patterns in the sample.

## Evidence model

Classify each conclusion by the strongest method actually used.

| Evidence | Can support | Cannot establish alone |
|---|---|---|
| Source or metadata inspection | Alternative attributes, track declarations, fallback markup, player configuration, intended states | Contextual accuracy, rendered accessible name, caption synchronization, playback behavior, assistive-technology experience |
| Static rendered inspection | Visible context, duplicated text, apparent controls, poster and paused states | Audio content, timing, synchronization, changing frames, autoplay behavior, complete keyboard or screen-reader operation |
| Browser accessibility inspection | Computed names, roles, states, descriptions, hidden or duplicated nodes | Whether the wording is equivalent to the media purpose, caption accuracy, transcript completeness, visual content over time |
| Manual context review | Decorative versus informative purpose, alternative relevance, complex-image equivalence, duplication | Runtime behavior not exercised, unprovided audio or frames, behavior in untested environments |
| Media playback | Autoplay, control timing, caption synchronization, audio-description timing, pause or hide behavior, changing visual and audio content | Assistive-technology support unless tested, unplayed segments, other media variants or environments |
| Keyboard or assistive-technology test | Operability and experienced names, roles, states, values, navigation, and fallback access for the tested combination | Universal support across untested browsers, platforms, assistive technologies, or input methods |
| Flash or frame analysis | Flash frequency and threshold evidence for analyzed content and settings | Other variants, responsive crops, overlays, ads, live feeds, or dynamically generated sequences |

Record the target version, page or component state, media segment or timestamp, environment, method, and evidence reference. Use `needs-validation` when stronger evidence is required; do not convert unavailable evidence into a pass.

## Workflow

1. **Frame the audit.**
   - Record the target, requested WCAG 2.2 level, media sample, user tasks, supported environments, available evidence, and exclusions.
   - State that the result is a scoped technical audit, not a conformance determination.
   - Identify third-party, user-generated, live, localized, personalized, or dynamically assembled media because these may require separate sampling and ownership.

2. **Build a media inventory.**
   - Assign a stable target ID to each representative media occurrence or shared implementation.
   - Record the media type, route or component, state, purpose, surrounding context, functional role, live or prerecorded status, synchronized or standalone status, autoplay behavior, duration, available alternatives, controls, and evidence.
   - Inventory CSS images, pseudo-element icons, animated images, embedded players, ads, canvas, WebGL, charts, maps, diagrams, and custom graphics as well as explicit `<img>`, `<svg>`, `<audio>`, and `<video>` elements.
   - Group identical implementations only when their purpose, context, configuration, and alternative remain materially the same.

3. **Determine each non-text item's purpose in context.**
   - Classify the occurrence as decorative, informative, functional, complex, sensory, a test or exercise, or another WCAG 2.2 non-text-content case.
   - Treat an item as decorative only when removing it would lose no information, relationship, mood required by the content, control purpose, or task cue.
   - For a linked image, button image, icon, or control graphic, evaluate the action or destination that needs a name rather than merely describing appearance.
   - Check whether nearby text already provides the same information and whether the alternative would create useful context or redundant noise.
   - Document the contextual evidence for the classification. Do not cite filenames, hashes, stock-photo labels, or empty attributes as the rationale.

4. **Evaluate image and graphic alternatives.**
   - Verify that informative alternatives communicate the equivalent purpose and essential information with wording proportionate to context.
   - Flag alternatives that are inaccurate, generic, keyword-stuffed, filename-derived, unnecessarily prefixed with format descriptions, or duplicated by adjacent text.
   - For images of text, verify both equivalent text access and whether real text could provide the visual presentation unless the image is customizable or essential.
   - For grouped images or composite visuals, evaluate the group meaning and avoid fragmented repetition from every decorative part.
   - For complex charts, maps, diagrams, infographics, and data graphics, require a concise identification or summary plus a discoverable extended description, equivalent data view, or other method that conveys the relationships, trends, values, and conclusions required by the task.

5. **Inspect icons and SVG.**
   - Verify that informative standalone icons expose an appropriate text alternative in their actual context.
   - Verify that icon-only links and buttons have a stable accessible name describing their action or destination.
   - When visible text labels a control, verify that the accessible name contains that visible label.
   - Ensure decorative icons and SVG fragments are excluded from the accessibility tree without hiding meaningful parent content.
   - Inspect the computed accessibility tree rather than requiring one SVG naming technique in every browser. Check for missing names, duplicate title announcements, exposed drawing primitives, and state changes that are not programmatically available.

6. **Evaluate audio and video alternatives.**
   - Classify each asset as prerecorded audio-only, prerecorded video-only, prerecorded synchronized media, live synchronized media, or live audio-only media before selecting requirements.
   - For prerecorded audio-only media, verify an equivalent alternative for time-based media, including relevant speech, speaker identification, and meaningful non-speech audio.
   - For prerecorded video-only media, verify an equivalent time-based alternative or audio track that conveys the meaningful visuals.
   - For prerecorded synchronized media, verify accurate synchronized captions and the applicable audio-description or full-media-alternative requirement.
   - For live synchronized media, verify live captions. Apply live audio-only alternatives when the target includes the relevant Level AAA requirement.
   - Evaluate captions for accuracy, synchronization, speaker identification, and meaningful non-speech information.
   - Evaluate transcripts and full media alternatives for equivalent information, correct sequence, meaningful audio and visual events, and clear association with the media.
   - Evaluate audio description for visual information needed to understand or operate the content, including text shown on screen, speaker or scene changes, demonstrations, and meaningful actions not already conveyed by the main audio.
   - Verify that users can find, identify, and activate each alternative. A correct track that cannot be discovered or selected is not an effective result.

7. **Audit player and media controls.**
   - Test play, pause, stop, replay, mute, volume, seek, playback rate, full-screen, captions, transcript access, audio-description selection, and any other supplied functions.
   - Verify keyboard access, logical focus order, visible and unobscured focus, no keyboard trap, and operation without pointer-only dragging.
   - Verify accessible name, role, state, and value for custom controls, including pressed, selected, muted, current time, duration, volume, and caption or description state where applicable.
   - Check that visible control labels agree with accessible names and that icons, tooltips, color, position, or sound are not the only way to understand a control.
   - Check control contrast and pointer target size when author styling or custom controls place them in scope.
   - Test the actual supported browser and platform. Do not infer native-control accessibility from the element name alone or custom-player support from documentation alone.

8. **Audit autoplay, moving content, and user control.**
   - Record whether audio or visual motion starts without user request, whether audio is initially muted, when controls become available, and whether user preferences are respected.
   - For automatically playing audio lasting more than three seconds, verify a pause or stop mechanism or independent audio-volume control.
   - For moving, blinking, or scrolling content that starts automatically, lasts more than five seconds, and appears alongside other content, verify a pause, stop, or hide mechanism unless the movement is essential.
   - For auto-updating information presented alongside other content, verify pause, stop, hide, or update-frequency control unless the updating is essential.
   - Include animated images, video backgrounds, carousels, progress animations, canvas animation, parallax, and embedded third-party media when applicable.
   - Evaluate reduced-motion behavior and, when Level AAA is in scope, whether non-essential interaction-triggered motion animation can be disabled.

9. **Assess flashing content safely.**
   - Identify flashing risks in animation, video, games, canvas, CSS effects, transitions, ads, embeds, and live or user-generated media.
   - Inspect specifications and files before playback. Use controlled frame or flash analysis when a sequence may exceed three flashes in one second or approach general or red-flash thresholds.
   - Record the analyzed segment, viewport or crop, brightness conditions, overlay state, tool and version, and threshold result.
   - Treat a playback control or warning as insufficient evidence for WCAG 2.2 SC 2.3.1. The content itself must stay within the criterion.
   - Stop and report a coverage gap when safe analysis is unavailable. Do not ask a tester to visually endure suspected hazardous content.

10. **Evaluate canvas and custom-graphic fallbacks.**
    - Verify that meaningful canvas, WebGL, drawing surfaces, custom charts, and other programmatic graphics provide an equivalent accessible representation through fallback DOM, adjacent content, a data view, or another supported method.
    - Confirm that the alternative communicates current information and relationships, not merely that a canvas or chart exists.
    - For interactive graphics, verify accessible names, roles, states, values, keyboard operation, focus behavior, instructions, and an equivalent way to perform the task.
    - Exercise dynamic changes and confirm that the accessible representation stays synchronized with the visual state.
    - Test the accessibility tree and supported assistive technology; source fallback markup alone is not proof that users can reach or use it.

11. **Define and execute the required manual tests.**
    - Mark every test with one or more methods: `manual-context-review`, `rendered-inspection`, `media-playback`, `keyboard`, `assistive-technology`, or `flash-analysis`.
    - Require manual context review for decorative classification, alternative-text meaning, complex-image equivalence, and icon purpose.
    - Require playback for caption accuracy and synchronization, transcript equivalence, audio-description coverage and timing, autoplay, player-state changes, pause or hide behavior, and time-varying content.
    - Require keyboard and assistive-technology testing for custom controls, icon names, SVG exposure, canvas fallbacks, alternative discovery, and state or value announcements.
    - Require specialist flash analysis when source inspection cannot rule out threshold violations.
    - Record setup, environment, timestamps or states, expected result, actual result, and retained evidence for every executed test.

12. **Map applicable WCAG 2.2 criteria.**
    - Use the applicability guide below, then include only criteria supported by the finding's target and evidence.
    - Record the criterion number, name, level, and a short mapping rationale.
    - Apply Level AAA criteria only when the target standard includes AAA or when clearly labeled as advisory beyond the requested level.
    - Do not map ordinary media duration to timing criteria. Map separate time limits or interruptions only when their requirements independently apply.

13. **Normalize and prioritize findings.**
    - Use the shared finding contract in the output format, including every required field.
    - Merge occurrences that share the same target behavior, root cause, user impact, recommendation, and verification method; retain all affected locations.
    - Keep separate findings when similar symptoms have different causes, alternatives, owners, or retest methods.
    - Base severity on affected users, task criticality, breadth, persistence, harm, and workaround quality. Record confidence separately from severity.
    - Separate confirmed findings, provisional source-based findings, tests that need validation, and coverage gaps.

14. **Return the audit.**
    - Summarize user-impact themes before counts.
    - Include the media inventory or sampled coverage, normalized findings, applicable-criteria ledger, manual and playback test matrix, and untested scope.
    - If no issue is found, say that no findings were confirmed in the tested sample and list the evidence and remaining limitations. Do not claim the target passes WCAG.

## WCAG 2.2 applicability guide

Use this guide to select candidate mappings; it does not replace criterion-level analysis.

| WCAG 2.2 criterion | Level | Apply when |
|---|---:|---|
| 1.1.1 Non-text Content | A | Images, icons, SVG, canvas, controls, sensory content, tests, or decoration need equivalent text, a descriptive identification, an accessible name, or an ignorable implementation as applicable. |
| 1.2.1 Audio-only and Video-only (Prerecorded) | A | Prerecorded standalone audio or video-only content needs the specified equivalent alternative or audio track. |
| 1.2.2 Captions (Prerecorded) | A | Prerecorded audio in synchronized media needs captions, subject to the criterion's labeled-media-alternative exception. |
| 1.2.3 Audio Description or Media Alternative (Prerecorded) | A | Prerecorded synchronized media needs audio description or an alternative for time-based media, subject to the criterion's exception. |
| 1.2.4 Captions (Live) | AA | Live audio in synchronized media needs captions. |
| 1.2.5 Audio Description (Prerecorded) | AA | Prerecorded video in synchronized media needs audio description; a transcript alone does not satisfy this criterion. |
| 1.4.2 Audio Control | A | Audio plays automatically for more than three seconds and needs pause, stop, or independent volume control. |
| 2.2.2 Pause, Stop, Hide | A | Applicable moving, blinking, scrolling, or auto-updating content starts automatically and needs user control unless essential. Apply its duration and parallel-presentation conditions exactly. |
| 2.3.1 Three Flashes or Below Threshold | A | Any page content flashes and must stay at three or fewer flashes per second or below the general and red-flash thresholds. |
| 1.3.1 Info and Relationships; 1.3.3 Sensory Characteristics; 1.4.1 Use of Color | A | A graphic or instruction relies on visual or auditory relationships, position, shape, sound, or color that must also be available programmatically or through another cue. |
| 1.4.3 Contrast (Minimum); 1.4.5 Images of Text; 1.4.11 Non-text Contrast | AA | Caption text, images of text, essential graphical objects, or custom player controls trigger the respective visual requirements. |
| 2.1.1 Keyboard; 2.1.2 No Keyboard Trap; 2.1.4 Character Key Shortcuts | A | Author-provided media controls, custom graphics, or shortcuts require keyboard operation, escape, or shortcut control. |
| 2.4.3 Focus Order | A | Focus order within or around a player or interactive graphic affects meaning or operation. |
| 2.4.7 Focus Visible; 2.4.11 Focus Not Obscured (Minimum) | AA | Keyboard focus on media controls or interactive graphics must be visible and not entirely hidden by author-created content. |
| 2.5.1 Pointer Gestures; 2.5.3 Label in Name | A | A media function uses multipoint or path-based gestures, or a visible control label must be included in its accessible name. |
| 2.5.7 Dragging Movements; 2.5.8 Target Size (Minimum) | AA | A custom timeline or media control requires dragging, or author-controlled pointer targets trigger the minimum-size or spacing requirement. |
| 4.1.2 Name, Role, Value | A | Custom media controls, interactive canvas content, SVG controls, or changing states and values must be programmatically available. |
| 1.2.6 Sign Language (Prerecorded); 1.2.7 Extended Audio Description (Prerecorded); 1.2.8 Media Alternative (Prerecorded); 1.2.9 Audio-only (Live) | AAA | The corresponding prerecorded or live media type is present and Level AAA is in scope. |
| 1.3.6 Identify Purpose; 1.4.7 Low or No Background Audio | AAA | Programmatic icon purpose or qualifying prerecorded speech with background audio triggers the criterion and Level AAA is in scope. |
| 2.3.2 Three Flashes; 2.3.3 Animation from Interactions | AAA | Flashing or non-essential interaction-triggered motion animation is present and Level AAA is in scope. |

For time-based media, use SC 1.1.1 to assess descriptive identification where applicable and the relevant SC 1.2.x criterion for the actual alternative. Do not use a generic alt-text finding to hide a missing caption, transcript, full media alternative, or audio description.

## Output format

Return the audit using this structure:

```md
## Summary

- Outcome and main user-impact themes:
- Scope and sample:
- Confirmed findings:
- Findings needing validation:
- Important coverage gaps:
- Conformance disclaimer:

## Scope and evidence

| Target or sample | Media type and purpose | Context and states | Evidence used | Not tested |
|---|---|---|---|---|

## Findings

### MAA-001 — Short finding title

- `id`: MAA-001
- `target`: Route, component, media occurrence, state, role, environment, and timestamp or segment as applicable.
- `evidence`: Evidence type, method, reference, environment, and reproducible observation.
- `user_impact`: Affected users, blocked or impaired task, consequence, and workaround.
- `status`: `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk`.
- `severity`: `critical`, `high`, `medium`, `low`, or `advisory`.
- `confidence`: `high`, `medium`, or `low`, with the reason and missing evidence.
- `framework_mappings`:
  - WCAG 2.2 SC X.X.X Name (Level X) — finding-specific rationale.
- `recommendation`: Outcome-focused remediation guidance, constraints, and responsible surface.
- `verification`: Retest steps, expected result, method, environment, and evidence required to close.
- `source_skill`: `media-alternatives-accessibility-audit`
- `related_ids`: Optional related finding IDs.
- `root_cause`: Optional normalized root cause.

## Media coverage

| Target ID | Type | Purpose in context | Alternative or control | Evidence status | Result |
|---|---|---|---|---|---|

## Manual and playback tests

| Test ID | Target and state or segment | Method | Setup and environment | Expected result | Status and evidence |
|---|---|---|---|---|---|

## Applicable WCAG 2.2 ledger

| Criterion and level | Applicable target | Finding or test IDs | Evidence state | Mapping rationale |
|---|---|---|---|---|

## Coverage gaps and limitations

- Untested assets, segments, states, roles, locales, environments, assistive technologies, live feeds, or third-party content:
- Evidence needed to resolve `needs-validation` items:
```

Omit empty optional finding fields. When no criteria apply to an advisory finding, use an empty `framework_mappings` list and explain the good-practice basis in the recommendation.

## Shared finding contract

Every finding must include:

| Field | Requirement |
|---|---|
| `id` | Stable unique identifier |
| `target` | Route, component, flow, state, role, environment, and occurrence as applicable |
| `evidence` | Evidence type, method, reference, environment, and reproducible observation |
| `user_impact` | Affected users, blocked or impaired task, consequence, and workaround |
| `status` | `confirmed`, `provisional`, `needs-validation`, `not-reproduced`, `resolved`, or `accepted-risk` |
| `severity` | `critical`, `high`, `medium`, `low`, or `advisory`, based on user and task impact |
| `confidence` | `high`, `medium`, or `low`, with the reason and missing evidence |
| `framework_mappings` | Zero or more valid WCAG 2.2 criteria or other requested framework mappings, each with rationale |
| `recommendation` | Outcome-focused remediation guidance, constraints, and responsible surface |
| `verification` | Retest steps, expected result, method, environment, and evidence required to close |

Allow `source_skill`, `related_ids`, and `root_cause` as optional traceability fields. Treat `accepted-risk` as a documented product decision, not an auditor-selected shortcut. Keep severity, confidence, status, and WCAG conformance level distinct.

## Quality bar

The task is complete only when:

- The audit scope, requested WCAG 2.2 level, media sample, evidence, environment, and exclusions are explicit.
- All in-scope image, icon, SVG, canvas, custom-graphic, audio, video, animation, and time-based-media patterns are inventoried or represented by a justified sample.
- Decorative, informative, functional, complex, and sensory purposes are judged from content purpose and surrounding context rather than filename or attribute conventions.
- Informative alternatives, complex descriptions, icon accessible names, captions, transcripts, audio description, and canvas or custom-graphic fallbacks are evaluated when applicable.
- Media controls, autoplay, pause, stop, hide, reduced-motion behavior, and flashing risks are evaluated in the states where they occur.
- Every conclusion states what the available evidence can and cannot establish.
- Tests requiring manual context review, media playback, keyboard, assistive technology, or flash analysis are explicitly identified with setup and expected evidence.
- Every WCAG mapping includes the criterion, level, finding-specific rationale, and sufficient evidence.
- Every finding follows the shared contract and separates user-impact severity from confidence and conformance level.
- Untested media, segments, states, environments, and third-party or live content remain visible as coverage gaps.
- The result avoids remediation side effects, legal conclusions, and unqualified conformance claims.

## Edge cases

- **Same asset in different contexts:** Audit each materially different purpose. Reuse of the file does not guarantee reuse of its alternative.
- **Screenshot or design only:** Review apparent purpose and visible alternatives, but mark semantics, playback, keyboard behavior, synchronization, audio description, and assistive-technology output as not tested.
- **Source only:** Confirm declarative presence and flag evident defects, then create playback, accessibility-tree, keyboard, and assistive-technology tests for runtime claims.
- **Generated alt text, captions, or transcripts:** Treat generation as an input, not validation. Manually review accuracy, context, names, terminology, timing, and meaningful non-speech or visual information.
- **Media alternative for text:** Verify that the media presents no more information than the text and is clearly labeled before applying criterion exceptions.
- **Silent video or animated image:** Do not require captions without audio, but assess video-only alternatives, motion controls, and flashing.
- **Live or changing media:** Sample planned scenarios and retained recordings where possible, document latency and accuracy, and keep unsampled live behavior as a limitation.
- **Third-party embeds or ads:** Distinguish owned remediation from vendor configuration, replacement, wrapping, fallback, procurement, and accepted-risk decisions.
- **User-generated media:** Review the authoring workflow, prompts, preservation of supplied alternatives, and representative published output; do not assume every upload can be audited individually.
- **Native media controls:** Test supported browser and platform combinations. User-agent controls may differ and author styling can introduce new failures.
- **Dynamic canvas or custom graphics:** Verify that the accessible representation updates with visual state and that interactive tasks remain equivalent.
- **Complex data visualizations:** A raw data dump may not communicate the relationships or conclusion the visual was designed to show; judge task equivalence.
- **Essential motion or animation claims:** Require a documented, narrow rationale. Do not accept branding or preference as proof of essentiality.
- **Suspected flashing:** Do not rely on visual endurance, warnings, or pause controls. Use safe analysis or report the unresolved risk.
- **Localized media:** Sample translated alternatives, caption language, reading order, speaker labels, audio-description tracks, and the discoverability of language selection.

## Related skills

- `inclusive-interface-audit-orchestrator`
- `accessibility-validation-planner`
- `motion-behavior-planner`
- `interface-state-coverage-review`
