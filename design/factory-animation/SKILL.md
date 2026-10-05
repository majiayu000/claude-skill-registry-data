---
name: factory-animation
description: Motion discipline distilled across builds. Attention as a fixed per-viewport budget, figure/ground separation (calm the ground, load motion into the figure), one focal point of motion per screen, diegetic-over-decorative test, trigger-on-intent-then-settle over perpetual loops, and the prefers-reduced-motion fallback. Recipe pairs Astro with a Remotion video kit (rendered assets in public/). Read whenever you add motion to a marketing surface or any page where movement competes with reading. Paired with factory-design, which owns the static visual vocabulary motion sits on top of.
---

# Factory animation

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the Astro + Remotion shape we use), and **Failure mode** when there's one to name.

Motion is the most expensive ink on the page. `factory-design` sets the static vocabulary; this skill governs what's allowed to move on top of it. The default answer is "almost nothing" — and that's a feature.

## Attention is a fixed budget per viewport

**Principle.** Every viewport hands the eye one budget of attention; each moving or high-contrast element draws against it, and decorative motion draws without informing.

**Why.** The eye doesn't have a separate fund for "tasteful" animation — a shifting gradient and the headline you actually want read are competing for the same fixed pool. Designers reason about each animation in isolation ("this glow is subtle, this loop is slow") and never sum the bill, so a page that's calm element-by-element is noisy in aggregate. The discipline is to treat the budget as scarce: spend it where it informs, and treat every decorative draw as a debit against the thing you wanted seen.

**Recipe.** Before adding any motion, name what it teaches the viewer. If the honest answer is "it makes the page feel alive," it's a debit with no credit — cut it. Budget one deliberate spend per viewport (next section), not one per component.

## Figure/ground discipline — calm the ground, move the figure

**Principle.** The background is *ground* — it must recede: flat, low-contrast, static. Contrast and motion belong to the *figure*.

**Why.** This is the single highest-leverage rule in the skill, because animated or patterned backgrounds are the most common source of a noisy landing page. A shifting gradient, a drifting grid, a scanline sweep, an ambient glow — each sits *behind* the content and so competes with every word in front of it, everywhere, all the time. Ground that moves can never recede, so the figure can never read cleanly no matter how good it is. The fix is structural, not cosmetic: flatten the ground to a static low-contrast field and load all the contrast and motion you were tempted to spread around into the one figure that earns it.

**Recipe.** Background is a flat theme color (`bg` from `factory-design`), no animated pattern layer. If a texture is non-negotiable, it's static and below the contrast floor of body text. Render motion assets *onto* that flat ground so the rendered frame and the live page share one background — no seam, no second competing field.

**Failure mode.** A patterned or animated background behind everything — grid, shifting gradient, glow, scanlines. It reads as "alive" in isolation and "noisy" the moment real content sits on it. Calm the ground first; it fixes more than any per-component tweak.

## One focal point of motion per viewport

**Principle.** At most one thing moves per screen; if two move, they fight.

**Why.** Motion is a pointer — it says "look here." Two simultaneous motions issue two contradictory pointers, and the eye, unable to obey both, settles on neither and reads the screen as busy rather than directed. One focal motion per viewport keeps the pointer unambiguous: the moving element *is* the thing you wanted looked at. The cost is restraint — most components stay still even when you could animate them. The benefit is that the one animation you keep actually directs attention instead of joining a scrum.

**Recipe.** One animated component per scroll-height of viewport; everything else around it is static. When a second candidate for motion appears on the same screen, the question isn't "how do I make them not clash" — it's "which one earns the spend, and the other holds still."

## Diegetic over decorative — motion demonstrates the product

**Principle.** Motion exists to show the product working — a timeline ticking, a value filling, a terminal typing, a standard drifting — never to ornament.

