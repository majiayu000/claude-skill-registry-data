---
name: interaction-design
description: >
  Apply interaction design (IxD) principles and frameworks to product and service design work.
  Use this skill when designing or evaluating interaction flows, micro-interactions, feedback
  mechanisms, affordances, mental models, component states, response time, animation and
  transitions, error recovery, input validation, task flows, or navigation patterns.
  Core audiences: product designers, UX designers, UI designers, service designers, and
  interaction designers working on digital products and services.
  Trigger on: interaction flow, micro-interaction, affordance, feedback design, state design
  (hover/focus/error/loading/empty), response time, transition, animation, mental model,
  task flow, user flow, navigation design, interaction spec, handoff annotation, gesture,
  input validation, error state, loading state, empty state, system feedback, signifier,
  design review, interaction audit, IxD principles.
metadata:
  version: 1.0.0
---

# Interaction Design

A practitioner's guide to interaction design for product designers, UX designers, UI designers,
service designers, and interaction designers. This skill covers the full scope of IxD work —
from foundational principles to practical state design, flow specification, and interaction review.

## What This Skill Covers

- Designing and specifying interactions: flows, states, transitions, affordances
- Evaluating interaction quality against established principles
- Writing interaction specifications and handoff annotations
- Micro-interaction design (trigger, rules, feedback, loops)
- Feedback system design: timing, type, and hierarchy
- Response time standards and perceived performance
- Role-specific IxD responsibilities across design disciplines
- Common interaction anti-patterns and how to fix them

Tell Claude what you need. Examples:

- "Help me design the interaction flow for a multi-step checkout"
- "What states does this button need?"
- "Review this interaction — does the feedback arrive at the right time?"
- "I need to write an interaction spec for this drag-and-drop feature"
- "What's the right animation duration for this modal?"
- "How should I handle empty states in this dashboard?"

---

## The 5 Dimensions of Interaction Design

Interaction design operates across five materials. Every interaction is composed of some combination of these dimensions.

| Dimension | What It Is | Design Questions |
|---|---|---|
| **Words** | Labels, instructions, microcopy, error messages, button text | Is the language clear and action-oriented? Does it set accurate expectations? |
| **Visual representations** | Icons, images, typography, color, data visualizations | Does the visual communicate the interaction affordance clearly? |
| **Physical objects/space** | Device type, screen size, input modality (touch/mouse/voice/keyboard), physical environment | Is the interaction designed for the right input modality and context of use? |
| **Time** | Duration of transitions, animation timing, response latency, sequences | Does timing feel responsive and purposeful? Does it communicate state change? |
| **Behaviour** | System responses to user actions — what the product does, how it reacts | Does the system behaviour match the user's mental model and stated intent? |

When designing an interaction, identify which dimensions are in play. Most interaction failures
are dimension mismatches — a system behaviour that contradicts the visual affordance, or
microcopy that does not match what actually happens.

---

## Core Principles

### Norman's 6 Fundamentals

Norman's 6 fundamentals remain the most widely applicable framework for interaction quality.

**Visibility**
Make the state of the system and available actions visible. Users should not have to guess
what the system is doing or what they can do next.

- Visible current state (selected, loading, active, error)
- Visible affordances (interactive elements look interactive)
- Visible navigation and location within the product

❌ A form that submits silently with no loading state
✅ A submit button that transitions to a spinner immediately on click

**Feedback**
Every action should produce an immediate, perceivable response. The system must communicate
that it received the user's input and what it did with it.

- Immediate acknowledgment (within 100ms — before processing completes)
- Clear outcome communication (success, failure, in-progress)
- Feedback proportional to action significance

❌ A delete action with no confirmation, animation, or acknowledgment
✅ A delete action that shows an undo toast immediately, then fades the item out

**Constraints**
Limit available actions to only those that are valid in context. Prevent errors rather than
recovering from them.

- Disable invalid actions rather than showing errors after attempting them
- Use progressive disclosure to surface only relevant controls
- Form fields that only accept valid input types

❌ Allowing date entry as free text, then showing "invalid date" on submit
✅ Using a date picker that constrains selection to valid dates only

**Mapping**
The relationship between controls and their effects should be intuitive. Controls should
spatially or conceptually relate to what they affect.

- Scroll up → content moves up (natural mapping)
- Volume slider increases left-to-right
- A "Next" button is on the right; "Back" is on the left

❌ A brightness control labeled only with an icon that looks like contrast
✅ A slider labeled "Brightness" that increases in the direction of "more light"

