---
name: screenshot-iteration
description: Make design decisions from rendered pages, not from code or plans. Capture the page at 390, 768, 1280 and 1920 wide, compare against the last round, name the concrete problems you can see, fix only those, and capture again. Written measurements are hypotheses; screenshots decide. Use when designing or polishing a page with an AI agent, or whenever a plan's numbers and the real page disagree.
---

# /screenshot-iteration

A plan says "the image is 50vw wide and overlaps the cards by 9rem". The page is built exactly to the plan, and it looks wrong. That happens all the time, because a layout described in words can't be judged in words. This skill makes the rendered page the source of truth: build, look, compare, fix what you see, look again.

## Purpose

Run design work as a loop of rendered rounds. Each round produces screenshots at four widths, a short list of visible problems, and a small set of fixes, so decisions are made by looking at the result rather than by trusting a description of it.

## Use when

- You're building or polishing a page, and how it looks matters.
- A plan contains measurements (widths, overlaps, offsets, type sizes) that haven't been seen rendered yet.
- Feedback refers to how something looks.
- You want to compare two versions honestly.

## Don't use when

- You're hunting responsive **defects**: horizontal overflow, small touch targets, unreadable text, console errors. That's `/responsive-audit`, which measures them. The two work together: **`/responsive-audit` finds what's broken; `/screenshot-iteration` decides what's better.**
- The change can't be seen (logic, data, types). Test it instead.
- The page can't run yet. Get it running first; don't iterate on imagination.

## Inputs

- The running page (local dev server or a preview URL) and the routes to look at.
- The last round's screenshots, if there are any, to compare against.
- The goal of this round in one sentence ("make the hero less crowded", "make the two plans read as different levels").
- Playwright. If it isn't installed: `npm i -D playwright && npx playwright install chromium`, in a scratch directory.

## Process

### 1. Capture

Save this as `shots.mjs` in a scratch directory (not in the project) and run `node shots.mjs <base-url> <out-dir> <path> [path…]`. It saves the first screen and the full page at four widths, and reports horizontal overflow and console errors so a broken round is never mistaken for a design result.

```js
// Screenshot iteration: captures each path at four widths (first screen + full page), notes overflow and errors.
import { chromium } from "playwright";
import fs from "node:fs";

const [base, out = "./shots", ...paths] = process.argv.slice(2);
const WIDTHS = [[390, 844], [768, 1024], [1280, 800], [1920, 1080]];
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
for (const [width, height] of WIDTHS) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: width < 1000 ? 2 : 1 });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  for (const path of paths.length ? paths : ["/"]) {
    await page.goto(base + path, { waitUntil: "networkidle" });
    await page.waitForTimeout(1500); // let entrance motion settle
    const name = `${(path === "/" ? "home" : path.slice(1).replaceAll("/", "-"))}-${width}`;
    await page.screenshot({ path: `${out}/${name}-first.png` });
    await page.screenshot({ path: `${out}/${name}-full.png`, fullPage: true });
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    console.log(name, overflow > 0 ? `OVERFLOW ${overflow}px` : "ok", errors.splice(0).join(" | "));
  }
  await page.close();
}
await browser.close();
```

Full-page screenshots don't scroll, so lazy images and lazily mounted content may be missing from them. To judge one section properly, scroll it into view and screenshot that element.

### 2. Look before you read your notes

Open the first-screen captures side by side, then the full pages. Before rereading the plan, write what you see in one or two lines per width: what's first, what's largest, what competes, what feels empty or crowded.

### 3. Name concrete problems

Each problem must point at something visible, at a specific width:

- "At 768, the image and the first card overlap, and the card covers his face."
- "At 1280, there are 180px of empty space between the buttons and the first cards."
- "At 390, the second plan's price wraps under its name."

Not: "the hero could be stronger". If you can't point at it, it isn't a problem for this round.

### 4. Fix only what you named

Treat every number in the plan as a starting point. If the plan says 9rem and the screenshot says it's crowding, change it. Fix the listed problems and nothing else. Changes you didn't list can't be judged this round.

### 5. Capture again and compare

Run the same script with the same paths into a new folder (`round-2`, `round-3`). Compare round against round at each width:

- Did each named problem go away?
- Did anything that was fine get worse?
- Did a fix at one width break another?

### 6. Decide

- **Better, nothing broke:** keep it, and stop or start the next round with a new short list.
- **Better at one width, worse at another:** adjust the breakpoint rule rather than the whole design.
- **Not better:** revert that change. Don't stack another change on top of a failed one.

Stop when a round produces no problems you can point at. Don't keep iterating on taste.

## Acceptance criteria

- Every round has captures at all four widths, saved in their own folder.
- Every change in a round traces to a problem named against a specific screenshot.
- No round shows horizontal overflow or console errors.
- The final round is compared against the first, not only against the previous one, so slow drift is visible.

## Common failure modes

- **Trusting the plan.** Keeping a measurement because it was written down, while the screenshot shows it doesn't work.
- **Judging one width.** A desktop-only review; the phone layout quietly breaks.
- **Judging the code.** Reading the CSS and deciding it "should" look right.
- **Too many changes per round.** You can't tell which one helped, so you can't revert the one that didn't.
- **Iterating forever.** Rounds keep going on preference after every concrete problem is gone.
- **Screenshot artefacts taken as real.** A sticky header over an element screenshot, missing lazy images in a full-page capture, a dev server caught mid-recompile. Recapture before you "fix" them.

## Final self-review

- Do I have this round's captures at 390, 768, 1280 and 1920?
- Can I point at every problem I fixed?
- Did I compare against the previous round and the first round?
- Did I revert anything that didn't help?
- Is there overflow or a console error in any capture?

## Copyable instruction

```text
Work in screenshot rounds; the rendered page is the source of truth, not the plan.
Each round:
1. Capture the page at 390, 768, 1280 and 1920 wide (first screen and full page) into a new folder.
2. Look first: write what you see at each width before rereading the plan.
3. List concrete problems, each pointing at something visible at a specific width.
4. Fix only those. Treat every measurement in the plan as a hypothesis you may change.
5. Capture again and compare with the last round and the first. Revert any change that didn't help.
Check every capture for horizontal overflow and console errors.
Stop when there is nothing left you can point at.
```
