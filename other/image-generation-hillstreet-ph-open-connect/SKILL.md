---
name: image-generation
description: Generate images from text prompts or input images using an async API. Use this skill whenever the user wants to create, generate, or edit images — including text-to-image, image-to-image style transfer, or compositing multiple images. The workflow is submit a task, then poll until complete, then save the result. Triggers on requests like "generate an image of...", "create a picture of...", "convert this photo to...", "make an illustration of...", or any request involving AI image creation or editing.
license: MIT
---

# Image Generation (Advanced Version)

## Capability Overview

This skill drives an asynchronous image-generation service that supports three modes:

| Mode | Description |
|------|-------------|
| Text-to-Image | Generate an image from a text prompt alone |
| Image-to-Image | Upload one image + a text instruction (e.g. style transfer, background swap) |
| Multi-Image-to-Image | Compose two or more images together guided by a text prompt |

The workflow is always **submit → poll → result**. Tasks typically take up to 10 minutes; poll every 5–10 seconds.

> Read `references/submit-api.md` for the full submit endpoint spec.
> Read `references/query-api.md` for the full query/poll endpoint spec.

---

## End-to-End Async Workflow

```typescript
// Full async workflow: submit → poll → result
async function generateAndWait(
  contents: ContentPart[]
): Promise<string> {                      // returns the raw markdown image text
  const { taskId } = await submitTask(contents);

  const POLL_INTERVAL_MS = 7000;          // 5–10 s recommended
  const TIMEOUT_MS = 10 * 60 * 1000;     // 10 minutes
  const deadline = Date.now() + TIMEOUT_MS;

  while (Date.now() < deadline) {
    await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    const result = await queryTask(taskId);
    if (result.status === "SUCCESS") {
      // result.result.candidates[0].content.parts[0].text contains
      // the image as a Markdown string: ![image](data:image/jpeg;base64,...)
      return result.result.candidates[0].content.parts[0].text;
    }
    if (result.status === "FAILED") {
      throw new Error(`Task failed: ${JSON.stringify(result.error)}`);
    }
    if (result.status === "TIMEOUT") {
      throw new Error(`Task ${taskId} timed out on the server side`);
    }
    // PENDING → keep polling
  }
  throw new Error(`Task ${taskId} timed out after 10 minutes`);
}
```

---

## Generation-Time Usage (Agent Direct Call)

Use the built-in scripts for generation-time calls. The scripts read `INTEGRATIONS_API_KEY` from the environment, submit the task, poll until it finishes, extract the Base64 image embedded in the Markdown result, and save it to disk.

**The Bash tool timeout MUST be set to 600000ms (600 seconds).**

**Submit + poll (all-in-one):**

```bash
# Text-to-image
python3 <skill-path>/scripts/generate_image.py \
  --prompt "A cute orange kitten in a sunny garden, cartoon style" \
  --output /tmp/generated-image.jpg

# Image-to-image / multi-image composition (repeat --image)
python3 <skill-path>/scripts/generate_image.py \
  --prompt "Convert to cartoon illustration style" \
  --image /path/to/photo.png \
  --output /tmp/generated-image.jpg
```

**Resume polling an existing task:**

```bash
python3 <skill-path>/scripts/query_image.py --task-id "<task_id>" --output /tmp/generated-image.jpg
```

The scripts print one JSON line:
- On success: `{"status":"succeed","task_id":"...","file":"/tmp/generated-image.jpg"}`
- If still processing: `{"status":"processing","task_id":"..."}`

On failure they print an error to stderr and exit with a non-zero code.

> **Note**: The Base64 image data exists only in the current response. The script saves it to `--output` immediately — always pass `--output`.

---

## Post-Generation Usage (In-App via Edge Function)

See `references/submit-api.md` for the submit Edge Function boilerplate and `references/query-api.md` for the query Edge Function boilerplate.

The recommended application-side pattern is:

1. Frontend calls the `image-generation-submit` Edge Function → receives `taskId`
2. Frontend polls the `image-generation-query` Edge Function every 7 seconds
3. On `SUCCESS`, the Edge Function decodes the Base64 and uploads to Supabase Storage, returning a persistent `publicUrl`
4. Frontend displays the image from `publicUrl`

---

## Note

Each complete generation (submit + poll to terminal state) is billed as **1 call**. Avoid resubmitting the same task.

---

## Notes

- **Key security**: `INTEGRATIONS_API_KEY` may only be read server-side in an Edge Function; never expose it to the frontend.
- **Error handling**: Always handle 429 (quota exceeded) and 402 (insufficient balance); forward those error bodies verbatim to the frontend.
- **Base64 format**: When uploading images, `inline_data.data` must be a pure Base64 string — do not include the `data:image/xxx;base64,` prefix.
- **Request size**: The total size of a single request (including all images) must not exceed **20 MB**.
- **Supported formats**: PNG, JPEG, WEBP.
- **Timeout**: Set the task timeout to at least 10 minutes; poll every 5–10 seconds.
