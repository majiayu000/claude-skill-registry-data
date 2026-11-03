---
name: carousel-generator
description: "Designs fire 4:5 (1080x1350) Instagram carousels with a HYBRID engine: an AI-generated cover (Higgsfield/Nano Banana Pro) for the thumb-stopping slide 1, then a token-locked HTML/CSS design system for the body slides. Claude writes the cover concept + slide copy in the creator's voice + a JSON manifest, you generate the cover, preview the real deck, then Playwright screenshots crisp 2x PNGs — plus a caption package with the offer CTA (from backbone/offer.md). Saveable template library for repeatable decks. No Canva. Triggers: make a carousel, instagram carousel, ig carousel, carousel generator, turn this into a carousel, slide deck for instagram, 4:5 slides, design a carousel, trend carousel, news carousel, post carousel."
---

> **Video Studio:** this skill lives in `engines/content-os` (Content OS, inside this repo). Before running anything from it, `cd engines/content-os` and use that folder's copy (`.claude/skills/carousel-generator/`), which has its scripts and reference files. Every path below is relative to that folder. This copy only lets Claude find the skill from the Video Studio folder.


# Carousel Generator — hybrid AI-cover + HTML body, 4:5 IG carousels

Turns a topic / trend / news item / post (or a pipeline pick) into a polished Instagram carousel: an **AI-generated cover image** for slide 1, **token-locked HTML/CSS** body slides, crisp 1080×1350 PNGs + a caption package.

**Why hybrid (the whole point):** pure-HTML carousels all look the same — that's the AI-slop tell. The single highest-leverage slide is the cover (the thumb-stopper), so we generate it with a real image model (Nano Banana Pro) for a striking, differentiated look. The body slides don't need to be visually stunning — they need to deliver value fast, cheap, and repeatably — so they stay in the token-locked HTML system (free, instant re-roll, perfectly consistent, voice-locked copy). Best of both: AI-image differentiation on the cover, designer-grade consistency everywhere else.

**Text is never baked into the cover image.** The image model generates the *visual only* (textless). The headline is overlaid in HTML by the renderer — so copy stays crisp, editable, on-brand, and free to re-roll without re-generating the image. (AI glitch-text is impossible.)

## The Flow

```
0. One-time bootstrap: bash .claude/skills/carousel-generator/install.sh (from the project root).
1. Claude gathers the content (topic, or a trend/news/post the creator pastes) + optional inspiration.
2. Claude writes carousel.json at carousel/outputs/<slug>/carousel.json (project-root relative):
     - ONE theme + ONE font + per-slide layouts + copy in the creator's voice
     - a `cover` block: a TEXTLESS cinematic image prompt for slide 1
3. COVER GEN — python3 cover.py carousel/outputs/<slug>/carousel.json (python on Windows)  →  cover variants land in
   carousel/outputs/<slug>/cover/. Claude (or the creator) picks the best, sets slides[0].image to it.
4. PREVIEW GATE — render.js --preview opens the real composited deck in your default browser. The creator eyeballs it.
5. On approval, render → 2x PNGs + caption.md + contact_sheet.png beside the manifest in carousel/outputs/<slug>/.
```

All commands in this skill are written from the **project root** (the folder that contains `.claude/`), so script paths are `.claude/skills/carousel-generator/scripts/...`. The manifest, its `cover/` variants, and the rendered PNGs all live together in `carousel/outputs/<slug>/`, so a deck can be re-previewed, re-copied, or saved as a template any time later.

The preview is the safety gate — the creator sees the actual design (cover image + overlaid text + body slides), not JSON, before it's final. Edit copy/tokens in the manifest and re-preview freely; re-rolling copy or layout costs nothing (only the cover image costs credits).

**Reuse:** once a deck performs, save it as a template (`library.js save`). Later, "do carousel v10 on this topic" = `library.js new <template> <slug>` + swap the copy + re-gen the cover. The look is locked, the copy is fresh.

## Step 3 — Writing the cover concept (the AI image)

The `cover` block drives `cover.py`. Write the `concept` like a cinematic photography brief, not a description of a slide:

