---
name: ozor-document-video
description: "Turn a real document (PDF, PPTX, DOCX, Keynote export, slide deck, proposal, whitepaper, report) into a finished AI-generated video using the Ozor MCP. Use this skill whenever the user attaches, uploads, references, or points to a document file and wants a video from it — e.g. 'make a video from this pitch deck', 'turn this PDF into a video', 'video from my proposal.docx', 'generate a video from this PowerPoint', 'create a video from this report', 'this whitepaper → video'. This skill runs the document-to-video pipeline: analyze_document → present the plan to the user → update_plan if needed → generate_from_plan → export_video → wait_for_export → get_embed_code. It always uses the plan-based flow so slide visuals are preserved. Do NOT use this skill for plain-text creative briefs (use ozor-generate) or for URLs/landing pages (use ozor-url-to-video)."
---

# Ozor Document-to-Video

End-to-end document-to-video on Ozor.ai. Takes a real file (PDF, PPTX, DOCX, etc.), analyzes it on Ozor's side to produce a structured plan, lets the user approve/edit the plan, then generates and exports a finished video — preserving slide visuals along the way.

## When to use

Use this skill when the input is a **document/file**. Signals:
- User attached or referenced a PDF, PPTX, DOCX, Keynote export, slide deck, proposal, whitepaper, report, one-pager
- "Turn this deck into a video"
- "Make a video from this PDF"
- "Video from my pitch / proposal / report"

**Do NOT use this skill when:**
- Input is a short creative text brief → `ozor-generate`
- Input is a URL or landing page → `ozor-url-to-video`
- User only wants a written Ozor prompt → `ozor-doc-to-video` (prompt-only skill)
- User wants to manage existing videos → `ozor-video-library`

## Required MCP tools

- `mcp__ozor__analyze_document` — analyzes the doc, returns a `planId` plus the structured plan
- `mcp__ozor__prepare_document_upload` — gets a curl-uploadable URL for local files with no public URL (the common path)
- `mcp__ozor__get_plan` — fetches the latest plan state
- `mcp__ozor__update_plan` — applies user edits to the plan before generation
- `mcp__ozor__generate_from_plan` — kicks off the video build from the approved plan, returns `projectId`
- `mcp__ozor__export_video` — starts the render (use the `projectId` as `videoId`)
- `mcp__ozor__wait_for_export` — blocks until the render is ready
- `mcp__ozor__get_embed_code` — returns the `<iframe>` HTML

If the Ozor MCP isn't connected, tell the user and stop. Do not extract content yourself and fall back to `generate_video` with a hand-written script — that loses the slide visuals and overflows the 2000-char prompt limit. **The plan-based flow is mandatory for documents.**

## Workflow

### Step 1 — Get the document to Ozor

Pick the best source, in priority order:

1. **Public URL** → pass `url` directly to `analyze_document`. No size limit, no token cost. Best whenever available.
2. **Local file (the common case)** → call `mcp__ozor__prepare_document_upload`, then run the returned curl command to push the bytes directly to Ozor's storage. Bytes never traverse a tool call, so files up to ~50 MB work. Use this for any multi-MB PDF/PPTX/DOCX the user has uploaded into the conversation.
3. **`fileBase64` + `fileName` on `analyze_document`** → only for small files (≲ a few hundred KB). Avoid for big decks — it burns tokens.

If `prepare_document_upload` isn't in the tool list, uploads are disabled on this server — fall back to a URL or small base64.

### Step 2 — Analyze the document

Once Ozor has the file, call:

```
mcp__ozor__analyze_document({
  url | uploadId | fileBase64+fileName,
  ...optional hints: targetDuration, format (16:9 / 9:16), audience, tone
})
```

This returns `{ planId, plan }`. The plan contains the proposed scenes, narration, visual notes, and which slides/pages map to which scenes.

### Step 3 — Present the plan to the user and STOP

**This is the critical step.** Do NOT skip to generation. Show the user a concise rendering of the plan:

```
📋 Ozor plan for "<document name>"

**Format:** 16:9 (or 9:16)
**Estimated duration:** ~X seconds
**Scenes:** N

(1) <scene title> — <one-line narration / visual>
(2) <scene title> — <one-line narration / visual>
...

Want me to generate this as-is, or change anything? You can:
- Edit a scene ("change scene 2 to ...")
- Reorder / drop / add scenes
- Change tone, length, or format
- Approve and generate
```

