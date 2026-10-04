---
name: youtube-thumbnail
description: Dedicated YouTube thumbnail generator — interviews you for exactly the style elements you want (environment, text budget, extras, accent color), then renders high-contrast, vibrant, face-consistent thumbnails with Nano Banana Pro and verifies every frame before showing it. Use whenever you want to create, redo, or iterate thumbnail variants for a video — "make a thumbnail", "new version of B", "more realistic", "less text", "put the app on the screen", "another angle for the test". Renders into videos/<project>/packaging/thumbs/. Works standalone or as the render engine for Stage 5 of /packaging (which owns titles, bets, and descriptions).
---

# YouTube Thumbnail Generator

Turns a thumbnail concept into **rendered, verified frames** — with the style built from an
**element menu you pick from**, not a fixed template. One number matters: **CTR**.

**Division of labor:** `/packaging` decides *what to bet on* (one fixed title, 3 distinct
thumbnail levers, honesty checks). This skill decides *what the frame looks like* and renders
it. Run standalone for iteration ("give me a new B"), or let packaging Stage 5 delegate here.
Both inherit two non-negotiables from packaging:

- **Honesty guardrail** — the frame must promise only what the video keeps.
- **Loud-vs-calm** — thumbnails are deliberately louder than `brand.md`. Never tone down to
  match the in-video brand.

## The baseline look (always on, never asked about)

Every render, regardless of selections: **high contrast** (deep darks OR clean brights, never
flat) · **vibrant saturated color** with one accent doing the work · **clear focal hierarchy**
(headline → hero object → face, three steps max) · **big high-energy positive face** from the
`media/library/faces/` kit · **premium, clickable finish** — crisp edges, no clutter · **every
text element perfectly spelled and razor sharp**.

These came from a real before/after CTR comparison (the "Image 13" guide, 2026-08): the flat,
low-contrast, no-hierarchy frame lost to the bold high-contrast hierarchical one ~4.4x on
views. The *axes* are always-on; the *decorations* below are strictly opt-in.

## The element menu (opt-in — this is what you ask about)

Exact prompt language for every element lives in `references/style-elements.md`. Summary:

| Element | What it is | Cost |
|---|---|---|
| `single-hook` | ONE text element, huge (word or number) | the default; cleanest |
| `tiered-headline` | small white italic context line + huge green grunge power line | +1 text block |
| `sticker` | tilted yellow badge, black caps, red underline, arrow to the hero | +1; ≤2 short words or it garbles |
| `checkstrip` | slim bottom strip, 3 green-check benefits | +3 micro-texts; busy fast |
| `brush-tag` | brush-stroke tag at strip end (e.g. WITH CLAUDE) | +1 |
| `results-fan` | fan/burst of result cards from the hero (pure imagery, no lettering) | busy-frame risk |
| `glow-burst` | neon energy + particles radiating from the hero | cheap, usually worth it |
| `real-logo` | pass the actual logo file as a `--ref` so it renders faithfully | extra ref |
| `real-app-screen` | pass a real UI screenshot as a `--ref` for the on-screen app | extra ref; micro-text caveat |

**Environments** (pick one): `dark-studio` (neon-on-black, dramatic) · `real-office` (candid
DSLR look, anchored to the real room visible in the face refs) · `bright-graphic` (saturated
studio composite, the classic loud style).

## The flow

### 1 — Locate context
Project dir, existing `packaging/thumbs/` (what letters/versions exist), the locked title if
packaging ran (thumbnail text must never repeat it), face kit present (no kit → stop and ask,
see `media/library/faces/README.md`), `GEMINI_API_KEY` in `.env`.

### 2 — The interview (the point of this skill)
**Ask before generating** — one `AskUserQuestion` round. Skip any axis the user already
specified in their request; ask only what's still open.

