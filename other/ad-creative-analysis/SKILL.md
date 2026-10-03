---
name: ad-creative-analysis
description: Analyze ad creatives (video and image) for competitive research and inspiration. Use when breaking down competitor ads, building swipe files with annotations, understanding what makes an ad work, or analyzing ad creative strategy. Handles video ads (via Gemini video understanding) and image ads (via vision model). Produces structured marketing-focused analysis covering hook, script, visual approach, emotional angle, CTA, and format.
---

# Ad Creative Analysis

Analyze ad creatives like a media buyer — not generic descriptions, but tactical breakdowns of what makes ads work.

## Video Ad Analysis

Upload video to Gemini Files API, then run analysis via `gemini-2.5-flash`.

### Step 1: Upload video

```bash
FILE_SIZE=$(wc -c < "$VIDEO_PATH" | tr -d ' ')

# Start resumable upload
UPLOAD_URL=$(curl -s -i -X POST \
  "https://generativelanguage.googleapis.com/upload/v1beta/files?key=$GEMINI_API_KEY" \
  -H "X-Goog-Upload-Protocol: resumable" \
  -H "X-Goog-Upload-Command: start" \
  -H "X-Goog-Upload-Header-Content-Length: $FILE_SIZE" \
  -H "X-Goog-Upload-Header-Content-Type: video/mp4" \
  -H "Content-Type: application/json" \
  -d "{\"file\": {\"displayName\": \"$(basename $VIDEO_PATH)\"}}" \
  | grep -i 'x-goog-upload-url' | tr -d '\r' | cut -d' ' -f2)

# Upload file
RESULT=$(curl -s -X POST "$UPLOAD_URL" \
  -H "X-Goog-Upload-Command: upload, finalize" \
  -H "X-Goog-Upload-Offset: 0" \
  -H "Content-Length: $FILE_SIZE" \
  --data-binary @"$VIDEO_PATH")

FILE_URI=$(echo "$RESULT" | jq -r '.file.uri')
```

Wait for `state: "ACTIVE"` before proceeding (poll with GET on the file URI + API key).

### Step 2: Analyze with Gemini

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [
      {"fileData": {"mimeType": "video/mp4", "fileUri": "'"$FILE_URI"'"}},
      {"text": "<ANALYSIS_PROMPT>"}
    ]}],
    "generationConfig": {"temperature": 0.3, "maxOutputTokens": 2000}
  }'
```

Use the analysis prompt from `references/prompts.md` — select the appropriate variant (video, image, or comparative).

## Image Ad Analysis

Use the built-in `image` tool directly — no upload step needed. Pass the image file path and the image analysis prompt from `references/prompts.md`.

## Output Format

All analysis follows a consistent structure. See `references/prompts.md` for the full prompt templates that produce this format:

1. **Hook** — First 3 seconds (video) or first impression (image). What stops the scroll?
2. **Script/Copy** — Full voiceover transcript (video) or all text in the creative (image)
3. **Visual Approach** — Style, transitions, format (talking head, UGC, motion graphics, etc.)
4. **Emotional Angle** — Primary emotion driving the ad (fear, aspiration, curiosity, urgency, etc.)
5. **CTA** — What action, how presented, friction level
6. **Ad Format** — Aspect ratio, duration, platform optimization
7. **What Makes It Work** — Tactical takeaways for your own ads
8. **Weaknesses** — What could be improved

## Comparative Analysis

When analyzing multiple ads from the same advertiser, add a comparison section after individual analyses. See the comparative prompt in `references/prompts.md`. Covers:

- Creative patterns (what do they repeat across ads?)
- Testing strategy (what are they A/B testing?)
- Funnel consistency (do all ads drive to the same offer?)

## Integration with Other Skills

This skill is designed to work alongside:
- **meta-ads-library** — Extract ads, then analyze each creative
- **landing-page-analysis** — Analyze the destination page behind the CTA

Typical pipeline: extract → analyze creative → analyze landing page → compile report.
