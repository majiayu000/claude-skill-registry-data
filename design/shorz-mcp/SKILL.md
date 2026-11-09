---
name: shorz-mcp
version: 1.0.0
description: Control Shorz via MCP to create and edit projects, configure panels, import assets, generate videos and thumbnails, build and run Canvas node graphs, publish to YouTube or TikTok, and run headless single-file video/image edits (no project required).
---

# Shorz MCP Server Agent Skill

Before any Shorz MCP tool call, confirm **Shorz is running** and the **MCP server is connected**. For panel-level or project-type-specific work, **load the matching reference file** from `references/` (paths in the tables below) before changing settings or triggering renders.

This skill is the entry point (`SKILL.md`). Detailed workflows live under `references/panel-workflows/` (cross-project panels), `references/project-workflows/` (per-`projectType` end-to-end flows), `references/headless-workflows/` (**project-independent** file operations), and `references/creative-strategy/` (viral formats, hooks, and content brainstorming). The routing tables tell you which file to open.

## Operating Model

- Treat Shorz as a stateful desktop runtime. Always read current state before writes.
- Most menu/panel option changes map to `read_project_settings` + `update_project_settings` (targeted deep-merge patches).
- Generation and long-running workflows are asynchronous. For **project video creation**, poll **`get_video_generation_status`** as the default way to know running vs done vs error. Use **`fetch_app_events`** only if the user asks for live logs/progress, or when you are **diagnosing** a failed or stuck render (see **Event stream**).
- Prefer deterministic/headless arguments (override paths) over dialog-driven behavior.
- **Live UI vs MCP write races** — when the Shorz Electron app has the target project open, certain fields (notably `UI_SETTINGS.user_input_instructions` / PromptBar) can be reactively rewritten by the renderer shortly after an MCP write, because the input box owns its own in-memory state. If a configure-only patch on PromptBar appears to "revert," it is the live UI overwriting disk. Workarounds: write again after a moment, ask the user to close the project, or accept the renderer's value as the new truth. This is not a tool failure — the `set_user_instructions` write itself succeeded.

## Workflow routing

Pick the matching workflow file before editing a project or panel. Don't improvise — the per-file skills lock in tool names, enums, persistence keys, and known clamps/rejects.

### Guided creation (wizard) — vague idea, no concrete inputs

When the user expresses **intent to make a video or asset without the concrete inputs** it needs (no file path/URL, no format, no counts, no script — e.g. "i want to clip a youtube video", "make me an avatar video", "I need a thumbnail", "an animated intro"), do **NOT** improvise questions and do **NOT** start configuring. Open **`references/guided-creation/README.md`** first (trigger rules, question protocol, the 11 design rules, summary + confirmation contract), then run the matching flow:

| Intent sounds like | Guided flow file |
|---|---|
| clip/cut a long video into shorts | `references/guided-creation/clipping.md` |
| edit my own footage/photos into one video | `references/guided-creation/auto-edit.md` |
| make a video about X / from a script / faceless | `references/guided-creation/text-to-video.md` |
| talking head / AI presenter | `references/guided-creation/avatar.md` |
| two-person dialogue / AI podcast | `references/guided-creation/podcast.md` |
| ad / promo for my product | `references/guided-creation/advertisement.md` |
| music video for my song / visualize this track | `references/guided-creation/music-video.md` |
| thumbnail / cover image | `references/guided-creation/thumbnail-creator.md` |
| animated intro, logo reveal, kinetic text, title card | `references/guided-creation/animation-studio.md` |

Each flow asks a short option-driven sequence (interactive question tool when available; ≤4 preset options, recommended default first, custom input always possible, never re-asking anything already given), ends with a readable summary + an explicit confirmation, and only then executes via the matching `references/project-workflows/*.md` or panel workflow. If the user already gave a complete spec, skip the wizard and confirm the gaps in one question.

**Widget steps:** inside every guided flow, the image-slot, model and voice steps are rendered as inline card widgets via the client's `show_widget` tool when it exists (it is usually deferred — `ToolSearch` for it before assuming it is missing). Rules and templates: `references/guided-creation/widgets.md`. On those steps never open the native file picker yourself; the widget's button does.

### Project workflows (one per `projectType`)

| `projectType` | Workflow file | Primary MCP tools |
|---|---|---|
| `auto-edit` | `references/project-workflows/auto-edit.md` | Panel `set_*_settings` (subtitle, title, border, audio, overlay, broll, general video) + `switch_project_aspect_ratio` |
| `auto-edit` / `text-to-video` — **edit an already rendered video** | `references/project-workflows/edit-generated-video.md` | `edit_generated_video` (one plain-text instruction → new version; everything else pinned) |
| `text-to-video` | `references/project-workflows/text-to-video.md` | `set_text_to_video_settings`, `save_text_to_video_speech_audio`, `save_text_to_video_reference_images` |
| `avatar` | `references/project-workflows/avatar.md` | `set_avatar_settings`, `select_avatar_image`, `select_avatar_angle_image`, `select_avatar_audio`, `save_avatar_image`, `save_avatar_audio` |
| `podcast` | `references/project-workflows/podcast.md` | `set_podcast_settings`, `select_podcast_avatar_image`, `list_elevenlabs_voices` |
| `advertisement` | `references/project-workflows/advertisement.md` | `set_advertisement_settings`, `select_advertisement_image`, `remove_advertisement_image` |
| `music-video` | `references/project-workflows/music-video.md` | `select_music_video_audio`, `set_music_video_settings`, `remove_music_video_audio`, `select_music_video_character_image`, `remove_music_video_character_image` |
| `clipping` | `references/project-workflows/clipping.md` | `update_project_settings` (`CLIPING`, `ASSET_PATHS`), `download_social_video`, `switch_project_aspect_ratio` |

### Headless workflows (no project, no `projectType`)

These MCP tools work on **local files only**. They do **not** use projects, `settings.json`, PromptBar, Create Video, or any `projectType`. Do **not** call `create_project` or `read_project_settings` before using them.

| Workflow | File | Primary MCP tools |
|---|---|---|
| Single-file deterministic edits | `references/headless-workflows/single-asset-edit.md` | `trim_video`, `remove_ranges`, `crop_media`, `change_video_speed`, `remove_audio`, `set_audio_volume`, `rotate_media`, `flip_media`, `reverse_video`, `loop_video`, `fade_video`, `freeze_frame`, `set_image_duration`, `audio_fade`, `remove_silence`, `edit_image_with_ai`, `get_media_info`, `resize_media`, `fit_to_aspect`, `extract_audio`, `replace_audio`, `concat_media`, `extract_video_frames` |
| Pexels stock media search | `references/headless-workflows/pexels-stock-media.md` | `pexels_search_photos`, `pexels_search_videos`, `pexels_curated_photos`, `pexels_popular_videos`, `pexels_get_photo`, `pexels_get_video` |
| GIPHY GIF + sticker search and download | `references/headless-workflows/giphy-gifs-stickers.md` | `giphy_search_gifs`, `giphy_search_stickers`, `giphy_trending_gifs`, `giphy_trending_stickers`, `giphy_get_gif`, `download_giphy_gif` (free, signed in; stickers composite as transparent cut-outs, GIFs as opaque clips) |
| Public-domain audio search (SFX + music) | `references/headless-workflows/openverse-audio.md` | `openverse_search_sound_effects`, `openverse_search_music` (`length`: `tracks` \| `loops`), `download_openverse_audio` (**no Shorz credits and no sign-in**; every result is CC0, so the user owes no attribution) |
| X (Twitter) live search | `references/headless-workflows/x-search.md` | `x_search` (natural-language X search with citations; **spends Shorz credits**) |

See **`references/headless-workflows/README.md`** for when to use headless edits vs a full project workflow. To put an edited file into a project afterward, that is a **separate** import step (`import_frontend_assets`, `save_file_as`, or project-specific path patches).

### Companion skills

| Skill | Use it for |
|---|---|
| **`shorz-ui-automation`** | Driving the app through its **actual UI** with a real, visible cursor — tutorial footage, feature demos, screenshots for the website or docs, onboarding walkthroughs. It owns the `get_ui_map` → `ui_click` → `get_ui_map` loop and the six UI tools (`get_ui_map`, `scroll_ui_element_into_view`, `ui_click`, `ui_type`, `ui_press_keys`, `ui_scroll`), which are **not** covered anywhere else in this skill. Load it whenever the deliverable is a *visual of the UI*. For changing a setting or rendering **without filming it**, stay here — the tools in this skill are faster and need no UI. |
| **`shorz-motion-graphics`** | Generating a green-screen motion graphics overlay and chroma-keying it onto an existing video, any length, in `16:9` / `9:16` / `1:1`. Covers every style — explainer graphics, infographics and data callouts, kinetic typography, broadcast lower-thirds, annotation arrows, chapter cards, and high-energy short-form. Load it instead of improvising from the Animation Studio panel workflow whenever the goal is graphics **on top of existing footage** — it carries the source-analysis, safe-zone, segmentation, chroma-key and compositing rules that panel reference does not. |

### Creative and strategy workflows