- **Textless, always.** End every prompt with: `no text, no screens, no user interface, no buttons, no logos`. Text is added in HTML.
- **No UI metaphors.** Never name screens, terminals, dashboards, chat bubbles, app windows. Substitute *physical machine metaphors* — sleek machines, gears, control panels rendered as objects, robotic arms, glowing cores, workbenches. (Same no-UI-metaphor rule as any Higgsfield thumbnail prompt.)
- **Match the creator's mood, not a generic stock look.** Read the niche + voice lines in `CLAUDE.md`'s Creator Profile and the positioning principle in `backbone/messaging.md`, then pick a physical world that fits. Example: a builder/operator brand reads as workbench / lab / industrial-studio, real machines rather than stage polish; no Lambos, no fake luxury.
- **Cinematic spec words that work:** "cinematic", "photoreal", "ultra high contrast", "single key light / rim light", "volumetric haze", "shallow depth of field", "matte black", plus an accent color that matches the deck theme (e.g. electric-blue for `midnight`/`azure` (default), acid-lime for `obsidian`, magenta for `plum`).
- **Leave headroom for text.** The headline overlays the bottom third with a dark scrim — keep the visual interest in the upper/center of the frame.

```json
"cover": {
  "concept": "Cinematic product-hero shot of a sleek matte-black machine on a raw concrete workbench in a dim industrial studio, single cool key light raking across it, faint electric-blue rim glow, volumetric haze, shallow depth of field, photoreal, ultra high contrast, no text, no screens, no user interface, no logos",
  "face_refs": false,
  "aspect": "4:5",
  "variants": 3
}
```

- `face_refs` — default **false** (scene/object covers). Set **true** to put the creator in the shot (pulls `assets/face-refs/`); use only when the concept genuinely calls for a person.
- `aspect` — default `"4:5"` (matches the canvas). The cover is `object-fit: cover` cropped to fill 1080×1350 regardless, so a near-ratio still fills cleanly.
- `variants` — images per concept (default 3). For multiple cover *directions*, use `"concepts": [{ "id": "a", "prompt": "..." }, { "id": "b", "prompt": "..." }]` instead of `concept`.

Run it from the project root: `python3 .claude/skills/carousel-generator/scripts/cover.py carousel/outputs/<slug>/carousel.json` (`--dry-run` prices it without submitting, `--variants N` overrides the count, `--only-concept <id>` generates a single direction from a multi-concept `concepts[]`). The `[y/N]` confirm only appears when a human runs it at a TTY; from Claude's Bash (no TTY) it submits straight away, and `--yes` forces that from a terminal too. Each image ≈ 2 credits. It downloads to `cover/` next to the manifest and prints the path to drop into `slides[0].image`.

## Token Menus — pick ONE theme + ONE font per deck

Consistency across slides is the #1 "professionally designed" signal. **One theme, one font, for the whole deck.** Don't mix. Match the cover concept's accent color to the theme. Pick the theme whose accent matches the creator's brand color (`brand-kit.md` when present) or the post's energy; `midnight` is only the fallback default, not anyone's brand.

### Themes (`theme`)
| key | mode | vibe |
|---|---|---|
| `midnight` | dark | electric blue on deep navy — clean SaaS/tech *(default)* |
| `azure` | dark | brighter cyan-blue on ocean navy — punchy, high-energy blue |
| `cloud` | light | electric blue on cool grey — crisp, corporate-clean (light blue) |
| `obsidian` | dark | acid-lime on near-black — modern, techy, high-energy |
| `amber` | dark | warm amber on charcoal — confident |
| `plum` | dark | magenta on aubergine — bold, punchy |
| `forest` | dark | mint on deep green — fresh, calm-but-modern |
| `paper` | light | vermilion on warm paper — editorial, premium |
| `sage` | light | green ink on bone — earthy, trustworthy |

### Fonts (`font`)
| key | display / body | vibe |
|---|---|---|
| `character` | Bricolage Grotesque / Hanken Grotesk | modern with personality, clean *(default)* |
| `heavy` | Hanken Grotesk 800 / 450 | minimal, single-family, punchy |
| `grotesk` | Space Grotesk / Hanken Grotesk | techy, geometric |
| `editorial` | Fraunces (serif) / Hanken Grotesk | premium magazine editorial |
| `impact` | Anton / Hanken Grotesk | loud, condensed, ALL-CAPS impact |

