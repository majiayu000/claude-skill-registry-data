---
name: create-video
description: Generate synchronized audio-video locally with MiniMax H3 Turbo on the ROCm GPU. ALWAYS use this skill whenever the user mentions generating, creating, or making animation/video—including 生成動畫、生成影片、製作動畫、製作影片、做動畫、做影片、animate、animation、video、movie、film、short clip—or mentions MiniMax H3, Minimax H3, or Hailuo H3 for video generation. Also use it to animate an image or turn a photo/text prompt into a moving image with sound.
version: 2.1.0
author: Hermes Agent
license: MIT
prerequisites:
  commands: [ffmpeg]
  paths: [~/src/ComfyUI]
metadata:
  hermes:
    tags: [video, generation, ai, minimax, minimax-h3, hailuo-h3, comfyui, text-to-video, image-to-video, t2v, i2v, fl2va, diffusion, audio, animation]
    related_skills: [create-image, create-music, mock-voice, restyle-music]
---

# Create Video — MiniMax H3 (synchronized audio, ROCm)

Generate text-to-video and first-frame image-to-video with MiniMax H3 on the Radeon
8060S/gfx1151 through the persistent ComfyUI service at `http://127.0.0.1:8188`.
MiniMax H3 is the only backend in this skill.

## When to use

Load this skill unconditionally when the request contains **生成動畫**, **生成影片**,
**製作動畫**, **製作影片**, **做動畫**, **做影片**, **animate**, **animation**,
**video**, **movie**, **film**, **short clip**, or asks for **MiniMax H3**, **Minimax H3**,
or **Hailuo H3** moving-image generation.

Use it when:

- The user asks for a generated `.mp4`.
- The user provides a still and asks to animate it.
- The user wants synchronized ambience, SFX, dialogue, or music generated with the video.
- A longer story should be built from several polished 3–5 second H3 segments.
- A 2D anime request needs `/create-image` storyboard assistance before video generation.

## Validated defaults

| Setting | Default |
|---|---:|
| Resolution | 864×480 |
| Frame rate | 24 fps |
| Requested duration | 5 seconds |
| Valid frames | 124 (`17k+5`) |
| Actual duration | about 5.167 seconds |
| Sampler | Turbo v4 step600 EMA |
| Steps | 6 |
| Audio | native 32 kHz stereo, on |
| Typical wall time | about 5m25s |

Use 8 Turbo steps when quality matters more than time. Use the 20-step reference sampler
only for controlled comparisons or a shot that repeatedly fails to reach its endpoint.

## Standard workflow

1. Convert the request into a shared cinematic Shot Map: story beat, shot size, viewpoint
   angle/height, simulated focal length, framing/depth of field, viewpoint movement, subject
   movement, continuity constraints, environmental progression, sound, and intended join.
2. For 2D anime, create horizontal storyboard/keyframe images with `/create-image`, passing
   `--output-size` equal to the planned H3 video resolution (normally `864x480`).
3. Verify each PNG's pixel dimensions exactly match the video canvas, then show storyboard
   stills to the user and obtain visual approval before expensive generation.
4. Give each H3 segment one main character action and one environmental progression.
5. Generate one 3–5 second segment at a time.
6. Chain longer stories using motion context when available, otherwise the previous segment's
   actual final frame and optional FL2VA endpoint.
7. Assemble with duplicated-context trimming and a hard join or tiny audiovisual microfade.
8. Validate dimensions, fps, duration, video/audio streams, finite audio, visual continuity,
   and scene evolution before delivery.

## CLI

```bash
$HOME/.pi/agent/skills/create-video/create_video.sh \
  -p "integrated_multimodal_description: [Shot 1] ... overall_soundscape: ... non_diegetic_music: ..." \
  -o output.mp4
```

### Put an approved storyboard/reference image into MiniMax H3

The wrapper's `--image` option is the CLI input for an approved storyboard keyframe. It routes
the image to H3 FL2VA as the **exact first frame and geometry anchor**; it is not a loose style
reference. Use one clean horizontal frame generated at **exactly the same resolution as the
planned video**—normally 864×480. A matching aspect ratio alone is not sufficient.

