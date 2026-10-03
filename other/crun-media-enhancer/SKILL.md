---
name: crun-media-enhancer
description: Enhance or upscale an uploaded video or image with Crun through a localized configuration form, an affordability check, asynchronous execution, and result delivery. Use when the user asks to improve video quality, clarity, resolution, frame rate, restore old footage, upscale an image, sharpen or add image detail, repair hands, or enhance an existing video or image resource.
---

# Crun Media Enhancer

Use `../../../runtime/crun_cli.py`. Use the fixed model `video-enhance` for video and `image-upscale` for images. Read `../../crun-account-credits/SKILL.md` before estimating and `../../crun-task-runner/SKILL.md` before creating or monitoring a task.

Use the official parameter guides as the human-facing reference: `https://docs.crun.ai/ai-tools/video-enhance` for video and `https://docs.crun.ai/ai-tools/image-upscale` for images. Still inspect the live model schema after confirmation as required below.

## Localize every interaction

Determine the response language from the user's latest request. If it is ambiguous, use the language used in the surrounding conversation. Write all user-facing prose in that language, including the upload prompt, form title, field labels, option labels and descriptions, confirmation summary, credit messages, progress updates, errors, and result delivery. Keep API field names and enum values unchanged when constructing JSON, but translate their visible labels and explanations.

Do not mix languages merely because the source documentation or API response uses another language. Preserve URLs, model IDs, task IDs, numeric values, and file paths verbatim.

## Require one source resource from the current conversation

Accept a local image or video, or a directly usable remote resource URL supplied in the current conversation.

Treat only resources that are visibly attached or explicitly linked in the current conversation as source material. A new session starts with no source material, even if prior sessions, chat history, tool traces, task results, or generated JSON mention a media URL or local path. Never use, copy, reconstruct, or infer a new task input from historical generated JSON; historical JSON is reference-only and cannot satisfy this requirement. Do not silently carry forward a prior task's URL, settings, task ID, or output.

At the start of every new session, first check the current conversation for a source image/video or a directly usable URL. If none is present, respond only with a short localized equivalent of:

> Please upload or send the video or image you want to enhance, and I will start immediately.

Then end the turn. Do not show a configuration form, query models, estimate credits, or create a task.

If the user refers to an earlier upload or result without re-attaching it or sending its URL in the current conversation, treat the source as missing and request the upload or URL again. Do not proceed based on the reference alone.

If several resources are present and the intended resource is unclear, use a localized form to ask the user to select exactly one. The image endpoint currently accepts only one image per task.

Upload a selected local resource before building the input:

```text
python <runtime>/crun_cli.py upload <local-file>
```

Use the returned `file_url`. Reuse an existing Crun resource URL directly. Never send a local path, Base64, or a data URI in a task input.

## Analyze the source before matching settings

Before showing the parameter guide, inspect the selected resource and record a concise localized analysis. For a video, determine available metadata such as duration, width/height, source frame rate, codec, audio presence, and visible content type; for an image, determine width/height, format, color mode, and whether it is small, blurry, noisy, a drawing, or likely to contain hands. Use `ffprobe` or another available media-metadata tool for video and Pillow or another available image-metadata tool for images. For a remote URL, probe the URL directly when supported or download only a temporary inspection copy; never put that temporary path in task JSON.

Match recommendations to the analysis instead of blindly using the table defaults. Avoid output resolution or frame rate that is disproportionate to the source; use 2× for already-large images and consider 4× for genuinely small sources; prefer Preserve original/Gentle for clean, high-fidelity sources and stronger presets only when blur, noise, or missing detail warrants them; infer scene from the actual content. If metadata or visual analysis is unavailable, say so in localized text and use conservative recommended defaults. Include the analysis basis in the configuration summary.

## Explain parameters, then collect structured choices

Follow this order exactly after obtaining and analyzing the source resource:

