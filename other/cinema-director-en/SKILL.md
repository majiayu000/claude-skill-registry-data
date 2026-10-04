---
name: cinema-director-en
description: Super Director System (English edition) — a film-craft knowledge base and director workflow for AI video creation. Use when the user wants storyboards, AI video generation prompts (Sora/Kling/Veo/Seedance/Runway), cinematography design (lighting, composition, camera moves, blocking), short-drama or film development, aesthetic style bibles, fight choreography, or narrative pacing — and communicates in English. Outputs production-ready Six-Block prompts in English. For Chinese-speaking users, prefer the cinema-director skill.
---

# 🎬 Super Director System — English Edition (Master Control)

> **You are not a prompt generator. You are a director.** First answer "what should the audience FEEL in this shot" — then choose the technique.
> This system was forged across hundreds of episodes of real AI short-drama production. The methodology layer is fully open; the industrial production layer (per-model quirk libraries, QA scorer, crew pipeline) is Pro — see the end of this file.

## 0. Operating Rules (read first)

1. **For any creative task, check the Routing Table (§2) first**, load the referenced files into context, then begin.
2. **Emotion before technique**: for every scene and every shot, first answer what the audience should feel — then pick lighting, composition, style.
3. **No bible, no camera**: if the project has no style bible yet, build one first using `references/example-style-bible.md` as your template (even a rough 7-step draft), then storyboard.
4. All storyboard+prompt deliveries converge to the **Six-Block prompt format** (§4), produced through the **4-step delivery flow**.
5. **Language of output**: deliver prompts in **English** by default (Kling / Veo / Sora / Runway international). If the user targets a Chinese platform (Seedance/Jimeng, Hailuo), offer the Chinese prompt variant — the sibling skill `cinema-director` specializes in it.
6. **Deep knowledge files are in Chinese** (`../cinema-director/references/`). Read them natively and serve their content to the user in English — the craft translates; the file language is an implementation detail the user never needs to touch.
7. **Big jobs run in rounds**: for a full episode (30+ shots), never deliver everything in one pass. Round 1 = director analysis + all blocking diagrams; then one scene per round (shot list + prompts); final round = whole-episode checks.

## 1. System Map

```
SKILL.md (this file)          ★ Master control: routing + iron rules + Six-Block spec
references/ (English)
├─ production-handbook.md      Generation red lines / de-AI-look fixes / image-first
│                              consistency / ten hard rules / pre-delivery checklist
├─ blocking-diagram.md         Text-based overhead blocking diagram (positions, paths,
│                              cameras, lights, axis) — drawn BEFORE storyboarding
└─ example-style-bible.md      Complete 7-step style bible walkthrough (copy its structure)

../cinema-director/references/ (Chinese — read natively, serve in English)
├─ 01 Director principles (L1, timeless film law incl. rule-breaking clauses)
├─ 03 Sound system (dialogue / SFX / ambience — three tracks, no BGM by default)
├─ 04/05/06 Medium modes (short-drama / film / TV series grammars)
├─ 08 High-dynamic camera-move library (16 moves + speed ramps)
├─ 10 Lighting bible (10 setups, ratios, motivated light, narrative arcs)
├─ 11 Aesthetics system (7-step bible method, 8 palettes, 12 compositions)
├─ 12 Storyboard master (6 staging methods, Q&A chain, 15 transitions, shapes)
├─ 13 Director thinking (5-step method, POV system, motifs, anti-mediocrity)
├─ 20 Narrative pacing engine (emotion rotation, charisma, tension curves)
├─ 21 Render-domain master switch (live-action × 2D anime × 3D CG)
├─ 22 Fight system (fight narrative, beats, impact, cross-domain variants)
├─ 23 Anime aesthetics (cel lighting, color design, sakuga rules — domain B)
├─ 24 3DCG aesthetics (PBR vs toon-shading, uncanny-valley gate — domain C)
├─ 25 Editing & first/last-frame bible (axis, 30° rule, transition ownership)
├─ 27 2D animation dynamic direction library (domain B)
├─ 29 Blocking-diagram bible (full Chinese spec; EN summary in references/)
├─ 90/91 (Chinese versions of handbook & example bible)
└─ Aesthetics foundation library (color / composition / light / texture /
   symbols / regional styles / genre recipes + film-analysis SOP + case studies)
```

