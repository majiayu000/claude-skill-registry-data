---
name: interaction-polish
description: "Elevate the feel, polish, and 'juice' of UI interactions and animations, in the craft tradition of Emil Kowalski (sonner, vaul) and Josh Comeau. Apply it WHENEVER the user wants an interface to feel better, smoother, more polished, responsive, satisfying, delightful, or 'alive'; when they say an interaction feels stiff, janky, dead, cheap, flat, or off; when they mention adding animation, motion, micro-interactions, springs, transitions, easing, or hover/press effects; or when they ask to 'add juice', 'make it feel good', 'make it satisfying', or 'polish' a button, modal, toast, drawer, toggle, menu, list, or page transition. Works on existing components (improves them in place) or a described interaction (builds it), CSS-first and adapting to the project's stack, with accessibility (prefers-reduced-motion) and performance (compositor-only) built in, and the taste to know when NOT to animate. Trigger phrases: 'make this feel nicer', 'add some juice', 'this feels stiff', 'this feels janky', 'polish this interaction', 'make it satisfying', 'improve the animation', 'it feels cheap', 'make it more delightful', 'give it some life'."
---

# Interaction Polish: the craft of feel

The goal is not "add animations." It is to make an interaction feel **considered**, 
responsive, alive, and effortless, the way Emil Kowalski's (sonner, vaul) and Josh Comeau's
work feels. Often that means adding one small, well-tuned piece of feedback. Sometimes it means
*removing* animation that's getting in the way. This skill is the taste to tell the difference,
plus the concrete technique to execute it well.

> "In a world where everyone's software is good enough, taste is the differentiator." (Emil Kowalski)

## The one idea: feedback, not decoration

Game designers have a word for this: **juice**. The same action can feel *dead* or *alive*
purely from the feedback layered on top, without changing what the action does or slowing the
user down. A button that instantly swaps state feels dead; the same button with a 120ms
scale-and-spring-back feels alive. In the anatomy of a micro-interaction (Trigger → Rules →
**Feedback** → Loops), juice lives in the *feedback* layer.

So the operating principle is: **add the smallest feedback that confirms the action, and add
flourish only at genuine moments** (a success, a completion, a first-time delight). Decoration
that doesn't answer *"did my action register / what changed / where did it go?"* is noise.

## First, do no harm

The fastest way to make UX *worse* is to over-animate. Internalize these before touching
anything. Most are about restraint, and they're what separate this skill from cargo-cult
"add a fade everywhere":

- **Never make the user wait.** If interaction pauses while motion plays, you've made the app
 *slower*. Don't block input on an animation; keep anything on the user's path well under
 300ms; prefer non-blocking feedback that the user can interrupt or tap through.
- **Frequency-gate every animation.** The more often a user triggers an action, the less it
 should animate. Emil's rule: **100+ times/day (keyboard shortcuts, command palette, core
 nav) → no animation at all**; motion there reads as lag. Tens/day (hovers, list nav) →
 tiny and fast or none. Occasional (modals, toasts) → standard. Rare/first-time → room for
 delight. Raycast feeling instant is the goal, not a flourish.
- **Every animation needs a job.** Spatial continuity, state change, feedback, explanation, or
 softening a jarring jump. If the only reason is "it looks cool" and the user sees it often,
 don't.
- **Accessibility and performance are not optional.** Ship the `prefers-reduced-motion` path
 and compositor-only properties *by default*, not as an afterthought. See
 `references/accessibility-performance.md`.
- **Delight is rare by nature.** A boop, a particle burst, a celebration works *because* it's
 uncommon. The litmus test: *would this still be charming on the 50th encounter?* If no, make
 it rarer, quieter, or motion-free.

## Workflow

1. **Read the interaction and its frequency.** What is it (button, toggle, modal, drawer,
 toast, tabs, list, reveal, page transition)? How often will a real user hit it? What does it
 do *now*? an instant snap? a `transition: all`? a slow sluggish fade? The frequency decides how
 much (or whether) to animate; the current state tells you the highest-leverage fix.

