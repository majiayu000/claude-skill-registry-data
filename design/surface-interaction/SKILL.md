---
name: surface-interaction
description: Make interaction design decisions about gestures, spatial logic, timing intent, and physical behaviour. Use when building swipe-to-dismiss, drag-and-drop, swipe-to-reveal, pinch-to-zoom, pull-to-refresh, navigation transitions, scroll-linked interactions, command menus, or deciding whether something should animate. Covers gesture intent, spatial consistency, kinetic physics, interruptibility, frequency calibration, metaphor reuse, snap points, progressive reveal, and elastic resistance. Does NOT provide easing curves, duration values, or animation code (use surface-motion). Does NOT cover platform quirks, CSS details, or accessibility specifics (use surface-details). Does NOT cover colour, typography, or component APIs.
---

# Interaction

Interaction design decisions for web interfaces. This skill answers the questions that come before animation: Should this element move? When should a gesture commit? Where should this transition come from? What happens when the user interrupts?

Based on the interaction thinking of [Rauno Freiberg](https://rauno.me/craft/interaction-design), the [drag gesture patterns](https://jakub.kr/work/drag-gesture) of Jakub Królikowski, and the perceptual heuristics of [Laws of UX](https://lawsofux.com).

**This skill decides whether and why. surface-motion decides how.**

For the shared design philosophy behind these decisions, see `references/design-philosophy.md`. For multi-skill task sequencing, see `references/composition.md`.

---

## 1. Gesture Intent

Not all gestures should trigger at the same moment. The right trigger point depends on the cost of accidental commitment.

### Trigger during the gesture (lightweight actions)

The action fires after a distance threshold while the finger is still down. This suits: revealing overlays, peeking at content behind a view, showing search, sliding between adjacent screens.

Why: the user gets immediate feedback and can dismiss without lifting. If the wrong thing appeared, they simply reverse the gesture.

### Trigger on gesture end (heavyweight actions)

The action fires only after the finger lifts, regardless of distance. This suits: dismissing an app, deleting an item, confirming a destructive action, reordering a list.

Why: the user can change their mind mid-gesture. If they've swiped halfway through a delete and realise it's the wrong item, they can reverse without consequence.

### The decision rule

Ask: "If the user accidentally crosses the threshold, what's the cost of the action firing?"

- Low cost (an overlay appeared, they can close it): trigger during.
- High cost (data was deleted, an app was closed): trigger on end.

---

## 2. Responsive Feedback

Every gesture must respond from the first pixel of movement. Never wait for a threshold before showing any visual feedback.

The element should track the pointer immediately. The "snap to final position" animation happens after the gesture ends or after a threshold is crossed, but the tracking starts from frame one.

A pinch gesture that shows no response until a threshold is crossed gives the user zero confidence that the element is even interactive. Apply the scale delta from the first touch movement, then snap past the threshold. The initial feedback is the affordance.

This applies equally to drags, swipes, pulls, and any custom gesture. The element moves with the finger from the start. The decision about what happens (commit or cancel) comes later.

---

## 3. Spatial Consistency

Motion must communicate where things are. Every transition answers two questions: "Where did this come from?" and "Where is it going?"

### Rules

**Expand from trigger.** An element that opens from a button should animate from that button's position, not from the centre of the screen. This creates a spatial relationship between the trigger and the result.

**Dismiss reverses entry.** If a sheet slid up from the bottom, it slides back down. If a modal scaled up from a button, it scales back down to the button. The return path mirrors the arrival path.

**Forward = right, backward = left.** This mirrors reading direction and how we turn pages. Navigating deeper into a hierarchy moves content to the left (new content enters from the right). Navigating back reverses this.

**Animate from the source when the source matters.** If a music player can open from either its icon on the home screen or a floating mini-player, animate from whichever the user tapped. The transition tells the user which source they activated.

**Crossfade when the origin is ambiguous.** If an element has no clear spatial origin (it's not triggered by something visible), a crossfade is better than a directional animation that implies a false location.

### Shared element transitions

When two views share a visual element (a card that expands to a detail view, a thumbnail that becomes a full image), the shared element should morph continuously between states. Never unmount the element in one view and mount a separate instance in the next.

This continuity tells the user they're looking at the same thing in two forms. Breaking the continuity (a card disappearing and a detail view fading in separately) tells the user two things happened instead of one.

---

## 4. Frequency and Novelty

Animation is not always an improvement. Its value decreases with repetition.

### The calibration

**Hundreds of times per day** (keyboard shortcuts, right-click menus, tab switching, command palettes): No entry animation. The macOS context menu appears instantly. The App Switcher appears instantly. Command-K palettes should appear instantly. A subtle fade on exit is the most that's appropriate.

**Tens of times per day** (opening a modal, switching views, toggling a panel): Brief, functional transitions. Enough to maintain spatial awareness, not enough to feel like waiting.

**A few times per session** (completing a multi-step flow, first successful action, reaching a milestone): Richer motion. This is where the Delight pillar earns its keep.

**Once ever** (first launch, onboarding, account creation): Full theatrical treatment. This moment won't repeat, so invest in it.

### The 50-use test

After building an interaction with animation, use it 50 times in rapid succession. If the animation starts to feel like waiting, remove it or reduce it to instant.

### Keyboard vs touch

Keyboard input has an inherent disconnect from on-screen response. Pressing a key is mechanical and indirect. Keyboard-triggered actions (command palettes, app switchers, shortcuts) almost always feel better without entry animation.

Touch input is visceral and direct. The finger is on the screen. Touch interactions benefit from motion that tracks the finger. But even on touch, very high-frequency actions (pull-to-refresh on a feed checked every 30 seconds) should be minimal.

### Staging: one focal animation at a time

Only one element should animate prominently at any given moment. When a modal opens, everything behind it dims and stills. When a notification enters, it is the only thing moving. When a card expands, neighbouring cards recede.

Competing simultaneous animations split the user's attention and create visual noise. If two elements are animating at the same time, one must be clearly primary and the other clearly secondary (supporting the primary, not competing with it). See surface-motion's secondary action pattern for the implementation side of this.

Background treatments (dimming, blurring, desaturating) are the primary staging tool in UI. They direct focus by reducing everything that isn't the focal element.

---

## 5. Kinetic Physics

Interactions that model real-world physics feel alive. Three properties matter:

### Momentum

When a gesture releases an element mid-motion, the element should continue in the direction it was moving, at a speed proportional to the release velocity, then decelerate to a stop. The final resting position is influenced by the gesture, not predetermined.

### Variable timing

Real objects don't move in perfectly consistent arcs. When a card is swiped away, the angle, speed, and final position should vary based on how it was swiped. If every dismiss animation looks identical regardless of the gesture, it feels robotic.

### Interruptibility

Every animation must be interruptible by a new gesture. If a modal is mid-entrance and the user taps elsewhere to dismiss it, the entrance should stop immediately and the dismiss should begin from wherever the animation currently is. No queuing, no "wait for it to finish."

If your transition system locks out user input for its duration, the interaction is broken. This is the most commonly violated principle in web UI. Test by rapidly triggering and interrupting transitions.

---

## 6. Metaphor Reuse

The fewer gestures a user needs to learn, the more powerful each one becomes. Before inventing a new gesture, check whether an existing one can extend to the new context.

**Swipe dismisses layers.** Swiping up dismisses a lock screen, an app, a notification, a bottom sheet. One gesture, consistent meaning: "move this layer away."

**Pinch adjusts precision.** Pinching zooms in maps, photos, web pages, canvases. The anchor point is always between the fingers. One gesture, universal meaning: "adjust the level of detail."

**Long-press reveals options.** Long-pressing reveals context menus on icons, text, images, list items. One gesture, consistent meaning: "show me more."

A new gesture is a new thing to learn. An extended gesture is a reward for having learned the first one.

---

## 7. Drag Design Patterns

Drag gestures on the web require deliberate decisions about snap behaviour, progressive reveal, and when to suppress physics.

### Snap points

When a dragged element reaches a threshold, it should snap to a defined position rather than landing wherever the user released it. Define discrete snap points (left, centre, right, or open/closed) and a commit threshold.

The decision: if the drag distance exceeds the threshold, snap to the nearest target. If it doesn't, snap back to the origin. This gives the interaction a clear "commit or cancel" feel.

Disable momentum for snap interactions. Momentum (the element continuing to coast after release) makes the final position unpredictable. For swipe-to-reveal actions, you want the element to land precisely on the snap point, not overshoot it. Reserve momentum for free-scrolling contexts like lists and canvases where precise landing positions don't matter.

### Progressive reveal during drag

Not all actions need to appear at once. In a swipe-to-reveal pattern (e.g. swiping a message to show action buttons), reveal actions progressively as the drag distance increases:

- First action appears after a short threshold (e.g. 44px)
- Second action appears after a longer threshold (e.g. 88px)
- Full-swipe commits a primary action

This teaches the user that there are multiple options without overwhelming them. Each action animates in (opacity + scale) as its threshold is crossed.

### Elastic resistance

When a drag reaches its boundary, it should resist further movement rather than stopping dead. Apply diminishing returns to movement past the constraint: the further past the boundary, the less the element moves per pixel of pointer travel.

Low elasticity (0.05) provides minimal overshoot and a tight feel. Higher elasticity (0.3-0.5) feels looser and more playful. Match the elasticity to the context: precision interactions (sliders, snap actions) want low elasticity; playful or exploratory interactions (photo browsing, card stacks) can tolerate more.

### Velocity-based dismiss

Distance alone is not enough to determine whether a gesture should commit. A fast, short swipe should dismiss just as effectively as a slow, long drag. Check both distance and velocity: if the swipe exceeds either the distance threshold or the velocity threshold, commit the action.

Calculate velocity as distance divided by elapsed time. A velocity above ~0.11 px/ms (tune by feel) should commit regardless of distance. This makes swipe-to-dismiss feel responsive to quick flicks, not just deliberate drags.

### Pointer capture

When a user drags an element, their pointer may leave the element's bounds (particularly on fast or diagonal swipes). Without pointer capture, the drag event stops and the element freezes mid-gesture. Set pointer capture on drag start so the element continues receiving pointer events even when the cursor or finger moves outside it.

### Web-specific interaction patterns

Most examples in this skill reference native iOS patterns, but the principles apply equally to the web. Common web implementations:

**CSS scroll-snap** provides native snap points for scroll containers without JavaScript. Use `scroll-snap-type: x mandatory` for carousels and `scroll-snap-type: y proximity` for vertical snap sections.

**IntersectionObserver** triggers state changes when elements enter or leave the viewport: lazy loading, scroll-triggered animations, infinite scroll pagination.

**`:focus-within`** enables parent-level styling when any child receives focus. Useful for form groups, search containers, and navigation that changes appearance when actively used.

---

## Perceptual Heuristics

These heuristics from Laws of UX inform interaction design decisions:

**Fitts's Law.** Time to reach a target depends on its distance and size. Frequent actions go within easy reach. Touch targets are large (minimum 44px). Screen edges and corners are infinitely tall for mouse pointers.

**Hick's Law.** Decision time increases with the number and complexity of choices. Reduce visible options. Use progressive disclosure. A command palette with 200 items is useless without filtering.

**Doherty Threshold.** Productivity soars when response time is under 400ms. If an action will take longer, show a response immediately (optimistic update, progress indicator, skeleton).

**Goal-Gradient Effect.** Effort increases as the goal gets closer. Progress bars, step indicators, and "almost there" states exploit this. Show how close the user is.

**Peak-End Rule.** Experiences are judged by their peak moment and their ending. Invest in completion states (success animations, confirmation screens). A brilliant form experience ruined by a flat "Submitted" message is a wasted opportunity.

---

## Anti-Patterns

1. **Waiting for threshold before feedback.** Every gesture must track from the first pixel. No dead zone before visual response.
2. **Non-interruptible transitions.** If a user can't override a running animation with a new gesture, the interaction is broken.
3. **Uniform dismissal.** Every swipe-to-dismiss landing at the same speed, angle, and position regardless of gesture velocity. It feels mechanical.
4. **Animating keyboard shortcuts.** Command palettes, app switchers, and keyboard-triggered actions should appear instantly.
5. **Spatial lying.** Animating from a direction that doesn't match the element's conceptual origin. If there's no real source, crossfade.
6. **Novel gestures for standard actions.** If swipe, pinch, or long-press can serve the purpose, don't invent something new.
7. **Overanimating high-frequency actions.** If it's used 50+ times a day, strip the animation back to nearly nothing.
8. **Momentum on snap interactions.** Drag-to-reveal and snap-to-position interactions should disable momentum. The element must land on the snap point, not overshoot it.
9. **All actions revealed at once.** Swipe-to-reveal should progressively disclose actions at increasing thresholds, not dump everything at the first pixel.
10. **Hard stop at drag boundaries.** Drags that hit a constraint should resist with elastic diminishing returns, not stop dead.
11. **Competing focal animations.** Two or more elements animating prominently at the same time. One must be primary; everything else must be secondary or still.

---

## Checklist

### Intent
- Lightweight actions trigger during the gesture
- Heavyweight/destructive actions trigger on gesture end
- The cost of accidental trigger is explicitly considered

### Responsiveness
- Every gesture tracks from the first pixel of movement
- No dead zone before visual feedback
- Release animations use gesture velocity, not fixed values

### Spatial Logic
- Elements expand from their trigger's position
- Dismissals reverse their entry direction
- Forward = right, backward = left
- Ambiguous origins use crossfade, not false directional animation
- Shared elements morph continuously between states

### Physics
- Released elements carry momentum
- Final positions vary with gesture speed and angle
- All animations are interruptible by new gestures

### Frequency
- High-frequency keyboard actions have no entry animation
- The 50-use test has been applied to repeated interactions
- Touch interactions track the finger; keyboard interactions are instant
- Only one element animates prominently at a time (staging)
- Background dims/blurs to direct focus during modal and overlay transitions

### Drag
- Snap points are defined with clear commit thresholds
- Momentum is disabled for snap-to-position interactions
- Dismiss checks both distance and velocity (fast short swipes commit)
- Pointer capture is set on drag start
- Swipe-to-reveal progressively discloses actions at distance thresholds
- Drag boundaries use elastic resistance, not hard stops

---

## Learning from Usage

After completing an interaction design task, review the output against the checklist. Append findings to `learnings.md` in this skill's folder. Installed learnings are local runtime notes preserved across suite updates; consult `learnings.md` before starting any new task.