```bash
REF_IMAGE="/absolute/path/to/approved_storyboard_shot01_864x480.png"
OUT="$HOME/generated/minimax-h3/shot01.mp4"

$HOME/.pi/agent/skills/create-video/create_video.sh \
  --model minimax-h3 \
  --image "$REF_IMAGE" \
  --resolution 864x480 \
  --duration 5 \
  --steps 6 \
  --prompt "For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced. integrated_multimodal_description: [Shot 1] Preserve Picture 1's exact adult character identity, costume, horizontal composition, scene geography, landmarks, eye-level camera, and focal length. The character <one concrete action>. At the same time <one environmental change travels from foreground through mid-ground to background>. By the end <exact character and environment end state>. Traditional hand-drawn 2D cel animation; do not replace the background. overall_soundscape: <continuing ambience and action-linked sounds>. non_diegetic_music: <music development or none>." \
  --output "$OUT"
```

Paths containing spaces are safe when enclosed in double quotes. When creating the storyboard,
set one shared resolution variable and pass the exact same value to both tools:

```bash
VIDEO_RESOLUTION="864x480"
STORYBOARD_DIR="$HOME/generated/minimax-h3/storyboards"
mkdir -p "$STORYBOARD_DIR"

cd "$HOME/models-work/flux2"
source .venv-rocm72/bin/activate
FLUX2_BIG_WMMA_LINEAR=1 python \
  "$HOME/.pi/agent/skills/create-image/scripts/create_image.py" \
  "Horizontal landscape 16:9 full-bleed anime image, not portrait or square. <exact shot design>" \
  --anime --aspect-ratio 16:9 --output-size "$VIDEO_RESOLUTION" \
  --out-dir "$STORYBOARD_DIR" --prefix shot01

# Confirm the returned final_path is exactly 864x480 before using it.
ffprobe -v error -select_streams v:0 -show_entries stream=width,height \
  -of csv=s=x:p=0 "/absolute/final_path/from/create-image.png"

$HOME/.pi/agent/skills/create-video/create_video.sh \
  --image "/absolute/final_path/from/create-image.png" \
  --resolution "$VIDEO_RESOLUTION" \
  --prompt "For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced. <motion, environment, and sound>" \
  --output "$HOME/generated/minimax-h3/shot01.mp4"
```

Do not generate a 1920×1080 storyboard for an 864×480 video and rely on H3 to resize it.
Generate the storyboard at the final video canvas from the start. Use FFmpeg cropping only to
repair legacy or externally supplied images that cannot be regenerated.

Direct ComfyUI generator equivalent, for debugging the wrapper:

```bash
cd "$HOME/src/ComfyUI"
./.venv/bin/python scripts/minimax_h3_generate.py \
  --image "/absolute/path/to/approved_storyboard_shot01_864x480.png" \
  --prompt "For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced. <observable motion, environment, and sound>" \
  --width 864 --height 480 --seconds 5 --steps 6 --seed 12345 --turbo \
  --prefix "video/storyboard_shot01" --server http://127.0.0.1:8188
```

**Multiple storyboard rule:** do not pass several unrelated storyboards into one wrapper call.
Generate one H3 clip per approved storyboard. For a continuous segment 2, prefer clip 1's
losslessly extracted actual final frame as segment 2's `--image`; use the next storyboard as
a planned endpoint only in an explicitly endpoint-enabled FL2VA workflow. For a deliberate
new viewpoint or focal length, use that storyboard as a new shot and join it with an editorial
cut.

### Options

| Flag | Meaning | Default |
|---|---|---:|
| `--model` | Compatibility selector: `minimax-h3`, `minimax`, or `h3` | `minimax-h3` |
| `-p, --prompt` | Observable visual and audio description | required |
| `-i, --image` | Exact first-frame image for FL2VA | none |
| `-d, --duration` | One-shot duration; 3–5 seconds recommended | `5` |
| `--fps` | Native fps; must remain 24 | `24` |
| `-a, --aspect` | Aspect ratio when resolution is omitted | `16:9` |
| `-r, --resolution` | Explicit dimensions, snapped to multiples of 32 | `864x480` |
| `--hq` | Use a 576-pixel short side | off |
| `-o, --output` | Output MP4 | timestamped path |
| `--seed` | Random seed | random |
| `--steps` | Denoise steps | Turbo `6`, reference `20` |
| `--turbo` | Turbo v4 sampler | on |
| `--no-turbo` | Reference sampler | off |
| `--audio` | Keep synchronized native stereo audio | on |
| `--no-audio` | Strip audio from final MP4 | off |

