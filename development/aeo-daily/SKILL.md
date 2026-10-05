---
name: aeo-daily
version: 0.6.0
description: |
  Local AEO daily content engine — FORKED VOICE + voice filter (v0.4.2). One command → today's pack across 5 BUSINESS channels by default (was 11). Travel pack on-demand via --voice flag.
  BUSINESS voice (5 channels, default): LI personal, FB page, IG pro, YT pro, TikTok pro. Carousel + reels + comment-bait.
  TRAVEL voice (6 channels, on-demand): FB profile, IG travel x2, TikTok travel x2, Pinterest. Daily-life narrative, no agency talk.
  Pipeline writes single MASTER.html (all channels embedded as iframes + sticky TOC) at outputs/<DATE>/MASTER.html.
  All saved to <repo>\outputs\YYYY-MM-DD\copy.json (forked schema, see config/copy-schema.json).
  Legacy v0.3 still supported: --legacy flag falls back to single LI post + 8-slide carousel.

  Voice = the author's locked LinkedIn template (contrarian hook → reframe → → arrow lines → vulnerability beat → CTA + 5-8 hashtags).
  Authenticity layer required: 1 local anchor per post (named cafe / local currency / scooter / your local spot).
  1 real client win referenced (a SaaS client / a real-estate client / dental flagship / a client).
  Voice-linted before render via lint_voice.py — hard-fails on 60+ AI tells.

  Hook-bank rotation locked: Mon test-LLMs / Tue prompt-exposure / Wed contrarian /
  Thu client-proof / Fri tool-stack / Sat builder-life / Sun meta-recap.
  Each day = 2 hook variants for A/B pick.

  Replaces v2 n8n cloud flow. $0 infra. Runs in Claude Code.

  Trigger: "/aeo-daily", "today's aeo pack", "ship today's content", "aeo daily content".
license: MIT
compatibility: claude-code
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# /aeo-daily v0.6 — Local Daily AEO Content Engine

Ships **1 LinkedIn post (voice-clean) + 8-slide carousel + comment-bait reply pack + GHL CSV row** every day.

Source repo: `<repo>`

> **WEDGE (locked 2026-06-08):** ONE thing this engine sells — **"Get Cited": make SMBs the answer ChatGPT / Perplexity / Gemini gives.** Every BUSINESS post points at that. TRAVEL voice is NOT a second business — it is the **proof-of-life layer** of the same wedge (solo operator running an AI agency from a local cafe). Default `--voice business`. Travel runs 3x/week max on personal IG/TikTok only, never competing for the business CTA, with at most ONE subtle bridge line/week ("built this from a local cafe").
>
> **FUNNEL (locked 2026-06-08):** content is not the product, leads are. Every business post carries a `funnel` block `{cta_keyword, lead_magnet_ref, booking_link}`. Flow: reel/post -> comment keyword (e.g. CITED) -> DM auto-reply -> free **AEO Visibility Snapshot** (`scripts/snapshot_gen.py`) -> book call. Snapshot = lead magnet + demo + close in one. CTA bank: `funnel/cta-bank.json`. DM script: `funnel/dm-flow.md`. Full spec: `funnel/README.md`.

---

## CHANGELOG

