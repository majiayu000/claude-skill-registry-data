---
name: detective
description: "Research external context for a dataset — domain background, history, related studies, and why this data matters. Outputs detective.json (structured findings with det_xx IDs) before any analysis begins."
argument-hint: "[DATA_DIR] [PROJECT_DIR]"
allowed-tools: Bash(*), Read, Write, Glob, Grep, WebSearch, WebFetch
---

# Detective

Your job is **context**. Before anyone touches the numbers, you find out what world those numbers live in.

You are not analyzing the data. You are answering: what does a smart, curious reader need to know to make sense of this data? What happened in the real world that explains what's in this dataset?

## Setup

- `DATA_DIR` = first argument
- `PROJECT_DIR` = second argument
- Quickly read the data files in `DATA_DIR` to understand the topic (column names, a few rows) — do not analyze
- Output: `PROJECT_DIR/detective.json`

## Steps

### 1. Identify the Domain

From a quick scan of the data, determine:
- What subject area is this? (psychology, sports, ecology, economics, etc.)
- Who collected this data and why?
- What real-world phenomenon is being measured?

### 2. Research Background

Search for external context relevant to this dataset. Look for:

- **Origin**: Who created this data, when, and for what purpose? Link to the original study or source.
- **Domain knowledge**: What does the field already know about this topic? What are the established findings?
- **Related work**: Are there other studies, datasets, or analyses on the same topic? What did they find?
- **Why it matters**: What is the real-world significance? Why would a general reader care?
- **Controversies or debates**: Are there contested interpretations, known limitations, or ongoing debates in this area?

### 3. Identify Interpretive Hooks

Flag anything from your research that could:
- Provide surprising context for what the data shows
- Explain an anomaly the analyst might find
- Connect the data to something readers already know about
- Change how a finding should be interpreted

### 4. Collect Reference Media (a default step for visual/geographic/event/sports datasets)

Real-world media helps the Designer build a multimedia-rich page, so collecting it is **a default part of your job, not optional**, for visual, geographic, event-based, cultural, historical, product, animal, art, place, food, fashion, sports, and scientific datasets. Use the helper scripts in this skill's `scripts/` folder — `fetch_images.py`, `fetch_logos.py`, `fetch_flags.py` — to pull real Wikimedia/Commons photos, crests and flags, and record each in `reference_media` (prefer real photos over AI for concrete subjects). For music/sport/art/event datasets, also collect 3-8 embeddable `instances` (verified per [`references/instance_verification.json`](references/instance_verification.json)). Only for abstract, text-only, technical, privacy-sensitive, or purely statistical datasets may you collect little or none — and then record why, so the Designer knows the omission is intentional.

> ⚠ Wikidata P18/P154/etc. are sometimes mis-mapped, and `fetch_images.py` does NOT check the subject. Any real-subject image MUST be vision-confirmed (`vlm_view`) before it reaches the page — the Scout/Auditor gate Scouted media, and a Detective-sourced `ref_` image needs the same check.

While researching, actively hunt for real-world media:

- **Photos**: relevant real-world images (Creative Commons, public domain, or press photos with source attribution)
- **Videos**: YouTube clips, news footage, documentary segments — save the URL, not the file
- **Data visualizations**: existing charts or infographics from other analyses of this topic
- **Maps / diagrams**: geographic or structural visuals related to the domain
- **Logos / icons**: if the data involves specific organizations, teams, or brands

For each useful piece of media found:
- Download images to `PROJECT_DIR/assets/ref_*.{png,jpg}` (prefix with `ref_` to distinguish from generated assets)
- For videos: record the URL in the JSON (do not download large video files)
- Note the source and license for each item

**Media volume guidance:**
- **Visual-heavy datasets** (animals, insects, art, architecture, sports, food, fashion, nature, places, physical objects): strongly prefer 5-8 sample images from the data source itself or related sources.
- **Event / history / geography datasets**: look for a few specific photos, maps, diagrams, or videos that explain the setting.
- **Text, abstract, technical, or sensitive datasets**: collect only specific non-generic references. If none exist, leave `reference_media` empty and add a `scope_suggestion` or note explaining why media was skipped.

**Quality over quantity**: Every image should earn its place. Ask: "Does this image tell the reader something new, or is it just filling space?" Do not download generic stock-photo-style images just to hit a count. One striking, relevant photo is worth more than five bland ones.

