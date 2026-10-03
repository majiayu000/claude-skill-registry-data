---
name: model-routing
description: >
  Choose the best Renoise image, video, or audio model and write prompts for it.
  Always use before any Renoise generation estimate or task, and when the user
  asks for the best model, model comparison, model routing, which model to use,
  or “用哪个模型 / 模型选择”. Use alongside the active generation workflow;
  this Skill does not execute tasks.
user-invocable: false
metadata:
  author: renoise
  version: 0.3.1
  category: media-generation
  tags: [model-routing, prompting, image, video, audio, portable]
---

# Renoise Model Routing

Select by task, not by habit. Then prompt for the selected model instead of sending every model the same generic brief.

## Hard Boundary

Live model capabilities are authoritative for availability, defaults, input roles, combinations, limits, duration, ratio, resolution, and audio controls. This Skill contains only researched routing preferences and prompting styles.

1. Preserve a model explicitly named by the user.
2. Filter candidates by the live capabilities required by the task.
3. Route only to the newest live generation of a model family; older generations remain available only when the user explicitly names one.
4. Choose the best specialist below.
5. Use the live `isDefault` model only when no specialist clearly fits or candidates tie.
6. Inspect the selected model's live guidance before writing the final prompt.
7. Let the selected model's profile override generic prompt-craft advice when prompt structure, density, or reference wording conflicts.
8. Never pass a role or parameter merely because this guide mentions a public model capability; the Renoise deployment may expose a narrower contract.

Live availability alone is not a routing recommendation. Omit older generations, fully dominated models, and models without a clear task advantage; an explicitly named model still follows rule 1.

## Routing Questions

Classify the request before selecting:

- **Kind:** image, video, or audio.
- **Operation:** create, edit, continue, interpolate, animate a reference, or upscale.
- **Priority:** final quality, strict instruction following, aesthetics, identity consistency, speed, or cost.
- **Structure:** exact text/layout, one cinematic shot, multi-shot narrative, dialogue performance, music, or a complete audio scene.
- **References:** none, one source image, several identity/style references, source video, endpoint frames, or voice/audio references.

Do not call a model “best” without naming the task it is best for.

# Image Routing

## Decision Order

| Task | Prefer | Why |
|---|---|---|
| Exact text, UI, diagrams, ads, packaging, compositing, identity-sensitive image-to-image work, or peak final quality | `gpt-image-2.5-sunburst` | Route a generic GPT Image 2.5 request here; use `gpt-image-2.5-flare` when explicitly requested. Image references guide transformations, but neither variant exposes mask inpainting. |
| General high-quality photorealistic or commercial image | live image default | Start with the deployment's current default when no specialist better fits; do not infer local-edit or typography guarantees from the model family. |
| Fast, inexpensive drafts and simple variants | `nano-banana-2-lite` | Lightweight Google-family tier when its live output resolution is enough; it may still accept several references. |
| Balanced Google workflow, extreme aspect ratios, several references, multilingual localization, or conversational iteration | `nano-banana-2` | Google-family workhorse balancing quality, latency, text, reference reasoning, and broad formats. |
| Maximum Google-family world knowledge, brand consistency, localization, or reasoning-heavy composition | `nano-banana-pro` | Specialist for intricate professional assets and precise spatial relationships. |
| Aesthetic exploration, stylized art direction, editorial mood, or concept art | `mj-v8.2` | Current Midjourney generation and strong aesthetic prior. |
| Seedream output resolution or image-reference count beyond what the live Pro contract accepts | `seedream-5-0-lite` | Choose Lite when its advertised limits fit and Pro's do not; otherwise use the live default for general Seedream work. |
| xAI image request | `grok-image` for lower-cost iteration; `grok-image-quality` when higher quality justifies the added cost | Both support direct natural-language generation and editing through the live Renoise contract. |

## Image Prompting Styles

### GPT Image 2.5 — production brief

For complex production briefs, use labeled, ordered instructions:

```text
USE: [ad / packaging / UI / infographic / edit]
SCENE/BACKGROUND: ...
SUBJECT: ...
COMPOSITION: ...
LIGHTING/MATERIALS: ...
EXACT TEXT: "..." with placement, hierarchy, font character, and color
PRESERVE: identity, geometry, layout, logo, and all unmentioned elements
CHANGE ONLY: ...
AVOID: ...
```

