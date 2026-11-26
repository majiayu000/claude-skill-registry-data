---
name: video-prompt
description: AI video generation prompt engineering. Guided interview -> cinematic prompt. Use when the user asks for a video prompt, AI video, motion graphics, or names a video model (Veo, Kling, Runway, Seedance, Hailuo, Sora, Wan, Luma). Covers scene, camera, lens, lighting, audio, multi-shot timecodes, references, and per-model syntax. Do not use for general/non-video prompt writing — use `prompt-engineer`, `prompt-master-patterns`, or `prompt-master-templates` instead; do not use for making/rendering the video itself — use `video-produce` instead.
personas:
  - MARKETING
triggers:
  - برومبت فيديو
  - video prompt
  - ai video
  - موشن جرافيك
  - motion graphics
  - جنرييت فيديو
  - veo
  - kling
  - runway
  - seedance
  - hailuo
  - sora
  - wan ai
  - luma
  - cinecode
  - bang-motion
---
[SKILL] video-prompt
[OBJ] Turn a plain-language video idea into a production-ready AI video prompt. The user never needs to know cinematography vocabulary — the interview extracts intent, the assembly layer translates it into model-ready direction.

[CORE] The user describes in their own words (Arabic/Egyptian OK); the skill does the translation. Never ask the user to write camera/lighting terms — offer choices in plain language and map them to film vocabulary internally.

[RULES]

## 1. Trigger & Intake

Fire when the user asks for a video prompt OR names a video model. Before asking anything, extract what the message already answers:

- subject/idea (always needed — if absent, ask it as plain text first)
- platform → aspect ratio (TikTok/Reels/Shorts=9:16, YouTube/landing=16:9, ads=16:9 with 4:5 crop note)
- duration → shot structure (≤5s single shot, 10-15s multi-shot timecode, longer=extend)
- audio need → silent / music / SFX+ambience / dialogue
- style/mood, camera feel, character, references, target model

Never re-ask what the user already stated. If the user says "اختار انت" / "you decide" on anything, decide and state the assumption in the output notes.

## 2. Interview Protocol (multiple-choice first)

Use `ask_user_question` — ONE call, max 4 questions, only for dimensions still unknown. Map every option to technical values silently; the user sees plain Arabic, never jargon.

Primary question set (skip answered ones, keep ≤4):

| # | Question (plain Arabic) | Options → internal mapping |
|---|---|---|
| Q1 | نوع الفيديو؟ | إعلان/تسويق → tight pacing, product hero · قصصي/سينمائي → narrative beats · موشن جرافيك/تكست → motion typography, flat design · UGC/سوشيال → handheld, natural, authentic |
| Q2 | هيتعرض فين؟ | TikTok/Reels/Shorts → 9:16 · YouTube/عرض → 16:9 · إعلانات/لاندينج → 16:9 (+4:5 crop note) · مش متأكد → 16:9 default |
| Q3 | المدة؟ | 5 ثواني → single shot, 1-2 beats · 10-15 ثانية → multi-shot timecode, 3-4 beats · أطول → suggest 10s + extension workflow |
| Q4 | الصوت؟ | صامت → no audio fields · موسيقى بس → music genre/mood only · مؤثرات+محيط → SFX+ambience · حوار/voiceover → dialogue block |

Conditional second call — ONLY when still ambiguous after Q1-Q4:

| # | Question | Options → mapping |
|---|---|---|
| Q5 | إحساس الكاميرا؟ | ثابتة locked-off · حركة واحدة سلسة (default: slow push-in) · handheld طبيعي · مبهرج (orbit/crane/crash zoom) |
| Q6 | كراكتر/مرجع؟ | Dynamic: list `characters/*-char.md` names (max 4 options) + "كراكتر جديد" + "مفيش" |

Rules:
- Max 2 `ask_user_question` calls total. Prefer 1.
- If a character name is already in the message, skip Q6 — resolve via the Character Library (§4) and only confirm if ambiguous.
- If the user gives a detailed brief up front, skip the interview entirely and go straight to assembly.

## 3. Prompt Assembly

Order of layers (all optional except subject+action; more layers = more control):

`[shot type + framing] + [subject doing action] + [setting/context] + [camera movement + speed + purpose] + [lens/focus] + [lighting/atmosphere] + [style anchors ≤3] + [audio layers] + [technical specs]`

