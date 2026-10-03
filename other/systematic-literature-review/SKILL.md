---
name: systematic-literature-review
description: "Systematic literature review across multiple arXiv papers."
allowed-tools:
  - bash
  - web_search
  - browse_page
  - write_file
  - present_files
enabled: true
related-skills: [arxiv, academic-paper-review]
license: MIT
author: Adapted from deer-flow (Bytedance, MIT)
---

# Systematic Literature Review

## Overview

Produces a structured **systematic literature review (SLR)** across multiple
academic papers on a research topic. Given a topic query, searches arXiv,
extracts structured metadata from each paper, synthesizes themes, and emits a
final report with consistent citations.

**Distinct from `academic-paper-review`:** that skill does deep peer review of
a single paper. This skill does breadth-first synthesis across many papers.

> **Poirot note:** The original deer-flow skill uses a bundled
> `scripts/arxiv_search.py` + subagent `task` tool for parallel extraction.
> Poirot has neither, so this version uses `bash` with `curl` to the arXiv API
> directly + sequential single-agent extraction.

## When to Use

- A literature survey on a topic ("survey transformer attention variants")
- A synthesis across multiple papers ("what do recent papers say about X")
- A systematic review with consistent citation format
- An annotated bibliography on a topic
- An overview of research trends in a field over a time window

**Do not use when:**
- User provides exactly one paper (use `academic-paper-review`)
- User asks a factual question (answer directly)

## Workflow

### Phase 1: Plan

Confirm with the user:
- **Topic**: the research area in plain English
- **Scope**: how many papers (default 20, hard upper bound 50), optional time
  window, optional arXiv category (e.g. `cs.CL`)
- **Citation format**: APA, IEEE, or BibTeX (default APA)

If user says "50+ papers", cap at 50 and explain synthesis quality degrades
past that.

### Phase 2: Search arXiv

Use `bash` with `curl` to the arXiv API. Extract 2-3 core keywords before
searching — don't pass the full topic description as the query.

```bash
# Search arXiv (use 2-3 core keywords, not the full topic)
curl -s "https://export.arxiv.org/api/query?search_query=all:transformer+attention&max_results=20&sortBy=relevance" | python3 -c "
import sys, xml.etree.ElementTree as ET, json
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.fromstring(sys.stdin.read())
papers = []
for entry in root.findall('a:entry', ns):
    papers.append({
        'id': entry.find('a:id', ns).text.split('/')[-1],
        'title': entry.find('a:title', ns).text.strip().replace('\n', ' '),
        'authors': [a.find('a:name', ns).text for a in entry.findall('a:author', ns)],
        'published': entry.find('a:published', ns).text[:10],
        'abstract': entry.find('a:summary', ns).text.strip(),
        'pdf_url': [l.get('href') for l in entry.findall('a:link', ns) if l.get('title') == 'pdf'],
        'abs_url': entry.find('a:id', ns).text,
    })
print(json.dumps(papers, indent=2, ensure_ascii=False))
"
```

**Query tips:**
- Use 2-3 core keywords, not the full topic phrase
- Use `--category` (arXiv `cat:` field) to narrow, not stuffing field names into query
- Always use `sortBy=relevance` (not `submittedDate`) for topical searches
- Run search exactly once; don't retry with modified queries

### Phase 3: Extract metadata (sequential)

> **Poirot note:** The original skill delegates extraction to parallel
> subagents. Poirot has no subagents, so extract sequentially in your own
> context. For >20 papers, warn the user that sequential extraction is
> token-heavy and suggest splitting.

For each paper, extract from its abstract:
- `arxiv_id`
- `title`
- `authors`
- `published_date`
- `research_question` (1 sentence — what problem the paper tackles)
- `methodology` (1-2 sentences — how they tackle it)
- `key_findings` (3-5 bullet points)
- `limitations` (1-2 sentences)

### Phase 4: Synthesize and format

**Cross-paper synthesis** — the report must do more than list papers:
- **Themes**: 3-6 recurring research directions across the set
- **Convergences**: findings multiple papers agree on
- **Disagreements**: where papers reach different conclusions
- **Gaps**: what the collective literature doesn't address

**Citation formatting** (inline, no bundled templates — format manually):

**APA (default):**
```
Author, A., & Author, B. (Year). Title. arXiv preprint arXiv:XXXX.XXXXX.
```

**IEEE:**
```
[1] A. Author and B. Author, "Title," arXiv preprint arXiv:XXXX.XXXXX, Year.
```

**BibTeX** (arXiv papers are `@misc`, not `@article`):
```bibtex
@misc{authorYear,
  title={Title},
  author={Author, A. and Author, B.},
  year={Year},
  eprint={XXXX.XXXXX},
  archivePrefix={arXiv}
}
```

### Phase 5: Save and present

Save the full report to `.poirot/outputs/slr-<topic-slug>-<YYYYMMDD>.md` via
`write_file`. Present via `present_files`.

In the chat message, show a short preview:
1. **Executive summary** — 3-5 sentence paragraph
2. **Themes list** — bullet list of themes
3. **Paper count + file pointer**

Do NOT dump the full report inline — per-paper annotations and references
belong in the file.

## Report Structure

```markdown
# Systematic Literature Review: [Topic]

## Executive Summary
[3-5 sentence overview]

## Methodology
[Search strategy, paper count, inclusion criteria]

## Themes
### Theme 1: [Name]
[Cross-paper analysis with citations]

### Theme 2: [Name]
[...]

## Convergences
[Findings multiple papers agree on]

## Disagreements
[Where papers diverge]

## Gaps
[What the literature doesn't address]

## Paper Annotations
### [Paper 1 Title]
- **Authors**: ...
- **Year**: ...
- **Research Question**: ...
- **Methodology**: ...
- **Key Findings**: ...
- **Limitations**: ...

### [Paper 2 Title]
[...]

## References
[Formatted per chosen citation style]
```

## Pitfalls

- **Query too specific**: `"diffusion models in computer vision"` → 0 results.
  Use 2-3 core keywords + category filter.
- **sortBy=submittedDate**: returns most recent papers in category regardless
  of topic relevance. Use `sortBy=relevance`.
- **Synthesis, not listing**: A report that only lists papers one after another
  is a failure mode. If you can't find themes, say so explicitly.
- **>50 papers**: synthesis quality degrades. Split by sub-topic.
