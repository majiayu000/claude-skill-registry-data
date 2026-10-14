---
name: dk-wiki-article-writing
description: Use when writing a Wikipedia-style article or comprehensive research-backed document on a technical topic. Produces balanced, well-sourced articles with proper citations by researching from multiple angles before writing.
compatibility: "Python 3.10+ with uv. BRAVE_API_KEY env var for web search (ddgr used as primary, Brave API as fallback)."
allowed-tools: bash, read, write, edit, subagent
license: MIT
disable-model-invocation: true
metadata:
  author: dushyantkhosla
  version: "2.0"
  requires: "uv"
  optional: "BRAVE_API_KEY for web search"
  opencode/autoinvoke: false
---

# Wiki Article Writing

A research-first workflow for writing comprehensive, balanced, Wikipedia-style articles on technical topics. The core principle: **research breadth before writing depth** — never start writing until you've heard from voices you didn't expect to find.

## Overview

This skill enforces a 6-phase pipeline that prevents the most common failure mode in AI-assisted article writing: **advocacy bias from narrow sourcing**. When you only search for the names you already know, you get a highlight reel, not an encyclopedia.

Research is parallelised via subagents — multiple research threads run concurrently, each writing findings to files. Synthesis happens only after all threads complete.

## When to Use

- Writing a Wikipedia-style article on a technical topic
- Creating a comprehensive research document that needs balanced coverage
- Producing an HTML page displaying a well-sourced article
- Any task requiring multi-source research synthesis before writing

## When NOT to Use

- Quick summaries or opinion pieces (no balance needed)
- Internal documentation (no citation requirements)
- Topics with no existing discourse (nothing to balance against)

---

## Phase 0: Research Plan

**Goal:** Define what to research before searching. This prevents reactive, unfocused searching.

1. **Create the research folder:**

```bash
mkdir -p research_{topic_slug}
```

2. **Write `research_{topic_slug}/research_plan.md`** containing:

```markdown
# Research Plan: {Topic}

## Main Research Question
{What is this article about?}

## Subtopics (3-5, non-overlapping)

### Subtopic 1: {name}
- **Search angles:** {2-3 specific queries}
- **Expected sources:** {what kind of blogs, docs, discussions}
- **Budget:** 3-5 searches max

### Subtopic 2: {name}
- **Search angles:** {2-3 specific queries}
- **Expected sources:** {what kind of blogs, docs, discussions}
- **Budget:** 3-5 searches max

### Subtopic 3: {name}
...

## Synthesis Approach
How will findings combine into a balanced article?
```

**Subtopic sizing guide:**

| Topic complexity | Subtopics | Parallel subagents |
|-----------------|-----------|-------------------|
| Simple fact-finding | 2 | 2 |
| Comparative analysis | 3 | 3 |
| Complex multi-perspective | 4-5 | 3 (batch remaining) |

**Save to:** `research_{topic_slug}/research_plan.md`

---

## Phase 1: Wikipedia Baseline

**Goal:** Understand what already exists and mine references.

Fetch the Wikipedia article:

```bash
uv run {baseDir}/scripts/wiki.py "YOUR_TOPIC_HERE" --full --refs --toc
```

`uv run` auto-installs pywikibot on first run. Outputs article text, reference URLs, and TOC links.

**Note gaps:** What's missing? What's underdeveloped? What's the tone?

**Save to:** `research_{topic_slug}/wikipedia-baseline.md`

---

## Phase 2: Parallel Research (Subagents)

**Goal:** Find voices across the full spectrum — proponents, critics, practitioners, independent observers — efficiently via parallel delegation.

### Delegation Strategy

Launch all research subagents in a **single `subagent({ tasks: [...] })` call** using PARALLEL mode. Do not spawn them one at a time — the system only allows one subagent invocation per turn, so parallel mode is the only way to run concurrent research.

**Subagent task template:**