**Consistency**
Similar actions should work similarly throughout the product. Users build mental models
from patterns — breaking them causes errors and confusion.

- Internal consistency: same component behaves the same way everywhere
- External consistency: aligns with platform conventions users already know
- Consistency across breakpoints and platforms

❌ Swipe-to-dismiss works in one list but not another
✅ Every destructive action uses the same confirmation pattern

**Affordance**
UI elements should look like they behave. The appearance of a component should signal
how to interact with it.

- Buttons look pressable
- Draggable elements have visible drag handles or respond to hover with a cursor change
- Tappable items have sufficient size and visual weight

❌ Flat text that is actually a link but looks identical to static body text
✅ Links are underlined or use a distinct color that is never applied to non-interactive text

---

### Tognazzini's 19 Principles

The 19 principles cover the broader system of human-computer interaction.
These are applied principles for practitioners.

**Anticipation**
Bring information and tools to users before they need to search for them. Design ahead
of the user's next step.

- Surface related actions contextually
- Pre-fill known data (shipping address from account)
- Warn before a destructive point in a flow

**Autonomy**
Users need to feel in control. The system should operate within constraints the user
understands and can override.

- Allow customization of defaults
- Never take irreversible action without explicit confirmation
- Show system state transparently so users know what is happening

**Consistency**
Maintain consistency at four levels: within the product, across the platform, across
industry conventions, and with user expectations. When in doubt, consistency with user
expectations matters most.

**Defaults**
Defaults should represent the best choice for most users in most situations. Make them
easy to override, clearly labeled, and meaningful — not just the safest technical choice.

- Smart defaults reduce friction for common cases
- Default selections should be clearly indicated
- Avoid jargon in default labels

**Discoverability**
If users cannot find a feature, it does not exist for them. Controls should be visible
and accessible without requiring prior knowledge.

- Navigation should expose primary paths without instruction
- Features should be discoverable through exploration, not manuals
- Progressive disclosure for advanced features, not hidden features

**Efficiency of the User**
Optimize for the user's time, not the system's. Common tasks should be fast. Expert
users should have shortcuts. The most-used path should be the shortest path.

- Keyboard shortcuts for frequent actions
- Bulk actions for repeat operations
- Single-click for primary actions (not multi-step confirmation for common tasks)

**Explorable Interfaces**
Users should be able to explore without fear. Reversible actions allow experimentation.

- Undo for all destructive actions
- Preview before committing (image crop, document format)
- Breadcrumbs and clear back navigation

**Fitts's Law**
Time to acquire a target = f(distance, size). Larger targets and shorter distances reduce
interaction time and error.

- Touch targets: minimum 44×44px (iOS/Android), 48×48px (Material)
- Mouse targets: minimum 32×32px
- Primary CTAs should be the largest interactive element in the area
- Place related actions close together
- Use screen edges and corners — they are infinite targets in one direction

**Latency Reduction**
Respond to input within 100ms. If processing takes longer, acknowledge the action
immediately and show progress.

- 0–100ms: no feedback needed beyond visual state change
- 100ms–1s: show a loading indicator (spinner or skeleton)
- 1s–10s: show a progress indicator with estimated completion
- 10s+: allow background processing, notify on completion

**Learnability**
Interfaces should be learnable over time, not just usable on first contact. Expert usage
should be faster than novice usage.

- Reveal progressive complexity as users gain experience
- Tooltips and inline guidance for non-obvious features
- Don't optimize only for first-time use

**Metaphors**
Use metaphors that accurately convey what a system does. Abandon them when they constrain
or mislead.

- A "trash" icon affords deletion and recovery
- A "folder" affords organization and nesting
- Avoid metaphors that imply constraints that do not exist

**Protect the User's Work**
Never destroy data due to interface errors or unexpected user behavior. Auto-save
continuously, provide undo, and confirm before overwriting.

- Auto-save drafts
- Warn before navigating away from unsaved state
- Never clear a form on validation failure

**Readability**
Text must be legible for your full user population, not just ideal conditions.

- Minimum 16px body text for web
- 4.5:1 contrast ratio minimum (WCAG AA)
- Line length 50–75 characters for prose
- Test with users over 50 and in bright light conditions

**Simplicity**
Simple is not the same as minimal. Simplicity means reducing unnecessary complexity
while preserving all functionality users need.

- Use progressive disclosure, not feature removal
- Avoid false simplicity that hides necessary controls
- Every element on screen should earn its place

