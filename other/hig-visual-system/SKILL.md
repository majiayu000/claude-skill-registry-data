---
name: hig-visual-system
description: "Improve hierarchy, layout, typography, color, materials, icon consistency, and motion in an existing interface while preserving brand and task fit."
---

# Repair the visual system around the task

Follow the [root contract](../../SKILL.md). Reference HIG-003–007 and APPLE-003/007/008 in [Apple rule cards](../../references/apple-rule-cards.md). Read [numeric safeguards](../../references/numeric-and-web-rules.md) before applying dimensions. The token and comparison procedure below is WORKFLOW.

## Baseline the system that already exists

Inspect shared styles, tokens, component variants, fonts, icons, breakpoints or native size adaptation, motion preferences, and theme handling. Capture representative screens under identical conditions before and after changes. Record exceptions that have a legitimate task or platform reason.

Identify what currently communicates hierarchy: placement, grouping, type role, contrast, spacing, size, and persistence. If everything appears equally prominent, do not fix it by making every control smaller. Determine which task, status, and information should lead.

## Establish semantic roles

Map existing values to roles before inventing a new palette or scale. Useful roles include page surface, grouped surface, foreground, secondary foreground, separator, action, selection, danger, warning, positive status, and focus indicator. Their actual values should follow the product and verified target environment.

Record type roles such as page title, section title, body, label, helper, and tabular value. Define wrapping, truncation, and scaling per role. Critical information must not silently disappear into ellipses without an accessible way to obtain it.

Use a coherent spacing system that expresses relationships. There is no requirement in this pack that every value be a multiple of eight. Match the existing geometry when it works; justify exceptions for optical alignment, hit regions, dense data, and native components.

## Layout repair procedure

Start with real content, including long titles and dense states. Group by task or meaning, then align related labels, controls, and values. Remove redundant containers only when the grouping remains understandable. Preserve useful scanning density in administrative and expert interfaces.

Test intermediate window sizes, not only named device presets. At each width or text-size transition, decide whether a group wraps, stacks, collapses, scrolls, or changes navigation presentation. Define the trigger by available space and task requirements rather than user-agent guesses.

Keep primary work and recovery controls reachable when the keyboard, safe-area inset, toolbar, banner, or sticky footer occupies space. Edge-to-edge backgrounds do not authorize placing critical content beneath system obstructions.

## Typography, color, and icon review

Prefer established semantic type roles and appropriately licensed assets. On native Apple surfaces, use platform text-style and scaling behavior where suitable. On the web, retain readable fallback fonts and user zoom; do not distribute Apple font files with a site or assume platform assets are universally licensed.

Measure color pairs in their actual states and backgrounds. Audit selected, hover, pressed, focused, disabled, warning, loading, and error variants. A beautiful palette can still make state distinctions unusable. Do not use color alone to encode critical meaning.

Map icons to concepts, not visual fashion. Keep a concept’s icon and label consistent. Add visible text when an icon’s interpretation is not reliably familiar. Decorative symbols should not create noisy duplicate accessible names.

## Materials and motion

Use the materials card for where Liquid Glass belongs; do not spread blur across all content cards. On the web, treat glass styling as an optional aesthetic, not Apple compliance. Provide a legible fallback for unavailable effects, transparency preferences, and unfavorable backgrounds.

Every proposed animation needs a purpose: explain a transition, connect cause to result, show progress, or support a task. Define interruption, cancellation, and reduced-motion behavior. Do not delay task completion merely to finish an effect or animate the entire page because one value changed.

Measure the actual changed path for rendering and input responsiveness. Set a project-specific performance guardrail from the baseline or existing budget, not an invented universal millisecond limit. Heavy blur, large filters, layout shifts, and needless re-renders need evidence-based evaluation.

## Output and gate

Deliver a semantic token map, changed component variants, responsive rules, preference fallbacks, before/after evidence, and remaining exceptions. A visual-system pass must improve hierarchy or consistency without reducing task visibility, accessibility, content fidelity, or responsiveness.