Then **wait** for the user to approve or request edits. Do not call `generate_from_plan` on your own initiative — the plan is the user's checkpoint for cost and creative control.

### Step 4 — Apply edits (if any)

If the user requests changes, call `mcp__ozor__update_plan({ planId, ... })` with the edits. Re-fetch with `get_plan` and re-show the updated plan. Loop until the user approves.

### Step 5 — Generate from the plan

When the user approves:

```
mcp__ozor__generate_from_plan({ planId })
```

This returns `{ projectId }`. Use `projectId` as `videoId` for every subsequent call.

If the response includes a `jobId`, wait on it with `wait_for_job({ videoId: projectId, jobId })`. Otherwise proceed to export.

### Step 6 — Export

```
mcp__ozor__export_video({ videoId: projectId })
mcp__ozor__wait_for_export({ videoId: projectId })
```

Returns `shareUrl`, `editorUrl`, `downloadUrl`.

### Step 7 — Embed

```
mcp__ozor__get_embed_code({ videoId: projectId })
```

### Step 8 — Present results

```
🎬 Video ready from "<document name>"

**Share:** <shareUrl>
**Editor:** <editorUrl>
**Download:** <downloadUrl>

**Embed:**
```html
<iframe ...></iframe>
```

Want a 9:16 social cut from the same plan? I can regenerate.
```

## Hints to pass into `analyze_document`

Pass any of these if the user mentioned them or they're obvious from the document:

- `targetDuration` — e.g. `"60s"`, `"90s"`. Default ~60s for proposals/decks, ~30s for one-pagers.
- `format` — `"16:9"` (default) or `"9:16"` for social.
- `audience` — investors, customers, developers, internal team, ...
- `tone` — confident, warm, technical, energetic, ...
- `focus` — optional, a one-line note like "lean into the metrics on slide 4" or "skip the team slide".

## Adaptation by document type

| Document | Default duration | Format | Tone | Focus |
|----------|------------------|--------|------|-------|
| Pitch deck | 60–90s | 16:9 | Confident | Problem → solution → traction → CTA |
| Proposal (DOCX) | 60s | 16:9 | Professional | Outcomes + price + next step |
| Whitepaper / report | 60–90s | 16:9 | Authoritative | 3 key findings, link to full doc in CTA |
| Sales one-pager | 30–45s | 16:9 | Punchy | Hook → 3 benefits → CTA |
| Release notes | 30–45s | 16:9 | Energetic | One scene per feature |
| Training / SOP | 90s+ | 16:9 | Calm, clear | Numbered steps, split into a series if > 7 scenes |

When in doubt, propose a default in your initial call and let the user override after seeing the plan.

## Iterating after generation

If the rendered video needs changes:
- Small narration/copy tweaks → `update_plan` + regenerate (this re-runs from the plan, no need to re-analyze the doc)
- New scene order or tone → same path
- New focus or audience → may be cheaper to call `analyze_document` again with stronger hints

## Errors and recovery

- **`analyze_document` fails because the file is too big** → use `prepare_document_upload` instead of base64.
- **The plan has missing or wrong content** → call `update_plan` with corrections rather than restarting.
- **`generate_from_plan` fails** → the error usually points at a specific scene. Fix via `update_plan`, retry.
- **Export hangs** → safe to call `wait_for_export` again; it resumes.

## Rules

1. **Always go plan-first.** Never call `generate_video` with hand-written prose extracted from the document. The whole point of this skill is that Ozor sees the slides directly.
2. **Always show the plan to the user and wait for approval** before `generate_from_plan`. Generation is the expensive step; the plan is the checkpoint.
3. **For local files, use `prepare_document_upload` + curl.** Base64 is for tiny files only.
4. **Use `projectId` as `videoId` everywhere after `generate_from_plan`.** It's the same identifier.
5. **Surface every URL** — share, editor, download, embed.
6. **Don't summarize the document yourself** — Ozor's `analyze_document` does that and preserves visuals. Your job is to orchestrate the MCP and curate the plan, not to rewrite the content.
