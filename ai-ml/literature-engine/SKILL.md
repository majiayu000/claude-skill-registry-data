---
name: literature-engine
description: >
  ALWAYS activate when the user needs to find, organize, review, or synthesize
  academic literature. Uses academic APIs (Semantic Scholar, OpenAlex, CrossRef, arXiv)
  via scripts/academic_search.py. Handles search strategy, snowballing, screening,
  concept matrices, narrative synthesis, and literature monitoring (detecting new
  publications since last search). NEVER use web scraping for paper discovery —
  APIs first, web search only for verification.
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Literature Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (literature-engine)
> **Input:** [brief description of the search/synthesis request]
> **Output:** [brief description of results — e.g., "47 papers found across 4 databases, deduplicated to 38"]
> ```

# Literature Engine

## Data Source Priority — STRICT

1. **Academic APIs** via `scripts/academic_search.py` — ALWAYS first
   - Semantic Scholar (200M+ papers): citation graphs, TLDR, snowballing
   - OpenAlex (474M+ works): broadest coverage, German publications, CC0
   - CrossRef (150M+ works): DOI resolution, journal metadata
   - arXiv (2.4M+ preprints): CS/AI/ML cutting-edge
2. **Web search** — ONLY for: VHB-JOURQUAL rankings, specific CFPs, conference info
3. **Firecrawl** — LAST RESORT for sources without APIs (AIS eLibrary, specific repositories)

## Search Strategy

### Step 1: Query Construction

For any research topic, construct 4-6 search queries:

| Query Type | Purpose | Example (GenAI/Agents paper) |
|-----------|---------|------------------------------|
| Core English | Main topic | "generative AI enterprise implementation" |
| Synonym English | Alternative terms | "large language models organizational adoption" |
| Narrow English | Specific aspect | "autonomous AI agents business process" |
| Adjacent English | Related field | "AI transformation strategy organizational change" |
| German | German publications | "generative KI Unternehmen Implementierung" |
| Theoretical | Theory-specific | "sociotechnical systems artificial intelligence" |

### Step 2: Execute Search

```python
from scripts.academic_search import search_all, search_semantic_scholar, search_openalex, snowball, deduplicate_papers, papers_to_csv, papers_to_bibtex_file

# Round 1: Broad multi-API search
papers = search_all("generative AI enterprise implementation", 
                    max_results_per_source=20, year_from=2020)
papers += search_all("autonomous AI agents organizational", 
                     max_results_per_source=20, year_from=2020)
papers += search_all("LLM adoption business strategy", 
                     max_results_per_source=15, year_from=2022)

# Round 2: German sources via OpenAlex
papers += search_openalex("generative KI Implementierung Unternehmen", 
                          max_results=15, year_from=2020)

# Deduplicate
papers = deduplicate_papers(papers)
print(f"After dedup: {len(papers)} unique papers")
```

### Step 3: Snowball Key Papers

```python
# Sort by citations, snowball top 5
top = sorted(papers, key=lambda p: -(p.get("citation_count") or 0))[:5]
for p in top:
    if p.get("doi"):
        result = snowball(p["doi"], direction="both", limit=15)
        papers.extend(result.get("forward", []))
        papers.extend(result.get("backward", []))

# Also snowball seminal papers you know are relevant
seminal_dois = [
    # Add known seminal papers here, e.g.:
    # "10.2307/25148667",  # DeLone & McLean IS Success
]
for doi in seminal_dois:
    result = snowball(doi, direction="forward", limit=20)
    papers.extend(result.get("forward", []))

papers = deduplicate_papers(papers)
```

### Step 4: Export & Save

```python
# Save for further analysis
papers_to_csv(papers, "literature_base.csv")
papers_to_bibtex_file(papers, "references.bib")
```

## Screening

### Quick Screening (for building a paper's literature base)
Not a full SLR — just filter the most relevant papers:
- Year range appropriate? 
- Published in a reputable venue?
- Title/abstract clearly relevant to the research questions?
- Methodology aligned with what we're looking for?

### Formal SLR Screening
Use `scripts/screening.py` for systematic reviews:

```python
from scripts.screening import screen_title_abstract, save_screening_results, generate_prisma_counts