**State**
Track where users are and what they have done. Restore state across sessions.

- Remember scroll position, form progress, open panels
- Clearly indicate current location (breadcrumbs, active nav item)
- Distinguish between new and visited content

**Visible Navigation**
Users should always know where they are, where they can go, and how to get back.

- Highlight active location in navigation
- Breadcrumbs for deep hierarchies
- Back button behavior should match expectations (browser and native)
- Never trap users in a flow without an obvious exit

**Aesthetics**
Visual design affects perceived usability. A polished interface is trusted more.

- Aesthetic quality is not decoration — it signals care and quality
- Never let aesthetic trends degrade usability
- Test visual changes for their effect on task performance

**Color**
Color communicates meaning. Design for users who cannot rely on color alone.

- Never use color as the sole indicator of meaning (error, success, required)
- Support color-blind users with shape, pattern, and label
- Red for errors only — don't use red for neutral actions

**Human-Interface Objects**
Interactive objects should behave consistently regardless of where they appear. A button
is a button. A link is a link.

- Component behavior should be predictable from appearance
- Reuse established patterns rather than reinventing interaction for each screen

---

### NNGroup's Interactivity Attributes

NNGroup identifies eight interaction qualities that shape how users perceive the product —
and by extension, the brand behind it.

| Attribute | Definition | Design Implication |
|---|---|---|
| **Responsiveness** | Speed of element reaction to input | Every action needs acknowledgment within 100ms |
| **Direct manipulation** | Whether users interact with objects themselves or through intermediaries | Drag-and-drop vs. menus; direct editing vs. form dialogs |
| **Precision** | Granularity of user control | Slider with fine control vs. coarse steps |
| **Pliability** | Ease of effecting change | How much effort does it take to change something? |
| **Continuous vs. discrete** | Smooth vs. stepped transitions | Volume slider vs. volume buttons |
| **Clear labels/feedback** | How well the system communicates available actions and consequences | Tooltips, labels, ARIA, helper text |
| **Expected behavior** | Alignment with user mental models | Does it do what it looks like it does? |
| **Consistency** | Conformity to established patterns | Same component → same behavior, always |

---

## Response Time and Feedback Design

### The Three Response Thresholds

| Threshold | Time | User Perception | Design Response |
|---|---|---|---|
| **Instantaneous** | ≤ 0.1s | Feels direct, no delay perceived | Visual state change only (button active state) |
| **Flow maintained** | 0.1s – 1.0s | User notices delay but stays focused | Spinner or skeleton screen |
| **Attention limit** | 1s – 10s | User disengages; must retain focus consciously | Progress indicator with estimated time |
| **Abandonment risk** | > 10s | Users leave, especially on web | Background processing + notification on complete |

### Feedback Types

**Visual feedback** — the default. Every interaction should have a visual state change.

**Motion feedback** — communicates that change is happening and in what direction.
- Page transitions communicate navigation direction (slide left = forward)
- Height animations communicate expand/collapse
- Fade communicates appearance/disappearance

**Haptic feedback** — for native mobile. Use sparingly and for meaningful confirmation.
- Success: single tap
- Warning: double tap
- Error: buzz pattern

**Audio feedback** — contextual. Avoid for routine actions.

### Perceived Performance Patterns

**Skeleton screens** — show layout structure while content loads. Better than spinners
for page-level content because they reduce perceived wait time and prevent layout shift.

**Optimistic UI** — apply the result of an action immediately in the UI before server
confirmation. Roll back on failure. Best for high-confidence actions (like, follow, upvote).

**Progress indicators** — use for actions over 1 second where the user is waiting. Show
percentage when deterministic; use animated indicator when indeterminate.

**Instant transitions** — avoid animating page-level transitions faster than 150ms or
slower than 400ms. The sweet spot is 200–300ms.

→ *See [reference/response-time.md](reference/response-time.md) for full implementation patterns.*

---

## Designing Interactions

### Component States

Every interactive component needs a complete state set. Missing states cause visual
regressions, accessibility failures, and inconsistent behavior.

