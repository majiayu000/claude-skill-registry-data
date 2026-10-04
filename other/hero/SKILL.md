---
name: hero
description: "Craft the COVER — the one animated <video> hero that opens the page above the headline, built from a Scout-verified still (or an abstract generated still) via a deterministic source ladder. The cover is animated by DEFAULT; a static <img> is only the recorded last rung. Owns the hero video + its static furniture; the Interaction Engineer owns the pick-a-side overlay, the Cinematographer stages the cover as cin_00. Reuses data-des=des_hero_video (no new provenance prefix). Outputs hero.json + assets/teaser.webm + _web.mp4 + .jpg poster."
argument-hint: "[PROJECT_DIR]"
allowed-tools: Bash(*), Read, Write, Glob
---

# Hero

> **Premium-profile stage.** The orchestrator runs the Hero only in the `premium` profile; in `fast` the Designer's static cover image is used instead. The "animated cover is the default, every run has one" rules below apply *within* premium.

Your job is **the cover** — the first thing the reader sees, before the headline, before any prose. The cover is the most load-bearing detail of the whole page: it is the hook. **A crafted animated cover is the DEFAULT** — you walk a deterministic source ladder and the cover ends up a short muted `<video>` loop on every rung but the last; a static `<img>` cover is **only** the recorded final fallback when every animation rung degraded.

You own the **hero video + its static furniture** (headline band, kicker, credit, decorative monogram/chips/particles/scrim). You do NOT own the pick-a-side interactive overlay — that is the **Interaction Engineer's** `int_01`. You do NOT redo the scroll background — the **Cinematographer** stages your cover as the first cinematic scene (`cin_00`). You realize the Designer's `content.hero_strategy` as a rendered, verifiable cover.

## Setup
- `PROJECT_DIR` = first argument; `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story-pro/hero`).
- Read: `editor.json` (`interactives.hero` — does the centerpiece front-load on the teaser?), `scout.json` (verified `sct_` stills / clips), `designer.json` (`content.hero_strategy` + any registered `des_` stills), `interaction.json` (the `int_01` the centerpiece resolved to), and the shared **[`../references/topic_profile.json`](../references/topic_profile.json)** (`is_visual` / `tags` — same classifier the Detective resolved).
- Reuse the Designer's media scripts: `image2video` (`SKILL_DIR/../designer/scripts/openrouter-image2video/scripts/generate_video_from_image.py`), `text2image` (`.../openrouter-text2image/...`), and `optimize_assets.py` (`SKILL_DIR/../designer/scripts/optimize_assets.py`). Generation routes through OpenRouter (`OPENROUTER_API_KEY` must be set).
- Read [`references/hero_recipes.json`](references/hero_recipes.json) (the source ladder + the winning-pattern build recipe + the IP record) and [`references/schema.json`](references/schema.json) (the `hero.json` shape) before rendering.
- Output: `PROJECT_DIR/hero.json` + assets → `PROJECT_DIR/assets/teaser.webm` + `teaser_web.mp4` + `teaser.jpg` (poster). The hero IS the `teaser` section.

## When to run
**Always** — every run has exactly one cover. There is no "skip the hero" path: the floor of the ladder (an abstract generated still, animated) is always available, so even a sober computational topic with no star entity gets a *moving* cover. The only thing the ladder decides is *which* source feeds the cover, never *whether* there is one. (A genuinely abstract topic still gets a cover; it is just an atmospheric/abstract one, often the `interactive` rung.)

## Step 1 — Resolve the source (the deterministic ladder)
Walk the rungs in [`references/hero_recipes.json`](references/hero_recipes.json) `source_ladder` and take the **first that resolves** — this is deterministic, not a free pick. Record the chosen rung in `meta.source_ladder_rung` + a one-line `meta.why`:

0. **Interactive-hero passthrough** — if `editor.json.interactives.hero` is non-null AND its `section == "teaser"`, the centerpiece interaction is the Interaction Engineer's `int_01`. Render the **animated backdrop** behind it (descend rungs 1-4 for the still/motion) and yield the click surface: set `hero.interactive_overlay_ref = "int_01"`. You own the video + static furniture; the Interaction Engineer owns the pick-a-side overlay.
1. **Scout real still (no public figure)** → `image2video` the still into a cinemagraph; default Veo is fine for non-faces.
2. **Recognizable real PUBLIC FIGURE, WITH a fetched identity-verified photo** → `image2video --model kwaivgi/kling-v3.0-std` (the one faces-safe model — **Veo/Wan deterministically refuse real faces, code 15236754**). This is **allowed-with-conditions**, not banned: the face is held enough to avoid warping, but **subtle natural motion IS permitted** (slight head/body sway, a blink) on top of the moving atmosphere/lighting. **Warp-quality guard:** reject any candidate where the face distorts → fall back to ffmpeg Ken-Burns + boomerang on the same still (faces stay original pixels). Set `subject_is_real_public_figure:true` + a **proportionate** AI-motion-added `disclosure` (a small caption that the motion was added / it is not real footage — lightweight, not a banner). The thing that stays disallowed is generating the face **from scratch** (photoreal OR illustration) — the still here is always FETCHED.
3. **License-clean STOCK clip** → a Scout `sct_` `kind:"video"`. **R5 constraint:** stock video isn't fetched today (`fetch_stock.py` is images-only), so restrict this rung to a **Commons/Openverse CC clip or a verified oEmbed** — not a paid stock-video API. A copyrighted self-hosted clip is a `des_` `publish_blocker` (see the IP record).
4. **Abstract/atmospheric still** → `text2image` a no-real-referent still (mood/texture/metaphor), then `image2video` it. The always-available floor that keeps even a sober cover *moving*.
5. **Static fallback (only)** → ship the poster as a static `<img>`: `kind:"image"`, `assets.video_webm/_mp4 = null`, with a recorded `media_blocker`. The ONLY sanctioned static-cover path — reachable only when every animation rung degraded (`image2video` printed `FALLBACK_USED=static_poster` / `VIDEO_UNUSED=1`, or no clip/still could be produced).

