---
name: video-produce
description: End-to-end video production — turns a brief into a delivered MP4 (or an approved prompt) across every available path. Routes to generative models, coded-film kits (cinecode, bang-motion, motion-graphics, motion-design), the hyperframes HTML renderer, the code2video Manim plugin, or MoneyPrinterTurbo. Keeps recurring characters consistent via the characters/ library. Use when the user asks to MAKE a video (not just write a prompt) — "اعمل فيديو", "make a video", "video about X", "فيديو عن", "اصنع موشن", "production", or names a kit/preset (cinecode, bang-motion, hyperframes).
personas:
  - MARKETING
  - DEV
triggers:
  - اعمل فيديو
  - اصنع فيديو
  - make a video
  - produce video
  - video production
  - رندر فيديو
  - render video
  - cinecode
  - bang-motion
  - hyperframes
  - motion graphics
  - موشن جرافيك
  - كراكتر في الفيديو
  - نفس الكاركتر
---
[SKILL] video-produce
[OBJ] Deliver a finished video from a plain-language brief. The user never needs to know which engine fits — the router picks the cheapest path that satisfies the ask, asks only the questions that change the output, and keeps characters/brands consistent across productions.

[CORE] Prompt → produce → deliver. When the user only wants a prompt, hand off to `video-prompt` and stop. When they want the video, this skill owns the whole run: intake → route → kit questions → build → gates → deliver.

[RULES]

## 1. Intake — extract before asking

From the message + chat history, extract: subject/idea, platform (aspect), duration, audio needs, style/mood, characters named, references sent, target model or kit named, deadline/cost sensitivity. Never re-ask answered dimensions.

If a **character alias** appears (any `characters/*-char.md` name), load the sheet BEFORE routing — it decides which paths are viable (see §4).

If the ask is "برومبت بس" / "just the prompt" → delegate to `video-prompt` skill and stop here.

## 2. Route — pick ONE primary path

| Path | Produces | Cost | Best for | Engine location |
|---|---|---|---|---|
| **GEN** generative model | prompt only (user renders in Veo/Kling/Runway UI or API) | per-gen $$ | cinematic realism, talking heads, footage that must look filmed | `video-prompt` skill output |
| **CINECODE** | MP4 film (quick ~3min or film-mode gated) | free + tokens | narrative shorts, animation, ads, explainers 15s–10min | `~/.aizee/media/kits/cinecode/` |
| **BANG-MOTION** | `index.html` → MP4 via export-frames | free + tokens | openers, promos, kinetic type, 6 explainer styles | `~/.aizee/media/kits/bang-motion/` |
| **MOTION-GRAPHICS** | MP4 (WebGL+Canvas2D, motion blur, multi-format) | free + tokens | social ads/Reels, launch pieces, beat-synced edits, VO+narration | `~/.aizee/media/kits/motion-graphics/` |
| **MOTION-DESIGN** | MP4 (seek(t) engine, synthesized score) | free + tokens | launch films, showreels, LinkedIn/X videos, remake-a-video | `~/.aizee/media/kits/motion-design/` |
| **HYPERFRAMES** | MP4 from HTML compositions | free + tokens | any HTML→video, captions/overlays, registry blocks, Studio preview | `hyperframes` CLI (global npm) |
| **CODE2VIDEO** | MP4 educational animation (Manim) | API keys + Docker | lessons, explainers, classroom content | `plugins/code2video` (`aizee generate video`) |
| **MPT** | MP4 topic→shorts | LLM/TTS keys | faceless shorts at volume, batch | `~/.aizee/media/apps/MoneyPrinterTurbo/` |
| **EDIT** | cut/dub/subtitle of user's footage | free | user's own recordings | ffmpeg + transcript (whisper optional) |

Route rules:
- Named kit/model in the message wins ("cinecode-style film" → CINECODE).
- Realism/camera-footage feel → GEN. Everything else defaults to a coded path (free, deterministic, character-consistent).
- Hybrid is normal: coded graphics + generated plates (MOTION-GRAPHICS `generative-video.md` roles). Plan per-segment, not per-video.
- Verify the kit exists before routing (`Test-Path`); if missing, say so and offer install or fallback — never pretend.

## 3. The question flow — what the model asks, and when

ONE `ask_user_question` call per gate, ≤4 questions, plain Arabic, ★ = recommended. Skip anything already answered. Total interview budget: intake (this skill) + the kit's own gates — never stack two question rounds back-to-back.

| Gate | When | Questions (plain Arabic → internal) |
|---|---|---|
| G0 Route | after intake, path not obvious | "الأسلوب؟" → ★ الأنسب للطلب (each option names the path in user words: فيلم قصير / موشن جرافيك / فيديو ذكي بالـ AI / مونتاج على ضحكتك) · "أو اختار مسار معين" |
| G1 Brief | kit needs it (all coded paths) | the kit's own first round — see §5 per-path table |
| G2 Plan/Style | before any build | concept pick or style-brief approval — ONE question, artifact shown first |
| G3 Paid | only if billable calls exist | "هتحتاج N عملية توليد مدفوعة (~cost) — أوافق؟" approve/revise |
| G4 Draft | draft rendered | watch → "Final / ملاحظات / رأي تاني" |

