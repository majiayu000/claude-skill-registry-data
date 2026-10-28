---
name: kling-image-to-video
description: Generate AI videos from static images using Kling's Image-to-Video API with audio-visual sync. Use this skill whenever the user wants to animate an image, convert a photo to video, create an AI video from a picture, add motion to a still image, generate video from image with camera movement or voice, or use Kling image2video — even if they don't say "Kling" explicitly.
license: MIT
---

# Kling Image-to-Video (Audio-Visual Sync)

Generate high-quality videos from static images using Kling AI. Supports multiple model versions (kling-v1 through kling-v2-6), professional quality mode, camera control, motion brush trajectories, end-frame control, and voice synthesis. Videos can be 5s or 10s.

This is an **async** skill: submitting the task returns a `task_id` immediately; the video becomes available only after polling until `task_status` is `succeed`.

> Read `references/create-task-api.md` for the full submit-task specification and Edge Function code.
> Read `references/query-task-api.md` for the full query-task specification and Edge Function code.

---

## End-to-End Workflow

### Generation-time usage (Agent direct call)

Use the built-in scripts for generation-time calls. The scripts read `INTEGRATIONS_API_KEY` from the environment.

**The Bash tool timeout MUST be set to 600000ms (600 seconds).**

**Submit + poll (all-in-one):**

```bash
# From a local image file
python3 <skill-path>/scripts/generate_image_to_video.py \
  --image /path/to/image.jpg \
  --prompt "A slow camera pan across the scene" \
  --duration 5 \
  --output-dir /tmp/kling_video

# From an image URL
python3 <skill-path>/scripts/generate_image_to_video.py \
  --image-url "https://example.com/photo.jpg" \
  --prompt "Gentle wind blowing through the trees" \
  --mode pro \
  --output-dir /tmp/kling_video
```

**Resume polling an existing task:**

```bash
python3 <skill-path>/scripts/query_image_to_video.py --task-id "<task_id>" --output-dir /tmp/kling_video
```

The scripts print one JSON line:
- On success: `{"status":"succeed","task_id":"...","videos":[{"url":"...","file":"..."}]}`
- If still processing: `{"status":"processing","task_id":"..."}`

On failure they print an error to stderr and exit with a non-zero code.

**Generation-time file download (required):**

Video URLs are ephemeral CDN links (expire after 30 days). If `--output-dir` is not passed, download immediately:

```bash
curl -L -o ./output_video.mp4 "<generated video URL>"
```

> For detailed parameter descriptions, see `references/create-task-api.md` (submit) and `references/query-task-api.md` (query).

---

## Post-generation usage (in-app via Edge Function)

For production apps, use two Edge Functions — one per endpoint — so the platform API key never reaches the browser. After the query Edge Function retrieves the video URL, transfer it to Supabase Storage for persistence.

> Read `references/create-task-api.md` for the complete submit Edge Function (`edge-functions/kling-submit-image2video.ts`).
> Read `references/query-task-api.md` for the complete query Edge Function (`edge-functions/kling-query-image2video.ts`) including Supabase Storage transfer.

**Frontend polling loop:**

```typescript
// 1. Submit task via Edge Function
const { data: submitData, error: submitError } = await supabase.functions.invoke(
  "kling-submit-image2video",
  { body: { image, prompt, model_name: "kling-v2-6", mode: "pro", duration: "5" } }
);
if (submitError) throw submitError;
const taskId: string = submitData.data.task_id;

// 2. Poll via Edge Function until done
const POLL_INTERVAL_MS = 7000;
const TIMEOUT_MS = 10 * 60 * 1000;
const deadline = Date.now() + TIMEOUT_MS;

while (Date.now() < deadline) {
  await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));

  const { data: queryData, error: queryError } = await supabase.functions.invoke(
    "kling-query-image2video",
    { body: { task_id: taskId } }
  );
  if (queryError) throw queryError;

  const { task_status, task_status_msg, task_result } = queryData.data;
  if (task_status === "succeed") {
    // task_result.videos[].url is now a persistent Supabase Storage URL
    return task_result.videos;
  }
  if (task_status === "failed") throw new Error(`Generation failed: ${task_status_msg}`);
}
throw new Error("Timed out waiting for video generation");
```

---

## Parameter Summary

For full parameter tables, see `references/create-task-api.md` (submit) and `references/query-task-api.md` (query).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | Yes | Reference image (Base64 or URL), jpg/jpeg/png, ≤10MB, ≥300px, aspect ratio 1:2.5~2.5:1 |
| `prompt` | string | No | Positive text prompt, ≤2500 characters |
| `model_name` | string | No | Model version, default `kling-v2-6` |
| `mode` | string | No | Generation mode: `std` / `pro`, default `pro` |
| `duration` | string | No | Video duration (seconds): `5` or `10`, default `5` |
| `image_tail` | string | No | End-frame control image, same format requirements as `image` |
| `static_mask` | string | No | Static motion brush mask image (Base64 or URL); aspect ratio must match `image` |
| `camera_control` | object | No | Camera movement control; mutually exclusive with `image_tail` and `dynamic_masks`/`static_mask` |
| `camera_control.type` | string | No | Preset type: `simple` (custom) / `down_back` / `forward_up` / `right_turn_forward` / `left_turn_forward` |
| `camera_control.config.horizontal` | number | No | Left/right translation [-10, 10]; only when `type=simple`, only one config field may be non-zero |
| `camera_control.config.vertical` | number | No | Up/down translation [-10, 10] |
| `camera_control.config.pan` | number | No | Pitch [-10, 10] |
| `camera_control.config.tilt` | number | No | Yaw [-10, 10] |
| `camera_control.config.roll` | number | No | Roll [-10, 10] |
| `camera_control.config.zoom` | number | No | Focal length [-10, 10] |

---

## Notes

- **Key security**: `INTEGRATIONS_API_KEY` must only be read server-side in Edge Functions; never expose it to the frontend.
- **Error handling**: Always handle 429 (quota exceeded) and 402 (insufficient balance).
- **Billing**: The submit task endpoint (`api-eLMlJj3KJD89`) is billed. The query endpoint (`api-rLobzpqX85m9`) is free. Avoid re-submitting duplicate tasks to minimise unnecessary charges.
- **Mutually exclusive parameters**: `image+image_tail`, `dynamic_masks/static_mask`, and `camera_control` cannot be used simultaneously.
- **Base64 format**: Do not include the `data:image/xxx;base64,` prefix in Base64 image data; pass only the encoded string itself.
- **Mask images**: The aspect ratio of a mask image must match the input `image`; otherwise the task will fail.
- **Video expiry**: Generated video CDN links are automatically cleared after 30 days — download or transfer to Supabase Storage promptly.