| State | When It Applies | Design Requirements |
|---|---|---|
| **Default** | Initial, uninteracted state | Clear affordance of interactivity |
| **Hover** | Cursor/pointer over element (desktop) | Subtle visual change; avoid large layout shifts |
| **Focus** | Keyboard or programmatic focus | Must be visible (WCAG 2.4.7); never remove outline without replacement |
| **Active / Pressed** | Element currently being clicked/tapped | Depressed or highlighted to confirm receipt of input |
| **Loading** | Action in progress | Disable further input; show progress |
| **Disabled** | Action not currently available | Reduced opacity or style; no hover state; cursor: not-allowed |
| **Error** | Validation failure or system error | Red color + icon + text; never color-only |
| **Success** | Action completed successfully | Positive confirmation; transient for routine actions |
| **Empty** | No content to display | Never a blank screen; provide context and a next action |
| **Skeleton** | Content loading for first time | Match the layout of the content that will appear |

**State design checklist:**
- [ ] All 10 states defined for interactive components
- [ ] Focus state is visible and meets WCAG 2.4.7
- [ ] Error state uses color + icon + text (not color alone)
- [ ] Disabled state is visually distinct but does not rely on color alone
- [ ] Empty state provides a path forward

### Interaction Flows

A flow is the path a user takes through a product to accomplish a goal. Good flows have
a clear entry point, a happy path, branching for edge cases, and error recovery.

**Flow anatomy:**

```
Entry point → [Trigger] → Interaction sequence → [Decision] → Outcome
                                                      ↓
                                                  Error path → Recovery → Resume
```

**Flow design questions:**
- What is the user's goal entering this flow?
- What information does the user need at each step?
- Where are the decision points? What happens on each branch?
- What can go wrong? What is the recovery path?
- What is the exit? Is it clear and consistent?

**Multi-step flow principles:**
- Show progress (step indicator, breadcrumb, percentage)
- Allow backward navigation without data loss
- Save progress automatically so users can resume
- Surface errors inline, at the step they occur — not at submission
- Confirm destructive exits ("Are you sure you want to leave? Your progress will be lost.")

### Transitions and Animation

Animation serves one purpose in IxD: communication. It communicates state change,
spatial relationships, and system feedback. Avoid animation for decoration.

**When to animate:**
- Appearance/disappearance of elements (fade, scale)
- Navigation between views (slide, push)
- Expand/collapse of content (height transition)
- Loading and progress states
- Confirmation and error states

**When NOT to animate:**
- Hover states (a slight color change is enough)
- Tooltip appearance (instant is fine)
- Text changes
- Any transition where the user is waiting for the result

**Duration guide:**

| Interaction Type | Duration | Easing |
|---|---|---|
| Micro-interactions (button state, toggle) | 100–150ms | ease-out |
| Small component transitions (dropdown, tooltip) | 150–200ms | ease-out |
| Medium component transitions (modal, panel) | 200–300ms | ease-in-out |
| Full page transitions | 250–400ms | ease-in-out |
| Loading animations | Loop at 1–2s | linear |

**Easing:**
- `ease-out` — starts fast, ends slow. Use for elements entering the screen.
- `ease-in` — starts slow, ends fast. Use for elements leaving the screen.
- `ease-in-out` — smooth through the transition. Use for repositioning.
- `linear` — constant speed. Use for loading spinners and progress bars.

### Affordances and Signifiers

**Affordance** — the actual capability of an element (a button can be pressed).

**Perceived affordance** — what the element looks like it can do. This is what matters.

**Signifier** — a signal that communicates how to interact (a drag handle, an underline,
a placeholder in a text field).

Design for perceived affordance, not just actual affordance:
- A flat button with no shadow, no background, and no border has poor perceived affordance
- A text input needs a border, background contrast, or underline to signal editability
- Draggable elements need a visual handle or cursor change to signal draggability

**Anti-affordances** — signals that something cannot be done (a disabled button, a greyed
text field). These are as important as affordances — they prevent error attempts.

### Mental Models

A mental model is the user's internal representation of how a system works. Good
interaction design aligns system behavior with the user's existing mental model.

**When to align with mental models:**
- Navigation patterns (back button, hamburger menu location)
- Form behavior (tab order, validation timing)
- Destructive actions (confirm → proceed, not proceed → confirm)
- Data persistence (auto-save vs. explicit save)

**When mental models conflict:**
If a new interaction pattern breaks an established mental model, you must:
1. Signal the change clearly before it happens
2. Provide onboarding at the point of the deviation
3. Consider whether the deviation is worth the cost

❌ Changing the meaning of a swipe gesture without warning
✅ Adding a tooltip on first use: "Swipe left to archive (previously: delete)"

---

## Micro-Interactions

Micro-interactions are the small, contained interactions that handle a single use case.
They are the fabric of an interface — not headline features, but what makes a product
feel polished and intentional.

**The micro-interaction framework:**