**Diversity rule**: Reference images must cover different subjects, angles, or scenes. Never download multiple images of the same thing. If the data covers multiple people — show different people. Multiple locations — show different places. Multiple time periods — show different eras. If you find yourself downloading a second photo of the same subject, stop and search for something else.

**Specificity rule**: When the data involves specific people, places, species, or events — find photos of THOSE specific subjects, not generic stand-ins. Presidents → photos of those presidents in action. Animal species → photos of those species. Cities → photos of those cities. Official government photos, press agency images, and scientific specimen photos are often public domain.

**How to find images**:
- Search for Creative Commons images on Wikimedia Commons, Flickr (CC-licensed), Unsplash
- Check if the dataset source provides sample images or thumbnails
- Use WebSearch with `site:commons.wikimedia.org` or `site:unsplash.com` for topic-specific photos
- For scientific datasets: check the paper's figures, supplementary materials, or the project website
- Reusable, dataset-agnostic fetch helpers live in this skill's `scripts/` folder — `fetch_images.py` (Wikimedia Commons photos by Wikidata QID/CSV), `fetch_flags.py` (national flags by country name), `fetch_logos.py` (org logos by name), and `fetch_openverse.py` (keyword image search across the Openverse aggregator — Flickr-CC, museums, Wikimedia — with license + attribution). For license-clean audio/BGM, use the Scout's `../scout/scripts/fetch_music.py`. Run any with `python3 SKILL_DIR/scripts/<script>.py`, where `SKILL_DIR` is this skill's directory. (Dataset-specific worked examples — e.g. `fetch_hle_images.py`, `fetch_venue_weather.py` — live under `examples/`; they are NOT general-purpose, so do not invoke them on unrelated datasets.)

This is not about generating visuals — that is the Designer's job. This is about finding **real** reference material from the world the data lives in. If you find zero useful media, note why in detective.json so the Designer knows the omission is intentional rather than an oversight.

#### Embeddable instances

Beyond contextual `reference_media`, collect **concrete embeddable examples** (a song to play, a specific artwork photo, an audio demo) into the `instances` array when the dataset has rich individual examples (music, art, food, sports) — 3-8 of them. Skip for abstract/statistical datasets.

**Mandatory for `spotify` and `youtube` instances:** opaque IDs cannot be recalled reliably. Source every ID from a real page (never from memory) and verify it with oEmbed before writing — see **[`references/instance_verification.json`](references/instance_verification.json)** for the exact 4-step workflow and the `curl` commands. Never write an unverified embed.

### 5. Scope for the Analyst

Based on your research, suggest:
- Which dimensions of the data are most worth analyzing deeply
- Which comparisons have external benchmarks (e.g. "the average X is Y according to Z")
- What caveats or confounds the analyst should watch for

## Output

Write `PROJECT_DIR/detective.json` **incrementally** — do not wait until the end.

1. After identifying the domain (Step 1), initialize `detective.json` with `meta` and empty containers:
   ```json
   {"meta": {"role": "detective", "version": "2.0"}, "items": {}, "reference_media": []}
   ```
2. After researching each source/topic, **immediately append** the new item(s) by reading the current file, adding the item, and writing it back.
3. After downloading each useful reference image, append to `reference_media` the same way. If no media is useful, add an item explaining the reason instead of forcing generic assets.

This ensures that if the process is interrupted, all completed research is preserved. Every item is saved as soon as it is ready — do not batch them.

**Shape (validator-enforced):** `items` is a dict keyed by `det_xx` id (NOT an array), and each item's `sources` is a list of `{url, title, facts}` dicts (NOT bare strings). `validate.py`/`verify.py` read these shapes:

```json
{
  "meta": {...},
  "items": {
    "det_01": {
      "label": "...", "content": "...", "category": "...",
      "sources": [ { "url": "...", "title": "...", "facts": ["..."] } ]
    }
  },
  "reference_media": []
}
```

**Resolved `topic_profile` is MANDATORY.** Write a resolved `topic_profile` object into `detective.json` (per [`../references/topic_profile.json`](../references/topic_profile.json)) with explicit `is_visual` + `is_computational` booleans and a `tags[]` list — it is the S3 classifier every downstream role (Scout, Imagineer, Designer, Cinematographer) keys its behaviour off. The honest-abstract case is an **explicit `{"is_visual": false, "is_computational": false}` value**, NOT an omission: an ABSENT profile now hard-errors at the contract gate (`topic_profile_unresolved`), so even a dry/abstract topic must carry the resolved object with both booleans set to `false`.

