---
name: kelly-mv
description: "Music-video production skill for turning an existing MP3 into a pure-visual (no-voiceover) music video through a bundled Busabase App-in-Skill UI. Use when the user wants to build an MV from a song they upload: write a one-line concept, keep a cast of characters with reference cards, and break the song into storyboard shots where each shot has a scene description and an image + video that can be either AI-generated (image-to-image from the character cards, draft video via local LTX) or uploaded by the user. Same character/storyboard management model as kelly-drama. Song generation (creating the song itself, incl. voice-cloned singing) is a documented future capability."
metadata:
  category: production
  tags:
    - risk:local-write
    - surface:busabase
    - surface:moonrouter
  busabase:
    template: true
    folderSlug: kelly-mv
    resources:
      - project
      - settings
      - cast
      - shots
    risk: local-write

---

# Kelly MV

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly MV concept view"></td>
    <td width="50%"><img src="assets/screenshots/storyboard.webp" alt="Kelly MV storyboard"></td>
  </tr>
  <tr>
    <td><strong>Concept</strong><br>MV concept workbench with project checklist, next-step guidance, concept form, and how-to walkthrough.</td>
    <td><strong>Storyboard</strong><br>Shot list with duration, image status, and a detail pane for description, image generation, and video upload.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/cast.webp" alt="Kelly MV cast"></td>
    <td width="50%"><img src="assets/screenshots/song.webp" alt="Kelly MV song"></td>
  </tr>
  <tr>
    <td><strong>Cast</strong><br>Character list with reference card status and a detail form for visual description, wardrobe, and consistency anchors.</td>
    <td><strong>Song</strong><br>MP3 upload and song metadata form with auto-detected duration and song-gen backend status.</td>
  </tr>
</table>

## Core Idea

Use this skill as a music-video creative workspace. The app is the human editing surface; the skill is the creative producer: it reasons, drafts, validates, exports, and fulfills the AI-generation requests the app can only queue. The app reads and writes a Busabase workspace — one Folder, four Bases (project/settings/cast/shots) — plus Busabase Drive Assets for every uploaded or generated MP3/image/video.

An MV here is **pure picture — no voiceover, no dialogue, no on-screen lyrics**. The job is simple: take an existing MP3 and give it visuals. The final video is the storyboard shots played in order over the song. (For voiced/dialogue drama, use `kelly-drama` instead — that is its job.)

The app has exactly four areas: **概括 (Concept)**, **Song**, **角色 (Cast)**, **分镜 (Storyboard)**. Keep it that simple — don't reintroduce song sections, timeline tiling, or large per-shot production sheets.

Default to the AirApp for ongoing creative work — give the user the clickable AirApp URL, or run `pnpm --dir content/kelly-mv-app dev` for a local preview. Use chat-only mode only when the user explicitly asks for "chat only", "no UI", "纯聊天", or similar.

## Default Flow

1. Open the AirApp (or `pnpm --dir content/kelly-mv-app dev` for local preview, which asks you to connect Busabase and select a Space — never an API key).
2. On first run the workspace is empty; provision it from the app's setup screen, then seed the bundled starter (a 静夜思 sample MV) with `node scripts/create_sample_project.mjs --apply`, or start from scratch.
3. Use the app, following the sidebar **下一步 (next step)**:
   - **概括 (Concept)**: one-line summary of what the MV is and its tonality, a one-line visual `look`, and aspect ratio. That's it.
   - **Song**: upload an MP3. Duration is read automatically. Optional title/artist. Nothing else.
   - **角色 (Cast)**: the people on screen. Stable id, role, three-view visual notes, wardrobe, anchors, forbidden drift, and a **character reference card** image. Generate reference cards before storyboard work when consistency matters. No voice profiles (pure-visual MV). Same model as kelly-drama.
   - **分镜 (Storyboard)**: an ordered list of shots. Each shot has a **画面描述 (scene description)**, on-screen characters, a duration, and an **image + a video**. Image and video can each be **AI-generated** (image-to-image from the character cards; draft video via local LTX) **or uploaded** by the user.
4. Clicking a "Generate" button in the app only writes a **request** onto the character/shot record (`reference_card_status` / `image_status` / `video_status` = `requested`) — the browser cannot hold the image-API key or spawn the local LTX process. After the user asks, fulfill pending requests with `node scripts/execute_generation_requests.mjs --apply` (dry run without `--apply`).
5. After edits, run `node scripts/validate_shot_readiness.mjs` (each shot has a title, description, and sane duration; warns on cast missing reference cards) before generating.
6. Export a readable concept + shotlist with `node scripts/export_story_bible.mjs` for handoff.

## Creative Operating Rules

