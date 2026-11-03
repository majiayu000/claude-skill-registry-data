---
name: literature-research
description: >
  Use when the user wants to find related work, survey a research area,
  run a literature gap analysis, or discover open-source implementations.
  Maps existing work on a topic and confirms with web search what is missing.
  Triggers on phrases like "find papers on", "related work",
  "literature review", "what papers exist", "gap analysis",
  "literature gaps", "what's missing in", "open source implementation",
  or "papers with code".
---

# Literature Research Methodology

You are helping a researcher conduct systematic literature research. Follow this methodology to ensure thorough, accurate coverage.

## Step 1: Scope Definition

Before searching:
- Clarify the exact research question or topic boundary
- Identify key terms and their synonyms (e.g., "content moderation" = "safety filtering" = "NSFW detection")
- Define inclusion/exclusion criteria (year range, venue type, methodology type)
- Ask if the user has seed papers to start from

## Step 2: Systematic Search

Use multiple search strategies in order:

### 2a. Direct Search
Use [Paper Search CLI](https://github.com/fcakyon/paper-search-cli). Follow [paper search setup](references/paper-search.md) if it is missing.

```bash
paper-search search 'object detection' -s fast -n 5
paper-search search 'object detection' -s arxiv,crossref -n 5
```

Inspect the JSON `errors` field and retain each paper's source ID and URL. Report unavailable providers rather than treating errors as an empty literature search. Vary search terms to catch different framings of the same concept. Use web search for proceedings and sources the CLI cannot access, and check Google Scholar, Semantic Scholar, and arXiv. Look for survey papers that map the area.

### 2b. Citation Chaining
From seed papers or initial results:
- **Forward chaining**: run `paper-search tool get_citing_papers <doi>`
- **Backward chaining**: run `paper-search tool get_referenced_papers <doi>`
- Both accept a DOI or OpenAlex work ID, not a title. Inspect pagination and truncation metadata. Neither command promises an exhaustive citation list. Read the paper's reference section to verify cited works.
- This catches papers that use different terminology but address the same problem

### 2c. Venue Mining
- Identify top venues for the topic (conferences, journals, workshops)
- Check recent proceedings of these venues for relevant papers
- Workshop papers often contain early-stage work not yet in main conferences

### 2d. Open Source Discovery
- Search GitHub for implementations related to the topic
- Check Papers With Code for the specific task/dataset
- Look for "awesome-X" lists curated by the community

## Step 3: Categorization

Organize found papers into a structured taxonomy:
```
| Paper | Year | Venue | Approach | Key Result | Code? | Relevance |
|-------|------|-------|----------|-----------|-------|-----------|
```

Group by methodology or approach type, not chronologically.

## Step 4: Gap Identification

Map what exists vs. what's missing:

1. **Coverage table**: one row per approach, with the problem aspects it covers:
   ```
   | Approach | Representative Papers | Coverage | Gap? |
   |----------|----------------------|----------|------|
   ```
2. **Rows marked Gap?** and aspects no approach covers = potential gaps
3. For each candidate gap:
   - Search specifically for work filling this gap (it may exist under different terms)
   - Check very recent papers (last 6 months) on arXiv that might have addressed it
   - Assess whether the gap is meaningful (would filling it advance the field?)

## Step 5: Gap Validation

For each identified gap, verify it's real:
- [ ] Searched with at least 3 different phrasings
- [ ] Checked proceedings of top-3 venues from last 2 years
- [ ] No preprint on arXiv addressing this gap
- [ ] The gap is technically feasible to address
- [ ] Filling the gap would be a meaningful contribution

Rate confidence: HIGH (every box above checked, clearly missing), MEDIUM (niche venues unchecked), LOW (limited search, gap may exist under different terminology).

## Step 6: Output Format

Produce a structured overview of the field. Title it `Gap Analysis: [Topic]` when the user asked for a gap analysis.

```
## Literature Research: [Topic]

### Research Landscape
[2-3 sentence overview of the research area]

### Paper Table
[Step 3 table: year, venue, approach, results, code availability]

### Coverage Table
[Step 4 table]

### Identified Gaps
| Gap | Confidence | Evidence of Absence | Why It Matters |
|-----|-----------|---------------------|---------------|

### Recommended Readings
[Top 5-10 most relevant papers for the user's specific work]

### Candidate Citations
[BibTeX entries for papers worth citing, verified per Citation Integrity]
```

## Citation Integrity

Verify every paper you mention with check 5 (Citations) in [paper-check](../paper-check/SKILL.md) before presenting it, including any result numbers you quote. Flag any detail you cannot confirm rather than guessing.
