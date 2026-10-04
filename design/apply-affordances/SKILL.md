---
name: apply-affordances
description: Use when designing interactive elements — buttons, links, inputs, sliders, drag handles — to ensure visual appearance communicates the available action without requiring instructions or labels.
source: Gibson "The Ecological Approach to Visual Perception" (1979); Norman "The Design of Everyday Things" (Basic Books, 1988/2013); NNG "Affordances and Signifiers" guideline
tags: [affordances, signifiers, interaction-design, ux, usability, visual-cues, ui-patterns]
---

# Apply Affordances

Design interactive elements so their appearance signals how they behave — without instructions, tooltips, or onboarding required.

## Why This Is Best Practice

**Adopted by:** Apple Human Interface Guidelines, Google Material Design, and Microsoft Fluent Design all codify affordance patterns (raised surfaces = pressable, underlines = clickable, cursor changes = draggable) as mandatory standards for their component libraries; IDEO's interaction design curriculum uses Norman's affordance model as the foundational framework
**Impact:** Norman (2013) identifies affordance failures — interactive elements that look decorative, or decorative elements that look interactive — as the primary cause of user errors in digital interfaces; NNG usability studies consistently find that unlabeled affordance violations (flat buttons indistinguishable from text, no hover cursor on clickable areas) account for 15–25% of task failures in unmoderated usability tests
**Why best:** Labels and instructions compensate for missing affordances but require reading; tooltips only appear on hover (unavailable on mobile); affordance-based design communicates function at a glance, in any language, without additional cognitive load — the signifier is the interface

Sources: Gibson "The Ecological Approach to Visual Perception" (Houghton Mifflin, 1979); Norman "The Design of Everyday Things" revised edition (Basic Books, 2013) Ch. 1–2; NNG "Signifiers, Not Affordances" (Norman, 2008)

## Steps

### 1. Identify the action each element affords

For each interactive element, state the affordance explicitly:

| Element | Afforded action |
|---------|----------------|
| Button | Press (triggers an action) |
| Link | Navigate (moves to a destination) |
| Input field | Enter text |
| Checkbox | Toggle on/off |
| Slider | Drag to a value |
| Drag handle | Reorder by dragging |
| Expand arrow | Reveal hidden content |

If you cannot name the afforded action in one word, the element's purpose is ambiguous to users too.

### 2. Apply the correct signifier for each affordance

A **signifier** is the visual property that communicates the affordance. Norman's distinction: the affordance is the capability; the signifier is the perceivable signal of it.

**Press (button):**
- Elevated shadow or border distinguishes from flat text
- Filled background or strong outline separates it from surrounding content
- Cursor: `pointer` on hover
- State: visibly pressed/active on click (slight scale or color shift)

**Navigate (link):**
- Underline or color contrast from body text
- Cursor: `pointer` on hover
- No underline links require color + weight contrast sufficient to distinguish from non-interactive text (WCAG 1.4.1 requires non-color distinction or 3:1 contrast ratio against surrounding text)

**Enter text (input):**
- Visible border or underline indicating a writable area
- Placeholder text inside the field (showing expected format, not repeating the label)
- Focused state with higher-contrast border

**Toggle (checkbox / switch):**
- Checkbox: square with visible boundary; filled when checked
- Toggle switch: pill shape; clearly distinct on/off positions with color + position change
- Never use ambiguous visual metaphors (a circle that could be a radio button or indicator)

**Drag (handle / reorder):**
- Grip dots, lines, or handle icon — not implied by layout alone
- Cursor: `grab` at rest; `grabbing` during drag
- Show affordance on hover, not just on activation

### 3. Check every state is perceptible

Each element must have visually distinct states:

| State | Must be perceivable |
|-------|-------------------|
| Default | The element exists and is interactive |
| Hover | Element responds to pointer |
| Focus | Keyboard focus visible (min 3:1 contrast, WCAG 2.4.11) |
| Active/pressed | Element is being activated |
| Disabled | Element is not interactive (reduced opacity + cursor: `not-allowed`) |
| Loading | Element is processing (spinner inline or disabled state) |

If two states are visually identical, users cannot tell the interface responded.

### 4. Test the blur test

Screenshot the UI and apply a Gaussian blur (5–8px). Any element that was obviously interactive before blur should remain distinguishable from non-interactive content after blur. If buttons, links, and body text look identical when blurred, signifiers are insufficient.

### 5. Test on mobile (no hover state)

Hover-only affordances (tooltip, cursor change) are invisible on touch devices. Every interactive element must be identifiable as interactive without hover:
- Buttons must look tappable without a hover shadow
- Links must be visually distinct from body text without the underline appearing on hover only
- Tap targets must be at minimum 44×44 CSS px (Apple HIG) or 48×48 dp (Google Material)

### 6. Audit for false affordances

Decorative elements that look interactive damage trust:

- Underlined decorative text → users click and nothing happens
- Card with drop shadow → users expect it to be tappable
- Icon without action → users tap and nothing happens

Remove decorative signifiers from non-interactive elements, or add the afforded action.

## Rules

- Every visible interactive element must have a signifier that communicates its action — tooltips and labels are supplements, not substitutes
- Never use color alone to signal interactivity — colorblind users and users on low-quality displays cannot distinguish color-only affordances
- All interactive states (hover, focus, active, disabled) must be visually distinct — identical states break the feedback loop
- Touch targets must be ≥44×44 CSS px — affordance breaks down when the tappable area is too small to activate reliably
- Consistent signifiers across the same component type — if one card is tappable, all cards in the same pattern should look tappable

## Common Mistakes

- **Ghost buttons (outline-only)**: low contrast, especially on colored backgrounds; users frequently miss them as interactive elements — use filled buttons for primary actions
- **Flat design without signifiers**: removing all shadows, borders, and underlines in pursuit of "clean" design leaves users guessing what's interactive; signifiers and minimalism are not opposites
- **Cursor: pointer on non-interactive elements**: using pointer cursor on div containers or decorative images trains users to expect a click that does nothing
- **Disabled state identical to default**: if disabled looks the same as enabled (just grayed text), users don't know why clicks fail; add `cursor: not-allowed` and reduced opacity
- **Affordance only revealed on hover**: critical affordances (the element is tappable) must not require hover to discover; hover should reinforce, not reveal

## When NOT to Use

- When designing for a platform with established component conventions (iOS, Android, Web) — defer to the platform's design system signifiers rather than inventing new ones; users already know what a native button looks like
- When the interactive element is part of a gesture-based or game UI where affordances are taught through onboarding — some interactions (swipe to dismiss, pinch to zoom) have no pre-existing signifier and require deliberate onboarding
