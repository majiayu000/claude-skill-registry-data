---
name: ads-video-library
description: >-
  Name, store and catalogue finished ad videos — canonical file names, a poster frame for every video (optionally baked in as frame 0 so feeds and chats show it as the thumbnail), contact sheets for QA, storage under Month / Language / Type in a local folder or a Google shared drive, a CSV catalogue (plus an optional Google Sheet), and a gallery.html review page with approve / reject / notes. Use after rendering any batch of ad creatives — motion cards, UGC, demos, cut-downs. Triggers: "upload the renders", "catalogue these videos", "name these files", "publish the creatives", "make a review page". Not for rendering.
---

# Ads video library

Where finished ad creatives live, what they are called, and how a team reviews and finds them again. Rendering is someone else's job; this skill starts the moment an mp4 exists.

One command does everything:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/publish.py manifest.json --catalog catalog.csv
```

1. **Names** every file canonically — the name says what the file is without opening it.
2. **Pulls a poster** — the strongest settled frame (text fully in, nothing mid-transition) → `<name>.jpg`.
3. **Makes a contact sheet** — six stills across the video → `<name>.sheet.jpg`, for QA.
4. **Stores** the video and poster under `<Month> / <LANG 🏳> / <Video type>` — in a local folder (default) or on a Google shared drive.
5. **Writes the catalogue** — `catalog.csv`, the source of truth, plus a Google Sheet tab if configured.
6. **Writes `dist/gallery.html`** — a review page: every video with its poster, fields and contact sheet, and approve / reject / note buttons. "Copy review" puts the verdicts on the clipboard to paste back here.

Run `--dry-run` first on any batch you haven't published before: it prints the names, the folders and the chosen poster times, and touches nothing.

Needs **FFmpeg** (`ffmpeg`, `ffprobe`) on PATH. Google Drive mode also needs `pip install google-auth requests`.

## The manifest

The generating agent writes it; it is the only file that knows anything about the batch:

```json
{
  "type": "motion",
  "label": "Motion Cards",
  "lang": "en",
  "extras": ["headline", "cta", "caption"],
  "items": [
    {"topic": "hr-interviews", "src": "renders/hr.mp4", "voice": "female",
     "headline": "An AI scheduler for recruiters", "cta": "Try for free",
     "caption": "Candidates pick an interview slot in their own time zone. No back-and-forth emails."}
  ]
}
```

`type` goes into the file name, `label` is the folder and the Sheet tab, `extras` are the columns this type carries beyond the core set. Per item `topic`, `src` and `voice` are required; `poster_at` (seconds) overrides the automatic poster pick. Full contract: `references/manifest.md`.

## Configuration

`library.json` in the working folder (or `~/.config/marketing-agent-kit/video-library.json`):

```json
{"storage": "local", "local_root": "~/Ads Video Library"}
```

For Google Drive: `{"storage": "gdrive", "drive_id": "<shared drive id>", "sheet_id": "<optional sheet id>"}` — setup in `references/setup.md`. Without a config file the skill uses local storage in `~/Ads Video Library`.

## Posters and frame 0

Read `references/posters.md`. In short:

- Almost every player and feed shows **frame 0** as the idle thumbnail, and frame 0 of an ad is usually a fade or a half-drawn title. `--bake-poster` replaces only frame 0's pixels with the poster: same duration, same frame count, audio untouched, invisible on playback — but every thumbnail grabber now shows a real frame.
- Platforms that accept a custom thumbnail upload (Meta, TikTok, YouTube, the LinkedIn post editor) get the `.jpg`.
- **Look at the posters and contact sheets before reporting.** Automatic picking is a good default, not a guarantee. If a poster lands on the wrong moment, set `poster_at` for that item and re-run.

## Review loop

1. Publish → open `dist/gallery.html` (or send it to the reviewer with the `dist/` folder).
2. The reviewer approves, rejects and leaves notes, then clicks **Copy review** and pastes the text into the chat.
3. Update each item's `status` (`approved` / `rejected`) and `notes` in the manifest, fix the rejected ones, re-run `publish.py`. The catalogue and the gallery update; links stay valid.

## Read before publishing a new video type

- `references/naming.md` — the name, field by field, and why the catalogue never joins on it
- `references/storage.md` — folder layout, what belongs in the library and what doesn't
- `references/manifest.md` — the manifest contract
- `references/setup.md` — Google credentials, and what to do when Google stops trusting them
- `references/posters.md` — posters, frame 0, contact sheets, captions

## What this skill won't decide for you

- **The type slug and label.** A new format is a new folder beside the existing ones. Keep the slug short, lowercase, no underscores — underscores separate fields in the name.
- **What belongs in `extras`.** A column is worth adding when someone choosing a creative to run would sort or filter on it: the headline, the CTA, the hook, the caption. Not the render settings.

## Things that cost time to learn

- **The catalogue joins on `id`, never on the file name.** `id` is `<type>_<topic>_<lang>_<aspect>_<voice>` and survives re-renders, new dates, new lengths and new versions; an EN and an ES cut, or a 16x9 and a 9x16 cut, are separate ids. Ad performance joined on a file name splits one creative's history in two.
- **Length and date are in the name, so a re-render renames the file.** The publisher retires what is in the type's folder and not in the batch — locally into `_retired/`, on Drive into the trash. Skip it with `--no-sweep` and the folder fills with older renders, all looking current.
- **`created` is remembered for an id already in the catalogue.** Always pass `--catalog`: without it the publisher has no memory and every run stamps today.
- **Two items with the same id or the same name is a refusal, not a warning.** Two render projects producing the same basename once shipped the wrong screen inside a card for a week.
- **One `catalog.csv` for the whole library.** A batch replaces its own rows and leaves other types and languages alone; columns you added (spend, CTR) are kept. Rows whose files the sweep just retired get `status` = `retired`.
- **A Sheet tab is overwritten wholesale.** The CSV is the source of truth; anything typed into the tab by hand is gone on the next run.
- **Drive: a service account can only write to a shared drive** (it has no storage of its own), and every call against a shared drive needs `supportsAllDrives`. Details in `references/setup.md`.

## Adapt it

- Add your languages to `"langs"` in `library.json` (`{"sv": "SV 🇸🇪"}`).
- Write a small manifest generator in your render project: it is the only project-specific part. Everything after it is this skill.

Poster selection and the frame-0 technique are adapted from [/brag](https://github.com/latent-spaces/brag) (MIT).
