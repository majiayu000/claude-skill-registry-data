---
name: motion-director
description: Design and audit interface motion so every animation explains something - direction, amount, cause, state - with a shared vocabulary of durations and easings, interruptible transitions, cheap properties and a real reduced-motion version. Includes a Playwright script that records every animation a page runs and flags layout-costly, overlong, inconsistent or reduced-motion-violating motion. Use when adding animation, when motion feels random or sluggish, or before shipping animated UI.
---

# /motion-director

Motion is information delivered over time. Every animation should answer a question the user has in that moment:

- Where did it go?
- What changed, and by how much?
- What caused this?
- Is it still working?
- What happens next?

If an animation answers none of these, it's decoration. Make it much quieter or remove it.

## 1. Say what each motion explains

List every moving thing and write one line for each: *"The indicator stretches toward the new tab, so you see the direction and distance of the change."* If the line ends in "…so it feels nice" or "…to add polish", cut the motion or merge it into one that does explain something.

Good jobs for motion:

| Job | Example |
|---|---|
| **Continuity** | An item moves to its new place instead of disappearing and reappearing, so you can follow it (FLIP). |
| **Direction and distance** | An indicator stretches toward its target before it settles. |
| **Amount** | Only the digits that changed turn over, so the size of a change is visible. |
| **Cause** | The thing you pressed is where the change starts. |
| **State** | A slow breath only while the system is waiting on you or on the network, and nowhere else. |
| **Time** | Remaining time shown as a line that shortens. |

## 2. Build a vocabulary

A site needs few motions, used consistently. Define them once as tokens:

```css
:root {
  --dur-press: 120ms;   /* response to a press or toggle */
  --dur-move: 280ms;    /* things changing place or size */
  --dur-enter: 420ms;   /* things arriving; leaving is ~70% of this */
  --dur-story: 900ms;   /* rare, deliberate moments: a first load, a completed task */
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);      /* arrive and settle */
  --ease-in-out: cubic-bezier(0.65, 0, 0.35, 1);  /* move between two places */
  --ease-in: cubic-bezier(0.7, 0, 0.84, 0);       /* leave */
}
```

Rules of thumb:

- **Responses land in 120–400 ms.** Longer feels sluggish unless the user is watching a story unfold.
- **Leaving is faster than arriving.**
- **Bigger distance means a longer duration**, but not proportionally: 300 px might take 320 ms, 1000 px 480 ms.
- **Springs and overshoot only where the material would do it**, like a liquid or a spring. Never on text.
- **Stagger by at most 30–60 ms per item**, and cap the total. Ten items must not take a second to arrive.
- **Don't animate on scroll by default.** Content that fades up as you scroll makes reading slower. Reserve it for one moment per page, if any.

## 3. Build it properly

- **Animate `transform` and `opacity`.** Animating width, height, top or left runs layout every frame. That's acceptable for one small positioned element and a problem for anything large or repeated.
  - To animate height, use `grid-template-rows: 0fr → 1fr`.
  - For moving between layouts, use FLIP: measure, invert with a transform, play.
- **Make it interruptible.** A second click mid-animation must start from where things are now, not jump to the end first. CSS transitions do this for free; keyframe animations and timelines usually need `getAnimations()` or the current computed value.
- **Never block input** while something animates.
- **Stop what isn't seen.** Loops and canvases pause when offscreen (IntersectionObserver) or when the tab is hidden, and run slower on low-power devices.
- **No layout shift.** Reserve the space before content arrives, so motion never pushes what you're reading.

## 4. Reduced motion is a design, not an off switch

Under `prefers-reduced-motion: reduce`, and ideally a `motion="reduced"` prop too, keep the **information** and drop the **travel**:

- movement becomes a short crossfade (≤150 ms) or an instant change
- parallax, drift, loops and autoplay stop
- progress still shows, as a static bar instead of a moving one
- nothing that conveyed meaning disappears: if the stretch showed direction, the reduced version still highlights the destination

## 5. Audit

Save this as `motion.mjs` in a scratch directory (it needs `playwright`) and run it against the running app:

```
node motion.mjs http://localhost:3000/pricing --click "[role=tab]:nth-of-type(2)"
```

It records every CSS animation, transition and Web Animation during load and after an optional `--click` or `--hover`.

- It prints a table: target, name, duration, delay, easing, loops, and animated properties.
- It flags:
  - more than six durations or four easings
  - layout-property animation
  - responses over 700 ms
  - infinite loops
  - anything that still moves under reduced motion

