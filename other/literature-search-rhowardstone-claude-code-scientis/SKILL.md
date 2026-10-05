---
name: literature-search
description: Orchestrates comprehensive literature search across multiple databases. Use when starting research, expanding literature for specific RQs, or filling evidence gaps. Implements triple-search strategy with citation expansion.
user-invocable: true
---

# Literature Search Workflow

Execute comprehensive literature search for research questions.

## ⛔ STOP - READ THIS BEFORE DOING ANYTHING ⛔

**DO NOT CALL MCP TOOLS DIRECTLY. DO NOT CALL search_openalex. DO NOT CALL search_pubmed.**

If you are about to call an MCP literature tool, STOP. You are doing it wrong.

**MANDATORY: Use the bulk Python pipeline instead.**

## WHY THIS MATTERS

Each MCP call returns ~12,000 tokens directly into your context.
5 searches × 12k tokens = 60k tokens = CONTEXT EXHAUSTION = COMPACTION = LOST WORK.

The Python pipeline runs OUTSIDE your context:
- Searches 3 databases in parallel
- Downloads PDFs in bulk
- Extracts structured sections
- Saves to JSON files
- You read only the summaries

**VIOLATION OF THIS RULE WILL CAUSE SESSION FAILURE.**

---

## CRITICAL: Token Conservation Architecture

**YOU ARE THE ORCHESTRATOR, NOT THE READER.**

The main conversation context is EXPENSIVE. Every token you consume here is money burned.

**THE POWER IS IN THE PYTHON PIPELINE, NOT MANUAL MCP CALLS.**

Craig has a bulk literature acquisition pipeline that can process 1000+ papers in ~2 hours:
- Parallel PDF downloads across multiple sources (Unpaywall, arXiv, PMC, bioRxiv, etc.)
- PyMuPDF4LLM / Marker AI for text extraction
- Structured section extraction (abstract, intro, methods, results, discussion → JSON)
- Pre-reading that lit scouts can query with `jq` instead of reading full papers

**MANDATORY WORKFLOW:**
1. Save RQs to `$SESSION_DIR/rqs.json` (goal decomposition does this)
2. Run: `./scripts/run_literature_pipeline.sh $SESSION_DIR`
3. Pipeline creates pre-read structured JSON files + `pipeline.log` with detailed progress
4. Spawn lit-scout subagents to query the structured JSON
5. Lit scouts use `jq` to extract sections, NOT read raw papers

**Note:** `$SESSION_DIR` is set by `./session.sh` for parallel-safe operation. Falls back to `workspace/current`.

