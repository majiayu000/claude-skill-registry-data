---
name: tokenlab-animate-image
description: "Turn one still image into a short video clip with TokenLab image-to-video models. Use when the user says \"animate this photo\", \"make this picture move\", \"bring this image to life\", \"turn this still into a video\", \"add motion to my artwork\", or \"make a living photo / cinemagraph\". The image becomes the first frame; the prompt describes the motion and the camera. For a clip that must end on a second image, use tokenlab-keyframe-transition. For a product ad, use tokenlab-product-ad-video. For a speaking face, use tokenlab-talking-avatar. For a person who copies the moves in another video, use tokenlab-motion-control."
license: MIT
metadata:
  category: video
---

# Animate Image

Turn one still into a short clip. The image is the first frame. The prompt says what moves, how the camera moves, and what you hear.

## Inputs to collect

- **Image:** a public `https` URL or a TokenLab result URL. Crop it to the target aspect ratio first. Many models follow the input image shape and ignore `aspect_ratio` for this operation.
- **Motion:** what moves, and how much ("hair moves in a light wind", "she turns her head and smiles").
- **Camera:** static, or one move (slow push-in, pan left, orbit).
- **Length and size:** seconds and resolution. Start short for a first test.
- **Sound:** with or without audio. Some models always add audio; some can be silent.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `image-to-video` | `veo3.1-fast` | default | General image-to-video with sound |
| `image-to-video` | `kling-v3.0` | alternative | Alternative; sound on or off (not live-tested) |
| `image-to-video` | `hailuo-h3` | alternative | Alternative with native audio (not live-tested) |
| `image-to-video` | `seedance-2.0` | alternative | Alternative; long clips and high resolution (not live-tested) |
| `image-to-video` | `pixverse-v6` | alternative | Silent loop or background plate |
| `image-to-video` | `grok-imagine-video` | alternative | Low-cost draft |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

### How to choose

Exact fields and values come from each model's contract.

- **Veo 3.1 Fast:** the general choice with sound. 4, 6, or 8 s at 720p or 1080p. Audio is always on.
- **Kling 3.0:** an alternative with sound on or off. 3-15 s.
- **Hailuo H3:** an alternative with native audio. 6 or 10 s at 768p. Takes `negative_prompt`.
- **Seedance 2.0:** long clips (4-15 s) and high resolution (up to 4k).
- **PixVerse:** silent loops and background plates. Lists `output_audio`, 1-15 s, 360p-1080p.
- **Grok Imagine video:** a low-cost draft. 1-15 s at 480p or 720p. The output follows the input image shape.

All of these use `POST /v1/videos/generations` with `operation: "image-to-video"`. Most take the image in `image_url`; some (for example Vidu Q3) list `image` and `start_image` instead. Send `output_audio` only when the operation lists it.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation image-to-video`. Note `supported_parameters`, `allowed_durations`, `allowed_resolutions`, and `delivery`. Use only listed fields and values.
2. Estimate the cost: `python ../tokenlab-run/scripts/tokenlab_run.py price MODEL`. Most video models price per second, so multiply the per-second price for your resolution (and audio setting, if the price depends on it) by `duration`. Use the Official price as the upper bound. Tell the user the estimate before you start the job.
3. Write the prompt (see Technique) and build the body:

   ```json
   {"model": "MODEL_ID", "operation": "image-to-video", "image_url": "https://...", "prompt": "She smiles, raises her right hand, and waves at the camera twice. Static camera, soft studio light.", "duration": 2, "resolution": "480p"}
   ```

   Take `MODEL_ID` from the Models list above for `image-to-video`. Set `duration` and `resolution` to values its contract lists.

4. Call and wait: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/videos/generations --json @body.json --wait`. Save the task ID before you poll. The helper polls every 5 s; keep the interval at 5-10 s.
5. If your wait times out, resume with `python ../tokenlab-run/scripts/tokenlab_run.py poll TASK_ID`. Never create a second task for the same request.
6. On `failed`, read `error_details.code` and `param`, fix the body, and ask the user before a paid retry.
7. Return the video URL (`video_url`, `video.url`, or `videos[]`), the model, the task ID, and the estimate.

## Technique

- **Describe the change, not the picture.** The model already sees the image. Spend the prompt on action, camera, and sound. "The waves roll in and foam over the rocks; slow pan right" beats a full description of the beach.
- **Prompt parts:** subject + action, then camera position or move, then composition, lens or focus, and ambiance. These are the parts Google lists for Veo prompts, and they work as a checklist for any model.
- **One main action per clip.** Short clips have room for one gesture or one camera move. Make a second clip for the next beat, or extend the clip with `tokenlab-extend-video`.
- **Keep identity.** Say what must not change: "keep her face, hair, and jacket exactly as in the image."
- **Sound on Veo.** Veo 3.1 always makes audio. Describe the sounds you want ("soft wind, distant gulls"). Put spoken words in quotes. If you say nothing, you still get audio.
- **Silent output.** Pick a model whose contract lists `output_audio` and send `false`. Do not send `output_audio` to a model that does not list it.
- **Aspect ratio.** Crop the image before you call. Image-to-video output on Grok Imagine video follows the input image shape.
- **Prompt is required on some models.** Hailuo H3 Max needs a non-empty prompt for every operation.

## Quality bar

- The first frame matches the input image. Face, product, and text do not change shape or color.
- Motion is smooth and physically plausible. No melting hands, no jump cuts.
- Camera behavior matches the request (a static request stays static).
- Duration, resolution, and aspect ratio match what the user asked for.
- The user saw the cost estimate before the job, and the answer names the model and task ID.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-keyframe-transition`: set both the first and the last frame.
- `tokenlab-extend-video`: continue the clip past its last frame.
- `tokenlab-product-ad-video`: product shots and ad clips.
- `tokenlab-cinematic-video`: shots built from camera language.
- `tokenlab-prompting`: prompt craft per model family.
