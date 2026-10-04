---
name: summarize
description: Summarizes, condenses, or extracts text, transcripts, and key points from URLs, articles, web pages, PDFs, podcasts, YouTube videos, and local files. Handles transcript extraction, transcript-to-document conversion, and acts as a fallback transcription tool when the user asks to transcribe, digest, recap, or get the gist of a link, video, or document.
homepage: https://summarize.sh
metadata:
  {
    "otto":
      {
        "emoji": "🧾",
        "requires": { "bins": ["summarize"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "steipete/tap/summarize",
              "bins": ["summarize"],
              "label": "Install summarize (brew)",
            },
          ],
      },
  }
---

# Summarize

Fast CLI to summarize URLs, local files, YouTube links, extract transcripts, and convert transcripts to structured documents.

## When to use (trigger phrases)

Use this skill immediately when the user asks any of:

- "use summarize.sh"
- "what's this link/video about?"
- "summarize this URL/article"
- "transcribe this YouTube/video" (best-effort transcript extraction; no `yt-dlp` needed)
- "get the transcript" / "extract the transcript"
- "convert this transcript to a doc" / "turn this transcript into an article"
- "digest this" / "recap this" / "give me the gist"

## Quick start

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

## YouTube: summary vs transcript

Best-effort transcript (URLs only):

```bash
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto --extract-only
```

If the user asked for a transcript but it's huge, return a tight summary first, then ask which section/time range to expand.

## Transcript-to-Document Conversion

When the user has a raw transcript (from YouTube, a meeting, podcast, etc.) and wants it converted to a structured document:

1. **Extract or receive the transcript** -- use `--extract-only` for YouTube, or accept a pasted/uploaded transcript
2. **Identify the target format** -- article, meeting notes, blog post, documentation, summary with key points
3. **Convert** using summarize with appropriate length and model:
   ```bash
   # For a detailed conversion
   summarize "/path/to/transcript.txt" --length long --model google/gemini-3-flash-preview

   # For a concise summary
   summarize "/path/to/transcript.txt" --length short --model google/gemini-3-flash-preview
   ```
4. **Structure the output** based on the target format:
   - **Article**: Title, introduction, sections with headers, conclusion
   - **Meeting notes**: Attendees, agenda items, decisions, action items
   - **Key points**: Bulleted list of main takeaways with timestamps if available
   - **Documentation**: Structured reference doc with sections and code blocks if applicable

## Model + keys

Set the API key for your chosen provider:

- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- xAI: `XAI_API_KEY`
- Google: `GEMINI_API_KEY` (aliases: `GOOGLE_GENERATIVE_AI_API_KEY`, `GOOGLE_API_KEY`)

Default model is `google/gemini-3-flash-preview` if none is set.

## Useful flags

- `--length short|medium|long|xl|xxl|<chars>`
- `--max-output-tokens <count>`
- `--extract-only` (URLs only)
- `--json` (machine readable)
- `--firecrawl auto|off|always` (fallback extraction)
- `--youtube auto` (Apify fallback if `APIFY_API_TOKEN` set)

## Config

Optional config file: `~/.summarize/config.json`

```json
{ "model": "openai/gpt-5.2" }
```

Optional services:

- `FIRECRAWL_API_KEY` for blocked sites
- `APIFY_API_TOKEN` for YouTube fallback