| Strategy area | Workflow file | Primary purpose |
|---|---|---|
| Content brainstorming & viral playbooks | `references/creative-strategy/content-brainstorming.md` | Designing high-retention hooks, formats, and CTAs mapped to Shorz tools |

Open **`references/creative-strategy/content-brainstorming.md`** when the user asks for content ideas, viral formats, organic growth playbooks, or hook/CTA variants — then switch to the matching **`references/project-workflows/*.md`** (or headless workflow) to execute.

### Panel workflows (cross-project; usable on matching sidebar panels)

| Sidebar panel | Workflow file | Primary MCP tool |
|---|---|---|
| General Video / Auto Zoom | `references/panel-workflows/settings.md` | `set_general_video_settings` |
| B-roll (Assets / Web / GIF / AI / Emoji) | `references/panel-workflows/broll.md` | `set_broll_settings` |
| Audio (mix, dubbing, reverb, visualization) | `references/panel-workflows/audio.md` | `set_audio_settings` + `set_audio_visualization_settings` |
| Overlay | `references/panel-workflows/overlay.md` | `set_overlay_settings` + `get_overlay_effects` lifecycle |
| Border | `references/panel-workflows/border.md` | `set_border_settings` |
| Text → captions / subtitles | `references/panel-workflows/subtitle.md` | `set_subtitle_settings` |
| Text → headline / banner | `references/panel-workflows/title.md` | `set_title_settings` |
| Thumbnail Creator (modal) | `references/panel-workflows/thumbnail-creator.md` | `open_thumbnail_creator`, `set_thumbnail_creator_settings`, `thumbnail_creator_generate`, `get_thumbnail_creator_generation_status` |
| Animation Studio (modal) | `references/panel-workflows/animation-studio.md` | `animation_studio_*`, `compile_remotion_preview`, `remotion_render` |
| Canvas (node-graph video builder, ⋮ → Canvas; no project) | `references/panel-workflows/canvas.md` | `canvas_list`, `canvas_get`, `canvas_build`, `canvas_remove`, `canvas_run` (+ `get_job_status`), `canvas_stop`, `canvas_pick_take`, `canvas_duplicate`, `canvas_rename`, `canvas_delete` |
| Your Library (VIDEO / BROLL / SOUND / MUSIC) | `references/panel-workflows/your-library-assets.md` | `update_project_settings` (`ASSET_PATHS`); `delete_asset` only when deleting files on disk |

The **Text** sidebar shows subtitles and titles together but uses **two** tools with **two** key families (`subtitle*` vs `title*`). Never send subtitle keys to `set_title_settings` or vice versa — for both kinds, call each tool once with a minimal patch.

### Main VIDEO import (“Import Main Assets”) vs project type

In the Electron app, **`import_frontend_assets`** with `assetType: "video"` mirrors the UI **Import Main Assets** lane (fills the main timeline / `assets.VIDEOS`, which persists to **`ASSET_PATHS.main_video_asset_paths`** on save alongside other library categories). The single source of truth is **`isMainAssetsLaneEnabled`** (`frontend/src/utils/mediaAssetUtils.ts`): the main VIDEOS lane is **disabled** for **`podcast`**, **`avatar`**, **`advertisement`**, **`music-video`**, and for **`text-to-video`** unless **`textToVideoSourceMedia === "imported"`**. That rule gates the UI (import button, Your Library → VIDEOS tab, timeline strip) **and is enforced main-process-side**: a headless `import_frontend_assets` call with `overridePaths` and `assetType: "video"` into a lane-disabled open project is **rejected with an error** (redirecting to `"broll"`) instead of persisting `main_video_asset_paths`. Match this in guidance: never tell users they can “add main timeline videos” in templates that hide or disable main-video import.

| `projectType` | Main VIDEO import in UI (timeline / PromptBar gateway) | Your Library shows VIDEOS tab |
|---|---|---|
| `auto-edit` | Yes | Yes |
| `clipping` | Yes (typically one long source patched to **`ASSET_PATHS.main_video_asset_paths`**) | Yes |
| `text-to-video` | **Only when** Source Media is **`imported`** | **Only then** |
| `avatar` | **No** (`canImportMainAssets` false) | **No** |
| `podcast` | **No** (`canImportMainAssets` false) | **No** |
| `advertisement` | **No** (main lane disabled) — **workflow is reference stills**, not a main VIDEO lane — use **`select_advertisement_image`** / **`import_frontend_assets`** with **`image`** | **No** (tab hidden) |
| `music-video` | **No** — the input is the song (**`select_music_video_audio`**); the MUSIC lane is off too, and a headless `"music"` import is **rejected with an error** | **No** (VIDEOS and MUSIC tabs hidden) |

**Agents:** Use **`avatar`**, **`podcast`**, **`advertisement`**, **`music-video`**, **`text-to-video`** (unless `imported`) workflows for their **typed** inputs (still images, avatars, product/person images, script/audio, generated sources). `import_frontend_assets` with **`video`** into these projects is **rejected with an error** (headless `overridePaths` path) — import supporting footage as **`broll`**, which every project type keeps.

### One asset per file name (every library lane)

A lane (VIDEO / BROLL / SOUND / MUSIC) holds **at most one asset per file name** — compared case-insensitively, folder ignored, and **per lane** (the same file may legitimately sit in both VIDEO and BROLL) — because the backend addresses assets by basename: PromptBar `@mentions`, the Python render maps, and music/SFX name lookups. The **UI and MCP enforce the same rule**: `import_frontend_assets` **skips** a file whose name the lane already holds and lists it in **`skipped`** (reason `duplicate-name`), and an `update_project_settings` patch of a lane collapses repeated names and reports **`duplicateAssetNamesDropped`**. Nothing errors and nothing is overwritten — so **always check `skippedCount` before telling the user an import is done**, especially after a paid generation. Need both files? Rename one. Full contract and result shapes: **`references/panel-workflows/your-library-assets.md`** → *One asset per file name*.

### PromptBar semantics by project type

The PromptBar (`set_user_instructions` → `UI_SETTINGS.user_input_instructions`) does **not** mean the same thing for every project type. Source: `frontend/src/data/projects.ts` (`projectTypePromptPlaceholderMap`).

| Type | PromptBar role | Spoken/script content lives in |
|---|---|---|
| `auto-edit` | Primary creative brief (required for Create Video). Can also direct per-clip editing with no panel toggle: transitions between clips, camera motion, speed/volume/reverse/loop/flip/rotate, fill-the-frame framing, beat-synced cuts to imported music, and the imported-music bus itself (MUSIC lane holds any number of tracks, played back to back — the brief can reorder tracks, trim each one, and place/fade/mix the music) — full vocabulary in `references/project-workflows/auto-edit.md` → *What the PromptBar can direct* | n/a |
| `text-to-video` | Optional **look and mood** guidance | `textToVideoScript` (or saved speech audio in `audio` input mode) |
| `avatar` | Optional guidance for **enabled auto-edit features** (captions, B-roll, music, etc.) — **not the spoken script**. Can also arrange imported music (order, sections, placement, volume, fades, mix) | `avatarScript` (script mode) or `avatarAudioUrl` (audio mode) |
| `podcast` | Optional B-roll / music / SFX guidance — **not the dialogue**. Can also arrange imported music (order, sections, placement, volume, fades, mix) | `podcastScript` with `[Interviewer]` / `[Interviewee]` line tags |
| `advertisement` | Ad creative brief | Product/person images via `set_advertisement_settings` |
| `clipping` | **Optional** — only when steering topics, clip length, platform, or hooks | Source video at `ASSET_PATHS.main_video_asset_paths` |
| `music-video` | The creative brief — concept, look, who appears, how each section should feel (**never the lyrics**) | The song, set with `select_music_video_audio` (`MUSIC_VIDEO.music_video_audio_path`); the lyrics are transcribed from it at render time |

**Rule:** Never overwrite PromptBar with a script for `avatar`, `podcast`, or `text-to-video`, or with lyrics for `music-video`. Put the spoken text in the panel field listed above.

**Referencing a specific asset:** to point the brief at one file in the project library, write its **filename in double quotes** — `use "intro.mp4" as the opener`. That is exactly what the desktop app's `@` picker and its drag-from-timeline shortcut insert, and the app renders any such reference as a pill. Get the real filenames from `read_project_settings` (`ASSET_PATHS`) or `get_video_assets` / `get_audio_assets` first — a name that isn't in the library is just prose to the analyzers.

**Output framing (all project types):** PromptBar / `set_user_instructions` text is **never** the place for export geometry. Do **not** include aspect-ratio tokens (`9:16`, `16:9`, `1:1`), pixel dimensions (`1080×1920`, `1920×1080`, `1280×720`), `video_width` / `video_height`, or output **fps** in the creative brief — the project already has **`VIDEO_SIZE`** from the UI or **`switch_project_aspect_ratio`**. Platform or delivery names for creative intent (`TikTok`, `Reels`, `Shorts`, “vertical short”) are fine; technical sizing belongs in the aspect tool, not PromptBar. When the user asks for a format change, call **`switch_project_aspect_ratio`** and strip sizing lines from any PromptBar text you persist.

### PromptBar main AI model

The PromptBar **model dropdown** (all project types) selects which AIML chat model Create Video and backend LLM calls use. It is **not** the same as panel-specific models (`textToVideoImageModel`, thumbnail `imageGenerator`, etc.).

