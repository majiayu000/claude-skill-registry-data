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
- Reusable Wikimedia/Commons fetch helpers live in this skill's `scripts/` folder — `fetch_images.py`, `fetch_logos.py`, `fetch_flags.py`, `fetch_hle_images.py`, `fetch_venue_weather.py` (run with `python3 SKILL_DIR/scripts/<script>.py`, where `SKILL_DIR` is this skill's directory)

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

**References:**
- **[`references/schema.json`](references/schema.json)** — the full output structure (`items`, `reference_media`, `instances`).
- **[`references/field_rules.json`](references/field_rules.json)** — field-by-field semantics, including the one-fact-one-source traceability rule and instance fields.
- **[`references/categories.json`](references/categories.json)** — the eight `category` values and what goes in each.
- **[`references/instance_verification.json`](references/instance_verification.json)** — mandatory ID provenance + oEmbed verification for spotify/youtube instances.

## Scientific Paper Mode

When `DATA_DIR` contains `paper.pdf` and `metadata.json`, activate academic investigation: paper positioning, task-demo extraction, venue & review context, impact assessment, and review/audit deep-dives. The full steps, the `task_demo.json` schema, the `paper_previews.json` schema, and which detective categories each addition maps to are in **[`references/paper_mode.json`](references/paper_mode.json)**.

Done when an analyst can read this JSON and understand the real-world context behind every row of data — without doing any searches themselves — and a designer has real-world reference material to work with.
