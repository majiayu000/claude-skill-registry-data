---
name: summary-academic
description: Academic paper summarizer for papers, research articles, and scholarly publications. Structured summaries with citations, thesis, conclusions, methodology, implications, and critical analysis. Triggers on "summarize this paper", "summarize this research", "academic summary", "/academic-summary", "quick academic summary", "brief paper summary", and "/academic-summary quick".
when_to_use: Use when the source is scholarly, a journal article, a preprint, a working paper, a dissertation, or a conference paper, and the user wants it summarized with its thesis, methodology, conclusions, implications, and a critical read. Use summary-general instead for news articles, blog posts, videos, podcasts, and other non-scholarly sources. A request for a quick or brief summary selects the short form of this same skill rather than a different one.
---

# Academic Paper Summary

Use this skill **only for academic papers, research articles, and scholarly publications** (peer-reviewed journals, conference proceedings, working papers, preprints, dissertations).

For non-academic content (news articles, blog posts, videos, podcasts, general web content), use the **summary-general** skill instead.

## Input Handling

- **PDF attachments**: Prefer an existing `<basename>_text.md` extract at any size (read the extract, not the PDF). Otherwise check the page count: **4 pages or fewer** read the PDF directly; **more than 4 pages** split with the split-pdf skill into 4-page chunks and read them in a subagent that writes `notes.md`, then read `notes.md` as text in the main thread. Reading a long PDF this way keeps the source out of the main context window and avoids shallow comprehension. When this skill is driven by a parent workflow (for example, a slides pipeline) that feeds pre-extracted text, summarize that text directly; the page gate applies only to the standalone PDF path.
- **TXT attachments**: Read the full document before summarizing.
- **Web links**: Fetch and extract the article content.
- **Pasted text**: Process directly.

## Style Requirements

- Write in an **expository style**: explain and inform directly without referencing the source material.
- **Never use** phrases like "the author," "the paper," "the article," or "the study argues."
- Present information as **factual statements**.
- Use only the **explicit section headings** specified below.
- Do not introduce any other section headings, subheadings, or labels.
- Take an **ideologically neutral position**.
- Insert **two blank lines** between each section.
- **Define acronyms on first use** as `Term (ACRONYM)`; bare `ACRONYM` thereafter. First use is the first time the acronym appears anywhere in the summary, not per section. Universally recognized acronyms (US, EU, AI, ML, LLM, CEO, GDP, ROI, R&D, and similar) stay bare. Paper-specific acronyms (for example, RCT, GMM, IV, DID, RLHF) are always expanded on first use.

## Length Guidance

| Section | Target Length |
|---------|---------------|
| Key points | 5-15 bullets |
| Conclusions | 1-10 conclusions, 3-6 sub-bullets each |
| Summary paragraph | 100-300 words (scale with complexity) |
| Implications | 3-8 bullets |

## Output Format

Structure your response exactly as follows:

### 1. Citation (no heading)
Provide a citation in **Chicago Author-Date style**:

**Published articles:**
`Author's Last Name, First Name. Year. *Title of the Article*. Name of the Publication. Date. URL.`

**Preprints (arXiv, SSRN, bioRxiv, etc.):**
`Author's Last Name, First Name. Year. *Title of the Article*. Preprint, [Platform Name]. Date. URL.`

**Working papers:**
`Author's Last Name, First Name. Year. *Title of the Article*. Working Paper, [Institution]. Date. URL.`

"Date" is the full publication date after the publication name (for example, "March 3, 2026" for a specific day, "March 2026" for month-level).

For 3 or more authors, use: `First Author's Last Name, First Name, et al. ...`

### 2. Thesis (no heading, no label)
Write **one sentence** that accurately describes the thesis.

**Special cases:**
- **Literature reviews**: State "This is a literature review with no single thesis; it synthesizes research on [topic]."
- **Meta-analyses**: State the primary research question being analyzed.
- **Exploratory studies**: State the central research question.

### 3. Key Points (no heading)
Create a detailed bullet-point summary (5-15 bullets):
- Use hyphen and space (`- `) for each bullet.
- Include main ideas, themes, and quantitative facts.
- Eliminate unnecessary language.
- Rely exclusively on the provided content.

### 4. Conclusions:
List 1-10 key conclusions. Under each (3-6 sub-bullets):
- Summarize main ideas and concepts.
- Include evaluation methods.
- Quantify effects with numerical data.
- State implications.
- Include verbatim quotes when helpful.
- Use sub-bullets with hyphen and space (`- `).

### 5. Population:
Describe in paragraph form:
- Population sampled or targeted.
- Research methodology used.
- Time frame covered.

**Skip this section entirely** (no heading) if not applicable, such as for:
- Theoretical papers.
- Literature reviews without original data collection.
- Purely conceptual or philosophical works.
- Mathematical proofs.

### 6. Implications:
List real-world applications using bullet points (3-8 bullets, `- `).

### 7. Concepts:
List scientific or economic concepts commonly understood by someone with an undergraduate degree:
- Name each concept.
- Explain it briefly.
- Describe how it relates to the content.

**Skip this section entirely** (no heading) if no such concepts exist.

### 8. Issues:
List any:
- **Factual errors**: State the error and correct information.
- **Logical fallacies**: Identify type, analyze, and quote relevant text.
- **Strong counterarguments**: Detail alternative viewpoint and quote relevant text.

**Skip this section entirely** (no heading) if none exist.

### 9. Summary (no heading)
Write a concluding paragraph (100-300 words):
- Capture main points and themes.
- Use neutral tone with clear, concise language.
- Simple, straightforward sentence structure.
- No flowery language or empty phrases.
- Scale length with complexity of conclusions.

## Output

Save the summary as a markdown file:

- **Filename:** `<project_name>_summary.md`
- **Location:** The project folder (the output directory), never in a subfolder like `TeX/` or `_build/`.
- **When invoked by a parent workflow** (for example, a slides pipeline): follow the parent workflow's placement rules instead.

`<project_name>` resolves in this order: a name the user specified, otherwise the single source filename without its extension, otherwise the project folder name.

## Final Check

Before submitting, verify compliance with:
- All style requirements (expository, no source references).
- Correct section headings only.
- Proper bullet formatting with hyphens.
- Two blank lines between sections.
- Appropriate citation format (published vs. preprint vs. working paper).
- Skipped sections where not applicable.
- Output file placed in the project folder with correct `<project_name>_summary.md` naming.

---

# Quick Academic Summary Variant

**Invoke with**: "quick academic summary", "brief paper summary", or `/academic-summary quick`

When a quick summary is requested, provide only:

1. **Citation** (Chicago Author-Date, same format as above).
2. **Thesis** (one sentence; or state it is a literature review or exploratory study).
3. **Key Points** (5-8 bullets maximum).
4. **Summary** (75-150 words).

Skip the Conclusions, Population, Implications, Concepts, and Issues sections.