1. **Environment** — dark-studio / real-office / bright-graphic.
2. **Text budget** — `single-hook` **(recommended default)** / `headline-plus-one` (tiered
   headline + at most ONE accent element) / `full-kit` (headline + sticker + checkstrip +
   tag — warn that it's the busy end; opt-in only).
3. **Extras** (multi-select) — glow-burst, results-fan, real-logo, real-app-screen, a
   prop/object, none.
4. **Accent color** — green (house default) / yellow / red / cyan.

**Calibration note (real creator feedback, 2026-08): the default is MINIMAL text.** The
full-kit look was tried and rejected as "too much text"; high contrast + vibrant were
explicitly kept. Never stack every element just because the guide contains them — each text
block after the first must earn its slot.

### 3 — Confirm the words
Echo the exact hook text (and sticker/strip words if selected) before rendering. Check
against the locked title: **thumbnail text never repeats title words** — the two combine
into one message.

### 4 — Build the prompt
Assemble from `references/style-elements.md` blocks: labeled brief (Reference roles → Subject
& Action → Composition & Hierarchy → Setting & Lighting → Text → Style), letter-by-letter
spelling for every rendered word, positive framing with the one earned negation (sub-images
carry no lettering/logos). Hardware rule: laptops/phones are "generic, plain dark bezel, no
logos or lettering on the hardware" — otherwise you get a MacBook.

### 5 — Render
```
venv/Scripts/python tools/gen_thumbnail.py --prompt-file videos/<p>/packaging/thumbs/<X>.txt \
    --out videos/<p>/packaging/thumbs/<X>.png --jpg --seed <N>
```
- Default refs = the whole face kit. **Any explicit `--ref` replaces that default** — when
  passing a logo or app screenshot, re-include the face ref explicitly, and name each
  image's role in the prompt ("Image 1 = identity, Image 2 = the app").
- `real-app-screen` source: pull a frame from the project's baked preview with ffmpeg, crop
  to the window, save to `media/projects/<p>/` (reusable, committed path) — never screenshot
  by hand if the beat already exists in the video.

### 6 — Verify (every render, before the user sees it)
Read the image back: hook spelled right + legible · face reads as the creator · one dominant
focal element · bright/saturated/positive expression · hands sane (count fingers, no phantom
limbs) · no stray lettering in sub-images · hardware unbranded · honesty (screen/props match
the real product) · 16:9, JPG <2MB. Fix-and-rerender before surfacing; flag anything
borderline honestly (e.g. micro-text garble in a real-app screen).

### 7 — Iterate
- **Letters are bets, numbers are dressings** (A, A2, D3…): a new *concept* gets a new
  letter; a restyle/refinement of the same lever bumps the number. One A/B/C test slot per
  letter family.
- Before overwriting `<X>.txt`/`.png`, preserve the old one as `<X>-v1.*`.
- Hold `--seed` to iterate composition-stable; change seed to explore. Change one thing at a
  time.
- Restitch the labeled contact sheet (`thumbs/_ABC-set.jpg`) after every accepted render so
  the set is always comparable at browse-wall scale.

## Failure modes → fixes (learned on real renders)

| Symptom | Fix |
|---|---|
| Sticker/badge word garbled | ≤2 short words per badge, letters spelled out (L-I-F-E-T-I-M-E); re-render |
| Checkstrip drops a checkmark | phrase as "each item a green circular checkmark immediately followed by…" |
| MacBook bezel / brand on hardware | "generic slim laptop, plain dark bezel, no logos or lettering on the hardware" |
| Real app screen: micro-text garbles | expected — invisible at browse size; if it matters, blur-text reroll or perspective-warp the real screenshot in post |
| Face color cast (purple/green hand or skin) | name the light: "warm skin tones preserved; the screen adds only a faint cool glow" |
| Clone/double renders a stranger | "BOTH men in this image are this exact man" + give the double a distinct material (wireframe, hologram) |
| Office looks generic | anchor it: describe the real room visible in the face ref (wall color, plant) and say "match the real office behind him in Image 1" |
| Word spelled right but flat/pasted | grunge texture + soft outer glow + hard drop shadow, restate "razor sharp" |

Model ids, API details, template history: `.claude/skills/packaging/references/thumbnail-generation.md`.
Worked examples (proven prompts): `videos/video-1/packaging/thumbs/*.txt` — A2 (bright-graphic
+ full kit + real logo), B (dark-studio outcome scene), C (dark-studio clone), D2 (real-office
+ full kit), D3 (real-office + single-hook + real-app-screen).
