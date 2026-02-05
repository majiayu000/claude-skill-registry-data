---
name: using-gemini
description: Use when needing to analyze images (screenshots, diagrams, photos), analyze videos (screencasts, recordings), summarize YouTube videos, fetch and analyze web content, or perform web searches with Google. Gemini CLI provides multimodal and web access capabilities Claude lacks natively. Do NOT use for tasks Claude can handle directly (text analysis, code review, file reading of text files).
---

# Using Gemini CLI

**Gemini CLI extends Claude's capabilities with multimodal and web access features.** Use it for tasks Claude cannot do natively: analyzing images, analyzing videos, accessing YouTube content, fetching web pages, and searching the web with Google.

## Base Command Syntax

```bash
gemini --allowed-mcp-server-names "" [other-flags] "Your prompt here"
```

**Always use `--allowed-mcp-server-names ""` to disable MCP servers for faster startup.**

## Controlling Detail Level

Control the detail level of Gemini's responses through your prompt wording:

- **For comprehensive analysis:** Add "in detail" to your prompt
- **For quick summaries:** Use "briefly" in your prompt

**Note:** Each use case may have specific wording requirements. Check the reference file for use-case-specific guidance on prompt wording.

## Use Cases

**Read the specific reference file for the action you need to perform.** Each reference contains the exact command patterns, flags, and examples for that use case.

### Image Analysis
**When:** Analyze screenshots, diagrams, photos, or extract text from images
**Read:** [references/image-analysis.md](references/image-analysis.md)

### Video Analysis
**When:** Analyze local video files (screencasts, recordings, demos)
**Read:** [references/video-analysis.md](references/video-analysis.md)

### YouTube Videos
**When:** Summarize YouTube videos, extract information, or get key points
**Read:** [references/youtube.md](references/youtube.md)

### Web Fetch
**When:** Fetch and analyze content from any URL (articles, documentation, pages)
**Read:** [references/web-fetch.md](references/web-fetch.md)

### Web Search
**When:** Search Google for current information or documentation
**Read:** [references/web-search.md](references/web-search.md)