```
Research "{SUBTOPIC_NAME}" for a Wikipedia-style article about {TOPIC}.

Search angles:
- {query_1}
- {query_2}
- {query_3}

Use the search tool:
  {baseDir}/scripts/search.sh "{query}" 10

For the 2-3 most important results, fetch full content (captures nuance that snippets miss):
  {baseDir}/scripts/search.py "{url}" -n 1 --content

CRITICAL: You MUST write your findings to research_{topic_slug}/findings_{subtopic_slug}.md using the write tool BEFORE finishing your session. Do not end without writing this file.

Write your findings with:
- Key claims and arguments (with attribution)
- Notable quotes (exact text)
- Source URLs
- Stance (pro/con/neutral/nuanced)
- What this source ignores or assumes

Budget: 3-5 searches maximum. Stop when you have enough for a balanced view.
```

**For the 1-2 most critical sources** (especially criticism pieces and practitioner experience reports), fetch full content during Phase 2 rather than waiting for a separate deep-dive phase. Full text reveals nuance, blind spots, and verbatim quotes that search snippets miss.

### Video Transcripts (Optional)

For YouTube videos relevant to the article, extract transcripts directly. **Do not use the CLI tool's summarization step** — the parent agent will read and synthesize the transcripts itself.

**Preferred method (direct, no dependencies):**

```bash
# Download auto-captions only (no audio download)
yt-dlp --skip-download --write-auto-subs --sub-langs "en.*" \
  --sub-format vtt -o "tmp_%(id)s" "https://youtube.com/watch?v=VIDEO_ID"

# Clean VTT to plain text
sed 's/<[^>]*>//g' tmp_VIDEO_ID.en.vtt | tr -s '\n' ' ' | fold -s -w 100 > tmp_VIDEO_ID.txt
```

**Fallback method (if subtitles are unavailable or garbled):**

```bash
# Use the transcription tool for audio fallback (requires OPENROUTER_API_KEY)
cd {transcribe-skill-dir}/scripts && uv run transcribe_pdf.py "URL" --method subtitles
```

The parent agent reads the cleaned transcript text directly and synthesizes findings — no LLM API needed for summarization. This avoids the OPENROUTER/LM Studio dependency entirely. If the transcript is too large (>50K words), instruct the transcription tool to summarize as a fallback:

```bash
uv run transcribe_pdf.py "URL" --prompt "Extract: core thesis, key takeaways, notable quotes with attribution, speaker credentials."
```

**Save extracted transcripts to:** `research_{topic_slug}/transcripts/`

### What to Record Per Finding

- **Title** and **URL**
- **Source type:** official blog, practitioner blog, news, forum, academic, docs
- **Stance:** pro, con, neutral, nuanced
- **Key claim** (one sentence)
- **Notable quote** (exact text, with attribution)

### Rate Limit Handling

If `search.sh` returns errors, wait 3-5 seconds between calls. The script auto-falls back from ddgr to Brave API.

**Save each subagent's output to:** `research_{topic_slug}/findings_{subtopic_slug}.md`

---



---

## Phase 3: Source Audit & Gap Analysis

**Goal:** Verify balanced coverage before writing. This is the phase most workflows skip.

### The Balance Checklist

Read all files in `research_{topic_slug}/`. Ask yourself:

- [ ] Do I have **at least 2 strong critical perspectives**?
- [ ] Do I have **independent voices** (not just vendor blogs)?
- [ ] Do I have **community sentiment** (Reddit, HN, forums)?
- [ ] Do I have **practitioner experience reports** (not just theory)?
- [ ] Can I articulate the **strongest argument against** this topic?
- [ ] Do I know **what opponents would say** about my article?
- [ ] Am I including voices **I didn't expect to find**?

If any answer is "no", spawn one more targeted subagent to fill the gap.

### Identify Missing Perspectives

- **Who is missing?** (geographic, institutional, methodological)
- **What angle is underrepresented?**
- **What criticism have I not found?**

**Save to:** `research_{topic_slug}/source-audit.md`

---

## Verification Gate

**Goal:** Confirm all research files exist and are substantive before writing. This prevents discovering missing research mid-article.

Run before Phase 4:

```bash
echo "=== Research file inventory ==="
ls -la research_{topic_slug}/findings_*.md
echo "=== Word counts ==="
wc -w research_{topic_slug}/findings_*.md
echo "=== Expected files ==="
# Verify every subtopic from the research plan has a corresponding findings file
grep -c 'findings_' research_{topic_slug}/research_plan.md || echo "(check manually)"
```

**If any expected findings file is missing or empty**, re-run the failed subagent task before proceeding.

---

## Phase 4: Write the Article