## Prompt structure

Use a structured multimodal prompt:

```text
integrated_multimodal_description: [Shot 1] <subject, concrete action, environment,
lighting, viewpoint, focal length, framing, camera movement, temporal progression>.
overall_soundscape: <continuing ambience and synchronized visible SFX>.
non_diegetic_music: <genre, instruments, development, or "none">.
```

For image-to-video, begin with:

```text
For the target video, at 0.00 seconds into the target video, Picture 1 is fully referenced.
```

Then specify what moves and changes. Do not redescribe a conflicting identity, costume,
geometry, or viewpoint.

## Cinematic Shot Map: angle, focal length, and movement

Before generating storyboards or clips, maintain one shared Shot Map as the source of truth.
Do not invent independent image and video prompts: derive both from the same row.

```text
Shot/beat | duration | shot size | viewpoint angle and height | simulated focal length
framing and depth of field | viewpoint movement | subject movement | start state | end state
environment and light progression | screen direction/continuity | audio | next-shot join
```

### Shot size and viewpoint angle

Use shot size and viewpoint angle as separate controls:

- **EWS/WS/full shot:** geography, full-body action, choreography, and floor contact.
- **MS/MCU:** body language, dialogue, hand actions, and social tension.
- **CU/ECU/insert:** expression, eye line, impact reaction, or decisive prop detail.
- **Eye-level:** neutral human scale. **Low angle:** power or threat. **High angle:**
  vulnerability or overview.
- **Overhead/bird's-eye:** spatial geometry and choreography. **Worm's-eye:** extreme upward
  force, heroic jumps, falling debris, or vertigo.
- **Dutch angle:** instability or impact; state an observable horizon tilt, normally 10–25°,
  instead of merely saying “Dutch angle.”
- **Profile/three-quarter/OTS/POV/reverse:** specify which shoulder or character owns the
  foreground, where the view looks, and the subjects' spatial relationship.

Describe viewpoint geometry in natural language. Avoid the bare word `camera` in image prompts
when a model may render equipment; use `viewpoint`, `view`, or `framing`. Video prompts may use
standard cinematography terms when describing motion.

### Simulated focal-length guide

Millimetres are visual intent for generative models, not guaranteed physical calibration.
Always pair a focal length with visible perspective cues:

| Simulated lens | Use | Observable cues to request |
|---|---|---|
| 14–18 mm ultra-wide | worm's-eye, extreme speed, monumental space | strong near/far scale, enlarged foreground, converging lines, edge stretch |
| 20–24 mm wide | close action, narrow interiors, movement toward view | pronounced depth, foreground energy, readable environment |
| 28–35 mm moderate wide | establishing, full-body combat, tracking | natural wide perspective, character plus geography |
| 40–50 mm normal | dialogue, medium shots, neutral observation | restrained distortion, natural proportions |
| 65–85 mm short telephoto | portrait, emotion, close-up | shallow depth, clean face, separated background |
| 100–135 mm telephoto | standoff, pursuit, surveillance | compressed distance, stacked background planes |
| 200 mm+ long telephoto | remote observation, extreme compression | flattened depth, narrow field of view, strong isolation |
| Fisheye | comic aggression or surreal motion | curved edges and deliberate radial distortion |

Do not choose lens by shot size alone: an 18 mm close-up exaggerates the face, while an 85 mm
close-up flatters and isolates it. For character beauty shots, prefer 50–85 mm. For dynamic
foreshortening, prefer 14–28 mm and explicitly identify the enlarged foreground limb or prop.
Treat 28 mm establishing, 50 mm medium, and 85 mm close views as editorial cuts, not endpoints
to be morphed together.

### Viewpoint-movement grammar

For every moving shot specify **movement type + direction/path + amplitude + speed + subject
relationship + endpoint**:

- `slow push-in from a wide two-shot to a medium close-up, stopping before the face crops`
- `fast side-tracking left-to-right parallel to the runner, keeping the full body centered`
- `low 18 mm viewpoint retreats rapidly as the swordswoman lunges toward it`
- `crane rises three metres into an overhead view, revealing the circular spell pattern`
- `clockwise 120° orbit at constant radius while both fighters remain opposite each other`
- `whip-pan follows the strike and resolves on the opponent's impact pose`

