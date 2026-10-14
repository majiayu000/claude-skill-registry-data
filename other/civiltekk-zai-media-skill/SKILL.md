---
name: civiltekk-zai-media-skill
description: >-
  Z.AI media production, four routes. image: generate images from text
  prompts via the GLM-Image API (/images/generations), saved as local PNGs.
  video: generate video from a text or first-frame-image prompt via
  CogVideoX-3 — submit then poll the async result, saved as local MP4.
  transcribe: transcribe audio files to text via GLM-ASR (wav/mp3, ≤25MB,
  ≤30s). ocr: extract text and layout from images or PDFs via GLM-OCR
  layout_parsing. Triggers: image generation, generate image, text to
  image, draw a picture, video generation, generate video, text to video,
  image to video, transcribe, speech to text, ASR, audio transcription,
  OCR, extract text from image, layout parsing, document text extraction.
license: Apache-2.0
compatibility: opencode
category: Media Generation
---

Consolidates zai-image-generation-skill + zai-video-skill + zai-asr-skill +
zai-ocr-skill (#604). Alias: formerly those four skills.

## What I do

Z.AI media generation and extraction across four routes. Every route is a
bash recipe against a direct Z.AI HTTP endpoint — OpenCode's provider layer
is chat-only, so none of these endpoints is reachable through a provider:

1. **Detect the route** (§Routes) — explicit > inferred > ask-once.
   Explicit: the request names the activity ("generate image", "draw a
   picture", "text to image" → `image`; "generate video", "text to video",
   "image to video" → `video`; "transcribe", "speech to text", "ASR" →
   `transcribe`; "OCR", "extract text from image", "layout parsing" →
   `ocr`). Inferred: the artifact shape (a picture from a prompt →
   `image`; an MP4 from a prompt or first-frame image → `video`; a
   transcript from an audio file → `transcribe`; text/layout from an
   image or PDF → `ocr`). Ambiguous ("make media for this README") → ask
   once per run, then proceed on the answer.
2. **Load the route's values file** (§Side files) and run its recipe
   verbatim — do not improvise endpoints, models, or parameters.
3. **Run the shared lifecycle** (§Lifecycle) around that recipe: key
   resolution → endpoint call → parse → persist → return.

## Lifecycle (shared method — every route)

| Step | Rule |
|------|------|
| 1. Key resolution | `$ZAI_API_KEY` env first, then the OpenCode credential-store fallback — the exact jq snippet lives per route in the values files and **stays verbatim**: key order differs by route (`image` prefers the coding-plan key; the pay-as-you-go routes prefer the `zai` key). If neither source has the key, **stop and report** — do not proceed. |
| 2. Endpoint call | Endpoint policy is **per route and must not be unified**: `image` defaults to the coding-plan endpoint via `ZAI_IMAGE_ENDPOINT` (plus its compliance note); `video`/`transcribe`/`ocr` target pay-as-you-go `https://api.z.ai/api/paas/v4` via `ZAI_MEDIA_ENDPOINT`. Exact defaults live in the values files. |
| 3. Parse | python3 JSON parse of the response; an `"error"` key → print the error body and stop (do not retry-loop). |
| 4. Persist | `image`/`video`: the API returns a temporary URL — download to a local file and verify with `file(1)` before claiming success. `transcribe`: transcript text on the `TRANSCRIPT:` line. `ocr`: extracted content on stdout. |
| 5. Return | Path contract (§Return Contract) — the `SAVED:` / `TRANSCRIPT:` / stdout result, never the API response JSON or temporary URLs. |

Harness binding for step 1 (§Portability contract): the `ZAI_API_KEY` env
var is the portable credential row — it alone works on every harness. The
`~/.local/share/opencode/auth.json` fallback reads OpenCode's credential
store (bonus row; ignore elsewhere — export the env var). Other/none (no
auth.json store): export `ZAI_API_KEY` — the env var alone is sufficient.
Recipe execution needs bash + curl + jq (any harness with a shell tool).
Requires bash (git-bash/WSL on Windows).

## Background shells (video poll loop)

Video generation takes **minutes** — the poll loop must not block the
session as a foreground command. Harness binding (§Portability contract):

- OpenCode — shell `background: true`: the call returns immediately and
  you are notified when the command exits — continue other work and read
  the result then.
- Claude Code — Bash `run_in_background: true`.
- Other/none — run the same loop in the foreground and tell the caller it
  blocks the session (correct, just slower).

Requires bash (git-bash/WSL on Windows).

## Side files (load rules)

| Read | When | Use |
|------|------|-----|
| `references/image.md` | route `image` | GLM-Image recipe: coding-plan endpoint default + `ZAI_IMAGE_ENDPOINT` override, SIZE/QUALITY/MODEL options, `mfile.z.ai` reachability note, compliance note (separate PAYG product; risk-control on the coding endpoint) |
| `references/video.md` | route `video` | CogVideoX-3 recipe: PAYG only (`ZAI_MEDIA_ENDPOINT`), submit → background poll → download/verify, ~$0.20/video cost note |
| `references/asr.md` | route `transcribe` | GLM-ASR recipe: PAYG only (`ZAI_MEDIA_ENDPOINT`), ≤25 MB / ≤30 s / wav-mp3 hard limits, ffmpeg split/convert |
| `references/ocr.md` | route `ocr` | GLM-OCR recipe: PAYG only (`ZAI_MEDIA_ENDPOINT`), Path A public-URL `layout_parsing`, Path B local-file vision fallback (ponytail note on the base64 rejection) |

Side files carry VALUES only; this file carries the METHOD plus the
lifecycle and background-shell bindings above.

## Routes

| Situation | Route |
|-----------|-------|
| "image generation", "generate image", "text to image", "draw a picture"; a picture artifact from a text prompt | `image` |
| "video generation", "generate video", "text to video", "image to video"; an MP4 artifact from a prompt or first-frame image | `video` |
| "transcribe", "speech to text", "ASR", "audio transcription"; a transcript from a `.wav`/`.mp3` file | `transcribe` |
| "OCR", "extract text from image", "layout parsing", "document text extraction"; text/layout from an image or PDF | `ocr` |
| Ambiguous | ask once (§What I do step 1), then route |
| **Sync vs async** | `image`, `transcribe`, `ocr` — one synchronous call. `video` — **minutes-long async**: submit, then poll loop as a background shell (§Background shells). |

## Boundaries

- Analyzing or describing an *existing* image or video (not producing one)
  is perception work, not this skill — use native vision
  (`image-analyzer-subagent`); this skill only *produces* artifacts.
- Z.AI chat/vision-provider work outside these four endpoints (web
  search, chat completions) is the provider layer's space, not this
  skill's.
- Audio longer than 30 s: split first (ffmpeg segment), then transcribe
  the segments in order and concatenate — see `references/asr.md`.
- `zai-media-subagent` is the agent that runs this skill by route
  (delegated media production keeps payloads and key usage out of the
  primary context).

## Agent behavior rules

- **Announce billable cost before submitting.** `video`/`transcribe`/`ocr`
  are pay-as-you-go and not covered by the GLM Coding Plan; async video
  tasks are billable once they run — submit only after the caller
  confirmed intent.
- **Stop on missing key** — never fabricate an artifact or transcript;
  report `Status: failed` ("ZAI_API_KEY not set").
- **Verify before success** — a route is successful only after the file
  exists on disk and `file(1)` reports the expected type (`image`,
  `video`), or the text actually parsed (`transcribe`, `ocr`).
- Headless/CI: no asks — read the route from the delegation prompt and use
  its documented default behavior.

## Return Contract

```
**Status:** [success | partial | failed]
**Output:** [artifact path / transcript / extracted text — one line]
**Summary:** route `{route}` — [2–3 sentences max]
**Issues:** [blockers, incl. missing key / API error / unreachable download host, or "None"]
```