- **Pure visual.** Never add dialogue audio, narration TTS, or burned-in subtitles/lyrics. The only audio is the song itself.
- **Keep it simple.** The shot is just a scene description + characters + duration + image + video. Do not add camera-spec sheets, song-section taxonomies, lyric timelines, or strict timeline-coverage rules.
- **Pace to the music.** Cut shot lengths to the song — quick moments run short (4–6s), establishing/hero/montage runs longer (8–12s). A single AI-generated shot must be 4, 5, 6, 8, 10, or 12 seconds and never exceed 12s. (Uploaded clips can be any length.)
- **Two ways to fill a shot.** Each shot's image and video can be **generated** or **uploaded** — both append as non-destructive candidates and the user picks the active one. Respect what the user wants; don't overwrite an uploaded asset by regenerating.
- **Character consistency via real image-to-image.** Storyboard image generation feeds the existing character reference-card images to the image `/images/edits` endpoint as actual input pixels, not just text. If a character lacks a generated reference card, that shot falls back to text-to-image and the likeness drifts — generate the card first.
- **Generate in dependency order**: song uploaded → concept written → cast reference cards → storyboard images → draft shot videos. The shot's `description` is the image prompt; an optional `negative_prompt` and `video_prompt` refine generation.
- **Photoreal MV look (when realism is the target):** request cinematic music-video stills, real lensing, filmic grain; forbid on-screen lyrics/captions/watermarks/UI, readable fake text, plastic skin, and malformed hands.

## Song Generation (future capability)

Selecting/importing an existing song is the supported path today. Creating the song itself — including singing in the user's **cloned voice** — is wired as a documented stub: `scripts/generate_song_draft.mjs` spawns `scripts/gen_song.py`, mirroring the local-draft / cloud-prod split used for video. `gen_song.py` stays Python deliberately (the local backends worth recommending are Python-ecosystem ML models with no Node equivalent); `generate_song_draft.mjs` is the trusted wrapper that uploads whatever it produces to Busabase.

Recommended local backends (Apple Silicon, no cloud):

- **SongGeneration v2 (Tencent)** — native MLX weights `mlx-community/SongGeneration-v2-large`. Best fit for "本地 MLX 最好"; same family path as the local TTS/audio stack. **Primary recommendation.**
- **ACE-Step 1.5** — strongest local model, runs on Mac, <4GB, full vocals + instruments, supports **audio-prompt timbre cloning** and lyric editing → the path for "用我 clone 的声音创歌" (pass a reference clip as the timbre prompt).
- **YuE** / **DiffRhythm** — full-length song-from-lyrics alternates; heavier.

Caveat: cloning a *singing* voice needs a singing reference clip; a spoken sample clones timbre but not vocal performance well. To enable generation, install a backend into a local venv, implement the inference call in `scripts/gen_song.py`, then run `scripts/generate_song_draft.mjs --apply`.

## Busabase Resources

One Folder (`kelly-mv`), four Bases, declared in `content/kelly-mv-app/app/js/config.js` and
the generated template sidecars under `content/`:

- `project`: single-row MV project meta — song title/artist/asset-id/duration/source and the concept (`treatment_summary`/`treatment_look`/`treatment_aspect_ratio`).
- `settings`: one row (`record-id: "config"`) with the image-generation backend (base URL/model/size — the API key itself is an env var, never stored) and the song/video generation backend names.
- `cast`: on-screen characters — visual notes, wardrobe, anchors/forbidden-drift (JSON arrays), and the reference-card's status/prompt/asset id.
- `shots`: ordered storyboard shots (`position` field carries the order) — description/negative-prompt/video-prompt/duration/on-screen characters (JSON array of cast ids), and the image/video asset id + status + JSON-encoded candidate list.

Binary media (uploaded MP3, character reference images, shot images/videos)
are **Busabase Drive Assets**, not Base fields — uploaded from the browser
via `busabase-sdk`'s real `assets` client (`createUploadUrl` → PUT bytes →
`confirm`), with only the returned asset id stored on the owning record. See
`references/ui-schema.md` for the full field <-> asset mapping and a known
limitation of the standalone OSS CLI's asset-upload route.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space. A soft-delete `deleted` text field
(`"true"`/`"false"`) backs the app's Delete buttons on `cast`/`shots` — there
is no destructive record delete in the write surface.

## When To Read References

- Read `references/mv-workflow.md` when designing or improving an MV concept, cast library, shot breakdown, or image/video prompt workflow.
- Read `references/ui-schema.md` when editing the app, generating/validating project data, or working with the Busabase field shapes or Drive Assets.

## Useful Commands

```bash
pnpm --dir skills/kelly-mv/content/kelly-mv-app dev
node skills/kelly-mv/scripts/create_sample_project.mjs --apply
node skills/kelly-mv/scripts/validate_shot_readiness.mjs
node skills/kelly-mv/scripts/export_story_bible.mjs
node skills/kelly-mv/scripts/execute_generation_requests.mjs --apply
node skills/kelly-mv/scripts/generate_song_draft.mjs --apply
```

Run `validate_shot_readiness.mjs` (optionally `--strict`) before an image/video generation pass. Every trusted script here connects with its own credentials (`BUSABASE_BASE_URL` / `BUSABASE_API_KEY` / `BUSABASE_SPACE_ID`), never the AirApp's ambient session, and defaults to a dry run wherever it writes or generates.

## Execution reports

Re-read the active Busabase workspace immediately before fulfilling any pending generation request. `scripts/execute_generation_requests.mjs` records each concrete operation, target, status, and error directly on the owning `cast`/`shots` record (`*_status` = `generated`/`blocked`) — there is no separate execution-report file.
