---
name: hig-accessibility
description: "Audit and repair interaction and information barriers using Apple accessibility guidance and explicitly distinguished web standards."
---

# Treat accessibility as task completion

Follow the [root contract](../../SKILL.md). Read [numeric-and-web-rules.md](../../references/numeric-and-web-rules.md) before citing thresholds. HIG-002 informs native Apple adaptation; WEB-001–009 cover selected web criteria and patterns. This is a practical audit workflow, not a complete conformance evaluation.

## Establish the test scope

Record platform, browser/app version, assistive technology, input method, content state, zoom/text setting, and role. Identify complete tasks rather than checking isolated components only. Include a representative creation/editing flow, navigation/search, and one error recovery path when present.

For native Apple apps, inspect accessibility labels, traits, values, grouping, reading order, actions, text scaling, and supported system preferences. For web products, inspect semantic HTML, accessible names, roles, states, relationships, and input behavior. Prefer a correct native element before adding ARIA.

## Keyboard and focus

Complete the task without a pointer. Verify logical focus order, visible focus, entry/exit from overlays, shortcuts, and escape paths. Check that sticky UI does not hide the focused control. Check nested scrolling, virtualized content, and route transitions that can strand focus.

Test complex controls against their actual pattern. Arrow keys within tabs or listboxes are not interchangeable with tabbing through a set of ordinary page links. Do not assign a widget role without implementing its required interaction behavior.

## Screen reader and meaning

Navigate by headings, landmarks, fields, buttons, links, and relevant native groupings. Read the accessible name and state of each changed control. Check duplicate names, unlabeled icon buttons, decorative noise, incorrect required/invalid states, and visual instructions with no programmatic relationship.

Trigger asynchronous progress, success, validation, and failures. Ensure meaningful updates can be discovered without moving focus unnecessarily or announcing every keystroke. A live region is not an excuse to repeatedly read an entire page.

Check that visual order and reading order remain compatible after responsive changes. A canvas or 3D scene needs a usable alternate route to essential controls and information; a one-sentence alt label for a complex interactive task is not automatically sufficient.

## Vision and perception

Test enlarged text and web zoom independently where relevant. Check wrapping, truncation, control labels, form errors, and completion actions. Compare all necessary foreground/background pairs, not only the default theme.

Test meaning without color cues. Confirm that selection, errors, and chart series have adequate non-color distinctions. Review light/dark appearance, increased contrast, reduced transparency, and forced-color behavior when supported and applicable. Do not invent a universal browser API for every native setting.

Check captions, transcripts, and visual alternatives for meaningful audio; check non-audio access to essential alerts. Review motion-heavy interactions for a reduced-motion alternative that retains the information and completion path.

## Motor, cognitive, and authentication barriers

Measure the actual activated region and neighboring targets, not only the visible icon. Provide alternatives to gesture-only, drag-only, timed, or precision-dependent actions when the task permits. Avoid accidental activation during scrolling and destructive neighboring controls.

Identify unexplained abbreviations, shifting layouts, inconsistent labels, vanished instructions, excessive recall, and unexplained timeouts. Preserve useful context and allow correction. Do not claim to diagnose or simulate a disability with a checklist.

Check sign-in with password managers, paste, alternative verification methods, and assistive input. Use the exact web authentication criterion when assessing compliance; avoid a blanket claim that every CAPTCHA or memory task is prohibited in every context.

## Evidence and reporting

Separate automated scan results, DOM/accessibility-tree inspection, manual keyboard testing, actual assistive-technology testing, and user research. Report each method honestly. If no screen reader or native device is available, provide the manual test and mark it unrun.

Prioritize an access blocker by its effect on the affected user group, not its prevalence in a general sample. Track criteria, exceptions, and test conditions in [verification.md](../../templates/verification.md). Never claim complete WCAG conformance from this subset or from a passing scanner.

## Completion gate

A changed task is verified only within the documented methods and conditions. Remaining untested combinations stay visible. Require no newly introduced blocker, meaningful semantics, operable focus, understandable recovery, and readable content under the tested adaptations.