Available movement vocabulary includes static, pan, tilt, push/pull, tracking, side tracking,
arc/orbit, crane/boom, pedestal, handheld, zoom, and dolly zoom. Distinguish viewpoint movement
from subject movement. Avoid stacking more than one dominant viewpoint move and one subject
action in a 3–5 second segment unless deliberately testing a complex shot.

### Continuity checks

Track these across connected shots: identity, wardrobe, prop/weapon hand, eye line, screen
direction, character facing, ground position, scene geography, landmark placement, light
source direction, weather, environmental state, and action phase. Preserve the 180-degree rule
unless a motivated crossing shot visibly re-establishes geography. Every shot must have a new
story function; do not repeat the same pose, distance, and angle without narrative purpose.

For action, preserve readable causality:

```text
anticipation/charge → initiation → contact or evasion → reaction → settle/new threat
```

A single storyboard frame should depict one readable instant, not several moments at once.

## Segmentation and editorial assembly plan

Choose the join before generation; continuity does not mean forcing every clip through the
previous final frame.

| Relationship to next segment | First-frame source | Recommended join |
|---|---|---|
| Same continuous action and viewpoint | previous clip's actual final frame or motion context | remove duplicate context/frame; hard seamless join |
| Same scene, deliberate new angle or focal length | independently approved storyboard | cut-on-action, reaction cut, match cut, or audio J/L cut |
| New scene or time | new storyboard | motivated hard cut, ambience bridge, flash/occlusion if appropriate |
| Fast combat montage | independent 2–3 s shots | impact cut or whip-pan cut |
| Dialogue/emotional scene | independent 4–6 s shots | reaction cut with J/L-cut dialogue or ambience |
| Incompatible existing clips | dedicated bridge only if spatially plausible | otherwise keep an honest editorial cut |

Use 3–5 second clips by default. Split whenever there is a major change in viewpoint, focal
length, location, dominant action, or environmental state. For each segment write:

```text
Segment N — duration/frame count; start state; one dominant action; one dominant viewpoint
move; environment/light progression; sound progression; exact end state; continuity source;
join type and trim/crossfade amount.
```

Assembly rules:

1. Prefer motion-context continuation for a truly continuous shot; otherwise extract the
   previous clip's lossless final frame for chained I2VA/FL2VA.
2. Use a fresh approved storyboard for a genuine cut. Do not let the previous frame lock a new
   angle into a weak morph.
3. Trim duplicated motion-context time or the repeated opening frame before concatenation.
4. Prefer a hard cut. Use only a 0.1–0.25 second audiovisual microfade when needed; never hide
   broken geometry with a long dissolve.
5. Preserve ambience across cuts with J/L cuts, but keep visible impact SFX synchronized.
6. Inspect several frames before and after every join for pose, velocity, screen direction,
   lighting, identity, audio phase, and background continuity.

## MiniMax H3 operational rules

- Source images should match the target aspect ratio. For the tuned path, prepare the approved
  keyframe at exactly 864×480 because it is the first-frame geometry anchor.
- Width and height must be divisible by 32.
- Use native 24 fps.
- Valid frame counts follow `17k+5`: 73 ≈ 3.04 s, 90 ≈ 3.75 s,
  107 ≈ 4.46 s, and 124 ≈ 5.17 s.
- Keep one primary shot/action in each segment. Describe concrete movement rather than
  internal emotion.
- State dialogue, ambience, visible SFX, and music explicitly. Keep dialogue short and quote
  exact words.
- Do not enable global SageAttention; long-sequence backend corruption has been reported.
- Use the validated FP16 video VAE path. Do not force FP32 video VAE. Audio VAE stays FP32.
- This host is UMA. CPU offload does not release physical memory and only adds copies.
- Never stop or shrink `qwen-mtp.service` to make room. H3 is validated while it remains active.

## Videos longer than five seconds

Never force a long request into one unreliable generation. Plan it as ordered 3–5 second H3
segments. Every segment needs:

```text
Segment N — frame count; start state; character action; environmental progression;
camera/lens; sound development; exact end state; next context source.
```

Keep resolution, fps, identity, scene geography, screen direction, lens logic, and base art
direction coherent across a continuous shot.

### Preferred: latent and audio motion context

