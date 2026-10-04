---
name: apple-design
description: Apply Apple-inspired interface principles to web UI with emphasis on direct manipulation, fluid gesture-driven motion, spring behavior, momentum, interruptibility, translucent materials, depth, typography, restraint, and inclusive feedback. Use for building or reviewing touch interactions, sheets, drawers, carousels, drag and swipe behavior, or an Apple-like design direction. Keep ordinary motion review in frontend-motion-review and general UI planning in frontend-design.
license: MIT
metadata:
  source: emilkowalski/skills
  compatibility: harness-neutral; framework-specific examples are conditional
---

# Apple Design

Use this as an optional design direction, not a mandatory visual style. The
goal is an interface that feels direct, predictable, and physically coherent:
feedback begins immediately, content tracks the user's gesture, motion carries
velocity, and an interaction can be interrupted or reversed at any time.

This skill does not require a particular framework, motion library, browser, or
Apple platform. Inspect the existing stack first and adapt the principles to
the project's components, tokens, accessibility contract, and brand rules.

## Design foundations

Use these principles to explain a design decision:

1. **Purpose** — spend attention and motion only where it improves the task.
2. **Agency** — keep people in control, provide forgiveness, and reserve
   confirmation for genuinely destructive irreversible actions.
3. **Responsibility** — make privacy, safety, errors, and consequences clear.
4. **Familiarity** — preserve predictable placement, mapping, and behavior.
5. **Flexibility** — support devices, input methods, text sizes, languages, and
   abilities instead of optimizing for one ideal viewport.
6. **Simplicity** — remove unnecessary steps while keeping useful context
   visible and advanced options discoverable.
7. **Craft** — defend spacing, type, color, iconography, motion, and alignment
   with observable reasons.
8. **Delight** — treat delight as the result of the preceding principles, not
   decoration added to compensate for a confusing flow.

When a choice is subjective, label it as a recommendation and tie it to the
user's task, not to an assumed Apple aesthetic.

## 1. Response and direct manipulation

- Give press feedback on pointer-down or `:active`, not only after release.
- Remove unnecessary debounce, artificial timers, transition waits, and input
  latency from the interaction path.
- During a drag, slider, or sheet gesture, update the visible value
  continuously and proportionally to the pointer.
- Respect the point where the user grabbed an object; do not snap it to its
  center when the gesture starts.
- Use Pointer Events and pointer capture when the web stack supports them.
- Provide a keyboard and non-pointer equivalent for every meaningful gesture.

```css
.button:active {
  transform: scale(0.97);
  transition: transform 100ms ease-out;
}
```

## 2. Interruptibility and continuity

An interaction should be redirectable while it is moving. Never lock out input
just because a transition is running.

- Animate from the current presentation value, not a stale logical target.
- Use transitions for simple state changes and springs for gestures or motion
  that can be grabbed, reversed, or retriggered.
- Carry velocity through a reversal instead of starting from rest.
- Keep the X and Y components independent when their velocities or targets
  differ.
- Enter and exit through coherent paths. A panel that arrives from the right
  should normally leave to the right.
- Set a transform origin that reflects the interaction source for anchored
  menus, popovers, and sheets. Centered modals are the exception.

## 3. Springs, velocity, and momentum

Use springs when the user can touch or redirect the object. A spring's settle
time emerges from its parameters; it is not interchangeable with a fixed
duration.

- Start ordinary UI critically damped with no overshoot.
- Add a small amount of bounce only when the gesture carried momentum, such as
  a flick, throw, or drag release.
- Pass release velocity into the settling animation so the handoff from drag
  to rest has no visible seam.
- Project a flick toward its likely resting point before choosing the nearest
  snap target; do not always snap from the release point.

Conceptual spring defaults, translated to APIs that support these parameters:

| Interaction        | Damping | Response |
| ------------------ | ------: | -------: |
| Reposition or move |     1.0 |     0.4s |
| Rotation           |     0.8 |     0.4s |
| Drawer or sheet    |     0.8 |     0.3s |

Use the actual API and existing project tokens. For a web spring API expressed
as bounce and duration, begin with no bounce for ordinary UI and reserve
`bounce: 0.1–0.3` for physical momentum.

For a bounded gesture, an exponential projection can be used when it matches
the product's interaction model:

```js
function project(initialVelocity, decelerationRate = 0.998) {
  return ((initialVelocity / 1000) * decelerationRate) / (1 - decelerationRate);
}

const projected = currentPosition + project(releaseVelocity);
const target = nearestSnapPoint(projected);
```

Treat the constants as starting points, not universal truth. Verify feel with
the actual device, content size, and input velocity.

## 4. Gesture details

For drag, swipe, carousel, sheet, or interactive dismissal:

1. Give immediate visual feedback on pointer-down.
2. Track the grab offset and a short position/time history.
3. Use a small movement threshold, around 10px, before committing a direction.
4. Capture the pointer so tracking continues outside the original bounds.
5. Ignore additional touch points after a gesture begins.
6. Apply progressive resistance beyond a natural boundary instead of a hard
   invisible wall.
7. Decide dismissal from both distance and velocity when a flick should count.
8. Settle with a spring that carries release velocity.
9. Support cancellation by dragging away, release, Escape, and keyboard input
   where the interaction has a meaningful equivalent.

Rubber-band resistance can be modeled as:

```js
function rubberband(overshoot, dimension, constant = 0.55) {
  return (
    (overshoot * dimension * constant) /
    (dimension + constant * Math.abs(overshoot))
  );
}
```

Do not use a final `swipeleft`-style event as the only signal when continuous
feedback is required; it discards the movement history needed for a fluid
interaction.

## 5. Materials and depth

Translucency can communicate hierarchy when it preserves legibility and does
not become decoration for its own sake.

- Use translucent layers for floating toolbars, navigation, or sheets only
  when content genuinely scrolls underneath.
- Make heavier structural surfaces darker or more opaque and lighter
  interactive surfaces less visually dominant.
- Do not stack multiple light translucent surfaces when the combined contrast
  makes text difficult to read.
- Pair blocking modal surfaces with a scrim; keep non-blocking parallel panels
  separate from the main flow without unnecessarily dimming it.
- Prefer a subtle edge fade or gradient where floating chrome overlaps content
  instead of adding dividers everywhere.
- For a glass-like surface, materialize blur, opacity, and scale together so it
  reads as a surface arriving rather than a plain fade.

```css
.toolbar {
  background: rgb(255 255 255 / 0.6);
  backdrop-filter: blur(20px) saturate(180%);
}

@media (prefers-reduced-transparency: reduce) {
  .toolbar {
    background: rgb(255 255 255 / 0.98);
    backdrop-filter: none;
  }
}
```

Always check contrast over the actual changing background. If the browser does
not support `backdrop-filter`, the opaque fallback must remain understandable.

## 6. Typography and layout

- Prefer the platform/system font before adding a custom face.
- Treat tracking and leading as size-specific. Large display type usually
  needs tighter tracking; body text generally stays near normal tracking.
- Build hierarchy from size, weight, and leading together.
- Use `rem` or `em` for spacing that should scale with user text settings.
- Test larger text sizes, narrow widths, localization, and rotation.
- Keep labels specific and controls near the content they affect.

```css
:root {
  font:
    100%/1.5 system-ui,
    sans-serif;
}

.display {
  font-size: clamp(2rem, 5vw, 4rem);
  line-height: 1.05;
  letter-spacing: -0.02em;
  font-optical-sizing: auto;
}
```

## 7. Accessibility and alternate inputs

Reduced motion is not a reason to remove useful state feedback. Replace
slides, parallax, and elastic movement with short opacity or color transitions;
remove overshoot and large positional changes.

```css
@media (prefers-reduced-motion: reduce) {
  .sheet {
    transition: opacity 200ms ease;
    transform: none !important;
  }
}

@media (prefers-contrast: more) {
  .surface {
    background: Canvas;
    border: 1px solid CanvasText;
  }
}
```

Also verify:

- focus is visible throughout transitions;
- keyboard users can open, operate, cancel, and close the interaction;
- semantic controls expose state to assistive technology;
- touch targets have adequate hit area and do not rely on hover;
- color, sound, haptics, and motion are supplemental rather than the only
  feedback channel; and
- large moving surfaces do not cause vestibular or flashing discomfort.

## 8. Multimodal feedback

Add sound or haptics only when they earn their cost:

1. **Causality** — feedback fires on the event that caused it.
2. **Harmony** — visual, sound, and haptic feedback are synchronized.
3. **Utility** — reserve extra channels for meaningful success, error, commit,
   or snap events.

Respect platform permissions and user settings. Never add external services or
permissions as an automatic consequence of using this skill.

## Review checklist

- [ ] The interaction has a named purpose and supports user agency.
- [ ] Pointer-down feedback and continuous gesture tracking are present.
- [ ] The gesture preserves grab offset and uses pointer capture where needed.
- [ ] The motion starts from the current presentation value.
- [ ] Release velocity and momentum are handed off where relevant.
- [ ] Bounds use progressive resistance rather than a hard stop.
- [ ] Enter/exit paths and transform origins are spatially coherent.
- [ ] Spring parameters match the interaction and existing tokens.
- [ ] Materials have a legible opaque fallback and no contrast regression.
- [ ] Typography scales with user settings and localization.
- [ ] Reduced motion, reduced transparency, and increased contrast are handled
      where the surface uses those features.
- [ ] Focus, keyboard, semantic state, and non-pointer alternatives work.
- [ ] Browser/device evidence supports any visual or accessibility claim.

If a rendered or device check was not available, report the limitation instead
of calling the interaction fluid, accessible, or Apple-like.
