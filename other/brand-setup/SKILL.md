---
name: brand-setup
description: Makes this repo's videos look like YOUR channel instead of the house default — interviews you for palette, fonts, wordmark, motion energy, delivery specs and SFX taste, then rewrites brand.md + remotion/src/brand.ts + remotion/src/fonts.ts together and renders a proof card so you SEE it. Use whenever the user wants to set up or change their brand, rebrand the repo, "make it my colors/fonts", change the accent color, set their wordmark, adjust the motion feel, or asks why their videos look like someone else's. Run it once before the first video. Not for per-video art direction (that is /make-tsx) and not for thumbnails, which are deliberately louder than the brand (that is /packaging).
---

# Brand Setup

**Run this once, before your first video.** This repo ships with a house brand — a calm, premium
indigo look. It's a real, working brand, not a placeholder, and you're welcome to keep it. But if you
never touch it, every video you make here looks like the channel it came from. This skill fixes that
in one pass.

## What this skill owns

Three files that **must stay in sync**, and this skill is the only thing that should write all three:

| File | What it holds | Who reads it |
|---|---|---|
| `brand.md` | the contract, in prose | every step-2+ skill (`/make-tsx`, `/suggest-sfx`, `/packaging`) |
| `remotion/src/brand.ts` | the same tokens as code — `COLORS`, `GRADIENT`, `RADIUS`, `SHADOW`, `EASINGS`, `BRAND` | every shot |
| `remotion/src/fonts.ts` | the font families, loaded from `@remotion/google-fonts` | every shot |

**They drift silently.** `brand.md` says indigo, `brand.ts` says teal, and nothing errors — the docs
just quietly stop describing the videos. That's why one skill writes all three in one pass.

Every shot imports from `brand.ts` / `fonts.ts`, so changing a value here re-brands **every video in
the repo, retroactively.** That's the whole point of a contract.

## The flow

---

### Stage 1 — Interview (ONE message, not twenty questions)

Ask it all at once, and **say up front that "keep the default" is a valid answer to any of it** —
most people care about two or three of these and have no opinion on the rest.

1. **Channel identity** — the wordmark text, and what the channel is about in a sentence. The
   wordmark renders in three parts with the **middle part in the accent color**
   (`['Learn','With','Hasan']` → the "With" is indigo). Two-part marks use an empty third
   (`['Acme','Labs','']`). Also: the sign-off line for the end card.
2. **The feeling** — calm/premium, loud/energetic, playful, editorial, technical? This drives motion
   and shape more than color does.
3. **Palette** — do they have brand colors already (paste hex), or should you propose from the
   feeling? Light base or dark base? The accent is the single most important choice: it's the key
   words, the highlights, the CTAs, the wordmark's middle.
4. **Type** — existing brand fonts, or propose to fit the feeling? Must be Google Fonts (see the
   hard gate in Stage 3).
5. **Delivery specs** — **what does your camera actually shoot?** Resolution and frame rate. This is
   not taste; it's the one value that must match reality (see the trap below).
6. **SFX taste** — subtle accents under the voice, or louder/punchier?

---

### Stage 2 — Propose before you write