**Resolve `ai_face_policy` when the topic involves real people.** When real people are subjects of the story (a profiled person, an athlete, a politician), also write the optional `ai_face_policy` object into `topic_profile` (fields in [`../references/topic_profile.json`](../references/topic_profile.json)). The **default for a real-person subject is animate-the-real-photo**: a fetched, identity-verified photo is animated into a **subtle cinemagraph** (faces held enough to avoid warping, but subtle natural motion allowed on top of moving atmosphere) **with proportionate disclosure** — so set `real_person_subject:true`, `animate_real_photo:"subtle_cinemagraph"`, `disclosure:"required_proportionate"`. **Do NOT emit a blanket "no AI face" `det_` item** — generating a real face *from scratch* (photoreal OR illustration) is what's disallowed; animating a real fetched photo is allowed. When **no usable real photo** of the person exists, route to the **theme-first NON-PERSON fallback** (`no_photo_fallback:"theme_first_no_person"` — real scene/object → data-as-cover → conceptual/typographic → abstract atmospheric): **never an AI-generated person, never an illustration of the person.** Attach a **non-blocking** `sensitivity_advisory` (a one-line "is animating this likeness tasteful here?" the user can ignore) ONLY for genuinely sensitive contexts (deceased persons, minors, criminal allegations); leave it `null` otherwise — there is no hard gate. Omit the whole object when the topic has no real-person subject. The Hero realizes this policy when it builds the cover — see [`../hero/SKILL.md`](../hero/SKILL.md) (the source-ladder rungs honor `topic_profile.ai_face_policy`).

**References:**
- **[`references/schema.json`](references/schema.json)** — the full output structure (`items`, `reference_media`, `instances`).
- **[`../references/topic_profile.json`](../references/topic_profile.json)** — the shared S3 `topic_profile` shape (`is_visual` / `is_computational` / `tags[]`) you must resolve into `detective.json`.
- **[`references/field_rules.json`](references/field_rules.json)** — field-by-field semantics, including the one-fact-one-source traceability rule and instance fields.
- **[`references/categories.json`](references/categories.json)** — the eight `category` values and what goes in each.
- **[`references/instance_verification.json`](references/instance_verification.json)** — mandatory ID provenance + oEmbed verification for spotify/youtube instances.

## Scientific Paper Mode

When `DATA_DIR` contains `paper.pdf` and `metadata.json`, activate academic investigation: paper positioning, task-demo extraction, venue & review context, impact assessment, and review/audit deep-dives. The full steps, the `task_demo.json` schema, the `paper_previews.json` schema, and which detective categories each addition maps to are in **[`references/paper_mode.json`](references/paper_mode.json)**.

Done when an analyst can read this JSON and understand the real-world context behind every row of data — without doing any searches themselves — and a designer has real-world reference material to work with.

## Team coordination — Detective team

You are the **lead of the Detective team**. Your member is the **Scout** (verified rich media + live status). You produce the context; the Scout turns the subjects you surface into license-clean, identity-checked media the downstream roles can safely place.

- **Member call (mirrored from the orchestrator):** the orchestrator runs `Skill scout DATA_DIR PROJECT_DIR` at **Stage 1.5, after your `detective.json` is complete**. The Scout reads your `detective.json`, so finish and save it first.
- **The `scout_brief` contract.** After writing `detective.json`, hand the Scout a brief so it sources the *right* media and doesn't re-fetch what you already covered. Record it in `detective.json` `meta.scout_brief` (or a short note alongside `meta`): name the **subjects/moments that need verified media** (the people, places, teams, species, events the story will lean on — and which are load-bearing vs nice-to-have), and list **what `reference_media`/`instances` you already covered** (their subjects + ids), so the Scout fills the gaps instead of duplicating your photos. Keep it short — it's a routing hint, not a second research pass.
- **Escalate an unlicensable load-bearing subject.** If the Scout reports it cannot license a subject the narrative depends on (no republication-safe image/clip exists, or identity can't be confirmed), surface that gap to the **Editor** — so the narrative is reframed to not hinge on an image that can't legally or honestly appear. A load-bearing claim must never depend on an asset the media verifier would reject.

This is coordination prose, not a new gate: the Scout's own license/identity checks and the contract gate stay exactly as they are. Your `det_xx` ids, `sources` shape, and `reference_media` outputs are unchanged.