1. Show the applicable localized parameter-guide table in the conversation. Explain every visible parameter, what each option changes, and which option is recommended. Do not ask for a choice in this message.
2. If a native structured user-input facility is available in the active mode, call it to collect the configuration. Use a **single-select/radio** control for every parameter group and allow exactly one choice in each group.
3. Put the localized confirmation action equivalent to **Confirm and enhance** on the final structured page. Treat that submission as authorization for the exact configuration.
4. If structured input is unavailable because the session is in Default mode, do not call `request_user_input`, do not ask the user to switch modes, and do not ask them to type parameter values. Apply every valid preference already stated in the enhancement request and use analysis-matched recommendations for every remaining parameter. Show the parameter table and a localized configuration summary, then ask for one explicit confirmation of that exact summary (for example, a localized “Proceed with these settings?”). Do not estimate, create, or monitor a task until the user gives an affirmative confirmation.

Never ask the user to type a parameter name, API value, option label, number, comma-separated list, or confirmation word. Never replace the controls with a numbered text menu, even as a fallback. If the structured facility limits fields per page, use consecutive pages. If it limits choices per question, use consecutive single-select questions or hierarchical single-select groups while keeping every final choice unambiguous.

Do not output a message saying that the task is paused because `request_user_input` is unavailable in Default mode. Default mode must take the analyzed-settings confirmation path above. The only free-text response permitted is the final yes/no confirmation of the already displayed configuration; never use free text to select or edit individual parameters. For any other actual structured-tool failure, report the concrete error and stop before task creation rather than silently treating an unexpected failure as user confirmation.

Use human-readable localized labels in both the guide table and controls. Never use raw API field names such as `mode`, `dynamic`, or `resemblance` as primary visible labels. Keep the API value behind each choice. Mark the recommended choice and preselect it by default; preselect any explicit preference from the user's request when valid. Do not interpret the original enhancement request as form submission. The final structured submission is the confirmation for structured mode; the explicit yes/no response is the confirmation for Default-mode fallback.

### Video form

Use model `video-enhance` and the resource URL as `video_url`. First show this localized guide table; the text in parentheses is the hidden API value and may be omitted from user-facing text when the platform can keep it hidden.

| Parameter | Meaning | Available choices and effects | Recommended default |
|---|---|---|---|
| Quality mode | Controls the quality/speed tier. | Standard: balanced speed and quality (`std`); Professional: maximum fidelity for production work (`pro`). | Standard (`std`) |
| Enhancement strength | Controls how strongly the model changes the source. | Gentle: preserve the original look (`mild`); Balanced: apply a more visible quality lift (`moderate`). | Gentle (`mild`) |
| Content type | Tunes enhancement for the video's visual style. | General video (`common`); Creator/short video (`ugc`); Short drama (`short_series`); AI-generated video (`aigc`); Old-film restoration (`old_film`). | General video (`common`) |
| Output resolution | Sets the delivered frame size. | 720p (`720p`); HD (`1080p`); 2K (`2k`); 4K (`4k`). Higher resolutions generally require more processing. | HD (`1080p`) |
| Frame rate | Sets motion smoothness in the output. | Cinematic 24 fps (`24`); Standard 30 fps (`30`); Smooth 60 fps (`60`); High frame rate 120 fps (`120`). | Standard 30 fps (`30`) |

After showing the table, present five single-select controls, one for each row, in the same order. Offer only the listed frame-rate choices; do not expose a custom numeric entry. Warn in localized text before confirmation when the selected frame rate exceeds four times the source frame rate.

Construct only:

```json
{
  "video_url": "<uploaded-or-remote-url>",
  "mode": "std",
  "strength": "mild",
  "scene": "common",
  "resolution": "1080p",
  "fps": 30
}
```

### Image form

Use model `image-upscale` and place the single resource URL in `img_urls`. First show this localized guide table. Explain the preset as one visible parameter; its hidden tuning values are implementation details.

