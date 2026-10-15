---
name: tokenlab-extend-video
description: "Continue a video clip past its last frame with TokenLab video-extension models. Use when the user says \"make this video longer\", \"extend this clip\", \"continue the shot\", \"what happens next in this video\", \"add 5 more seconds\", or \"keep the scene going\". The new footage starts where the clip ends; join the parts in an editor. For a new clip from one still, use tokenlab-animate-image. For a clip that must end on a chosen image, use tokenlab-keyframe-transition. To change the look or content of the existing clip, use tokenlab-edit-video."
license: MIT
metadata:
  category: video
---

# Extend Video

Add new footage after the last frame of a clip. There are two kinds of input: a public video URL (any clip that meets the size and content rules), or the task ID of a clip that the same model made on TokenLab.

## Inputs to collect

- **Source clip:** a public `https` `.mp4` URL, or a TokenLab result URL. If the clip was made on TokenLab, also keep its task ID and model.
- **What happens next:** the action and camera for the new part. Keep the same subject, place, and light.
- **Added length** and output resolution.
- **Sound:** with or without audio.

## Models

<!-- tokenlab:models:start -->
<!-- Generated from the live catalog by scripts/sync_models.py. Do not edit; change preferredModels in catalog.json. -->

| Operation | Model | Pick | Use |
| --- | --- | --- | --- |
| `video-extension` | `seedance-2.0` | default | Continue any public clip from its video_url |
| `video-extension` | `seedance-2.0-fast` | alternative | Faster, up to 720p (not live-tested) |
| `video-extension` | `seedance-2.5` | alternative | Newer tier, up to 720p (not live-tested) |
| `video-extension` | `seedance-2.0-mini` | alternative | Low-cost, up to 720p |
| `video-extension` | `veo3.1-fast` | alternative | Known limit: task_id extension of a clip this model made returned 400 in live tests; prefer Seedance |
| `video-extension` | `grok-imagine-video` | alternative | Known limit: task_id extension of a clip this model made returned 400 in live tests; prefer Seedance |

This list refreshes daily from the live catalog. Preferred models come first; otherwise models are ranked by their 24-hour success rate. Before a call, confirm the model with `GET /v1/models/{model}` and read its price from `GET /v1/models/{model}/pricing`.
<!-- tokenlab:models:end -->

### How to choose

Exact fields and values come from each model's contract.

- **Seedance 2.0:** the default. Continues any public clip from its `video_url`. Adds 4-15 s, 480p up to 4k.
- **Seedance 2.0 Fast:** faster, up to 720p.
- **Seedance 2.5:** the newer tier, up to 720p. Adds up to 30 s.
- **Seedance 2.0 Mini:** low cost, up to 720p.
- **Veo 3.1 Fast and Grok Imagine video:** extend only a clip that the same model made, by `task_id`. Known limit: every live test of this path returned `400`, so treat it as unreliable and prefer Seedance.

All use `POST /v1/videos/generations` with `operation: "video-extension"`. Veo and Grok extension have Verified supply only, and they need the task ID of a clip from the same model. If TokenLab rejects the task ID with a `400` (for example `record not found` or `cannot currently honor these request parameters`), that clip cannot be extended on that model. Use the Seedance path with the clip's `video_url`.

## Workflow

Run each call with `tokenlab-run` (contract → estimate → call → poll → result). Commands below use its helper, `../tokenlab-run/scripts/tokenlab_run.py`, a path relative to this skill's folder. If you installed this skill without `tokenlab-run`, send the same requests with `curl`. `--wait` stops after 100 s; a longer task keeps running, so continue with the `resume` command it prints.

1. Read the contract: `python ../tokenlab-run/scripts/tokenlab_run.py contract MODEL --operation video-extension`. Note the input fields (`video_url` or `task_id`), durations, resolutions, and `delivery`.
2. Check the source clip (Seedance path): it shows no realistic human face, and each frame has at least 407,696 pixels (for example 640×640 or 1280×720). Clips that break either rule fail with `400` when you create the task. Use `ffprobe` to read the size.
3. Estimate the cost: `python ../tokenlab-run/scripts/tokenlab_run.py price MODEL`.
   - Seedance prices per million video tokens, with a separate price when the request has video input. The task result reports `usage.total_tokens`; the charge is tokens × that price. For scale, a 4 s 480p extension of a 2 s 720×720 clip reported 67,600 tokens.
   - Per-second models: per-second price × added seconds.
   Use the Official price as the upper bound. Tell the user the estimate.
4. Build the body:

   ```json
   {"model": "MODEL_ID", "operation": "video-extension", "video_url": "https://....mp4", "prompt": "Extend the video: the steam keeps rising from the full mug, and the camera slowly pushes in. Same morning window light.", "duration": 4, "resolution": "480p", "output_audio": false}
   ```

   Take a Seedance `MODEL_ID` (`seedance-2*`) from the Models list above for `video-extension`. Set `duration` and `resolution` to values its contract lists.

5. Call and wait: `python ../tokenlab-run/scripts/tokenlab_run.py run /v1/videos/generations --json @body.json --wait`. Save the task ID. Poll every 5-10 s.
6. If a wait times out, resume with `python ../tokenlab-run/scripts/tokenlab_run.py poll TASK_ID`. Never create a duplicate task.
7. The Seedance result is the new part only, starting from the source's last frame. Join the source and the new part in an editor or with `ffmpeg` (see Technique).
8. Return the new video URL, the model, the task ID, the estimate, and the joined file if you made one.

## Technique

- **Continue, do not restart.** Start the prompt with the intent ("Extend the video: ...") and describe only the next action. Repeat the key look words from the original prompt (subject, place, light) so the style holds.
- **One beat per extension.** Add one action per call. For a long scene, extend several times and check each part before the next call.
- **Match the source settings.** Use the same aspect ratio and resolution as the source, so the parts join cleanly.
- **Seedance input rules.** Seedance rejects a source clip that "may contain real person", and that check also caught a photoreal AI-generated person. Real people need TokenLab's Seedance material and real-person verification flow. Very small clips are rejected for pixel count.
- **Grok fields.** Grok Imagine video takes `task_id`, `prompt`, `extend_at` (the second in the source where the new part starts), and `extend_times` (the added seconds as a string, for example `"6"`). It does not take `duration` or `resolution` for this operation.
- **Veo fields.** Veo 3.1 and Veo 3.1 Fast take `task_id` (or `origin_task_id`) and `prompt`. Google's Veo docs say an extension continues from the final second of the clip and that a voice is hard to continue if it is not present in the last second.
- **Join the parts.** When both files have the same size, frame rate, and audio layout: `ffmpeg -i part1.mp4 -i part2.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" -map "[v]" joined.mp4` (video only). Add audio back in the editor if you need it.

## Quality bar

- The first frame of the new part continues the last frame of the source: same subject, place, light, and framing.
- No jump in color, size, or position at the join.
- The new action matches the prompt, and the added length matches the request.
- The user saw the estimate before the job, and the answer names the model and task ID.

## Related skills

- `tokenlab-run`: the call, poll, and result mechanics.
- `tokenlab-animate-image`: start a new clip from a still.
- `tokenlab-keyframe-transition`: end on a chosen image.
- `tokenlab-edit-video`: change the existing clip instead of continuing it.
