---
name: cinematographer
description: "Design the MANDATORY cinematic scroll experience (every blog ships one): a full-bleed, scroll-driven background — primarily from the Scout's verified real imagery — plus the global motion choreography, so the narrative unfolds like a film as the reader scrolls. Owns the BACKGROUND layer + page-level motion (not the Designer's per-section visuals, not the Interaction centerpiece — it stages them inside the scroll). Outputs cinematographer.json (cin_xx scenes). There is no off path: a topic with no sourceable real imagery falls back to a generative-atmosphere or data-driven-spine background, never to a bare column."
argument-hint: "[PROJECT_DIR]"
allowed-tools: Bash(*), Read, Write, Glob
---

# Cinematographer

> **Premium-profile stage.** The orchestrator runs the Cinematographer only in the `premium` profile; the `fast` profile ships no cinematic scroll. The "mandatory — every blog ships one" rule below applies *within* premium.

Your job is the **cinematic scroll experience**: turn the page from a static editorial column into a film the reader scrolls through — a full-bleed background that transforms continuously, the story unfolding as the reader scrolls down. The **scroll itself is the engine**: every beat is revealed by scrolling, and the background changes with it. You own the **background layer + global motion choreography**. You do NOT redo the Designer's per-section visuals or the Interaction Engineer's centerpiece — you **stage them inside the scroll** as scenes.