2. **Decide what should animate, and what shouldn't.** Sometimes the best change is to *remove*
 a gratuitous animation or a layout-thrashing one. Pick the 1-3 changes that will move the
 feel the most rather than touching everything.

3. **Apply, CSS-first, in the project's idiom.** Default to CSS transitions/animations; they
 run off the main thread and stay smooth under load. Reach for a spring / JS motion library
 only when the motion is *dynamic, interruptible, or gesture-driven* (drag, momentum,
 physical "alive" elements). Match whatever the codebase already uses (vanilla CSS, Tailwind,
 Framer Motion / Motion, Vue/Svelte transitions); don't introduce a new dependency unless the
 interaction genuinely needs it.

4. **Make it correct by default.** Animate only `transform` and `opacity`. Name exact
 properties (never `transition: all`). Add the `prefers-reduced-motion` variant (keep fades,
 drop movement). Gate hover effects behind `(hover: hover)`.

5. **Apply the change AND explain the why.** Edit the code, then briefly walk through each
 change and the principle it serves, so the user gains the taste, not just a diff. Keep
 explanations tight (a line each). If you removed something, say why that's the improvement.

## The core toolkit (condensed, deep tables in `references/`)

- **Easing.** `ease-out` for things entering/exiting (fast start = feels responsive); never
 `ease-in` on UI (it delays the moment the user is watching); `ease-in-out` for things moving
 across the screen; plain `ease` is fine for hover color changes; `linear` only for constant
 motion (spinners, marquees), never for spatial movement. Built-in curves are weak; prefer a
 strong custom one like `cubic-bezier(0.23, 1, 0.32, 1)`. **Easing is the single highest-leverage
 variable.** Full curves, durations, and spring configs are in
 `references/easing-springs-timing.md`.

- **Duration.** Keep UI under **300ms**. Button press 100-160ms · tooltip 125-200ms · dropdown
 150-250ms · modal/drawer 200-500ms. Make it **asymmetric**: respond fast to the user, return
 to rest a touch slower; generally exits faster than enters.

- **The press.** Every pressable element should acknowledge touch: `:active { transform:
 scale(0.97) }` with a ~150ms ease-out transition. It's the cheapest possible "the UI is
 listening." Subtle range 0.95-0.98.

- **Springs vs. transitions.** Springs shine for drag/momentum and "alive" elements *because
 they keep velocity when interrupted*: a CSS keyframe restarts from zero, whereas a spring reverses
 smoothly mid-gesture. Use CSS **transitions** (not keyframes) for anything retriggered rapidly
 (toasts, toggles) so it retargets instead of restarting.

- **Don't scale from zero.** Enter from `scale(0.95)` + `opacity: 0`, not `scale(0)`. Real
 things don't blink in and out of existence.

- **Restraint flourishes.** The boop (a momentary, self-resetting hover wiggle), particle
 bursts, confetti, hit-flashes are powerful precisely because they're rare. Recipes in
 `references/patterns.md`.

## When the input is a description (no code yet)

Build the interaction from scratch applying everything above. Choose the project's stack if one
exists; otherwise default to CSS + a minimal motion approach. Produce real, runnable code, not
pseudocode, and still explain the choices.

## References

Read the relevant one when you need depth; don't load all of them for a small tweak.

- **`references/easing-springs-timing.md`**, the easing decision tree, concrete cubic-beziers,
 the duration table, spring configs (Apple-style & physics), and CSS `linear()` overshoot for
 native springs.
- **`references/patterns.md`**, per-component recipes: button, toggle, like/favorite, modal,
 drawer/sheet, toast, tabs, accordion, hover/focus, drag-reorder, loading (optimistic /
 skeleton), scroll reveal, page transition. Includes the sonner/vaul drag mechanics and Josh's
 "boop" and "friendly shadow" techniques.
- **`references/accessibility-performance.md`**, `prefers-reduced-motion` (what to keep vs.
 drop), compositor-only properties, `will-change` as a scalpel, and the full anti-pattern list.