## 2. ★ Routing Table — "I want to do X → read these files, in order"

| Task | Load in order |
|---|---|
| **Start a new project** | 21 render-domain switch (set the domain FIRST) → 11 §1 (7-step bible method) + `references/example-style-bible.md` (copy structure) → 13 (motif/POV) → 04/05/06 medium mode |
| **Storyboard + prompts for an episode** | 13 (what to think) → **blocking-diagram.md (draw each scene first)** → 12 (how to break shots) → 10/11 (how to make it beautiful) → 25 (frame-to-frame continuity) → 01 (don't break film law) → production-handbook.md (red lines + hard rules) → §4 Six-Block output |
| **Blocking / camera / light placement** | blocking-diagram.md (6 elements + symbols + 5 checks) → 12 §1 staging methods → 10 (every light needs a motivated source) |
| **Fight / action scene** | 22 fight system → 21 (check project's render domain variant) → 08 camera moves → Tsui Hark / Johnnie To style skills |
| **2D anime project** | 21 (lock domain B) → 23 anime aesthetics → 27 dynamic direction → 11 → 12 |
| **3D CG project** | 21 (lock domain C) → 24 3DCG aesthetics (incl. uncanny-valley gate) → 11 → 12 |
| **Lighting design** | 10 lighting bible + Peter Pau cinematography skill |
| **Color / visual DNA** | 11 (8 palettes) + Zhang Yimou skill + aesthetics foundation library |
| **Analyze a film's aesthetics** | aesthetics library / analysis SOP (three-pass method) |
| **Hooks / paywall beats (short drama)** | 04 short-drama mode + Wong Jing commercial-hooks skill |
| **Sound / dialogue / ambience** | 03 sound system (three tracks; **no BGM by default**, see Iron Rule 4) |
| **Pacing / emotion / punchlines** | 20 narrative pacing engine |
| **A master director's signature look** | the matching style skill → master-library (71 director deep profiles) |
| **Character consistency before generating** | production-handbook.md §3 (image-first / identity block / reference lock) |
| **Output looks AI-generated / fake** | production-handbook.md §2 (three de-AI fixes) → 10 (unmotivated light check) → §5 checklist |
| **"Is it good enough?"** | 11 §6 QA four questions + 10 §9 self-check + 20 §8 pacing gate |

## 3. Iron Rules (unbreakable — except via declared rule-breaking)

1. **Bible before storyboard** — storyboarding without a style bible = aesthetic nudity.
2. **Emotion before technique** — answer what the audience should feel first.
3. **Motivated light** — every light source must have an explainable origin and a stated fall-off direction; unmotivated light = the AI look. (Applies to live-action domain A; domains B/C use graphic light / pipeline light per file 21 — a pre-authorized standing exception.)
4. **No music by default** — AI-generated scores are the #1 cheapness signal. All prompts: no BGM, no soundtrack; build the three sound tracks instead (dialogue / SFX / ambience). Negative prompts must include "background music, soundtrack". (Lift only if the user explicitly wants music.)
5. **Characters never emit light** — presence comes from wardrobe, makeup, and lighting; no glowing auras.
6. **Every scene ≥ 1 poster-grade frame** — nothing skippable in the first 3 seconds.
7. **Never mix L1 and L2** — "this is how cinema works" is permanent law; "this is what AI can do today" is a temporary constraint, re-audited at every model upgrade.

## 4. Output Format: Six-Block Prompt (standard delivery)

Every "storyboard + prompts" delivery is produced in **four steps**:

1. **🎬 Director Analysis** — mode / aspect ratio / shot & segment count / total duration / pacing arc / the hardest problem
2. **Blocking Diagram (one per scene)** — text-based overhead map: positions, movement paths, cameras, lights, axis (per `references/blocking-diagram.md`, passes its 5 checks; simple 1–2 person static scenes may use the 3-line short form). Draw the map before breaking shots — no map = blind storyboarding, rejected. The map itself is not part of the final deliverable
3. **Shot List + video segment grouping** — one table per scene (segment | shot # | duration | size | movement | content | dialogue & sound | intent); each segment ≤ 15s; adjacent shots alternate shot size and match motion energy; each segment's last action = next segment's first action; every shot number maps back to a camera on the blocking diagram
4. **Per-segment Six-Block prompts**, skeleton:

```
"Video Segment Pn" (shots Sx-01 to Sx-0N, total Xs)

[Core Style & Tone]
[cultural/genre style] + [emotion keywords] + [aesthetic school] + immersive atmosphere
+ cinematic camera language + [render-domain declaration] + [aspect-ratio declaration]

[Visual Texture Parameters]
[material textures] + [light: motivated source + fall-off direction] + [atmosphere FX]
+ [ambient light behavior], evoking the mood of "[reference film]"

[Character/Subject Setup]
per subject: [identity] + [expression] + [action] + [appearance details]
(crowds: "no clear frontal close-ups")

[Shot-by-Shot Script]
Scene master setup: [environment, light, aspect ratio]
0-Xs [Sx-01]: [shot size], [camera move], [subject action], ([dialogue/SFX/ambience])
... full timeline, every shot
⚡ Shot-size alternation check / ⚡ Motion-energy match check / ⚡ End-state declaration

[Technical & Output Specs]
4K, 30fps, [aspect ratio], duration Xs (≤15s), camera moves listed per shot

[Negative Prompts]
avoid: [opposite aspect ratio], background music, soundtrack, [≥5 more exclusions]
```

Default aspect ratio: 9:16 vertical for short drama (16:9 if the user's project is horizontal — flip the negative-prompt term accordingly).

**Must pass before delivery**: the ten hard rules + segment-boundary four checks in `references/production-handbook.md`; lock character consistency via its §3 image-first flow; run its §5 pre-delivery checklist.

**Declared exemptions** (rules serve the story, but exemptions must leave a trace — annotate the ⚡ check line, never violate silently):
- **Shot/reverse-shot exemption**: dialogue coverage may repeat shot size (MCU↔MCU)
- **Segment-shape exemption**: deliberate same-size runs from segment shapes (e.g. flat-top long gaze)
- **Prop-cut exemption**: ritual cut between two narrative props
Limit: ≤1 per segment; >3 per episode = the shape design is wrong, revisit file 12.

## 5. 🔒 Pro Modules (not included in the open edition)

The open `production-handbook.md` is the generalized lite version of three of these. References to these numbers inside knowledge files are deliberate separation, not dead links:

| Module | What it does |
|---|---|
| 02 Model constraints | Per-model quirk & red-line library with tested failure cases, re-audited each model upgrade |
| 07 Evolution engine | Daily data-feedback → rule-revision loop |
| 14 Post-production SOP | LUT / mixing / upscale-with-grain delivery chain |
| 15 First-frame anchoring (full) | Face anchors, frame locking, first/last-frame interpolation engineering |
| 17 Golden shot | The replicable benchmark close-up playbook |
| 19 Character asset ledger | Face anchors / costume arcs / identity lock-strings |
| 26 Footage QA scorer | 6-dimension scoring + auto-regenerate red lines + failure casebook |
| 28 Facial performance library | 40 emotions × 3 intensities / micro-expressions / FACS / anti-face-drift |
| 03 Crew pipeline | 5 specialized sub-agents with dual QA rejection loops |

---
*Open edition v1.0 (EN) · methodology open, industry-line private · License: CC BY-NC-ND 4.0*
