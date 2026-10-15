---
name: tokenlab-motion-control
description: "Make a character from one image perform the motion of a reference video with TokenLab motion-control models. Use when the user says \"make my character do this dance\", \"copy the moves from this video\", \"motion transfer\", \"apply this motion to my photo\", \"make this person move like the person in the clip\", or \"drive this image with a video\". The image sets who appears; the reference video sets the motion and the length. For free motion from one still, use tokenlab-animate-image. To restyle the reference clip itself, use tokenlab-edit-video. For a talking head from audio, use tokenlab-talking-avatar."
license: MIT
metadata:
  category: video
---

# Motion Control

Give the model a character image and a motion video. The output shows the character from the image doing the moves from the video. The output length follows the motion video.

## Inputs to collect

- **Character image:** a public `https` URL or a TokenLab result URL. One clear character, body and head visible.
- **Motion video:** a public `https` `.mp4` URL or a TokenLab result URL, 3-30 s. One person doing the motion, steady camera.
- **Resolution:** `720p` or `1080p`.
- **Prompt** (optional): the scene, background, or style around the character.

Both the image and the video must have an aspect ratio between 2:5 and 5:2.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `motion-control` | `kling-2.6-motion-control` | default | Character image plus motion video |
| `motion-control` | `kling-3.0-motion-control` | alternative | Newer tier (not live-tested) |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

### How to choose

Exact fields and values come from each model's contract.

- **Kling motion control 2.6:** the default. A character image plus a motion video.
- **Kling motion control 3.0:** the newer tier, with the same inputs.
- **Both:** the motion video is 3-30 s and sets the output length. The image and the video must be within 2:5 to 5:2. `resolution` (`720p` or `1080p`) is required.

All use `POST /v1/videos/generations` with `operation: "motion-control"`. `resolution` is a required selector.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation motion-control`. Read `durations_label`, `aspect_ratios_label`, and `notes` in the full model detail (`GET /v1/models/{model}`).
2. Check the inputs: the motion video is 3-30 s, both inputs are within 2:5 to 5:2, and the image framing matches the video (half-body with half-body, full-body with full-body). Use `ffprobe` for the video length.
3. Estimate the cost: `python ../tokenlab-run/scripts/tokenlab_run.py price MODEL`. Price is per second at the chosen resolution, and the output is as long as the motion video. Estimate = per-second price × motion video seconds. Tell the user the estimate.
4. Build the body:

   ```json
   {"model": "MODEL_ID", "operation": "motion-control", "image_url": "https://...character.jpg", "video_url": "https://...motion.mp4", "prompt": "The man in the green sweater in a warm beige studio.", "resolution": "720p"}
   ```

   Take `MODEL_ID` from the Models list above for `motion-control`.

5. Call and wait: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/videos/generations --json @body.json --wait --timeout 1800`. These jobs can take several minutes. Save the task ID. Poll every 5-10 s.
6. If a wait times out, resume with `python ../tokenlab-run/scripts/tokenlab_run.py poll TASK_ID`. Never create a duplicate task.
7. Return the video URL, the model, the task ID, and the estimate.

## Technique

- **Match the framing.** A half-body image with a half-body motion clip, or full body with full body, so the model does not have to invent body parts the image does not show.
- **One person, steady camera.** A motion clip with one person, a clear silhouette, and no cuts gives the cleanest result.
- **Show the whole character.** The head, hands, and the body parts that move must be visible and not cut by the frame edge in the image.
- **Prompt for the scene, not the moves.** The motion comes from the video. Use the prompt for background, clothing details, and light.
- **Sound.** The output keeps the motion video's soundtrack by default, and there is no mute field. Remove or replace the audio in an editor if needed.
- **Cost control.** The motion video length sets the output length and the charge. Trim the motion clip to the moves you need before you call.
- **Make a motion clip.** If the user has no clip, generate one with `tokenlab-animate-image` or `tokenlab-cinematic-video` (at least 3 s), then use its result URL.

## Quality bar

- The character keeps the face, clothes, and body shape from the image.
- The motion follows the reference: timing, pose, and direction.
- No extra or missing limbs, no flicker on the face or hands.
- The output length matches the motion clip; the user saw the estimate first.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-animate-image`: motion from a prompt instead of a reference clip.
- `tokenlab-edit-video`: restyle the reference clip itself.
- `tokenlab-character-consistency`: make a consistent character image first.
- `tokenlab-talking-avatar`: a talking head driven by speech.