Rules:
- An approved gate starts the next step in the SAME turn — "تمام" is a go, not an end.
- Show before asking: boards/stills/drafts are shown, never described blind.
- Long jobs (>~2 min) get a progress note with done/total + ETA; "خلص؟" is answered from the status file, never guessed.
- "استنى/وقف" pauses at the next gate; "كمّل على طول" runs to draft without questions (choices logged, each reversible as a note).

## 4. Character consistency in production

The `characters/` library is the single source — every path consumes it differently:

| Path | How the character stays identical |
|---|---|
| GEN (prompt) | `video-prompt` injects the sheet's `VERBATIM:` block word-for-word + `[ImageN]` refs from `<name>-char/` where the model supports them |
| GEN (video gen segments) | reference images = angle-matched sheet images + previous segment's last frame (carry-forward); verify keyframe still BEFORE animating |
| CINECODE / BANG-MOTION / MOTION-* | character = code/data: build once as a profile/rig (palette, proportions, signature detail from the sheet) and reuse the SAME asset files across films — identical by construction, zero drift |
| CODE2VIDEO | character appears only as narration/avatar — sheet informs voice + on-screen label |

Hard rules:
- NEVER paraphrase the `VERBATIM:` block; NEVER regenerate a locked anchor/portrait.
- Sheet missing but user wants recurrence → offer to create via `_template-char.md` (2-3 visual details) BEFORE producing.
- Multiple characters → each gets its own binding in the plan (orkas rule: describe by visual features, not names, in gen prompts).
- Record per-production which sheet version + refs were used (in the film folder's STATE/plan file) so a resumed run reproduces the same look.

## 5. Per-path execution notes

- **CINECODE** — read `kits/cinecode/SKILL.md`; it drives its own interview (mode Quick/Film + purpose). Setup: `python3 scripts/init_film.py <name> --quick|--to-film`. Needs Node≥22, Python≥3.9, ffmpeg, Chrome — verify with `aizee deps` first (deps.yaml).
- **BANG-MOTION** — read `kits/bang-motion/SKILL.md` (Indonesian; translate instructions, keep rules). Flow: style brief (3 concept candidates + palette-with-sources) → approve → build `index.html` → `snap.mjs` verify → `export-frames.mjs` MP4. Watch = browser only; export needs Node+ffmpeg.
- **MOTION-GRAPHICS (igorls)** — read `kits/motion-graphics/SKILL.md`. Brand profiles live in `kits/motion-graphics/profiles/` + `profiles/local/` (private). Engine = `template/` (bun + ffmpeg + Chrome). Generative clips via `scripts/comfy.ts`/adapters when keys exist.
- **MOTION-DESIGN (howseen)** — read `kits/motion-design/SKILL.md`. Flow: inputs → BEATMAP → 4 stills → `render_template.py` (Playwright) → `audio_template.py` → critics → FIXES. `INDEX.md` film library pattern — append each finished film.
- **HYPERFRAMES** — `npx hyperframes init <dir>` → write compositions → `npx hyperframes check --json` → `snapshot --review` → render on approval. Contract: `class="clip"` + `data-start/duration`, paused `__timelines`, no Date.now/random/fetch. Registry search before hand-writing effects.
- **CODE2VIDEO** — `aizee generate video --topic "..."` (plugin; needs Docker image built once + provider API key env).
- **MPT** — if installed: topic → WebUI/API/CLI; EdgeTTS free, LLM key for scripts.
- **EDIT** — ffmpeg cut/trim/silence; whisper.cpp or Groq whisper for transcripts → word-timed captions.
- **GPU encode** — `scripts/gpu-bin/` ships an ffmpeg shim that rewrites `libx264/x265/AV1` → `*_nvenc` and **auto-passes-through to CPU when NVENC is absent** (no GPU = everything works unchanged). Put it first on PATH for kit renders (`aizee deps` entries `ffmpeg-nvenc`, `gpu-shim-on-path`, `gpu-chrome-hiperf`); `AIZEE_FFMPEG_NVENC=0` forces CPU, `=1` forces GPU. When `aizee deps` shows `ffmpeg-nvenc` ok, fold the choice into G2: "نرندر على الكارت ولا الـ CPU؟" (★ GPU — أسرع ~3x) and record it in the plan file; when absent, never mention it.

## 6. Long videos — segment, don't marathon

Duration >~60s or multi-scene: write a `plan.json`/EDL first (segment list: each {path, refs, duration, audio, status}). Produce segment-by-segment; each segment re-renders independently. Carry-forward frames/decision cache between adjacent segments (same scene → last frame becomes next segment's top reference). State total segment count + est. time before starting; get one OK.

## 7. Deliver

1. The file — absolute path, playable MP4 (or `index.html` for browser-native pieces + MP4 on request).
2. One-line AR summary: path used, duration, resolution, what was decided.
3. Open choices — anything made by ★ that the user may want swapped (one line each).
4. For coded pieces: the project folder path (STATE.md/plan file inside) so "كمل من حيث وقفنا" resumes correctly.

[PROHIBIT]
1. No paid/generative calls without G3 confirmation stating exact count + cost.
2. No full render before stills/keyframe approval on coded paths.
3. No paraphrasing VERBATIM character blocks; no regenerating locked anchors.
4. No hardcoded kit paths — `~/.aizee/media/kits/` convention + `AIZEE_MEDIA_DIR` env override only.
5. No claiming a file exists before it does; no silent long renders — progress notes required.
6. No kit internals copied into this skill — kits are read at runtime from their install dir; this file holds only routing + gates + consistency rules.
