---
name: ozor-url-to-video
description: "Turn any URL — landing page, blog post, product page, documentation page, changelog, public PDF, or web article — into a finished AI-generated video using the Ozor MCP. Use this skill whenever the user gives a link and wants a video from its content: 'make a video from this URL', 'video from my landing page', 'turn this blog post into a video', 'video from https://...', 'video from our homepage', 'generate a video from this product page', 'create a video from this article'. This skill runs analyze_document with the url parameter (no scraping needed on our side), presents the resulting plan to the user, then generates → exports → embeds. Do NOT use this skill for a short text brief (use ozor-generate) or for an attached local file (use ozor-document-video)."
---

# Ozor URL-to-Video

End-to-end web-page-to-video on Ozor.ai. Hand Ozor a URL, get a plan back that reflects the actual page content (headlines, value props, social proof, CTA), approve or edit, and ship a finished video.

## When to use

Use this skill when the input is a **URL**. Signals:
- "Make a video from https://..."
- "Video from my landing page / homepage / product page"
- "Turn this blog post into a video"
- "Video from this article / changelog page"
- Any message that contains a URL the user expects you to read

**Do NOT use this skill when:**
- Input is a short text brief → `ozor-generate`
- Input is an attached local file (PDF/PPTX/DOCX) → `ozor-document-video`
- User wants a written prompt only → `ozor-landing-page-to-video` (prompt-only skill)
- User wants to manage existing videos → `ozor-video-library`

## Required MCP tools

- `mcp__ozor__analyze_document` — accepts a `url` parameter directly; no upload needed
- `mcp__ozor__get_plan` / `mcp__ozor__update_plan` — review/edit the plan before generation
- `mcp__ozor__generate_from_plan` — kicks off the build, returns `projectId`
- `mcp__ozor__wait_for_job` — if the response includes a `jobId`
- `mcp__ozor__export_video`, `mcp__ozor__wait_for_export`
- `mcp__ozor__get_embed_code`

If the MCP isn't connected, tell the user and stop. **Do not browse the URL yourself and hand-write a prompt** — Ozor extracts brand colors, hero imagery, and structure directly from the page. Your scraped text would lose that.

## Workflow

### Step 1 — Hand the URL to Ozor

```
mcp__ozor__analyze_document({
  url: "<the URL>",
  ...optional hints: targetDuration, format, audience, tone, focus
})
```

For URLs:
- **Landing pages / product pages** → default to `format: "9:16"` or `"16:9"` (ask if not obvious — vertical is great for social, landscape for embedding on the site itself), `targetDuration: "30s"`–`"45s"`, tone `"confident"`.
- **Blog posts / articles** → `format: "16:9"`, `targetDuration: "60s"`–`"90s"`, tone `"informative"`.
- **Changelog / release pages** → `format: "16:9"`, `targetDuration: "30s"`–`"45s"`, tone `"energetic"`, focus `"one scene per shipped feature"`.
- **Documentation pages** → `format: "16:9"`, `targetDuration: "60s"`, tone `"clear, technical"`, focus `"explain what this feature does and how to use it"`.

Returns `{ planId, plan }`.

### Step 2 — Present the plan and STOP

Render the plan to the user concisely:

```
📋 Ozor plan for <URL>

**Source:** <page title or domain>
**Format:** 16:9 / 9:16
**Estimated duration:** ~X seconds
**Detected brand:** <colors / product name if Ozor surfaced them>
**Scenes:** N

(1) <scene title> — <one-line direction>
(2) <scene title> — <one-line direction>
...

Approve as-is, or change anything? You can edit scenes, swap format, change tone, or shift focus.
```

**Wait for approval.** Don't call `generate_from_plan` yet.

### Step 3 — Apply edits (if any)

Use `mcp__ozor__update_plan({ planId, ... })`. Re-show the plan with `get_plan`. Loop until approved.

### Step 4 — Generate

```
mcp__ozor__generate_from_plan({ planId })   // -> { projectId, jobId? }
```

If a `jobId` comes back, `mcp__ozor__wait_for_job({ videoId: projectId, jobId })`.

### Step 5 — Export

```
mcp__ozor__export_video({ videoId: projectId })
mcp__ozor__wait_for_export({ videoId: projectId })   // -> shareUrl, editorUrl, downloadUrl
```

### Step 6 — Embed

```
mcp__ozor__get_embed_code({ videoId: projectId })
```

### Step 7 — Present results

```
🎬 Video ready from <URL>

**Share:** <shareUrl>
**Editor:** <editorUrl>
**Download:** <downloadUrl>

**Embed (drop this on your site):**
```html
<iframe ...></iframe>
```

Want a vertical 9:16 cut for social, or a longer 90s explainer version? I can regenerate from the same plan.
```

## What the URL flow does best

- **Landing pages** — Ozor picks up the hero headline, the value prop, social proof, the CTA, and brand colors. Your prompt would lose all of that.
- **Blog posts** — picks up the thesis and section structure; produces an explainer that maps to the article.
- **Changelogs** — naturally maps each release/feature to its own scene.
- **Product pages** — pulls product screenshots / hero imagery into scenes when available.

## Format-decision heuristic

If the user didn't say:

- URL is a homepage or product page **and** the obvious use case is social/ads → `9:16`
- URL is a homepage or product page **and** the obvious use case is embedding on the page itself → `16:9`
- URL is a blog / article / doc / changelog → `16:9`

When ambiguous, propose `16:9` as default and offer a `9:16` rerun at the end.

## Variants worth offering after the first render

Mention these only after the user has the first video — don't preemptively generate them:

- **9:16 social cut** of a landscape video → regenerate from the same plan with `update_plan({ planId, format: "9:16" })`.
- **Short teaser (15s)** + **full explainer (60s)** from the same page.
- **Two audiences** (e.g. "technical buyer" vs "executive buyer") — re-analyze with a different `audience` hint.

## Errors and recovery

- **`analyze_document` returns a thin plan** (often: paywalled page, JS-rendered SPA Ozor couldn't read) → tell the user, ask for an alternative URL or whether they can paste the key content as a brief for `ozor-generate`.
- **Detected brand colors look wrong** → `update_plan` with corrected colors before generating.
- **Generation fails** → check the scene the error references, fix via `update_plan`, retry.
- **Export hangs** → call `wait_for_export` again; it resumes.

## Rules

1. **Always pass the URL to `analyze_document`.** Never scrape the page yourself and route to `generate_video` — that throws away Ozor's brand and visual extraction.
2. **Always show the plan and wait for approval** before `generate_from_plan`. The plan is where format and tone get locked in.
3. **Use `projectId` as `videoId`** for export, wait_for_export, and embed.
4. **Surface every URL** — share, editor, download, embed.
5. **Propose, don't pre-generate, variants.** Don't burn renders on 9:16 + 16:9 + teaser without being asked.
