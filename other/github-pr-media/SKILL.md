---
name: github-pr-media
description: "Upload a local image or video file to GitHub's user-attachments API and embed the returned hosted URL in a pull request description or comment. Use when asked to add screenshots, before/after images, diagrams, screen recordings, or other media to a PR/issue body or comment. Triggers on requests like \"attach this screenshot to the PR\", \"add the before/after images\", \"embed this recording in the description\", or when a PR body needs visual evidence of a UI change. Does NOT handle remote URLs, image generation, or text-only diffs."
metadata:
   version: 0.2.2
---

# GitHub PR Media Uploads

Upload local images/videos to GitHub and embed them as markdown in a PR description or comment.

## Workflow overview

1. **Check eligibility** — a real local media file, and a GitHub destination
2. **Run the upload script** — `scripts/upload-asset.ps1` (or curl fallback below)
3. **Embed the returned URL** — `![...](url)` for images, bare URL line for videos

## Step 1: Check eligibility (do not upload speculatively)

Only proceed when **all** of the following hold:

- A **concrete local file path** exists in the conversation — absolute or relative — for an image (png, jpg, jpeg, gif, webp, svg) or video (mov, mp4, webm).
- The destination is GitHub — a PR description, issue body, PR/issue comment.
- A visual genuinely improves reviewer understanding (before/after screenshots, architecture diagrams, behavior recordings).

**Otherwise, do not upload.** Output a `no-op:` note and stop. Never invent a path, never upload a placeholder, never upload from a remote URL. "Should I add a screenshot?" is a question, not a trigger.

## Step 2: Upload and get the hosted URL

### Preferred: run the wrapper script (Windows/pwsh)

```powershell
pwsh -NoProfile -File skills/github-pr-media/scripts/upload-asset.ps1 `
  -FilePath "before.png" [-Repository "owner/name"]
```

The script resolves auth and the repository ID from `git remote`, derives the MIME type from the extension, URL-encodes the filename, enforces size limits, checks the HTTP status, and emits the asset URL on stdout. Pass `-Repository` only when uploading from a worktree whose remote is not the target repo. Run it **once per file** — never batch.

### Fallback: curl (any OS)

1. Authenticate and resolve the repository database ID:
   ```bash
   TOKEN=$(gh auth token)
   REPO_ID=$(gh api "repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)" --jq .id)
   ```

2. URL-encode the filename and MIME type — **required**: curl rejects raw spaces/special characters in URLs (empirically verified):
   ```bash
   ENC_NAME=$(printf '%s' "before.png" | jq -sRr @uri)        # or [uri]::EscapeDataString in pwsh
   ENC_MIME=$(printf '%s' "image/png" | jq -sRr @uri)
   ```

3. Upload raw bytes; capture the HTTP code:
   ```bash
   RESPONSE=$(curl -s -w "\n%{http_code}" \
     "https://uploads.github.com/user-attachments/assets?name=$ENC_NAME&content_type=$ENC_MIME&repository_id=$REPO_ID" \
     -X POST \
     -H "Content-Type: application/octet-stream" \
     -H "Accept: application/json" \
     -H "X-GitHub-Api-Version: 2022-11-28" \
     -H "Authorization: Bearer $TOKEN" \
     --data-binary "@before.png")
   HTTP_CODE=$(echo "$RESPONSE" | tail -1)
   BODY=$(echo "$RESPONSE" | sed '$d')
   ```

4. Validate the response — success is HTTP **201** with a JSON `url` field:
   ```bash
   [ "$HTTP_CODE" = "201" ] || { echo "Upload failed: HTTP $HTTP_CODE — $BODY" >&2; exit 1; }
   URL=$(echo "$BODY" | jq -r '.url // empty')
   [ -n "$URL" ] || { echo "No 'url' in response: $BODY" >&2; exit 1; }
   echo "$URL"
   ```
   Response shape (empirically verified 2026-08):
   ```json
   {"url": "https://github.com/user-attachments/assets/<uuid>"}
   ```

## Step 3: Embed the URL in markdown

- **Images** (png, jpg, jpeg, gif, webp, svg): `![before.png](https://github.com/user-attachments/assets/...)`
- **Videos** (mov, mp4, webm): paste the URL on its own line — GitHub auto-renders video URLs, and `![](url)` would break that.

## Limits and constraints (from docs.github.com "Attaching files")

| File type | Max size |
|---|---|
| Images and GIFs | 10 MB |
| Videos (paid GitHub plan) | 100 MB |
| Videos (free plan) | 10 MB |
| Other files | 25 MB |

The wrapper script enforces these; for curl, check the size before uploading.

## MIME types by extension

| Extension | content_type |
|---|---|
| `.png` | `image/png` |
| `.jpg`, `.jpeg` | `image/jpeg` |
| `.gif` | `image/gif` |
| `.webp` | `image/webp` |
| `.svg` | `image/svg+xml` |
| `.mov` | `video/quicktime` |
| `.mp4` | `video/mp4` |
| `.webm` | `video/webm` |

For videos prefer H.264 encoding for widest browser compatibility.

## Verifying your upload rendered

- **Uploaded URL behavior**: `github.com/user-attachments/assets/<uuid>` responds with a 302 redirect to an S3 object (`github-production-user-asset-...s3.amazonaws.com`) that serves the file bytes. A plain `GET` (e.g. `Invoke-WebRequest`, browser) follows it automatically; `HEAD` may return 403 — that is expected, browsers use GET.
- **Image visibly renders** only if the file is a real, non-trivial image. A 1×1 pixel PNG (e.g. a generated placeholder) is technically "rendered" but invisible — always verify with a visually meaningful test file (real screenshot dimensions).
- **Markdown render check** (without opening GitHub): call the rendering API and confirm an `<img>` tag is produced:
  ```bash
  gh api -X POST markdown -f "text=![name]($url)" -f "mode=gfm"
  # expect: <p><img src="...user-attachments/assets/..." ...></p>
  ```
- **Retrieve the bytes** the browser would get:
  ```bash
  curl -sL -o downloaded.png "$url"   # follows the 302 to S3; verify size/dimensions
  ```

## Troubleshooting

- **HTTP 401** — token invalid or missing scopes (`repo`). Run `gh auth status`.
- **HTTP 404** — repository ID wrong, or repo is private and token lacks access.
- **HTTP 422** — invalid `content_type`, unsupported extension, or name/length issue.
- **HTTP 502** — transient upstream failure; retry once.
- **No `url` in response** — the endpoint moved or rejected auth; re-check headers.
- **Cleanup**: there is **no list/delete API** for user attachments (DELETE returns 404, verified 2026-08). Remove unwanted assets manually in the GitHub web UI under the uploaded conversation.

## When not to use it

- Text-only changes where the diff already explains everything
- A simple markdown list or code snippet is clearer than an image
- The media is already hosted remotely (S3, Slack, etc.) — link it directly