- Route a generic GPT Image 2.5 request to Sunburst; use Flare when explicitly requested. Neither live contract supports mask inpainting.
- Put literal in-image text in quotes and specify hierarchy and placement.
- For image-to-image transformations, say **change only X; preserve everything else**.
- Identify every reference by its job: source, identity, product, layout, or style.
- Prefer one-change iterations over rewriting the whole brief; do not promise mask inpainting.

### Nano Banana family — conversational creative direction

```text
[Subject] + [action] + [location] + [composition] + [style]
Camera/viewpoint: ...
Lighting/materials: ...
Exact text: "..."
Keep unchanged: ...
```

- Start with a clear operation verb and use positive, concrete natural language.
- For references, state each source's job, the relationship among them, and the new scenario.
- For edits, separate the requested change from what remains unchanged; repeat preservation requirements on later turns.
- Quote exact visible copy and specify its hierarchy, placement, visual character, and localization target.
- Nano Banana 2: relate multiple references explicitly and iterate conversationally.
- Lite: keep one clear composition and few dependencies rather than relying on long multi-turn edits.
- Pro: state brand invariants, localization requirements, and complex spatial relationships precisely.

### Seedream 5 — design brief

Put the deliverable format first, then subject, layout, light, exact text, and invariants:

```text
[DELIVERABLE FORMAT and ratio/use case]
Subject and setting: ...
Layout and spatial relationships: ...
Lighting, materials, and palette: ...
Exact visible copy: "..."
Keep exactly: ...
```

- Pro: specify dense layout, multilingual copy, materials, local edit regions, and everything the edit preserves.
- Lite: natural language works well; make causal/spatial relationships explicit for complex transformations.
- Assign each reference a clear role and avoid vague pronouns in multi-reference edits.

### Midjourney — aesthetic visual phrase

Use a concise visual description, not a requirements document:

```text
[subject], [medium], [environment], [lighting], [palette], [mood], [composition]
```

- Prefer concrete visual nouns and adjectives over keyword spam.
- Name the lighting and composition that matter instead of relying on “cinematic.”
- Use Midjourney for look development rather than text-heavy layouts or surgical edits.

### Grok Imagine Image — concise scene direction

```text
[subject doing action] in [setting], [camera/framing], [lighting], [material/style]
```

- Use standard for lower-cost iteration and Quality when the higher-quality tier is worth the added cost.
- For edits, attach the source image or images and describe the requested change directly.
- Keep the prompt concrete enough that the main subject and action remain dominant.

# Video Routing

## Decision Order

| Task | Prefer | Why |
|---|---|---|
| General multimodal video, continuous 16–30 second sequences, rich mixed references, source-video edits, or forward/backward extension | `seedance-2.5-byteplus` | Newest Seedance generation and the long-form, reference-heavy specialist with precise edit/extension workflows. |
| Short 720p generation, text rendering, or source-video edit within its narrow live contract | `gemini-omni-flash` | Strong short-form instruction following, multi-shot generation, and conversational editing. |
| H3-family 2K delivery, high-fidelity endpoint control, or focused multimodal references | `hailuo-h3` | Full-quality tier with image/video/audio references; choose it when Max's live contract cannot meet the task. |
| Fast H3-family text-to-video, first/last-frame, or reference-to-video with image/video/audio sources | `hailuo-h3-max` | Faster multimodal tier when its live quality and resolution fit; suitable for source-video variants without discarding the source. |
| Fastest, lowest-cost H3-family text-to-video or first/last-frame generation without generic references | `h3-max-turbo` | Turbo supports text and endpoint frames, not reference image/video/audio inputs; use H3 Max or H3 for references. |
| xAI one-image animation with native sound | `grok-video-1.5` | Newest Grok video generation; the current Renoise contract requires exactly one input image. |
| Upscale an existing video without changing its content | `upscale-video-topaz-starlight-2.5` | Dedicated restoration/upscaling model; use a generation or editing model when objects, motion, timing, or style should change. |

### Tier and version notes

- Within the H3 family, use full H3 when its higher-quality output or 2K matters; choose H3 Max when speed/cost matters and its live image/video/audio reference roles, combinations, and output quality fit. Turbo is the text/first/last-frame budget tier, not a generic reference mode. A source video needs `reference_video`; `first_frame` alone is not equivalent.
- Grok's public upstream capabilities may move faster than Renoise's contract. Route from live roles and limits rather than assuming an upstream feature is connected.
- Model preference leaderboards are task-, resolution-, and audio-filter-specific; use them as volatile evidence, not a single aggregate ranking.

