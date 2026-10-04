---
name: rag-quality
description: Evaluate retrieval quality from the local RAG index
triggers:
  - rag quality
  - retrieval quality
  - query scores
  - rag performance
---

# RAG Quality

Measure how well the RAG system retrieves relevant documents. Identify zero-hit queries (gaps in the corpus), low-confidence hits, and retrieval quality regressions.

## Quick quality check

Start with the weekly report:

```bash
cat ~/.claude/rag-index/weekly.md
```

This shows:
- Zero-hit query list (queries with no results above cosine 0.25)
- Stale chunk count (outdated or orphaned chunks)
- Chunk distribution by source type and repo
- Quality summary table

**The report is authoritative.** If it's >1 week old, refresh it:

```bash
cd ~/.claude/rag-index
venv/bin/python report.py
```

## Score interpretation

Cosine similarity (0.0–1.0) measures how close a result is to the query. Use this scale:

| Cosine | Meaning | Action |
|--------|---------|--------|
| <0.25 | No meaningful match — corpus has a gap | Add docs, then curate |
| 0.25–0.40 | Weak hit — system retrieved *something*, but poorly | Curate corpus or rephrase query |
| 0.40–0.55 | Borderline hit — may or may not be useful | Monitor; curate if repeated |
| >0.55 | Good hit — relevant and confident | Working as intended |

**Zero-hit threshold:** If cosine is below 0.25 for all results, the corpus does not contain knowledge for that query.

## Run a test query

```bash
cd ~/.claude/rag-index
venv/bin/python query.py "your question here" --top 5 --scope-repo all
```

**Output example:**
```
Query: how do I write a skill in forgekit?

Results:
1. path: ~/.claude/skills/adt-rag-quality/SKILL.md
   rrf: 2.85, cos: 0.73, bm25: 8.2
   snippet: "---\nname: rag-quality\ndescription: Evaluate retrieval quality..."

2. path: /Volumes/External\ HD/Desenvolvimento/forgekit/packages/catalog/catalog/skills/adt-rag/SKILL.md
   rrf: 2.12, cos: 0.61, bm25: 7.1
   snippet: "# Creating a skill\n\nSkills in forgekit..."
```

**Score meanings:**
- `rrf` = reciprocal rank fusion (combined BM25 + cosine; higher is better)
- `cos` = cosine similarity (0–1; the primary quality metric)
- `bm25` = keyword match strength (context-dependent)

## Test with scope filters

Narrow the search to specific repositories or content types:

```bash
# Query only skill docs
venv/bin/python query.py "authentication patterns" --scope skills

# Query only code from the Lucky repo
venv/bin/python query.py "async request handler" --scope code --scope-repo Lucky

# Query plans and standards
venv/bin/python query.py "project roadmap" --scope plans,standards
```

Available scopes: `code`, `claude-mem`, `commit`, `skills`, `repo-docs`, `handoffs`, `plans`, `changelog`, `standards`, `codex`, `spec`

## Identify zero-hit queries

Zero-hits signal corpus gaps. Read the weekly report:

```bash
grep -A 50 "Zero-hit queries" ~/.claude/rag-index/weekly.md
```

Example output:
```
Zero-hit queries (cosine < 0.25):
- how do I set up DI containers in the service layer? (0 results, 0.0)
- what's the async/await pattern for error handling? (0 results, 0.0)
- naming convention for internal utilities? (1 result, 0.18)
```

**Next steps for each zero-hit:**
1. Does the corpus document this topic anywhere? (use `adt-rag-inspect` to audit)
2. If not → write a short standards doc, skill, or handoff explaining the topic
3. Reindex: `build.py --incremental <new-file>`
4. Re-test the query to verify it now returns good results

## Quality metrics table

Use this checklist weekly:

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Zero-hit queries (recurring) | <5 per week | — | — |
| Avg cosine (all queries) | >0.50 | — | — |
| Stale chunks | <20 | — | — |
| Total chunks | ≥14,000 | 14,355 | ✓ |
| Skills coverage | ≥500 chunks | — | — |
| Handoffs coverage | ≥200 chunks | — | — |

Fill in "Current" by running `report.py` and checking `weekly.md`.

## Detect regressions

Compare this week's report to last week:

```bash
# Show chunk count over time
ls -lh ~/.claude/rag-index/weekly*.md

# Compare recent reports
diff <(grep "Total chunks" ~/.claude/rag-index/weekly.md | tail -1) \
     <(grep "Total chunks" ~/.claude/rag-index/weekly.2024-12-20.md | tail -1)
```

If chunk count dropped >5%, a full rebuild may have failed or a source was deleted.

## Retest after improvements

After curating the corpus or reindexing, re-run the failing query:

```bash
venv/bin/python query.py "previously zero-hit question" --top 5
```

Expect cosine >0.40 after curation. If still <0.25, the added doc may not be specific enough — revise it or add more keywords.

## See also

- `adt-rag-index-rebuild` — reindex after adding/updating corpus docs
- `adt-rag-curate` — fix zero-hit gaps by adding missing documentation
- `adt-rag-coverage` — audit corpus distribution (which source types are thin)
- `adt-rag-inspect` — examine what's actually in the index