| MCP tool | Persistence | Allowed values |
|---|---|---|
| `set_main_ai_model` | `AI_MODEL.main_ai_model_name` | Server-driven — call **`list_main_ai_models`** for the live lineup and pass an id from its response. At time of writing: `anthropic/claude-opus-5-5` (Opus 5.5, default), `anthropic/claude-fable-5-1` (Fable 5.1), `anthropic/claude-sonnet-5-5` (Sonnet 5.5 — replaced Sonnet 5 on 2026-09-28 by migration `0054`, whose old id still resolves to it; 1 / 2 credits per 1k, the cheapest Claude), `openai/gpt-6-1-sol` (GPT 6.1 Sol — 1 / 2 credits per 1k; replaced GPT 6 Sol on 2026-09-30 at the same price, and `openai/gpt-6-sol` plus both old GPT 5.6 ids now silently serve 6.1 Sol), `openai/gpt-6-luna` (GPT 6 Luna, added 2026-09-23 — ~0.01 / 0.07 credits per 1k, the cheapest paid row), `openai/gpt-6-astra` (GPT 6 Astra, OpenAI's flagship, added 2026-09-05 — 2 / 7 credits per 1k, the priciest row; the proxy serves every GPT 6 model over OpenAI's Responses API, which is what lets Astra call function tools at all), `google/gemini-3.8-flash` (Gemini 3.8 Flash, ~0.2 / 1 credits per 1k tokens — much cheaper than Opus 5.5; a normal paid-selectable model billed like any other, **and** the only id a free run zero-rates) — seven models; treat that as a snapshot, not an allowlist. This model also drives image / video-frame asset analysis, including key-subject localization. **On a free-tier run** (`auto-edit` / `clipping`, zero-balance user) only `google/gemini-3.8-flash` is zero-rated — the in-app picker locks itself to it, but the MCP path does not, so **you** must `set_main_ai_model` (or pass `mainAiModelName`) with that id or the render bills and 402s |

- **Read current model:** `read_project_settings` → `AI_MODEL.main_ai_model_name`.
- **Before Create Video:** When the user names Opus, Fable, GPT 6.1 Sol, GPT 6 Luna, GPT 6 Astra, Gemini 3.8 Flash, or a specific model id, call **`set_main_ai_model`** before **`trigger_create_video`** / **`generate_video`**, or pass **`mainAiModelName`** on **`trigger_create_video`** for a one-shot run (persists to disk first, matching the UI dropdown at generate time).
- **Live UI:** Patches go through `update-project-settings`; the open app reloads the dropdown from disk (unlike PromptBar text, the model selector rarely races with in-memory UI state).

### Animation Studio chat model

The Animation Studio modal has its **own** model picker (labels like `claude-opus-5`). It does **not** read `AI_MODEL.main_ai_model_name`.

| MCP | Role |
|---|---|
| `animation_studio_list_models` | Supported chat **`model`** ids for this build |
| `animation_studio_send_*` optional **`model`** | Per-call override; default **`anthropic/claude-opus-5-5`** |

**Allowed ids:** server-driven — `animation_studio_list_models` returns the live lineup (same `main_ai` catalog category as the PromptBar picker; at time of writing seven: Opus 5.5, Fable 5.1, Sonnet 5.5, GPT 6.1 Sol, GPT 6 Luna, GPT 6 Astra, Gemini 3.8 Flash). Call it and pass an id from the response rather than one from this page. **`anthropic/claude-opus-4-6`**, **`anthropic/claude-opus-4-7`** and **`anthropic/claude-opus-4-8`** are retired from the selector — use **`anthropic/claude-opus-5-5`** instead. (**`anthropic/claude-sonnet-5-5`** is the Sonnet in the selector since `0054` on 2026-09-28; `anthropic/claude-sonnet-5` still resolves to it through a disabled legacy-alias row.) (The proxy still resolves `anthropic/claude-opus-4-8` via a disabled legacy-alias catalog row so older saved projects keep working, but do not pass it for new work.) Full workflow: **`references/panel-workflows/animation-studio.md`** → *Model selection*.

### Project targeting rules (apply to every **project** workflow)

**Skip this section for headless single-asset edit tools** (`trim_video`, `crop_media`, etc.) — they only need `inputPath` and Shorz running. See **`references/headless-workflows/single-asset-edit.md`**.

1. If the user names a project, resolve it with `list_projects` and use it. If not found, follow rule 5.
2. If the user says "current / open / this project", use `get_current_open_project`.
3. If the user gives no project identity, prefer `get_current_open_project`; otherwise ask whether to use existing or create new. **Never auto-pick** when multiple candidates match.
4. If the requested workflow conflicts with the current `projectType`, **do not silently repurpose** — ask whether to continue in the current project or create/select a matching type.
5. Create a new project only when the user explicitly asks, when a named target is missing and they approve creation, or when they ask for clean separation.
6. Never run destructive project actions (`delete_project`) without explicit confirmation. Same for `delete_asset`, `delete_overlay_effect`, `remove_animation_studio_export`, `clear_animation_studio_exports`.

### Asset verification: project main media vs My Assets library

Two different things — agents mix them up. Pick the right one.

- **Project main / timeline media** (the path(s) synced from the main VIDEO lane — **only workflows that expose main VIDEO import**, see **Main VIDEO import** above — e.g. `auto-edit` montage clips, clipping’s long source, `text-to-video` with **`imported`** source media): read `read_project_settings` → `ASSET_PATHS.main_video_asset_paths`, verify with **`file_exists`**. **`avatar`** / **`podcast`** templates do **not** use this lane in the shipped UI — do not treat `main_video_asset_paths` as required for Create Video there. **`advertisement`** center on **`ADVERTISEMENT.*` image paths**, not timeline video. **`music-video`** has no main lane: its input is the song at **`MUSIC_VIDEO.music_video_audio_path`** — verify that path with **`file_exists`**, not `main_video_asset_paths`. There is **no** MCP tool that lists "the project's VIDEOS tab"; for clipping do not verify the source via `get_video_assets`.
- **My Assets library tabs** (cross-project inventory; AI-generated outputs, imports, downloads): use the per-tab `get_*_assets` tools or filtered **`query_my_assets`** as described in `references/panel-workflows/README.md` → *Library and cross-cutting MCP tools*.

### Removing imported project assets (Your Library)

When the user asks to **remove**, **clear**, or **delete** something from the project **Your Library** lanes (**VIDEO**, **BROLL**, **SOUND**, **MUSIC**), they usually mean **drop it from the project**, not erase the file from disk. Full tab mapping and steps: **`references/panel-workflows/your-library-assets.md`**.

| UI tab | `ASSET_PATHS` field | Clear entire lane |
|---|---|---|
| VIDEO (Import Main Assets) | `main_video_asset_paths` | `update_project_settings` → `{ ASSET_PATHS: { main_video_asset_paths: "" } }` |
| BROLL | `broll_video_asset_paths` | `… { broll_video_asset_paths: "" }` |
| SOUND (sound effects) | `audio_fx_asset_paths` | `… { audio_fx_asset_paths: "" }` |
| MUSIC | `music_asset_paths` | `… { music_asset_paths: "" }` |

- **Default tool:** **`update_project_settings`** on the matching field. Paths are **comma-separated**; to remove one file, read settings, split/filter/rejoin, then patch. **Do not** use `delete_asset` unless the user explicitly wants the **file deleted from disk** (destructive; confirm first).
- **UI parity:** In-app trash on a library card only updates project paths (same as clearing via MCP); it does not unlink the source file.
- **Not the same as:** `get_*_assets` / My Assets modal inventory (use `delete_asset` there only when user wants the library file gone). Playback outputs (`last_generated_final_video_for_playback_mode`, `playback_history_video_paths`) stay until changed separately.
- **VIDEO tab availability** depends on `projectType` — see *Main VIDEO import* above before clearing main video on `avatar` / `podcast` / etc.

## Required Workflow Rules

