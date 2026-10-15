---
name: tokenlab-cinematic-video
description: "Make cinematic shots from text or a still image with TokenLab video models, using film camera language: shot size, camera move, lens, light, and sound. Use when the user says \"make a cinematic shot\", \"film-like video of ...\", \"movie trailer shot\", \"drone shot of ...\", \"slow dolly-in on ...\", \"b-roll for my video\", or \"storyboard these shots into clips\". One call makes one shot; plan a sequence as several shots with a shared look. For a product-focused ad, use tokenlab-product-ad-video. To simply animate a photo, use tokenlab-animate-image. For exact first and last frames, use tokenlab-keyframe-transition."
license: MIT
metadata:
  category: video
---

# Cinematic Video

Write each shot like a director: what the camera sees, how it moves, through which lens, in which light, and what you hear. Make one clip per shot and keep a shared style line across shots.

## Inputs to collect

- **Shot list:** one line per shot (subject + action + place). Ask for the order if there is more than one.
- **Look:** genre or film style, color palette, time of day, and era.
- **Camera:** shot size, angle, and one move per shot.
- **Sound:** ambience, effects, dialogue, or silence.
- **Format:** aspect ratio (16:9, 9:16, 21:9), length per shot, and resolution.
- **Anchor image** (optional): a still that fixes the look or the character. Use it with image-to-video.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `text-to-video` | `veo3.1` | default | Cinematic shot with sound |
| `text-to-video` | `seedance-2.0` | alternative | Alternative; long clips, 21:9 (not live-tested) |
| `text-to-video` | `kling-v3.0` | alternative | Alternative (not live-tested) |
| `text-to-video` | `hailuo-h3` | alternative | Alternative; negative prompt (not live-tested) |
| `text-to-video` | `wan-3.0` | alternative | Alternative; long clips (not live-tested) |
| `text-to-video` | `grok-imagine-video` | alternative | Low-cost draft |
| `image-to-video` | `veo3.1-fast` | default | Still to shot with sound |
| `image-to-video` | `veo3.1` | alternative | Higher tier (not live-tested) |
| `image-to-video` | `seedance-2.0` | alternative | Alternative; long clips, 21:9 (not live-tested) |
| `image-to-video` | `kling-v3.0` | alternative | Alternative (not live-tested) |
| `image-to-video` | `hailuo-h3` | alternative | Alternative; negative prompt (not live-tested) |
| `image-to-video` | `wan-3.0` | alternative | Alternative; long clips (not live-tested) |
| `image-to-video` | `grok-imagine-video` | alternative | Low-cost draft |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

### How to choose

Exact fields and values come from each model's contract.

- **Veo 3.1:** the default text-to-shot model with sound. 4, 6, or 8 s at 720p or 1080p. Audio is always on.
- **Veo 3.1 Fast:** the default still-to-shot model; same durations and always-on audio, faster and lower cost. Veo 3.1 is the higher tier for a still.
- **Seedance 2.0:** an alternative for longer clips (4-15 s) and 21:9.
- **Kling 3.0:** an alternative, 3-15 s.
- **Hailuo H3:** an alternative that takes `negative_prompt`. 6 or 10 s at 768p.
- **Wan 3.0:** an alternative for long clips, 2-30 s at 480p-1080p.
- **Grok Imagine video:** a low-cost draft. 1-15 s at 480p or 720p.

All use `POST /v1/videos/generations` with an explicit `operation`. Send `output_audio` or `negative_prompt` only when the operation lists it.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. **Plan the shots.** Write one prompt per shot with the template in Technique. Keep one style line and reuse it word for word in every shot.
2. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation text-to-video` (or `image-to-video`). Use only listed fields and values.
3. Estimate the cost: `python ../tokenlab-run/scripts/tokenlab_run.py price MODEL`, then per-second price × `duration` for each shot. Veo audio is always on, so use its with-audio price. Use the Official price as the upper bound. Tell the user the total before you start.
4. Make a cheap test of the hardest shot first (short duration, lowest resolution, or a low-cost model). Fix the prompt, then make the final shots.
5. Build each body:

   ```json
   {"model": "MODEL_ID", "operation": "text-to-video", "prompt": "Slow dolly-in, eye level, 35mm lens. A lighthouse keeper in a yellow raincoat climbs wet stone stairs at dusk; waves crash below. Cold blue light with a warm lamp glow from the window. Film noir mood, light rain. Sound: wind, surf, his boots on wet stone.", "duration": 8, "resolution": "720p", "aspect_ratio": "16:9"}
   ```

   Take `MODEL_ID` from the Models list above for the shot's operation. Set `duration` and `resolution` to values its contract lists.

6. Call and wait: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/videos/generations --json @shot1.json --wait`. Save each task ID. Poll every 5-10 s.
7. If a wait times out, resume with `python ../tokenlab-run/scripts/tokenlab_run.py poll TASK_ID`. Never create a duplicate task.
8. Return each shot's video URL, model, task ID, and estimate, in shot order.

## Technique

- **Prompt template** (the parts Google lists for Veo prompts): camera move and position → composition → subject and action → place → lens and focus → light and ambiance → style → sound. Leave out any part you do not need.
- **One camera move per shot.** "Slow dolly-in" or "pan left", not both. Make a second shot for the next move.
- **Name the lens and focus.** "35mm, deep focus" for context; "85mm, shallow focus" for faces; "macro lens" for textures; "wide-angle lens" for space.
- **Light sets the mood.** Name its direction and color: "low warm sun from behind", "cold blue night with neon spill", "single overhead practical".
- **Sound on Veo.** Veo always makes audio. Describe effects and ambience explicitly. Put dialogue in quotes: `She whispers, "We're late."`
- **Consistency across shots.** Reuse the same character description and style line. For a fixed character or set, make a still first (see `tokenlab-character-consistency`) and use image-to-video from it.
- **Exclusions.** Use `negative_prompt` only on models that list it (for example Hailuo H3). Elsewhere, describe the result you want instead.
- **Shot vocabulary:** see `references/shot-language.md`.

## Quality bar

- Each shot shows the requested shot size, camera move, and light.
- The camera move is smooth and single; no unasked cuts inside a shot.
- Characters, wardrobe, and the style line stay the same across shots.
- Sound matches the action (Veo) or the shot is silent when asked (models with `output_audio`).
- The user saw the total estimate first, and the answer lists every shot's model and task ID.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-product-ad-video`: product-focused shots.
- `tokenlab-animate-image`: animate a single still.
- `tokenlab-keyframe-transition`: fix the first and last frame of a shot.
- `tokenlab-extend-video`: make a shot longer.
- `tokenlab-prompting`: prompt craft per model family.