- **v0.6.0 (2026-06-08):** WEDGE + FUNNEL + engine truth-up (4-agent fanout). (1) **Wedge locked** = "Get Cited" AEO-for-SMBs; travel demoted to 3x/wk proof-of-life layer (see WEDGE callout above). (2) **Funnel built** — `scripts/snapshot_gen.py` (AEO Visibility Snapshot lead magnet, client-presentable cream/purple HTML), `funnel/cta-bank.json` (10 one-word keyword CTAs, zero "DM me"), `funnel/dm-flow.md`, `funnel/README.md`. `copy.json` now carries a `funnel` block. (3) **Missing scripts now REAL** — the v0.5.0 vaporware is built: `config/scroll-hooks.json` (150 hooks / 15 triggers, `___` blanks, `_meta.angle_to_category`), `scripts/suggest_hooks.py`, `scripts/export_text.py`, `scripts/export_variants.py`, `scripts/build_master_html.py`. (4) **lint_voice.py hardened (v1.2.0)** — now enforces `ai_tell_structures` (negation-parallelism / rule-of-three / balanced-pair-warn / framework-promise), scans ALL business channels (was linkedin.post only), added U+2018 + funnel.cta_keyword rule (fail under --strict, warn without), UTF-8 stdout fix. (5) **Engagement loop live (true v0.6)** — `analytics/weekly.csv` + `scripts/weight_hooks.py` -> `config/hook-weights.json`; `suggest_hooks.py` reorders an angle's categories by learned cta_trigger weight. (6) **client-wins.json refreshed** (+5 real wins through 06-07). Canonical psych-category vocab = the 15 hyphen-named categories in scroll-hooks.json (weekly.csv must use them).
- **v0.5.0 (2026-06-07):** HOOK LIBRARY wired in. New `config/scroll-hooks.json` = 150 scroll-stopper hooks across 15 psychology triggers (curiosity-gap, loss-aversion, contrarian, identity-callout, transformation, secret, authority, urgency, shock, question, specificity, story-loop, problem-agitate, confession, benefit), each with `___` blank for any topic. New `scripts/suggest_hooks.py` maps weekday angle → best psych categories and prints N filled hooks (deterministic, `--offset` to rotate). New MANDATORY PHASE 2.5 — engine ALWAYS surfaces 8 matched hooks before writing copy; LI hook + video 0-4s beat must be built from them. Browsable viewer `HOOK-LIBRARY.html` (live topic-fill + filter + search + copy).
- **v0.4.2 (2026-05-20):** TRAVEL SOFT-DISABLED by default + MASTER.html + image v2.
  - `build_pack_v2.py` new `--voice business|travel|all` flag (default `business`). Travel platforms skipped from render loop unless explicitly requested. Travel code path preserved — flip to `--voice all` to resume both tracks. `run-aeo-daily.bat` now passes `--voice business` for the 07:00 local-time auto-build.
  - `scripts/build_master_html.py` new — fans every channel pack into ONE `MASTER.html` (iframes + sticky TOC + angle header + GHL CSV download block). Auto-invoked by `build_pack_v2.py` right after `INDEX.html`. Voice filter respected → travel iframes simply don't exist when skipped.
  - `INDEX.html` template no longer renders empty "Travel Voice" section when 0 travel cards present.
  - `process_image.py` v2 — face-detect now runs on ANY filename NOT starting `DJI_` (was: only `IMG_*`, missed all `SCENE-*` portraits). Multi-cascade union (`frontal_default` + `frontal_alt2` + `profileface` with horizontal flip). CLAHE histogram equalize before detect → recovers faces in shaded/backlit outdoor frames. Headroom guard in `_crop_to` shifts crop DOWN when face would clip top edge (kills "forehead at hairline" bug). Per-ratio focal-Y lift — 1×1 → 0.40, 4×5 → 0.38, 9×16 → 0.32 (face lands in upper third for reels). `--debug` flag for verbose face-detect logging.
