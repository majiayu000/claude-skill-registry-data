---
name: verification-engine
description: >
  Activate when the user needs to verify citations, check source accuracy,
  or validate that referenced papers actually support the claims attributed
  to them. Retrieves source abstracts and full text (for open-access papers),
  compares each citation claim against actual source content, and produces
  a structured verification report with classifications (VERIFIED, PLAUSIBLE,
  MISMATCH, UNVERIFIABLE, NOT FOUND).
---

> **Orchestration Log**: When this skill is activated, append a log entry to `outputs/orchestration_log.md`:
> ```
> ### Skill Activation: Verification Engine
> **Timestamp:** [current date/time]
> **Actor:** AI Agent (verification-engine)
> **Input:** [brief description of the verification request]
> **Output:** [brief description of results — e.g., "Verified 42 citations: 35 VERIFIED, 5 PLAUSIBLE, 2 MISMATCH"]
> ```

# Verification Engine

## Core Principle

A citation is only as good as its accuracy. This engine systematically checks whether
the papers you cite actually say what you claim they say. It fetches real source
material — abstracts at minimum, full text when available — and compares each
attribution claim against the actual content.

This addresses the dominant failure mode of LLM-generated academic writing: citation
hallucination and misattribution. Even when citations point to real papers (no
fabricated DOIs), the attributed claims may not match what the source actually says.

## When to Activate

- User says "verify citations", "check my references", "validate sources"
- Before final submission of any paper with 20+ references
- After major revisions that added new citations
- When a reviewer questions citation accuracy
- As Phase 7 in the paper-machine pipeline (optional quality gate)

---

## Step 1: Extract Citation Claims

### From LaTeX (`paper.tex`)

Scan the `.tex` file for all citation commands and extract the surrounding context:

```
\citep{key}         → parenthetical: "... as shown previously (Author, Year)."
\citet{key}         → textual: "Author (Year) demonstrated that ..."
\citeauthor{key}    → author name reference
\citeyear{key}      → year reference
```

For each citation occurrence, extract:
1. **Citation key** (the BibTeX key)
2. **Claim context** — the full sentence containing the citation, plus the preceding
   sentence if needed for meaning. This is the "attributed claim."
3. **Section** — which section of the paper contains this citation
4. **Claim type** — classify as:
   - **Specific finding** ("X found that Y increases Z by 78%") — highest verification priority
   - **General attribution** ("X surveys this space") — medium priority
   - **Methodological reference** ("following X's framework") — lower priority
   - **Existence citation** ("see X for a review") — lowest priority

### From Markdown (`draft.md`)

Same logic, but scan for `(Author, Year)` and `Author (Year)` patterns instead of
LaTeX citation commands.

### Group by Source

Multiple citations of the same paper should be grouped. One paper may be cited 5 times
with 5 different claims — each claim needs independent verification.

**Output:** A list of `{key, claim, section, claim_type, priority}` tuples.

---

## Step 2: Match to BibTeX Entries

For each citation key, look up the entry in `references.bib`:

1. Extract: `title`, `author`, `year`, `doi`, `journal`, `note`
2. If DOI exists: this is the primary lookup key for Step 3
3. If no DOI: use title + first author as search query
4. Flag any citation keys that have NO matching BibTeX entry (orphan citations)

**Output:** Enriched list with DOI and metadata for each citation.

---

## Step 3: Fetch Source Material (3-Tier Retrieval)

For each unique referenced paper (not each citation — deduplicate by BibTeX key):

### Tier A — Abstract Retrieval (always attempt)

This is the baseline. Fast, reliable, works for any paper with a DOI or indexed title.

**Strategy (try in order, stop at first success):**

1. Search Semantic Scholar by title (use `academic_search_semantic_scholar` MCP tool):
   - Set `max_results: 3` (to find best match)
   - Set full abstract retrieval to get complete abstract text
   - Semantic Scholar also provides TLDR summaries — use both
2. Search OpenAlex by title (use `academic_search_openalex` MCP tool):
   - Broader coverage (474M+ works), good for non-CS papers
   - CC0 data, reliable abstracts
3. Search CrossRef by title (use `academic_search_crossref` MCP tool):
   - Best for DOI verification
   - Abstracts sometimes available

**What you get:** Title confirmation, abstract (50-300 words), TLDR (1-2 sentences),
citation count, open access status, and PDF URL if available.

### Tier B — Full-Text Retrieval (when available)

For open-access papers, go beyond the abstract:

1. **Check for open-access PDF URL** in the API response metadata
   - Semantic Scholar: `openAccessPdf.url` field
   - OpenAlex: `open_access.oa_url` field
