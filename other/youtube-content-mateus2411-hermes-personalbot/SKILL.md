---
name: youtube-content
description: "YouTube transcripts to summaries, threads, blogs."
platforms: [linux, macos, windows]
---

# YouTube Content Tool

## When to use

Use when the user shares a YouTube URL or video link, asks to summarize a video, requests a transcript, or wants to extract and reformat content from any YouTube video. Transforms transcripts into structured content (chapters, summaries, threads, blog posts).

**Pitfall — URL mismatch**: Before processing, verify the video title/topic from the URL. The `v=` param identifies *a* YouTube video, but not necessarily the one the user expects. Today we saw `Ke90Tje7VS0` (a React JS tutorial) passed as a "landing page Figma tutorial." Cite a source or check the page title before assuming content matches intent.

## Setup

`youtube-transcript-api` v1.x is required. The old static API (`YouTubeTranscriptApi.get_transcript()`) was removed — v1.x uses instance methods.

```bash
pip install youtube-transcript-api
python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; api = YouTubeTranscriptApi(); print('OK')"
```

## Helper Script

`SKILL_DIR` is the directory containing this SKILL.md file. The script accepts any standard YouTube URL format, short links (youtu.be), shorts, embeds, live links, or a raw 11-character video ID.

```bash
# JSON output with metadata
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# Plain text (good for piping into further processing)
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# With timestamps
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# Specific language with fallback chain
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## Persistence — Save to Obsidian Vault

After extracting content for study/assignment purposes, **save it to the user's Obsidian vault** with proper frontmatter:

```yaml
---
tags: [subject, topic, class]
title: "Descriptive Title — Source Info"
source: "https://youtube.com/watch?v=VIDEO_ID"
---
```

**Location convention**: `escola/<subject>/<topic-slug>.md` (e.g., `escola/física/ferro-de-passar-explicacao.md`).

Always commit vault changes afterward via `git add` + `git commit -m "update vault: <description>"`.

## Output Formats

After fetching the transcript, format it based on what the user asks for:

- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Summary**: Concise 5-10 sentence overview of the entire video
- **Chapter summaries**: Chapters with a short paragraph summary for each
- **Thread**: Twitter/X thread format — numbered posts, each under 280 chars
- **Blog post**: Full article with title, sections, and key takeaways
- **Quotes**: Notable quotes with timestamps

### Example — Chapters Output

```
00:00 Introduction — host opens with the problem statement
03:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

### Extract Topic (study notes / assignment help)

For extracting a **specific explanation or section** from a transcript (e.g., a student needs the part about how an iron works for a physics assignment):

1. **Fetch the full transcript** using MCP rippr tool
2. **Search the transcript text** for the relevant section using keyword matching
3. **Extract the exact professor's speech** — preserve it literally, verbatim
4. **Structure the output** as:
   - Context: what the professor was explaining before (e.g., bimetallic strip principle)
   - Literal transcription: the exact words, in quote blocks
   - Summary: condensed version for the assignment, with key bullet points
5. **Save to Obsidian vault** if the user has one, with proper frontmatter (tags, title, source link)

**Important — plan verification**: If the user has previously experienced issues with terminal scripts (forced exit codes, crashes), **show the execution plan first before running anything**. List each step in plain language and wait for confirmation. Prefer MCP tools over terminal scripts when available — they are more reliable and don't produce forced-exit errors.

**Important — verbatim preservation**: When the user says "salva exatamente o que ele falar" (save exactly what he said), do NOT paraphrase or summarize the professor's words. Quote the transcript directly in blockquotes, then optionally add a summary section after. The literal transcription is the primary deliverable.

## Workflow

### Primary Path — MCP rippr Tool (preferred)

If the `mcp_rippr_mcp_rip_transcript` MCP tool is available, use it as the **primary** method. It handles download, storage, and formatting natively and avoids IP-blocking issues:

```
mcp_rippr_mcp_rip_transcript(format="text", url="https://youtu.be/VIDEO")
```

**Parameters:**
- `format`: `"text"` or `"json"` (default). Text format produces a single-line transcript in a markdown file with YAML frontmatter (title, channel, language, videoId, videoUrl, durationSeconds, rippedAt).
- `url`: Full YouTube URL (any format: youtu.be, youtube.com/watch?v=, shorts, etc.)

**Result handling:** The tool returns a file path like `/home/keila/rippr/transcripts/<slug>.md`. Read it with `cat` or the `read_file` tool. The transcript body is in the markdown content after the frontmatter. Auto-generated captions (language `pt (auto-generated)`) come as a single paragraph — read the whole file to get the full content.

**Fallback to CLI:** If the MCP tool is not available, use the `rippr` CLI:
   ```bash
   rippr download <VIDEO_URL> --format txt -o <output_dir>
   ```
   **Note on `--format txt`**: rippr produces a single-line output with no newline separators. The output includes YAML frontmatter with title, channel, language, duration, and video URL.

### Fallback Path — Helper Script

