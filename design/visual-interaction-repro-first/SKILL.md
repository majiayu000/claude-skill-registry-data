---
name: visual-interaction-repro-first
description: Reproduce visual or interactive defects whose correctness depends on browser rendering, timing, viewport, input sequence, animation state, computed layout, or performance before fixing them. Use this whenever an animation, motion, responsive layout, scroll, resize, drag, hover, focus, visual transition, View Transition, Motion/FLIP, clipping, blur, jank, or "it looks wrong" report cannot be conclusively proven from data, unit tests, or static code reading alone.
---

# Visual Interaction Repro First

Use this skill when the reported problem is visual or interactive enough that code reading alone can point in the wrong direction.

The goal is to create a concrete reproduction path before changing code, then use the same path to prove the fix. For animation and UI interaction bugs, reproduction often takes longer than the patch. That is normal and usually cheaper than debugging the wrong hypothesis.

## Core Principle

Do not start with a fix. Start with a witnessed failure.

A visual interaction bug is considered witnessed when you can state:

- exact page, route, story, or component surface
- viewport/device scale/browser if relevant
- user interaction sequence
- expected visual behavior
- actual visual behavior
- one piece of evidence: screenshot, video, extracted frame, DOM/computed-style sample, animation-frame sample, or performance trace

If the evidence is ambiguous, keep reproducing. Ambiguous evidence is still useful for forming hypotheses, but it is not enough to justify a code change.

## Reproduction Gate

Before editing code, pass this gate unless the user explicitly asks for analysis only or the defect is already mechanically proven.

Mechanically proven means the failure follows directly from one of these:

- a failing visual/e2e test that already captures the target interaction
- a user-provided screenshot or video with enough route, viewport, state, and steps to identify the broken browser-rendered behavior
- a deterministic DOM/CSS invariant, such as a selector that is always fixed-positioned when the product contract requires normal flow

Instrumentation-only edits are allowed before the gate when they are needed to expose state, add a debug id, or make sampling possible. Keep them temporary or clearly separated from the fix.

1. **Restate the target behavior**
   - Convert the user's report into a precise visual invariant.
   - Example: "The tab bar should translate with the right panel during expand/collapse; it should not appear pinned to the page."

2. **Find the live surface**
   - Prefer the exact app URL, Storybook story, or local dev server the user referenced.
   - If a server is already running, use it. Do not create a parallel surface unless needed.
   - Record the URL and viewport used.

3. **Capture the failure**
   - Use the lightest tool that can make the failure undeniable.
   - Screenshots are enough for static wrong states.
   - Video or frame extraction is better for timing, disappearance, flashing, clipping, or cross-fade problems.
   - Animation-frame DOM sampling is better when an element appears fixed, drifting, clipped, or transformed.
   - Performance traces are better when the claim is about jank, layout storms, or repeated expensive reflow.

4. **Localize the moving parts**
   - Identify the element the user is looking at.
   - Identify the container it should follow.
   - Sample both geometries over time when motion is involved.
   - Inspect computed `transform`, `opacity`, `filter`, `clip-path`, dimensions, and view-transition pseudo-element styles when relevant.

5. **State the reproduction result before fixing**
   - Tell the user or record in notes what you observed.
   - Include the evidence type and the concrete mismatch.
   - Example: "During toggle, the panel `left` changed from 565 to 746, while the tablist stayed at 788 and had computed transform `matrix(...)`."

Only then start implementation.

## Tool Selection

Pick the tool based on the defect shape, not habit.

### Screenshots

Use screenshots when:

- the bug is visible in a stable state
- layout, clipping, spacing, z-index, or wrong initial render is the issue
- the user supplied a screenshot and you need to compare your result

Good screenshot notes include URL, viewport size, device scale factor, and the interaction state.

### Video And Frame Extraction

Use video or extracted frames when:

