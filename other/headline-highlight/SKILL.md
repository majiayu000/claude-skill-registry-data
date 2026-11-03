---
name: headline-highlight
description: Turn a screenshot of a news headline, article or document into a short Remotion video. The article sits on a white background, starts blurred and sharpens, slowly zooms and tilts in 3D, and a yellow highlighter draws left to right behind the key words. Renders a vertical (1080x1920) or horizontal (1920x1080) MP4. Use this whenever the user wants to highlight words in a headline, article or document screenshot for a video, make a highlighted-headline or news b-roll clip for Reels, TikTok, Shorts or YouTube, animate a marker over a screenshot, or turn an article link into a highlight video, even if they never mention Remotion.
---

> **Video Studio:** how this skill runs here (these lines win over the steps below where they differ).
> - **Project folder:** `projects/remotion/headline-highlight-<job id or slug>/`, a fresh Remotion project each time as below (`projects/` is never committed). It is its own project, separate from `engines/split-screen`, so it runs whatever `styles/engines.json` says. Run every `npx` command from inside it.
> - **Footage from a studio job:** copy (never move) `jobs/<id>/source.*` into the project's `public/`.
> - **OCR on Windows:** install Tesseract once with `winget install --id UB-Mannheim.TesseractOCR -e` (then reopen the terminal so `tesseract` is on PATH).
> - **Colour:** the highlighter stays marker-yellow (it has to read as a highlighter); use brand accentLight #C4B5FD only if Bryan asks for purple.
> - **Where it fits:** B-roll for any style when the script cites an article, study, review or document ("according to...", a `[PROOF]` or `[IMAGE]` cue). Render the clip at the style's aspect and cut it in. Only real articles or Bryan's own documents; never a made-up headline attributed to a real publication.
> - **Remotion licence:** free for individuals and companies of up to 3 people; above that it needs a company licence (remotion.dev/license).
> - **Deliver:** copy the rendered MP4 into the job folder (`jobs/<id>/preview.mp4` while reviewing, `final.mp4` when approved) or `outputs/`, and log what was added in `edits.json` so the review page can take notes on it.

# Headline Highlight

Makes a 5-second clip of a news headline or document with a highlighter
sweeping across its key words, the kind of insert creators drop into
commentary videos. The user brings a screenshot (or an article URL), Claude
proposes which words to highlight, the user confirms and picks vertical or
horizontal, and Claude renders the MP4.

## The original brief

This skill automates the result of this prompt. Every visual decision below
traces back to it:

> Use Remotion best practices. Import the attached image into the project. Use
> tesseract CLI to do OCR and find the positions of the text. In Remotion, make
> a new composition where you load the image and pad the article generously on
> a white full HD background. While the composition is running for 5 seconds,
> slowly, very subtly, zoom into it and slightly rotate the article in 3D from
> left to right. The overall rotation should be around 15deg for each axis. At
> the beginning, blur the whole composition and unblur it over 1 second. After
> the blur is done, evolve a highlighter from left to right using Node.js over
> the words "left-leaning", "immigration" and "crackdown". The image has a white
> background. Make sure the marker appears behind the text. When installing new
> dependencies, check for existing lockfiles and use the right package manager.

How it was interpreted, and how the skill keeps doing it:

- **15deg per axis** is a sweep from -7.5deg to +7.5deg on both X and Y over
  the full clip. Z stays at 0, because rotating Z spins the article flat
  instead of tilting it.
- **"Using Node.js"** means the OCR post-processing is a Node.js script: it runs
  the tesseract CLI, parses the word boxes and writes them to JSON for the
  composition.
- **Adjacent highlighted words on the same line become one stroke.**
  "Immigration Crackdown" gets one continuous swipe, the way a person would
  drag a real marker across them.
- **The marker sits behind the text** because the markers are painted first
  and the screenshot is drawn over them with `mix-blend-mode: multiply`. White
  paper takes on the marker color while black ink stays black. This depends on
  a light background (see step 1).
- **"Full HD"** is 1920x1080 for horizontal. The vertical version is 1080x1920
  with the same treatment.

## Workflow

### 1. Get the screenshot

