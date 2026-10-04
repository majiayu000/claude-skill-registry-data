---
name: accessibility-baseline
description: Use this skill whenever writing any UI component, interactive element, form, modal, notification, simulation HUD, or any code that affects the learner-facing interface. This defines the WCAG 2.2 AA baseline requirements, keyboard navigation contract, focus management rules, caption requirements, and the reduced-motion policy for the Myelin platform. Load before writing any UI code.
---

This skill defines the accessibility baseline for the Myelin platform. WCAG 2.2 Level AA is the target. Level A is mandatory from v1. Level AA is required before any ministry or government-linked institutional deployment. All components must be built accessibility-first — retrofitting is significantly more expensive.

---

## WCAG 2.2 Level A — v1 Mandatory

The following criteria are blocking for v1 release (see `release-gate-checklist` PA4 advisory → blocking for government deployments).

### 1.1.1 Non-text Content

Every non-decorative image, icon, and control must have a text alternative.

```html
<!-- Icon button — use aria-label, not title -->
<button aria-label="Close simulation session">
  <svg aria-hidden="true" focusable="false">...</svg>
</button>

<!-- Informational image -->
<img src="/hasp-diagram.png" alt="Diagram showing hasp fully seated on valve stem">

<!-- Decorative image — hidden from assistive technology -->
<img src="/background-texture.png" alt="" role="presentation">
```

SVG icons used in interactive controls must always have `aria-hidden="true"` and `focusable="false"`. The text alternative lives on the parent control, not the SVG.

### 1.3.1 Info and Relationships

Structural relationships must be expressed in markup, not only visually.

```html
<!-- Form with explicit label association -->
<label for="cohort-select">Select cohort</label>
<select id="cohort-select" name="cohortId">...</select>

<!-- Error message linked to input -->
<input id="email-input" aria-describedby="email-error" aria-invalid="true">
<span id="email-error" role="alert">Enter a valid email address</span>

<!-- Data table with headers -->
<table>
  <thead>
    <tr>
      <th scope="col">Learner</th>
      <th scope="col">Completion</th>
      <th scope="col">Last active</th>
    </tr>
  </thead>
  <tbody>...</tbody>
</table>
```

### 1.4.1 Use of Colour

Information must not be conveyed by colour alone.

- Step status indicators must show a text label or icon pattern alongside the colour
- The pressure gauge emissive state (red/amber/green) must have an accompanying text label visible in the HUD
- Form validation errors must show an error icon plus text, not just a red border

### 2.1.1 Keyboard Accessible

All functionality must be operable via keyboard. No keyboard trap except for modal dialogs (which must have an accessible close mechanism).

### 2.4.3 Focus Order

Focus order must follow a logical sequence. DOM order determines focus order — do not use `tabindex > 0` to create an artificial order. Use `tabindex="0"` to make non-focusable elements focusable, and `tabindex="-1"` to programmatically focus elements without including them in the tab sequence.

### 4.1.2 Name, Role, Value

All interactive components must expose name, role, and state to assistive technology.

```javascript
// Progress indicator
<div
  role="progressbar"
  aria-valuenow={completedSteps}
  aria-valuemin={0}
  aria-valuemax={7}
  aria-label={`LOTO simulation: ${completedSteps} of 7 steps completed`}
>
```

---

## WCAG 2.2 Level AA — Government Deployment Requirement

### 1.4.3 Contrast Ratio

- Normal text: minimum 4.5:1 against background
- Large text (18pt / 14pt bold): minimum 3:1
- UI component boundaries (input borders, button outlines): minimum 3:1

Use the design system colour tokens defined in `design-system-tokens` skill — they are validated for contrast compliance. Do not introduce custom colours without checking contrast ratios.

```javascript
// Programmatic contrast check during development
function checkContrast(foreground, background) {
  const ratio = calculateContrastRatio(foreground, background);
  if (ratio < 4.5) console.warn(`Contrast ratio ${ratio} below 4.5:1 minimum`);
}
```

### 1.4.4 Resize Text

All text must remain readable and functional when resized to 200% via browser zoom. No truncation, no overlap, no horizontal scroll at 200% zoom on a 1280px viewport.

### 2.4.6 Headings and Labels

Every page must have a descriptive `<h1>`. Section headings must use the correct heading hierarchy (h1 → h2 → h3 — do not skip levels). Form inputs must all have visible labels.

### 2.4.7 Focus Visible

Focus indicators must be clearly visible. Do not use `outline: none` or `outline: 0` without providing an equivalent custom focus indicator.

```css
/* Minimum acceptable focus indicator */
:focus-visible {
  outline: 3px solid var(--color-focus-ring);
  outline-offset: 2px;
}
```

The `--color-focus-ring` token from the design system is validated for visibility against both dark and light theme backgrounds.

### 3.3.1 Error Identification

When a form field contains an error, the error must be described in text — not only indicated by colour or icon.

### 3.3.2 Labels or Instructions

Provide visible labels for all inputs. Placeholder text is not a label — it disappears on input and fails for users of assistive technology.

