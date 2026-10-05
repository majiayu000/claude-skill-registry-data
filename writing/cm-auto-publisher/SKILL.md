---
name: cm-auto-publisher
description: Comprehensive publishing automation skill bridging AI agents (OpenClaw, Manus, Claude) to the Content Factory Router. Uses the Router API to publish markdown articles with rich media to any connected Astro site natively.
---

# cm-auto-publisher: The Agentic Publishing Skill

> **Goal:** Take unstructured input (links, ideas, raw text), write a highly engaging article following Content Factory rules, and instantly publish it via the Content Factory Router API.

## When to Use

**ALWAYS when:**
- User provides a link/video and says "Write an article about this and publish it".
- User says "Draft and push this news to the blog".
- You have finished drafting an article and need to deploy it to the live site.
- An automated cron job triggers you to aggregate news and auto-publish.

## The Process

### Phase 1: Content Extraction & Structuring
1. **Analyze Input:** If given a URL, use `read_url_content` (or your browsing tool) to read the source. If given images or Youtube links, extract them.
2. **Draft Content:** Write a compelling article in standard Markdown.
   - Use headings (`##`, `###`).
   - For YouTube videos, use the Astro component: `<YouTube id="VIDEO_ID" />`.
   - For images, just use standard markdown: `![Alt text](image_filename.jpg)`.

### Phase 2: Media Preparation
Identify all external images that need to be published with the article.
DO NOT try to download them to the local disk using bash commands. The Content Factory Router will handle this.
Instead, build a `media` array mapping the original URLs to the desired clean filenames.

```json
"media": [
  {
    "url": "https://source.com/raw-image-123.jpg",
    "filename": "clean-seo-friendly-name.jpg"
  }
]
```

### Phase 3: API Payload Construction
Construct the JSON payload matching the target site's schema.
Standard Target: `cody-master` (mapped to `tody-agent/todyle-web`).

```json
{
  "site_id": "cody-master",
  "title": "[Engaging Title]",
  "description": "[1-2 sentence SEO meta description]",
  "category": "news", // or "guide", "use-case"
  "readingTime": "5 min read",
  "tags": ["AI", "Vibe Coding", "Automation"],
  "content": "The raw markdown content here...",
  "media": [ ... ]
}
```

### Phase 4: Publish via Router API
Send the payload to the Cloudflare Worker via a standard `fetch` or `curl` command.

1. **Get the Secret:** Retrieve the API token from the `.env` file or ask the user for the `PUBLISHER_API_KEY`.
2. **Send POST Request:**
   Use a local script or curl to send the data to the worker.

```bash
# Example curl (assuming the payload is saved to payload.json)
curl -X POST https://content-factory-router.<YOUR-CLOUDFLARE-ACCOUNT>.workers.dev/publish \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <API_KEY>" \
  -d @payload.json
```

### Phase 5: Verification
1. Check the response from the Worker. It should return `{"success": true, "message": "Published...", "commit_sha": "..."}`.
2. Inform the user that the article has been successfully committed to GitHub and Cloudflare Pages is now building it.

---

## Red Flags - STOP!
- ❌ **DO NOT** manually create `.mdx` files in `src/content/articles/` and run `git push` if using this skill! Let the Router API handle the Git history and image blob creation to ensure data consistency.
- ❌ **DO NOT** use `cat` or `echo` to build complex JSON payloads in bash. Save the payload to a `.json` file using your file writing tool, then pass it to `curl`.