Pairing guide: techy hot-take → `midnight`+`character` *(default)*. Bolder blue energy → `azure`+`heavy`. Premium/story → `paper`+`editorial`. Loud/contrarian → `midnight`+`impact`. Match the energy of the post and the cover.

## Layouts (`slides[].type`)

Each slide is one layout. **Slide 1 should be `cover_image` (the AI cover); last slide `cta`.** Vary the body slides.

| type | fields | use for |
|---|---|---|
| `cover_image` | `image`, `headline`, `kicker?`, `subhead?`, `swipe?` | **slide 1, the default** — AI cover image full-bleed, text overlaid at the bottom |
| `cover` | `kicker?`, `headline`, `subhead?`, `swipe?` | typographic (no-image) cover — the fallback when you don't want an AI cover |
| `statement` | `kicker?`, `headline`, `body?` | one big idea per slide |
| `list` | `kicker?`, `headline?`, `items[{title, body?}]` | numbered steps / breakdown (2–5 items) |
| `media` | `image`, `headline?`, `kicker?`, `body?` | body slide with a raster image — a screenshot, product shot, or web image |
| `stat` | `kicker?`, `value`, `label`, `body?` | a big number (a view count, a dollar figure, hours saved) |
| `quote` | `quote`, `attribution?` | a member win or punchy line |
| `cta` | `kicker?`, `headline`, `body?`, `action?`, `button?` | last slide — the funnel ask |

- **`image` field** (on `cover_image` + `media`): a local path (relative to the manifest file), an absolute path, an `http(s)` URL, or a `data:` URI. `render.js` downloads/embeds it as base64 automatically — the deck stays self-contained. Cover images come from `cover.py`; `media` images are usually real screenshots the creator provides (GitHub, a product, a result) or a web image URL.
- `swipe` on a cover: short cue text (`"How it works"`, `"Swipe →"`); set `false` to hide.
- `action` (cta) renders as a bold line w/ accent bar; `button` renders a filled accent pill. Use one.
- **Inline emphasis in any text:** `*word*` → accent color, `**word**` → bold ink. Use sparingly (one highlight per headline max). Never put markdown/emphasis in an `image` field.

## Manifest Schema

Illustrative example only: `<...>` are placeholders, the stat value and the quote are made-up shapes, not real figures. Real numbers come from `backbone/messaging.md`'s proof bank; offer name and comment keyword from `backbone/offer.md`.

```json
{
  "slug": "example-system-breakdown",
  "topic": "How I <got the result> with one simple system",
  "theme": "midnight",
  "font": "character",
  "handle": "@yourhandle",
  "cover": {
    "concept": "Cinematic matte-black machine on a concrete workbench, electric-blue rim glow, volumetric haze, photoreal, ultra high contrast, no text, no screens, no UI, no logos",
    "face_refs": false,
    "aspect": "4:5",
    "variants": 3
  },
  "slides": [
    { "type": "cover_image", "image": "cover/cover_v2.png", "kicker": "<KICKER>", "headline": "I <got the result> with one simple system", "subhead": "Here's the exact build — steal it.", "swipe": "How it works" },
    { "type": "statement", "kicker": "THE PROBLEM", "headline": "You're the bottleneck in your own <workflow>.", "body": "Every <task> waits on *you*." },
    { "type": "list", "kicker": "THE BUILD", "headline": "3 parts, one pipeline", "items": [
      { "title": "Trigger", "body": "What kicks it off automatically." },
      { "title": "Worker", "body": "The part that does the actual job." }
    ]},
    { "type": "media", "kicker": "PROOF", "headline": "It runs while I sleep.", "image": "shots/run.png", "body": "Real run, zero hands on keyboard." },
    { "type": "stat", "kicker": "THE RESULT", "value": "1.2M", "label": "views on one post" },
    { "type": "quote", "quote": "I went from X to Y in Z.", "attribution": "a member" },
    { "type": "cta", "kicker": "YOUR MOVE", "headline": "Want the exact system?", "body": "I break down every build inside <offer name>.", "action": "Comment <KEYWORD> and I'll send the link" }
  ],
  "caption": {
    "hook": "I <got the result> with one simple system. Here's the build 👇",
    "body": "Most people think they have a <X> problem...",
    "cta": "Comment <KEYWORD> and I'll send you the link to <offer name>.",
    "hashtags": ["#<niche-tag-1>", "#<niche-tag-2>", "#<niche-tag-3>"],
    "first_comment": "optional — drop the link / extra context here"
  }
}
```