2. **arXiv preprints:** If DOI starts with `10.48550/arxiv.` or BibTeX key suggests arXiv,
   construct the PDF URL: `https://arxiv.org/pdf/{arxiv_id}`
3. **Fetch the PDF:**
   - Use `WebFetch` with the PDF URL to get content, OR
   - Download to `/tmp/verify_papers/{bib_key}.pdf` and use the `Read` tool
     (supports PDFs up to 100 pages)
4. **Extract relevant sections:** Don't read the entire paper. Search for:
   - The abstract (always)
   - The introduction (usually contains the paper's key claims)
   - The results/findings section (for empirical papers)
   - The conclusion

**When to use Tier B:**
- Paper is a load-bearing citation (Tier 1 priority)
- Abstract alone is insufficient to verify the specific claim
- Paper is open-access (arXiv, DOAJ, PLoS, MDPI, Frontiers, etc.)

### Tier C — Extension Point (Future)

For large-scale verification (100+ papers) or complex documents with tables/figures:

- **LlamaParse MCP:** Add `llamacloud-mcp` server to `plugin.json` for high-fidelity
  PDF parsing with table extraction and semantic chunking
- **SemTools CLI:** Install `semtools` for `parse` and `search` commands over local
  PDF collections
- **Local vector store:** Index all retrieved papers for semantic search across the
  entire reference corpus

Not implemented in v5.1.0 — documented here as the upgrade path.

---

## Step 4: Verify Claims Against Sources

For each `{claim, source_content}` pair, perform the comparison:

### Classification Rubric

| Status | Criteria | Evidence Required |
|--------|----------|-------------------|
| **VERIFIED** | Claim directly supported by source | Quote or close paraphrase found in abstract/text |
| **PLAUSIBLE** | Abstract consistent, claim reasonable | Topic match, no contradiction, but specific claim not explicit |
| **MISMATCH** | Claim contradicts or misrepresents source | Source says something different from what's attributed |
| **UNVERIFIABLE** | Couldn't access source content | No abstract found, paywalled, API returned nothing |
| **NOT FOUND** | Paper doesn't appear to exist | DOI doesn't resolve, title search returns nothing |

### Verification Process

For each citation claim:

1. **Read the claim carefully.** What exactly is being attributed to this source?
   - A specific number or statistic? → must match exactly
   - A general finding or argument? → abstract should clearly support it
   - A methodological approach? → source should describe that method
   - A classification or taxonomy? → source should contain it

2. **Read the source material.** What does the paper actually say?
   - Start with TLDR/abstract
   - For specific claims, search full text if available (Tier B)

3. **Compare.** Does the claim match the source?
   - VERIFIED: "Asai et al. found GPT-4o fabricates citations 78-90% of the time"
     → Abstract states: "Without retrieval, GPT-4o generates citations that are
     78-90% fabricated" → Direct match
   - PLAUSIBLE: "Wang et al. survey autonomous agents"
     → Abstract is about LLM-based autonomous agents → Topic matches, general claim
   - MISMATCH: "Smith et al. found productivity increased by 55%"
     → Abstract states: "14% increase in productivity" → Wrong number

4. **Record evidence.** For each classification, note:
   - The specific claim text
   - The relevant source quote (from abstract or full text)
   - Brief justification for the classification

### Batch Processing

Process citations in order of priority tier (see Prioritization Strategy below).
After completing each tier, save intermediate results to `verification_report.md`
so the user can act on critical findings immediately.

---

## Step 5: Generate Verification Report

Save to `verification_report.md` with this structure:

### Report Template

```markdown
# Citation Verification Report

**Paper:** [paper title]
**Date:** [YYYY-MM-DD]
**Total unique sources:** [N]
**Total citation instances:** [N]

## Summary

| Status | Count | % |
|--------|-------|---|
| VERIFIED | [n] | [%] |
| PLAUSIBLE | [n] | [%] |
| MISMATCH | [n] | [%] |
| UNVERIFIABLE | [n] | [%] |
| NOT FOUND | [n] | [%] |

**Source material depth:**
- Full text retrieved: [n] papers (Tier B)
- Abstract only: [n] papers (Tier A)
- No content: [n] papers

## Priority Issues

### MISMATCH — Requires Immediate Attention

#### 1. [bib_key] — [Author (Year)]
- **Section:** [where cited]
- **Claim:** "[exact sentence from paper]"
- **Source says:** "[relevant quote from abstract/text]"
- **Issue:** [what's wrong — wrong number, reversed finding, etc.]
- **Recommendation:** [how to fix]

[repeat for each mismatch]

### NOT FOUND — BibTeX Entry May Be Wrong

#### 1. [bib_key] — [Author (Year)]
- **DOI:** [doi or "none"]
- **Title searched:** "[title]"
- **Result:** [what happened — DOI doesn't resolve, no results, etc.]
- **Recommendation:** [verify manually, check DOI, etc.]

## Detailed Findings

### Section: [Section Name]

| # | Source | Claim Type | Status | Note |
|---|--------|-----------|--------|------|
| 1 | Author (Year) | Specific finding | VERIFIED | Abstract confirms |
| 2 | Author2 (Year) | General attribution | PLAUSIBLE | Topic match |
| 3 | Author3 (Year) | Specific statistic | MISMATCH | See Priority Issues |

[repeat for each section]

## Manual Review Queue

Papers that require human verification (paywalled, no abstract):

| # | Source | DOI | Why Unverifiable | Claim to Check |
|---|--------|-----|-----------------|----------------|
| 1 | Author (Year) | 10.xxx | Paywalled | "[claim]" |

## BibTeX Corrections Applied

- [bib_key]: [what was corrected — DOI added, author name fixed, etc.]

## Methodology Note

This verification used [Tier A / Tier A+B] retrieval:
- Abstracts fetched via Semantic Scholar, OpenAlex, CrossRef APIs
- Full text retrieved for [n] open-access papers
- Claims compared against source content by Claude [model version]
- Limitations: Abstract-level verification catches ~80-90% of misattributions
  but cannot verify claims that only appear in the body of paywalled papers
```

---

## Prioritization Strategy (Tiered Processing)

### Tier 1 — Load-Bearing Citations (verify first)

These citations carry the paper's core arguments. A mismatch here is a structural problem.

- Citations in the **gap statement** (Introduction) — these define the contribution
- Citations supporting **specific statistics or numbers** anywhere in the paper
- Citations in **key claims** in Discussion/Findings — the paper's main arguments
- Citations that are **attributed specific findings** (e.g., "X found that...")
- Any citation mentioned **3+ times** — it's structurally important

**Typical count:** 10-20 citations. **Target:** Verify within first pass.

### Tier 2 — Methodology and Theory Citations

These ground the paper's approach. Mismatches here undermine credibility.

- Theory citations (e.g., "Following Hutchins' distributed cognition framework...")
- Methodology references (e.g., "Adapted from Hevner's DSR guidelines...")
- Framework citations (e.g., "Autor's task-based automation framework...")

**Typical count:** 8-15 citations.

### Tier 3 — Background and Context Citations

Lower risk but still worth checking for a polished paper.

- Literature review citations ("X surveys this space")
- Context-setting references ("AI is transforming knowledge work, see X, Y, Z")
- Existence citations ("For a review, see X")

**Typical count:** remaining 20-30 citations.

### Progress Updates

After each tier, present:

```
VERIFICATION PROGRESS
Tier 1 (Load-bearing): [15/15] Complete
  VERIFIED: 11 | PLAUSIBLE: 2 | MISMATCH: 1 | UNVERIFIABLE: 1
  >> 1 mismatch found — see verification_report.md

Tier 2 (Method/Theory): [0/12] Queued
Tier 3 (Background):    [0/28] Queued

Continue to Tier 2? [proceeding unless you redirect]
```

---

## Limitations & Extension Points

### What This Engine Can Do
- Verify that cited papers exist (DOI resolution, title search)
- Confirm that general claims match source abstracts
- Catch wrong statistics, reversed findings, misattributed arguments
- Identify orphan citations (cited but not in BibTeX)
- Flag paywalled papers for manual review

### What This Engine Cannot Do
- Verify claims that only appear in the body of paywalled papers (abstract-level limit)
- Assess whether a citation is the *best* source for a claim (only whether it's *accurate*)
- Verify books, reports, or sources without DOIs/abstracts (flags as UNVERIFIABLE)
- Judge the *quality* of cited work (methodology, sample size, etc.)
- Detect missing citations (papers that *should* be cited but aren't)

### Extension Points for Future Versions

**LlamaParse Integration (Tier C retrieval):**
Add to `plugin.json` under `mcpServers`:
```json
"llamaparse": {
  "command": "npx",
  "args": ["-y", "@llamaindex/llamacloud-mcp"],
  "env": { "LLAMA_CLOUD_API_KEY": "${LLAMA_CLOUD_API_KEY}" }
}
```
This enables high-fidelity PDF parsing with table extraction for complex papers.

**SemTools CLI Integration:**
```bash
pip install semtools
sem parse /tmp/verify_papers/*.pdf --output /tmp/verify_cache/
sem search "citation hallucination rate" /tmp/verify_cache/
```
Enables CLI-level parse and search over local PDF collections.

**Automated Re-Verification:**
After fixing mismatches and recompiling, re-run verification on changed citations only
(diff-based verification).