**Why.** Diegetic motion (motion that belongs to the product's own world) pays for its attention cost by teaching: the viewer watches the thing *do its thing* and understands it better than a static screenshot could convey. Decorative motion teaches nothing and so is pure debit against the attention budget. The discriminating test is a counterfactual: *if this animation demonstrated nothing about the product, would the page be worse without it?* If the answer is no, it's ornament — cut it. Most "nice touch" animations fail this test, and cutting them is a net gain, not a sacrifice.

**Recipe.** Animate the product surface itself — a metric counting up to its real value, a log streaming, a chart drawing in, a process advancing a step. Don't animate chrome: section dividers, decorative shapes, floating particles, the logo. The motion should be something a screen recording of the real product would also show.

## Trigger on intent, settle fast — no perpetual loops

**Principle.** Animate once when the component enters view, then hold the end-state; "play once on scroll, then hold" beats "loop forever."

**Why.** A loop never lets the eye rest. Even a subtle perpetual animation — a pulsing dot, a breathing glow, a gradient that cycles — re-fires the "look here" pointer indefinitely, so the viewer can never finish reading and move on; it reads as low-grade noise precisely because it has no end. Triggering on intent (the component scrolling into view) spends the attention budget exactly when the viewer arrives, then settling to a held end-state returns the budget so the rest of the page can be read. The end-state is also a free static poster for the reduced-motion and pre-scroll cases (next section).

**Recipe.** Scroll-trigger reveals via `IntersectionObserver`; play the animation once on first intersection, then settle and unobserve. The hero demo is the one allowed exception — a single looping autoplay video, because it *is* the product demonstration and the page has exactly one. Everything else plays once and holds.

**Failure mode.** Pulsing dots, breathing glows, looping ambient gradients, "alive" indicators — multiple of them per screen, each a small perpetual draw the eye can never finish. Even subtle, they sum into the noisy feel calm-element-by-element review never catches.

## Always ship a reduced-motion end-state

**Principle.** Every animation has a static poster — its settled end-state — served to `prefers-reduced-motion`.

**Why.** Reduced-motion isn't a preference to degrade gracefully toward; for some users motion is a vestibular trigger, so it's a correctness requirement. The cheap way to honor it is structural rather than bolted-on: because "play once then hold" already produces a meaningful end-state, that frame *is* the reduced-motion poster. A design that has no sensible static end-state is usually a decorative loop in disguise — the reduced-motion requirement doubles as a diegetic check.

**Recipe.** Wrap motion in `@media (prefers-reduced-motion: reduce)` (or the JS `matchMedia` equivalent) and render the settled end-state — the final video frame as a poster image, the counter at its real value, the chart fully drawn. For the hero video, set `poster` to the last frame and don't autoplay under reduced-motion.

## One signature motif, used sparingly

**Principle.** Pick a single recurring visual motif and use it as a rare accent, not a wallpaper.

**Why.** A signature motif (registration marks, a corner bracket, a single recurring glyph) builds brand recognition cheaply *because* it's rare — its scarcity is what makes it read as a mark rather than a texture. Apply it to every surface and it stops being a signature and becomes the patterned ground this skill spent its second section telling you to calm. The motif and the figure/ground rule are the same rule seen twice: identity comes from a sharp accent against quiet ground, never from filling the field.

**Recipe.** One motif (e.g. registration marks framing the hero demo), placed on one or two surfaces total — not on every section header, card, and divider. If the motif is starting to feel like a background, it's being overused; pull it back to the single surface where it lands hardest.

## Source patterns

The Astro + Remotion split: motion assets are rendered in the Remotion video kit and emitted to `public/` as `.mp4`/poster pairs; the Astro page mounts them on the flat `bg` ground, autoplay-loops the single hero demo, and `IntersectionObserver`-gates the supporting figures to play-once-then-hold. Pairs with `factory-design` (the static token vocabulary the motion sits on) and `factory-frontend` (loading/empty/error states are the non-motion sibling of "always ship an end-state").
