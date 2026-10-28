---
name: kling-omni-image
description: Generate high-quality AI images using Kling's Omni-Image model via an async submit→poll workflow. Supports text prompts, reference images (URL or Base64), element library composition, resolutions up to 2k, flexible aspect ratios, and single/series output modes. Use this skill whenever the user wants to generate, create, or produce images with Kling AI, asks about Omni-Image, wants multi-modal image generation with reference images or elements, or needs batch image series output.
license: MIT
---

# Kling Omni-Image — Image Generation

## Overview

Based on Kling AI's Omni-Image model, supports generating high-quality images via text prompts, reference images (URL or Base64), and element library resources. Supports 1k/2k resolution, multiple aspect ratios, and two output modes: single image (single) and image series (series).

**Workflow (async):**

1. Call the submit endpoint (POST) to create a generation task and obtain a `task_id`
2. Poll the query endpoint (GET) until `task_status` becomes `succeed` or `failed`
3. Retrieve image URLs from `task_result.images` (single mode) or `task_result.series_images` (series mode)
4. Transfer image URLs to Supabase Storage (CDN links expire after 30 days)

> Read `references/submit-api.md` for the full specification and code for the submit endpoint.
> Read `references/query-api.md` for the full specification and code for the query endpoint.

---

## Complete Async Workflow

```typescript
const apiKey = process.env["INTEGRATIONS_API_KEY"]!;

async function generateOmniImage(params: SubmitParams): Promise<ImageResult[]> {
  // Step 1: Submit task
  const submitResp = await fetch("https://app-dohnbj5by5mp-api-2Y00Vzbe0MBY.gateway.appmedo.com/v1/images/omni-image", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Gateway-Authorization": `Bearer ${apiKey}`,
    },
    body: JSON.stringify(params),
  });

  if (!submitResp.ok) throw new Error(`Submit HTTP error: ${submitResp.status}`);
  const submitJson = await submitResp.json();
  if (submitJson.code !== 0) throw new Error(`Submit API error ${submitJson.code}: ${submitJson.message}`);

  const taskId: string = submitJson.data.task_id;

  // Step 2: Poll until done
  const POLL_INTERVAL_MS = 7000;
  const TIMEOUT_MS = 10 * 60 * 1000;
  const deadline = Date.now() + TIMEOUT_MS;

  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));

    const queryResp = await fetch(
      `https://app-dohnbj5by5mp-api-n9QVxo8blgrL.gateway.appmedo.com/v1/images/omni-image/${taskId}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "X-Gateway-Authorization": `Bearer ${apiKey}`,
        },
      }
    );

    if (!queryResp.ok) throw new Error(`Query HTTP error: ${queryResp.status}`);
    const queryJson = await queryResp.json();
    if (queryJson.code !== 0) throw new Error(`Query API error ${queryJson.code}: ${queryJson.message}`);

    const status: string = queryJson.data.task_status;

    if (status === "succeed") {
      const result = queryJson.data.task_result;
      // Return images array (single mode) or series_images (series mode)
      return result.images?.length > 0 ? result.images : result.series_images ?? [];
    }
    if (status === "failed") {
      throw new Error(`Task failed: ${queryJson.data.task_status_msg}`);
    }
    // submitted / processing → keep polling
  }

  throw new Error(`Task ${taskId} timed out after 10 minutes`);
}
```

**Important constraints (must be followed):**
- When `result_type = single`: the `series_amount` field **must NOT appear** in the request body
- When `result_type = series`: `series_amount` **must be provided**, range [2, 9]
- Base64 images must be raw encoded content, **without** prefixes like `data:image/jpeg;base64,`

---

## Generation-time File Download (Required)

The URLs returned by the generation API are temporary CDN links that expire after 30 days. During generation time (Agent direct call scenario), after obtaining a URL, **you must immediately use the Bash tool to download the file locally** so the user can view the result.

```bash
curl -L -o <local-path>.jpg "<generated image URL>"
```

**Complete generation-time workflow (including download step):**

1. Call `generateOmniImage()` to execute the submit → poll loop and obtain the list of image URLs
2. For each image, use the Bash tool to run `curl -L -o <local-path> "<url>"` to download the file locally
3. Notify the user of the file paths where images have been saved

> **Note**: Upstream CDN links expire after 30 days. Download immediately after obtaining the URL — do not delay.

---

## Generation-time Usage (Agent Direct Call)

See the "Generation-time Usage" section in `references/submit-api.md` for the complete TypeScript call example.

See the "Generation-time Usage" section in `references/query-api.md` for the query endpoint call example.

---

## Post-generation Usage (In-app via Edge Function)

See the "Post-generation Usage" section in `references/submit-api.md` for the Edge Function code for the submit endpoint (including Supabase Storage transfer logic).

See the "Post-generation Usage" section in `references/query-api.md` for the Edge Function code for the query endpoint.

---

## Notes

- **Key security**: `INTEGRATIONS_API_KEY` may only be read server-side in an Edge Function — never expose it to the frontend.
- **Error handling**: Always handle 429 (quota exceeded) and 402 (insufficient balance).
- **Note**: The submit (create task) endpoint is billed. The query endpoint (polling) is not billed. Avoid unnecessary duplicate submissions.
- **Image storage**: Generated image URLs are valid for 30 days — transfer them to Supabase Storage or another persistent store promptly.
- **series_amount constraint**: When `result_type=single`, passing `series_amount` is strictly forbidden and will cause the request to fail.
- **Base64 images**: Must not include the `data:image/...;base64,` prefix — pass only the raw encoded string.
- **Image size limits**: Each reference image must not exceed 10MB, minimum size 300px, aspect ratio between 1:2.5 and 2.5:1.