Optional manifest flags: `show_page_numbers` (default true), `show_progress` (top ticks, default true).

## Design Rules (baked in — respect them in COPY)

The template enforces layout/type/color. Your job is copy that fits:

- **Slide count: 6–9.** Cover + 4–7 body + CTA. Under 6 feels thin, over 10 loses people.
- **Cover hook < 12 words.** It's a thumb-stopper, not a sentence. Front-load the payoff or tension.
- **One idea per slide. ≤ ~125 characters of body per slide.** Walls of text are the #1 AI-slop tell — auto-fit shrinks huge blocks, but that means you wrote too much. Cut.
- **`list` items: 2–5 max**, each title ≤ 4 words, body one line.
- **`media` body caption: one line.** The image is the point; the caption just frames it.
- **No emoji *in slides*** (headless Chromium has no color-emoji font — they render as boxes; also they read amateur). Emoji are fine in the `caption` (plain text).
- **Numbers/proof beat adjectives.** Use `stat` slides for real, *exact* figures from `backbone/messaging.md`'s proof bank (views, revenue, hours saved, followers) — never round, never invent.
- Write in **the creator's voice**: read `voice-dna.md` (openers, minimizers, re-hooks, anti-patterns) and the voice one-liner in `CLAUDE.md`'s Creator Profile; document real systems from `backbone/messaging.md`, don't manufacture hype.

## Funnel CTA (every carousel ends here)

One offer, one motion. Every carousel's CTA slide + caption CTA tie to the offer in `backbone/offer.md` (offer name, positioning, deliverables, comment keyword; never hardcode the price in copy, read it from the backbone if it has to appear). Close templates:

- "Comment <KEYWORD> and I'll send you the link." *(comment-keyword is the default close; use the keyword `backbone/offer.md` names if it has one, else one word that names the giveaway)*
- "Join <offer name>. <one-line positioning from backbone/offer.md>."
- "<anti-positioning line from backbone/messaging.md's positioning principle>."

Example only: "Comment SYSTEM and I'll send you the link to the community."

A soft mention can appear mid-deck; the hard ask is the `cta` slide. Never pitch anything `backbone/offer.md` marks as retired, dead, or not sold (its "What is NOT sold" list when it has one); no side-door CTAs. Never drop the CTA by accident.

## Template Library — repeatable decks

```bash
# from the project root
node .claude/skills/carousel-generator/scripts/library.js list                                # show saved templates
node .claude/skills/carousel-generator/scripts/library.js new <template> <slug> [--out PATH]  # scaffold carousel/outputs/<slug>/carousel.json (--out PATH to put it elsewhere)
node .claude/skills/carousel-generator/scripts/library.js save <manifest.json> <name>         # save a deck you like as a reusable template
```

Templates live in `templates/*.json` (theme + font + cover concept + layout skeleton + placeholder copy; embedded base64 images are stripped on save so they stay tiny). Seeded with `ai-system-breakdown` and `myth-vs-reality`. The workflow: `new` a template → swap the copy + cover concept → `cover.py` → `render.js`.

## Usage