**Goal:** Produce a balanced, well-structured, Wikipedia-style article with proper citations.

### Article Structure

```markdown
# {Topic Name}

**{Topic Name}** is {one-paragraph bold definition}. {2-3 sentences of context}. {Why it matters now}.{superscript citations}

---

## Contents
1. [Overview](#overview)
2. [History and origins](#history-and-origins)
3. [Key proponents](#key-proponents)
4. [Comparison with other approaches](#comparison-with-other-approaches)
5. [How it works](#how-it-works)
6. [Tools and ecosystem](#tools-and-ecosystem)
7. [Practical benefits](#practical-benefits)
8. [Criticism and limitations](#criticism-and-limitations)
9. [See also](#see-also)
10. [References](#references)
11. [External links](#external-links)

---

## Overview
{Expanded definition, core concepts, why it matters}

## History and origins
{Chronological narrative with citations}

## Key proponents
{Subsections for major voices — not just the famous ones}

## Comparison with other approaches
{Table format — neutral, factual}

## How it works
{Numbered workflow steps}

## Tools and ecosystem
{What exists, with links}

## Practical benefits
{What proponents claim, cited}

## Criticism and limitations
{What critics say, cited — EQUAL weight to benefits}

## See also
{Related topics}

## References
{Footnote-style numbered citations with URLs}

## External links
{Key URLs}
```

### Writing Rules

1. **Neutral tone** — "Proponents argue..." not "This is better because..."
2. **Cite everything** — use `<sup>[N]</sup>` footnote syntax
3. **Give criticism equal weight** — if benefits get 500 words, criticism gets 500 words
4. **Include dissent** — the strongest counterargument, not a straw man
5. **No advocacy** — encyclopedia entry, not blog post
6. **Target 2,500–4,000 words** for comprehensive coverage

### HTML Generation (Optional)

If an HTML page is needed, create a self-contained file:

- Wikipedia-inspired design (serif body, sans-serif UI)
- Dark mode via `prefers-color-scheme`
- Responsive (max-width ~960px, mobile breakpoints)
- Styled comparison table with alternating rows
- Citation superscript links
- All CSS inline, zero external dependencies

See [references/html-template.md](references/html-template.md) for reusable CSS patterns.

---

## File Organization

```
output-directory/
├── research_{topic_slug}/
│   ├── research_plan.md           # Phase 0
│   ├── wikipedia-baseline.md      # Phase 1
│   ├── findings_{subtopic}.md     # Phase 2 (one per subagent)
│   ├── findings_{subtopic}.md
│   ├── ...
│   └── source-audit.md            # Phase 3
├── {topic-name}.md                # Phase 4: The article
└── {topic-name}.html              # Phase 4: HTML page (optional)
```

---

## Common Mistakes

| Mistake | Why It Happens | Fix |
|---------|---------------|-----|
| Skipping research plan | Eagerness to start searching | Phase 0 is mandatory — plan first |
| Searching for specific names | Treating examples as exhaustive list | Search by concept angle, let voices emerge |
| Single-threaded research | Habit | Use `subagent({ tasks: [...] })` PARALLEL mode |
| Skipping criticism research | Confirmation bias | Make criticism a required subtopic |
| Using only search snippets | Convenience | Fetch full articles in Phase 2 (during research) |
| Writing before source audit | Eagerness | Verification gate + Phase 3 are mandatory — check balance |
| Advocacy tone | Unconscious bias | "Proponents argue..." not "This is better..." |
| Unequal section lengths | Natural enthusiasm for the positive | Explicitly balance word counts |

---

## Quality Checklist

Before delivering the article, verify:

- [ ] **Research plan** written before searching (Phase 0)
- [ ] **All findings files verified** (Verification Gate)
- [ ] **2,500+ words** (comprehensive coverage)
- [ ] **10+ sections** (all phases covered)
- [ ] **20+ citations** (footnote-style with URLs)
- [ ] **Comparison table** (at least 3 related approaches)
- [ ] **Criticism section** (at least 400 words, with named sources)
- [ ] **Independent voices** (not just vendor blogs)
- [ ] **Community sentiment** (Reddit/HN/forum perspectives)
- [ ] **Neutral tone** (no advocacy language)
- [ ] **HTML page** renders correctly (if generated)