- **v0.4.1 (2026-05-19 PM):** Round-3 production patch. (a) `build_ghl_csvs.py` is now schema-aware: tries nested `copy[track][slug]` first, falls back to legacy flat keys → 4 travel CSVs (`ig_travel_1/2`, `tt_travel_1/2`) no longer SKIPPED on extended schema. New `--copy` flag accepts override path. Image refs sourced from `_picks_log.json` (Track C source-of-truth) with avatar-dir glob fallback. (b) `config/hook-bank.json::image_picker_hints` now holds real filename PATTERNS (glob) + literal stems pulled from rotation pool, never invented filenames. (c) `build_pack_v2._resolve_image_hint` supports glob matching (`DJI_*`, `SCENE-2026-*-street-*`) in addition to exact/prefix. (d) `copy.image_picks` MUST reference real stems or glob patterns — see PHASE 3 note below.
- **v0.4.0 (2026-05-19):** FORKED VOICE schema. copy.json now contains shared{} + business{linkedin,fb*page,ig_pro,yt,tt_pro} + travel{fb_profile,ig_travel_1,ig_travel_2,tt_travel_1,tt_travel_2,pinterest} = 11 per-platform variants written in one pass. New `travel_rotation` 7-day hook bank added to `config/hook-bank.json` (cafe-discovery / visa-life / expat-mistake / scooter-day / food-find / builder-life / week-recap-travel). `lint_voice.py --voice business|travel|both` enforces both tracks independently. Travel voice hard-blocks AEO/agency/client/SkynetLabs/schema/n8n/MRR/Loom/Fiverr terms + DM-me CTAs. Image picker hint per voice — business uses IMG*\_ portraits, travel uses DJI\_\_ + scene\_\* scenes. Schema doc at `config/copy-schema.json`.
- **v0.3.0 (2026-05-18):** brand palette swap (drop pure-black → cream base + brand purple #6b3fa0 + cyan #2dc6d6 + coral #ff6b5b + gold detail), 2→4 photo picks (portrait priority — IMG*\* over DJI*\*), photo prominence (hook bg duotone, context top strip, data 2-photo grid, CTA gold-bordered portrait), per-role slide styling (hook/context/data/confession/fix/cta classes).
- **v0.2.0 (2026-05-18):** 5→8 slide carousel (research: 60% dwell gap), voice-lint script (60+ AI tells blocked), client-wins + local-anchor + banned-phrases configs, hook variants A/B per day, hashtag tail required, comment-bait reply pack (first 60 min), founder-voice + local authenticity layer, arrow glyph fix (→ not ▸).
- **v0.1.0 (2026-05-18):** initial scaffold + 5-slide pipeline.

---

## VOICE FORK — v0.4 (READ FIRST)

The engine now writes 11 per-platform variants in 2 voices in a single pass.

### BUSINESS voice (5 channels: linkedin, fb_page, ig_pro, yt, tt_pro)

- Voice spine = locked LinkedIn template (contrarian hook → reframe → arrow lines → vulnerability beat → CTA).
- Anchor: local-life PUNCH (one specific detail dropped mid-post).
- Client win mandatory (`shared.client_win_ref` from `config/client-wins.json`).
- Hashtags: business pool (`#aeo #linkedinmarketing #agencyowner #automation #brandtracking #claudecode #n8n #b2b`).
- Hook bank: `config/hook-bank.json` → `rotation[<weekday>]`.
- Image picker: IMG\_\* portraits (face-on-camera).
- Lint: `python scripts/lint_voice.py --date <DATE> --voice business --strict`.

### TRAVEL voice (6 channels: fb_profile, ig_travel_1, ig_travel_2, tt_travel_1, tt_travel_2, pinterest)

- NO AEO, NO agency, NO client pitches, NO SkynetLabs, NO schema/citation/n8n/MRR/B2B talk.
- Self-deprecating, observational. Local daily-life (cafes, scooters, beach, expat scene, food, local-currency prices).
- Anchor: local-life DRIFT (one detail per post, plus 1 named place + 1 real currency amount).
- Story anchor mandatory (`travel.fb_profile.story_anchor`) = small embarrassing/funny moment.
- Hashtags: travel pool (`#travel #digitalnomad #nomadlife #expatlife #cafehopping #scooterlife #slowtravel`). Blocklist: any business tag.
- Hook bank: `config/hook-bank.json` → `travel_rotation[<weekday>]`.
- Image picker: DJI*\* + scene*\*.jpg + IMG_4\*\*\* scenes (NOT portraits).
- Lint: `python scripts/lint_voice.py --date <DATE> --voice travel --strict`.
- Banned CTA patterns: "DM me", "I'll reply with X", "follow for more", "save this".

### Travel rotation (locked v0.4)

| Day | Angle             | Sample hook                                                                      |
| --- | ----------------- | -------------------------------------------------------------------------------- |
| Mon | cafe-discovery    | "New cafe in town. Flat white was cheap. Wifi held for 2 hours."                 |
| Tue | visa-life         | "Visa run on Tuesday. Agent quoted the 60-day rate. Standard."                   |
| Wed | expat-mistake     | "Rented a scooter without checking the brakes. Found out at the first downhill." |
| Thu | scooter-day       | "Cross-town on the scooter today. 90 minutes if you skip the toll."              |
| Fri | food-find         | "Local plate for a few bucks at a spot behind the apartment. Extra sauce added." |
| Sat | builder-life      | "Saturday looks like: wifi-cafe morning, beach walk noon, local dinner."         |
| Sun | week-recap-travel | "Week recap: 1 visa run, 2 new cafes, 1 wipeout learning to surf."               |

### Lint both tracks in one call

```bash
python scripts/lint_voice.py --date <DATE> --voice both --strict
```

---

## VOICE — LOCKED (the author's reference posts, do not flatten)

### Reference POST 1 — "Freelancer → Operator" reframe (his top-engaging)

> Stop calling yourself a freelancer.
> Words shape ceilings.
> Freelancer says: "I trade hours for cash."
> Operator says: "I run systems that deliver outcomes."
> The market pays operators 10x more. Same skills. Different label. Different price.
> → Stop saying "rate" → start saying "engagement"
> → Stop saying "available hours" → start saying "client capacity"
> → Stop sending invoices → start sending retainer agreements
> → Stop chasing leads → start filtering inbound
> What's on your LinkedIn headline today? Calling myself out first — mine literally said "freelancer" 12 months ago.

### Reference POST 2 — "Claude Routines killed my n8n flows"

> I spent 2 years building automations on n8n.
> Last week, Claude Routines replaced three of them in under 10 minutes.
> No nodes. No webhooks. No 2 AM error emails.
> Just a text box and a schedule.
> Here's one I'm running daily at 9 AM:
> → Pulls last 24-48 hrs of news across AI automation, n8n, Claude API, Next.js, Meta Ads
> → Filters for what's actually relevant to my agency and content pipeline
> → Writes 30-45 sec vertical video script — hook, body, CTA — ready to film
> I wake up. Script is waiting. I shoot. I post.
> A genuine ask to the builders here: What's the most creative Routine you've deployed?

### Voice spine (every post)

1. **Contrarian hook** — 1 line, ≤210 chars, ≤10 words ideal (hits 2.3x engagement per 2026 LI data).
2. **Reframe** — 2-3 short lines, fragments OK.
3. **Arrow lines** (`→`) — 3-5 items (keep glyph per voice memory — do NOT use ▸ ▪ • or em-dash).
4. **Personal vulnerability beat** — admit specific past mistake, dated ("12 months ago" / "last quarter" / "the dental call last week").
5. **CTA question + compile-promise** — "drop X below, I'll reply with Y."
6. **Hashtag tail** — 5-8 tags (`#aeo #linkedinmarketing` etc).

### Anti-AI authenticity layer (NEW v0.2 — required)

- 1 **anchor** per post — a named local cafe, a ride-hail detail, a local-currency amount, a power-cut, a surf/commute time, or another concrete detail from your city.
- 1 **real client win** referenced — slug from `config/client-wins.json` (dental-flagship / real-estate-voice / saas-email / healthcare-workflow / security-av / travel-client-site).
- Allowed local code-switch sparingly: 1-2 colloquial words from your own dialect (max 1 per post, italicized).
- Mid-post drift allowed — "Anyway." / "Scratch that, actually —" / trail-off ellipsis (`...` straight, not `…`).

---

## BANNED PATTERNS (lint_voice.py hard-fails)

Full list: `config/banned-phrases.json`. Highlights:

**Phrases:** delve, moreover, navigate, leverage, robust, seamless, holistic, transformative, groundbreaking, pivotal, evolving landscape, in essence, at its core, the real question is, embark on, foster, harness, "let that sink in," "read that again."

**Openers BANNED:** "Unpopular opinion:" / "Hot take:" / "Plot twist:" / "Real talk:"

**Closers BANNED:** "What's your take?" / "Agree?" / "Save this post" / "Bookmark this"

**Structures BANNED:**

- Negation parallelism — "It's not X, it's Y"
- Forced rule-of-three — "innovation, inspiration, insight"
- Balanced sentence pairs — "Talent gets you in. Discipline keeps you there."
- Unnamed framework promise — "Here's the 3-step framework" (OK if named after real client)

**Encoding BANNED:** em-dash (—), en-dash (–), curly quotes (" " '), unicode ellipsis (…). Use straight ASCII.

**Travel cliches BANNED:** paradise, island vibes, manifesting, sunset views, nomad lifestyle.

---

## EXECUTION FLOW (one session, ~6 min)

### PHASE 1 — Fetch + dedup feeds (30s)

```bash
cd "<repo>" && \
python scripts/fetch_feeds.py --date $(date +%Y-%m-%d) --top 30
```

20 RSS, 48h SQLite dedup, writes `outputs/<DATE>/today_items.json`.

### PHASE 2 — Pick today's angle (5s)

```bash
python scripts/pick_angle.py --date $(date +%Y-%m-%d)
```

Weekday → `angle.json` w/ 2 hook variants + top 5 candidates.

### PHASE 2.5 — Surface scroll-stopper hooks (MANDATORY, 3s)

Always show the user matched psychology hooks BEFORE writing copy. Pull from the 150-hook library, filled with today's topic noun.

```bash
python scripts/suggest_hooks.py --angle <angle_slug> --topic "<topic noun>" --n 8
```

- `<angle_slug>` = `angle.json::angle_slug`. The script maps angle → best psych categories via `config/scroll-hooks.json::_meta.angle_to_category`.
- `<topic noun>` = the concrete subject of today's post (the niche/service/pain, e.g. "editing video in the terminal", "AEO for clinics").
- Print the 8 hooks to the user. The LinkedIn hook + the video 0-4s beat MUST be built from one of these (paraphrase tightly to keep voice — never paste verbatim).
- Full library viewer for browsing/filtering: `HOOK-LIBRARY.html` (live topic-fill box + search + copy). Dump all 150 grouped: `python scripts/suggest_hooks.py --all --topic "<noun>"`.
- Hook rule: first line ONLY. Pay off the open loop within the next 2 lines or it trains distrust. ASCII only (no em-dash / curly quotes).

### PHASE 3 — Claude writes copy.json (~5 min, v0.4 FORKED schema)

Read: `angle.json`, `config/client-wins.json`, `config/local-anchors.json`, `config/banned-phrases.json`, `config/hook-bank.json` (read BOTH `rotation` for business AND `travel_rotation` for travel), `config/copy-schema.json`.

Pick **once per day**:

- 1 source from candidates (most agency-relevant) → business block only.
- 1 business hook variant from `hook-bank.rotation[<weekday>]` (or tight paraphrase).
- 1 travel hook variant from `hook-bank.travel_rotation[<weekday>]`.
- 1 client_win_slug (`shared.client_win_ref`).
- 1 local anchor (`shared.local_anchor`) — STYLED DIFFERENTLY in each track (business = punch / travel = drift).
- 1 vulnerability_beat (`shared.vulnerability_beat`) — used by business only.
- 1 story_anchor (`travel.fb_profile.story_anchor`) — used by travel only.

Write `outputs/<DATE>/copy.json` with the forked schema:

```json
{
  "date": "2026-05-19",
  "angle_slug": "prompt-exposure",
  "weekday": "tuesday",
  "source_url": "https://...",
  "source_title": "...",
  "hook_variant_chosen": 2,
  "shared": {
    "news_anchor": "...",
    "client_win_ref": "dental-flagship",
    "local_anchor": "Coffee at the corner cafe, a few bucks.",
    "vulnerability_beat": "I used to think AEO was schema + FAQ. Cost me 2 closes in Q1."
  },
  "business": {
    "linkedin": {"post": "<900-1200ch w/ 8-role spine>", "slides": [...8 slides...], "hashtags": [...5-8...], "comment_bait": [...3...]},
    "fb_page": {"cards": [...3...], "post": "<200-800ch>", "hashtags": [...3-5...]},
    "ig_pro": {"slides": [...8...], "caption": "...", "hashtags": [...5-8...], "reel_script": "30-45s"},
    "yt": {"thumb": {"headline":"...","sub":"..."}, "shorts_script": "45-60s", "title": "<=70ch", "desc": "..."},
    "tt_pro": {"cover": {"headline":"...","sub":"..."}, "script": "30-45s", "caption": "...", "hashtags": [...3-5...]}
  },
  "travel": {
    "angle_slug": "visa-life",
    "hook_variant_chosen": 1,
    "story_anchor": "Stood in the immigration line 90 min. Agent took 20 USD over WA.",
    "fb_profile": {"cards": [...3...], "post": "<150-700ch>", "story_anchor": "..."},
    "ig_travel_1": {"slides": [...5...], "caption": "...", "hashtags": [...5-8...], "reel_script": "15-30s"},
    "ig_travel_2": {"slides": [...5...], "caption": "...", "hashtags": [...5-8...]},
    "tt_travel_1": {"script": "...", "caption": "...", "hashtags": [...3-5...]},
    "tt_travel_2": {"script": "...", "caption": "...", "hashtags": [...3-5...]},
    "pinterest": {"pin": {"headline":"...","overlay":"...","size":"1000x1500"}, "desc": "...", "board": "Travel", "hashtags": [...8-12...]}
  }
}
```

Full schema spec: `config/copy-schema.json`.

### image_picks block — MUST use real filenames OR glob patterns (v0.4.1)

Authoring `image_picks` is the #1 cause of "PENDING_IMAGES" CSV rows. The hint **MUST** be one of:

1. **A literal stem present in the rotation pool** — verify before writing:

   ```bash
   python "<your-images>/_pick-next.py" --count 400 | grep -E "^DJI_|^SCENE-|^IMG_"
   ```

   Examples that resolve today: `IMG_4105`, `SCENE-2026-05-07-garden-variant`, `DJI_20260518_0023`.

2. **A glob pattern with `*` or `?`** — `build_pack_v2._resolve_image_hint` runs `fnmatch` against every candidate stem (case-insensitive). The FIRST match wins, which means the rotation-log order decides which actual file you get.
   - Travel scenes: `DJI_*`, `SCENE-2026-*-street-*`, `SCENE-2026-*-garden-*`.
   - Business portraits: `IMG_*`, `SCENE-*-rooftop-portrait-*`, `SCENE-*-veranda-*`.

3. **NEVER** invent filenames like `scene_street_01.jpg` or `scene_beach_low_tide` unless they actually exist on disk. They will not resolve, drop to fallback (whatever-track-appropriate is available), and you lose authorial control over which image pairs with which slide.

Pattern cheat-sheet lives in `config/hook-bank.json::image_picker_hints`. Add new globs there as new naming families enter the pool. NEVER edit `process_image.py` for this — the resolver is in `build_pack_v2.py`.

### PHASE 3.5 — Voice lint, BOTH tracks (3s, HARD GATE)

```bash
python scripts/lint_voice.py --date $(date +%Y-%m-%d) --voice both --strict
```

Business fails on ANY: banned phrase, encoding tell, hook>210 chars, hashtag count off, missing vulnerability beat, missing anchor, missing client_win_ref, wrong slide count/roles.

Travel fails on ANY: banned business term (aeo/agency/client/SkynetLabs/n8n/MRR/Loom/Fiverr/schema/citation), blocked travel hashtag, missing local-currency anchor, missing named place, missing story_anchor, business-CTA pattern ("DM me" / "I'll reply with"), encoding tell.

**If lint fails → fix copy.json + re-run BEFORE Phase 4.**

### PHASE 4 — Export TEXT-ONLY pack (5s) — DEFAULT since 2026-05-31

**Preferred: 3 variants per platform** (story / contrarian / confession-style angles for A/B). Author `outputs/<DATE>/variants.json` (see shape in `scripts/export_variants.py` header — `platforms[].variants[]` each = {style, angle, body, hashtags}), then:

```bash
python scripts/export_variants.py --date $(date +%Y-%m-%d)
```

Emits `VARIANTS.html` (bright theme, 3 labelled copy-boxes per platform + Copy button) + `VARIANTS.txt`. 11 platforms x 3 = 33 ready posts. Pick one variant per platform, attach own image, post.

Voice rules for variants (research-backed, 2026): open IN-SCENE (a moment, not a thesis) · uneven rhythm (short. fragment. one longer line) · KILL rule-of-three / "it's not X it's Y" / inflated words / em-dashes · end on a LOW-LOAD CTA that drives comments (binary "chase or wait?", "tell me I'm wrong", fill-in-blank, oddly-specific question) NOT "what's your take?" · LI 900-1500 chars, IG hook <125 chars, FB/TT short.

**Video = ONE shared, SHOOT-READY script, NOT per-platform.** `video_scripts.{business,travel}[]` each = {style, angle, shots:[{t, line, angle, delivery, broll}], caption, hashtags}. The `shots` array is a director's breakdown: each beat tells you the exact LINE to say, the CAMERA angle/framing, the DELIVERY cue, and the ON-SCREEN/B-roll text. Rotate camera angles across beats (front-on tight -> push-in/lean -> 3/4 angle -> back to front-on for CTA) so the video isn't static. One shoot -> post to YouTube Short + TikTok + IG Reel + FB Reel. Do NOT write separate YT/TikTok/IG/FB scripts.

- **business video scripts MUST be driven by the LATEST industry/service news** — pull a real, dated item from PHASE 1's `today_items.json` (AI agents / automation / AEO / the niches we sell), attribute the source claim (no fabricated stats), then tie it to a SMB service angle + comment CTA. One real news anchor per variant.
- travel video scripts stay personal lifestyle (local daily-life), NOT industry news.

**Single-copy fallback** (1 per platform, from `copy.json`):

```bash
python scripts/export_text.py --date $(date +%Y-%m-%d)
```

- Reads `copy.json`, emits `COPY.html` + `COPY.txt`.
- NO images, NO `_avatars`, NO picker, NO html2canvas. You select + push your own images.

> Image carousels are DEPRECATED (the old `build_pack_v2.py` render still works if ever needed, but the renderer had a silent blank-text bug; text export is the supported path). To resume rendered images: `python scripts/build_pack_v2.py --date <DATE>`.

### PHASE 5 — (optional) GHL CSV row (5s)

```bash
python scripts/append_ghl.py --date $(date +%Y-%m-%d) --slot 10:00
```

6-col canonical CSV → tomorrow 10:00 local time. `imageUrls` left blank; paste manually-chosen image URLs before import. Skip entirely if posting by hand.

### PHASE 6 — Tell the user what to do

Print:

```
OPEN: outputs/<DATE>/COPY.html

1. 📋 Each platform = a Copy button. Click → paste into the native composer.
2. 🖼  Pick + attach your own image(s) per post.
3. 📋 LinkedIn: fire the 3 comment-baits 1 per 15-20 min in first 60 min.
4. Done.
```

---

## TOOL-STACK WARNING (research-backed)

- **NEVER post via Taplio** — 30% reach penalty + 55% engagement penalty. LinkedIn algo flags AI-template patterns from Taplio.
- **Safe:** native LI scheduler, Buffer, GHL scheduler.
- **Analytics-only (zero algo risk):** AuthoredUp (hook preview), Shield Analytics (retro).
- **AVOID:** Hypefury for LI (it's Twitter-first, weaker LI signal).

---

## OUTPUT CONVENTION

```
outputs/YYYY-MM-DD/
├── today_items.json     # 30 deduped RSS items
├── angle.json           # angle + 2 hook variants + 5 candidates
├── copy.json            # Claude-written, voice-linted
├── index.html           # 8-slide carousel + post + reply pack
├── _avatars/            # 2 picked photos
├── _picked_images.json  # rotation audit
└── csv/ghl-linkedin.csv # tomorrow 10:00 local time
```

---

## RULES (REPRIORITIZED v0.2)

1. **Voice spine = locked** (reference POST 1 + POST 2). Don't flatten.
2. **Anchor required** — 1 real local detail per post.
3. **Client win required** — slug from `client-wins.json`. No invented stats.
4. **Vulnerability beat required** — dated, specific, uncomfortable.
5. **Hook ≤210 chars** — LI "See more" truncate point.
6. **Hashtags 5-8** — no more, no less.
7. **Comment-bait pack** — 3 pre-staged replies. Fire 1 per 15-20 min first hour.
8. **lint_voice.py --strict** must pass before render.
9. **Rotation log sacred** — always `--mark` photos.
10. **No Taplio.** Ever.

---

## ANTI-PATTERNS

- Don't paste hook from `hook_variants` verbatim — paraphrase tightly to keep voice unique.
- Don't reuse a client win slug 2 days in a row.
- Don't drop the `→` arrow glyph for `▸` `•` or em-dash — voice memory locked.
- Don't fill `vulnerability_beat` with generic "I used to think AI was overhyped" — needs date, person, currency, or specific fail.
- Don't omit the comment-bait pack — that's where 70% of reach lives.

---

## TROUBLESHOOTING

| Symptom              | Fix                                                                 |
| -------------------- | ------------------------------------------------------------------- |
| `feedparser` missing | `pip install -r requirements.txt`                                   |
| 0 items after dedup  | `rm cache/seen.sqlite`                                              |
| Image picker fails   | check `_USAGE_LOG.json` exists in <your-images>                     |
| html2canvas blank    | hard-refresh; check `_avatars/` populated                           |
| lint_voice.py FAILS  | read each FAIL line; fix copy.json; re-run                          |
| Hook too long        | use only first variant from `angle.json`, strip trailing clause     |
| Anchor missing       | inject 1 line from `local-anchors.json` into Slide 2 + LI post body |

---

## ROADMAP

- **v0.3** — wire `/reel-studio` mograph mode for daily 30s video off same angle.
- **v0.4** — auto-push PNGs to GitHub `carousels-png/<DATE>/` for ManyChat asset library.
- **v0.5** — Task Scheduler invocation: `claude -p /aeo-daily` daily 7am local time.
- **v0.6** — DONE (2026-06-08): engagement-loop live via `weight_hooks.py` + `hook-weights.json` overlay read by `suggest_hooks.py`.
- **v0.7** — auto-generate 2 hook variants via Claude inside Phase 3 (not pre-baked).
- **v0.8** — wire `build_master_html.py` auto-invoke into `build_pack_v2.py`; add `--voice` flag to `build_pack_v2.py` (still missing — renderer always emits all channels).
- **v0.9** — live-query the AEO Visibility Snapshot (auto-run ChatGPT/Perplexity/Gemini for the prospect instead of manual fill).

---

Last updated: 2026-06-08 (v0.6.0 — WEDGE "Get Cited" + FUNNEL (snapshot lead magnet, cta-bank, dm-flow) + 6 missing scripts built + lint v1.2.0 hardened across all channels + engagement hook-weighting loop live + client-wins refreshed)