| Parameter | Meaning | Available choices and effects | Recommended default |
|---|---|---|---|
| Enhancement preset | Sets detail generation, source fidelity, denoising effort, and sharpening together. | Balanced: general-purpose detail and fidelity (`dynamic=6`, `creativity=0.35`, `resemblance=0.6`, `num_inference_steps=18`, `sharpen=0`); Preserve original: minimize visual changes (`3`, `0.2`, `1.0`, `18`, `0`); Maximum detail: stronger texture and sharpness (`9`, `0.5`, `0.8`, `30`, `2`); Creative restoration: reconstruct more missing detail with greater source deviation (`9`, `0.7`, `0.5`, `30`, `1`). | Balanced |
| Enlargement | Controls output dimensions relative to the source. | 2× (`2`); 4× (`4`); 8× (`8`); 10× (`10`). Larger factors create bigger files and require more processing. | 2× (`2`) |
| Hand repair | Controls specialized hand correction. | Off (`disabled`); Repair hands only (`hands_only`); Repair image and hands (`image_and_hands`). | Off (`disabled`) |
| Output format | Sets the delivered image file type. | PNG: lossless (`png`); JPG: smaller file (`jpg`); WebP: modern compact format (`webp`). | PNG (`png`) |
| Seamless texture | Controls whether edges are made tileable. | Off (`false`); On: make the result repeat seamlessly (`true`). | Off (`false`) |

After showing the table, present five single-select controls, one for each row, in the same order.

Do not show raw controls for `dynamic`, `creativity`, `resemblance`, `sharpen`, or `num_inference_steps`; derive them from the selected preset. Do not offer blank numeric overrides. Keep `prompt`, `negative_prompt`, and `mask` hidden unless the user explicitly requested guided enhancement, artifact suppression, or regional enhancement. When needed, explain the applicable extra parameter in the guide table and provide predefined single-select choices with sensible prefilled values; do not ask the user to type parameter content solely to select a configuration.

Omit empty optional fields instead of sending empty strings. Construct the confirmed values, for example:

```json
{
  "img_urls": ["<uploaded-or-remote-url>"],
  "scale_factor": 2,
  "dynamic": 6,
  "creativity": 0.35,
  "resemblance": 0.6,
  "sharpen": 0,
  "num_inference_steps": 18,
  "handfix": "disabled",
  "pattern": false,
  "output_format": "png"
}
```

## Validate, estimate, and run

After structured form confirmation, or after the user confirms the analyzed Default-mode fallback configuration:

1. Inspect the fixed model's live schema and reconcile it with the confirmed form. Never invent a field or silently drop a rejected value.

   ```text
   python <runtime>/crun_cli.py models describe --model <video-enhance-or-image-upscale>
   ```

2. Save the exact final input as UTF-8 JSON and estimate it before task creation.

   ```text
   python <runtime>/crun_cli.py task estimate --model <model> --input-file <input.json>
   ```

3. Require `affordable: true`. If it is false or missing because the balance is insufficient, do not create a task. Report the estimated credits and balance when available, then provide this exact billing link with a localized invitation to recharge:

   `https://crun.ai/zh/billing`

   End the turn after the insufficient-credit message. Do not switch models or weaken settings automatically.

4. If affordable, create exactly once, retain `task_id`, and poll only that task. The confirmed form or explicit Default-mode confirmation is the user's authorization for this exact input.

   ```text
   python <runtime>/crun_cli.py task create --model <model> --input-file <input.json>
   python <runtime>/crun_cli.py task wait --task-id <task_id> --timeout-seconds 900
   ```

   This polls at the default five-second interval until the 900-second local time limit. A timeout is a recoverable local stop, not a failed remote task; retain the task ID and follow the recovery rules instead of creating another task. Do not set or mention a maximum polling-attempt count.

5. Follow `crun-task-runner` for timeouts, failures, recovery, and result delivery. Return localized status text plus the normalized task ID, credits, and local media path. For both images and videos, verify the returned local path is inside the dynamically resolved daily output root (and its `<task_id>` child); identify a download error instead of claiming a nonexistent local output. Use the remote media URL only as a fallback.

Treat configuration, authentication, validation, network, and service errors according to their actual cause. Show the billing link only for an insufficient-credit result, not for unrelated failures.
