---
name: notion-upload
description: Upload local image files to a Notion page using the Notion File Upload REST API. Use when the user wants to embed local images (PNG, JPG, etc.) into a Notion page.
argument-hint: "<notion_page_url_or_id> <file_path(s) or glob pattern>"
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
---

# Notion File Upload

You are uploading local image files to a Notion page via the Notion File Upload REST API (3-step process).

## Step 1: Parse arguments and resolve files

- `$ARGUMENTS` contains a Notion page URL or ID, followed by one or more file paths or a glob pattern.
- Extract the page ID from the URL if needed (strip `https://www.notion.so/` prefix, extract 32-char hex ID).
- Resolve file paths using Glob if a pattern is given (e.g., `notebooks/figures/*.png`).
- Verify all files exist and are images (PNG, JPG, GIF, SVG, WEBP).
- List the files and ask the user to confirm before uploading.

## Step 2: Get the Notion integration token

Look for `NOTION_API_TOKEN` in these locations (in order):
1. Project `.env` file
2. Environment variable `NOTION_API_TOKEN`

If not found, tell the user:
> Create a Notion integration at https://www.notion.so/profile/integrations, share the target page with it, then set `NOTION_API_TOKEN=ntn_...` in your `.env` file.

## Step 3: Upload each file

For each image file, run these 3 API calls:

### 3a. Create file upload object
```bash
curl -s -X POST "https://api.notion.com/v1/file_uploads" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{}'
```
Extract the `id` from the JSON response.

### 3b. Send the file data
```bash
curl -s -X POST "https://api.notion.com/v1/file_uploads/$UPLOAD_ID/send" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -F "file=@$FILEPATH"
```
Verify the response has `"status": "uploaded"`. If not, report the error and skip this file.

### 3c. Collect upload IDs
Store all successful `(upload_id, filename)` pairs for the batch append.

## Step 4: Append image blocks to the page

Use Python to build the JSON payload and send a single PATCH request:

```python
import json, subprocess

children = []
for upload_id, filename in successful_uploads:
    caption = filename.rsplit('.', 1)[0].replace('_', ' ').title()
    children.append({
        "type": "image",
        "image": {
            "type": "file_upload",
            "file_upload": {"id": upload_id},
            "caption": [{"type": "text", "text": {"content": caption}}]
        }
    })

payload = json.dumps({"children": children})
subprocess.run([
    "curl", "-s", "-X", "PATCH",
    f"https://api.notion.com/v1/blocks/{page_id}/children",
    "-H", f"Authorization: Bearer {token}",
    "-H", "Content-Type: application/json",
    "-H", "Notion-Version: 2022-06-28",
    "-d", payload
], capture_output=True, text=True)
```

Use the filename (without extension, underscores → spaces, title-cased) as the default caption.

## Step 5: Report results

Print a summary:
- Number of files uploaded: X / Y
- Notion page URL: `https://www.notion.so/<page_id>`
- Any failures with error messages
- Note: images are appended at the END of the page — drag them into position in the Notion UI.

## Error handling

- **401 Unauthorized**: Token is invalid or expired. Ask user to regenerate at notion.so/profile/integrations.
- **403 Forbidden**: Page not shared with the integration. Ask user to add the connection via the page's "..." menu > Connections.
- **413 Too Large**: File exceeds 20 MB limit. Skip and report.
- **File not found**: Skip missing files with a warning.
