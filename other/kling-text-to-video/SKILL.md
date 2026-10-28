---
name: kling-text-to-video
description: Generate short videos from text prompts using the Kling AI text-to-video API. Use this skill whenever the user wants to create a video from a script, scene description, or keywords — for e-commerce marketing, creative promotion, educational content, or entertainment production.
license: MIT
---

# Kling Text-to-Video

## Overview

Converts text descriptions into short videos using the Kling AI model, supporting asynchronous task polling (up to 10 minutes). Suitable for e-commerce marketing, creative promotion, educational content, and entertainment production.

| Property | Value |
|----------|-------|
| Submit Endpoint | `POST https://app-dohnbj5by5mp-api-qYGWo8XA7JVY.gateway.appmedo.com/v1/videos/text2video` |
| Query Endpoint | `GET https://app-dohnbj5by5mp-api-oLpZ7eD5j2Pa.gateway.appmedo.com/v1/videos/text2video/{id}` |
| Auth | Bearer Token (platform_managed) |
| Request Format | `application/json` |
| Response Format | JSON (includes video URL) |
| Note | The submit endpoint is used to create the task and is billed; the query endpoint is used to poll for results and is free |

### Main Request Parameters (Submit)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | `string` | Yes | Video generation prompt |
| `model_name` | `string` | No | Model name: `kling-v1`, `kling-v1-6`, `kling-v2-master`, `kling-v2-1-master`, `kling-v2-5-turbo` |
| `negative_prompt` | `string` | No | Negative prompt |
| `aspect_ratio` | `string` | No | Video aspect ratio: `16:9`, `9:16`, `1:1` |
| `duration` | `string` | No | Video duration in seconds: `5` or `10` |

> For complete parameter descriptions and code, see `references/submit-api.md` and `references/query-api.md`.

---

## End-to-End Async Workflow

Kling video generation is an **async task**: first submit the task to obtain a `task_id`, then poll the query endpoint until the status becomes `succeed` or `failed`.

```typescript
// Full async workflow: submit → poll → retrieve video URL
async function generateAndWait(prompt: string, options?: {
  model_name?: string;
  aspect_ratio?: string;
  duration?: string;
  negative_prompt?: string;
}) {
  // Step 1: Submit task
  const { taskId } = await submitTextToVideo(prompt, options);

  // Step 2: Poll until complete
  const POLL_INTERVAL_MS = 7000;          // Recommended 5–10 seconds
  const TIMEOUT_MS = 10 * 60 * 1000;     // Max 10 minutes
  const deadline = Date.now() + TIMEOUT_MS;

  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    const result = await queryTask(taskId);
    if (result.task_status === "succeed") return result;
    if (result.task_status === "failed")  throw new Error(`Task failed: ${result.task_status_msg}`);
    // submitted / processing → continue polling
  }
  throw new Error(`Task ${taskId} timed out after 10 minutes`);
}
```

Task status descriptions:
- `submitted` — Task submitted, waiting to be processed
- `processing` — Task is being processed
- `succeed` — Task completed successfully; `task_result.videos` contains the video URL
- `failed` — Task failed

---

## Generation-Time Usage (Direct Agent Call)

Use the built-in scripts for generation-time calls. The scripts read `INTEGRATIONS_API_KEY` from the environment.

**The Bash tool timeout MUST be set to 600000ms (600 seconds).**

**Submit + poll (all-in-one):**

```bash
python3 <skill-path>/scripts/generate_text_to_video.py \
  --prompt "A serene mountain stream flowing through a forest" \
  --aspect-ratio 16:9 \
  --duration 5 \
  --mode std \
  --output-dir /tmp/text2video
```

**Resume polling an existing task:**

```bash
python3 <skill-path>/scripts/query_text_to_video.py --task-id "<task_id>" --output-dir /tmp/text2video
```

The scripts print one JSON line:
- On success: `{"status":"succeed","task_id":"...","videos":[{"url":"...","file":"..."}]}`
- If still processing: `{"status":"processing","task_id":"..."}`

On failure they print an error to stderr and exit with a non-zero code.

**Generation-time file download (required):**

Video URLs are ephemeral CDN links. If `--output-dir` is not passed, download immediately:

```bash
curl -L -o /tmp/generated_video.mp4 "<task_result.videos[0].url>"
```

> For full parameter details, see `references/submit-api.md` (submit) and `references/query-api.md` (query).

---

## Post-Generation Usage (In-App via Edge Function)

In the application, proxy requests through two separate Edge Functions: one for submitting tasks and one for querying status. The query Edge Function transfers the video URL to Supabase Storage upon task completion and returns a persistent public URL to the frontend.

> For the complete Edge Function code and frontend call patterns see the "Post-Generation Usage" sections in `references/submit-api.md` and `references/query-api.md`.