```
Trigger → Rules → Feedback → Loops & Modes
```

### Trigger
What initiates the micro-interaction? User-initiated triggers are explicit (a button click,
a swipe). System triggers are automatic (a notification arrives, a download completes).

### Rules
What happens when the trigger fires? Rules define the behavior:
- What state changes?
- What is the sequence of events?
- What are the constraints? (Can you undo? Is there a minimum/maximum?)

### Feedback
How does the user know the rules are executing?
- Visual: state change, animation, color shift
- Text: label change, confirmation copy, error message
- Sound: notification chime, error beep (use sparingly)
- Haptic: confirmation tap (native mobile only)

### Loops & Modes
Does the micro-interaction repeat? Does it change behavior based on history?
- A password strength meter runs in a loop as the user types
- A toggle switches between two modes
- A pull-to-refresh is a loop with a discrete completion

### Common Micro-Interaction Examples

**Button states:**
Trigger: click → Rule: submit form → Feedback: button text changes to "Saving...", spinner appears → Loop: resolves to "Saved" or "Error"

**Inline form validation:**
Trigger: blur (leave field) → Rule: validate format → Feedback: green checkmark or red error message inline → Loop: re-validates on change

**Toggle:**
Trigger: tap → Rule: flip boolean → Feedback: thumb slides, color shifts, label updates → Mode: on / off

**Pull-to-refresh:**
Trigger: pull past threshold → Rule: fetch new data → Feedback: spinner, "Refreshing...", then content updates → Loop: available again after completion

**Like / reaction:**
Trigger: tap → Rule: toggle liked state → Feedback: icon fills with color, count increments (optimistic UI) → Mode: liked / not liked

---

## Role-Specific Application

### Product Designers

Your IxD work spans the full product — flows, states, feedback, and transitions.

- **In exploration**: Use flows to map the full task, not just the happy path. Identify branches and error states early.
- **In spec**: Annotate behavior, not just appearance. "Button is disabled until all required fields are valid" is more useful than a visual showing a grey button.
- **In handoff**: Document all 10 component states. Annotate transition durations and easing. Include motion references (Figma prototype or video) for non-obvious animations.
- **In critique**: Anchor interaction decisions to the user's goal. "This is consistent with the mental model of..." is a stronger argument than "this feels right."

### UX Designers

Your IxD focus is on task flows, information architecture, and error recovery.

- Map all flows before designing any screen. Identify dead ends — states the user can reach but cannot exit gracefully.
- Treat error recovery as a primary design task, not an afterthought. Every error state needs: what happened, why, and what to do next.
- Write microcopy as part of the interaction design, not after. The label, placeholder, error message, and helper text are part of the interaction.
- Validate flows with task-based testing before moving to visual design.

### UI Designers

Your IxD focus is component states, motion design, and interaction fidelity.

- Deliver all 10 states for every interactive component — not just default and hover.
- Use a motion system, not one-off animations. Define duration tokens (fast: 150ms, medium: 250ms, slow: 400ms) and apply them consistently.
- Prototype interactions before handing off — engineers implement what they understand, not what they infer.
- Review the built product against your specs. Interaction quality degrades in implementation without designer involvement.

### Service Designers

Your IxD work extends beyond screens to cross-channel touchpoints and staff-facing systems.

- Interactions happen at every touchpoint: web, app, kiosk, IVR, in-person. Map them all in a service blueprint before designing individual screens.
- Staff-facing interactions have different requirements than customer-facing: efficiency over discovery, error-tolerance, and context awareness (staff are busy and may be interrupted mid-flow).
- Transitions between channels are interactions too: "You'll receive a confirmation email" is an interaction spec.
- Test with both customers and frontline staff. Staff experience failures become customer-facing failures.

### Interaction Designers

As a dedicated IxD role, your ownership covers the full behavior layer.

- Own the motion system and ensure it is implemented consistently.
- Conduct interaction audits across the product to identify inconsistency and missing states.
- Write behavior specifications that engineering can implement without follow-up questions.
- Partner with accessibility specialists to ensure interaction patterns are keyboard and screen-reader accessible.

---

## Interaction Review Checklist

Use this checklist when reviewing designs before handoff or release.

### Flows
- [ ] Happy path is clear and unambiguous
- [ ] All decision branches are designed (not just the expected one)
- [ ] Error paths lead to recovery, not dead ends
- [ ] Multi-step flows show progress and allow backward navigation
- [ ] Destructive exits warn before proceeding

