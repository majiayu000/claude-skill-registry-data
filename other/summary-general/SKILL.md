---
name: summary-general
description: Summarizer for news articles, blog posts, videos, and podcasts. Structured summaries with citations, thesis, themes, and critical analysis. Not for academic papers; use summary-academic. Triggers on "summarize this", "summarize this article", "general summary", "/general-summary", "quick summary", "brief summary", and "/general-summary quick".
when_to_use: Use when the user wants a news article, a blog post, a video, a podcast, or a similar general-audience source summarized with its thesis, main themes, citations, and a critical read. Use summary-academic instead when the source is a scholarly paper, a preprint, or a dissertation, which needs the methodology and implications treatment this skill does not apply. A request for a quick or brief summary selects the short form of this same skill rather than a different one.
---

# General Content Summary

Use this skill for **non-academic content**: news articles, blog posts, opinion pieces, videos, podcasts, interviews, reports, and general web content.

For academic papers, research articles, peer-reviewed publications, preprints, or dissertations, use the **summary-academic** skill instead.

## Input Handling

- **PDF attachments**: First check for an existing `<basename>_text.md` extract in the PDF's folder; if it exists, read the extract instead of the PDF (preferred at any size). Otherwise check the page count (PyPDF2 or `pdfinfo`):
  - **4 pages or fewer**: read the PDF directly in the main thread before summarizing.
  - **More than 4 pages**: do not read it in the main thread. Split it into 4-page chunks with the split-pdf skill and read the chunks in a subagent that writes `notes.md`, then read `notes.md` as text and summarize from it. This keeps the full document out of the main context window.
- **TXT attachments**: Read the full document before summarizing.
- **Web links**: Fetch and extract the content.
- **Video/podcast links**: Extract the transcript or available description.
- **Pasted text**: Process directly.

## Style Requirements

- Write in an **expository style**: explain and inform directly without referencing the source material.
- **Never use** phrases like "the author," "the article," "the video," or "the piece argues."
- Present information as **factual statements**.
- **No section headings** except "Issues:" (and only if issues exist).
- Remove all citation markers from your response except the Chicago citation.
- Take an **ideologically neutral position**.
- Insert **two blank lines** between each section.
- **Define acronyms on first use** as `Term (ACRONYM)`; bare `ACRONYM` thereafter. First use is the first time the acronym appears anywhere in the summary. Universally recognized acronyms (US, EU, AI, ML, LLM, CEO, GDP, ROI, R&D, and similar) stay bare. Domain-specialized acronyms are always expanded on first use.

## Length Guidance

| Section | Target Length |
|---------|---------------|
| Themes | 5-12 bullets |
| Issues | 1-5 bullets (only if found) |
| Summary paragraph | 75-200 words (scale with complexity) |

## Output Format

Structure your response exactly as follows (no headings except Issues):

### 1. Citation (no heading)
Provide a citation in **Chicago Author-Date style**:

**Standard format:**
`Author's Last Name, First Name. Year. *Title of the Article*. Name of the Publication. Date. URL.`

**For 3 or more authors:**
`First Author's Last Name, First Name, et al. Year. *Title*. Publication. Date. URL.`

**For videos/podcasts:**
`Creator/Host Last Name, First Name. Year. *Title of Episode/Video*. Platform/Show Name. Date. URL.`

**For content without a clear author:**
`Publication Name. Year. *Title*. Date. URL.`

"Date" is the full publication date after the publication name (for example, "March 3, 2026" for a specific day, "March 2026" for month-level).

### 2. Thesis (no heading)
Write **one sentence** that accurately describes the thesis or main argument.

**Special cases:**
- **News reports**: State the central event or development being reported.
- **Interviews**: State the main topic or thesis of the interviewee.
- **Opinion pieces**: State the central argument.
- **Explainers**: State the main concept being explained.

### 3. Themes (no heading)
Create a comprehensive bullet-point summary (5-12 bullets):
- Use hyphen and space (`- `) for each bullet.
- Include main themes, ideas, and arguments.
- **Include specific numerical data**: statistics, percentages, ratios, comparative figures.
- Cite concrete examples and measurements.
- Present in logical flow: broad themes to specific supporting evidence.
- Rely exclusively on the provided content.

### 4. Issues:
**Only include this section if issues are found. Otherwise, omit entirely (no heading).**

Conduct a thorough analysis to identify:
- **Factual errors**: State the error and correct information, relying on widely accepted, verifiable facts.
- **Logical fallacies**: Identify the type, analyze it, and quote relevant text.
- **Strong counterarguments**: Detail the alternative viewpoint and quote relevant text.

Present as a bulleted list under the "Issues:" heading. Each issue is a separate bullet.

### 5. Summary (no heading)
Write a concluding paragraph (75-200 words):
- Capture main points and themes.
- Use neutral tone with clear, concise language.
- Simple, straightforward sentence structure.
- No flowery language or empty phrases.
- Scale length with content complexity.

## Output

Save the summary as a markdown file:

- **Filename:** `<project_name>_summary.md`
- **Location:** The project folder (the output directory), never in a subfolder like `TeX/` or `_build/`.
- **When invoked by a parent workflow** (for example, a slides pipeline): follow the parent workflow's placement rules instead.

`<project_name>` resolves in this order: a name the user specified, otherwise the single source filename without its extension, otherwise the project folder name.

## Final Check

Before submitting, verify:
- Expository style (no source references like "the author says").
- No section headings except "Issues:" (and only if issues exist).
- All citation markers removed except the Chicago citation.
- Proper bullet formatting with hyphens.
- Two blank lines between sections.
- Numerical data and statistics included where available.
- Output file placed in the project folder with correct `<project_name>_summary.md` naming.

---

# Quick General Summary Variant

**Invoke with**: "quick summary", "brief summary", or `/general-summary quick`

When a quick summary is requested, provide only:

1. **Citation** (Chicago Author-Date, same format as above).
2. **Thesis** (one sentence).
3. **Themes** (4-6 bullets maximum, with key statistics).
4. **Summary** (50-100 words).

Skip the Issues section entirely for quick summaries.
