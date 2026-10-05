---
name: surface-motion
description: Implement animation and transitions with precise easing, timing, and transform rules. Use this skill whenever writing CSS transitions, keyframe animations, spring animations, Motion (Framer Motion) configs, or any code that moves elements on screen. Also triggers for animation vocabulary, pattern names, easing curves, duration tuning, transform-origin placement, scale ranges, exit/entrance patterns, staggered entrances, icon swap animations, AnimatePresence, scroll-triggered reveals, CSS transition vs keyframe selection, animation libraries, spring physics, reduced motion, and "feels janky" or "too slow/fast" complaints. Provides the exact values, code patterns, and implementation recipes for web animation. Does NOT decide whether something should animate or what spatial logic to follow (use surface-interaction for those decisions). Does NOT cover gesture design, frequency/novelty calibration, or interaction intent. Does NOT cover colour, typography, layout, or component APIs.
---

# Motion

Animation implementation for web interfaces. This skill provides the exact values, properties, and code patterns for making things move well. It is the implementation layer of the Fluidity pillar from the shared `references/design-philosophy.md`. Incorporates the [12 Principles of Animation](https://www.raphaelsalaja.com/library/12-principles-of-animation) adapted for UI by Raphael Salaja and the practical animation patterns of [Emil Kowalski](https://emilkowal.ski).

**surface-interaction decides whether and why. This skill decides how.** For accessibility across all skills, see `references/accessibility.md`. For multi-skill task sequencing, see `references/composition.md`.

For animation polish reviews, paired element timing, CSS-only icon swaps, `AnimatePresence initial={false}`, and frame-by-frame debugging, read `references/polish-recipes.md`.

For animation vocabulary, pattern names, and prompt terminology, read `references/animation-vocabulary.md`.

---

## Easing

### Default easing

```css
/* Use this unless you have a specific reason not to */
transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
```

This is an ease-out curve with a fast start and gentle deceleration. It suits the vast majority of UI transitions: elements appearing, overlays opening, panels sliding.

### Never use

- `linear` for UI transitions. Linear motion looks mechanical and lifeless.
- `ease` (the CSS default). Its ease-in start creates a sluggish feel. Exception: `ease` works for trivial hover effects like background colour changes.
- `ease-in` for entrances. Elements should decelerate into their resting position, not accelerate into it. Ease-in is only appropriate for exits (elements accelerating away).
- Built-in CSS curves (`ease-in-out`, `ease-out`) without modification. They are generally too gentle to feel energetic. Use custom cubic-bezier curves instead. See [easing.dev](https://www.easing.dev/) or [easings.co](https://easings.co/) for stronger alternatives.

### Easing reference

| Context | Curve | Character |
|---|---|---|
| Default (most transitions) | `cubic-bezier(0.16, 1, 0.3, 1)` | Fast start, gentle settle |
| Entrance (element appearing) | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Decelerate in |
| Exit (element leaving) | `cubic-bezier(0.4, 0.0, 1, 1)` | Accelerate out |
| Emphasis / bounce | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Overshoot and settle |
| Spring (via Motion) | `type: "spring", stiffness: 400, damping: 30` | Physically modelled |

### Springs

Springs model real physics: mass, stiffness, and damping. They produce more natural motion than bezier curves because duration is emergent from the physics, not prescribed.

Use springs (via Motion) when:
- An element needs to feel weighty or bouncy (modals, cards, draggable items).
- Motion should respond to velocity (gesture-driven animations where release speed matters).
- You want overshoot that settles naturally.

Use bezier curves when:
- The animation is simple and brief (opacity fades, colour changes).
- You need precise, fixed-duration timing (synchronising multiple elements).
- Spring physics would be overkill (button hover states, focus ring transitions).

```tsx
// Spring config for a modal entrance
<motion.div
  initial={{ opacity: 0, scale: 0.85 }}
  animate={{ opacity: 1, scale: 1 }}
  transition={{ type: "spring", stiffness: 400, damping: 30 }}
/>
```

---

## Duration

### Limits

| Category | Maximum | Notes |
|---|---|---|
| Micro-interactions (hover, press, focus) | 150ms | Must feel instant |
| Interactions (toggle, switch, tab change) | 200ms | Responsive, not sluggish |
| Entrances and exits (modals, overlays, sheets) | 300ms | Perceptible but not slow |
| Page/view transitions | 400ms | Upper bound for anything |
| Content reveals (accordions, expanding sections) | 250ms | |

Nothing in a UI should animate for longer than 400ms per individual element. If it takes longer, the user is waiting. Orchestrated sequences (staggered entrances, multi-step reveals) may run longer in total, but each element within the sequence should respect the 400ms limit.

### Duration scaling

Larger elements should animate slightly slower than smaller ones. A full-screen modal at 300ms feels right; a tiny tooltip at 300ms feels sluggish. Scale duration with visual size:

- Small (tooltips, badges, icons): 100-150ms
- Medium (dropdowns, popovers, cards): 150-250ms
- Large (modals, sheets, full-screen): 200-350ms

---

## Properties

### Prefer compositor-friendly properties

Prefer `transform` and `opacity`. They are the safest defaults because browsers can usually composite them without recalculating layout or repainting the element's contents.

Treat other properties by cost:

- **Layout-triggering:** `width`, `height`, `top`, `left`, `margin`, `padding`, and similar geometry changes can recalculate layout.
- **Paint-triggering:** `background-color`, `box-shadow`, `border-color`, and many visual effects may avoid layout but still repaint.
- **Expensive compositor effects:** `filter` and `backdrop-filter` can be useful, but blur in particular is costly and must be tested on target hardware.

**How to achieve common effects with performant properties:**

| Desired effect | Implementation |
|---|---|
| Element grows/shrinks | `transform: scale()` |
| Element moves | `transform: translate()` |
| Element appears/disappears | `opacity: 0` to `1` (with `transform: scale()` or `translateY()`) |
| Soft entrance/exit | Small `filter: blur()` combined with opacity, after testing on target hardware |
| Background colour changes | Layer a pseudo-element and animate its `opacity` |
| Width/height changes | Animate `transform: scaleX()` / `scaleY()` on a wrapper |

`filter: blur()` is useful for masking imperfect transitions (see blur as transition mask, below) but carries a performance cost. Test on real hardware. Disable under `prefers-reduced-motion`.

### Hardware acceleration

When the main thread is busy (page navigation, heavy rendering), JavaScript-driven animations such as Motion or `requestAnimationFrame` can drop frames. CSS transitions and WAAPI can run some compositor-friendly animations away from the main thread, but only for properties the browser can composite. If an animation stutters during navigation or data loading, reduce work first, then consider moving simple `transform`/`opacity` motion from JavaScript to CSS or WAAPI and profile again.

### The `transition: all` ban

Never use `transition: all`. It triggers transitions on every property change, including unintended ones (colour, padding, border). Explicitly list the properties you want to animate:

```css
/* Wrong */
transition: all 200ms ease;

/* Right */
transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1),
            opacity 200ms cubic-bezier(0.16, 1, 0.3, 1);
```

---

## Scale Ranges

### Entrances

Never scale an element from 0. An element appearing from nothing looks like a glitch, not a transition. Minimum entry scale is 0.85.

```tsx
// Modal entrance
initial={{ opacity: 0, scale: 0.85 }}
animate={{ opacity: 1, scale: 1 }}
```

For smaller elements (tooltips, popovers), use a tighter range: 0.92 to 1.

### Press feedback

Active/pressed states should scale down subtly. The target range is 0.96 to 0.98. Anything more dramatic (0.9 or below) feels like a cartoon.

```css
button:active {
  transform: scale(0.97);
}
```

### transform-origin

Overlays, popovers, and dropdowns must set `transform-origin` to the position of the element that triggered them. A modal triggered by a button in the top-right should grow from the top-right, not from the centre of the screen.

```tsx
<motion.div
  style={{ transformOrigin: `${triggerX}px ${triggerY}px` }}
  initial={{ opacity: 0, scale: 0.85 }}
  animate={{ opacity: 1, scale: 1 }}
/>
```

Radix and Base UI provide CSS variables that set `transform-origin` automatically based on the trigger's position. Use these instead of calculating manually:

```css
/* Radix */
.popover-content {
  transform-origin: var(--radix-popover-content-transform-origin);
}

/* Base UI */
.popover-content {
  transform-origin: var(--transform-origin);
}
```

shadcn/ui applies this by default. If you're using Radix or Base UI directly, set it yourself.

---

## Exit Patterns

### Exits should be faster than entrances

Entrances introduce something new: the user needs time to register what appeared. Exits remove something the user is done with: they should feel immediate. A good ratio is entrance duration x 0.7 for the exit.

### Exit direction

An element should exit in the direction that makes spatial sense. If it entered from the bottom, it exits to the bottom. If it entered by scaling up from a trigger, it exits by scaling back down to the trigger.

For elements that don't have a clear spatial origin, fade out (opacity to 0) with a slight downward translate (3-5px). Fading upward feels like the element is floating away; fading downward feels like it's settling out.

### Subtle exits

Exit animations should be less dramatic than entrances. An entrance might use `translateY("calc(-100% - 4px)")` to slide in the full height. The corresponding exit should use a fixed small value like `translateY(-12px)` rather than reversing the full distance. Some motion should remain to indicate direction, but exits should not demand the same attention as entrances.

```tsx
<motion.div
  initial={{ opacity: 0, y: "calc(-100% - 4px)", filter: "blur(4px)" }}
  animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
  exit={{ opacity: 0, y: "-12px", filter: "blur(4px)" }}
  transition={{ type: "spring", duration: 0.45, bounce: 0 }}
/>
```

### AnimatePresence for conditional elements

When elements are conditionally rendered (mounting/unmounting based on state), wrap them in Motion's `AnimatePresence` to enable exit animations. Without it, unmounted elements disappear instantly with no transition.

```tsx
<AnimatePresence>
  {isVisible && (
    <motion.div
      key="panel"
      initial={{ opacity: 0, scale: 0.85 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.85 }}
    />
  )}
</AnimatePresence>
```

Every conditionally rendered element that has an entrance animation should also have an exit animation via `AnimatePresence`. Appearing with motion and disappearing instantly is worse than no animation at all.

---

## Patterns

### Staggered entrances

When multiple elements enter at once (a list of cards, a hero section with title, description, and buttons), split them into individual items and stagger their entrance with increasing delay. This draws the eye through the content in reading order.

```tsx
{items.map((item, i) => (
  <motion.div
    key={item.id}
    initial={{ opacity: 0, y: 8, filter: "blur(5px)" }}
    animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
    transition={{ delay: i * 0.1, duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] }}
  />
))}
```

Or with CSS only:

```css
@keyframes enter {
  from {
    transform: translateY(8px);
    filter: blur(5px);
    opacity: 0;
  }
}

.stagger-item {
  animation: enter 800ms cubic-bezier(0.25, 0.46, 0.45, 0.94) both;
  animation-delay: calc(var(--delay, 0ms) * var(--stagger, 0));
}
```

Three levels of granularity: animate the container as one block (weakest), animate sections individually with 80-100ms delay (good), animate individual words or items with shorter delays (strongest, use sparingly).

### Icon swap animation

When an icon changes state (copy to checkmark, play to pause, open to close), animate the swap with opacity, scale, and optionally blur. The outgoing icon fades and shrinks; the incoming icon fades in and grows. Never instant-swap icons.

```tsx
<AnimatePresence mode="wait">
  {isCopied ? (
    <motion.span
      key="check"
      initial={{ opacity: 0, scale: 0.5, filter: "blur(4px)" }}
      animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
      exit={{ opacity: 0, scale: 0.5, filter: "blur(4px)" }}
      transition={{ type: "spring", duration: 0.3, bounce: 0 }}
    >
      <CheckIcon />
    </motion.span>
  ) : (
    <motion.span
      key="copy"
      initial={{ opacity: 0, scale: 0.5 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.5 }}
      transition={{ type: "spring", duration: 0.3, bounce: 0 }}
    >
      <CopyIcon />
    </motion.span>
  )}
</AnimatePresence>
```

Use `mode="wait"` on AnimatePresence to ensure the outgoing icon exits before the incoming one enters. Springs produce more natural icon swaps than CSS easing.

### CSS transitions vs keyframe animations

CSS transitions and keyframe animations have fundamentally different interruptibility behaviour. Understanding this distinction is critical for choosing the right tool.

**CSS transitions interpolate toward the latest state.** If you change the target value while a transition is running, it smoothly redirects from its current position to the new target. This makes transitions inherently interruptible and ideal for interactive animations (hover, toggle, drag feedback).

**CSS keyframe animations run on a fixed timeline.** They do not retarget. If the trigger condition changes mid-animation, the animation either completes or restarts. This makes keyframes unsuitable for interactions that can be interrupted, but good for staged sequences that run once (page entrance, loading states, decorative loops).

Rule of thumb: CSS transitions for interactions. Keyframe animations for choreographed sequences. Motion (Framer Motion) springs for anything that needs both interruptibility and physics.

### Scroll-triggered reveals with whileInView

Use Motion's `whileInView` for elements that animate when they scroll into the viewport. Combine with `initial` for the pre-reveal state.

```tsx
<motion.div
  initial={{ opacity: 0, y: 20, filter: "blur(8px)" }}
  whileInView={{ opacity: 1, y: 0, filter: "blur(0px)" }}
  viewport={{ once: true, amount: 0.3 }}
  transition={{ type: "spring", duration: 0.6, bounce: 0 }}
/>
```

Set `viewport.once: true` so elements only animate on first appearance, not every time they re-enter. `amount: 0.3` means 30% of the element must be visible before triggering.

### Blur as transition mask

When a crossfade between two states still feels rough after adjusting easing and duration, adding 2-4px of `filter: blur()` during the transition smooths the visual gap. The blur bridges the old and new states, tricking the eye into seeing a continuous morph rather than two distinct objects.

```tsx
<AnimatePresence mode="wait">
  <motion.div
    key={currentState}
    initial={{ opacity: 0, filter: "blur(4px)" }}
    animate={{ opacity: 1, filter: "blur(0px)" }}
    exit={{ opacity: 0, filter: "blur(4px)" }}
    transition={{ duration: 0.2 }}
  />
</AnimatePresence>
```

This is particularly effective for icon swaps, text changes, and state transitions where the shape changes significantly. It is a last resort after easing and timing have been tuned, not a first reach.

### CSS enter animations with @starting-style

The `@starting-style` at-rule allows CSS transitions on elements that are newly inserted into the DOM, without JavaScript. This provides interruptible enter animations using pure CSS:

```css
.popover {
  opacity: 1;
  transform: scale(1);
  transition: opacity 200ms ease-out, transform 200ms ease-out;
}

@starting-style {
  .popover {
    opacity: 0;
    transform: scale(0.93);
  }
}
```

This replaces the React pattern of mounting with a `data-mounted="false"` attribute and toggling it via `useEffect`. Browser support is broad (Chrome 117+, Safari 17.5+, Firefox 129+). For older browsers, fall back to the `useEffect` + data-attribute pattern.

---

## Animation Principles for UI

Three principles from traditional animation, adapted from the [12 Principles of Animation](https://www.raphaelsalaja.com/library/12-principles-of-animation) by Raphael Salaja, are particularly valuable for web interface motion. They separate animation that feels alive from animation that feels mechanical.

### Anticipation

A brief preparatory motion before the main action. It tells the user "something is about to happen" and makes the subsequent motion feel deliberate rather than abrupt.

In UI: a button scales down slightly (0.97) before a modal expands from it. A pull-to-refresh indicator winds up before releasing. A delete action shows a brief gather before the item flies away.

Anticipation should be extremely subtle in UI (50-100ms, 2-5% movement). Anything more feels theatrical. The user should feel it, not see it.

### Follow-through and overlapping action

Parts of an element continue moving after the main motion stops. Not everything arrives at the same time.

This is why springs feel alive: the overshoot-and-settle behaviour IS follow-through. The element passes its target and eases back. Without it, elements stop dead and feel robotic.

In compound elements, children should settle slightly after the parent. A card lifts, then its shadow adjusts. A modal reaches its position, then its content fades in 50ms later. A dragged item snaps to position, then its badge bounces once.

Staggered entrances (covered above) are overlapping action: each element begins its motion slightly after the previous, creating a cascade rather than a simultaneous block.

### Secondary action

A complementary animation that supports and reinforces the primary action without competing for attention.

When a modal opens (primary action), the background dims and blurs (secondary). When a card lifts on hover (primary), its shadow deepens and spreads (secondary). When a toast enters (primary), other toasts shift down to make room (secondary).

The rule: secondary actions must be less prominent than the primary. If the secondary action draws attention away from the primary, it is competing, not supporting. Test by watching only the secondary: if it's distracting on its own, it's too strong.

### Arcs

Natural motion follows curved paths, not straight lines. In UI this is subtle: a notification entering from the top-right can follow a very slight arc rather than a perfectly linear diagonal. Elements transitioning between positions look marginally more natural on gently curved trajectories.

This principle matters most for longer-distance movements (page transitions, elements moving across the viewport). For short movements (tooltips, dropdowns, small reveals), straight-line motion is fine.

---

## Reduced Motion

Respect `prefers-reduced-motion: reduce`. This is a system-level accessibility setting, not optional.

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

In Motion:

```tsx
const prefersReduced = useReducedMotion();

<motion.div
  animate={{ opacity: 1, y: 0 }}
  transition={prefersReduced ? { duration: 0 } : { type: "spring", stiffness: 400, damping: 30 }}
/>
```

Do not disable animations entirely. Reduce them to instant state changes so the UI still works logically.

---

## Libraries

Use these before rolling your own:

| Library | Purpose | Install |
|---|---|---|
| [Motion](https://motion.dev) | Layout animations, springs, gestures, exit animations | `npm i motion` |
| [number-flow](https://number-flow.barvian.me) | Animated number transitions | `npm i @number-flow/react` |
| [torph](https://torph.lochie.me/) | Text morphing between strings | `npm i torph` |
| [liveline](https://benji.org/liveline) | Real-time animated line charts | `npm i liveline` |
| [vaul](https://vaul.emilkowal.ski) | Drawer/tray component with gesture physics | `npm i vaul` |
| [sonner](https://sonner.emilkowal.ski) | Toast notifications (background info only) | `npm i sonner` |

---

## Anti-Patterns

1. **`transition: all`.** Explicitly list animated properties. `all` triggers unintended property animations.
2. **Scaling from 0.** Minimum entry scale is 0.85. Zero-to-one looks like a glitch.
3. **Centred transform-origin on triggered elements.** Overlays must grow from their trigger's position.
4. **Animating layout properties.** `width`, `height`, `top`, and `left` often cause jank. Prefer `transform` and `opacity`; use paint-heavy properties only when the effect is worth the cost and has been tested.
5. **Exit slower than entrance.** Exits should be ~70% of entrance duration.
6. **Ignoring `prefers-reduced-motion`.** Non-negotiable accessibility requirement.
7. **Linear easing.** Never for UI transitions. It looks robotic.
8. **Instant icon swaps.** Icons changing state (copy/check, play/pause) should animate with opacity and scale, not snap.
9. **Block entrance animation.** Animating an entire container as one unit instead of staggering its children.
10. **Keyframe animations for interactive state.** Keyframes don't retarget. Use CSS transitions or Motion springs for anything the user can interrupt.
11. **No AnimatePresence on conditional elements.** Elements that enter with animation but vanish instantly on unmount.
12. **Dead-stop motion.** Elements reaching their target and stopping without any overshoot or settle. Use springs for follow-through.
13. **Competing secondary actions.** A secondary animation (background blur, shadow shift) that is more prominent than the primary. Secondary must always be subordinate.

---

## Checklist

- Default easing is `cubic-bezier(0.16, 1, 0.3, 1)` (not `ease`, not `linear`)
- Micro-interactions are under 150ms
- Entrances/exits are under 300ms
- No animation exceeds 400ms
- Layout-triggering properties are avoided for routine motion
- `transform` and `opacity` are the default animated properties
- `filter` and paint-heavy effects are used sparingly and tested on target hardware
- No `transition: all` anywhere
- Entry scale minimum is 0.85
- Press feedback scale is 0.96-0.98
- `transform-origin` is set to trigger position for overlays
- Exits are faster than entrances
- `prefers-reduced-motion` is respected with instant fallbacks
- Springs are used for gesture-driven and weighty animations
- Bezier curves are used for simple, fixed-duration transitions
- Multi-element entrances are staggered, not animated as one block
- Icon state changes animate with opacity + scale (never instant swap)
- Conditional elements are wrapped in AnimatePresence for exit animations
- Exit animations use small fixed translate, not full entrance distance reversal
- CSS transitions are used for interactive state; keyframes for staged sequences
- Paired elements share timing and easing
- Default-state toggles and icon swaps do not animate on initial page load
- Scroll reveals use `whileInView` with `viewport.once: true`
- Springs provide follow-through (overshoot-and-settle) on significant transitions
- Compound elements have children settling slightly after the parent
- Secondary actions (blur, shadow) support but never compete with the primary
- Brief anticipation (50-100ms, 2-5% movement) precedes significant actions

---

## Learning from Usage

After completing a motion task, review the output against the checklist. Append findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting any new task.
