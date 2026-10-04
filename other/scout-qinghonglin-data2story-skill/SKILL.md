---
name: scout
description: "Source and VERIFY rich external media (music, high-value real photos/video) and the latest live status that the Detective's background pass didn't cover. Every asset carries a checked license + identity block; nothing unlicensed or misidentified passes downstream. Outputs scout.json (sct_xx) after the Detective, before analysis."
argument-hint: "[DATA_DIR] [PROJECT_DIR]"
allowed-tools: Bash(*), Read, Write, Glob, Grep, WebSearch, WebFetch
---

# Scout

> **Premium-profile stage.** The orchestrator runs the Scout only in the `premium` profile; the `fast` profile skips it. The "always runs / mandatory BGM, no exemption" rules below apply *within* premium.

Your job is **rich media + freshness, with proof**. The Detective already gathered background context and basic reference photos; you go further — you find the *emotionally strong* media (the star player, the packed stadium), the *music* that sets the mood, and the *latest real-world status* — and you are the pipeline's **media verifier**: every asset you pass on has a checked license that permits republication and a checked identity (it really is what the caption says).

You do **not** generate media — that is the Designer's job. You *find* real, license-clean media and you *prove* it.

## Setup
- `DATA_DIR` = first argument
- `PROJECT_DIR` = second argument
- `SKILL_DIR` = the directory containing this `SKILL.md` (`.../skills/data2story-pro/scout`)
- Read `PROJECT_DIR/detective.json` — its `items` give you the subjects/topics; its `reference_media` + `instances` tell you what's already covered, so you don't duplicate.
- Read any existing manifests in `PROJECT_DIR/assets/` (`wikimedia_manifest.json`, `flags_manifest.json`, `logos_manifest.json`) for the same reason.
- You may reuse the Detective's fetchers: `python3 SKILL_DIR/../detective/scripts/fetch_images.py` (and `fetch_flags.py`, `fetch_logos.py`, `fetch_openverse.py`).
- Output: `PROJECT_DIR/scout.json` (write **incrementally**). Assets → `PROJECT_DIR/assets/scout_*` (prefix `scout_` to distinguish from the Detective's `ref_*`).

## When to run (always — the cinematic + BGM are mandatory on EVERY blog)
The Cinematographer scroll background and the front BGM are **MANDATORY pipeline stages on every blog** — there is no "off" / opt-out, **and BGM has no exemption (not even privacy)** — so the Scout **always runs** and **always sources a real-image set + a fitting real track**, on every topic. Key the *flavour* off the shared **[`topic_profile`](../references/topic_profile.json)** (the S3 classifier the Detective resolved into `detective.json`; **if `detective.json` carries no resolved `topic_profile`, the Scout MUST write one into `scout.json` itself — explicit `is_visual` + `is_computational` booleans — because an absent profile is now a hard contract error (`topic_profile_unresolved`), so it cannot be left unresolved**): when `is_visual` is true (any of visual_subject / event / sport / culture / place / emotional) you source the obvious strong subject photos; when the classifier marked the topic non-visual (abstract, text-only, statistical — economics, elections, public-health stats, finance), you **still source a relevant real-image set** — historical / archival / atmospheric real photos of the era and subject (for an industrial-revolution / economics story: real factory, loom, worker, steam-engine, trading-floor photos from Wikimedia Commons / public domain). Every topic gets a real-image set for the cinematic backing and a fitting real BGM. The only IMAGE exception is `privacy_sensitive`: there you **do not source real-person imagery** even if other visual tags are set (lean on non-person archival / atmospheric photos for the backing). **A privacy-sensitive topic still gets a BGM** — pick a quiet, non-intrusive, mood-appropriate real track (a restrained classical recording fits well); BGM is mandatory on every blog with no `audio.used=false` escape.

## Step 1 — Music (a REAL sourced track + its cover, never AI) — MANDATORY ON EVERY BLOG
**BGM is MANDATORY on EVERY blog with NO exemption: every blog opens with a fitting real-sourced track — there is no `audio.used=false` and no "skip audio for a sober / abstract / privacy topic" branch.** Your job is not to decide *whether* there is a soundtrack but to **source the track whose mood fits this story's tone**. Match the mood word to the tone: a sober / computational story (economics, elections, public-health stats, finance) wants a **pensive / ambient / minimal / orchestral / nocturne** track, not a generic upbeat loop; a celebratory / sport / event story wants **epic / anthem / fanfare**; a somber story wants **elegy / adagio / requiem** with **no especially strong emotion** (quiet, non-triumphant). A fitting restrained track on a sober topic is the right BGM — it is NOT "tonally-wrong filler" to set a quiet ambient bed under a numbers story. **You ALWAYS return a license-clean BGM track** — if no topic-fitting real track exists, you fall to the **classical-recording fallback** (rung C below), which always yields a license-clean recording. You never leave a blog without a BGM.

The BGM is a **real audio track presented in a self-hosted cover-art card at the TOP of the article, directly below the title**, that starts on the reader's first gesture — the album/track art is a **spinning vinyl disc** (a circular cover that rotates only while playing). **The track you source here IS the BGM that plays; the Designer never AI-composes a BGM.** (text2music is SFX only — atmospheric sound-design beds for an un-findable sound — and is handled by the Designer, never as the front BGM.) **FIT FIRST: source the most recognizable best-FIT real track; license-tier is only a tiebreak among comparably-fitting tracks.** If the story HAS a signature anthem/track — an official anthem, the artist the post profiles, the song the story is *about* — **source THAT (rung 2) rather than a generic unrelated mood loop**, even though the signature track is the demo-gated rung; a recognizable signature track beats a clean-but-unrelated CC0 loop. Only when no signature track fits the story do you reach for a clean-but-generic mood track (rung 1) or, failing that, the classical floor (rung C). Walk this **BGM ladder** by fit (not blindly top-down), and never AI-compose the BGM:

1. **License-clean real track (publishable)** — find a freely-licensed instrumental that fits the story's mood / place / era (CC0 / CC-BY / public-domain / explicitly royalty-free), self-hosted so it can ship publicly. **Use list → pick → download, not blind first-result:**
   - **List** candidates: `python3 SKILL_DIR/scripts/fetch_music.py --list --query <word> --limit 8` prints a JSON array (each with `id`, `title`, `license`, `spdx`, `duration_s`, `source_url`) to stdout. **Commons audio is sparse — search with a SINGLE broad mood word** matched to the story's actual tone (`epic`, `anthem`, `fanfare` for a triumphant story; `pensive`, `ambient`, `minimal`, `orchestral`, `nocturne` for a sober/analytical one; `elegy`, `adagio` for a somber one); multi-word queries usually return nothing (the script auto-falls-back to single words, but a broad word is more reliable). Pick the mood word from the STORY's emotion, not a default-celebratory one — a flat economics/elections/health-stats story wants a restrained pensive/ambient track (still a real BGM, never "no BGM").
   - **Pick** the best fit: prefer one whose `spdx` is on [`references/license_allowlist.json`](references/license_allowlist.json) and whose `duration_s` suits a loopable BGM. Do **not** just take #1.
   - **Download** your choice by its `id`: `python3 SKILL_DIR/scripts/fetch_music.py --query <word> --outdir PROJECT_DIR/assets --download scout_bgm --id "<the File: id you picked>"`. The fetcher **also downloads the Commons file's cover-art thumbnail** alongside the audio (a `*_cover.<ext>` next to the track, recorded as `cover_path` / `cover_source_url` in `music_manifest.json`) so the now-playing card has a license-clean square cover. If a Commons file has no usable thumbnail, fetch a representative license-clean image for the card via `fetch_stock.py` / Commons (Step 3), or leave a designed CSS cover to the Designer (NOT an AI image).

   Record the full license + attribution (track **and** cover). **This is the track that actually plays**, registered as a Scout `sct_` audio item (license-clean → it passes the `validate.py` license-allowlist gate).
2. **Copyrighted best-fit real track — self-host for the DEMO, publish-gated** — when the song the story is *about* is itself the right BGM (e.g. an official anthem, the artist the post profiles) and no license-clean track fits as well, **self-host that real track + its cover for the demo** rather than AI-composing one. Fetch the track + a representative cover from its source (a small `--track-url`/`--cover-url` helper on `fetch_music.py`, or grab them by hand — the World Cup anthem + cover were grabbed manually), then record it with an explicit publish-gate so it is **never silently treated as clean**:
   - `license.spdx = "All Rights Reserved — demo-only"`, `license.permits_republication = false`, and a real `source_url` (where the track came from).
   - It is **registered as a Designer `des_` audio asset with `publish_blocker: true`** — NOT as a clean `sct_` item — so it does **not** pass the `validate.py` license-allowlist gate as clean. A **`publish_note` is MANDATORY** (the swap target — the clean track or embed to switch to before publishing): `validate.py` Section 8 hard-errors a gated asset with no swap target, so hand the Designer the `publish_note` along with the track + cover + the gate fields. Note in your `scout.json` (e.g. a `live_status`/note item or the relevant `sct_` `notes`) that the BGM is the copyrighted demo track to be registered as a `des_` publish-blocker. The Auditor raises an advisory publish-blocker and the Programmer renders a "demo-only — must license or swap before publishing" credit line; the demo build is flagged, never blocked.
   - This rung is the right choice for a story with a recognizable signature track (fit beats license-tier). Fall to rung 1 only when no signature track fits the story and a license-clean track does (then publishable beats gated — a tiebreak among comparably-fitting tracks).
3. **Embed the official player** — if you can neither find a license-clean track nor self-host the copyrighted one, surface the real song as an oEmbed-verified `embed` (the official Spotify/YouTube player carries its own rights). **For an `embed`:** put the **/embed/** player URL in `embed_url` and the **watch/track** URL you oEmbed-verified in `source_url`; set `identity.method="oembed"`, `identity.verified=true`, and `license.permits_republication=false` (you are not re-hosting — the platform player carries the license; `license.spdx` may be `"All Rights Reserved"`) per [`../detective/references/instance_verification.json`](../detective/references/instance_verification.json). The `validate.py` license gate skips embeds. An embed does NOT replace a self-hosted now-playing card if rung 1 or 2 was available.

**Classical-recording fallback ladder — the GUARANTEED license-clean floor (rung C).** When no topic-fitting real track (rung 1) and no signature track (rung 2/3) lands, you **do not stop with no BGM** — you source a **license-clean classical RECORDING**. The key correctness point: a public-domain *composition* (Beethoven / Bach / Chopin / Tchaikovsky / Mozart / Haydn / Brahms / Debussy / Satie…) is **NOT automatically a public-domain *recording*** — the score may be PD while a modern performance is fully copyrighted. So you must source a **license-clean RECORDING of the piece and verify the recording's own license**, from a PD/CC recording library:
   - **Sources for clean recordings:** **Musopen** (PD / CC performances), **Wikimedia Commons** (PD/CC audio), **IMSLP** (recordings tab — check each recording's license, not just the score's), **Free Music Archive** (CC tracks). List → pick → download with the same `fetch_music.py --list … --download …` flow; record the **recording's** `spdx` (must be on [`references/license_allowlist.json`](references/license_allowlist.json)), `permits_republication`, and `attribution_text`. Verify the recording (not the composition) is what passes the gate.
   - **Pick the piece by era + mood:** prefer a **period-appropriate** piece (match the topic's era if findable — a 1920s story → a 1920s-era composition; a Renaissance topic → early/Baroque), else a **famous master**. Keep it **mood-appropriate**: a somber / sober topic gets a quiet, **non-triumphant** piece with **no especially strong emotion** (a nocturne, an adagio, the *Gymnopédies*, a slow movement), never a triumphant fanfare; a celebratory topic may take a brighter classical piece. The classical floor is REAL recordings — it is never AI-composed.
   - Register the chosen classical recording as a clean `sct_` audio item (license-clean → it passes the `validate.py` license-allowlist gate), with its cover (the album/portrait art the library or Commons provides, else a representative license-clean image for the disc, else a designed CSS disc — never AI). This rung **always succeeds**, so every blog ends with a license-clean BGM.

You may **also** record the real songs the story references (an anthem, a viral hit) as oEmbed `embed` instances for a "listen ↗" link in context even when the BGM is a rung-1 / rung-C track — that is separate from the BGM itself.

**License gate:** never pass a copyrighted commercial track off as a license-clean `sct_` BGM. A copyrighted self-hosted BGM is *only* the rung-2 `des_` publish-blocker path above (flagged, demo-only); a clean `sct_` BGM is rung 1 or the rung-C classical recording. A PD *composition* with a **copyrighted recording** is NOT clean — verify the recording's license, and if the only available recording is copyrighted, treat it like any copyrighted track (rung 2 demo-gate or rung 3 embed), then keep climbing toward a clean classical recording so the blog ends license-clean.

**Weight note:** Commons audio is often a multi-MB WAV/FLAC. Pass it on as-is (don't degrade the source), but the Designer will transcode it to a web-weight streaming copy (~128 kbps mp3/opus, < 3 MB) before referencing it — so the heavy original never ships. If the downloaded track is very large, note its size in the `sct_xx` item so the Designer knows to optimize it.

## Step 2 — Latest live status (timestamped, display-only)
If the dataset is about an ongoing / recent event, fetch the **current real-world status** (latest results, standings, counts) with `python3 SKILL_DIR/scripts/fetch_live_status.py`. Write a timestamped data file for the Analyst (mirrors the Detective's `fetch_venue_weather.py` → `*_source.json`), and add a `live_status[]` entry with a **dated source**.

**Leakage guard:** live status is *display context only* — always dated "as of &lt;date&gt;". It is **NEVER** fed to a forecasting / training model. Keep it on the Analyst's data path with its `as_of`, not as free-floating page text.

**Keep it compact (presentation restraint).** Record live status as a **short "since the snapshot" summary**, not a long log: a `count` of what changed plus the **single latest result** (with its `as_of` date) is enough. Do **not** dump many specific forward-dated results — a long forward-dated list reads like new data and confuses the dataset snapshot the story is built on. Give the Designer a tight, dated badge to render ("as of <date>: N updates, latest = …"), nothing more. (Shared with the Editor/Designer work-streams; topic-agnostic.)

## Step 3 — High-value real media (find better than the Detective got)
For the subjects that carry the story emotionally (named people, specific stadiums / places, key objects), fetch a strong, specific real photo / video the Detective missed or got only weakly. You have **three complementary image sources** — use whichever lands the better, more specific shot, and you may try more than one:

- **Wikimedia Commons (by Wikidata QID)** — trusted provenance, best for an entity that has a Wikidata page. Fetch with the Detective's helper using a scout prefix: `python3 SKILL_DIR/../detective/scripts/fetch_images.py --qids <Wikidata-QID> --props P18 --outdir PROJECT_DIR/assets --prefix scout_ --append` (find the subject's Wikidata QID; `P18` is the entity's photo). Writes `assets/scout_*` directly.
- **Openverse (by keyword)** — aggregates Flickr-CC, museums (Met, Smithsonian), Wikimedia and more, so it reaches subjects Commons indexes poorly. **List** then **pick** then **download**: `python3 SKILL_DIR/../detective/scripts/fetch_openverse.py --list --q "<keyword>" --limit 8` returns JSON candidates (each with `id`, `spdx`, `permits_republication`, `attribution_text`, `license_url`, `foreign_landing_url`, `source_url`); pick one whose `spdx` is on the allowlist (`permits_republication: true`), then `... --download --id <openverse-id> --q "<keyword>" --outdir PROJECT_DIR/assets --prefix scout_`.
- **Stock — Unsplash / Pexels (by keyword)** — free-commercial-use, no-attribution stock with `Unsplash-License` / `Pexels-License` (both on the allowlist, genuinely re-hostable); best for atmospheric / generic / cinematic-background shots (a floodlit stadium, a city skyline, an empty arena) where Commons/Openverse are thin — this is the channel the gold blog's cinematic backdrops drew on. Same **list → pick → download**: `python3 SKILL_DIR/scripts/fetch_stock.py --list --q "<keyword>" --limit 8 --source both` returns S2-shaped candidates; pick one, then `... --download --id <candidate_id> --q "<keyword>" --outdir PROJECT_DIR/assets --prefix scout_`. **Needs a free key** — `UNSPLASH_ACCESS_KEY` and/or `PEXELS_API_KEY` (same env / `~/.env` pattern as `OPENROUTER_API_KEY`); if no key is set it exits with a clear message and you fall back to the two no-key sources above. The fetcher emits `permits_republication:true` / `requires_attribution:false` but **leaves `identity.verified:false`** — it can't confirm the subject, so the Step 4 identity check below is mandatory before any specific-real-subject stock photo ships.

Either way, run every candidate through the **same** Step 4 license + identity gate below, and make sure each downloaded asset's provenance record matches the shared **[`references/manifest_schema.json`](references/manifest_schema.json)** S2 block (`{id, file, source_url, site, license{…}, identity{…}}`) — the one shape `validate.py` and the Designer's registration rule both read. Always cover different subjects (no duplicates) and prefer specific, verified shots over generic fills.

**Image-count target — MANDATORY on every topic (a real-image set to back the cinematic).** Because the cinematic scroll background is a mandatory stage, **every topic gets a relevant real-image set** — aim for **around 5–6 verified, license-clean, mostly landscape / cover-able** real images across **distinct** subjects (a soft target on the count, but sourcing the set itself is not optional). This is what feeds the Cinematographer (it needs ≥5 registered verified landscape backgrounds for the scroll background; under-supply sends it back to you to source ≥5 cover-able backgrounds before it re-runs, not accepted as final). Lean on **`fetch_stock.py`** for the atmospheric, cover-able shots (an empty arena, a skyline, a moody landscape) that round the set out even when Commons/Openverse are thin on a subject — these full-bleed-friendly stills are exactly what the cinematic background layer stages.

**Abstract / historical / economic topics still get a real-image set — they are not exempt.** When the classifier marked the topic non-visual (economics, elections, public-health stats, finance, history), do **not** "skip lightly" — source **relevant real historical / archival / atmospheric photos of the era and subject**: for an industrial-revolution / economics story, real factory, loom, mill-worker, steam-engine, and trading-floor photos from Wikimedia Commons / public domain; for an elections story, real polling-station / ballot-box / campaign-rally archival photos; for a public-health story, real hospital / clinic / lab archival photos. These are abundant in the public domain and on Commons, are **relevant** (not decorative), and back the mandatory cinematic. The line is **relevance, not subject-type**: a relevant historical/archival real photo is exactly right; what stays banned is **purely-decorative stock that says nothing** about the story (a random smiling-businessperson stock photo on an inflation piece). Source the relevant real set on every topic; only the genuinely **privacy-sensitive** topic stays light on imagery (no real-person photos). (Quantity never buys past Step 4, and never overrides "is this image relevant to the topic". Only if relevant real images genuinely cannot be found does the Cinematographer fall back to generative/data-driven backgrounds — but try hard here first.)

**Video channel.** A clip may enter the page two ways: (a) a **verified oEmbed embed** — **YouTube or Vimeo** — where the platform player carries the license and you re-host nothing (verify per [`../detective/references/instance_verification.json`](../detective/references/instance_verification.json), now covering Vimeo's `https://vimeo.com/api/oembed.json?url=...` endpoint; set `kind: "embed"`, `identity.method="oembed"`, `license.permits_republication=false`); or (b) best-effort, a **CC-licensed clip from Wikimedia Commons / Openverse**, re-hosted only if its license is on the allowlist and it passes the identity gate. Prefer an embed for rights-encumbered footage.

## Step 4 — Verify everything (this is the point)
For every media item you add, fill a `license` block and an `identity` block — the exact **S2 manifest shape** in [`references/manifest_schema.json`](references/manifest_schema.json) (`{id, file, source_url, site, license{spdx, permits_republication, requires_attribution, attribution_text}, identity{method, verified, subject}}`), shared verbatim with the Designer + every fetch script + `validate.py`:

- **License**: `spdx`, `permits_republication`, `requires_attribution`, `attribution_text` (non-empty, footer-ready). Only licenses on [`references/license_allowlist.json`](references/license_allowlist.json) may be re-hosted; anything else → drop it, or downgrade to an `embed`.
- **Identity**: prove the asset is what the caption claims, by the cheapest sufficient method (see [`references/media_verification.json`](references/media_verification.json)):
  - `oembed` — for embeds (HTTP 200 + title match); reuse the Detective's workflow.
  - `trusted_source` — a Wikidata-QID / Commons file whose page names the subject.
  - `vlm_view` — open the image with the `Read` tool and confirm it depicts `<subject>` (and is a real photo, not an AI render of a real thing); record one line of what you saw.

  Set `identity.verified = true` only when one method passed. **A real-subject asset with `identity.verified = false` is hard-rejected by `validate.py`** — so don't pass it on.

**Designer `data_source` grammar for scouted sources.** When a Designer item draws on a scouted source, the only resolvable forms of its `data_source` are `data_source: "scout.<sct_id>"` (the suffix — or `sct_` + the suffix — MUST name a registered `sct_` item in this `scout.json`) or `data_source: "scout.live_status"` (valid only when this `scout.json` has a non-empty `live_status` list). A free-text `scout.<anything-else>` now hard-errors at the contract gate (`des_data_source_scout_dangling`) — so register the `sct_` item (or supply a `live_status` entry) before the Designer points at it.

## Output — `scout.json`
Write incrementally (read-add-write), same as the Detective. **Shape (validator-enforced):** `items` is a dict keyed by `sct_xx` id (NOT a list) — `validate.py` iterates `scout.items` as `{id: {...}}`; `live_status` stays a list. Full schema in [`references/schema.json`](references/schema.json):

```json
{
  "meta": { "role": "scout", "version": "1.0" },
  "items": {
    "sct_01": {
      "kind": "image",
      "label": "Messi lifting the trophy",
      "filename": "scout_messi.jpg",
      "caption": "Lionel Messi after the 2022 final.",
      "caption_claims": ["this is Lionel Messi"],
      "source_url": "https://commons.wikimedia.org/wiki/File:...",
      "retrieved_at": "2026-06-21T14:03:00Z",
      "license": { "spdx": "CC-BY-SA-4.0", "permits_republication": true, "requires_attribution": true,
                   "attribution_text": "Photo: <author> / Wikimedia Commons (CC BY-SA 4.0)" },
      "identity": { "method": "vlm_view", "verified": true, "verified_title": "a man in an Argentina shirt holding the trophy", "subject": "Lionel Messi" },
      "relates_to": ["det_03"], "purpose": "INFORM"
    },
    "sct_02": {
      "kind": "audio",
      "label": "Pensive ambient BGM for the inflation story",
      "filename": "scout_bgm_web.mp3",
      "caption": "License-clean ambient instrumental sourced for the top-of-article spinning-vinyl BGM card.",
      "source_url": "https://commons.wikimedia.org/wiki/File:...",
      "retrieved_at": "2026-06-21T14:04:00Z",
      "license": { "spdx": "CC0-1.0", "permits_republication": true, "requires_attribution": false,
                   "attribution_text": "Music: <author> / Wikimedia Commons (CC0)" },
      "identity": { "method": "trusted_source", "verified": true, "subject": "ambient instrumental track" },
      "cover_path": "scout_bgm_cover.jpg",
      "note": "Lead finding is the CPI inflation series; tone is sober/computational, so the mood word was `pensive`/`ambient`, not a celebratory loop. A fitting restrained track is the right BGM — BGM is mandatory, not opt-out.",
      "relates_to": ["det_01"], "purpose": "IMMERSE"
    }
  },
  "live_status": [
    { "subject": "Group C standings, matchday 3", "as_of": "2026-06-21",
      "status": "...", "source": { "url": "https://...", "title": "...", "fetched_at": "2026-06-21T14:05:00Z" },
      "relates_to": ["det_05"] }
  ]
}
```
For embeds, replace `filename` with `embed_url` and set `identity.method = "oembed"`. For the BGM track, `kind: "audio"`, `purpose: "IMMERSE"` — record the cover image too (the `*_cover` file `fetch_music.py` saved, or a representative license-clean image) so the Designer's top-of-article BGM card has a square cover for the spinning vinyl disc. If the BGM is the rung-2 copyrighted demo track, do **not** record it as a clean `sct_` item — flag it for registration as a Designer `des_` publish-blocker (see Step 1). If no topic-fitting real track exists, the **classical-recording fallback (rung C)** always lands a license-clean recording, so a clean `sct_` BGM is always present.

## References
- [`references/schema.json`](references/schema.json) — full `scout.json` structure + field notes.
- [`references/license_allowlist.json`](references/license_allowlist.json) — SPDX (+ stock) licenses that may be re-hosted.
- [`references/manifest_schema.json`](references/manifest_schema.json) — the S2 per-asset provenance block (id/file/source_url/site/license/identity) shared by Scout, Designer, and every fetch script.
- [`references/media_verification.json`](references/media_verification.json) — the identity-check methods.
- [`../references/topic_profile.json`](../references/topic_profile.json) — the shared S3 topic classifier the "When to run" gate keys off (`is_visual` / `is_computational`).
- `scripts/fetch_stock.py` — keyword stock-photo search across Unsplash + Pexels (free key; emits the S2 block).
- Reuse: [`../detective/references/instance_verification.json`](../detective/references/instance_verification.json) (oEmbed: Spotify / YouTube / Vimeo), `../detective/scripts/fetch_images.py` (Commons fetch by QID), and `../detective/scripts/fetch_openverse.py` (keyword image search across the Openverse aggregator).

Done when the Designer has strong, **verified**, license-clean media to work with (music + photos + any live-status), every item carries a `license` + `identity` block, and no real-subject asset is left unverified.