Golden rules (violating these is the #1 cause of bad output):

1. Every camera move gets a speed or duration: "slow dolly push-in over 4 seconds" — models have no default speed.
2. One main subject + one main action per shot. Sequential beats, not simultaneous.
3. Join subject motion and camera motion with a relationship verb: "camera follows", "truck left matching her pace".
4. Describe what enters frame at each phase instead of stacking movement verbs.
5. Dolly ≠ zoom: dolly = camera physically moves, background shifts; zoom = lens magnifies only.
6. Never use empty intensifiers alone: "cinematic", "dynamic camera", "4K", "beautiful" do no work — replace with named shot/lens/light.
7. Clip duration must cover the event — extra time gets filled with invented motion.
8. Prompts are in ENGLISH (models understand it best); explanations to the user are in Arabic.
9. Audio: prompt all 4 layers (dialogue, ambience, SFX, music) or explicitly state silence — unstated audio gets hallucinated (e.g., fake studio audience).
10. Dialogue: colon syntax `says:`, keep it short enough for the clip length, add `(no subtitles)`; repeat if needed.
11. Negative prompts are model-specific — see `references/model-formats.md` §negatives. Never assume a dedicated negative field exists.
12. Style anchors: max 2-3 film/director references; more dilutes.

Multi-shot (duration ≥10s or user wants sequence): timecoded blocks `[0-4s] … [4-9s] …`, each with shot+camera+action+light; transitions named explicitly ("hard cut to", "seamless morph into", "whip pan to"). Escalation pattern wide → medium → close-up → extreme close-up maps naturally to ~15s.

Vocabulary: full tables in `references/prompt-anatomy.md`. Per-model syntax/templates in `references/model-formats.md`.

## 4. Character Library

Canonical store: `characters/` at the aiZee root (global, works across projects — resolve via `config.discover_root()`, never a hardcoded path).

Convention — user's `-char` suffix design, refined:

```
characters/
├── README.md            # convention doc
├── _template-char.md    # copy this to create a character
├── sara-char.md         # THE SHEET — frontmatter + canonical description
└── sara-char/           # ASSETS folder (same basename)
    ├── ref-front.png    # reference images for image-to-video / character refs
    └── ref-full.png
```

- `*-char.md` = registry. Glob `characters/*-char.md` lists every character.
- `*-char/` = that character's reference assets (images/video/audio).
- Frontmatter `aliases:` carries Arabic + English names so "سارة"/"sara"/"Sara" all resolve.
- The sheet contains ONE block marked `VERBATIM:` — the canonical English character description. Paste it word-for-word into every prompt (verbatim repetition is what holds identity across clips). Never paraphrase it per-generation.
- Sheet also holds: voice/speaking style, palette, signature details, usage notes.

Runtime protocol:
1. User mentions a character (any alias) → glob + match → load sheet.
2. Inject VERBATIM block into the prompt's subject layer; list asset paths if the target model accepts references (`[Image1]` syntax where supported).
3. Name not found → offer to create a sheet: ask for 2-3 visual details (shape/build, palette, one signature detail) + optional voice, write `*-char.md` from `_template-char.md`, confirm with user before saving.
4. Multiple alias matches → ask which (MC if ≤4, else text list).

## 5. Output Contract

Every delivery contains, in order:

1. **The prompt** — one copyable code block, English, assembled per the target model's format (`references/model-formats.md`). If no model specified, produce the universal 7-layer prose form.
2. **AR explanation** — 2-3 lines in Egyptian Arabic: what choices were made and why (aspect ratio, shot structure, camera, audio).
3. **Alternate** — one variant (safer or bolder) unless the user asked for options upfront.
4. **Params note** — aspect ratio / duration / resolution / audio toggle are API/UI params, NOT prompt text; state them explicitly so the user sets them correctly.
5. **Refs used** — list character sheets/images injected, if any.
6. **Production handoff** — if the user wants the video MADE (not just the prompt), continue into `video-produce` with the approved prompt as input; state the chosen path in one line.

## 6. Iteration & Cost Discipline

- Default to ONE strong prompt, not a barrage. Offer alternates only on request or when ambiguity was high.
- If a generation fails: simplify first (freeze camera, reduce action, clear background), then add complexity back — one change per iteration.
- Multi-model workflow hint when relevant: cheap model for exploration (5-10 variations), premium model for final (5-10-1 rule).
- Never invent model names, parameter names, or resolution values — if unsure of a model's current specs, say so or check official docs.

## 7. Presets (user-defined modes)

Named routes the user can invoke by name. A preset selects the PRODUCTION path — hand off to `video-produce` after the prompt/brief is approved:

- `bang-motion` — browser motion graphics: opener/promo/knetic-type/explainer as a single `index.html` (GSAP+Three.js, anti-PPT rules, style brief → 3 concept candidates → approval → build → `export-frames.mjs` MP4). Kit: `~/.aizee/media/kits/bang-motion/`.
- `cinecode` — coded film: idea → MP4 via `film.html`/three.js/Web Audio. Quick mode (~3 min, one file) or Film mode (6 gated steps). Kit: `~/.aizee/media/kits/cinecode/`.
- `motion-graphics` — deterministic WebGL+Canvas2D engine, real motion blur, multi-format safe zones, generative clip adapters. Kit: `~/.aizee/media/kits/motion-graphics/`.
- `motion-design` — seek(t) single-file engine, synthesized score on the beat grid, parallel-chunk render, critic pass. Kit: `~/.aizee/media/kits/motion-design/`.
- `hyperframes` — HTML compositions → deterministic MP4 via `npx hyperframes` (check/snapshot/review/render loop, registry blocks).

When the user names a preset, route via `video-produce`; the kit's own SKILL.md then drives its interview. If a kit is missing on the device, say so and offer the fallback path rather than guessing.

[PROHIBIT]
1. No prompt delivery without at least subject + action + one camera instruction.
2. No asking the user to supply film terminology — translate, don't delegate.
3. No more than 2 interview calls; no re-asking answered dimensions.
4. No verbatim character description edits — paste the sheet block unchanged.
5. No fabricated model specs (aspect ratios, durations, parameter names) — use `references/model-formats.md`, which is sourced from official docs; flag anything uncertain.