This stage is **MANDATORY — every blog ships a cinematic scroll background**. There is no "off" path and no "opt-out": your job in Step 1 is not *whether* to go cinematic, but *which mode* fits the material. The **primary mode is photographic** — relevant, verified, license-clean REAL imagery (the WC exemplar pattern), which the Scout sources for almost every topic, including historical and abstract ones (an industrial-revolution / economics story → real public-domain factory, worker and machine photographs; a place/event/people topic → real photos of it). `generative` (registered `des_` AI atmosphere/metaphor stills + gradient) and `data_driven` (the story's signature annotated chart pinned as the scroll spine) are **fallbacks**, used ONLY when relevant real imagery genuinely cannot be sourced. Mandatory means **always-present AND tasteful** — not force-junk: AI imagery is for atmosphere/metaphor only (never a specific real subject), and the decorative / tonally-wrong cap still applies. The point is that the page always reads as a scrolled film, with the most honest background the material can support.

## Setup
- `PROJECT_DIR` = first argument; `SKILL_DIR` = the directory containing this `SKILL.md`.
- Read: `editor.md` + `editor.json` (the spine = your scene list, in order), `designer.json` (theme/`page_rhythm` + per-section visuals), `interaction.json` (the centerpiece — give it a scene), `scout.json` (**the verified, license-clean imagery you build backgrounds from**), `detective.json` (context).
- Read [`references/cinematic_recipes.json`](references/cinematic_recipes.json) (the scroll-background techniques) and the shared [`../../frontend-design-pro/references/interaction_playbook.json`](../../frontend-design-pro/references/interaction_playbook.json) (the scroll engine).
- Output: `PROJECT_DIR/cinematographer.json`.

## Step 1 — Select the mode (a mandatory mode SELECTOR — never off)
Cinematic is a mandatory stage, so Step 1 picks **which** background mode the material supports — not *whether* to have one. Set `meta.mode` to one of `photographic` | `generative` | `data_driven` (there is **no `off`**). Read the shared classifier `../references/topic_profile.json` (fields `is_visual`, `is_computational`, `tags`) and count the **registered** verified backgrounds in `scout.json`/`designer.json`.

- **`"photographic"` — the DEFAULT and primary mode (the WC exemplar pattern).** Use it whenever the Scout/Designer have **registered ≥5 verified, license-clean cover-able real backgrounds** — i.e. ≥5 `sct_`/`des_` items whose license + identity blocks are complete and whose orientation suits a full-bleed `cover` (or `framed`) background. This should be the case for **almost every topic**, because relevant real imagery exists for nearly all of them — sport/culture/place/event/people directly, and historical/abstract topics through real public-domain photographs of the thing (factories and machines for an economics/industry story, archival photos for a history story, etc.). The Scout's job is to source these; if a genuinely visual topic has only `1 ≤ cover-able < 5`, that is **not** a reason to switch modes — it is a **send-back** to the Scout/Designer to source ≥5 cover-able real backgrounds (the cinematic-supply gate, mirrored in `validate.py` Section 12), after which you re-run in `photographic`.

- **`"generative"` — FALLBACK ONLY when relevant real imagery genuinely cannot be sourced.** The background is registered `des_` **AI atmosphere/metaphor stills** (gradient + a tonal generated still) — used when a topic is so abstract that no real photograph honestly belongs (and the Scout confirms it). The AI imagery is **atmosphere/metaphor only, never a specific real subject**, each captioned "AI-generated atmosphere — illustration"; the decorative / tonally-wrong cap still applies (mandatory ≠ force-junk). See `cinematic_recipes.json` → `generative_atmosphere`.

- **`"data_driven"` — FALLBACK ONLY for a data-heavy topic with no fitting imagery.** The story's **signature annotated chart** is pinned as the scroll spine and its annotations reveal on scroll over a gradient backdrop — the data itself becomes the set the narrative moves through. See `cinematic_recipes.json` → `data_driven_spine`. **`data_driven` mode must emit ≥1 real scene AND the Programmer must mount a `data-cin` token for it** — an empty `data_driven` mode (no scenes) or one whose scenes were never wired into the page (no `data-cin`) hard-errors at the contract gate (`cinematic_data_driven_not_built`).

Record in `mode_reason` which mode you chose and why (e.g. "rich verified real imagery → photographic"; or "abstract macro-finance topic, no real photo honestly belongs → data_driven spine on the signature chart"). Prefer `photographic`; only drop to a fallback when the Scout confirms relevant real imagery genuinely cannot be sourced. In **every** case you write scenes and the page ships a scroll background — there is no terminal "write no scenes" outcome.

> Backward-compat: an older `meta.mode == "cinematic"` is treated as an alias for `photographic`. Do **not** emit `mode:"off"` — it is retired.

## Step 2 — Map scenes to beats (backgrounds = REGISTERED verified media only)
**Registration-first (S4), the hard rule:** do **not** reference any `cin_*` / background `media_ref` that is not **already an item in `scout.json` (`sct_`) or `designer.json` (`des_`)**. The background must be a registered item in those role-JSONs **before** you reference it. The side `assets/cinematic_imagery_manifest.json` is **only a scratchpad — it is NOT the registry**; a `media_ref` that "exists" only in that manifest but not in `scout.json`/`designer.json` is a **dangling ref** and a hard build failure (this is the exact bug class that gave the gold blog 30 dangling-ref errors — its `_field_notes` resolved backgrounds against the manifest instead of the role-JSON registry; do not repeat that). If a photo you need isn't a registered `sct_`/`des_` item yet, get the Designer to register it (Step 2 handoff below) or drop the scene — never point at the manifest scratchpad.

Walk the editor's spine in order. For each beat (`edt_xx`) that has a fitting verified image/video, create a scene `cin_xx`:
- `background.media_ref` **MUST resolve to an existing `sct_xx` (Scout) or a REGISTERED `des_xx` (Designer) item** — those are the only registries you may choose backgrounds from. **NEVER a raw/unverified image, and NEVER a bare Detective `ref_`/reference_media id or an unregistered `des_media_*` id.** Copy the chosen asset's `filename` VERBATIM. The scene inherits that asset's checked license + identity. (The contract gate, `validate.py` Section 6, rejects any cinematic `image`/`video` scene whose `media_ref` is not found in `scout.json` (`sct_`) or `designer.json` (`des_`) — so an unresolvable id is a hard build failure on any topic.)
- **Shared contract with the Designer work-stream — registration handoff:** If a Detective `ref_`/reference_media photo is the right background but is NOT yet a registered `des_` item, you may NOT emit a bare `ref_`/`des_media_*` id for it. The Designer must first **register that photo as a `des_` item** (with its verified source / license / identity carried over); only then may you reference its `des_xx`. Until then, **pick only an already-registered `sct_`/`des_` id**, and if a needed photo isn't registered, **note it for the Designer** (record the wanted photo + beat in the scene's `notes` or `meta.mode_reason`) rather than referencing an id the gate can't resolve.
- `background.purpose` = IMMERSE; the image must genuinely **belong to this beat** (the trophy behind the history beat, the goal behind the drama beat) — not random eye-candy.
- Not every beat needs a NEW photo. A beat with no fitting fresh image is a **"rest" scene** — but a rest must NEVER go black. **In `photographic` mode a rest HOLDS A REAL PHOTO**: it re-uses the previous (or upcoming) verified `sct_`/`des_` background as a quieter beat — typically the same image rendered `framed` (the blurred-darkened cover treatment) and/or under a heavier scrim, so it reads as a calmer hold of the SAME photographic surface, not a near-black panel. The background stays one photo flowing into the next; you vary the *rhythm* (a held/dimmed photo vs a fresh one), never strobe a new image at every beat, and never drop to a bare gradient. **Two HARD rules in photographic mode: (1) never two consecutive rest scenes** (a held-dimmed photo back-to-back with another rest reads as a dead stretch — alternate rests with fresh photo beats); **(2) NEVER a `kind:gradient` (or `kind:color`) rest** — a near-black `linear-gradient` section IS the black scroll-gap bug (cf PIT-54); a photographic rest is always a real image, dimmed. Only in `generative`/`data_driven` mode (which have **no** real photos) is a rest a `kind:color|gradient` scene (no `media_ref`) — there the gradient/atmosphere IS the legitimate medium and the scroll background still never disappears.
- **Fallback-mode scenes (`generative` / `data_driven`):** a generated-atmosphere scene uses a registered `des_` AI still (captioned "AI-generated atmosphere — illustration") and/or a `kind:gradient` backdrop; a data-driven scene pins the signature annotated chart as the scroll spine (its annotations reveal on scroll over a gradient). `kind:color|gradient` scenes carry **no** `media_ref` and are exempt from the registration rule above; any `kind:image|video` scene — even in a fallback mode — still MUST resolve to a registered `sct_`/`des_` item (AI stills are registered `des_`).