- the bug is a flash, jump, instant disappearance, or wrong transition timing
- old/new layers appear to cross-fade incorrectly
- blur enters or exits at the wrong time
- an element is correct at rest but wrong during the transition

When the user supplies a video, inspect frames around the reported moment. Do not rely only on watching it once at normal speed.

Useful outputs:

- frame number or timestamp where the first wrong state appears
- a short sequence of frames showing before, failure, and after
- a note about which layer moved, disappeared, changed scale, or lost blur

### Animation-Frame Sampling

Use requestAnimationFrame or Playwright/CDP evaluation when geometry needs proof.

Sample:

- `getBoundingClientRect()` for the moving container and suspect child
- computed `transform`, `opacity`, `filter`, `clip-path`, `width`, and `height`
- relevant attributes or CSS variables driving the animation

This is the right tool for "it looks fixed in place", "it jumps to the center", "the old screenshot is offset", and "the panel moves but the control does not follow."

Prefer before/after samples in the same format so the fix is easy to verify.

### DevTools, CDP, Playwright, And Agent Browser

Use whichever browser control path is already ready in the environment:

- `agent-browser` for quick screenshots, recordings, and page interaction when that skill is available.
- Playwright for deterministic repro scripts, viewport control, screenshots, video, and trace collection.
- Chrome DevTools Protocol for direct sampling on an existing user-visible Chrome session.
- DevTools MCP when you need Performance panel traces, layers, computed styles, or the exact active page state.

If the page uses View Transitions or visibility-sensitive APIs, activate the target tab before sampling. Hidden documents can reject or skip transitions and create false negatives.

### Minimal Playwright Geometry Recipe

Use a short script when you need deterministic viewport control and frame-by-frame geometry evidence:

```ts
import { chromium } from "playwright";

const browser = await chromium.launch({ headless: false });
const page = await browser.newPage({
  viewport: { width: 1280, height: 900 },
  deviceScaleFactor: 2,
});

await page.goto("http://localhost:4173/example");
await page.locator("[data-panel-toggle]").click();

const samples = await page.evaluate(async () => {
  const read = () => {
    const panel = document.querySelector("#detail-panel");
    const tablist = document.querySelector('[role="tablist"]');

    const panelRect = panel?.getBoundingClientRect();
    const tabRect = tablist?.getBoundingClientRect();

    return {
      panelLeft: panelRect?.left ?? null,
      tabLeft: tabRect?.left ?? null,
      tabTransform: tablist ? getComputedStyle(tablist).transform : null,
    };
  };

  const frames = [read()];

  for (let i = 0; i < 12; i += 1) {
    await new Promise((resolve) => requestAnimationFrame(resolve));
    frames.push(read());
  }

  return frames;
});

console.table(samples);
await page.screenshot({ path: "/tmp/repro-after-toggle.png", fullPage: true });
await browser.close();
```

Adapt selectors and interaction steps to the bug. Keep the script small enough that the evidence remains legible.

### Performance Trace

Use a performance trace when the claim is about cost, repeated layout, or jank.

Look for:

- repeated full content layout during drag or window resize
- expensive layout inside content that should be visually buffered
- paint/composite behavior around blur, transform, and opacity
- whether only the shell layer updates during the live phase
- whether the expensive content commit happens once at the trailing edge

Do not use a trace as the first tool for a simple visual mismatch; traces are slower to read and can obscure a simpler geometry bug.

## Common False Negatives

Before concluding "cannot reproduce," check for condition drift:

- the browser tab is hidden, so View Transitions or animation timing behave differently
- `prefers-reduced-motion` disables or changes animation
- browser, viewport, device scale factor, or zoom differs from the report
- auth, feature flags, seeded data, async loading state, or collapsed/expanded state differs
- scroll position, hover state, focus state, pointer position, or selected tab differs
- screenshot timing misses the bad frame
- test harness, Storybook decorator, or CI mode disables transitions
- browser-specific APIs or CSS features differ between Chrome, Safari, and Firefox