results = screen_title_abstract(
    papers=papers,
    include_keywords=["generative AI", "LLM", "AI agent", "implementation", "adoption", "organization"],
    exclude_keywords=["medical imaging", "drug discovery", "protein folding"],
    min_year=2020,
    require_abstract=True
)
save_screening_results(results, "screening/")
print(generate_prisma_counts(results))
```

### SLR Protocol Template (PRISMA-aligned)

```markdown
## Systematic Literature Review Protocol

### Research Questions
- RQ1: [Primary question]
- RQ2: [Secondary question]

### Search Strategy
- Databases: Semantic Scholar, OpenAlex, CrossRef, arXiv [+ manual: AIS eLibrary, Google Scholar]
- Search terms: [list all queries]
- Date range: [YYYY] to [YYYY]
- Language: English [+ German if applicable]

### Inclusion Criteria
- IC1: [criterion]
- IC2: [criterion]
- IC3: [criterion]

### Exclusion Criteria
- EC1: [criterion]
- EC2: [criterion]

### Quality Assessment
- [criteria: VHB B+, peer-reviewed, minimum citation threshold for older papers]

### Data Extraction Categories
- [list what to extract from each paper]

### Synthesis Method
- [Webster & Watson concept matrix / thematic synthesis / meta-analysis / vote counting]
```

## Organizing Literature: The Concept Matrix

The single most important tool for turning a pile of papers into a structured literature review
(Webster & Watson, 2002).

### How to Build One

```markdown
| Source | [Concept A] | [Concept B] | [Concept C] | [Concept D] | Method | Context |
|--------|------------|------------|------------|------------|--------|---------|
| Author1 (Year) | ✓ | ✓ | | | Survey | Enterprise |
| Author2 (Year) | | ✓ | ✓ | | Case Study | SME |
| Author3 (Year) | ✓ | | | ✓ | DSR | Healthcare |
```

### Example for the GenAI/Agents paper:

| Source | Implementation Strategy | Org. Change | Technical Architecture | Governance & Ethics | Human-AI Interaction | Method | Context |
|--------|----------------------|-------------|----------------------|-------------------|---------------------|--------|---------|
| [Author1] | ✓ | ✓ | | | | Case Study | Large Corp |
| [Author2] | | | ✓ | ✓ | | DSR | Enterprise |
| [Author3] | ✓ | | | | ✓ | Survey | Multi-industry |

### What the Matrix Tells You
- **Columns with many ✓**: Well-researched concepts → summarize, don't deep-dive
- **Columns with few ✓**: Gaps → opportunity for contribution
- **Row patterns**: Which studies are most comprehensive?
- **Method column**: What methods dominate? What's underrepresented?
- **Context column**: Which contexts are studied? Which are missing?

## Narrative Synthesis

### Turning the Concept Matrix into a Literature Review Section

For each concept (column), write one subsection:

```
[Concept Name] has received [considerable/growing/limited] attention in the literature.

[Dominant finding:] The majority of studies [find/suggest/demonstrate] that 
[main finding] (Author1, Year; Author2, Year; Author3, Year).

[Nuance/contradiction:] However, [Author4] (Year) argues that [alternative view], 
particularly in [context]. This is echoed by [Author5] (Year) who found [supporting 
evidence for the alternative].