If neither MCP nor rippr CLI is available, **Fetch** the transcript using the helper script with `--text-only --timestamps`.
3. **Validate**: confirm the output is non-empty and in the expected language. If empty, retry without `--language` to get any available transcript. If still empty, tell the user the video likely has transcripts disabled.
3. **Chunk if needed**: if the transcript exceeds ~50K characters, split into overlapping chunks (~40K with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested output format. If the user did not specify a format, default to a summary.
5. **Verify**: re-read the transformed output to check for coherence, correct timestamps, and completeness before presenting.

### Fallback Path A — When YouTube Is Blocked (IP / rate limit)

If `YouTubeTranscriptApi` raises `IpBlocked` or `RequestBlocked` (common from WSL, cloud VMs, or after rate limits), the YouTube API is blocking the IP. Do NOT retry more than once. Instead:

1. **Identify what topics to search for**. Extract the video title (from the URL, the user's description, or context).
2. **Search the web for topic summaries**. Use a web search tool (Composio remote workbench `web_search()`, browser search, etc.) with queries like `"UX Design Crash Course" transcript YouTube` or `"landing page Figma" tutorial layout`.
3. **Extract structured knowledge** from the search results. The LLM-powered search engines often return condensed summaries of the requested topic.
4. **Format the alternative content** into the same output structure (chapters, summary, key points) as you would from a transcript.
5. **Note the limitation** to the user: "Direct transcript unavailable (IP blocked). Content below is compiled from web research on the same topics."

The web-search fallback produces less detail than a true transcript but covers the core concepts.

### Fallback Path B — No Captions Available (video has no subtitles)

When video tools report "No captions found" or "Subtitles/closed captions unavailable" (common for live streams, newly uploaded videos, or creator-disabled captions):

1. **Navigate to the YouTube page in the browser**: Open the video URL directly. The transcript tools can't help — the content isn't captioned.
2. **Scroll down to the description section** and click the "...more" button to expand the full description text. Videos (especially courses, tutorials, live streams) often embed all their key links, companion resources, and even full topic breakdowns in the description.
3. **Extract all links** via `browser_console`: YouTube wraps visible links behind redirect URLs. Use `Array.from(document.querySelectorAll('a')).map(a => a.href)` to see the actual `q=` parameter destinations (the real URLs embedded in YouTube's redirect wrapper).
4. **Navigate companion resources**: Descriptions often link to:
   - Course registration pages
   - Companion websites (especially Lovable.app, Carrd, Notion, or other no-code sites)
   - PDF download links (SendFlow, Google Drive, direct)
   - WhatsApp/Telegram groups
   - Class-specific landing pages with full summaries
5. **Extract content from companion sites**: The companion site often contains the full structured content that the video covers — tool lists, prompts, methodologies, exercises. Extract it via `browser_navigate` + `browser_snapshot`, clicking any accordion/expand sections to reveal hidden content.
6. **Combine all sources** into a single structured note: video metadata (title, channel, duration) + companion site content + any extracted materials + all external links for further reference.

**Pitfall — truncated links in snapshots**: YouTube description text truncates visible URLs (showing "https://sendflow.click/l/materiais-ia..." instead of the full URL). Always use `browser_console` with `querySelectorAll('a')` to capture the full `href` attributes, which contain the actual redirect destinations.

**Pitfall — accordion/collapsed sections**: Companion sites often use accordion UI. Click each collapsed section button before taking the full snapshot, or you'll miss content.

**Pitfall — live stream replay availability**: Live stream replays are often available only for a limited window (e.g., "until next Sunday"). Note this to the user so they prioritize watching.

## Error Handling

- **Transcript disabled**: tell the user; suggest they check if subtitles are available on the video page.
- **Private/unavailable video**: relay the error and ask the user to verify the URL.
- **No matching language**: retry without `--language` to fetch any available transcript, then note the actual language to the user.
- **Dependency missing**: run `pip install youtube-transcript-api` and retry.
- **IP blocked**: see Fallback Path above. Do NOT retry with proxies or cookies — the web-search approach is simpler and more reliable.

## Pitfalls

- **IP blocking from WSL/cloud**: YouTube's transcript API blocks most cloud IP ranges (AWS, Azure, GCP) and some residential WSL connections. If `rippr` is installed, use it as the primary path (step 1 above) — it handles download differently and usually bypasses IP blocks. Only fall back to web-search if rippr is unavailable AND the API is blocked.
- **Video ID ≠ topic matching**: Always confirm the video's actual topic before processing. The URL alone may not match the user's description (e.g., a React tutorial URL was passed as a Figma landing page tutorial).
- **youtube-transcript-api v1.x API**: The class requires instantiation: `YouTubeTranscriptApi().fetch(video_id)`, not the old static `YouTubeTranscriptApi.get_transcript()`. Our helper script already handles this.
- **Rate limits**: Even after a successful fetch, YouTube may block subsequent requests. Space out bulk transcript fetches by 10+ seconds.
