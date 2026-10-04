---
name: anthropic-skilljar-extractor
description: >
  Extracts any Anthropic Academy (Skilljar) course into a structured markdown folder.
  Triggers when the user provides an anthropic.skilljar.com URL and asks to extract,
  research, download, or convert a course to markdown. Produces one markdown file per
  lesson organized into section folders, with course diagrams downloaded and described.
  Use when user says things like "extract this course", "convert to markdown", "deep
  research this skilljar link", or provides any anthropic.skilljar.com URL.
---

# Anthropic Skilljar Course Extractor

## Step 1: Run the Extraction Script

```bash
python3 scripts/extract_course.py \
  <skilljar_url> <output_dir>
```

This produces:
```
<course-slug>/
├── README.md
├── 01-<section>/
│   ├── 01-<lesson>.md
│   └── ...
└── assets/images/   ← downloaded .webp diagrams
```

## Step 2: Describe Diagrams

For each full-size `.webp` in `assets/images/` (not `-medium.webp`):
- Use the `Read` tool to view it visually
- Add a detailed alt-text block and embed with `![desc](../assets/images/file.webp)` in the relevant lesson markdown

Assign images to lessons based on topic — architecture diagrams go in intro lessons, code screenshots in hands-on lessons, summary slides in review lessons.

## Step 3: Enrich Lesson Markdown

The script embeds bullet-point notes. Expand each lesson file:
- Add proper `##` headings per concept
- Format code examples in fenced code blocks with language tags
- Convert "Key: value" lines to `**Key:** value` bold format
- Add tables for comparisons (e.g., message types, primitives)
- Keep the frontmatter block (Section, URL, Lesson Type)

## Step 4: Enhance README

Add to the auto-generated README:
- Full course description paragraph
- Key concepts reference table
- Quick-reference code snippets
- Diagram index with one-line descriptions per image

## How the Script Works (for debugging)

- Fetches page HTML; extracts `window.__chatData` (LLM notes embedded in every Skilljar page)
- Parses sidebar `<ul class="dp-curriculum">` for section/lesson structure
- Downloads CloudFront images from `d7juhi4i8fsw0.cloudfront.net/images/<slug>/`
- Deduplicates lessons by URL (curriculum HTML appears twice in page source)
- Fuzzy-matches notes to lessons by title similarity

## If Login Is Required

Individual lesson pages always require auth — do not fetch them.
If the course landing page itself requires login (script finds 0 lessons):
1. Ask user to save the page HTML (browser → Save As → Webpage, HTML Only)
2. Modify script's `fetch()` to `open(path).read()` and pass the local file
