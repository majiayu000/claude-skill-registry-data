---
name: ozor-video-library
description: "Browse, inspect, re-export, embed, or iterate on videos that already exist in the user's Ozor.ai account. Use this skill whenever the user wants to work with past or in-progress Ozor videos rather than create a new one — e.g. 'list my Ozor videos', 'show my recent videos', 'what's the status of my last video', 'get the embed code for that video', 'download my last Ozor video', 'share link for the explainer I made', 'check on the export', 'send a follow-up edit to that video', 'show the plan for video X', 'render that video again at 9:16', 'is the job done yet'. This skill orchestrates list_videos, get_video, get_job, get_plan, update_plan, send_message, wait_for_job, export_video, wait_for_export, and get_embed_code. Do NOT use this skill to create a new video from scratch — use ozor-generate, ozor-document-video, or ozor-url-to-video."
---

# Ozor Video Library

Manage existing Ozor.ai videos via the MCP: list, inspect, re-export, embed, or send follow-up edits to the video agent. This skill is the "everything except creating from scratch" surface for `mcp__ozor__*`.

## When to use

Use this skill when the user wants to operate on **videos that already exist** in their Ozor account. Signals:
- "List / show my videos"
- "What's the status of ..."
- "Get the share link / download / embed for ..."
- "Re-export that video at 9:16"
- "Send a follow-up edit: change scene 2 to ..."
- "Show me the plan for that video"
- "Is the job done yet" / "check on the export"

**Do NOT use this skill when:**
- Creating a new video from text → `ozor-generate`
- Creating from a document/file → `ozor-document-video`
- Creating from a URL → `ozor-url-to-video`

## Required MCP tools

| Task | Tool |
|------|------|
| List recent videos | `mcp__ozor__list_videos` |
| Get one video's details | `mcp__ozor__get_video` |
| Check a build job status | `mcp__ozor__get_job` |
| Block until a job finishes | `mcp__ozor__wait_for_job` |
| Fetch the plan a video was built from | `mcp__ozor__get_plan` |
| Edit a plan | `mcp__ozor__update_plan` |
| Trigger a (new) export | `mcp__ozor__export_video` |
| Block until export ready | `mcp__ozor__wait_for_export` |
| Get `<iframe>` for embedding | `mcp__ozor__get_embed_code` |
| Send a follow-up edit message to the agent | `mcp__ozor__send_message` |
| List available voices | `mcp__ozor__list_voices` |

If the MCP isn't connected, tell the user and stop.

## Common workflows

### A. List recent videos

```
mcp__ozor__list_videos({ limit?: 10 })
```

Present as a table:

```
| # | Title | Status | Format | Updated | videoId |
|---|-------|--------|--------|---------|---------|
| 1 | ...   | exported | 16:9 | 2h ago | abc...  |
```

Offer 2–3 obvious next actions: "Want share links for any of these? An embed code? Re-export one as 9:16?"

### B. Get details for a specific video

If the user names a video or gives an ID:

```
mcp__ozor__get_video({ videoId })
```

Surface: title, current status (draft / building / exported / failed), format, duration, last update, and any URLs that exist (share, editor, download).

### C. "What's the status of my last video?"

1. `list_videos({ limit: 1 })` to find the most recent.
2. If `status` is `building`, also call `get_job` (or `wait_for_job` if the user wants to block until it's done) to get progress.
3. If `status` is `exported`, show the URLs.

### D. Get the embed code

```
mcp__ozor__get_embed_code({ videoId })
```

If the video hasn't been exported yet, run the export first (workflow F below).

### E. Get the share / download URL

If the video is already exported, `get_video` returns the URLs. If not:

```
mcp__ozor__export_video({ videoId })
mcp__ozor__wait_for_export({ videoId })
```

### F. Re-export (e.g. user wants a fresh render after edits, or the URL expired)

```
mcp__ozor__export_video({ videoId })
mcp__ozor__wait_for_export({ videoId })   // -> fresh shareUrl, editorUrl, downloadUrl
mcp__ozor__get_embed_code({ videoId })    // -> fresh iframe
```

### G. Re-render at a different format (e.g. landscape → vertical)

Format changes go through the plan:

1. `mcp__ozor__get_plan({ videoId })` — fetch the current plan
2. `mcp__ozor__update_plan({ planId, format: "9:16" })` — apply the change
3. `mcp__ozor__generate_from_plan({ planId })` is on the create-from-plan path — if the user wants the **same project** updated, prefer `send_message` instead (workflow H). If they want a **new project** at the new format, fall through to `generate_from_plan`, then export.

Note: `generate_from_plan` lives in `ozor-document-video` / `ozor-url-to-video` because it creates a fresh project. Tell the user when you're about to spin up a new project rather than mutating the existing one.

### H. Send a follow-up edit to the agent

For copy/visual/scene tweaks on an existing video without starting over:

```
mcp__ozor__send_message({
  videoId,
  message: "<the user's edit, e.g. 'In scene 2, change the headline to X and make the background lighter'>"
})
```

This typically returns a new `jobId`. Then:

```
mcp__ozor__wait_for_job({ videoId, jobId })
mcp__ozor__export_video({ videoId })
mcp__ozor__wait_for_export({ videoId })
```

Surface the fresh URLs afterwards.

### I. Inspect / edit a plan

```
mcp__ozor__get_plan({ videoId | planId })
```

Render the scenes as a numbered list to the user. If they want changes:

```
mcp__ozor__update_plan({ planId, ... })
```

Then re-fetch to confirm. Plan edits alone don't change the rendered video — they have to be followed by a regeneration (`send_message` for in-place, `generate_from_plan` for a new project) and an export.

### J. List voices

When the user is choosing or swapping a voice:

```
mcp__ozor__list_voices()
```

Present a compact list (name, language, style). If swapping, `update_plan({ planId, voice: "<voice id>" })` then regenerate.

## Disambiguating "that video" / "my last video"

If the user says "that video" or "my last one" without an ID:

1. `list_videos({ limit: 5 })`.
2. If exactly one matches the description, use it.
3. If multiple plausible matches, show the short list and ask which.

Don't silently pick a random video.

## Presenting URLs

Always present available URLs labeled:

```
**Share:** <shareUrl>
**Editor:** <editorUrl>
**Download:** <downloadUrl>
**Embed:** (in a code block)
```

If a URL doesn't exist yet (e.g. video never exported), don't fabricate one — tell the user what's missing and offer to run the export.

## Errors and recovery

- **`videoId` not found** → list recent videos and ask which one they meant.
- **Job failed** → relay the failure message verbatim; offer `send_message` with a fix or a re-export.
- **Export failed** → retry once; if it fails again, surface the error and recommend opening the editor URL to inspect.
- **Plan / video out of sync** (plan edited but not regenerated) → tell the user the changes are staged but not rendered, and offer to regenerate.

## Rules

1. **Never invent video IDs, share URLs, or status.** Everything comes from the MCP.
2. **For in-place edits, prefer `send_message`** over creating a new project via `generate_from_plan`. The user almost always wants the existing video updated, not a duplicate.
3. **Re-exports are cheap and safe** — if the user wants fresh URLs, just rerun export.
4. **When the user is vague about which video, ask** — show a short list, don't guess.
5. **Surface every URL after every regeneration or re-export.** Stale URLs from earlier in the conversation may have expired.