**If the user attached or pointed to an image, use it.** Look at it before
doing anything else:

- **Is the background light?** The multiply trick needs light paper with dark
  ink. A dark-mode screenshot would swallow the marker. Ask for a light-mode
  capture, or offer the URL capture below.
- **Is it cropped to the part that matters?** A full-page or phone screenshot
  still works, but the headline will be small in the frame. Offer to capture
  from the URL, or ask for a tighter screenshot of the headline and the
  sentence under it.
- **Is it sharp?** Retina and phone screenshots are ideal. A tiny, blurry image
  will OCR badly and look soft once it fills the frame.

**If the user gave an article URL,** capture the headline block with the
script in [URL capture](#url-capture). The browser width depends on the
orientation: 1280 for horizontal, 430 for vertical. If the user hasn't chosen
yet, capture at 1280, and recapture at 430 if they later pick vertical. Open
the resulting PNG and confirm it shows the headline (and the dek/standfirst
under it) before going on.

If the capture is blocked (paywall, bot check, cookie wall), don't try to get
around it. Ask the user for a screenshot instead: Cmd+Shift+4 on a Mac,
Win+Shift+S on Windows, light mode, and browser zoom at 150% or more for crisp
text.

### 2. Set up the Remotion project (once per workspace)

Reuse an existing `headline-highlight/` project in the working directory if
one exists (it will have `src/HeadlineHighlight.tsx`). Otherwise scaffold a
fresh one. Never borrow some other Remotion project on the machine.

```bash
npx create-video@latest --yes --blank --no-tailwind headline-highlight
```

Then, inside `headline-highlight/`:

1. Install Remotion's official agent skills into the project and follow them
   for anything not covered here:
   `npx skills add remotion-dev/skills -a claude-code -y --copy`
2. Add the highlighter package. `remotion add` picks the package manager from
   the lockfile and pins the matching Remotion version:
   `npx remotion add @remotion/rough-notation`
3. Write `scripts/ocr.mjs` and `src/HeadlineHighlight.tsx` from
   [Reference code](#reference-code), and replace `src/Root.tsx` as shown
   there.
4. Delete the blank template's empty `src/Composition.tsx` (`MyComp`
   renders nothing).
5. Add `"ocr": "node scripts/ocr.mjs"` to the `package.json` scripts.

**Package manager rule:** before installing anything, look for a lockfile.
`package-lock.json` means npm, `pnpm-lock.yaml` means pnpm, `yarn.lock`
means yarn, and `bun.lock`/`bun.lockb` means bun. Install with that manager
and never create a second lockfile. A project scaffolded through `npx` uses
npm.

### 3. Make sure the tesseract CLI exists

Run `tesseract --version`. If it's missing, tell the user what you're
installing, then:

- **macOS with Homebrew:** `brew install tesseract`
- **Linux:** `sudo apt-get install -y tesseract-ocr` (needs their password,
  so have them run it)
- **Windows:** have them run
  `winget install --id UB-Mannheim.TesseractOCR -e`. The binary lands in
  `C:\Program Files\Tesseract-OCR\tesseract.exe`.
- **macOS or Linux without Homebrew or admin rights:** install a private copy
  from conda-forge into the project using micromamba. Nothing system-wide
  changes:

  ```bash
  # inside headline-highlight/. Platform: osx-arm64, osx-64, linux-64 or linux-aarch64
  mkdir -p .tools && cd .tools
  curl -Ls https://micro.mamba.pm/api/micromamba/osx-arm64/latest | tar -xj bin/micromamba
  MAMBA_ROOT_PREFIX="$PWD/mamba" ./bin/micromamba create -y -p "$PWD/tesseract" -c conda-forge tesseract
  # the package ships every language (~340MB); keep only what is needed
  find tesseract/share/tessdata -name '*.traineddata' ! -name 'eng.*' ! -name 'osd.*' -delete
  rm -rf mamba/pkgs
  ```

  Then point the OCR script at it with
  `TESSERACT=.tools/tesseract/bin/tesseract`. Add `.tools/` to `.gitignore`.

For non-English articles, also install that language's data
(`brew install tesseract-lang`, or keep its `.traineddata` file) and pass
`--lang deu` (or the right code) to the OCR script.

### 4. Read the text and propose the highlights

Copy the screenshot into the project as `public/headlines/<slug>.png`. Use a
short kebab-case slug for the story, such as `nyt-minnesota-surveillance`.
Then list what tesseract sees:

```bash
npm run ocr -- public/headlines/<slug>.png --text
```

Pick **1 to 3 phrases** worth highlighting. A good pick is the loaded or
surprising part of the claim, the words a viewer should remember after one
glance. In the original, those were "Left-Leaning" and "Immigration
Crackdown". Keep each phrase short (1 to 3 words). Highlighting half the
headline dilutes it. Use the exact spelling from the OCR output, because that
is what the matcher compares against.

Then ask the user **one** question that covers both choices: your proposed
words, which they can confirm or swap, and vertical (1080x1920 for Reels,
TikTok and Shorts) or horizontal (1920x1080 for YouTube), unless they already
said. Offer both orientations as an option. If they already named the words
and the orientation, skip the question.

### 5. Locate the words

```bash
npm run ocr -- public/headlines/<slug>.png src/headlines/<slug>.json "Left-Leaning" "Immigration" "Crackdown"
```

This writes the stroke boxes in the screenshot's own pixels. If a phrase isn't
found, the script prints every line it read. OCR sometimes misreads a letter,
so retry with the spelling it actually produced.

### 6. Register the video and check a frame

Add a `<Composition>` per orientation to `src/Root.tsx` (see the reference).
Use `<slug>-vertical` and/or `<slug>-horizontal` as the id. Then render the
last frame and **look at it** before spending time on the full render:

```bash
npx remotion still <slug>-vertical out/<slug>-vertical-check.png --frame=-1
```

Check that:

- each marker covers its word with a little breathing room and doesn't
  bleed into a neighbouring word;
- the ink is dark on top of the yellow (the marker is behind the text);
- the article has generous white space around it and nothing is clipped by
  the tilt.

If a marker touches a neighbouring word, shrink that stroke's
`padLeft`/`padRight` in the JSON. If the article looks small, the screenshot
probably has too much empty space around the text. Crop it tighter.

### 7. Render and deliver

```bash
npx remotion render <slug>-vertical out/<slug>-vertical.mp4
```

Give the user the path to the MP4. Rendering is only about 30 seconds, so
offer the other orientation. If they want to scrub or tweak first,
`npx remotion studio` opens the preview.

## Timing and look

All of these live in `src/HeadlineHighlight.tsx`:

| What | Value | Why |
| --- | --- | --- |
| Length | 5s, or longer if needed to leave 1.5s on the finished frame | The brief's 5 seconds. Long phrases still need time to land. |
| Blur | 24px down to 0 over 1s | "Unblur over 1 second" |
| First stroke | starts at 1s | "After the blur is done" |
| Stroke speed | about 1.9s per full article width, clamped to 0.35s–1.3s, with 0.2s between strokes | Short words still get a visible swipe, and long phrases don't drag |
| Zoom | 1.00 to 1.08 over the whole clip, ease in-out | "Slowly, very subtly" |
| Tilt | X +7.5deg to -7.5deg, Y -7.5deg to +7.5deg, perspective 2000px | 15deg per axis, turning left to right |
| Article size | at most 62% x 60% of a horizontal frame, or 80% x 55% of a vertical one | "Pad generously" |
| Marker | `rgba(255, 221, 0, 0.62)`, one stroke at roughness 1.5, padding 13% of line height above and 23% below | Reads like a real highlighter. Descenders poke out naturally. |

If the user wants a different marker color, change it in one place. Keep it
translucent so it still reads as ink on paper.

## Lessons from the first build

These caused real problems or were non-obvious, and the code below already
handles them:

- **Word boxes include descenders.** "Leaning" is taller than "Crackdown"
  because of the "g". The OCR script sizes each stroke from its line instead:
  the tallest top, and a baseline taken from words without descenders. That
  keeps every marker on a line the same height.
- **Words can sit only a few pixels apart.** A fixed left padding made the
  marker touch the "d" of "Investigated". The script measures the gap to the
  neighbouring word and pads less when it's tight.
- **Use `@remotion/rough-notation`, not a hand-rolled SVG.** Remotion's skill
  recommends it for highlights. It measures with `offsetLeft`/`offsetWidth`,
  which ignore transforms, so markers stay locked to the words through the zoom
  and the 3D tilt. Use `iterations={1}` so it only sweeps left to right.
  The default of 2 sweeps back again. Lower `roughness` to 1.5 as well. The
  default of 3 jitters the stroke ends by a fixed number of pixels, so on a
  short word the marker tilts and runs into the neighbouring words.
- **3D rotation with the `rotate` property:** Remotion's `interpolate` handles
  axis strings like `"x 7.5deg"`. X and Y need two nested elements, with
  `transformStyle: "preserve-3d"` on the outer one.
- **Screenshot resolution must not change the tilt.** A 2x retina screenshot
  is twice as wide in pixels, and CSS `scale` doesn't scale depth, so tilting
  the raw image would double the perspective effect. The card is therefore
  sized in video pixels, and the screenshot is scaled down inside it before
  anything rotates.
- **Remotion rules that apply here:** drive everything from
  `useCurrentFrame()` and `interpolate()` (CSS transitions don't render), load
  the image with `<CanvasImage>` and `staticFile()`, and give timed components
  `premountFor={fps}`.

## URL capture

Use this when the user gives a link instead of a screenshot. It opens the page
in their installed Chrome or Edge with no visible window, finds the headline
(matched against the page's `og:title`) and the dek under it, and hides
everything else on the page: nav bars, bylines, share buttons, cookie and
subscribe banners. It saves a 2x screenshot of the text on clean paper. It
never clicks or accepts anything.

Install `playwright-core` with the project's package manager (for npm:
`npm i -D playwright-core`). Save the script as `scripts/capture.mjs`, then run:

```bash
node scripts/capture.mjs "<url>" public/headlines/<slug>.png 1280
```

The last argument is the browser width. 1280 suits horizontal videos. For a
vertical video, use a phone width such as 430. The site switches to its
mobile layout and the headline wraps into more, shorter lines, which fills a
tall frame much better. (A mid width like 820 can make the headline *wider*
on some sites.) If no Chrome or Edge is installed,
`npx playwright-core install chromium` provides a browser.

Exit code 2 means the page blocked the capture or no headline was found. A
debug screenshot is saved next to the output so you can see why. Ask the user
for a manual screenshot at that point. The New York Times answers automated
browsers with a 403, so for NYT links go straight to asking for a screenshot.
Other paywalled publishers often behave the same way.

```js
// scripts/capture.mjs: screenshot an article's headline + dek.
// node scripts/capture.mjs <url> <out.png> [viewportWidth]
import { chromium } from "playwright-core";

const [url, out, widthArg] = process.argv.slice(2);
if (!url || !out) {
  console.error("Usage: node scripts/capture.mjs <url> <out.png> [viewportWidth]");
  process.exit(1);
}
const width = Number(widthArg ?? 1280);

const launch = async () => {
  for (const channel of ["chrome", "msedge", undefined]) {
    try {
      return await chromium.launch({ channel, headless: true });
    } catch {
      // try the next browser
    }
  }
  throw new Error(
    "No browser found. Install Google Chrome, or run: npx playwright-core install chromium",
  );
};

const browser = await launch();
const page = await browser.newPage({
  viewport: { width, height: 1600 },
  deviceScaleFactor: 2,
  colorScheme: "light",
});

const blocked = async (reason) => {
  const debug = out.replace(/\.png$/i, "") + "-debug.png";
  await page.screenshot({ path: debug }).catch(() => {});
  console.error(`Capture failed: ${reason}. See ${debug}`);
  await browser.close();
  process.exit(2);
};

const response = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
await page.evaluate(() => document.fonts.ready);

const title = await page.title();
if ((response && response.status() >= 400) ||
    /access denied|captcha|just a moment|are you a robot|verify you are human/i.test(title)) {
  await blocked(`page answered ${response?.status()} "${title}"`);
}

const box = await page.evaluate(() => {
  const norm = (s) =>
    (s ?? "").toLowerCase().replace(/[\u2018\u2019\u201c\u201d"']/g, "").replace(/\s+/g, " ").trim();
  const overlap = (a, b) => {
    const A = new Set(norm(a).split(" ").filter((w) => w.length > 2));
    const B = new Set(norm(b).split(" ").filter((w) => w.length > 2));
    if (!A.size || !B.size) return 0;
    let shared = 0;
    for (const w of A) if (B.has(w)) shared++;
    return shared / Math.max(A.size, B.size);
  };
  const meta = (sel) => document.querySelector(sel)?.getAttribute("content") ?? "";
  const ogTitle = meta('meta[property="og:title"]') || document.title;
  const ogDescription = meta('meta[property="og:description"]') || meta('meta[name="description"]');

  // Tight box around the text itself, not the (often full-width) element.
  const textRect = (el) => {
    const style = getComputedStyle(el);
    if (style.display === "none" || style.visibility === "hidden") return null;
    const range = document.createRange();
    range.selectNodeContents(el);
    const rects = [...range.getClientRects()].filter((r) => r.width > 1 && r.height > 1);
    if (!rects.length) return null;
    return {
      left: Math.min(...rects.map((r) => r.left)),
      top: Math.min(...rects.map((r) => r.top)),
      right: Math.max(...rects.map((r) => r.right)),
      bottom: Math.max(...rects.map((r) => r.bottom)),
    };
  };

  const headline = [...document.querySelectorAll('h1, h2, [itemprop="headline"]')]
    .filter((el) => textRect(el) && norm(el.textContent).length >= 8)
    .map((el) => ({
      el,
      score:
        3 * overlap(el.textContent, ogTitle) +
        (el.tagName === "H1" ? 1 : 0) +
        parseFloat(getComputedStyle(el).fontSize) / 40,
    }))
    .sort((a, b) => b.score - a.score)[0]?.el;
  if (!headline) return null;

  headline.scrollIntoView({ block: "start" });
  window.scrollBy(0, -160);

  const h = textRect(headline);
  const dek = [...document.querySelectorAll('p, h2, [class*="dek" i], [class*="summary" i], [class*="standfirst" i]')]
    .filter((el) => !el.contains(headline) && !headline.contains(el))
    .map((el) => ({ el, r: textRect(el), text: norm(el.textContent) }))
    .filter(({ r, text }) =>
      r && r.top >= h.bottom - 4 && r.top - h.bottom < 260 &&
      Math.abs(r.left - h.left) < 200 && text.length >= 30 && text.length <= 450)
    .sort((a, b) =>
      (overlap(b.text, ogDescription) >= 0.5) - (overlap(a.text, ogDescription) >= 0.5) ||
      a.r.top - b.r.top)[0];

  // Hide everything except the headline, the dek and the elements that
  // contain them: nav bars, bylines, share buttons, cookie and subscribe
  // banners, rules and borders. The capture is clean paper with only the text
  // left on it. Nothing is clicked or accepted.
  const keep = dek ? [headline, dek.el] : [headline];
  const style = document.createElement("style");
  style.textContent = `
    .hh-hide { visibility: hidden !important; }
    .hh-keep { border-color: transparent !important; box-shadow: none !important; outline: none !important; }
    .hh-keep::before, .hh-keep::after { visibility: hidden !important; }`;
  document.head.append(style);
  for (const el of document.querySelectorAll("body *")) {
    if (keep.some((k) => k.contains(el))) continue;
    el.classList.add(keep.some((k) => el.contains(k)) ? "hh-keep" : "hh-hide");
  }

  const rects = dek ? [h, dek.r] : [h];
  const pad = 40;
  const left = Math.max(0, Math.min(...rects.map((r) => r.left)) - pad);
  const top = Math.max(0, Math.min(...rects.map((r) => r.top)) - pad);
  return {
    headline: headline.textContent.trim(),
    dek: dek ? dek.el.textContent.trim() : null,
    x: left,
    y: top,
    width: Math.min(window.innerWidth, Math.max(...rects.map((r) => r.right)) + pad) - left,
    height: Math.max(...rects.map((r) => r.bottom)) + pad - top,
  };
});

if (!box) {
  await blocked("no headline found on the page");
}

await page.screenshot({
  path: out,
  clip: { x: box.x, y: box.y, width: box.width, height: box.height },
});
await browser.close();
console.log(JSON.stringify({ file: out, headline: box.headline, dek: box.dek }, null, 2));
```

## Reference code

### `scripts/ocr.mjs`

```js
// Runs the tesseract CLI over a screenshot and writes the boxes the
// highlighter needs. Coordinates are in the screenshot's own pixels.
//
//   npm run ocr -- <image> --text                       list what OCR read
//   npm run ocr -- <image> <out.json> "phrase" ...      locate phrases
//   options: --lang deu (default eng); TESSERACT=/path/to/tesseract
//
// Target words that sit next to each other on the same line are merged into
// one stroke, the way a person drags a marker across them in one go.

import { execFileSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const flag = (name) => {
  const i = args.indexOf(name);
  return i === -1 ? null : args.splice(i, 2)[1];
};
const lang = flag("--lang") ?? "eng";
const listOnly = args.includes("--text");
const [imagePath, outPath, ...phrases] = args.filter((a) => a !== "--text");
if (!imagePath || (!listOnly && (!outPath || !phrases.length))) {
  console.error('Usage: ocr.mjs <image> --text | ocr.mjs <image> <out.json> "phrase" ...');
  process.exit(1);
}

const tsv = execFileSync(
  process.env.TESSERACT ?? "tesseract",
  [imagePath, "stdout", "-l", lang, "--psm", "3", "tsv"],
  { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] },
);

const [header, ...rows] = tsv.trim().split("\n");
const columns = header.split("\t");
const records = rows.map((row) => {
  const cells = row.split("\t");
  const r = Object.fromEntries(columns.map((c, i) => [c, cells[i]]));
  for (const k of ["level", "block_num", "par_num", "line_num", "word_num", "left", "top", "width", "height"]) {
    r[k] = Number(r[k]);
  }
  r.line = `${r.block_num}-${r.par_num}-${r.line_num}`;
  return r;
});
const page = records.find((r) => r.level === 1);
const words = records.filter((r) => r.level === 5 && r.text?.trim());

const lines = new Map();
for (const w of words) {
  if (!lines.has(w.line)) lines.set(w.line, []);
  lines.get(w.line).push(w);
}

if (listOnly) {
  let n = 1;
  for (const lineWords of lines.values()) {
    console.log(`${String(n++).padStart(2)}  ${lineWords.map((w) => w.text).join(" ")}`);
  }
  process.exit(0);
}

// Word boxes include descenders ("g" in "Leaning"), which would give every
// marker a different height. Use the line instead: the tallest top, and the
// baseline from the lowest bottom among full-height words without descenders.
const band = (lineWords) => {
  const top = Math.min(...lineWords.map((w) => w.top));
  const tallest = Math.max(...lineWords.map((w) => w.height));
  const baseline = Math.min(
    ...lineWords
      .filter((w) => /[\p{L}\p{N}]/u.test(w.text) && w.height >= 0.7 * tallest)
      .map((w) => w.top + w.height),
  );
  return { top, height: baseline - top };
};

const normalize = (s) =>
  s.toLowerCase().replace(/[\u2010-\u2015]/g, "-").replace(/[^\p{L}\p{N}'-]/gu, "")
    .replace(/^[-']+|[-']+$/g, "");

// Each phrase must appear as consecutive words in reading order.
const picked = new Set();
for (const phrase of phrases) {
  const tokens = phrase.split(/\s+/).map(normalize).filter(Boolean);
  const start = words.findIndex((_, i) =>
    tokens.every((t, j) => words[i + j] && normalize(words[i + j].text) === t));
  if (start === -1) {
    console.error(`OCR did not find "${phrase}". It read:\n`);
    for (const lineWords of lines.values()) console.error(`  ${lineWords.map((w) => w.text).join(" ")}`);
    process.exit(2);
  }
  tokens.forEach((_, j) => picked.add(start + j));
}

// Group picked words into strokes: consecutive words on the same line.
const strokes = [];
let current = null;
[...picked].sort((a, b) => a - b).forEach((index) => {
  const word = words[index];
  const prev = words[index - 1];
  if (current && picked.has(index - 1) && prev.line === word.line) {
    current.words.push(word);
  } else {
    current = { words: [word] };
    strokes.push(current);
  }
});

const result = {
  image: {
    file: path.relative("public", imagePath).split(path.sep).join("/"),
    width: page.width,
    height: page.height,
  },
  strokes: strokes.map(({ words: ws }) => {
    const first = ws[0];
    const last = ws[ws.length - 1];
    const lineWords = lines.get(first.line);
    const { top, height } = band(lineWords);
    // Pad less where a neighbouring word is close, so the marker never
    // touches it.
    const before = lineWords[lineWords.indexOf(first) - 1];
    const after = lineWords[lineWords.indexOf(last) + 1];
    const room = (gap) => Math.max(0, Math.min(0.22 * height, gap - 0.15 * height));
    return {
      text: ws.map((w) => w.text).join(" "),
      x: first.left,
      y: top,
      width: last.left + last.width - first.left,
      height,
      padLeft: Math.round(before ? room(first.left - (before.left + before.width)) : 0.2 * height),
      padRight: Math.round(after ? room(after.left - (last.left + last.width)) : 0.23 * height),
    };
  }),
};

mkdirSync(path.dirname(outPath), { recursive: true });
writeFileSync(outPath, `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
```

### `src/HeadlineHighlight.tsx`

```tsx
import { Highlight } from "@remotion/rough-notation";
import {
  AbsoluteFill,
  CalculateMetadataFunction,
  CanvasImage,
  Easing,
  Interactive,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

// Stroke boxes come from scripts/ocr.mjs and are in the screenshot's own
// pixels. The screenshot is laid out at that size, scaled down into a card
// sized in video pixels, and the card is what zooms and tilts. That keeps the
// 3D effect identical whatever the screenshot's resolution.

type Stroke = {
  text: string;
  x: number;
  y: number;
  width: number;
  height: number;
  padLeft: number;
  padRight: number;
};

export type HeadlineHighlightProps = {
  data: {
    image: { file: string; width: number; height: number };
    strokes: Stroke[];
  };
  orientation: "horizontal" | "vertical";
};

const FPS = 30;

// How much of the frame the article may fill before the zoom. Generous white
// space is the look.
const LAYOUT = {
  horizontal: { width: 1920, height: 1080, maxWidth: 0.62, maxHeight: 0.6 },
  vertical: { width: 1080, height: 1920, maxWidth: 0.8, maxHeight: 0.55 },
} as const;

const BLUR_SECONDS = 1;
const GAP_SECONDS = 0.2;
const HOLD_SECONDS = 1.5;

// The marker crosses a full article width in about 1.9s, so a short word still
// takes a visible beat and a long phrase doesn't drag.
const planStrokes = (strokes: Stroke[], imageWidth: number) => {
  let t = BLUR_SECONDS;
  return strokes.map((stroke, i) => {
    if (i > 0) t += GAP_SECONDS;
    const start = t;
    t += Math.min(1.3, Math.max(0.35, (1.9 * stroke.width) / imageWidth));
    return { ...stroke, start, end: t };
  });
};

export const calculateMetadata: CalculateMetadataFunction<HeadlineHighlightProps> = ({ props }) => {
  const { width, height } = LAYOUT[props.orientation];
  const plan = planStrokes(props.data.strokes, props.data.image.width);
  const lastEnd = plan.length ? plan[plan.length - 1].end : BLUR_SECONDS;
  return {
    width,
    height,
    durationInFrames: Math.round(Math.max(5, lastEnd + HOLD_SECONDS) * FPS),
  };
};

export const HeadlineHighlight: React.FC<HeadlineHighlightProps> = ({ data, orientation }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const { image } = data;
  const layout = LAYOUT[orientation];
  const fit = Math.min(
    (layout.maxWidth * width) / image.width,
    (layout.maxHeight * height) / image.height,
  );
  const plan = planStrokes(data.strokes, image.width);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "white",
        filter: `blur(${interpolate(frame, [0, BLUR_SECONDS * fps], [24, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(0.4, 0, 0.2, 1),
        })}px)`,
      }}
    >
      <AbsoluteFill style={{ perspective: 2000, justifyContent: "center", alignItems: "center" }}>
        <Interactive.Div
          name="Camera"
          style={{
            width: image.width * fit,
            height: image.height * fit,
            flexShrink: 0,
            transformStyle: "preserve-3d",
            scale: interpolate(frame, [0, durationInFrames], [1, 1.08], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.37, 0, 0.63, 1),
              output: "perceptual-scale",
            }),
            rotate: interpolate(frame, [0, durationInFrames], ["x 7.5deg", "x -7.5deg"], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.bezier(0.37, 0, 0.63, 1),
            }),
          }}
        >
          <Interactive.Div
            name="Article"
            style={{
              position: "absolute",
              inset: 0,
              backgroundColor: "white",
              rotate: interpolate(frame, [0, durationInFrames], ["y -7.5deg", "y 7.5deg"], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: Easing.bezier(0.37, 0, 0.63, 1),
              }),
            }}
          >
            <div
              style={{
                position: "absolute",
                left: 0,
                top: 0,
                width: image.width,
                height: image.height,
                scale: fit,
                transformOrigin: "0 0",
                backgroundColor: "white",
              }}
            >
              {/* Markers are painted first and the screenshot is multiplied on
                  top: its white paper takes on the marker color while the
                  ink stays black, so the marker reads as being behind the text. */}
              {plan.map((stroke, i) => (
                <div
                  key={`${stroke.text}-${i}`}
                  style={{ position: "absolute", left: stroke.x, top: stroke.y, display: "flex" }}
                >
                  <Highlight
                    name={`Highlight: ${stroke.text}`}
                    from={Math.round(stroke.start * fps)}
                    premountFor={fps}
                    color="rgba(255, 221, 0, 0.62)"
                    iterations={1}
                    roughness={1.5}
                    seed={i * 4 + 3}
                    padding={{
                      left: stroke.padLeft,
                      right: stroke.padRight,
                      top: Math.round(stroke.height * 0.13),
                      bottom: Math.round(stroke.height * 0.23),
                    }}
                    progress={interpolate(frame, [stroke.start * fps, stroke.end * fps], [0, 1], {
                      extrapolateLeft: "clamp",
                      extrapolateRight: "clamp",
                      easing: Easing.bezier(0.5, 0, 0.3, 1),
                    })}
                  >
                    <span style={{ display: "block", width: stroke.width, height: stroke.height }} />
                  </Highlight>
                </div>
              ))}
              <CanvasImage
                name="Headline"
                src={staticFile(image.file)}
                width={image.width}
                height={image.height}
                style={{
                  position: "absolute",
                  inset: 0,
                  width: "100%",
                  height: "100%",
                  mixBlendMode: "multiply",
                }}
              />
            </div>
          </Interactive.Div>
        </Interactive.Div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

### `src/Root.tsx`

One `<Composition>` per video and orientation. `calculateMetadata` sets the
real size and length from the props, so the numbers written here are only
placeholders.

```tsx
import { Composition } from "remotion";
import { calculateMetadata, HeadlineHighlight } from "./HeadlineHighlight";
import nytMinnesota from "./headlines/nyt-minnesota-surveillance.json";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="nyt-minnesota-surveillance-vertical"
        component={HeadlineHighlight}
        calculateMetadata={calculateMetadata}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ data: nytMinnesota, orientation: "vertical" as const }}
      />
      <Composition
        id="nyt-minnesota-surveillance-horizontal"
        component={HeadlineHighlight}
        calculateMetadata={calculateMetadata}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ data: nytMinnesota, orientation: "horizontal" as const }}
      />
    </>
  );
};
```

When a new headline comes in, add its JSON import and its composition(s)
next to the existing ones. Keep earlier videos registered so they can be
re-rendered.
