---
name: image-to-video
description: Generate short videos from a static image using the Kling AI image-to-video API. Use this skill whenever the user wants to animate an image, create a video from a photo, turn a picture into a video clip, or generate AI video from an uploaded image.
license: MIT
---

# Image to Video

Use Kling AI to generate a short video (5 or 10 seconds) from a single image. Supports multiple model versions and optional text prompts to guide the generated content. The API is asynchronous — submit a task and then poll for status until completion.

## Capability Overview

| Item | Details |
|------|---------|
| Submit endpoint | `POST https://app-dohnbj5by5mp-api-rY7JZvg0dqdL.gateway.appmedo.com/v1/videos/image2video` |
| Query endpoint | `GET https://app-dohnbj5by5mp-api-oYA6Z8wDBRDa.gateway.appmedo.com/v1/videos/image2video/{id}` |
| Processing mode | Async — submit then poll, maximum wait 10 minutes |
| Video duration | `"5"` or `"10"` seconds |
| Image requirements | JPG/JPEG/PNG, ≤ 10 MB, minimum dimension ≥ 300 px, aspect ratio 1:2.5 ~ 2.5:1 |
| Note | The submit endpoint is used to create the task and is billed; the query endpoint is used to poll for results and is free |

### Response Example

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "task_id": "task_abc123",
    "task_status": "succeed",
    "task_result": {
      "videos": [
        {
          "id": "video_123",
          "url": "https://example.com/video.mp4",
          "duration": "5.0"
        }
      ]
    }
  }
}
```

## End-to-End Workflow (Async Polling)

```
1. Submit task (POST /v1/videos/image2video)  →  obtain task_id
2. Poll status (GET /v1/videos/image2video/{task_id})  →  every 7 seconds
3. When task_status === "succeed"  →  retrieve video URL from task_result.videos[0].url
4. Download the video URL to local storage / Supabase Storage
```

### Polling Pattern Code (SKILL.md Main Workflow)

```typescript
async function generateAndWait(
  submitFn: () => Promise<{ taskId: string }>
): Promise<{ videoUrl: string; duration: string }> {
  const { taskId } = await submitFn();

  const POLL_INTERVAL_MS = 7000;         // poll every 7 seconds
  const TIMEOUT_MS = 10 * 60 * 1000;    // maximum 10 minutes
  const deadline = Date.now() + TIMEOUT_MS;

  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    const result = await queryTask(taskId);
    if (result.task_status === "succeed") {
      const video = result.task_result.videos[0];
      return { videoUrl: video.url, duration: video.duration };
    }
    if (result.task_status === "failed") {
      throw new Error(`Task failed: ${result.task_status_msg ?? "unknown reason"}`);
    }
    // submitted / processing → continue polling
  }
  throw new Error(`Task ${taskId} timed out after 10 minutes`);
}
```

## Generation-Time Usage (Agent Direct Call)

Use the built-in scripts for generation-time calls. The scripts read `INTEGRATIONS_API_KEY` from the environment.

**The Bash tool timeout MUST be set to 600000ms (600 seconds).**

**Submit + poll (all-in-one):**

```bash
# From a local image file
python3 <skill-path>/scripts/generate_image_to_video.py \
  --image /path/to/image.jpg \
  --prompt "A cat running through a garden" \
  --duration 5 \
  --output-dir /tmp/video_output

# From an image URL
python3 <skill-path>/scripts/generate_image_to_video.py \
  --image-url "https://example.com/photo.jpg" \
  --prompt "Slow camera zoom" \
  --output-dir /tmp/video_output
```

**Resume polling an existing task:**

```bash
python3 <skill-path>/scripts/query_image_to_video.py --task-id "<task_id>" --output-dir /tmp/video_output
```

The scripts print one JSON line:
- On success: `{"status":"succeed","task_id":"...","videos":[{"url":"...","file":"..."}]}`
- If still processing: `{"status":"processing","task_id":"..."}`

On failure they print an error to stderr and exit with a non-zero code.

**Generation-time file download (required):**

Video URLs are temporary CDN links (expire after 30 days). If `--output-dir` is not passed to the script, download the video immediately:

```bash
curl -L -o ./output_video.mp4 "<generated video URL>"
```

See `references/submit-api.md` and `references/query-api.md` for the full parameter tables.

## Post-Generation Usage (In-App via Edge Function)

In-app integration requires two Edge Functions: one to submit the task and one to query status and download the video. For complete Edge Function code and frontend call examples, refer to:

- `references/submit-api.md` — Submit task Edge Function and frontend call
- `references/query-api.md` — Query task Edge Function (including Supabase Storage video transfer) and frontend call

## Notes

- **Key security**: `INTEGRATIONS_API_KEY` must only be read server-side in Edge Functions — never expose it to the frontend.
- **Base64 image format**: When using Base64, provide only the pure Base64 string — **do not** include the `data:image/png;base64,` prefix.
- **Error handling**: Always handle 429 (quota exceeded) and 402 (insufficient balance).
- **Note**: The submit endpoint is used to create the task; the query endpoint is used to poll status. Avoid unnecessary repeated submissions caused by parameter errors.
- **Concurrency limit**: For the same account, keep concurrent submission counts under control to avoid rate limiting.
