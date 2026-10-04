---
name: transcript-to-docs
description: Process a video/audio transcript into structured markdown documentation — extracting key topics, organizing into logical sections, and producing a polished reference document.
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep
---

Turn a transcript into documentation: $ARGUMENTS

$ARGUMENTS should include:
- A path to a transcript file (e.g. `transcripts/VIDEO_ID.md`) OR a glob pattern (e.g. `transcripts/*.md`)
- Optionally: `--style` followed by one of: `reference`, `tutorial`, `guide`, `summary`, `notes` (default: `reference`)
- Optionally: `--output PATH` to specify where to save the output
- Optionally: `--title "CUSTOM TITLE"` to override the document title
- If no arguments are given, ask the user which transcript to process

---

## Document Styles

| Style | Purpose | Structure |
|---|---|---|
| `reference` | Comprehensive documentation of all topics covered | Organized by topic with full detail |
| `tutorial` | Step-by-step walkthrough if the content is instructional | Sequential steps with explanations |
| `guide` | Practical guide extracting actionable advice | Problem/solution oriented sections |
| `summary` | Condensed overview of key points | Executive summary + bullet points |
| `notes` | Lightly structured study/meeting notes | Chronological with headers by topic shift |

---

## Before Starting

1. **Read the transcript file(s)** specified in $ARGUMENTS
2. If the file has frontmatter (title, video_id, url, duration), capture it for the output metadata
3. Read the plain text transcript section (not the timestamped version, if both exist)
4. If processing multiple files, process each one independently and save separate outputs

---

## Step 1 — Analyze the Transcript

Read the full transcript and identify:

1. **Core topics**: The 3-8 major subjects or themes discussed
2. **Key concepts**: Definitions, frameworks, models, or terminology introduced
3. **Actionable items**: Steps, recommendations, best practices, or instructions given
4. **Examples and stories**: Concrete illustrations, case studies, or anecdotes used
5. **Quotes**: Memorable or particularly clear statements worth preserving verbatim
6. **Speakers**: If multiple speakers are identifiable, note who said what
7. **Logical structure**: How topics flow and group — this determines your heading hierarchy

---

## Step 2 — Build the Document Structure

Based on the analysis, create a heading outline appropriate to the chosen style:

### For `reference` style:
```
# Document Title
## Overview (2-3 paragraph summary)
## [Topic 1 Heading]
### [Subtopic if needed]
## [Topic 2 Heading]
...
## Key Takeaways
## Source
```

### For `tutorial` style:
```
# Document Title
## Overview
## Prerequisites (if applicable)
## Step 1 — [Action]
## Step 2 — [Action]
...
## Summary
## Source
```

### For `guide` style:
```
# Document Title
## Overview
## [Problem/Goal 1]
### Context
### Approach
## [Problem/Goal 2]
...
## Quick Reference
## Source
```

### For `summary` style:
```
# Document Title
## Executive Summary (1 paragraph)
## Key Points
## Notable Quotes
## Source
```

### For `notes` style:
```
# Document Title
## Overview
## [Topic as discussed — roughly chronological]
## [Next topic shift]
...
## Open Questions / Follow-ups
## Source
```

---

## Step 3 — Write the Documentation

Transform the raw transcript into polished documentation following these rules:

### Content Rules

- **Reorganize, don't transcribe** — Group related points together even if they were discussed at different times. Documentation should be organized by topic, not by order of speech.
- **Clean up spoken language** — Remove filler words, false starts, tangents, and repetition. Convert spoken phrasing into clear written prose.
- **Preserve meaning precisely** — Do not add interpretations, opinions, or information not present in the transcript. If something is ambiguous, note it.
- **Keep valuable quotes** — When the speaker makes a particularly clear or memorable point, preserve it as a blockquote with attribution.
- **Use concrete examples** — If the speaker gave examples, include them. They make documentation useful.
- **Define terms** — If a concept is defined or explained in the transcript, include that definition clearly.
- **Add structure** — Use bullet lists, numbered steps, tables, and bold key terms to make the document scannable.

### Formatting Rules

- Use H2 (`##`) for major sections, H3 (`###`) for subsections. Do not go deeper than H4.
- Use **bold** for key terms on first mention within a section
- Use blockquotes (`>`) for direct quotes from the transcript
- Use code blocks for any technical content (commands, code, configs)
- Use tables when comparing items, listing properties, or presenting structured data
- Keep paragraphs short — 2-4 sentences max
- Use bullet lists for 3+ related items

---

## Step 4 — Add Metadata and Source Attribution

Include frontmatter and a source section:

```markdown
---
title: "DOCUMENT_TITLE"
source_title: "ORIGINAL_VIDEO_TITLE"
source_url: VIDEO_URL (if available from transcript frontmatter)
source_type: video | audio | transcript
date_processed: TODAY
style: reference | tutorial | guide | summary | notes
---
```

At the end of the document, add:

```markdown
---

## Source

- **Original**: [VIDEO_TITLE](VIDEO_URL) (DURATION)
- **Processed**: DATE
- **Style**: reference | tutorial | guide | summary | notes

> This document was generated from a video transcript. Some nuance from the original presentation (tone, visual aids, demonstrations) may not be fully captured.
```

---

## Step 5 — Save the Output

Save to `docs/{slug}.md` where `slug` is derived from the document title (lowercase, hyphens, no stop words). If `--output` was specified, use that path instead.

---

## Output

After saving, report:

```
## Documentation Generated

- **Title**: DOCUMENT_TITLE
- **Style**: STYLE
- **Source**: VIDEO_TITLE
- **Sections**: N major sections
- **Word count**: ~N words
- **Saved to**: PATH
```

---

## Error Handling

- **Transcript file not found** — List available files in `transcripts/` and ask the user to pick one
- **Empty or unreadable transcript** — Report the issue; suggest re-extracting with youtube-transcript
- **Transcript too short** (< 100 words) — Warn the user that the output may be thin; proceed anyway
- **Multiple transcripts** — Process each independently; report results for each