When a compatible H3 Motion Context workflow is installed, pass the previous segment's final
video latent and audio context into the next generation. This preserves speed, direction,
pose trajectory, color, ambience, and sound continuity better than decoding a single frame.

- Prefer 39 context frames (about 1.63 seconds) for routine continuation.
- Use 56 frames (about 2.33 seconds) for fast or complex movement when memory permits.
- Use 22 frames for calmer movement.
- Keep resolution unchanged throughout the chain.
- Continuation prompts must first preserve established movement, composition, environmental
  state, and sound bed, then introduce the next action.
- Trim duplicated context during assembly and inspect the exact join.
- The simple wrapper does not claim to perform latent/audio chaining automatically.

Community workflow: https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context

### Portable fallback: chained I2VA/FL2VA

1. Generate segment A.
2. Extract A's actual final frame losslessly.
3. Use it as segment B's `first_frame`.
4. For free continuation, describe forward development. For a planned endpoint, use the next
   approved storyboard as `last_frame` and describe one continuous path toward it.
5. Remove the duplicated opening frame during assembly.
6. Prefer a hard join. If required, use only a 0.1–0.25 second audiovisual microfade.
7. Never use a long dissolve to hide incompatible poses; it produces ghosting.

If independent clips already exist, generate a separate 3–5 second FL2VA bridge from clip A's
actual final frame to clip B's first frame.

### Deliberate shot changes

Do not morph incompatible focal lengths or viewpoints. Use an editorial cut, cut-on-action,
occlusion, petals, flash, or whip-pan. Preserve ambience with an audio J/L cut or tiny
acrossfade. Frame interpolation can smooth cadence within a shot but cannot repair identity,
pose, camera, or scene discontinuity.

## 2D anime storyboards with `/create-image`

For 二次元動畫, anime, cel-animation, and hand-drawn requests, use the `create-image` skill
with Anima to design keyframes before H3 generation.

1. Define exact subject ground position and screen position, body orientation, foot placement,
   action, viewpoint side, viewpoint height, focal length, framing, fixed landmarks, and
   entry/exit movement for every shot.
2. **Generate every storyboard horizontally and at the exact video resolution.** Produce one
   clean, full-frame **16:9 landscape image per shot** with `/create-image --output-size
   864x480` for the tuned default. If the video uses another canvas, pass that exact `WxH` to
   both `create-image --output-size` and `create_video.sh --resolution`. Never default to
   portrait, vertical, square, panels, or a contact sheet.
3. Begin image prompts with:
   `Horizontal landscape 16:9 full-bleed image, not portrait or square.`
4. Do not put panel numbers, captions, lens labels, camera diagrams, borders, or fake UI into
   image prompts.
5. Use non-native draft generation first. Spend native 1080p time only after art-direction
   approval or when the user explicitly requests a final high-quality still.
6. For hand-drawn style, specify varied ink lines, flat opaque cel colors, hard two-tone
   shadows, and painted gouache/paper backgrounds. Exclude 3D, CGI, glossy rendering, plastic
   skin, bloom, bokeh, volumetric effects, visible camera equipment, text, and watermarks.
7. Establish a character master and scene map. Reuse appearance, palette, screen direction,
   ground markers, and landmarks. Use conservative img2img for adjacent poses and inspect
   identity, hands, feet, clothing, background, and perspective after every generation.
8. Show stills to the user and obtain visual approval before generating video.
9. Use same-composition adjacent keyframes as FL2VA endpoints. Treat 28 mm establishing,
   50 mm medium, and 85 mm close views as deliberate cuts rather than forced morphs.
10. Confirm the `create-image` JSON `final_path` has the exact target dimensions before video
    generation. Do not silently resize a newly generated storyboard afterward; matching pixel
    geometry must be established during storyboard generation.

Image prompt skeleton:

```text
Horizontal landscape 16:9 full-bleed anime image, not portrait or square.
<adult character design> stands <exact world position> and appears <screen position>.
Body faces <direction>; feet and weight <placement>. Viewpoint is <side and height>,
<focal length>, <shot size>. <Fixed landmarks and screen direction>.
Traditional hand-drawn 2D animation keyframe, varied ink lines, flat cel colors,
hard two-tone shadows, painted paper background. No panels, captions, text, visible
camera, 3D, CGI, glossy rendering, bloom, bokeh, or watermark.
```

