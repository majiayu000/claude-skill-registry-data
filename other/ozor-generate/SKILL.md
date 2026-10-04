---
name: ozor-generate
description: "Generate an AI video end-to-end on Ozor.ai from a short text brief. Use this skill whenever the user wants to actually create a video (not just write a prompt) from a creative description, idea, or short brief — e.g. 'make me a video about X', 'generate a launch video for Y', 'create an explainer for Z', 'render a video', 'produce a 30s ad about ...', 'spin up a quick video for our new feature'. This skill runs the full Ozor MCP pipeline: generate_video → wait_for_job → export_video → wait_for_export → get_embed_code, and returns the shareUrl, editorUrl, downloadUrl, and a ready-to-paste <iframe> embed. Do NOT use this skill when the input is a document/PDF/PPTX/deck/URL — use ozor-document-video or ozor-url-to-video instead."
---

# Ozor Generate (Text-to-Video)

End-to-end video generation on Ozor.ai using the `mcp__ozor__*` tools. This skill takes a short creative brief and returns a finished, exported, shareable video — not just a prompt.

## When to use

Use this skill when the user wants to **actually produce a video** from a short text idea. Signals:
- "Make a video about ..."
- "Generate a launch video for ..."
- "Create a 30-second explainer about ..."
- "Spin up an ad for our new feature ..."
- "Render a video that says ..."

**Do NOT use this skill when:**
- The user has a document, PDF, PPTX, DOCX, deck, or file → use `ozor-document-video`
- The user gives a URL / landing page → use `ozor-url-to-video`
- The user just wants help **writing** an Ozor prompt without generating → use `ozor-video-best-practices`
- The user wants to manage existing videos → use `ozor-video-library`

## Required MCP tools

This skill assumes the Ozor MCP is connected. The tools are:

- `mcp__ozor__generate_video` — kicks off a text-to-video job
- `mcp__ozor__wait_for_job` — blocks until the agent finishes building the project
- `mcp__ozor__export_video` — starts the render
- `mcp__ozor__wait_for_export` — blocks until the render is ready, returns URLs
- `mcp__ozor__get_embed_code` — returns the `<iframe>` HTML
- `mcp__ozor__list_voices` — optional, lookup of available voices
- `mcp__ozor__send_message` — optional, follow-up edits to the video agent

If the Ozor MCP is not connected, tell the user to add it and stop — do not try to fall back to writing a prompt-only output.

## Workflow

### Step 1 — Shape the brief

The Ozor prompt is capped at **2000 characters** and should describe **one short video**. Before calling the MCP, make sure the brief includes:

- **What the video is about** in one sentence
- **Audience** (founders, developers, customers, general public, ...)
- **Format** — 16:9 (default, landscape) or 9:16 (vertical for social)
- **Approximate duration** — typically 15–90 seconds
- **Number of scenes** (3–6 is the sweet spot)
- **Tone** (confident, warm, energetic, technical, ...)
- **Visual style** (dark/light, color accent, minimal/bold)
- **A clear CTA** for the final scene

If any of these are missing AND the gap meaningfully changes the output, ask **one** focused question. Otherwise pick a sensible default and proceed — auto-mode behavior.

**Never paste a multi-scene script extracted from a document into this prompt.** That overflows the 2000-char limit and loses slide visuals. For documents, switch to `ozor-document-video`.

### Step 2 — Generate

Call:

```
mcp__ozor__generate_video({
  prompt: "<the compiled brief, under 2000 chars>",
  export: true   // recommended: triggers export automatically so you can skip step 4
})
```

This returns `{ videoId, jobId }`. Surface to the user that the job has started and that you're waiting on it.

### Step 3 — Wait for the build

Call:

```
mcp__ozor__wait_for_job({ videoId, jobId })
```

This blocks until the Ozor agent has finished building the project. If it fails, the error message will usually tell you what to fix in the prompt — relay it to the user and offer to retry with adjustments.

### Step 4 — Export (skip if you passed `export: true`)

If you did not pass `export: true` in step 2, call:

```
mcp__ozor__export_video({ videoId })
```

### Step 5 — Wait for the render

Call:

```
mcp__ozor__wait_for_export({ videoId })
```

This returns the final URLs:
- `shareUrl` — public link to the rendered video
- `editorUrl` — Ozor editor link for further tweaks
- `downloadUrl` — direct MP4 download

### Step 6 — Get the embed

Call:

```
mcp__ozor__get_embed_code({ videoId })
```

Returns a ready-to-paste `<iframe>` snippet.

### Step 7 — Present results to the user

Output in this format:

```
🎬 Video ready

**Share:** <shareUrl>
**Editor:** <editorUrl>
**Download:** <downloadUrl>

**Embed:**
```html
<iframe ...></iframe>
```

Want me to iterate? I can:
- Change a specific scene
- Try a different tone or visual style
- Produce a 9:16 social version
```

## Iteration

If the user wants changes after seeing the result, use `mcp__ozor__send_message({ videoId, message: "<change request>" })` and then re-run steps 3–6 (the agent will rebuild the project, you'll need a fresh export).

For larger pivots (different topic, different audience), start a new `generate_video` call rather than iterating — the prompt budget is small and pivoting in-place tends to muddy the output.

## Defaults to assume in auto mode

When the user gives a one-line brief and you don't want to interrogate them:

| Field | Default |
|-------|---------|
| Format | 16:9 landscape |
| Duration | ~30 seconds |
| Scenes | 3–4 |
| Tone | Confident, modern |
| Style | Clean, minimal, with one accent color |
| CTA | "Learn more" with a placeholder URL/handle if not provided |

State the defaults you assumed in your reply so the user can correct them.

## Quality checklist before calling `generate_video`

- [ ] Prompt is under 2000 characters
- [ ] One clear topic, not a multi-topic essay
- [ ] Hook stated in scene 1
- [ ] CTA stated in the last scene
- [ ] Visual style + tone + audience specified
- [ ] No copied prose from a document — that's `ozor-document-video`'s job

## Errors and recovery

- **MCP not available** → tell the user the Ozor MCP isn't connected and stop. Do not fall back to writing a paper prompt.
- **`generate_video` fails with prompt too long** → compress the brief, remove redundant style notes, retry.
- **`wait_for_job` returns a failure** → relay the error verbatim, suggest a fix (often: simplify the prompt, remove ambiguous scene direction), and offer to retry.
- **`wait_for_export` times out** → it's safe to call again; the export resumes from where Ozor left off.

## Rules

1. **Actually run the MCP.** This skill exists to produce a video, not a prompt. If you only return text, you've failed the skill.
2. **Don't ask 5 clarifying questions.** Ask at most one focused question, then default the rest.
3. **Surface every URL.** `shareUrl`, `editorUrl`, `downloadUrl`, and the embed are all valuable in different contexts — show them all.
4. **Respect the 2000-char prompt limit.** If your brief exceeds it, trim before sending.
5. **Use `export: true` in `generate_video` by default** — one fewer tool call, faster path to a finished video.