```js
// Motion audit: records every animation and transition a page runs (on load, and after an optional
// click or hover), then loads it again with reduced motion on and records what still moves.
import { chromium } from "playwright";

const [url, ...rest] = process.argv.slice(2);
if (!url) {
  console.error('usage: node motion.mjs <url> [--click "<selector>"] [--hover "<selector>"]');
  process.exit(1);
}
const flag = (name) => {
  const i = rest.indexOf(name);
  return i >= 0 ? rest[i + 1] : null;
};
const click = flag("--click");
const hover = flag("--hover");
const LAYOUT = /^(width|height|top|left|right|bottom|margin.*|padding.*|inset.*|font-size|line-height|gap|grid-template.*|flex-basis)$/;

async function record(reduced) {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 }, reducedMotion: reduced ? "reduce" : "no-preference" })).newPage();
  await page.goto(url, { waitUntil: "load" });
  await page.evaluate(() => {
    window.__motion = new Map();
    const label = (el) => (el ? el.tagName.toLowerCase() + (el.id ? "#" + el.id : "") + (typeof el.className === "string" && el.className ? "." + el.className.trim().split(/\s+/)[0] : "") : "?");
    const sample = () => {
      for (const a of document.getAnimations()) {
        const t = a.effect?.getTiming?.() ?? {};
        const kf = a.effect?.getKeyframes?.() ?? [];
        const props = [...new Set(kf.flatMap((k) => Object.keys(k).filter((p) => !["offset", "easing", "composite", "computedOffset"].includes(p))))];
        const name = a.animationName || a.transitionProperty || a.id || "script";
        const key = label(a.effect?.target) + "|" + name;
        if (!window.__motion.has(key))
          window.__motion.set(key, { target: label(a.effect?.target), kind: a.constructor.name.replace("Animation", "").toLowerCase() || "script", name, ms: Number(t.duration) || 0, delay: t.delay || 0, easing: t.easing, loops: t.iterations, props });
      }
    };
    window.__timer = setInterval(sample, 50);
  });
  await page.waitForTimeout(2500);
  if (hover) {
    await page.hover(hover);
    await page.waitForTimeout(1500);
  }
  if (click) {
    await page.click(click);
    await page.waitForTimeout(2000);
  }
  const list = await page.evaluate(() => (clearInterval(window.__timer), [...window.__motion.values()]));
  await browser.close();
  return list;
}

const full = await record(false);
const reduced = await record(true);

const camel = (p) => p.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase());
console.log(`\n# Motion on ${url}\n`);
console.log("target | kind | name | ms | delay | easing | loops | properties");
for (const m of full) console.log([m.target, m.kind, m.name, m.ms, m.delay, m.easing, m.loops, m.props.map(camel).join(" ")].join(" | "));

const durations = [...new Set(full.map((m) => m.ms).filter(Boolean))].sort((a, b) => a - b);
const easings = [...new Set(full.map((m) => m.easing).filter(Boolean))];
const layout = full.filter((m) => m.props.map(camel).some((p) => LAYOUT.test(p)));
const long = full.filter((m) => m.ms > 700 && m.loops !== Infinity);
const infinite = full.filter((m) => m.loops === Infinity);
const stillMoving = reduced.filter((m) => m.ms > 150 && !m.props.map(camel).every((p) => p === "opacity" || p === "color" || p.startsWith("background")));

console.log(`\n${full.length} animations · ${durations.length} distinct durations (${durations.join(", ")} ms) · ${easings.length} distinct easings`);
if (durations.length > 6) console.log("! More than six durations: the motion has no shared vocabulary.");
if (easings.length > 4) console.log("! More than four easings: pick a few and name them.");
for (const m of layout) console.log(`! Animates layout (${m.props.map(camel).filter((p) => LAYOUT.test(p)).join(", ")}): ${m.target} ${m.name}. Runs layout every frame: fine for one small positioned element, a problem on large or many elements; prefer transform.`);
for (const m of long) console.log(`! Long (${m.ms} ms): ${m.target} ${m.name}. Interface responses should land in 120–400 ms.`);
for (const m of infinite) console.log(`· Loops forever: ${m.target} ${m.name}. Make sure it pauses offscreen and stops for reduced motion.`);
console.log(`\nWith reduced motion: ${reduced.length} animations, ${stillMoving.length} still move something other than opacity or colour.`);
for (const m of stillMoving) console.log(`! Still moves with reduced motion: ${m.target} ${m.name} (${m.props.map(camel).join(" ")}, ${m.ms} ms)`);
```

Then look, because numbers can't judge meaning:

1. Record the interaction at normal speed, then slow it down: in Chrome DevTools, open Animations and set it to 25%.
2. Interrupt everything: click twice quickly, reverse mid-way, resize during a transition.
3. Use it with the keyboard. Motion must follow focus the same way it follows the pointer.
4. Turn on reduced motion (DevTools › Rendering › Emulate CSS prefers-reduced-motion) and repeat.

## Report

For each moving thing, give it a verdict:

- **keeps**
- **tune:** with the exact duration or easing change
- **replace:** with the transform-based version
- **cut:** with the reason

Say what the motion explains, and note anything that fails reduced motion or interruption. End with the vocabulary tokens the project should adopt if it doesn't have them.