## Animation philosophy: animate the world, not only the character

A successful animation is not a moving character pasted over a frozen illustration. Treat the
character, environment, light, atmosphere, sound, and camera as one causal system. A static
camera means stable framing, not a static world.

1. **Protect invariants; animate variables.** Keep identity, costume, geography, landmarks,
   screen direction, lens, and art direction stable. Deliberately evolve wind, grass,
   branches, clouds, water, crowds, practical lights, shadows, weather, particles, or distant
   activity.
2. **Give the environment an arc.** Every segment needs an environmental beginning,
   progression, and readable ending. The ending becomes the next segment's starting state.
3. **Use visible cause and effect.** A spell sends a light wave across flowers; footsteps
   disturb dust and grass; a door changes interior light. Avoid unrelated decorative motion.
4. **Stage change through depth and time.** Describe when motion reaches foreground,
   mid-ground, background, and landmarks. Use `begins`, `travels`, `one after another`,
   `gradually`, and `settles` rather than listing simultaneous effects.
5. **Keep change legible.** Prefer one dominant environmental transformation plus two or three
   supporting motions. Too many unrelated changes cause geometry replacement and flicker.
6. **Preserve geography during transformation.** Progressively transform the established
   scene; never suddenly replace the background.
7. **Let lighting tell time and emotion.** Cloud shadows, dusk shifts, lanterns, reflections,
   and magic illumination must affect both character and environment consistently.
8. **Make sound undergo the same event.** Continue ambience and add spatial cues in causal
   order. Music may develop with the transformation but must not restart as an unrelated take.
9. **Use stillness intentionally.** Held poses may contrast action, while breathing, cloth,
   light, and atmosphere retain life.
10. **Judge continuity as motion, not matching pixels.** Inspect velocity, direction,
    illumination, sound, and environmental state around every join.

Temporal prompt pattern:

```text
At first <stable character and environmental state>.
Then <character action> causes <dominant environmental event>.
The effect travels from <foreground> through <mid-ground> to <background landmark>.
Meanwhile <two supporting motions> evolve consistently.
By the end <character pose, lighting, environment, and sound settle into next state>.
Preserve <identity, geography, camera, lens, and art style>; do not replace the background.
```

## Deployment and performance

- ComfyUI: `~/src/ComfyUI`
- Service: `~/.config/systemd/user/comfyui.service`
- API: `http://127.0.0.1:8188`
- Generator: `~/src/ComfyUI/scripts/minimax_h3_generate.py`
- Diffusion model: `minimax_h3_fl2va_pruned_int8_convrot.safetensors`
- Text encoder: `qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors`
- Video VAE: `minimax_h3_video_vae_fp16.safetensors`
- Audio VAE: `minimax_h3_audio_vae_fp32.safetensors`
- Turbo LoRA: `minimax_h3_turbo_v4_step600_ema.safetensors`

The gfx1151 optimization materializes contiguous Q/K/V before SDPA. On the tuned workload it
improved sampling from about 461.6 seconds to 222 seconds and end-to-end wall time from about
565.4 seconds to 325.2 seconds. Do not remove this optimization without an exact-shape A/B.

## Validation before delivery

```bash
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=index,codec_name,codec_type,width,height,r_frame_rate,sample_rate,channels \
  -of json output.mp4
```

Confirm:

- MP4 exists and is non-empty.
- Video is H.264, requested dimensions, and 24 fps.
- Native-audio output contains AAC 32 kHz stereo.
- Decoded audio contains no NaN or Inf.
- Beginning, middle, end, and every segment join are visually inspected.
- Character identity, hands, feet, costume, geography, and screen direction remain coherent.
- The environment visibly evolves rather than behaving like a frozen illustration.
- Sound development matches visible events.
- No long ghosting dissolve hides a broken join.
- `comfyui.service` and protected `qwen-mtp.service` remain healthy.

## Sources

- Official ComfyUI workflow: https://docs.comfy.org/tutorials/video/minimax/minimax-h3
- Official model repository: https://huggingface.co/Comfy-Org/MiniMax-H3
- Official prompt guide: https://huggingface.co/MiniMaxAI/MiniMax-H3/blob/main/docs/VIDEO_PROMPT_WRITING_GUIDE_base_en.md
