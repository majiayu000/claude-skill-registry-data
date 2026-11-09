---
name: text-motion
description: >-
  Kinetic text-motion + gradient + transition toolkit for HTML/CSS motion-graphics videos —
  the polished "launch reel" look: keyword glow-highlight sweeps, gradient-filled hero words,
  scramble-decode headlines, ticker-roll word swaps, living color-arc gradient backgrounds with
  drifting blobs, concentric ring ripples, blueprint grids, and glass UI accents (pills, cursors,
  prompt cards). Use when making an animated title/heading feel dynamic and varied, adding a
  moving gradient background, giving each scene its own heading entrance, or matching a
  reference reel's text motion. Triggers: "make the headings more dynamic", "text motion",
  "highlight the keyword", "gradient background through the video", "animate the title like that
  reel", "scramble/decode text", "words rolling like a ticker", "make it more graphic".
  Complements kinetic-typography (word cascade / hero-push) and smooth-render (capture).
---

# Text Motion

Drop-in building blocks (`assets/textmotion.css` + `assets/textmotion.js`) for varied, dynamic
text motion and living backgrounds in plain HTML — distilled from launch-reel references and a
full documentary build. The point: **stop every heading animating the same way**, and give the
frame constant subtle motion (gradient + blobs) so nothing feels like a static slide.

All CSS timing scales by `--R` so effects survive slow-clock rendering. Every JS updater takes a
**logical time `t`** (your clock, in seconds) — call them from your render/rAF loop, never off
wall-clock, or motion speeds up under capture.

```html
<link rel="stylesheet" href="assets/textmotion.css">
<script src="assets/textmotion.js"></script>
```

## Pick a different entrance per heading (variety is the fix)
Reference reels never repeat one text move. Assign each scene its own:

| Effect | When to use | How |
|---|---|---|
| **Word-rise** | default, calm lines | `tmSplit(el)` then `tmReveal(el,t0,t1,t)` |
| **Scramble-decode** | crypto/tech/reveal beats | `tmScramble(el,'PLAIN',t0,t1,t,'<em>final</em>')` |
| **Keyword sweep** | the one word that matters | wrap it `<span class="tm-kw">word</span>`, `tmSweep(kw,at,t)` |
| **Gradient-fill hero** | big single-word hero | `<span class="tm-grad">Online</span>` |
| **Ticker-roll** | a slot cycling synonyms | `.tm-ticker>.tm-roll>i…`, `tmTicker(roll,t0,t)` |
| **Punch** | quick emphasis pop | `<span class="tm-punch">`, `tmPunch(el,at,t)` |
| **Typewriter + cursor** | a mark/dot is already travelling the frame | `tmTypeBuild(el,words,{pay})` then `tmType(el,t)` + `tmTypeCursor(el,t)` |
| **Highlighter pill** | the payoff word of a typed line | wrap it as the `pay` run — it lands in an accent pill that wipes in, white letters, 6° tilt settle |

### Keyword glow-highlight sweep (ref: "Truly **highlight** what matters", "**promotion?**")
The strongest, most-copied move: a light bar sweeps behind the key word, which then stays lit.
```html
<h3>Encryption ends where usefulness begins:
    <span class="tm-kw warm">in use</span></h3>
```
```js
tmSweep(document.querySelector('.tm-kw'), /*cue*/ 1.2, t);   // per frame
```
Variants: `.tm-kw` (mint), `.tm-kw.purple`, `.tm-kw.warm`. Add `.lit` fires automatically 0.35s after the sweep.

### Scramble-decode headline (ref: cipher reels)
```js
tmScramble($('#h'),'Could a machine compute on what it cannot read?',
           0.1, 1.5, t, 'Could a machine compute on what it <em>cannot read?</em>');
```

### Ticker-roll (ref: single-word heroes swapping)
```html
Your <span class="tm-ticker"><span class="tm-roll" id="rl">
  <i>intelligence</i><i>code</i><i>secrets</i><i>data</i><i>prompts</i></span></span> flows out.
```
```js
tmTicker(document.getElementById('rl'), /*scene t0*/ 0, t);  // holds word 1, then rolls; mask width tracks each word
```

## Living gradient background (ref: mesh / radial / ripple reels)
A background that **narrates**: a color arc across the film + slow drift = constant motion with
zero "busy" feeling.

