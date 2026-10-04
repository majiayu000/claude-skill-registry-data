---
name: animate-old-photos
description: >
  Animate old photos into AI-generated videos using the Animate Old Photos API.
  Upload a photo, generate a 5-second animation video, and download the result.
  Use when the user wants to animate a photo, bring an old photo to life,
  turn old photos into videos, create a video from a still image,
  or convert a photo to video.
  Requires a paid API key from https://animateoldphotos.org
---

# Animate Old Photos

Animate old photos into AI-generated videos via the [Animate Old Photos](https://animateoldphotos.org/) API. The agent uploads a photo, submits an animation task, polls for completion, and downloads the resulting MP4 video.

## Prerequisites

> **This is a paid service.** You need an API key and credits.
>
> - Official Website: [Animate Old Photos](https://animateoldphotos.org/)
> - Get your API key: [Profile > API Key](https://animateoldphotos.org/profile/interface-key)
> - Purchase credits: [Buy Credits](https://animateoldphotos.org/pricing)
>
> Each animation costs **3 credits**. [View pricing plans](https://animateoldphotos.org/pricing)

**System requirements:** `curl` and `jq` must be available in the shell.

## Workflow

### Before starting

1. Ask the user for their **API key** if environment variable `AOP_API_KEY` is not set.
2. Ask for the **image path**. Verify the file exists, is JPEG or PNG, and is under 10 MB.
3. Ask for an optional **prompt** describing desired motion (e.g. "grandmother smiling and waving"). If omitted the AI auto-generates motion.
4. Confirm with the user: "This will cost 3 credits. Proceed?"

### Step 1 — Authenticate

Exchange the API key for a short-lived access token and check the credit balance.

```bash
API_KEY="${AOP_API_KEY}"
AUTH=$(curl -s -X POST https://animateoldphotos.org/api/extension/auth \
  -H "Content-Type: application/json" \
  -d "{\"licenseKey\":\"${API_KEY}\"}")
TOKEN=$(echo "$AUTH" | jq -r '.accessToken')
CREDITS=$(echo "$AUTH" | jq -r '.creditBalance')
echo "Authenticated. Credits available: $CREDITS"
```

If `accessToken` is missing or `error_code` is `4010`/`4011`, tell the user their API key is invalid and link to <https://animateoldphotos.org/profile/interface-key>.

If credits < 3, tell the user to purchase more at <https://animateoldphotos.org/pricing> and stop.

### Step 2 — Upload image

Get a presigned upload URL, then PUT the image binary to cloud storage.

```bash
IMAGE_PATH="photo.jpg"
FILE_SIZE=$(stat -f%z "$IMAGE_PATH" 2>/dev/null || stat -c%s "$IMAGE_PATH" 2>/dev/null)
CONTENT_TYPE="image/jpeg"  # use image/png for .png files

UPLOAD=$(curl -s -X POST https://animateoldphotos.org/api/extension/upload-token \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"fileName\":\"$(basename "$IMAGE_PATH")\",\"contentType\":\"${CONTENT_TYPE}\",\"fileSize\":${FILE_SIZE}}")
UPLOAD_URL=$(echo "$UPLOAD" | jq -r '.uploadUrl')
KEY=$(echo "$UPLOAD" | jq -r '.key')
PUBLIC_URL=$(echo "$UPLOAD" | jq -r '.publicUrl')

curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Type: ${CONTENT_TYPE}" \
  --data-binary "@${IMAGE_PATH}"
echo "Image uploaded."
```

### Step 3 — Finalize upload

Confirm the upload and receive the encrypted payload needed for task submission.

```bash
FINALIZE=$(curl -s -X POST https://animateoldphotos.org/api/extension/upload-finalize \
  -H "Authorization: Bearer $TOKEN" \
  -F "key=${KEY}" \
  -F "publicUrl=${PUBLIC_URL}")
IMAGE_URL=$(echo "$FINALIZE" | jq -r '.url')
SS_MESSAGE=$(echo "$FINALIZE" | jq -r '.message')
DNT=$(echo "$FINALIZE" | jq -r '.dnt')
echo "Upload finalized."
```

### Step 4 — Submit animation task

Submit the animation job. The `Ss` header **must** contain the `message` value from Step 3.

```bash
PROMPT=""  # optional user prompt
TASK=$(curl -s -X POST https://animateoldphotos.org/api/extension/animate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Ss: ${SS_MESSAGE}" \
  -F "prompt=${PROMPT}" \
  -F "input_image_url=${IMAGE_URL}" \
  -F "dnt=${DNT}" \
  -F "type=m2v_img2video" \
  -F "duration=5" \
  -F "public=false")
TASK_ID=$(echo "$TASK" | jq -r '.taskId')
TASK_DNT=$(echo "$TASK" | jq -r '.dnt')
TASK_DID=$(echo "$TASK" | jq -r '.did')
echo "Task submitted (ID: $TASK_ID). Polling for result..."
```

If the response contains `error_code` `999990` or `10009`, the user has insufficient credits — link to <https://animateoldphotos.org/pricing>.

### Step 5 — Poll until done

Poll every 30 seconds. Typical completion time is 2–5 minutes.

```bash
OUTPUT="output.mp4"
while true; do
  sleep 30
  STATUS=$(curl -s -G "https://animateoldphotos.org/api/extension/animate" \
    --data-urlencode "taskId=${TASK_ID}" \
    --data-urlencode "dnt=${TASK_DNT}" \
    --data-urlencode "did=${TASK_DID}" \
    --data-urlencode "type=m2v_img2video" \
    -H "Authorization: Bearer $TOKEN")

  ERR_MSG=$(echo "$STATUS" | jq -r '.message // empty')
  if [ -n "$ERR_MSG" ]; then
    echo "Task failed: $ERR_MSG"
    break
  fi

  S=$(echo "$STATUS" | jq -r '.status')
  RESOURCE=$(echo "$STATUS" | jq -r '.resource // empty')
  if [ "$S" -ge 99 ] 2>/dev/null && [ -n "$RESOURCE" ]; then
    curl -s -o "$OUTPUT" "$RESOURCE"
    echo "Video saved to $OUTPUT"
    break
  fi
  echo "Still processing (status: $S)..."
done
```

Report the saved video path to the user when done.

### One-liner alternative

You can run the full pipeline with the bundled script:

```bash
bash scripts/animate.sh <API_KEY> <IMAGE_PATH> [PROMPT] [OUTPUT_PATH]
```

See [scripts/animate.sh](scripts/animate.sh) for details.

## Error Handling

| error_code | Meaning | Action |
|------------|---------|--------|
| `4010` | Invalid API key | Direct user to [get a key](https://animateoldphotos.org/profile/interface-key) |
| `4011` | API key expired | Direct user to [renew key](https://animateoldphotos.org/profile/interface-key) |
| `999998` | Access token invalid | Re-run Step 1 to get a new token |
| `999990` | Insufficient credits | Direct user to [buy credits](https://animateoldphotos.org/pricing) |
| `10009` | Insufficient credits | Direct user to [buy credits](https://animateoldphotos.org/pricing) |

For network errors, retry up to 3 times with exponential backoff (2s, 4s, 8s).

## Interaction Flow

1. **Trigger**: User says "animate this photo", "turn old photos into videos", "bring this photo to life", or similar.
2. **Gather inputs**: Ask for API key (if `AOP_API_KEY` not set), image path, and optional prompt.
3. **Confirm**: "This will cost 3 credits. You currently have {N} credits. Proceed?"
4. **Execute**: Run Steps 1–5, reporting progress at each stage.
5. **Complete**: "Your animated video has been saved to `{output_path}`."
6. **On error**:
   - Insufficient credits → "You need more credits. Purchase at: https://animateoldphotos.org/stripe"
   - Invalid API key → "Your API key is invalid or expired. Get one at: https://animateoldphotos.org/profile/interface-key"
   - Task failure → Show the error message and suggest the user retry or adjust the prompt.

## Constraints

- **Supported formats**: JPEG, PNG only
- **Max file size**: 10 MB
- **Min image dimension**: 300 × 300 px
- **Cost per animation**: 3 credits
- **Video duration**: 5 seconds
- **Typical processing time**: 2–5 minutes

For the complete API reference, see [animate-old-photos-api.md](reference/animate-old-photos-api.md).