## Video Prompting Styles

### Seedance 2.5 — multimodal director brief

Assign each reference an explicit job, then write shots:

```text
References:
- @material:<ID>: subject identity
- @material:<ID>: location/style
- @material:<ID>: motion/camera/voice

Shot 1: framing, subject action, camera move, environment, sound/dialogue.
Shot 2: ...
Continuity: traits and objects that must remain unchanged.
Constraints: no subtitles/logo/watermark unless requested.
```

- Use a few stable identity features rather than an exhaustive biography.
- Give each beat a clear camera behavior; avoid simultaneous conflicting moves.
- Describe body part, speed, force, and physical consequence for actions.
- Externalize emotion through visible behavior and direct dialogue/audio explicitly.
- Begin with the intended result, map every reference to its purpose, then use non-overlapping timestamp ranges or numbered shots with continuity notes.
- For a source-video edit, name the source, the intended change, its time range when relevant, and what remains unchanged.
- For extension, state forward or backward direction and describe the visual, motion, and audio continuity across the source boundary.

### Gemini Omni Flash — conversational generation/editing

- For creation: write a direct natural-language brief with subject, action, camera, setting, visible text, and desired audio.
- Gemini readily creates multi-shot clips; say “single continuous shot,” “single unbroken scene,” or “no scene cuts” when continuity is required.
- Use natural time phrases or `[0–3s]` blocks for important beats.
- For editing: identify the source, say **change only X**, and list what remains unchanged.
- Make one edit per turn when possible; use follow-up refinement rather than replacing the entire prompt.

### MiniMax H3 family — mode-specific audiovisual plan

Choose one mode that the selected model exposes. Full H3 and H3 Max can use generic reference mode when their live roles allow the specific image/video/audio mix; H3 Max Turbo supports text and first/last-frame modes, not generic references. Frame and reference roles are separate modes — do not combine them unless the selected model's live guidance explicitly permits it:

- **Text-to-video:** state the subject, action over time, camera movement, setting, lighting, and sound intent directly.

- **First frame:** describe only the motion, camera path, action development, and sound after the supplied opening state.
- **Last frame:** describe the plausible path that converges on the supplied ending.
- **First + last:** describe the continuous transition between states; avoid re-describing the two stills. Prefer one coherent shot unless a cut is essential.
- **Reference mode (H3 / H3 Max when live):** assign each image, video, and audio an explicit identity, motion, style, voice, action, or sound job. Attach the authorized source video directly when its motion/timing matters, and check the selected model's live duration and role-combination limits.

For complex reference work use:

```text
References: each @material:<ID> image/video/audio and its job.
Task summary: target result and what each source contributes.
Preserve: identity, motion, voice, style, or content that carries over.
[Shot 1] Visual action, camera motion, dialogue, and diegetic sound.
[Shot 2 at time] Cut and continuation.
Overall soundscape: ambience, Foley, and non-verbal sound.
Non-diegetic music: instrumentation, tempo, dynamics — or none.
```

Specify camera **type + amplitude + speed** only when they matter. Keep dialogue exact, label speakers consistently, and separate in-scene sound from background score.

### Grok Imagine Video — animate the change

For image-to-video, do not re-describe the static source:

```text
[subject motion/change], [one camera move], [atmosphere/lighting change].
Sound: specific dialogue/SFX/ambience; no music if unwanted.
```

- Use one primary action or a short causal sequence and front-load the important motion.
- Attach exactly one input image and describe the change from that starting frame.
- Give the attached image a clear visual or motion job.
- Request dialogue, effects, ambience, or music explicitly when native audio matters.

### Topaz Starlight — no creative prompt

Upscaling is not regeneration. Supply only the source video and settings required by the live capability; do not add a creative prompt or unrelated media inputs. If the user wants content changed, route to a video editing model instead.

# Audio Routing

| Task | Prefer | Why |
|---|---|---|
| Short song excerpt, instrumental, loop, preview, score cue, or music bed | `lyria-clip` | Dedicated 30-second music model for rapid iteration, social assets, and background cues. |
| Dialogue, expressive narration, podcast, dubbing/re-voicing, SFX/ambience, or a complete sound scene | `seed-audio-1.0` | Unified speech, dialogue, effects, and ambience generation; live default audio model. |