### States
- [ ] All 10 states designed for each interactive component
- [ ] Focus state is visible and WCAG-compliant
- [ ] Error state uses color + icon + text
- [ ] Empty state provides context and a next action
- [ ] Loading state prevents duplicate input

### Feedback
- [ ] Every action has immediate visual acknowledgment (within 100ms)
- [ ] Success and failure states are clearly differentiated
- [ ] Feedback is proportional to the significance of the action
- [ ] Long-running operations show progress

### Affordances
- [ ] Interactive elements look interactive (perceived affordance)
- [ ] Non-interactive elements do not look interactive
- [ ] Draggable elements have visual handles or cursor signals
- [ ] Disabled elements are visually distinct

### Motion
- [ ] All animations have a communicative purpose
- [ ] Duration and easing follow the motion system
- [ ] Animations do not delay user progression
- [ ] `prefers-reduced-motion` is respected

### Microcopy
- [ ] Button labels are action-oriented verbs
- [ ] Error messages say what happened, why, and what to do next
- [ ] Placeholder text is supplementary, not a substitute for labels
- [ ] Confirmation dialogs name what will be deleted/changed

### Accessibility
- [ ] All interactions are keyboard-accessible
- [ ] Focus order follows visual reading order
- [ ] Timed interactions can be extended or paused
- [ ] ARIA labels present for non-text interactive elements

---

## Common Anti-Patterns

### Invisible affordances
❌ Clickable text that looks identical to non-clickable text
❌ Draggable items with no visual signal
❌ Buttons that look like flat text
✅ Establish a clear, consistent visual language for interactivity. Interactive = looks interactive. Non-interactive = looks static.

### Missing states
❌ Components with only a default design — no error, empty, loading, or focus states
❌ Handoffs that show the happy path only
✅ Design all 10 states before handing off any component.

### Feedback arrives too late
❌ Form that validates only on submit, after the user has filled in five fields
❌ Destructive action with no immediate feedback
✅ Validate inline on blur. Acknowledge every action within 100ms.

### Animations that delay action
❌ A 600ms modal entrance animation that the user must wait through before interacting
❌ Animated transitions that run on every navigation, adding time to every action
✅ Keep entrances at 200–300ms. Never animate the user into waiting.

### No error recovery path
❌ An error message with only "Something went wrong" — no action, no retry
❌ A form that clears all fields on validation failure
✅ Every error state must say: what happened + why + what to do next. Preserve user input.

### Violating mental models without warning
❌ A swipe gesture that behaves differently than the user expects from their platform
❌ A "Back" button that resets state instead of navigating back
✅ Align with platform conventions. When you must deviate, signal it explicitly.

### Disabled without explanation
❌ A greyed-out button with no tooltip or context explaining why it is disabled
✅ Disabled states should communicate the condition for enablement: "Available after selecting a date."

### Breaking consistency
❌ The same component behaves differently on different screens
❌ Modals confirm on the left on some screens, the right on others
✅ Interaction patterns are system decisions, not per-screen decisions. Document and enforce them.

---

## Output Format

When this skill is active, Claude will adapt output to what you need:

### Interaction Specification
A full behavior spec for a component or flow:
- Trigger conditions
- State transitions
- Feedback description (visual, motion, copy)
- Edge cases and error handling
- Accessibility notes

### State Table
A structured table of all states for a component with:
- State name
- Visual description
- Trigger condition
- Transition behavior

### Flow Diagram (text)
A structured text representation of a flow:
- Entry point
- Sequence of states
- Decision branches
- Error paths and recovery
- Exit point

### Interaction Critique
Evaluation of existing interactions against principles:
- Which principle is violated
- Why it matters for users
- Specific, actionable fix

### Motion Brief
Animation specification:
- Element and property being animated
- Duration and easing
- Trigger and exit
- Reduced-motion alternative

### Format Conventions
- Structured headers for multi-part outputs
- Tables for state sets and comparison matrices
- ❌/✅ for anti-patterns vs. recommended practice
- Code format for timing values and CSS properties
- Annotations explaining the reasoning, not just the decision

---

## Reference Files

- [reference/principles.md](reference/principles.md) — Full Tognazzini 19 + Norman 6 with applied examples and violation patterns
- [reference/response-time.md](reference/response-time.md) — Nielsen's 3 response-time thresholds with implementation patterns for each loading/feedback scenario
- [reference/patterns-and-flows.md](reference/patterns-and-flows.md) — Common IxD patterns: forms, navigation, search, onboarding, error handling, empty states, modals