Show the full proposal in the chat **first** — palette as a table (role · hex · what it's for), the
font names, the motion feel, the delivery specs. Get a yes.

Reading hex codes in a table is cheap. Rewriting three files and re-rendering is not. Do not skip to
writing because the answers "seem clear."

---

### Stage 3 — Hard gate: the fonts must actually exist

**Fonts are the #1 way this breaks the build.** `fonts.ts` imports from `@remotion/google-fonts`, so
a family that isn't in that package fails to resolve. A local/purchased/system font will not work —
if they name one, tell them plainly and pick the closest Google family.

**Verify before writing. Both checks, every font:**

```bash
cd remotion

# 1. Does the family exist? (PascalCase, no spaces: "Space Grotesk" -> SpaceGrotesk)
ls node_modules/@remotion/google-fonts/dist/esm/ | grep -i "^Poppins\."

# 2. Does it HAVE the weights you're about to request?
grep -oE '"[0-9]{3}":' node_modules/@remotion/google-fonts/dist/esm/Poppins.mjs | sort -u
```

~1,800 families are available, so there is almost always a good match.

**The weight trap is real, not theoretical.** Space Grotesk stops at 700 — no 800/900. Oswald stops
at 700. Requesting a weight the family doesn't ship gives you a silent fallback or a broken render,
and you won't notice until a headline looks wrong. **Check, then request only what exists.**

---

### Stage 4 — Contrast gate

Text has to be readable, and a beautiful palette that fails here produces unreadable videos. Compute
it, don't eyeball it (`chroma-js` is already a dependency):

```bash
cd remotion && node -e "
const chroma = require('chroma-js');
const C = { ink:'#1a1a2e', muted:'#6b6b7b', paper:'#fffef7', accent:'#6366F1' };
const p = [['ink','paper'],['muted','paper'],['accent','paper'],['paper','accent']];
for (const [a,b] of p) console.log(a.padEnd(7),'on',b.padEnd(7), chroma.contrast(C[a],C[b]).toFixed(2)+':1');
"
```

Judge each pair **by how it's actually used**, not one blanket number:

| Pair | Used for | Gate |
|---|---|---|
| `ink` on `paper` | body text, everywhere | **≥ 7:1** |
| `muted` on `paper` | captions, secondary labels | **≥ 4.5:1** |
| `accent` on `paper` | large key words only (34px+) | **≥ 3:1** |
| `paper` on `accent` | pill/chip text, small | **≥ 4:1** |

For reference, the house default measures 16.87 / 5.17 / 4.42 / 4.42. Note the accent sits at 4.42 —
**comfortable for big words, tight for small ones.** That's the normal shape of this tradeoff: a
saturated accent that pops on a light base rarely also clears 7:1. Fine. Just don't put small text on
it.

**Below 3:1 on any pair, do not ship it — darken the shade and re-check.** Between 3:1 and the gate,
say so out loud and let them choose. Never silently accept a palette that can't be read.

---

### Stage 5 — Write all three files, in one pass

**`remotion/src/brand.ts`** — keep every exported name exactly as-is. 29 shots import `COLORS`,
`EASINGS`, `GRADIENT`, `RADIUS`, `SHADOW`, `BRAND`; renaming or dropping a role breaks all of them.
Change the **values**, never the keys. Fill every role — a palette that omits `warn` or `danger`
compiles and then explodes at render.

**`remotion/src/fonts.ts`** — swap the families and weights (verified in Stage 3). Keep
`FONT_DISPLAY` / `FONT_BODY` / `FONT_MONO` exported. `FONT_SERIF` exists only for the Claude Code
wordmark clone — it isn't a brand font, so leave it alone unless asked.

**`brand.md`** — rewrite §1–§7 and §9–§10 to match. **Do not touch §8 (Asset & source locations)** —
that's pipeline structure, not brand, and the other skills depend on it being accurate.

Keep brand.md's *shape*: the other skills read it by section, and `/suggest-sfx` reads §10 for its
SFX taste and function table specifically.

**The delivery-specs trap (§7).** Canvas + fps are the one place where taste is wrong and reality is
right: **the canvas fps must match the master cut's frame rate.** Shoot 1080p30 and it should say
1080p30. A mismatch here doesn't error — it desyncs every shot from the narration, and you'll blame
the timing before you blame the brand file. Ask what the camera shoots; never assume.

---

### Stage 6 — Prove it (do not skip)

Render the brand back at them and **read the frame yourself before showing it**:

```bash
cd remotion && npm run gen
npx tsc --noEmit
npx remotion still src/index.ts BrandProof out/brand-proof.png --frame=95
```

`BrandProof` (`remotion/src/shots/brand/BrandProof.tsx`) is a utility shot, not a video beat. It
hardcodes nothing — it reads `brand.ts` and `fonts.ts` live, so what renders is genuinely what the
shots will use. It shows the wordmark, the full palette with hex labels, the gradient, all three
fonts, the card depth, and the accent-legibility line.

Look at it and check: **is the wordmark right? Is the accent word legible? Do the fonts look like
what you proposed?** Then show them the image.

Finally, render one real example shot (`EndCard` is the fastest) to confirm nothing broke downstream.

---

## Hard rules

- **All three files or none.** Never update `brand.ts` without `brand.md`. Silent drift is the
  failure mode this skill exists to prevent.
- **Change values, never keys.** Every shot imports the token names. Renaming a color role breaks 29
  files at once.
- **Fonts must be verified in `@remotion/google-fonts` before writing** — family AND weights.
- **The palette must clear the contrast gate**, judged by usage. Below 3:1 is not shippable.
- **Delivery fps must match the camera**, not the brand's preference.
- **Don't touch brand.md §8.** It's structure, not style.
- **Never re-tune a thumbnail to match the brand.** Thumbnails are deliberately louder — they live on
  the browse wall and play by CTR rules. See `/packaging`. Two systems, on purpose.
- **The house default is a real brand, not a placeholder.** "Keep it" is a legitimate answer; the only
  thing that's genuinely wrong is shipping someone else's *wordmark* on your channel. If they keep
  everything else, still set `BRAND.wordmark`.
