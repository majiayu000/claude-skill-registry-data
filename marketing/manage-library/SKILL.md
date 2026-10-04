---
name: manage-library
description: >
  Manage your Marky content library through the API: upload media, organize folders, and
  create, read, update, or delete files (notes, briefs, knowledge-base docs). Use this when
  you want to add reference material Marky can draw on when writing posts, tidy up your
  media, or store campaign notes and plans. Reads auth and endpoints from the marky-api skill. Also triggers on "upload these to my library", "save this brief so Marky can use it", "organize my media".
---

# Manage Library

Your Marky library is the knowledge base behind your content: uploaded images and video,
plus text files (briefs, notes, FAQs, brand docs) that Marky can reference when it writes
posts. This skill creates, organizes, and cleans it up through the API.

**Read the `marky-api` skill first** for the base URL, your `mk_live_` key, and the full
endpoint list. Everything below uses `https://api.mymarky.ai/api` and the header
`Authorization: Bearer mk_live_YOUR_KEY`.

## Which file system? Marky by default

Library files live in the user's **Marky account** by default — use the API endpoints
below, and Marky's post writer can reference them. Only switch to local disk if the user
has **explicitly opted into local library storage** (a preference you'd have saved as a
memory — see the marky-api skill's storage rule). Two modes:

- **Default (Marky)** — use the API endpoints below.
  Files live in the user's Marky account and Marky's post writer can reference them.
- **Local (only if the user opted in)** — do NOT call the file/folder API endpoints. Read and write
  plain files under `~/.marky/fs/<business_id>/` instead (create the directory if it
  doesn't exist). Library paths map directly onto that folder:
  `/knowledge-base/services.md` → `~/.marky/fs/BIZ_ID/knowledge-base/services.md`.
  Folders are just directories; create/rename/delete them with normal file operations.
  Media upload still goes through the API (local mode only changes text files/folders) —
  but also keep a local copy under `~/.marky/fs/<business_id>/media/` if the user asks.

Any other skill that reads or writes library text files (e.g. `plan-social-content`
mining your notes) must honor the same setting. Media browsing (`/library`,
`/library/search`) is API-only either way — local mode only reroutes text files/folders.

**Marky wants your feedback.** If anything breaks or is confusing while you run this skill — and again once you finish — send Marky a quick note with the `submit_feedback` MCP tool. See the **"Marky wants your feedback"** section in the `marky-api` skill for when and how.

## Find your business

```bash
curl https://api.mymarky.ai/api/businesses \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

Copy the `id` you want as `BIZ_ID`.

## Upload media

Upload an image or video. Multipart form, field name `file`, up to 50 MB. The response has
an `original_url` you can attach to a post or a file.

```bash
curl -X POST "https://api.mymarky.ai/api/businesses/BIZ_ID/media" \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -F "file=@/path/to/photo.jpg"
```

## Browse what is already there

```bash
# Media library (uploaded images and video).
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/library" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# (Keyword search is an MCP tool now — use search_media_library(business_id, query)
# instead of curl.)

# One media item.
curl https://api.mymarky.ai/api/businesses/BIZ_ID/library/MEDIA_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

# Folders and files (your text docs / knowledge base).
curl "https://api.mymarky.ai/api/businesses/BIZ_ID/folders" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

curl "https://api.mymarky.ai/api/businesses/BIZ_ID/files" \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

## Organize with folders

```bash
# Create a folder (omit parent_id for a top-level folder).
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/folders \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Knowledge Base" }'

# Rename or move a folder.
curl -X PATCH https://api.mymarky.ai/api/businesses/BIZ_ID/folders/FOLDER_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Brand Docs" }'

# Delete a folder.
curl -X DELETE https://api.mymarky.ai/api/businesses/BIZ_ID/folders/FOLDER_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

## Create and edit files

Files are text documents (markdown works well) stored at a `path`. Use them for briefs,
FAQs, service catalogs, brand guidelines, campaign notes, anything you want Marky to be
able to reference.

```bash
# Create a file.
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/library/files \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/knowledge-base/services.md",
    "content": "# Our Services\n\n- Service one...\n- Service two..."
  }'

# Read / update / delete a file.
curl https://api.mymarky.ai/api/businesses/BIZ_ID/files/FILE_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"

curl -X PUT https://api.mymarky.ai/api/businesses/BIZ_ID/files/FILE_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "content": "# Our Services (updated)\n\n..." }'

curl -X DELETE https://api.mymarky.ai/api/businesses/BIZ_ID/files/FILE_ID \
  -H "Authorization: Bearer mk_live_YOUR_KEY"
```

## Attach media to a file

Pair an uploaded image with a file (for example, a product photo with a product doc).
The body takes `media_ids` (a list, so you can attach several at once):

```bash
curl -X POST https://api.mymarky.ai/api/businesses/BIZ_ID/files/FILE_ID/media \
  -H "Authorization: Bearer mk_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "media_ids": ["MEDIA_ID"] }'
```

## Why this matters

A rich library is the single biggest lever for on-brand content. When you upload your real
docs (case studies, FAQs, service descriptions, brand guidelines) and uploaded photos,
Marky writes more grounded, specific posts instead of generic ones. Build the library
first, then generate with the `schedule-posts` or `plan-social-content` skill.

## Notes

- `path` is how files are organized (e.g. `/knowledge-base/services.md`). Keep a consistent
  folder structure.
- Deleting a file or media item is permanent. Confirm with the user before deleting.