**YOU MUST NOT:**
- Read full paper text in main context (15k+ tokens per paper = WASTE)
- Process paper content directly (that's what lit-scouts do)
- Do detailed evidence extraction yourself (delegate to subagents)
- Call MCP tools one-by-one for 50+ papers (use bulk pipeline instead)

## Step 1: Save Research Questions

Create `workspace/rqs.json`:
```json
{
  "research_questions": [
    {"id": "RQ1", "question": "What is the effect of X on Y?"},
    {"id": "RQ2", "question": "How does Z compare to W?"}
  ]
}
```

## Step 2: Run Bulk Literature Pipeline

**USE THE HELPER SCRIPT - IT HANDLES EVERYTHING:**

```bash
./scripts/run_literature_pipeline.sh $SESSION_DIR
```

**For long searches, run in background:**
```bash
./scripts/run_literature_pipeline.sh $SESSION_DIR --background
# Monitor: tail -f $SESSION_DIR/literature/pipeline.log
```

**DO NOT construct complex multiline bash commands.** The script handles PYTHONPATH, validation, and error reporting.

**This produces:**
- `$SESSION_DIR/literature/raw_papers.json` - All discovered papers
- `$SESSION_DIR/literature/preread_papers.json` - Papers with structured sections
- `$SESSION_DIR/literature/subsets/RQ1_papers.json` - Papers per RQ for lit scouts
- `$SESSION_DIR/literature/prisma_flow.json` - PRISMA-style counts

**JSON Schema (IMPORTANT - don't guess, use this):**
```json
// raw_papers.json and preread_papers.json structure:
{
  "papers": [           // <-- Access via data['papers'], NOT data[:10]
    {
      "doi": "10.1234/example",
      "title": "Paper title",
      "authors": ["Last, First", ...],
      "year": 2024,
      "abstract": "...",
      "source": "openalex|pubmed|semantic_scholar",
      "sections": {     // Only in preread_papers.json
        "abstract": "...",
        "introduction": "...",
        "methods": "...",
        "results": "...",
        "discussion": "..."
      }
    }
  ],
  "paper_count": 47
}
```
**Query examples:**
```bash
jq '.paper_count' raw_papers.json                    # Get count
jq '.papers[:5] | .[].title' raw_papers.json         # First 5 titles
jq '.papers[] | select(.doi)' raw_papers.json        # Papers with DOIs
```

**Alternative: Step-by-step if you need control:**
```bash
# Set PYTHONPATH once for the session
export PYTHONPATH="$HOME/.craig:$PYTHONPATH"

# 1. Search only (replace with your actual search query)
python3 -m craig.cli.literature_pipeline search "sentence embedding retrieval" \
  --max-papers 100 \
  --output $SESSION_DIR/literature/search_results.json

# 2. Pre-read separately (bulk parallel download + extraction)
python3 -m craig.cli.literature_pipeline preread \
  $SESSION_DIR/literature/search_results.json \
  --output $SESSION_DIR/literature/preread_papers.json \
  --concurrent 10
```

## Step 3: Spawn Lit Scouts

After the pipeline completes, spawn lit-scout subagents to analyze the pre-read papers.

**The key insight:** Lit scouts DON'T read raw PDFs. They query the pre-read structured JSON with `jq`:

```bash
# Lit scout queries pre-read paper sections
jq '.papers[0].sections.results' $SESSION_DIR/literature/preread_papers.json
jq '.papers[] | select(.doi == "10.1234/abc") | .sections.methods' preread_papers.json
```

**USE THE TASK TOOL WITH THESE EXACT PARAMETERS:**

```
Task tool call:
- subagent_type: "lit-scout"
- model: "haiku"              <-- COST SAVINGS: Haiku is perfect for structured extraction
- run_in_background: true
- description: "Lit scout: [RQ theme]"
- prompt: See below
```

**Example prompt for Task tool:**
```
You are lit-scout-1, analyzing papers for RQ1.

Your data is PRE-READ - you do NOT need to download or extract PDFs.

Your assignment: $SESSION_DIR/literature/subsets/RQ1_papers.json

This file contains pre-read papers with structured sections:
- sections.abstract
- sections.introduction
- sections.methods
- sections.results
- sections.discussion
- sections.conclusion

Use `jq` to query specific sections efficiently:
  jq '.papers[0].sections.results' RQ1_papers.json
  jq '.papers[] | .title, .sections.abstract' RQ1_papers.json

For each paper, extract 2-5 claims with full provenance:
{
  "claim_text": "Specific finding",
  "source_doi": "10.xxxx/xxxxx",
  "quote": "Exact text from paper",
  "section": "results",
  "confidence": 0.9
}

Output to: $SESSION_DIR/literature/evidence/RQ1_evidence.json

Research Question to address:
- RQ1: [question text]
```

### Agent Scaling
Spawn 1-3 lit scouts depending on paper volume:
- <30 papers: 1 scout
- 30-100 papers: 2 scouts
- >100 papers: 3 scouts (max, due to concurrency limits)

**Launch agents in parallel** by making multiple Task tool calls in a single message.

## What the Pipeline Does (Under the Hood)

The `craig.cli.literature_pipeline` wraps Craig's full infrastructure:

1. **Triple Search** (per RQ):
   - Keyword searches via OpenAlex + PubMed
   - Natural language "Google the question" via Semantic Scholar embeddings
   - Citation graph expansion (forward + backward citations)

2. **Deduplication**: By DOI and title similarity

3. **Bulk PDF Acquisition** (parallel, with fallbacks):
   - Unpaywall (open access finder)
   - bioRxiv / medRxiv (preprints)
   - arXiv
   - PMC (PubMed Central)
   - Europe PMC
   - OA aggregators (CORE, BASE, DOAJ)

4. **Pre-Reading** (structured extraction):
   - PyMuPDF4LLM (optimized for LLM consumption)
   - Marker AI (AI-powered, best for scientific papers)
   - PyMuPDF / pdfplumber (fallbacks)
   - Section detection (abstract, intro, methods, results, discussion)
   - Figure/table caption extraction

5. **Caching**: PDFs cached at `~/.craig/pdf-cache/`, text cached separately

## Output Tracking

After pipeline completes, verify outputs:
```bash
ls -la $SESSION_DIR/literature/
# Expected:
#   raw_papers.json       - All discovered papers
#   preread_papers.json   - Papers with structured sections
#   prisma_flow.json      - PRISMA-style counts
#   subsets/              - Per-RQ paper subsets for lit scouts

jq '.paper_count' $SESSION_DIR/literature/raw_papers.json
jq '.successful' $SESSION_DIR/literature/preread_papers.json
```

## World Model Updates

Update world model with PRISMA-style flow:
```bash
# Read PRISMA flow from pipeline output
cat $SESSION_DIR/literature/prisma_flow.json
```

## Completion Criteria

**You have NOT completed literature search until:**
- [ ] RQs saved to `$SESSION_DIR/rqs.json`
- [ ] Bulk pipeline run: `./scripts/run_literature_pipeline.sh $SESSION_DIR`
- [ ] Pre-read papers available in `$SESSION_DIR/literature/preread_papers.json`
- [ ] Per-RQ subsets in `$SESSION_DIR/literature/subsets/`
- [ ] **Lit-scout subagents SPAWNED** via Task tool with `run_in_background: true`
- [ ] PRISMA flow tracked

**If you're calling MCP tools one-by-one for 50+ papers, you're doing it WRONG.**
**If you're reading full paper text in main context, you're doing it WRONG.**

**Use the bulk pipeline. Spawn lit-scouts. Let them query structured JSON.**
