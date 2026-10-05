---
name: drive-upload
description: Upload a file to Google Drive with 3-route fallback. Always defaults to the correct SHARED DRIVE (Marketing for OPC/McFolling/content, Higashi for mom's site). Use any time a file needs to land in Drive. Do not use for creating empty folders (use Drive MCP create_file with mimeType folder directly).
---

# Drive Upload — 3-Route Fallback

## When to use
- Uploading any file (image, PDF, video, transcript, script output) to Drive
- Saving content from scripts or GitHub Actions artifacts

## When NOT to use
- Creating empty folders → use `mcp__claude_ai_Google_Drive__create_file` (mimeType: folder) directly
- Writing content to an existing Google Doc → use `GOOGLEDOCS_UPDATE_DOCUMENT_MARKDOWN`
- Drive MCP `create_file` with `content=...` **ALWAYS fails silently** — do not use for file content

## Destination routing (MANDATORY check first)
- Higashi / Hig Negócios / mom's site / Alexandra → `0AN7aea2IZzE0Uk9PVA` (Higashi shared drive) → Claude Flow → Website folder `1CKWTojSg2uQmXjNnKlAaSBCTfxtSQBvH`
- OPC / Oak Park / McFolling / content / marketing → `0AIPzwsJD_qqzUk9PVA` (Marketing shared drive) → Claude Code Workspace
- NEVER upload to My Drive
- NEVER mix Higashi and Marketing

## 3 Routes

### Route A — OAuth resumable upload (preferred for any file > 5MB)
```
POST https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true
Authorization: Bearer <SHEETS_TOKEN access token>
Content-Type: application/json
Body: {"name": "<filename>", "parents": ["<SHARED_DRIVE_FOLDER_ID>"]}
```
- MUST include `supportsAllDrives=true` or shared drives return 404
- Get upload URL from `Location` header, then PUT the bytes
- Working implementation: `~/ClaudeWorkspace/_Scripts/build_carousel_v2.py` lines 15-100
- Also used in: `~/ClaudeWorkspace/_Scripts/daily_content_processor.py`

### Route B — Simple OAuth multipart (files < 5MB)
```
POST https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true
```
Same auth, metadata + media in a multipart body.

### Route C — MCP create_file (FOLDERS ONLY, never for content)
`mcp__claude_ai_Google_Drive__create_file` works perfectly for folders and empty Docs. Never attach `content` — it silently creates empty file.

## Verification (mandatory — do not skip)
After upload, confirm file lands in the correct shared drive path:
- Call `mcp__claude_ai_Google_Drive__search_files` with the filename
- Verify `parents` matches target folder ID
- Only then report "uploaded" with the Drive link

## Reference
- Full routing rules: `reference_active_connections.md`
- Working upload code: `~/ClaudeWorkspace/_Scripts/build_carousel_v2.py`
- 4AM agent uploads: `priihigashi/oak-park-ai-hub` → `scripts/4am_agent/` (GitHub)