---

## Keyboard Navigation Contract

### Tab order rules

1. Landmark regions first (skip navigation link → main content → sidebar)
2. Within a form: label → input → hint text → error message → next control
3. Modal dialogs: trap focus within the modal until dismissed
4. Simulation HUD: all HUD controls must be keyboard accessible, but Tab focus must not enter the 3D canvas — the canvas is operated by keyboard shortcuts documented in the UI, not by sequential tabbing

### Skip navigation

Every page must have a skip-to-content link as the first focusable element:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

The skip link is visually hidden until focused. It must be the very first element in the tab sequence.

### Keyboard shortcuts for simulation

The simulator must support these keyboard interactions:
- `Escape` — pause simulation and show confirmation dialog
- `R` — reset session (requires confirmation dialog)
- `H` — toggle HUD visibility
- `?` — open keyboard shortcut help modal

All keyboard shortcuts must be documented in a discoverable help surface. They must not conflict with browser shortcuts.

---

## Focus Management for Dynamic Content

When content changes dynamically — modals open, step pass/fail feedback appears, notifications arrive — focus must be managed explicitly.

```javascript
// Opening a modal
function openModal(modalElement) {
  const firstFocusable = modalElement.querySelector(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  previousFocus = document.activeElement;
  firstFocusable?.focus();
}

// Closing a modal — return focus to trigger element
function closeModal() {
  previousFocus?.focus();
}

// Step pass notification — focus the feedback region
function announceStepResult(result) {
  const liveRegion = document.getElementById('step-feedback-live');
  liveRegion.textContent = result === 'PASS'
    ? 'Step passed. Proceeding to next step.'
    : 'Step not yet complete. Try again.';
}
```

### ARIA live regions

Use `aria-live` to announce dynamic state changes without moving focus:

```html
<!-- Step feedback — assertive for immediate announcement -->
<div id="step-feedback-live" aria-live="assertive" aria-atomic="true"
     class="sr-only"></div>

<!-- Notification feed — polite to avoid interrupting current task -->
<div id="notification-live" aria-live="polite" aria-atomic="false"
     class="sr-only"></div>
```

Do not use `aria-live="assertive"` for non-critical updates — it interrupts screen reader reading of the current content. Use `polite` for everything except time-sensitive safety feedback.

---

## Caption and Audio Description Requirements

### Video content (module learning items)

- All pre-recorded video content must have closed captions
- Caption files must be synchronised to within ±0.5 seconds of the audio
- Caption format: WebVTT (`.vtt`)
- Language: match the video audio language; provide English captions as fallback

```html
<video controls>
  <source src="/modules/loto-intro.mp4" type="video/mp4">
  <track kind="captions" src="/modules/loto-intro.en.vtt" srclang="en" label="English" default>
</video>
```

### Simulation audio cues

The simulation audio cues (step pass tones, mechanical sounds) are supplementary — every audio cue has a visual counterpart (HUD indicator colour change, text label). Learners using the platform without audio receive the same assessed information through visual channels. Do not carry information exclusively in audio.

### AI agent voice (LIVE_CONVERSATIONAL mode)

Live conversational agent responses must be simultaneously displayed as text in the transcript panel. Audio-only delivery is never acceptable.

---

## Reduced Motion

Respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  /* Disable animations on UI transitions */
  .page-transition,
  .step-indicator-animate,
  .notification-slide {
    animation: none;
    transition: none;
  }

  /* Disable parallax and continuous motion elements */
  .background-animate {
    animation: none;
  }
}
```

In the simulator: when `prefers-reduced-motion` is active, suppress particle effects (arc flash, fluid leak, smoke) and replace them with static visual indicators. The simulation interaction itself (grab, rotate, align) is user-controlled motion and is not suppressed.

---

## Screen Reader Testing Targets

Automated testing catches approximately 30% of accessibility issues. Manual testing with screen readers is required before every production release (advisory gate PA4). Priority testing targets:

| Screen reader | Browser | Platform |
|---------------|---------|---------|
| NVDA (latest) | Chrome | Windows |
| JAWS (latest) | Chrome | Windows |
| VoiceOver | Safari | macOS |
| VoiceOver | Safari | iOS (tablet focus for logbook) |

Test each learner journey entry point: registration, consent gate, dashboard, active learning item, simulation HUD controls, submission form, result statement view.

---

## What Not To Do

- Do not use `outline: none` without a custom focus indicator replacement
- Do not use placeholder text as a label — always provide a visible `<label>` element
- Do not use `aria-live="assertive"` for non-urgent updates — use `polite`
- Do not convey step status by colour alone — include text label or icon pattern
- Do not allow Tab to enter the 3D canvas during simulation — keyboard shortcuts only
- Do not deliver AI agent voice responses without simultaneous text display
- Do not skip heading levels in the heading hierarchy
- Do not use `tabindex > 0` to create artificial focus order — fix the DOM order instead
- Do not suppress reduced-motion user-controlled interactions (grab, rotate) — only suppress decorative animations