```bash
# All from the project root (the folder containing .claude/).
SKILL=.claude/skills/carousel-generator

# 0. One-time bootstrap (npm deps + Playwright Chromium). THE install path, run it once per machine:
bash $SKILL/install.sh
#    (optional) scaffold a manifest from a saved template:
node $SKILL/scripts/library.js new ai-system-breakdown my-slug     # -> carousel/outputs/my-slug/carousel.json

# 1. Generate the cover image (after writing cover.concept in the manifest):
python3 $SKILL/scripts/cover.py carousel/outputs/<slug>/carousel.json
#    then set slides[0].image to the variant you picked (e.g. "cover/cover_v2.png").

# 2. Preview the real composited deck in your default browser (the approval gate):
node $SKILL/scripts/render.js carousel/outputs/<slug>/carousel.json --preview

# 3. Render final PNGs + caption + contact sheet (opens the sheet):
node $SKILL/scripts/render.js carousel/outputs/<slug>/carousel.json

# Options:
#   --scale 1     -> exact 1080x1350 (default 2 -> crisp 2160x2700; IG downscales cleanly)
#   --out DIR     -> override output dir (default: the manifest's own directory)
#   --no-open     -> don't auto-open the result
```

Output lands beside the manifest in `carousel/outputs/<slug>/`: `slide_01.png … slide_NN.png`, `caption.md`, `contact_sheet.png` (+ `preview.html` from preview runs), with the cover variants in `carousel/outputs/<slug>/cover/`. Everything for one deck is in one folder.

## Posting (manual)

Carousels are posted by hand: upload the `slide_01.png … slide_NN.png` set in the Instagram app and paste the caption block from `caption.md`. `auto-poster` is single-media only (one video or one image per post), so it cannot publish a multi-slide carousel. This skill stops at files + caption.

## Gotchas

- **Cover gen needs the Higgsfield CLI** installed + authed (`higgsfield auth login`; check is `higgsfield account status`). See README. If you only want a typographic cover, skip `cover.py` and use `type: "cover"` for slide 1.
- **One-time bootstrap before the first full render:** `bash .claude/skills/carousel-generator/install.sh` from the project root (npm install + Playwright Chromium). Without it, `render.js` dies at `require("playwright")` with MODULE_NOT_FOUND (preview mode still works — playwright loads only on the full-render path). If it later errors with "Executable doesn't exist" (Chromium cache wiped: `~/Library/Caches/ms-playwright` on macOS, `~/.cache/ms-playwright` on Linux, `%LOCALAPPDATA%\ms-playwright` on Windows), just re-run `install.sh`.
- **`cover.py` needs network** (Higgsfield API + image download). In Claude Code, run its Bash call with the sandbox disabled or it fails on the CLI call. `render.js` (Chromium) runs fine inside the sandbox.
- **Output is manifest-relative, not cwd-relative.** `render.js` writes slides, caption, and contact sheet into the manifest's own directory (`carousel/outputs/<slug>/` when you follow the convention); pass `--out DIR` to put them elsewhere. Run everything from the project root so `library.js new` and the docs' relative paths line up.
- **Images embed as base64** at render time — output is self-contained and identical on any machine. A bad/missing image path warns (`[carousel] missing image …`) and renders without it rather than crashing.
- **Cover image paths are relative to the manifest file**, not the cwd. `cover.py` drops them in `cover/` next to the manifest, so `"image": "cover/cover_v2.png"` just works.
- **`face_refs: true` with no photos** prints a loud `[cover] WARNING ... 0 reference photos` and generates without a face anchor. Photos go in `assets/face-refs/` at the project root (the skill resolves it from its own install location under `.claude/skills/`).
- **Auto-fit shrinks oversized headlines** to fit. If text looks small, the copy is too long — shorten it.
- **Preview vs final must match** — both use `template.html`. If they differ, something's wrong; don't ship.
- **One theme + one font per deck.** Per-slide overrides are intentionally unsupported (consistency is the design).
- **Posting is manual** (see Posting above). Don't hand the PNG set to `auto-poster`; it takes one media file per post.

## What This Skill Does NOT Do

- Pull research/trends automatically (Claude gathers the content first, or the creator pastes it).
- Post or schedule (carousels go up by hand in the IG app; `auto-poster` is single-media only).
- Generate AI imagery for *body* slides (only the cover is AI-generated; body images are real screenshots/product/web images you provide — by design: keeps body slides fast, cheap, consistent).
- Edit the design system from chat — to add a theme/font/layout, edit `template.html`'s token objects.