The real-subject guard from the Designer doctrine still holds: a recognizable real subject is a **FETCHED** verified still (Scout `sct_` / Detective `ref_`), never a generated one; `image2video` of a real face is only ever a held cinemagraph (subtle motion within the warp guard) via the faces-safe model with proportionate disclosure. The model facts (which models refuse real faces, the `4/6/8` duration constraint, the upscale recipe) live in [`references/hero_recipes.json`](references/hero_recipes.json) `ip_record` (and the Designer's `video_pipeline.json`).

**Honor `topic_profile.ai_face_policy` (real-person subjects).** When the Detective resolved an `ai_face_policy` (the topic involves real people — see [`../detective/SKILL.md`](../detective/SKILL.md) and [`../references/topic_profile.json`](../references/topic_profile.json)), it governs the cover. The default is **animate the real photo**: a real-person subject WITH a fetched, identity-verified photo → rung 2 (the subtle cinemagraph + warp guard + proportionate disclosure above). **AI face is allowed-with-conditions, never blanket-banned here.** When the real-person subject has **NO usable verified photo** (`no_photo_fallback:"theme_first_no_person"`), do **NOT** generate the person — neither a photoreal fake **nor an illustration of the person** — and skip rung 2; instead take a **THEME-FIRST non-person** cover, in this order, stopping at the first that expresses the theme: (a) **real scene/object media** — license-clean real imagery of the setting/objects/symbols (NOT the person), animated per rung 1/3; (b) **data-as-cover** — the story's signature visualization animated (the data IS the theme); (c) **conceptual / typographic** cover; (d) **abstract atmospheric** (generative, non-figurative) via rung 4 — **last resort only**. Theme-first means: if real scene/object media or the data can carry the theme, do **not** drop to the abstract floor. **Sensitivity is NOT a hard gate** — animate regardless of context and optimize for quality; if `ai_face_policy.sensitivity_advisory` is set (deceased persons, minors, criminal allegations), carry it through as a one-line note for the Critic — it never blocks the build.

## Step 2 — Render + optimize
- Animate with a **motion-only** prompt (describe only what moves: `flags ripple, smoke drifts, floodlights flicker; subject and faces held still, no camera shake`). **The cover must read as ALIVE at a glance — never near-still.** Require a clearly-**visible PRIMARY** motion + **1-2 strong SECONDARY** motions. **GOOD:** the canonical `hero_v5` — a player standoff with national flags **waving boldly** behind (subjects held, atmosphere unmistakably moving). **BAD:** `the dusk sky and thin clouds drift slowly, a faint pulse` over an otherwise-static stadium (a subtle cinemagraph that reads as a still — the weak current output, a richness fail). When the subject itself must stay still (building / landscape / held face), **require a bold animated foreground**: rippling/waving flags, a surging crowd, rising smoke/steam/embers, a sweeping floodlight, strong sky parallax. **Motion is IN-PLACE / cyclic** (wheels spinning, flags waving, smoke rising, crowd surging, sky drifting) — **never translate the subject across/off the frame** (a train driving off-screen / a rocket flying out of frame cannot loop seamlessly). Pick the concrete motion concept from [`references/hero_recipes.json`](references/hero_recipes.json) `topic_motion_library` (topic-adaptive; free choice within the guides). Keep the source still as the `<video poster>` so the cover degrades to frame-0. Duration is one of `4 | 6 | 8` (the OpenRouter video endpoint accepts no other).
- **Seamless loop (hard):** post-process every hero clip into a clean loop so head meets tail invisibly — a raw model clip almost always jumps. **Default = ffmpeg boomerang/ping-pong** (forward then reversed: `[0]reverse[r];[0][r]concat`, inherently seamless); **alt = crossfade the loop point** (`xfade`, blend last ~0.5s into first ~0.5s) when reverse looks unnatural. ffmpeg is **not on PATH** — resolve it via the `imageio-ffmpeg` wheel (`python3 -c "import imageio_ffmpeg,sys;sys.stdout.write(imageio_ffmpeg.get_ffmpeg_exe())"`), exactly as `optimize_assets.py` does. **Record the technique in `hero.json` as `loop`** (`"boomerang" | "xfade" | "native"`); the on-page `<video>` keeps the `loop` attribute. (The ffmpeg Ken-Burns fallback is already a boomerang.)
- After the render, **always** run `python3 SKILL_DIR/../designer/scripts/optimize_assets.py PROJECT_DIR/assets/` — it writes the VP9 `.webm` + H.264 `_web.mp4` + poster and repoints filenames. **Web-weight cover budget: < 3 MB.** (A heavier 2K upscaled hero is tolerated only when the page can clearly afford it — see `hero_recipes.json` / the Designer's `ai_upscale`; the default ships the optimized `_web` copies.) Reference the `_web` copies in `hero.assets`.
- Verify the files exist (`ls -la PROJECT_DIR/assets/teaser.*`). If `image2video` printed `FALLBACK_USED=...`, transcribe it into `hero.source.fallback_used`; `static_poster` means the cover degraded to a still → set `kind:"image"` and the rung-5 fields + a `media_blocker`.

## Step 3 — Spec the on-page build (the Programmer builds it; `validate.py` asserts it)
You **spec** this contract on the hero item; the **Programmer** builds it; **do NOT edit the frozen verify engine** — the `.cin-stage` wrapper makes the cover verify-immune with zero engine edits:
- The cover is a `<video webm+mp4+poster autoplay loop muted playsinline>` (or a `<img>` on the rung-5 fallback), **wrapped in `.cin-stage`** — cinematic-ON it is the `cin_00` layer of the live cinematic stage; cinematic-OFF a degenerate `<div class="cin-stage hero-only-stage">` that still paints the poster as backdrop. Either way the existing `isDecorative()` (which excludes `el.closest('.cin-stage')`) auto-excludes the cover from Verify.
- A reduced-motion `<img>` fallback (the poster) is always in the DOM; under `prefers-reduced-motion` / JS-off it shows and autoplay never fires. The `<video>` keeps `autoplay muted loop playsinline` (those attributes are correct — do **not** change them).
- **Autoplay-retry** (additive over the attributes above): muted-autoplay can be **blocked** on iOS Low-Power / some mobile, leaving the cover frozen on the poster. So the Programmer also wires a JS `video.play()` **retry on the first user gesture** — a one-time handler on the broad first-interaction set (mirror the BGM `sndKick` multi-event pattern: `pointerdown`/`touchstart`/`keydown`/`click` + `scroll`/`wheel`/`touchmove`), removed only on a resolved `.play()` promise — plus a visible **tap-to-play** affordance (a centred play glyph over the cover) shown if `.play()` rejects. Skip the retry under `prefers-reduced-motion`.
- A **single `.teaser` overlay** carries `data-des="des_hero_video"` — the cover's one Verify hit. Decorative furniture (VS monogram, FC-26-style chips, particle canvas, headline band, scrim) is `pointer-events:none` with **no `data-*`**; on rung 0 the interactive halves are `role="link"` (off the verify inner-interactive allow-list).
- Reuse `data-des="des_hero_video"` — **NO new provenance prefix** is minted.

The winning-pattern build recipe (the flagship cover: held-subject cinemagraph + transparent furniture overlay + the cinematic-stage handoff) is in [`references/hero_recipes.json`](references/hero_recipes.json) `build_recipe`.

## Output — `hero.json`
Full schema in [`references/schema.json`](references/schema.json). `hero` is a single object (exactly one cover). Reuses `data-des="des_hero_video"` — no new prefix:
```json
{
  "meta": { "role": "hero", "version": "1.0", "source_ladder_rung": 2, "why": "the real star is the cover subject; Kling animates the fetched still" },
  "hero": {
    "id": "des_hero_video",
    "kind": "video",
    "backs": "teaser",
    "subject_is_real_public_figure": true,
    "source": {
      "origin": "scout_real_figure", "still_ref": "sct_03",
      "model": "kwaivgi/kling-v3.0-std", "tool": "image2video",
      "prompt": "flags ripple, floodlights flicker; faces and subject held still, no camera shake",
      "duration": 6, "fallback_used": null
    },
    "loop": "boomerang",
    "assets": { "video_webm": "assets/teaser.webm", "video_mp4": "assets/teaser_web.mp4", "poster": "assets/teaser.jpg" },
    "reduced_motion_fallback": "assets/teaser.jpg",
    "furniture": { "headline_band": "Who wins 2026?", "kicker": "World Cup forecast",
                   "credit_line": "Photo: <author> / Wikimedia Commons (CC BY-SA 4.0) — identity verified; motion added",
                   "decorative": ["VS monogram", "particle canvas", "scrim"] },
    "interactive_overlay_ref": "int_01",
    "verify": { "hit_target": ".teaser", "data_attr": "data-des", "id": "des_hero_video", "class_marker": "teaser" },
    "disclosure": "Fetched verified still; motion = a camera move on the still (not AI video of a real person).",
    "publish_blocker": false,
    "ip_record_ref": "references/hero_recipes.json#ip_record"
  }
}
```

## Team coordination
- **Interaction Engineer** owns the pick-a-side overlay (`int_01`) when the Editor places the centerpiece on the teaser (rung 0); the Hero owns the video + static furniture and references it via `interactive_overlay_ref`. The two coexist — the overlay's halves are `role="link"`, off the verify inner-interactive allow-list.
- **Cinematographer** consumes the cover as `cin_00` via [`../cinematographer/references/cinematic_recipes.json`](../cinematographer/references/cinematic_recipes.json) `hero_as_cin_00_continuous_backdrop` — the same crossfade engine carries the cover seamlessly into `cin_01`. The hero's Verify hit stays on the `.teaser` overlay (`data-des=des_hero_video`), NOT on `cin_00`.
- **Designer** hands over `content.hero_strategy` (the rung intent) + any registered `des_`/`sct_` stills; the Hero realizes that strategy as the rendered, verifiable cover. The animated cover is the default — a static cover is only the recorded last rung.
- **Programmer** builds the `.cin-stage`-wrapped `<video>`/`<img>` + the single `.teaser` hit + the reduced-motion fallback + the autoplay-retry per Step 3; **Inspector `validate.py` Section 12** asserts the assets resolve on disk, the poster + reduced-motion are present, the `.teaser` carries `data-des`, the video sits inside a `.cin-stage` wrapper, **`hero.json` carries a `loop` marker, and the page wires an autoplay-retry** (the last two WARN by default, ERROR on a visual topic).

## References
- [`references/schema.json`](references/schema.json) — the full `hero.json` shape + field notes.
- [`references/hero_recipes.json`](references/hero_recipes.json) — the source ladder, the winning-pattern build recipe, and the IP record (Veo/Wan refuse real faces code 15236754; Kling works; the fallback ladder; the AI-likeness disclosure; the stock-clip publish-gate).
- [`../cinematographer/references/cinematic_recipes.json`](../cinematographer/references/cinematic_recipes.json) — `hero_as_cin_00_continuous_backdrop`, the seamless hero→scroll handoff.
- [`../designer/references/video_pipeline.json`](../designer/references/video_pipeline.json) — the still→motion mechanics (cinemagraph pipeline, the faces table, the upscale recipe, disclosure).
- [`../references/topic_profile.json`](../references/topic_profile.json) — the shared `is_visual` / `tags` classifier.

Done when the cover is a rendered, web-weight, **animated** `<video>` (or, only on the recorded last rung, a static `<img>` with a `media_blocker`), `hero.json` records the chosen ladder rung + the single `data-des="des_hero_video"` Verify hit, the assets resolve on disk, and the Programmer can wrap it in `.cin-stage` with a single `.teaser` provenance hit and a reduced-motion fallback.