## Reproduction Notes Template

Write a short note before fixing. It can be in the conversation, a scratch file, or an issue comment.

```markdown
Repro:

- Surface:
- Browser / viewport:
- Steps:
- Expected:
- Actual:
- Evidence:
- Suspect boundary:
```

Keep it concrete. The note should let you rerun the same path after the patch.

## Working With Hypotheses

After reproduction, form hypotheses from evidence:

- If parent geometry changes but child geometry does not, inspect child positioning, projection, portals, sticky/fixed positioning, and transforms.
- If old/new screenshots jump, inspect view-transition group geometry, image-pair sizing, transform origin, and clipping.
- If blur appears instant, inspect transition duration, play-state gating, and whether a later rule overrides the initial state.
- If content relayouts continuously during resize, inspect state commits, measured layout dependencies, debouncing, virtualization, and buffered visual vs locked layout state.
- If an element is hidden behind the transition layer, inspect top-layer pseudo-elements, view-transition names, z-index, and whether the control needs its own transition snapshot or overlay strategy.

Tie each code change to one hypothesis. Avoid broad refactors while the visual failure is still under investigation.

## Fix Verification

After editing, rerun the same reproduction path.

Keep relevant conditions identical: browser, viewport, device scale, zoom, reduced-motion setting, feature flags, auth/data state, scroll position, selected state, and interaction timing. If any condition changes, say so and explain why it does not invalidate the comparison.

Verify both:

- **The reported symptom is gone.** Use the same screenshot/video/frame/sample path.
- **The intended behavior still exists.** For motion, check both start/end states and the transition frames.

For interactive visual bugs, unit tests are supporting evidence, not the final proof. They can guard class names, state transitions, and accessibility, but they cannot prove that a cross-fade, blur timing, or FLIP geometry looks correct.

When possible, include a before/after comparison:

```markdown
Before:

- panel left changed; tablist transform counteracted parent movement

After:

- panel and tablist left changed together; tablist transform stayed none
```

## Complete Examples

Geometry/FLIP case:

```markdown
Repro:

- Surface: `http://localhost:4173/example`
- Browser / viewport: Chrome, 1280x900, deviceScaleFactor 2
- Steps: click the right-panel collapse button, sample 12 animation frames
- Expected: segmented control moves with the right panel
- Actual: panel `left` changes each frame; tablist `left` stays constant and has computed transform `matrix(...)`
- Evidence: requestAnimationFrame sample table plus screenshot at frame 4
- Suspect boundary: child Motion projection is compensating against parent FLIP
```

Performance/jank case:

```markdown
Repro:

- Surface: Storybook `BufferedSplitLayoutViewTransition`
- Browser / viewport: Chrome, 1440x900
- Steps: drag divider for 2 seconds, then release; repeat with window resize
- Expected: live phase updates shell width/scale/blur only; content layout commits once after release or debounce
- Actual: performance trace shows content subtree layout on almost every resize frame
- Evidence: trace screenshots of repeated Layout tasks under content nodes
- Suspect boundary: visual width updates are leaking into locked content layout state
```

## If You Cannot Reproduce

Do not make speculative visual fixes just to try something.

Instead:

- state exactly what you tried
- include the URL, viewport, and steps
- list what evidence did or did not show
- ask for the missing condition only if you cannot discover it locally
- use the user's video or screenshot to narrow the missing state
- inspect code to design the next repro, not to patch blindly

It is acceptable to spend most of the task on reproduction. For these bugs, a reliable repro path is part of the deliverable.

## Handoff Format

When reporting back, lead with evidence:

```markdown
Reproduced. The issue was visible during [interaction] on [surface].

Evidence:

- [screenshot/video/frame/sample/trace result]

Root cause:

- [specific boundary or element]

Fix:

- [small code change]

Verification:

- [same repro path now passes]
- [tests/checks run]
```

If you did not reproduce it, say that directly and do not claim a fix.
