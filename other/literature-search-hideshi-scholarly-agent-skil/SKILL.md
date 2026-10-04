---
name: literature-search
version: 1.1.1
description: Use during research planning or literature search phase to query open-access paper databases (OpenAlex, arXiv, Crossref, Semantic Scholar), discover opposing scholarly factions, and build literature matrices with contestation status
---

# Multi-Provider Literature Search Skill

## Purpose
Search open-access academic literature across configured providers (OpenAlex, arXiv, Crossref, Semantic Scholar) using [`config/literature_providers.json`](../../../config/literature_providers.json), evaluate relevance, and populate `docs/literature/literature-matrix.md` for downstream gap analysis.

## Trigger Conditions
- At the start of a new research project or thesis chapter
- When a new research question, concept, or claim requires supporting literature
- When a reviewer requests additional references on a specific topic

For diachronic papers (conceptual history, genealogy, institutional history), invoke [`diachronic-claim-typing`](../diachronic-claim-typing/SKILL.md) before API search. Channels outside these providers (classical digital libraries, J-STAGE, CiNii) are Step 3 of that skill.

## Provider Configuration
Add, enable, or disable API endpoints in `config/literature_providers.json`:

```json
{
  "default_provider": "openalex",
  "contact_email": "",
  "providers": {
    "openalex": { "name": "OpenAlex", "type": "openalex_json", "base_url": "https://api.openalex.org/works", "enabled": true },
    "arxiv": { "name": "arXiv", "type": "arxiv_atom", "base_url": "https://export.arxiv.org/api/query", "enabled": true },
    "crossref": { "name": "Crossref", "type": "crossref_json", "base_url": "https://api.crossref.org/works", "enabled": true },
    "semanticscholar": { "name": "Semantic Scholar", "type": "semanticscholar_json", "base_url": "https://api.semanticscholar.org/graph/v1/paper/search", "enabled": true }
  }
}
```

For OpenAlex / Crossref polite-pool access, pass the executor's own contact email via environment variable. Do not commit a personal address. Documentation placeholders such as `example.com` are rejected.

```bash
export SCHOLARLY_CONTACT_EMAIL="firstname.lastname@university.ac.jp"
export SEMANTIC_SCHOLAR_API_KEY="your-key"   # optional; use if you query Semantic Scholar often
```

If the value is unset, empty, or a dummy, the script exits with status 1 without sending HTTP and prints setup steps on stderr. The agent should ask the user for a real address and retry.

## Execution Steps

### Step 1: Run the Search Script
Search across all enabled providers or target a specific one:

```bash
# Search all enabled providers (Submodule: python3 .scholarly-agent-skills/scripts/search_literature.py ...)
python3 scripts/search_literature.py --query "hermeneutics AND 'large language models'" --provider all --max-results 5

# Target a specific provider (e.g., OpenAlex for broad humanities coverage)
python3 scripts/search_literature.py --query "hermeneutics" --provider openalex --max-results 5
```

> [!NOTE]
> When running inside a submodule deployment, prefix script paths with `.scholarly-agent-skills/` (e.g. `python3 .scholarly-agent-skills/scripts/search_literature.py`).

### Step 1.5: Faction Discovery

When a key claim or theory (especially one load-bearing for the thesis) is found, actively search for **opposing peer-reviewed literature** using the following methods:

1. **Refutation queries**: For claim X, run queries such as `"X" AND (critique OR criticism OR replication OR "failed to replicate" OR comment OR reply)` to find objections, replications, and comment papers.
2. **Citation networks**: Scan the citing literature of core papers (e.g., OpenAlex `cited_by`) for "Comment on" / "Reply to" / Retraction Notes / meta-analyses and systematic reviews.
3. **Retraction & correction check**: Verify that core papers are not Retracted or under an Expression of Concern (in OpenAlex, retracted works carry "RETRACTED ARTICLE" in the title). This prevents citing retracted work as established knowledge.
4. **Faction identification**: When a dispute is found, identify the representative papers and proponents of each camp and record them in the matrix's "Position / Camp" column.

> The anticipated objections in `counter-argument-tdd` rely on "imagined objections". This step excavates "real objections" from the literature, grounding reviewer-proofing, claim-tone calibration, and novelty positioning.

### Step 2: Populate the Literature Matrix
Append high-relevance results to `docs/literature/literature-matrix.md` and pass them to `literature-gap-analysis` (Literature Gap Analysis) for downstream processing.

#### Matrix Record Format (v1.1.0 extension)

Record each paper with the following columns:

```markdown
| # | Paper | Relevance | Position / Camp | Contestation Status | Relevance to This Project |
```

- **Position / Camp**: The school of thought, theoretical stance, or approach the paper belongs to (e.g., functionalist account / by-product theory; econometric camp / philological camp)
- **Contestation Status**: One of the following labels
  - `consensus`: Broadly accepted within the field
  - `replicated`: Independent replications exist
  - `contested`: Opposing peer-reviewed objections or counter-evidence exist (**must be acknowledged in the manuscript**)
  - `contradicted`: Large-scale counter-evidence or negative meta-analyses exist (**must not be cited as established fact**)
  - `retraction-watch`: Subject of retraction, correction, or Expression of Concern monitoring
  - `unknown`: Not yet investigated (default; investigate via Step 1.5 before assigning for load-bearing claims)

> The Field Disagreement axis of `claim-evidence-gate` reads this column to judge whether claim tone is warranted.

## Outputs
- Updated `docs/literature/literature-matrix.md`