Neither broadly replaces the other: Lyria composes short music clips; Seed Audio handles speech-led and complete sound scenes.

## Lyria 3 Clip — composer brief

```text
Genre/style: ...
Mood: ...
Instrumentation: ...
Tempo/rhythm: ... BPM
Vocals: instrumental OR voice type, delivery, and language
Lyrics/theme: exact lyrics or subject
Structure over ~30 seconds: intro → development → ending
Production: mix character, era, space, dynamics
```

- Explicitly say **instrumental** when vocals are unwanted.
- Name instruments, tempo, vocal range/texture, backing vocals, and language.
- Keep custom lyrics concise for 30 seconds; `Lyrics:`, `[Verse]`, and `[Chorus]` can clarify structure.
- Use timestamps only for meaningful structural changes; musical alignment follows bars rather than sample-accurate timing.
- Describe genre, era, instrumentation, and production traits instead of requesting a named artist imitation.
- Use an optional guide image only when the live material roles expose it.

## Seed Audio 1.0 — sound-scene script

```text
Setting/acoustics: ...
Continuous sound bed: ...
Speaker A (age, accent, timbre, emotion, pace): "Exact line."
Action-tied SFX: ...
Speaker B (...): "Exact line."
Music cue and ending: ...
```

- For full-scene work, direct it as a scene; for speech-only work, specify voice identity, performance, pacing, and acoustics.
- Label speakers and exact lines; match prompt language to dialogue language.
- Use clean authorized voice references, or an authorized character image for inferred voice, according to the mutually exclusive live reference modes.
- Use concrete Foley and ambience; onomatopoeia can clarify transient sounds.
- Use precise timing for dialogue; describe SFX, ambience, and music timing approximately unless live guidance says otherwise.

# Research Basis

Reviewed 2026-09-26 against live Renoise model contracts. Rankings are directional and decay quickly; live capabilities and task-specific tests override them.

Primary guidance:

- OpenAI GPT Image: https://openai.com/index/introducing-chatgpt-images-2-5/, https://developers.openai.com/api/docs/models/gpt-image-2.5-flare, https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst, https://developers.openai.com/api/docs/guides/image-generation, and https://developers.openai.com/cookbook/examples/multimodal/image-gen-models-prompting-guide
- Google Gemini image: https://ai.google.dev/gemini-api/docs/image-generation and https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-nano-banana
- Midjourney prompting/version docs: https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics, https://docs.midjourney.com/hc/en-us/articles/32199405667853-Version, and https://updates.midjourney.com/version-8-2/
- ByteDance Seedream: https://seed.bytedance.com/en/blog/deeper-thinking-more-accurate-generation-introducing-seedream-5-0-lite and https://seed.bytedance.com/en/blog/beyond-generation-it-understands-design-introducing-seedream-5-0-pro
- xAI Imagine image/video: https://docs.x.ai/developers/model-capabilities/imagine and https://docs.x.ai/developers/model-capabilities/video/generation
- BytePlus Seedance 2.5 and 2.0 prompt guides: https://docs.byteplus.com/en/docs/ModelArk/2607689 and https://docs.byteplus.com/en/docs/ModelArk/2222480
- MiniMax H3 family: https://www.minimax.io/blog/minimax-h3, https://platform.minimax.io/docs/guides/video-generation, https://huggingface.co/MiniMaxAI/MiniMax-H3/tree/main/docs, and https://blog.fal.ai/introducing-h3-max-by-fal/
- Topaz Starlight Precise 2.5: https://developer.topazlabs.com/video-models/starlight/starlight-precise-2.5
- Gemini Omni: https://ai.google.dev/gemini-api/docs/omni
- Lyria: https://ai.google.dev/gemini-api/docs/music-generation, https://deepmind.google/models/lyria/prompt-guide/, and https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-lyria-3-pro
- Seed Audio: https://seed.bytedance.com/en/blog/from-speech-to-audio-creation-introducing-the-seed-audio-1-0-audio-creation-model and https://docs.byteplus.com/en/docs/byteplusvoice/seedaudio-01
- Independent preference evidence: https://artificialanalysis.ai/image/leaderboard/text-to-image, https://artificialanalysis.ai/image/leaderboard/editing, https://artificialanalysis.ai/video/leaderboard/text-to-video, https://artificialanalysis.ai/video/leaderboard/image-to-video, and https://artificialanalysis.ai/video/leaderboard/video-editing
