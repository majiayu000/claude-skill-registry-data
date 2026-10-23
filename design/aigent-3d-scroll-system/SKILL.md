---
name: aigent-3d-scroll-system
description: Build premium AIgent-style 3D scroll web experiences with Spline, GSAP, Three.js, or Blender frame sequences. Use when creating or improving immersive landing pages, scroll-driven 3D backgrounds, asset galleries, cinematic product pages, Spline embeds, GSAP reveals, or mobile-safe premium web experiences that need strong taste and real browser verification.
---

# AIgent 3D Scroll System

Use this skill to build immersive web pages that feel designed, not generated.

## First Decision

Choose the lightest 3D technique that can carry the idea:

- Use **Spline embed** for fast immersive backgrounds and interactive scenes.
- Use **Blender frame sequence** for photoreal art direction and mobile-safe cinematic scroll.
- Use **Three.js** only when the page needs live interaction, procedural geometry, or real-time lighting.

Do not add random floating objects. The scene should support the story.

## AIgent Pattern

1. Start with a full-viewport scene.
2. Anchor a clear focal point.
3. Map scroll progress to scene progress.
4. Reveal text and cards only when they are readable.
5. Keep copy short and plain.
6. Verify mobile before calling it done.

## Spline Scroll Mapping

Use CSS variables to keep the animation simple and inspectable:

```js
const max = document.documentElement.scrollHeight - window.innerHeight;
const p = Math.min(1, Math.max(0, window.scrollY / max));
const scene = Math.min(1, p * 1.8);
root.style.setProperty("--scene-scale", (1 + scene * 1.4).toFixed(3));
root.style.setProperty("--scene-rotate", `${(scene * -72).toFixed(2)}deg`);
root.style.setProperty("--scene-x", "0px");
root.style.setProperty("--scene-y", "0px");
```

If the background effect is only half done when the page ends, increase the multiplier. If it finishes too early, lower it.

## Focal Point Rule

For tunnels, vortexes, and control-room backgrounds:

- Keep x/y translation at zero.
- Use scale and rotation for movement.
- Set `transform-origin` to the visual center.
- Do not let the center drift diagonally as the user scrolls.

## Text Rules

- H1 should fit the first viewport.
- Body copy should be 1-2 sentences.
- Avoid explaining features twice.
- Use plain labels over technical labels when the audience is not technical.
- Do not place dense copy over a busy part of the scene.

## Animation Rules

- Use GSAP for hero load and scroll reveals.
- Trigger reveals earlier on mobile.
- Animate cards one at a time for long lists.
- Use `prefers-reduced-motion`.
- Hover states should feel premium: slight lift, border glow, no cartoon scaling.

## Cinematic Deck Rules

When a hero loop hands off into a pinned video-scrub deck:

- Target the deck boundary on click, not a nested sticky scene anchor.
- For presented sponsorship decks, block free scrolling after entry and drive the internal scroll timeline with clear `Next` and `Previous` controls.
- Land guided moves on approved pause points where the clip is near its end state and copy is fully rendered.
- Reveal opening copy immediately on the first scrub frame or first approved pause point.
- Use one source of truth for opening copy. Do not add a duplicate overlay unless the scene copy is removed or hidden.
- Hide generic `Scroll` cues on the first deck slide after the hero.
- Make deck copy enter from the side closest to its layout anchor, not bottom-up by default.
- Give video-to-video transitions enough scroll distance to read. Push transitions should move opaque video, not behave like crossfades.
- Treat videos as scrub-ready on `canplay` or `readyState >= 2`, not metadata alone.
- Use 1080p scrub exports with frequent keyframes or all-intra encoding when clarity matters. Do not downgrade to blurry media to mask seek problems.
- Load the hero poster and hero loop first, warm the first scrub clip on CTA intent, then warm later clips only near their transition windows.
- Match video seek cadence to the source frame rate instead of seeking on every possible scroll tick.
- Confirm MP4 range requests return `206` and `Accept-Ranges: bytes`.
- Pin sticky facts only after their source slide has left.
- On mobile, use `object-fit: contain` for a hero loop that contains a readable brand mark.

For the full checklist, read `docs/cinematic-scroll-deck-playbook.md` in this repo.

## Verification

Before final:

- Desktop screenshot at 1440px.
- Mobile screenshot around 390px.
- Confirm no horizontal scroll.
- Confirm active sticky nav does not cover content.
- Confirm scene reaches its intended end state by the page bottom.
- Confirm links and external-link cues are actually clickable.
- For guided scrub decks, click through every `Next` and `Previous` pause point and inspect active video `currentTime`.
- Confirm the first page load does not request all 1080p scrub videos before interaction.

Use browser tooling or Playwright, not visual guessing.