0. **Pre-flight: the app's requirements guard does NOT protect you**
   - Since 2026-08-19 the desktop UI blocks **Create Video** and names what is missing when a
     project cannot possibly render. That check lives in the PromptBar's submit handler
     (`frontend/src/utils/generationRequirements.ts`) — **`trigger_create_video` and
     `generate_video` bypass it entirely.** Over MCP you get the old behaviour: the render starts,
     burns time, and fails (or silently returns the user's own file). Verify these yourself before
     triggering a render:

     | Project type | Must be true before you trigger |
     |---|---|
     | `auto-edit` | ≥1 file in the main VIDEOS lane **and** PromptBar instructions **> 10 chars** (below that the auto-editor is skipped and the source is re-exported untouched) |
     | `clipping` | **exactly one** video in the main lane — zero or two+ both fail |
     | `avatar` | avatar image set **and** (script **> 10 chars** **or** saved audio). Either input alone is enough; the mode toggle does not invalidate the other |
     | `podcast` | script **> 10 chars** in `[Interviewer]`/`[Interviewee]` form **and BOTH** avatar images set |
     | `text-to-video` | script **≥ 50 chars** **or** saved speech audio; plus ≥1 imported main asset when `textToVideoSourceMedia` is `imported` |
     | `advertisement` | **at least one** of product image / character image (either alone is fine) |
     | `music-video` | a song set (`MUSIC_VIDEO.music_video_audio_path` non-empty) **and** that file exists (`file_exists`) — without it the render stops (`music_video_no_song`) |

   - These mirror the renderer's own guards, so treat them as hard preconditions rather than
     advice. Re-read a setting after writing it when the render depends on it (`read_project_settings`).

1. **Project targeting first**
   - Prefer `get_current_open_project` first (active UI project source of truth).
   - If no active project is set, call `list_projects` and ask user to choose existing vs approve creating new.
   - Use absolute paths from `get_projects_path` and returned project metadata.

2. **Safe setting edits**
   - Call `read_project_settings` when you need the full picture or before non-trivial decisions.
   - Persist nested changes with `update_project_settings`: pass only the `updates` object for keys/sections to change (objects merge recursively; scalars and arrays replace). Optional `unsetPaths` deletes keys by dot notation. The main process reads the file, merges, validates, and writes atomically—**do not** reintroduce a manual read→edit full blob→write loop for ordinary edits.
   - For `set_*_settings` tools, MCP now performs strict validation:
     - unknown keys are rejected
     - invalid enum/color values are rejected
     - numeric values are range-validated; out-of-bounds values are **rejected or clamped per tool** (for example `set_border_settings` **clamps** `borderWidth` to 1–100 and `borderAnimationDuration` to 1–5)

3. **Asynchronous operations**
   - **Video generation (`generate_video` / Create Video)** — Poll **`get_video_generation_status`** until `lastStatus` is terminal (`completed`, `completed_no_output`, `error`, `stopped`, etc.). That is the main tool for project renders.
   - **`fetch_app_events`** — Use **sparingly**: when the user **explicitly** wants the raw event/log stream, or when **`get_video_generation_status` is unclear** (stuck, unexpected state) and you need the IPC log lines to see what the UI would have seen. Not the default loop for “wait for video.”
   - **Social video downloads (`download_social_video`)** — async by default; poll **`get_social_video_download_status`** until `lastStatus` is `completed` or `error`. YouTube extraction alone regularly takes minutes, so the blocking `awaitCompletion: true` form is only safe for short clips.
   - **Social publishing (`social_publish`)** — async by default; the tool starts the job and returns immediately. Poll **`get_social_publish_status`** until `lastStatus` is terminal (`completed` | `error`); its `result` carries the same per-platform payload as the blocking form. Media upload alone routinely runs for minutes, so pass `awaitCompletion: true` only when the MCP client's tool-call timeout exceeds ~8 minutes. A per-platform `status: "publishing"` is NOT final — PostPeer pushes to the platform asynchronously and it can still fail (e.g. X video-length limits); keep polling **`social_get_post_status`** with the returned `id` until it reports `published` (success) or `failed` (carries `lastError`, credits auto-refunded).
   - **All other long-running tools — async by default, poll `get_job_status`.** `generate_scene_image`, `generate_image_to_video`, `generate_images`, `edit_image_with_ai`, `remove_silence`, `transcribe_video_file`, `generate_tts_preview`, `generate_music`, `generate_sound_effect`, `remotion_render`, `x_search`, `youtube_upload_video`, `youtube_upload_from_local_file`, `download_generated_video`, `download_generated_music`, and `animation_studio_send_message` / `_send_and_compile` / `_send_compile_export` each return `{ started, jobId }` immediately. Poll **`get_job_status { jobId }`** every ~10–20s until `lastStatus` is `completed` (the `result` field holds the tool's full payload and `outputPaths` lists the absolute output files) or `error` (real error message in `error`). Pass `awaitCompletion: true` only when your tool-call timeout comfortably exceeds the tool's documented blocking window. **If a call or poll times out, the job is still running — NEVER blindly re-call the tool; paid generation would charge credits twice.** Jobs survive client-side timeouts but not an app restart.
   - **Other long-running work** (thumbnail creator UI flow) — follow each workflow; use `fetch_app_events` when those flows rely on IPC progress **and** the user cares about step-by-step output, or when debugging problems (see **Event stream**).
   - Report final completion/error to the user; use `fetch_app_events` for detail only when requested or when troubleshooting.

4. **Destructive actions**
   - Confirm user intent before `delete_project`, `delete_asset`, `delete_overlay_effect`,
     `remove_animation_studio_export`, or `clear_animation_studio_exports`.
   - **Removing a project library asset** (VIDEO/BROLL/SOUND/MUSIC) is usually **`update_project_settings`**, not `delete_asset` — see *Removing imported project assets* above.
   - For overlays, only imported/user overlays are deletable; default bundled overlays are protected.

5. **Keys and auth dependencies**
   - If provider features fail, check `read_api_keys`, balances, and auth status tools first.
   - For social posting, ensure account auth is active before upload.
   - Paid generation runs on Shorz account credits — use `get_shorz_credits` to confirm the user is
     signed in and has balance. If not signed in, sign them in with `shorz_sign_in_send_code` then
     `shorz_sign_in_verify_code` (ask the user for the emailed code).
   - **Zero-balance exception — the free tier.** A signed-in user whose balance is effectively empty
     (under 10 credits) still gets **4 free renders per week** (resets Monday 00:00 UTC, no rollover)
     on **`auto-edit` and `clipping` only**. So a low balance is not automatically a blocker for those
     two types — but it *is* for `text-to-video`, `avatar`, `podcast`, `advertisement` and `music-video`, which are
     paid only. The lease is opened and settled by the Electron **main** process around every render,
     so an MCP-triggered `trigger_create_video` / `generate_video` is covered exactly like the in-app
     Create Video button. A failed, stopped, or empty render does **not** consume one of the 4.
     (Unrelated to a desktop build that predates the tier: there the lease simply
     never opens and every call bills as before — a 402 on a zero-balance `auto-edit` render means
     this build, or the kill switch, not a mistake on your side.)
   - **Two things the app does for its own UI but NOT for you — do them yourself before a free render:**
     1. **Pin the model.** A free run zero-rates chat on **`google/gemini-3.8-flash`** and nothing else;
        any other model bills and 402s part-way through the render. The PromptBar pins it for
        button-started renders, but nothing pins it on the MCP path — call **`set_main_ai_model`** (or
        pass `mainAiModelName` on `trigger_create_video`) with `google/gemini-3.8-flash` first.
     2. **Check the source length.** Free runs cap the source at **30 minutes**. The renderer sends the
        probed duration so the proxy can refuse before the render starts; the MCP bridge does not send
        it, so an over-long source is **not** refused up front — probe with `get_media_info` and honour
        the cap yourself. Per-run abuse ceilings still apply server-side (6h lease, 400 LLM calls, 3M
        tokens, 5400 transcription seconds); tripping one ends the zero-rating mid-render, and the
        render then bills — i.e. 402s — from that point on.
   - **What a free run covers — the allowlist IS the paid boundary** (there is no second enforcement
     path): main-AI chat on the pinned model (plus a cheap analysis-tier Gemini id that a few pipeline
     steps hardcode — nothing for you to set), ElevenLabs **transcription**, and **web-image search**
     (the WEB B-roll source). Everything else bills normally inside a free run and therefore **402s at
     zero balance**. Free in a render: the LLM edit itself, local effects (cuts, filler-word/silence
     removal, zooms, face tracking, freeze frame, video colors), subtitles, titles, borders, overlays,
     **Auto SoundFX** (it places bundled sound files, no provider call), **four of the five B-roll
     sources — Assets, WEB, GIF and EMOJI** — and saving or exporting the finished file.
     Not free (do **not** enable or queue these for a zero-balance user):
     AI B-roll (`set_broll_settings.automaticAiBroll`, image *or* video), dubbing and auto-music and
     noise removal (`set_audio_settings`), thumbnail generation (`thumbnail_creator_generate`),
     Animation Studio chat (`animation_studio_send_*` — compiling/exporting an already-built animation
     is local and stays free), every standalone generation tool (`generate_images`,
     `generate_scene_image`, `generate_image_to_video`, `edit_image_with_ai`,
     `proxy_aiml_video_generation`, `generate_tts_preview`), `x_search`, and publishing
     (`social_publish`, `youtube_upload_*` — connecting an account is not itself billed, but the
     in-app Connect buttons are gated for these users, so don't promise a publish they can't pay for).
     **No silent-degradation cases:** everything on the free list above works in full on a free run —
     the only paid B-roll source is the **AI** tab, and every other lock above fails loudly with a 402
     rather than quietly dropping content from the finished video.
   - **Out of runs or out of credits?** There is no MCP purchase tool. Tell the user to buy credits in
     the app (**Buy Credits** opens Stripe Checkout in their **default browser**; the wallet is
     credited server-side and the app polls the balance), or to wait for the Monday 00:00 UTC reset.

## Tool Families

**Media always comes back as a file path, never base64.** No Shorz tool returns a data URL or a raw
base64 blob: generated and rendered media is written to disk and the response carries the absolute
path (`savedLocalFilePaths`, `pngFilePath`, `audioFilePath`, `outputPath`, `filePath`). Read that path
to inspect the file, or pass it straight to any tool that takes a local path. If a payload ever does
arrive inline, the server writes it to `%TEMP%\shorz-mcp-media\` and substitutes the path, appending a
note that names the extracted files — so a path is always what you act on.

### App and Configuration
- `check_for_update`
- `get_resource_path`
- `open_file_directory`, `file_exists`, `get_local_file_size`
- `read_api_keys`, `validate_elevenlabs_api_key`
- `get_elevenlabs_balance` (BYO ElevenLabs key balance; AIMLAPI key/license tools retired — paid generation runs on Shorz credits via the proxy)

### Shorz Account (credits + sign-in)
- `get_shorz_credits` — Shorz credit balance + entitlement for the signed-in user. Errors if no one is
  signed in or the credit server is unreachable. Check this before running paid generation tools. A
  balance under 10 credits means the free tier may apply — see *Keys and auth dependencies* below.
  The reply still carries a legacy **`watermark_free`** field: it is a deprecated alias for
  `has_purchased` and says nothing about exports. **Shorz watermarks nothing, at any tier** — never
  report that field to the user or treat it as an entitlement.
- `get_shorz_usage_and_pricing` — current model costs + recent usage for the signed-in user (same data
  as the in-app Usage & Pricing window): balance, recent calls, and per-model credit pricing. All
  amounts are in the credits the user pays (markup already included; never exposes our cost or markup).
  Free-tier renders appear in `recent_calls` as their own rows — `operation` reads
  **"Free run · Auto edit"** / **"Free run · Clipping"**, `units` shows the token spend, and `credits`
  is **0** (the in-app Usage tab renders those rows as "Free"). They carry `type: "addition"` as a
  quirk of the shared mapping — nothing was added; report them as free runs, not as credit grants.
- `shorz_sign_in_send_code` (email) → `shorz_sign_in_verify_code` (email + code) — email-OTP sign-in,
  identical to the in-app Sign-in button. Step 1 emails a one-time code; ask the user for it, then
  pass it (the 6–10 digit, usually 8-digit, value) to step 2. The Shorz desktop app must be running.

### Projects and Settings
- `create_project` (`projectType`: `auto-edit` \| `clipping` \| `text-to-video` \| `avatar` \| `podcast` \| `advertisement` \| `music-video` — hyphenated; anything else is rejected), `list_projects`, `delete_project`, `get_current_open_project`
- `read_project_settings`, `update_project_settings`
- `set_user_instructions` (PromptBar creative brief), `set_main_ai_model` (PromptBar main LLM)
- `switch_project_aspect_ratio` (directly updates `VIDEO_SIZE` width/height + optional fps)
- Direct panel settings tools:
  - `set_subtitle_settings`
  - `set_title_settings`
  - `set_border_settings`
  - `set_overlay_settings`
  - `set_audio_settings`
  - `set_audio_visualization_settings`
  - `set_broll_settings`
  - `set_text_to_video_settings`
  - `set_avatar_settings`
  - `set_podcast_settings`
  - `set_advertisement_settings`
  - `set_music_video_settings`
  - `set_general_video_settings`
- Panel styling and “looks” are applied only via granular `set_*_settings` (and project settings read/update); there are no MCP preset shortcut tools.

### Generation and Rendering
- `generate_video`, `stop_video_generation`, `get_video_generation_status` (primary status for project renders), `fetch_app_events` (IPC log stream; optional `since` cursor), `render_text_preview`
- `compile_remotion_preview`, `remotion_render`
- `proxy_aiml_video_generation`
- `generate_images` (standalone AIML image generation to library paths; no Thumbnail Creator modal). Optional `referenceImages` (up to 3 face/subject photos) preserve the **same face/identity** — the headless equivalent of the Avatar Creator modal's face-reference picker; use it to generate an avatar or podcast host that must look like a specific person.
- **Standalone generation assets (no project / no Create Video):**
  - `generate_scene_image` — Python text-to-video image stack (`Nano Banana 2`, `GPT Image 2` — the `GPT Image 2` id now serves GPT Image 2.5 — optional reference paths). Explicit `aspectRatio` or `width`/`height`. Does **not** read or write `SCRTIPT_TO_VIDEO`.
  - `generate_image_to_video` — Python i2v stack; requires `imagePath`, `prompt`, and explicit `videoModel` (same ids as `textToVideoVideoModel`). Optional `durationSec` (**rejected with an error if outside the per-model range** — Gemini Omni 1–10, Seedance 2.5 4–30, Seedance 2.0 family 4–15, Kling 3–15; omitted → 8), `aspectRatio` (**`16:9` or `9:16` ONLY, default `9:16`** — **1:1 is retired for video generation** and is rejected, even though standalone *image* generation still accepts it) or explicit dimensions, `generateAudio`. Does **not** run a project timeline.
  - Use these to produce library assets; use `import_frontend_assets` / project workflows when assembling a full video. **Do not** substitute these for `trigger_create_video` on text-to-video, avatar, or podcast projects.
  - Prefer `generate_scene_image` over `generate_images` for text-to-video parity (typed character/environment/style reference roles, exact TTV export dimensions). For **avatar / podcast face preservation** (keep a specific person's face), use `generate_images` with `referenceImages`. Prefer `generate_image_to_video` over `proxy_aiml_video_generation` for Shorz model routing (Gemini Omni native route, Seedance, Kling).
  - **Credits:** both tools call paid providers; invoke only when the user explicitly wants generation.
  - **Async by default:** `generate_scene_image`, `generate_image_to_video`, and `generate_images` return `{ started, jobId }` immediately — poll `get_job_status` (see rule 3 in **Required Workflow Rules**). Same for `remotion_render` and the `animation_studio_send_*` tools.
- `generate_music` — **text-to-music** into the generated-audio library (headless twin of the Music
  Generation panel). Two AIML models via the proxy: **`elevenlabs/eleven_music`** (default) honours
  `musicLengthMs` **10000–300000** and bills **~20 credits per MINUTE**, so cost scales with length;
  **`google/lyria2`** is a flat **~2 credits per generation**, picks its own length (**measured ~32.8s**)
  and **ignores `musicLengthMs`**. Use Lyria 2 for cheap loop/bed material, ElevenLabs Music when the
  track must match an exact duration. Async by default — poll `get_job_status`; the result is
  `{ success, path, newBalance }` with an absolute audio path whose extension matches the real
  container — **`.mp3` for eleven_music, `.wav` for Lyria 2** (48kHz PCM). Prompt instrumental-only when a voice-over
  sits on top. Distinct from render-time **auto-music** (`set_audio_settings`), which generates inside
  Create Video instead.
- `generate_sound_effect` — **one sound effect from a text description** (ElevenLabs sound generation,
  routed through the Shorz proxy on **Shorz credits**; a BYO ElevenLabs key is never used here — the same
  engine Auto SoundFX uses inside a render). `text` **3–450 chars**, optional `durationSeconds`
  **0.5–22** (default **1**) — match it to the motion it scores. One call per distinct cue (whoosh for a
  panel wipe, soft UI click, keyboard ticks, riser into a reveal, sub impact on a logo hit). Describe the
  sound physically and briefly (`'short airy whoosh, left to right, 0.4s, clean, no reverb tail'`) —
  material, speed and length beat film or brand names. For free CC0 library sounds search
  `openverse_search_sound_effects` first; generate when you need an exact length or a sound that does not
  exist. Async by default — poll `get_job_status`; the result is `{ success, path, newBalance }` with an
  absolute **`.mp3`** in the generated-audio library, ready for `import_frontend_assets` (assetType
  `'sound'`) or an Animation Studio `audioReferences` entry.
- `thumbnail_creator_generate`, `get_thumbnail_creator_generation_status`
- `animation_studio_list_models`, `animation_studio_send_message`
- `animation_studio_send_and_compile`
- `get_job_status` (generic poll for every async-by-default background job)

### Assets and Library
- Read/list: `get_my_videos`, `get_video_assets`, `get_image_assets`, `get_generated_thumbnails`,
  `get_audio_assets`, `get_downloaded_gifs`, `get_downloaded_images`, `get_available_fonts`
- Filtered search (multi-tab): `query_my_assets`
- **My Assets usage (not project-specific):** Library listing and search work whenever the user wants to inspect files (no open project required). Prefer **`query_my_assets`** when searching by name, date, or multiple tabs; use per-tab **`get_*`** for a full single-tab list. Fields, limits, and filter semantics: **`references/panel-workflows/README.md`** → *Library and cross-cutting MCP tools* → *Search and list My Assets*.
- Modify/import/export:
  - `import_frontend_assets` (`assetType`: `video` \| `broll` \| `sound` \| `music` \| `image` \| `avatar` \| `audio`; optional `overridePaths`) — **`assetType: "video"`** is main timeline / **Import Main Assets**; **only where the UI exposes it** (see **Main VIDEO import** above) — headless `overridePaths` imports into lane-disabled projects are **rejected with an error**. With **`overridePaths`**, library lanes (`video`/`broll`/`sound`/`music`/`audio`) validate, persist to **`ASSET_PATHS`**, and refresh Your Library in one call, returning `{ importedCount, imported[], skippedCount, skipped[], … }` — files whose name the lane already holds are **skipped, not added** (see **One asset per file name** above); read `skippedCount` before reporting success. **`image`/`avatar`** return metadata only — use typed panel tools to assign.
  - `rename_asset`, `delete_asset`, `save_file_as`,
  `save_image_data_as`, `download_generated_music`, `save_generated_sound_effect`,
  `download_generated_image`, `download_generated_thumbnail`, `download_generated_video`,
  `download_social_video` (**async by default** — returns immediately; poll
  **`get_social_video_download_status`** until `lastStatus` is `completed` or `error`.
  Pass `awaitCompletion: true` only for short clips: YouTube extraction alone routinely
  runs several minutes and will blow past the MCP request timeout.)
  - `download_generated_video` and `download_generated_music` are also **async by default**
    (large CDN files) — they return `{ started, jobId }`; poll **`get_job_status`**.
    Image/thumbnail downloads stay synchronous.

### Text-to-Video / Avatar Media Helpers
- `list_elevenlabs_voices`, `generate_tts_preview` (**async by default** — poll `get_job_status`; the completed `result` is `{ success, audioFilePath, mimeType, bytes, newBalance }` and the clip is a real file on disk. **Spends credits**, and a few thousand characters of narration render for minutes — never re-call it after a timeout, poll instead. Split long scripts into ~2,500-char chunks and re-join the mp3s with `concat_media`), `transcribe_video_file` (**async by default** — poll `get_job_status`; long footage transcribes for minutes)
- `save_avatar_image`, `save_avatar_audio`, `delete_avatar_audio`
- `save_text_to_video_speech_audio`, `delete_text_to_video_speech_audio`
- `save_text_to_video_reference_images`, `delete_text_to_video_reference_image`
- `select_local_image_for_import` (native file dialog; interactive — returns `{ success, filePath, fileName, canceled }`, the absolute path of the file the user picked; see `references/project-workflows/text-to-video.md`)

### Headless single-asset edits (no project)
- **Not tied to any `projectType`.** Operate on one local file via `inputPath`; optional `outputPath` for a stable save location.
- Tools: `trim_video`, `remove_ranges`, `remove_audio`, `set_audio_volume`, `change_video_speed`, `set_image_duration`, `rotate_media`, `flip_media`, `reverse_video`, `loop_video`, `fade_video`, `freeze_frame`, `crop_media`, `audio_fade`, `remove_silence`, `edit_image_with_ai`, `get_media_info`, `resize_media`, `fit_to_aspect`, `extract_audio`, `replace_audio`, `concat_media`, `extract_video_frames`
- Workflow: **`references/headless-workflows/single-asset-edit.md`**. Chain edits by passing each `outputPath` as the next `inputPath`. Do not substitute Create Video or an `auto-edit` project for a simple trim/crop request.

### Editing an already rendered auto-edit video (text instruction → new version)
- **`edit_generated_video { projectPath, videoPath, instruction }`** — one plain-language change to a video Create Video already produced ("cut 0:05-0:08", "swap the second and third clip", "remove the zoom near the start", "make the subtitles bigger", "add a zoom when I say launch", "turn the music down"). Works on auto-edit videos and on text-to-video stories made from generated images or AI clips (scene edits: "give scene 3 a different picture", "change what scene 2 says to …", "remove scene 4", "use a deeper voice", "dissolve between every scene"). Interprets the instruction into validated operations on the video's saved render plan (`<video>.plan.json`, written by every such render) and REPLAYS the render with every other AI decision pinned — nothing else changes, generated b-roll/GIFs/images and a story's narration, pictures and clips are reused, not re-billed. Produces a NEW versioned mp4 (the original stays), updates `last_generated_final_video_for_playback_mode`, and remembers the conversation per video. Async by default (poll `get_job_status`). `status`: `rendered` | `clarify` (answer the question with another call on the SAME `videoPath`) | `unsupported` | `failed` | `busy`. Videos rendered before this feature have no plan file → `unsupported`: create the video again first. Never use it to *create* a video, and never re-run `trigger_create_video` to "tweak" a finished one when this tool can.
- Workflow: **`references/project-workflows/edit-generated-video.md`**. The same editor exists in the app as the **Edit** pill over the PLAYBACK video.

### Headless project file pickers (local paths)

- Avatar: `select_avatar_image`, `select_avatar_angle_image`, `select_avatar_audio` → `references/project-workflows/avatar.md`
- Podcast avatars: `select_podcast_avatar_image` → `references/project-workflows/podcast.md`
- Advertisement images: `select_advertisement_image`, `remove_advertisement_image` → `references/project-workflows/advertisement.md`
- Music video song + artist image: `select_music_video_audio`, `remove_music_video_audio`, `select_music_video_character_image`, `remove_music_video_character_image` (take `filePath`, copy by path; `projectPath` defaults to the open music-video project) → `references/project-workflows/music-video.md`

### Overlay and Animation Studio
- `get_overlay_effects`, `import_overlay_effects`, `delete_overlay_effect`
- `get_animation_studio_exports`, `remove_animation_studio_export`,
  `clear_animation_studio_exports`

### Canvas (node-graph video builder)
- `canvas_list`, `canvas_get` — read canvases (free; opens nothing).
- `canvas_build` — create a canvas or add to one from `{ name, nodes, edges }` (the Build with AI
  JSON shape) plus `updates` for existing nodes. Strict and all-or-nothing; opens Canvas so the
  user watches. Free.
- `canvas_remove` — delete nodes (with their wires) and wires; `canvas_build`'s `remove` field does the
  same inside one all-or-nothing edit, so rewiring is a single call.
- `canvas_run` — runs only out-of-date nodes and returns the Export node's `outputPath`. **Two-step
  spend:** a paid plan returns the estimate and runs nothing until you call again with
  `maxCredits` ≥ the estimate — show the user that number first. Async: poll `get_job_status`.
- `canvas_stop` — stop the running canvas (like the Stop button; in-flight generations finish and
  are kept, the run's job ends with `stopped: true`). `canvas_rename`, `canvas_delete` (only when the
  user asked; moves the file to `Canvas/.trash`, media stays). None of the three opens Canvas.
- `canvas_pick_take` — choose a node's take (number, 1 = oldest, or id from `canvas_get` `takeList`);
  downstream becomes out of date. `canvas_duplicate` — copy a canvas with every take (branching).
  Neither opens Canvas.
- Full contract, node catalog and examples: **`references/panel-workflows/canvas.md`**.

### Social Publishing
- YouTube (native): `youtube_auth_status`, `youtube_auth_start`, `youtube_remove_account`,
  `youtube_sign_out`, `youtube_upload_video`, `youtube_upload_from_local_file`
- **Custom YouTube thumbnails:** both upload tools — and `social_publish`'s youtube entry (or its
  top-level `thumbnailSrc`) — accept optional **`thumbnailSrc`** (local image path), set via
  `thumbnails.set` right after the upload and auto re-encoded/downscaled under YouTube's 2MB cap.
  A thumbnail failure never fails the upload: the result stays `success:true` with
  `thumbnail:{set:false,error}` plus a `warning`. A **403 means the channel isn't phone-verified**
  (YouTube gates custom thumbnails on verification) — don't retry; verify at youtube.com/verify or
  set it in Studio.
- TikTok / Instagram / Facebook / X / LinkedIn / Threads / Pinterest: connect and publish via the unified `social_*` tools
  (`social_connect_account`, `social_publish`, `social_list_scheduled`, `social_disconnect_account`, …),
  routed through PostPeer. (YouTube can also publish/schedule via `social_publish`.)
- **Where `accountId` comes from:** `social_publish` requires an `accountId` per non-YouTube platform — get it
  from **`social_list_connections`** (returns `accountId`, `displayName`, `status` per connected account;
  `refresh: true` re-syncs from PostPeer). For YouTube use `youtube_auth_status` instead (it yields `channelId`).
  Board ids for Pinterest come from `social_get_posting_options`.
- **Quote the cost before publishing:** **`social_estimate_publish_cost`** (`platforms[]`, plus
  `xCaptionHasLink: true` when the X caption contains a URL) returns the server-priced credit breakdown.
  Prices are **not** uniform — **X costs ~5× the base rate, and ~50× when the caption carries a link**;
  every other platform including LinkedIn / Threads / Pinterest bills at the base rate. A multi-platform
  publish is one fan-out but **N separate charges**, so estimate first rather than assuming one post = one charge.
- **Every publish costs credits**, on both routes (`social_publish` bills per platform; the native
  YouTube upload is billed after the upload lands). The free tier does **not** cover publishing, so a
  zero-balance user cannot post even from a free render's output — connecting an account is not itself
  billed, but the in-app Connect buttons are gated for those users, so don't set up a publish they
  can't complete. `social_refresh_analytics` stays free.

### Event stream (`fetch_app_events`)

**When to use (project video):** Prefer **`get_video_generation_status`**. Call **`fetch_app_events`** only if the user asks for live logs/progress, or when **debugging** video creation (hangs, errors, stalls) and you need raw `video-generation-log` / channel traffic. Pass optional **`since`** (ms timestamp) to poll incrementally.

The bridge records **every** `mainWindow.webContents.send(...)` from the Electron main process to the renderer (ring buffer, latest ~2000 entries). **`fetch_app_events`** exposes that buffer over MCP; it is **not** limited to video generation.

- **Shape**: Each entry is `{ channel, args, timestamp }` where `timestamp` is a Unix ms clock value when the send occurred.
- **Args are summarized, not verbatim**: the log answers *what happened*, so long strings, long arrays and oversized payloads are recorded as markers (`[omitted image/png data URL, 1953.1 KB]`, `[+480 more items omitted]`). Read the settings or asset tools for full values; `fetch_app_events` is for channel traffic and log lines.
- **Incremental polling**: Pass optional `since` (number). The bridge returns events with **`timestamp` strictly greater than `since`**. After each response, set `since` to the **largest `timestamp` in that batch** (or the latest event you processed) so the next call returns only newer sends. This is a **time cursor**, not a sequential event index.
- **Typical channels during work** (non-exhaustive): `video-generation-state`, `video-generation-log` (callback log lines during `generate-video`), `youtube-upload-progress`, `social-publish-progress`, `remotion-render-progress`, `mcp-activity` (after MCP invoke calls complete), `animation-studio-mcp-workflow`, `thumbnail-creator-generation-state`, and routine UI traffic such as `window-state-changed`.
- **Idle / no active generation**: The tool still succeeds; batches may be empty or contain **unrelated** IPC from normal UI activity. Do not expect `video-generation-log` entries unless generation (or another feature emitting those channels) is actually running.
- **Completeness**: For whether generation finished, failed, or was stopped, **`get_video_generation_status`** is authoritative for projects. Use `fetch_app_events` to supplement, not replace, when diagnosing.

## Frontend Parity Guidance

- **Header menu**
  - API keys/license/update map to app/config tools where exposed over MCP. Opening external URLs (pricing, privacy, etc.) uses in-app IPC only, not MCP.
- **Project manager modal**
  - Create/list/delete/open behavior maps to project tools.
- **Panel option controls (Text-to-video, Avatar, Advertisement, Music Video, Settings, Border, Text, Audio, B-roll)**
  - Prefer direct tools (`set_*_settings`) for panel-level updates.
  - Static options are now defined in MCP input schemas via enums (no separate "list options" tool needed for fixed values).
  - Dynamic values still come from listing tools, e.g. `list_elevenlabs_voices`, `get_available_fonts`, social auth/account tools.
  - `set_border_settings` accepts `border` (toggle; matches the Border panel), optional legacy `borderActive` if `border` is omitted, plus `borderWidth`, `borderColor1/2`, `borderAnimation`, `borderAnimationDuration`.
  - `borderWidth` is clamped to **1–100**; `borderAnimationDuration` is clamped to **1–5** (matches Border panel sliders).
  - `borderAnimation` supports: `None`, `Fade`, `Circular`, `Moving Circles`, `Hypnotizing Grid`, `Wave`, `Grain`, `Scratches`, `Blink`, `Full Color Spectrum`.
  - Over MCP, `borderAnimation` must use those **exact** enum strings (case-sensitive at the tool boundary); invalid values fail validation with the allowed list. Server-side normalization applies only after a value passes MCP input validation.
  - `set_text_to_video_settings` static enums include:
    - `textToVideoInputMode`: `script` | `audio`
    - `textToVideoSourceMedia`: `imported` | `generated_images` | `generated_video`
    - `textToVideoTransitionType` / `textToVideoTransitionTypes`: `none`, `automatic`, `fade`, `dissolve`, `fadeblack`, `fadewhite`, `fadegrays`, `wipeleft`, `wiperight`, `wipeup`, `wipedown`, `slideleft`, `slideright`, `slideup`, `slidedown`, `smoothleft`, `smoothright`, `smoothup`, `smoothdown`, `revealleft`, `revealright`, `revealup`, `revealdown`, `circleopen`, `circleclose`, `circlecrop`, `radial`, `pixelize`, `distance`, `hrslice`, `hlslice`, `squeezeh`, `zoomin`, `hblur`
    - `textToVideoImageMotion` / `textToVideoImageMotions`: `none`, `ai`, `zoom_out`, `zoom_in`, `zoom_in_left`, `zoom_in_right`, `zoom_in_top`, `zoom_in_bottom`, `random_zoom`, `rapid_zoom`, `pan_left`, `pan_right`, `pan_up`, `pan_down`, `handheld_camera`, `rotation`
    - `textToVideoImageModel`: `Nano Banana 2`, `GPT Image 2` (= GPT Image 2.5 Flare, fast), `GPT Image 2.5 Sunburst` (sharper, a few seconds slower, same 2 credits) (Nano Banana 2 Lite is not a TTV option — it stays for AI B-roll and standalone generate_images)
    - `textToVideoVideoModel`: `bytedance/seedance-2-0-mini` (the server catalog default for `text_to_video`, and the cheapest at ~9 cr/s @720p), `klingai/video-v3-standard-image-to-video` (3–15s clips, ~26 cr/s), `gemini-omni-flash-preview` (native Google route, token-billed ~12 cr/s), `bytedance/seedance-2-5` (premium: 4–30s in ONE generation, 480p/720p, ~27 cr/s), `bytedance/seedance-2-0`, `bytedance/seedance-2-0-fast`. **Do not assume a persisted default** — the on-disk value varies by how the project was created; read it with `read_project_settings` and set it explicitly with `set_text_to_video_settings`. **Retired, do not send:** `google/veo-3.1-i2v-fast` (rejected on write) and `custom:happyhorse-1.0` (**passes MCP validation**, but its catalog row is disabled, so the write succeeds and the render then fails at generation time)
  - `set_music_video_settings` — `videoModel` / `imageModel` are **live catalog ids, not enums** (the `text_to_video` rows — the same models as Text-to-Video); an unknown or disabled id is rejected with the current list, and a new `videoModel` also stores its per-clip range. `cutPace`: `auto` | `relaxed` | `energetic`; `sectionTransitions`, `useFullSong` booleans; `rangeStartSec` / `rangeEndSec` seconds (`0` end = to the end of the song); `lipSync` boolean (a few AI-picked sung moments become close-ups lip-synced to the song) with `lipSyncModel` `Kling Avatar Pro` | `Kling Avatar` | `OmniHuman 1.5`. Full contract: `references/project-workflows/music-video.md`.
  - `set_text_to_video_settings` also accepts:
    - `textToVideoScript`: string
    - `textToVideoVoice`: string (typically an ElevenLabs voice id/name)
    - `textToVideoReferenceImagePaths`: `string[]` (local/URL image references)
  - `set_general_video_settings` Auto Zoom usage:
    - `zoomType: "Intelligent Auto Zoom"`: uses `zoomCount`, `zoomStrength`, `zoomSpeed`, `zoomInEffects`, `zoomOutEffects` (non-empty string arrays; allowed ids in `references/panel-workflows/settings.md`). Legacy `zoomInEffect` / `zoomOutEffect` single strings still accepted (+ `autoZoom` on this tool; `zoomSounds` on `set_audio_settings`).
    - `zoomType: "Zoom on Music Beat"`: UI exposes a reduced set; keep `autoZoom` / `zoomSounds` / `zoomType` primary and avoid assuming all Intelligent Auto Zoom tuning controls are active in this mode.
  - Title manual-only controls: `titleStartTime`, `titleDuration` (with `titlePlacement: Manual`).
  - **Title inline emojis (optional):** `titleText` may include standard Unicode emoji (e.g. `🔥`, `⭐`); they render inline in export and Editor preview when present. Plain text titles need no emoji and no extra MCP flag. Distinct from B-roll **`automaticEmojis`** (timed PNG overlays via `set_broll_settings`).
  - **Title/subtitle position:** `titlePositionX` / `subtitlePositionX` are horizontal **center** %; `titlePositionY` / `subtitlePositionY` are **top edge** %. Export and preview **clamp** so the measured text box stays inside ~2% frame insets — raw **100%** horizontal may clamp inward for wide titles. UI Position presets use measured text size; wait for metrics before relying on corner presets.
  - **Title text alignment (titles only):** `titleAlignment` (`left`/`center`/`right`, default `center`, persisted as `title_alignment`) aligns wrapped lines **inside** the title block — visible only when `titleMaxWordsPerLine` wraps the headline, and it does **not** move the block (that is `titlePositionX`/`titlePositionY`). The subtitle twin `subtitleAlignment` is still validated-then-dropped, so do not assume symmetry.
  - **B-roll overlay position:** same center-X / top-Y % model for fit-mode **Assets** (`brollPositionX`/`brollPositionY`), **Web** (`webImagesPositionX`/`webImagesPositionY`), **GIF** (`gifPositionX`/`gifPositionY`), and **AI** (`aiBrollPositionX`/`aiBrollPositionY`). Fullscreen assets ignore position. Legacy preset keys on disk migrate on load; MCP patches should use `*PositionX`/`*PositionY`. See **`references/panel-workflows/broll.md`**.
  - Title/subtitle stroke width inputs are validated to a minimum of `1` when enabled (`0` is only valid in disable flows).
  - `set_broll_settings` — full contract in **`references/panel-workflows/broll.md`**. Summary:
    - **Transitions:** every B-roll type has a separate entrance pool (`*TransitionAnimations`) and exit pool (`*TransitionOutAnimations`), same id set; exit plays the effect reversed as the asset leaves. Both default to `["None"]`.
    - **Assets:** `fullscreenBRoll`, `brollPositionX`/`brollPositionY` (`0..100`, fit only), `brollFitWidthPercent` (`30..100`, fit only), `brollTransitionAnimations`, `brollTransitionOutAnimations`, `brollTransitionDuration` (`0.2..1.0`, applies to in+out; only when transitions ≠ `None`)
    - **Web:** `automaticWebImages`, `webImagesTransitionAnimations`, `webImagesTransitionOutAnimations` + `webImagesAnimationDuration` (in+out; only when transitions ≠ `None`), `webImagesCount` `1..30`, `webImagesSize` `100..1920`, `webImagesPositionX`/`webImagesPositionY` `0..100` (each web image's on-screen time is derived from the transcript, not a setting — steer via prompt)
    - **GIF:** `automaticGifs`, `gifType`, `gifCount`, `gifPositionX`/`gifPositionY` `0..100`, `gifWidthPercent` `30..100`, `gifTransitionAnimations`, `gifTransitionOutAnimations`
    - **AI:** `automaticAiBroll`, `aiBrollType` (`"image"` stills or `"video"` text-to-video clips), `aiBrollImageModel` / `aiBrollVideoModel` (server-catalog ids, project type `broll` — e.g. `"Nano Banana 2"`, `"Nano Banana 2 Lite"`, `"GPT Image 2"` (= GPT Image 2.5 Flare), `"GPT Image 2.5 Sunburst"` / `"bytedance/seedance-2-0-fast"`, `"bytedance/seedance-2-0-mini"`, `"bytedance/seedance-2-5"`, `"klingai/video-v3-standard-text-to-video"`), `aiBrollCount`, `aiBrollPositionX`/`aiBrollPositionY` `0..100`, `aiBrollWidthPercent`, `aiBrollTransitionAnimations`, `aiBrollTransitionOutAnimations`. Video clip length is decided by the AI from speech timing (clamped to the model's range) — there is no length setting, and video mode costs far more than image mode.
    - **Emoji:** `automaticEmojis`, `emojiSounds`, `emojiCount`, `emojiAnimations`, `emojiPositionX`, `emojiPositionY`, `emojiSize`
    - **B-roll sounds (separate tool):** `set_audio_settings.imageSounds` for assets/web/gif/ai appearance SFX
  - Use `switch_project_aspect_ratio` for preview aspect ratio changes (`16:9`, `1:1`, `9:16`).
  - Fallback to `read_project_settings` + `update_project_settings` for unsupported edge keys (still pass only the nested keys you need in `updates`).
- **Thumbnail Creator**
  - Use `set_thumbnail_creator_settings` to patch draft state and `thumbnail_creator_generate` for one-call generation (default async: omit `awaitCompletion` or pass `false`, then poll `get_thumbnail_creator_generation_status` until `isGenerating` is false).
  - `referenceImages` and `youtubeReferenceUrl` remain persisted in draft across model switches.
  - `referenceImages` and `youtubeReferenceUrl` are consumed by **both** models: Nano Banana via `image_urls`, and GPT Image 2.5 via OpenAI image edits. (`youtubeReferenceUrl` applies in `16:9`.)
- **My Assets and Library**
  - Listing/search: see **Assets and Library** above and **`references/panel-workflows/README.md`** (*Search and list My Assets*). Import/download/delete/rename/save: same tool family as in **Assets and Library**.
- **Overlay panel**
  - Use `get_overlay_effects`, `import_overlay_effects`, `delete_overlay_effect`.
- **Animation Studio**
  - Use `references/panel-workflows/animation-studio.md` as the primary workflow reference.
  - For low-level/manual control, `compile_remotion_preview` and `remotion_render` remain available.
- **Social publishing**
  - YouTube (native): authenticate first, then upload. Prefer `youtube_upload_from_local_file` for headless runs: pass a disk path, resolve the account with `channelId` or `channelTitle`. Low-level `youtube_upload_video` remains available for full control. Both take optional **`thumbnailSrc`** (local image path) — set as the custom thumbnail via `thumbnails.set` after the upload, auto-fitted under YouTube's 2MB cap; a thumbnail failure never fails the upload (result carries `thumbnail:{set:false,error}` + `warning`; 403 = channel not phone-verified, don't retry). Schemas constrain **`privacy`** to `public` | `private` | `unlisted` and **`category`** to the same fixed names as the Electron `YOUTUBE_CATEGORY_IDS` map (optional; default category id 24 if omitted). Both upload tools are **async by default** — they return `{ started, jobId }`; poll `get_job_status` until `completed`/`error` (`awaitCompletion: true` blocks, needs a tool-call timeout >= 8 minutes).
  - TikTok / Instagram / Facebook / X / LinkedIn / Threads / Pinterest: connect with `social_connect_account`, then publish or schedule with `social_publish` (routed through PostPeer; charges Shorz credits per platform). Media is optional — `social_publish` accepts a **video**, an **image**, or **no media (text-only)** via `mediaSrc` (a local path; `videoSrc` is an alias). Optional top-level `thumbnailSrc` (local image) becomes the video's thumbnail on the PostPeer platforms **and** the YouTube custom thumbnail (a `thumbnailSrc` on the youtube platform entry overrides it). Support by platform: text-only → X / LinkedIn / Facebook / Threads; image → X / LinkedIn / Facebook / Instagram / Threads / Pinterest; video → all. Instagram & Pinterest always need media; YouTube & TikTok need a video. LinkedIn posts to a personal profile or company page and accepts `platformSpecific:{ visibility:'public'|'connections' }` (defaults public). Threads accepts `platformSpecific:{ replyControl:'everyone'|'accounts_you_follow'|'mentioned_only' }` (defaults everyone; captions max 500 chars). TikTok accepts `platformSpecific:{ privacyLevel:'PUBLIC_TO_EVERYONE'|'MUTUAL_FOLLOW_FRIENDS'|'SELF_ONLY' }` — TikTok **requires** a privacy level for a direct post, so the proxy defaults it to `PUBLIC_TO_EVERYONE` when omitted; pass it explicitly to post privately, and check the account really offers that level via `social_get_posting_options` (`privacyLevelOptions`). TikTok also accepts `platformSpecific:{ draft:true }` to send the video to the TikTok inbox instead of posting it (the user must then open TikTok and tap Post; no privacy level applies). Note a TikTok rejection is **asynchronous** — it surfaces ~90s after the slot, never at create time, so always poll `social_get_post_status` rather than trusting the create result. Pinterest **requires** `platformSpecific:{ boardId }` — list the account's boards first with `social_get_posting_options` (`platform:'pinterest'` → `boards[]`) — plus optional `title` (max 100 chars, defaults to the caption's first line), `link` (https destination URL), and `altText`. `social_publish` also handles YouTube. **Async contract:** default is non-blocking — poll `get_social_publish_status` for job completion, then poll `social_get_post_status` (by the result `id`) until `published`/`failed`: a `publishing` status means PostPeer has not finished the platform push yet and the post can still fail (failure auto-refunds and records `lastError`). Use `social_list_scheduled` / `social_get_post_status` / `social_reschedule_post` / `social_cancel_scheduled` to manage posts.
  - **"Where has this video already gone?"** every `social_list_scheduled` row carries `localPath` — the desktop path of the file that was published — so filter the calendar by it to answer that without asking the user. Rows carry **no account id**, so the answer is per platform, not per account. The app shows the same thing as platform icons on My Videos cards / the preview player and a POSTED tag in the Publish modal. Re-publishing the same file is **never blocked** (deleting a post and re-posting is normal and nothing can detect it), but do tell the user about a prior post before posting again rather than silently charging twice.
  - **Post performance:** published rows in `social_list_scheduled` carry `analytics` (`{metrics:{views, likes, comments, shares, impressions, reach, saves, clicks, engagementRate}, source, collectedAt}` — a `null` metric means that platform doesn't expose it) plus `analyticsAt`. Call `social_refresh_analytics` first for fresh numbers (free, no credit charge): it triggers the server's PostPeer analytics sweep and pulls YouTube stats via the user's own OAuth; `swept:false` + `nextAllowedInS` in its reply means the numbers were refreshed recently enough already (success, not an error). Platform gaps: TikTok has no impressions/reach; Instagram exposes likes/comments only; Facebook has no impressions; LinkedIn metrics exist for Company Pages only (personal-profile posts stay without analytics); X reports impressions rather than views; Pinterest counts saves/clicks; Threads exposes whatever its API reports.


## Example Workflow: Full Project Run

1. `create_project` (or `list_projects` + pick existing).
2. `read_project_settings` for a baseline when needed.
3. Apply user-requested panel option changes via `set_*_settings` and/or `update_project_settings` with partial `updates`.
4. `import_frontend_assets` / media save tools as needed.
5. `generate_video`.
6. Poll **`get_video_generation_status`** until `lastStatus` is terminal. Use **`fetch_app_events`** only if the user wants the log stream or you are troubleshooting a problem (see **Event stream**).
7. Export or publish via download/social tools.