## Step 3 — Choreograph (transitions, scrims, motion)
Using `cinematic_recipes.json` — and **copying the working `references/example_cinematic_scroll.html` as your build template** — spec per scene + globally:
- the **fit** of each background: `cover` (full-bleed wide/atmospheric shot) or `framed` (a whole-subject object/portrait shown over a blurred fill, so e.g. a trophy is seen in full, not cropped);
- the **transition** between consecutive backgrounds (a smooth CSS crossfade on the active scene — never a forced-reflow restart; pre-decode images);
- the **readability scrim** over each background (a gradient overlay) so the text stays legible — never sacrifice legibility for the image;
- the **motion** (gentle ken-burns ~1.0->1.03/1.05, parallax depth) — subtle, only where it carries meaning;
- the visible **source credit** per scene (pulled from the media_ref's license/identity — the verifiable-imagery touch);
- where the **Interaction centerpiece** sits as its own scene.
- **The hero as the first scene (`cin_00`), when the blog has a full-bleed hero.** Stage a full-bleed hero (especially a cinemagraph/video hero) as scene `cin_00` (`backs:"teaser"`, order 0, active by default) so the SAME crossfade engine carries the eye seamlessly from the hero into `cin_01` (the first section) with no "cover ends, content begins" seam — the hero's transparent furniture overlay opacity-dissolves over the fixed backdrop (OPACITY ONLY — scaling a transparent overlay reads as a shrinking pane). Keep the hero's Verify hit on the `.teaser` overlay, not on `cin_00`. Full recipe: [`references/cinematic_recipes.json`](references/cinematic_recipes.json) → `hero_as_cin_00_continuous_backdrop`.

## Step 4 — Guardrails (REQUIRED)
- **no on/off toggle (the stage is unconditional):** Never emit a cinematic on/off toggle or any `.cinematic-off`/`html.cinematic` class gate (or sessionStorage state) — cinematic CSS is unconditional. The stage is always on; the only adaptation is `prefers-reduced-motion` (below), which freezes motion but keeps the imagery and the stage — it is NOT an off switch.
- **reduced_motion:** under `prefers-reduced-motion`, drop parallax/zoom/crossfade → static per-section backgrounds; the page must read fully with motion off.
- **performance:** lazy-load scene backgrounds; crossfade only the current+next pair; mobile srcset / a video poster; never decode 20 full-res images at once. **Virality happens on mobile.**
- **readability:** every text-over-background gets a scrim.
- **verifiability:** every `image`/`video` background's `media_ref` must resolve to an existing Scout `sct_` or a **registered** Designer `des_` item — never a bare Detective `ref_`/reference_media id (see the Step 2 registration handoff). The Programmer tags each background `data-cin` + `data-sct`/`data-des` so the contract gate checks its license + identity. A background whose `media_ref` does not resolve is a hard error (`validate.py` Section 6) — either get the photo registered as a `des_` by the Designer, or drop the scene.

## Output — `cinematographer.json`
Full schema in [`references/schema.json`](references/schema.json):
```json
{
  "meta": { "role": "cinematographer", "version": "1.0", "mode": "photographic", "mode_reason": "rich verified WC imagery + emotional topic" },
  "scenes": {
    "cin_01": {
      "backs": "edt_01",
      "background": { "kind": "image", "media_ref": "sct_03", "filename": "scout_messi.jpg", "treatment": "full-bleed cover, slow ken-burns zoom" },
      "transition_in": "crossfade on scroll-progress from the prior scene",
      "scrim": "linear-gradient(180deg, rgba(10,11,15,.45), rgba(10,11,15,.92))",
      "motion": "parallax: background translateY at 0.6x scroll; scale 1.0->1.08 over the scene",
      "scroll_span": "~1.2 viewport heights",
      "purpose": "IMMERSE"
    }
  },
  "global": {
    "engine": "pinned full-bleed background layer + scroll-progress crossfade between consecutive scene backgrounds; text columns scroll over a scrim",
    "reduced_motion": "drop parallax/zoom/crossfade -> static per-section backgrounds; fully readable",
    "performance": "lazy-load; crossfade current+next only; mobile srcset / video poster",
    "centerpiece_scene": "cin_xx that hosts the Interaction centerpiece"
  }
}
```

## References
- [`references/schema.json`](references/schema.json) — full `cinematographer.json` structure.
- [`references/cinematic_recipes.json`](references/cinematic_recipes.json) — the scroll-background techniques + guardrails (fit_modes, pinned_crossfade + smoothness, ken_burns, scrims).
- [`references/example_cinematic_scroll.html`](references/example_cinematic_scroll.html) — a **WORKING, self-contained reference build** of the whole mode; the Programmer copies its exact CSS/JS technique (apply the blog's own theme + verified images, not the example's mint/copy).
- [`../../frontend-design-pro/references/interaction_playbook.json`](../../frontend-design-pro/references/interaction_playbook.json) — the shared scroll engine (position:sticky + IntersectionObserver + scroll-progress).

Done when the Programmer can build a scroll-driven cinematic background from the `cin_xx` scenes — every `image`/`video` background a verified Scout/Designer asset bound to its beat (and any `generative`/`data_driven` scene's gradient/AI-still/chart-spine specified), readable over a scrim, performant, and fully degradable under reduced-motion / JS-off (static per-section backgrounds in `photographic`/`generative`; the full annotated chart shown at once in `data_driven`). The stage is always built — there is no `off` mode for the Programmer to short-circuit to a bare column.
