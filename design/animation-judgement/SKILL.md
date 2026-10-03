---
name: animation-judgement
description: UI animation rules from Emil Kowalski's "Train Your Judgement" (emilkowal.ski/ui/train-your-judgement). Use when writing, reviewing, or critiquing motion — transitions, entries, exits, hovers, popovers, buttons, menus, staggered reveals. Consult before shipping any `transition-*`, `@keyframes`, `framer-motion`/`motion`, or CSS animation change.
---

# Animation Judgement

11 rules for making UI motion feel right instead of just "working." Source: Emil Kowalski, *Train Your Judgement*.

## When to use this skill

Apply proactively when:
- Adding or tweaking any `transition-*`, `@keyframes`, `animate-*`, `duration-*`, `ease-*` class.
- Writing `motion.*` or `AnimatePresence` from `framer-motion` / `motion`.
- Reviewing hover, press, entry, exit, or popover behavior.
- User says a motion "feels off," "sluggish," "janky," "too much," or "delightful but annoying."

Don't invoke for non-motion work.

## Framing

> "AI can write animation code. What it can't do is know what feels *right*. It produces motion that works, but feels mediocre, and if you can't tell the difference, you'll ship it."

The rules below are the named, articulable reasons behind "that feels off."

## The 11 Rules

### 1. Duration scales with distance
- Default: keep UI animations **under 300ms** (tooltips, dropdowns, buttons).
- Exception: large elements (full-screen menus, panels, sheets) need longer durations — a 150ms full-screen slide feels jarring.
- Mental model: a truck takes longer to stop than a bicycle. Heavier-looking things should animate slower.

### 2. Entry animations use `ease-out`
- `ease-in` starts slow → feels sluggish. **Never use for entries.**
- `ease-out` starts fast (instant feedback) and decelerates gently → feels elegant *and* faster.
- Exits can use `ease-in` (element accelerating away).

### 3. Never `scale(0)` — start from `0.90`–`0.95`
- `scale(0)` means "from nowhere" — unnatural.
- Real objects always have a shape (a deflated balloon still has form).
- `scale(0.9)` to `scale(0.95)` preserves the illusion the element was "always almost there."

### 4. Bounce is brand personality, not default behavior
- Bounce = playful. Zero bounce = professional.
- Learning/consumer app: bounce can add energy.
- Finance/enterprise app: bounce feels unserious, wrong for the context.
- **Default: zero bounce.** Add intentionally.

### 5. High-frequency interactions = no animation
- Animation on something used hundreds of times/day becomes annoyance, not delight.
- Hover-highlight fade *looks* smoother in a demo, but **trails the cursor** in real rapid use — the highlight is always one step behind.
- Instant highlights track the mouse perfectly. Direct connection > smoothness.
- Example: Raycast doesn't animate its open because frequent users would hate it.
- Rule of thumb: if the user will trigger this >10×/minute, strip the animation.

### 6. Button press = `scale(0.97)`, not `0.9`
- `0.9` (10% shrink) is visibly too aggressive in most product UIs.
- `0.97` is barely visible but still felt — subtlety reads as quality.
- Go lower (0.92–0.95) only for intentionally playful brands.
- Red flag: if you can clearly *see* the button shrinking in a recording, it's too much.

### 7. Use `mode="popLayout"` when removing list items
- Default `AnimatePresence`: exit animation finishes → *then* siblings reflow into the gap. Causes a visible pause.
- `mode="popLayout"`: exiting element leaves document flow on frame 1; siblings reflow **in parallel** with the exit. Feels tight.
- Applies to chips, tags, list rows, toast stacks — anything where removal triggers sibling reflow.

### 8. CSS transitions > CSS keyframes for toggleable UI
- Keyframes **jump to the new end state** when re-triggered mid-animation.
- Transitions **smoothly animate to the new target** from wherever they currently are.
- Applies to menus, modals, accordions, drawers — anything a user can toggle rapidly.
- If a user rapid-clicks and sees a jump, you used keyframes where you wanted a transition.

### 9. Popovers: `transform-origin` at the trigger
- Default `transform-origin: center` makes popovers appear "from nowhere."
- Origin at trigger location creates cause-and-effect: "I clicked this, this came from it."
- Radix UI and Base UI expose CSS variables for this (`--radix-popover-content-transform-origin`, etc.). Use them.

### 10. Stagger by hierarchy, never uniform
- Uniform stagger (same delay, duration, distance per element) = the motion equivalent of `linear` easing. Feels artificial.
- Vary timing: the most important element appears first and gets screen time alone before supporting elements follow.
- Decorative elements (badges, pills) can fade-only — no slide — because they matter less.
- Questions to ask before staggering: Which element matters most? Which is supporting? Which is decorative?

### 11. Don't stack entry animations
- Panel slides in → *then* menu items stagger in = two layers; user waits twice.
- Panel slides in → content is just there = faster, cleaner, readable immediately.
- **"Sometimes the best animation is no animation."**

## Meta-principles

- **Demo-polish ≠ product-quality.** (Rule 5) What looks better in a 5-second demo can be worse in actual repeated use.
- **Subtlety reads as quality.** (Rule 6) If the effect is obvious, it's probably overdone.
- **Absence is a valid choice.** (Rules 5, 11) "No animation" is often the right answer.
- **Context determines correctness.** (Rule 4) Bounce, stagger, duration all depend on brand + frequency, not universal "best."

## How to apply in review

When reviewing motion code, check in this order:
1. Does the element need animation at all? (Rule 5, 11)
2. Is duration appropriate for the element's size? (Rule 1)
3. Entry uses `ease-out`? (Rule 2)
4. Scale starts from 0.9+, not 0? (Rule 3)
5. Button press ≤ `scale(0.97)`? (Rule 6)
6. Removals use `popLayout`? (Rule 7)
7. Toggleable UI uses CSS transitions? (Rule 8)
8. Popover `transform-origin` anchored to trigger? (Rule 9)
9. Stagger has varied timing by importance? (Rule 10)
10. Bounce intentional for the brand, not accidental? (Rule 4)

## Source

https://emilkowal.ski/ui/train-your-judgement — captured 2026-04-19. Interactive page with 11 A/B exercises; each rule's "Vocabulary" line above is Emil's verbatim compression.