```html
<div class="tm-gradbg" id="bg">
  <div class="tm-blob b1"></div><div class="tm-blob b2"></div><div class="tm-blob b3"></div>
</div>
<!-- your content sits above with z-index > 0 -->
```
```js
const ARC = {                      // one palette per scene = the story turn
  problem:{ga:'#0e1622',gb:'#070a12',b1:'#26375e',b2:'#1a3a4e',b3:'#2a2a44'},
  cost:   {ga:'#161008',gb:'#0a0806',b1:'#6e5220',b2:'#3a2f5e',b3:'#7a4a1a'}, // warm/amber
  answer: {ga:'#0b1512',gb:'#080a12',b1:'#1e5a4e',b2:'#3a2f6e',b3:'#2a5a4a'}, // teal
  brand:  {ga:'#1a1206',gb:'#0a0708',b1:'#8a6522',b2:'#6e3f6e',b3:'#a05a2a'}, // gold reveal
};
tmGrad(bg, ARC[scene]);            // on scene change (CSS blends it)
tmDrift(bg, t);                    // every frame (logical time)
```
Extras: `.tm-rings` + `tmRings(host)` for concentric ripples (ref: "AI SaaS Animation");
`.tm-grid` for a blueprint field (ref: "Introducing").

> **Critical for rendering:** softness comes from radial-gradient *falloff*, **never
> `filter:blur()`** — blur is ~10× slower in headless Chromium/Edge (software-rasterized) and
> drops capture to ~5fps. This one rule is why the blobs are gradient-only.

## Glass UI accents (ref: prompt card, "Let's go" pill, live cursors)
The "design-tool" motif: a glass pill/button, a prompt card, or named collaborator cursors
gliding to the text.
```html
<span class="tm-pill">Let's go ✦</span>
<img class="tm-cursor" id="cur" src="cursor.svg">
<div class="tm-tag" style="background:#e8552e">Sarah</div>
```
```js
tmCursor(cur, [[0.3,50,46],[1.0,36,44,true]], t);   // path: [t, x%, y%, click?]
```

## Transitions between scenes (no more plain cross-fades)
- The shared `.tm-gradbg` persists, so a scene change is a **content cross-dissolve over a moving
  gradient** — already feels intentional.
- Use `.tm-sc` on every scene layer for the fade **plus a visibility flip after it** — this lets
  scene backgrounds be transparent (so the gradient shows) without the previous scene ever
  bleeding through. Toggle `.on` on the active scene each frame.

## Spark-driven text (typewriter · cursor · pill · echoes)
When something is already travelling through the frame — a logo, a dot, the spark from a reference
reel — the text can belong to it: the line **types**, the travelling element is the **cursor**, the
payoff word lands in a highlighter **pill**, and **ghost echoes** ripple off it.
```js
tmTypeBuild(line, [{w:'Block',at:0},{w:'it,',at:.31},{w:'in',at:.52},
                   {w:'real',at:.64},{w:'time.',at:.88}], {pay:[4,4], echo:true});
tmType(line, t);                                   // per frame
const c = tmTypeCursor(line, t, {space: stage});   // {x,y} of the typing edge — ride your mark there
```
The whole family (A17–A22) is written up in [PLATTER.md](PLATTER.md) under
**"A″ · Spark-driven text"**. The background half of the move — the rings the mark flew along, the
lit arc behind it, the glow where it landed — is the **mark-driven-ground** skill.

## Part of the motion-graphics super-skill
This skill is family **A (text)** of the **motion-graphics** umbrella. The full named menu of ~40
moves across all families (backgrounds, elements, glass/UI, transitions, UI/data) lives in
`motion-graphics/PLATTER.md`, and the shared building-block library (24 helpers) is mirrored in
`motion-graphics/assets/motion.{css,js}` (same source as this skill's `assets/textmotion.{css,js}`).
Ask for "the platter" to get the whole menu.

## Composes with
- **kinetic-typography** — word-cascade + hero-push staging (this skill is the effect *library*).
- **smooth-render** — render to MP4; scale CSS durations by `1/rate` via `--R`, drive JS updaters
  by logical time, and keep the `filter:blur` rule above or capture starves. Pause ambient
  animations when idle: `document.documentElement.classList.toggle('tm-paused', !playing)`.
- **vo-sync** — set each effect's cue time from VO word timestamps so the sweep/scramble/punch
  land on the spoken word.

## Notes
- Units in the assets are `%`/`em` so blocks scale to any container; set the accent palette via
  `--tm-accent / --tm-accent2 / --tm-warm` on `:root` or a wrapper.
- Give each scene a *distinct* entrance — the whole reason this skill exists is that identical
  headings read as a slideshow.
