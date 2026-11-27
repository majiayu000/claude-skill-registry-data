---
name: video-studio
description: "Make a short video or ad like a small studio: Producer, Writer, Director, Sound, Editor, Motion and a harsh Critic, each its own agent. Use for any TikTok, Reel, Short, promo or ad."
---

# Video studio

yskills, 2026-10-17: videos and ads are made "like a professional studio, everyone with their own
tasks and skills". Seven roles, one pipeline, one gate. Free, licence-clean tools first; anything
paid waits for yskills' card (CLAUDE.md, ask rule). Checked 2026-10-17; sources in
`docs/research/2026-10-17-video-studio.md` (`claude-setup/docs/research/2026-10-17-video-studio.md`).

Before anything else, every role reads [`learnings.md`](learnings.md): what earlier videos got
wrong and how they were fixed.

## The pipeline

| # | Step | Role | Output (in the project's `video/<slug>/` folder) | Gate |
|---|---|---|---|---|
| 1 | Brief | Producer | `BRIEF.md` from [`templates/brief.md`](templates/brief.md) | |
| 2 | Three concepts | Writer (Producer recommends) | three pitches, each with a first-frame still from the real product | **card**: yskills picks one |
| 3 | Script | Writer | hooks and `script.md`: hook, tension or turn, payoff; two columns with time ranges; `references.md` (2-3 top videos in the niche) | |
| 4 | Board | Director | `storyboard.md` (one still per shot from the real product, with timing, camera and sound cue), `animatic.mp4` (stills on the script's timing) | Critic on the animatic |
| 5 | Sound plan | Sound | `sound.md`: music bed with source and licence, beat map, SFX cue sheet on the cut points, per the preset in [`sound-kit.md`](sound-kit.md) | |
| 6 | Film and cut | Editor | raw capture, cut to the beat map, captions, grade, `draft.mp4` | |
| 7 | Motion and mix | Motion, Sound | titles, end card, transitions, overlays; then the mix and both masters | |
| 8 | Gate | Critic (fresh) | `critic.md`: scores against the references, pass or fail | pass before yskills sees it |
| 9 | Deliver | Producer | runs `python3 "${SKILL_DIR}/scripts/ready.py" video/<slug>` (non-zero means stop); `final.mp4`, `final-nomusic.mp4` (+ ad variants), the one line to the coordinator | to the `social-team` queue |

Fixing the animatic costs minutes; fixing a filmed cut costs a render. So the Critic sees step 4
before anything is filmed, then the cut at step 8. A failed gate goes back to the step that owns
the fault, never straight to yskills.

`SKILL_DIR` (step 9) is the absolute directory holding this SKILL.md.

Hard rules (T1, 2026-10-18: one agent played the whole team and graded itself; yskills: "would you
pay 10k dollars for that?"):

- **Each role is its own agent.** The Producer never collapses roles into one agent and never
  writes the concept or script into a brief: the Writer writes it.
- **The Critic is always a fresh agent** that made nothing it grades.
- **No step without its file.** The script, `storyboard.md`, the animatic's Critic pass and
  `sound.md` exist before the cut starts. Anything missing means stop and go back to its owner.
- **`ready.py` decides delivery**, not the Producer's word: it fails without the script, the
  board's stills, the music licence and the Critic's passes with their reference videos.

## Explainer format (Miso, 2026-10-24)

**Miso look REJECTED (yskills, 2026-10-24: "looks shit"; final taste call).** The cream cat, mint scarf and flat toon world never come back as a style. Only the pipeline below is kept (script, voice, word times, frames, encode); a new video gets a new look from the Designer's art direction and yskills' reference clips.

The test build behind this pipeline copied a viral TikTok explainer's format (recurring character, word-by-word captions on the beat); its look is rejected (above). [`templates/explainer/`](templates/explainer/README.md): `script.json` (title, scenes with `visual` and `text`) → `build.py` (Piper voice, word times from faster-whisper) → `render.mjs` (Playwright frames + ffmpeg) → 1080x1920 `video.mp4`, no video model, ~35 s to render 18 s. The test build's mascot and visuals (`mascot.js`, `visuals.js`, `sky.json`) are the rejected look: replace them per the new art direction, keep the code structure. Free and local; background music is optional (`music.*` in the out folder, licence in `sound.md`). It still goes through the pipeline's script, board and Critic steps before anything is posted. Style source and the other 28 videos: `docs/research/2026-10-24-video-batch.md`.

## Roles

| Role | Does | Playbook | Runs as |
|---|---|---|---|
| Producer | brief, the concept card, schedule, delivery; owns the whole video | [`roles/producer.md`](roles/producer.md) | the video's thread: `Producer · <video>` |
| Writer | hooks, script, captions, voice lines, ad variants | [`roles/writer.md`](roles/writer.md) | subagent of the Producer; a thread for an ad batch |
| Director | shot list, camera, storyboard stills, animatic | [`roles/director.md`](roles/director.md) | subagent of the Producer |
| Sound | music bed and licence, beat map, SFX, mix, loudness, both masters | [`roles/sound.md`](roles/sound.md) | subagent of the Producer; mixes in the Editor's thread |
| Editor | capture, cut, captions, grade, encode, frame check | [`roles/editor.md`](roles/editor.md) | thread `Editor · <video>` (renders are long) |
| Motion | the "After Effects" job: titles, end cards, kinetic text, transitions, overlays | [`roles/motion.md`](roles/motion.md) | subagent of the Editor; a thread for a template set |
| Critic | the harsh first viewer; never made what it grades | [`roles/critic.md`](roles/critic.md) | a fresh subagent of the Producer (`docs/TEAMS.md`, Film) |

Thread titles follow the operator rule (`<Role> · <what>`). Text roles stay subagents because every
thread re-reads its context; Editor gets a thread because filming and encoding run long. Models: the
role rows in `docs/TEAMS.md` (`claude-setup/docs/TEAMS.md`) (Film).

## Tools (one pick per job)

| Job | Pick | Notes |
|---|---|---|
| Footage of our own web app or game | Playwright, deterministic frame stepping | the recipe in `learnings.md`; real-time capture in the cloud stutters |
| Cut, captions, loudness, encode | ffmpeg | `media-editing` skill recipes |
| Transcript of a voice memo | faster-whisper | `media-editing` |
| Motion graphics, titles, kinetic captions | **HyperFrames** (HeyGen, Apache-2.0, HTML + GSAP to MP4) | the cloud's After Effects; `toolbox` `catalog/video-audio.md` |
| Same in a React project | **Remotion** with its official skills (`npx skills add remotion-dev/skills`) | licence: free for teams of up to 3 people |
| Watch a reference video yskills shares | `watch` skill | frames, transcript and edit timeline (cuts, beats, silences), free; a Take about look goes to `ui-review/TASTE.md` (one dated line), a video-format Take to `learnings.md` |
| After Effects itself | only on yskills' PC, only if they already own it | community MCP servers exist (e.g. `Dakkshin/after-effects-mcp`), not tried: read it first (install rule in `toolbox`) and ask by card |
| yskills saying lines he did not record | `twin` skill (his voice clone + his real face, mouth re-synced, on the laptop) | a failed twin shot means real footage; its Critic lines are in the `twin` SKILL.md |
| AI clips, AI voice, stock music | fal.ai, ElevenLabs | money and a new service: card first; AI people or voices need the AI label (`market` §4) |

Sold "Claude skill packs" from Instagram or Gumroad are prompt lists, not workflows: never bought.
Skim a free one only if it names something this table lacks.

Shot lists and scripts for the mascot-explainer, POV-magic and blockout-to-AI-video formats: [`formats.md`](formats.md). Prompt and script library: [`prompts.md`](prompts.md). People and POV video (free, cheap, paid tiers): [`people-video.md`](people-video.md). Cloud Blender (cloud first, estimate, starter scripts, measured times): [`templates/blender-cloud/`](templates/blender-cloud/README.md); cloud Blender POV scripts: [`templates/blender-pov/`](templates/blender-pov/README.md). Real Y-Land footage with real followers, plus a face cut-in in yskills' style: [`templates/yland-film/`](templates/yland-film/README.md). Fast, free launch or update promo from any repo in the product's own look (/brag + HyperFrames), not for his face-first posts: [`templates/launch-video/`](templates/launch-video/README.md). Answers-only rapid Q&A, solo phone shoot: [`templates/rapid-qa/`](templates/rapid-qa/README.md).

## Every video

- **Real product, real footage.** The video shows what the app really does; mocked UI or AI-made
  product shots are a fail.
- **Phone first.** 1080x1920, 30 fps, captions in the top band away from TikTok's right-side and
  bottom UI; one caption at a time, 3-5 words.
- **Sound.** Every video gets sound design and two masters, scaled by its preset ([`sound-kit.md`](sound-kit.md): presets, cut-on-beat, free library, `scripts/sound.py`); the role:
  [`roles/sound.md`](roles/sound.md). yskills' own voice memo when the concept needs a voice (exact lines from the Writer).
- **Ads.** Label and claims per `market` §4 (German advertising law); three hooks on one body so the
  ad can be tested; paying for ads is yskills' card.
- **Never posted by the studio.** `final.mp4` goes to the `social-team` queue; it posts per its Posting rules (`social-team`, Posting: personal account vs project accounts).
- **Lessons stick.** After delivery the Producer appends what went wrong and the fix to
  `learnings.md` (one line each, dated, project named) in the same PR flow as any setup change.