[Your position:] These mixed findings suggest that [your interpretation]. 
In particular, [specific aspect] warrants further investigation, especially 
in the context of [your study's context].
```

## Quality Indicators for Paper Selection

### Journal Rankings (German academic context)
- **VHB-JOURQUAL 3**: A+, A, B (minimum for good lit review), C (selective)
- **AIS Senior Scholars' Basket of Eight**: EJIS, ISJ, ISR, JAIS, JIT, JMIS, JSIS, MISQ
- **ABS/AJG**: 4*, 4, 3 (secondary reference)

### For AI/GenAI Topics (fast-moving field)
- **Preprints acceptable** for very recent developments (arXiv, SSRN)
- **Industry reports** (McKinsey, Gartner, Deloitte) useful for motivation, not for theoretical claims
- **Conference papers** from ICIS, ECIS, AAAI, NeurIPS useful for cutting-edge
- **Recency premium**: For GenAI topics, 2023+ papers carry extra weight

---

## Monitoring / Living Literature Review

### Purpose
Re-run searches periodically to detect newly published papers since the last search.
Essential for fast-moving fields (AI, GenAI) and for papers with long revision cycles
where the literature base may become stale.

### When to Run
- Before submitting a paper (check for new relevant work published during writing)
- During R&R (check what appeared between submission and revision)
- For living/systematic reviews (quarterly or monthly updates)
- When user runs `/monitor-literature`

### Monitoring Workflow

#### Step 1: Recover Original Search Parameters
Load the original queries from `framing.md` or reconstruct from `literature_base.csv` metadata:
- Extract unique search queries used
- Note the original date range (the `date_to` becomes the new `date_from`)
- If no metadata exists, ask the user for the approximate last search date

#### Step 2: Execute Update Search

```python
import sys
sys.path.insert(0, "scripts")
from academic_search import search_all, deduplicate_papers, papers_to_csv
import csv
from datetime import datetime

# Load existing literature base for deduplication
existing_papers = []
with open("literature_base.csv", "r") as f:
    reader = csv.DictReader(f)
    existing_papers = list(reader)

existing_titles = {p.get("title", "").lower().strip() for p in existing_papers}
existing_dois = {p.get("doi", "").strip() for p in existing_papers if p.get("doi")}

# Re-run queries with date filter
last_search_date = "2025-01-15"  # from metadata or user input
queries = [
    "generative AI enterprise implementation",
    "autonomous AI agents organizational",
    # ... original queries from framing.md
]

new_papers = []
for q in queries:
    results = search_all(q, max_results_per_source=20, year_from=int(last_search_date[:4]))
    new_papers.extend(results)

new_papers = deduplicate_papers(new_papers)

# Filter out papers already in the literature base
truly_new = []
for p in new_papers:
    title_match = p.get("title", "").lower().strip() in existing_titles
    doi_match = p.get("doi", "").strip() in existing_dois if p.get("doi") else False
    if not title_match and not doi_match:
        truly_new.append(p)

print(f"Found {len(truly_new)} new papers since {last_search_date}")
```

#### Step 3: Present New Papers for Review

```markdown
## Literature Monitoring Report

**Last search:** [date]
**Update search:** [today's date]
**Queries re-run:** [N]
**New papers found:** [N] (after deduplication against existing [N] papers)

### Potentially Relevant New Papers

| # | Title | Authors | Year | Venue | Citations | Relevance |
|---|-------|---------|------|-------|-----------|-----------|
| 1 | [Title] | [First author et al.] | [Year] | [Venue] | [N] | [Brief note] |
| 2 | [Title] | [First author et al.] | [Year] | [Venue] | [N] | [Brief note] |
| ... | | | | | | |

### Recommended Actions
- **Add to literature base:** Papers #[list] — directly relevant to RQs
- **Read in full:** Papers #[list] — potentially important, needs assessment
- **Skip:** Papers #[list] — tangential or out of scope

→ Approve to update literature_base.csv and references.bib with selected papers.
```

#### Step 4: Update Literature Base (upon approval)

```python
# Add approved new papers to literature base
approved_papers = [truly_new[i] for i in approved_indices]
all_papers = existing_papers + approved_papers
papers_to_csv(all_papers, "literature_base.csv")
papers_to_bibtex_file(approved_papers, "references.bib", append=True)
```

### Monitoring Metadata

After each monitoring run, save metadata for future runs:

```markdown
<!-- monitoring_metadata (appended to literature_base.csv or framing.md) -->
## Search History
| Date | Queries | Results | New Added | Total |
|------|---------|---------|-----------|-------|
| [initial date] | [N] queries | [N] papers | [N] | [N] |
| [update date] | [N] queries | [N] new | [N] added | [N] |
```

### Living Review Pattern
For papers maintained over months/years:
1. Set a **monitoring schedule** (monthly for fast fields, quarterly for stable fields)
2. Each run produces a timestamped monitoring report in `outputs/monitoring_[date].md`
3. Track cumulative additions to show the literature base is current
4. Note in the paper: "The literature search was last updated on [date]"
